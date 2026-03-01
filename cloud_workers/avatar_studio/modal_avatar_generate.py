"""
modal_avatar_generate.py  --  Modal serverless workers for Joi Avatar Studio

v0 functions (CPU, r2_image):
    avatar_upload_photos  -- Upload 3 photos to R2 (legacy)
    upload_single_photo   -- Upload 1 portrait photo to R2
    r2_health_check       -- Verify R2 connectivity
    r2_list_versions      -- List avatar versions in R2
    r2_download           -- Download a file from R2 (base64)

v2 functions (GPU, wav2lip_image):
    generate_wav2lip_video -- Wav2Lip lip-sync: portrait + audio -> MP4

All R2 access runs inside Modal using modal.Secret.from_name("joi-storage-secret").

To deploy:
    modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py
"""

import os
import base64

try:
    import modal

    app = modal.App("joi-avatar-studio")

    storage_secret = modal.Secret.from_name("joi-storage-secret")

    r2_image = modal.Image.debian_slim().pip_install("boto3")

    BUCKET = "joi-superai"

    def _get_r2_client():
        """Create boto3 S3 client using CLOUDFLARE_* env vars from Modal secret."""
        import boto3

        # Full endpoint URL preferred; fall back to building from account ID
        endpoint = os.environ.get("CLOUDFLARE_R2_ENDPOINT", "").strip()

        # Sanitize: some Modal secret UIs paste "S3endpointhttps://..." or similar
        if endpoint:
            idx = endpoint.find("https://")
            if idx > 0:
                endpoint = endpoint[idx:]
            endpoint = endpoint.rstrip("/")

        if not endpoint:
            account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "").strip()
            if not account_id:
                raise ValueError(
                    "Neither CLOUDFLARE_R2_ENDPOINT nor CLOUDFLARE_ACCOUNT_ID "
                    "found in Modal secret 'joi-storage-secret'"
                )
            endpoint = f"https://{account_id}.r2.cloudflarestorage.com"

        access_key = os.environ.get("CLOUDFLARE_ACCESS_KEY_ID", "").strip()
        secret_key = os.environ.get("CLOUDFLARE_SECRET_ACCESS_KEY", "").strip()

        if not access_key or not secret_key:
            raise ValueError(
                "CLOUDFLARE_ACCESS_KEY_ID or CLOUDFLARE_SECRET_ACCESS_KEY "
                "missing from Modal secret 'joi-storage-secret'"
            )

        return boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name="auto",
        )

    # ------------------------------------------------------------------
    # Upload 3 photos to R2 (legacy — kept for backward compat)
    # ------------------------------------------------------------------
    @app.function(secrets=[storage_secret], timeout=120, image=r2_image)
    def avatar_upload_photos(avatar_id: str, version: str, images_b64: dict) -> dict:
        """Upload 3 base64-encoded photos to R2 and verify round-trip.

        Args:
            avatar_id:  Unique avatar identifier.
            version:    Version string (e.g. "20260210_143022").
            images_b64: {"front": "<b64>", "left": "<b64>", "right": "<b64>"}

        Returns:
            {"ok": True, "keys": {...}, "sizes": {...}} or {"ok": False, "error": "..."}
        """
        try:
            s3 = _get_r2_client()
            keys = {}
            sizes = {}

            for angle in ("front", "left", "right"):
                b64_data = images_b64.get(angle)
                if not b64_data:
                    return {"ok": False, "error": f"Missing image data for '{angle}'"}

                image_bytes = base64.b64decode(b64_data)
                key = f"avatars/source/{avatar_id}/{version}/{angle}.jpg"

                s3.put_object(
                    Bucket=BUCKET,
                    Key=key,
                    Body=image_bytes,
                    ContentType="image/jpeg",
                )

                # Verify round-trip
                resp = s3.get_object(Bucket=BUCKET, Key=key)
                verified = resp["Body"].read()
                if len(verified) != len(image_bytes):
                    return {
                        "ok": False,
                        "error": (
                            f"Verification failed for {angle}: "
                            f"expected {len(image_bytes)} bytes, got {len(verified)}"
                        ),
                    }

                keys[angle] = key
                sizes[angle] = len(image_bytes)

            return {
                "ok": True,
                "keys": keys,
                "sizes": sizes,
                "avatar_id": avatar_id,
                "version": version,
            }
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Upload single portrait photo to R2
    # ------------------------------------------------------------------
    @app.function(secrets=[storage_secret], timeout=120, image=r2_image)
    def upload_single_photo(avatar_id: str, version: str, photo_b64: str) -> dict:
        """Upload a single base64-encoded portrait photo to R2.

        Stores at: avatars/source/{avatar_id}/{version}/portrait.jpg

        Returns:
            {"ok": True, "key": "...", "size": N} or {"ok": False, "error": "..."}
        """
        try:
            s3 = _get_r2_client()
            image_bytes = base64.b64decode(photo_b64)
            key = f"avatars/source/{avatar_id}/{version}/portrait.jpg"

            s3.put_object(
                Bucket=BUCKET,
                Key=key,
                Body=image_bytes,
                ContentType="image/jpeg",
            )

            # Verify round-trip
            resp = s3.get_object(Bucket=BUCKET, Key=key)
            verified = resp["Body"].read()
            if len(verified) != len(image_bytes):
                return {
                    "ok": False,
                    "error": (
                        f"Verification failed: expected {len(image_bytes)} "
                        f"bytes, got {len(verified)}"
                    ),
                }

            return {
                "ok": True,
                "key": key,
                "size": len(image_bytes),
                "avatar_id": avatar_id,
                "version": version,
            }
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------
    @app.function(secrets=[storage_secret], timeout=30, image=r2_image)
    def r2_health_check() -> dict:
        """Verify R2 connectivity by listing the avatars/ prefix."""
        try:
            s3 = _get_r2_client()
            s3.list_objects_v2(Bucket=BUCKET, Prefix="avatars/", MaxKeys=1)
            return {"ok": True}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # List versions
    # ------------------------------------------------------------------
    @app.function(secrets=[storage_secret], timeout=60, image=r2_image)
    def r2_list_versions(avatar_id: str) -> dict:
        """List all version strings for an avatar in R2.

        Returns:
            {"ok": True, "versions": [...]} or {"ok": False, "error": "..."}
        """
        try:
            s3 = _get_r2_client()
            prefix = f"avatars/source/{avatar_id}/"

            all_keys = []
            paginator = s3.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
                for obj in page.get("Contents", []):
                    all_keys.append(obj["Key"])

            versions = set()
            for k in all_keys:
                parts = k.split("/")
                if len(parts) >= 5:
                    versions.add(parts[3])

            return {"ok": True, "avatar_id": avatar_id, "versions": sorted(versions)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    # ------------------------------------------------------------------
    # Download file from R2 (base64 transport)
    # ------------------------------------------------------------------
    @app.function(secrets=[storage_secret], timeout=120, image=r2_image)
    def r2_download(key: str) -> dict:
        """Download a file from R2 and return base64-encoded bytes."""
        try:
            s3 = _get_r2_client()
            resp = s3.get_object(Bucket=BUCKET, Key=key)
            data = resp["Body"].read()
            ct = resp.get("ContentType", "application/octet-stream")
            return {
                "ok": True,
                "data_b64": base64.b64encode(data).decode("ascii"),
                "content_type": ct,
                "size": len(data),
            }
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    # ==================================================================
    #  V2 — GPU PIPELINE (Wav2Lip)
    # ==================================================================

    wav2lip_image = (
        modal.Image.debian_slim(python_version="3.10")
        .apt_install("libgl1-mesa-glx", "libglib2.0-0", "ffmpeg", "git", "libsndfile1")
        .run_commands(
            "pip install torch==2.1.2 torchvision==0.16.2 "
            "--index-url https://download.pytorch.org/whl/cu121"
        )
        .pip_install(
            "numpy==1.26.4",
            "opencv-python-headless==4.8.1.78",
            "librosa==0.9.2",
            "resampy",
            "scipy==1.11.4",
            "tqdm",
            "numba",
            "boto3",
        )
        .run_commands(
            # Clone Wav2Lip
            "git clone https://github.com/Rudrabha/Wav2Lip.git /opt/Wav2Lip",
            # Pre-download face detection model (s3fd) so inference doesn't need internet
            "mkdir -p /opt/Wav2Lip/face_detection/detection/sfd && "
            "python -c \""
            "import urllib.request; "
            "urllib.request.urlretrieve("
            "'https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth', "
            "'/opt/Wav2Lip/face_detection/detection/sfd/s3fd.pth'"
            ")\"",
        )
        .env({"PYTHONPATH": "/opt/Wav2Lip"})
    )

    model_cache = modal.Volume.from_name(
        "avatar-model-cache", create_if_missing=True
    )

    WAV2LIP_WEIGHT_URL = (
        "https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/"
        "_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA"
    )

    @app.function(
        secrets=[storage_secret],
        gpu="A10G",
        image=wav2lip_image,
        volumes={"/cache": model_cache},
        timeout=600,
    )
    def generate_wav2lip_video(
        avatar_id: str, version: str, audio_b64: str
    ) -> dict:
        """Generate a lip-synced MP4 video from a portrait photo + audio.

        Reads:  avatars/source/{avatar_id}/{version}/portrait.jpg  (from R2)
        Input:  audio_b64 — base64-encoded audio (MP3 or WAV)
        Writes: avatars/generated/{avatar_id}/{version}/{timestamp}.mp4
                avatars/generated/{avatar_id}/{version}/meta.json
        """
        import json
        import time
        import subprocess
        import traceback
        import tempfile

        start = time.time()

        try:
            import torch
            import cv2
            import numpy as np

            if not torch.cuda.is_available():
                return {
                    "ok": False,
                    "error": "CUDA not available — GPU pipeline requires a GPU.",
                    "avatar_id": avatar_id,
                    "version": version,
                }

            # ---- 1. Download portrait from R2 ----
            s3 = _get_r2_client()
            portrait_key = f"avatars/source/{avatar_id}/{version}/portrait.jpg"
            try:
                resp = s3.get_object(Bucket=BUCKET, Key=portrait_key)
                img_bytes = resp["Body"].read()
            except Exception as exc:
                return {
                    "ok": False,
                    "error": f"Cannot read source image {portrait_key}: {exc}",
                    "avatar_id": avatar_id,
                    "version": version,
                }

            print(f"[Wav2Lip] Portrait: {len(img_bytes)} bytes")

            # ---- 2. Decode audio, convert to WAV if needed ----
            audio_bytes = base64.b64decode(audio_b64)
            print(f"[Wav2Lip] Audio: {len(audio_bytes)} bytes")

            with tempfile.TemporaryDirectory() as tmpdir:
                portrait_path = os.path.join(tmpdir, "portrait.jpg")
                audio_input_path = os.path.join(tmpdir, "audio_input")
                audio_wav_path = os.path.join(tmpdir, "audio.wav")
                output_path = os.path.join(tmpdir, "output.mp4")

                # Write portrait
                with open(portrait_path, "wb") as f:
                    f.write(img_bytes)

                # Write audio (detect format)
                with open(audio_input_path, "wb") as f:
                    f.write(audio_bytes)

                # Convert to WAV using ffmpeg (handles MP3, M4A, OGG, etc.)
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", audio_input_path,
                    "-ar", "16000", "-ac", "1", "-f", "wav",
                    audio_wav_path,
                ]
                proc = subprocess.run(
                    ffmpeg_cmd, capture_output=True, text=True, timeout=60
                )
                if proc.returncode != 0:
                    return {
                        "ok": False,
                        "error": f"ffmpeg audio conversion failed: {proc.stderr[:500]}",
                        "avatar_id": avatar_id,
                        "version": version,
                    }
                print(f"[Wav2Lip] Audio converted to WAV")

                # ---- 3. Load Wav2Lip model ----
                checkpoint_path = "/cache/wav2lip_gan.pth"
                if not os.path.exists(checkpoint_path):
                    print("[Wav2Lip] Downloading model weights...")
                    import urllib.request

                    urls = [
                        "https://huggingface.co/Nekochu/Wav2Lip/resolve/main/wav2lip_gan.pth",
                        "https://huggingface.co/camenduru/Wav2Lip/resolve/main/checkpoints/wav2lip_gan.pth",
                        "https://huggingface.co/rippertnt/wav2lip/resolve/main/wav2lip_gan.pth",
                    ]
                    downloaded = False
                    for url in urls:
                        try:
                            print(f"[Wav2Lip] Trying: {url[:80]}...")
                            urllib.request.urlretrieve(url, checkpoint_path)
                            if os.path.exists(checkpoint_path) and os.path.getsize(checkpoint_path) > 1_000_000:
                                downloaded = True
                                break
                        except Exception as dl_exc:
                            print(f"[Wav2Lip] Download failed: {dl_exc}")
                            if os.path.exists(checkpoint_path):
                                os.remove(checkpoint_path)

                    if not downloaded:
                        return {
                            "ok": False,
                            "error": "Failed to download Wav2Lip model weights from all sources",
                            "avatar_id": avatar_id,
                            "version": version,
                        }

                    model_cache.commit()
                    print("[Wav2Lip] Model weights cached")

                weight_size = os.path.getsize(checkpoint_path)
                print(f"[Wav2Lip] Checkpoint: {weight_size} bytes")

                # ---- 4. Run Wav2Lip inference ----
                print("[Wav2Lip] Running inference...")

                wav2lip_cmd = [
                    "python", "/opt/Wav2Lip/inference.py",
                    "--checkpoint_path", checkpoint_path,
                    "--face", portrait_path,
                    "--audio", audio_wav_path,
                    "--outfile", output_path,
                    "--resize_factor", "1",
                    "--nosmooth",
                    "--pads", "0", "10", "0", "0",
                ]

                infer_proc = subprocess.run(
                    wav2lip_cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,
                    cwd="/opt/Wav2Lip",
                )

                infer_time = round(time.time() - start, 1)
                print(f"[Wav2Lip] Inference stdout: {infer_proc.stdout[-500:]}")

                if infer_proc.returncode != 0:
                    print(f"[Wav2Lip] Inference stderr: {infer_proc.stderr[-1000:]}")
                    return {
                        "ok": False,
                        "error": f"Wav2Lip inference failed (rc={infer_proc.returncode}): "
                                 f"{infer_proc.stderr[-500:]}",
                        "avatar_id": avatar_id,
                        "version": version,
                    }

                if not os.path.exists(output_path):
                    return {
                        "ok": False,
                        "error": "Wav2Lip produced no output file",
                        "avatar_id": avatar_id,
                        "version": version,
                    }

                # ---- 5. Read output and upload to R2 ----
                with open(output_path, "rb") as f:
                    mp4_bytes = f.read()

                print(f"[Wav2Lip] Output MP4: {len(mp4_bytes)} bytes")

                ts = time.strftime("%Y%m%d_%H%M%S")
                base_key = f"avatars/generated/{avatar_id}/{version}"

                mp4_key = f"{base_key}/{ts}.mp4"
                s3.put_object(
                    Bucket=BUCKET,
                    Key=mp4_key,
                    Body=mp4_bytes,
                    ContentType="video/mp4",
                )

                meta = {
                    "avatar_id": avatar_id,
                    "version": version,
                    "source_key": portrait_key,
                    "format": "mp4",
                    "mp4_size_bytes": len(mp4_bytes),
                    "audio_size_bytes": len(audio_bytes),
                    "inference_time_s": infer_time,
                    "total_time_s": round(time.time() - start, 1),
                    "pipeline": "Wav2Lip",
                    "gpu": "A10G",
                    "timestamp": ts,
                }

                meta_key = f"{base_key}/meta.json"
                s3.put_object(
                    Bucket=BUCKET,
                    Key=meta_key,
                    Body=json.dumps(meta, indent=2).encode(),
                    ContentType="application/json",
                )

                result_keys = {"video": mp4_key, "meta": meta_key}

                model_cache.commit()

                print(f"[Wav2Lip] Done in {meta['total_time_s']}s  keys={result_keys}")
                return {
                    "ok": True,
                    "avatar_id": avatar_id,
                    "version": version,
                    "keys": result_keys,
                    "meta": meta,
                }

        except Exception as exc:
            tb = traceback.format_exc()
            print(f"[Wav2Lip] FAILED: {exc}\n{tb}")
            return {
                "ok": False,
                "error": str(exc),
                "trace": tb,
                "avatar_id": avatar_id,
                "version": version,
            }

except ImportError:
    # modal is not installed — define no-ops so the file can be imported safely
    app = None

    def avatar_upload_photos(avatar_id, version, images_b64):
        return {"ok": False, "error": "modal package is not installed"}

    def upload_single_photo(avatar_id, version, photo_b64):
        return {"ok": False, "error": "modal package is not installed"}

    def r2_health_check():
        return {"ok": False, "error": "modal package is not installed"}

    def r2_list_versions(avatar_id):
        return {"ok": False, "error": "modal package is not installed"}

    def generate_wav2lip_video(avatar_id, version, audio_b64):
        return {"ok": False, "error": "modal package is not installed"}

    def r2_download(key):
        return {"ok": False, "error": "modal package is not installed"}
