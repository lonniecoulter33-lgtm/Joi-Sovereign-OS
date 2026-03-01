"""
modules/avatar_studio_api.py

Avatar Studio API -- Flask routes for the Wav2Lip talking-face video generator.
All R2 operations run inside Modal via modal_worker_client (no local R2 credentials).

Routes:
    POST /api/avatar_studio/upload_photo     -- Single portrait upload
    POST /api/avatar_studio/upload_photos    -- Legacy 3-photo upload
    POST /api/avatar_studio/generate         -- Start Wav2Lip video generation
    GET  /api/avatar_studio/job/<job_id>     -- Poll generation job
    GET  /api/avatar_studio/artifact         -- Download generated artifact (MP4/GLB)
    GET  /api/avatar_studio/list_versions    -- List uploaded versions
    GET  /api/avatar_studio/health           -- R2 health check
"""

from __future__ import annotations

import base64
import os
import traceback
from datetime import datetime
from flask import request as flask_req, jsonify

from flask import Response
from modules.modal_worker_client import (
    upload_photos, upload_photo, health_check, list_versions,
    start_generate, poll_generate, download_artifact,
)


# ---------------------------------------------------------------------------
# Route handlers
# ---------------------------------------------------------------------------

def upload_photo_handler():
    """POST /api/avatar_studio/upload_photo

    Accepts multipart form data:
        avatar_id  (string)  -- identifier for this avatar
        photo      (file)    -- portrait photo

    Sends to Modal for R2 upload + verification.
    """
    try:
        file_keys = list(flask_req.files.keys())
        form_keys = list(flask_req.form.keys())
        content_len = flask_req.content_length
        print(f"[AvatarStudio] POST /upload_photo  content_length={content_len}  "
              f"form_keys={form_keys}  file_keys={file_keys}")

        avatar_id = flask_req.form.get("avatar_id", "").strip()
        if not avatar_id:
            print("[AvatarStudio] REJECT: missing avatar_id")
            return jsonify({"ok": False, "error": "Missing required field: avatar_id"}), 400

        if "photo" not in flask_req.files:
            print(f"[AvatarStudio] REJECT: missing 'photo' file (received: {file_keys})")
            return jsonify({"ok": False, "error": "Missing required file: photo"}), 400

        file_obj = flask_req.files["photo"]
        photo_data = file_obj.read()
        print(f"[AvatarStudio]   photo: filename={file_obj.filename}  "
              f"size={len(photo_data)} bytes  type={file_obj.content_type}")

        if len(photo_data) == 0:
            return jsonify({"ok": False, "error": "Uploaded photo is empty"}), 400

        version = datetime.now().strftime("%Y%m%d_%H%M%S")

        print(f"[AvatarStudio] Calling Modal upload_photo  avatar_id={avatar_id}  version={version}")
        result = upload_photo(avatar_id, version, photo_data)
        print(f"[AvatarStudio] Modal result: ok={result.get('ok')}  "
              f"error={result.get('error', 'none')}")

        if result.get("ok"):
            return jsonify({
                "ok": True,
                "avatar_id": avatar_id,
                "version": version,
                "key": result.get("key", ""),
                "size": result.get("size", 0),
            })
        else:
            return jsonify({
                "ok": False,
                "error": result.get("error", "unknown")
            }), 502

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[AvatarStudio] EXCEPTION in upload_photo:\n{tb}")
        return jsonify({"ok": False, "error": str(exc), "trace": tb.split("\n")[-3:]}), 500


def upload_photos_handler():
    """POST /api/avatar_studio/upload_photos  (legacy 3-photo upload)"""
    try:
        file_keys = list(flask_req.files.keys())
        form_keys = list(flask_req.form.keys())
        content_len = flask_req.content_length
        print(f"[AvatarStudio] POST /upload_photos  content_length={content_len}  "
              f"form_keys={form_keys}  file_keys={file_keys}")

        avatar_id = flask_req.form.get("avatar_id", "").strip()
        if not avatar_id:
            return jsonify({"ok": False, "error": "Missing required field: avatar_id"}), 400

        missing = [name for name in ("front", "left", "right") if name not in flask_req.files]
        if missing:
            return jsonify({
                "ok": False,
                "error": f"Missing required image(s): {', '.join(missing)}"
            }), 400

        version = datetime.now().strftime("%Y%m%d_%H%M%S")

        images: dict[str, bytes] = {}
        for angle in ("front", "left", "right"):
            file_obj = flask_req.files[angle]
            data = file_obj.read()
            if len(data) == 0:
                return jsonify({"ok": False, "error": f"Uploaded file '{angle}' is empty"}), 400
            images[angle] = data

        result = upload_photos(avatar_id, version, images)

        if result.get("ok"):
            return jsonify({
                "ok": True,
                "avatar_id": avatar_id,
                "version": version,
                "keys": result.get("keys", {}),
            })
        else:
            return jsonify({"ok": False, "error": result.get("error", "unknown")}), 502

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[AvatarStudio] EXCEPTION in upload_photos:\n{tb}")
        return jsonify({"ok": False, "error": str(exc)}), 500


def list_versions_handler():
    """GET /api/avatar_studio/list_versions?avatar_id=..."""
    try:
        avatar_id = flask_req.args.get("avatar_id", "").strip()
        if not avatar_id:
            return jsonify({"ok": False, "error": "Missing required query param: avatar_id"}), 400

        result = list_versions(avatar_id)

        if result.get("ok"):
            return jsonify({
                "ok": True,
                "avatar_id": avatar_id,
                "versions": result.get("versions", []),
            })
        else:
            return jsonify({"ok": False, "error": result.get("error", "unknown")}), 502

    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


def health_handler():
    """GET /api/avatar_studio/health"""
    try:
        result = health_check()
        return jsonify(result)
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Generate / poll / artifact handlers
# ---------------------------------------------------------------------------

def generate_handler():
    """POST /api/avatar_studio/generate

    Body JSON: {
        "avatar_id": "...",
        "version": "..." (optional, uses latest if omitted),
        "audio_url": "/file/project/assets/audio/tts_xxx.mp3" (optional),
        "audio_b64": "<base64 audio>" (optional fallback)
    }

    Either audio_url or audio_b64 must be provided.

    Returns: {"ok": true, "job_id": "...", "version": "..."}
    """
    try:
        data = flask_req.get_json(force=True, silent=True) or {}
        avatar_id = data.get("avatar_id", "").strip()
        if not avatar_id:
            return jsonify({"ok": False, "error": "Missing avatar_id"}), 400

        version = data.get("version", "").strip()

        # If no version specified, find the latest
        if not version:
            vr = list_versions(avatar_id)
            if not vr.get("ok"):
                return jsonify({
                    "ok": False,
                    "error": f"Cannot list versions: {vr.get('error', 'unknown')}"
                }), 502
            versions = vr.get("versions", [])
            if not versions:
                return jsonify({
                    "ok": False,
                    "error": f"No uploaded versions found for '{avatar_id}'. Upload a photo first."
                }), 400
            version = versions[-1]

        # Resolve audio
        audio_bytes = None

        audio_url = data.get("audio_url", "").strip()
        if audio_url:
            # Resolve local file path from URL like /file/project/assets/audio/xxx.mp3
            # The /file/project/ prefix maps to the project root
            if audio_url.startswith("/file/project/"):
                rel_path = audio_url[len("/file/project/"):]
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                abs_path = os.path.join(root, rel_path.replace("/", os.sep))
            elif audio_url.startswith("/"):
                # Try relative to project root
                root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                abs_path = os.path.join(root, audio_url.lstrip("/").replace("/", os.sep))
            else:
                abs_path = audio_url

            print(f"[AvatarStudio] Resolving audio_url={audio_url} -> {abs_path}")

            if not os.path.isfile(abs_path):
                return jsonify({
                    "ok": False,
                    "error": f"Audio file not found: {abs_path}"
                }), 400

            with open(abs_path, "rb") as f:
                audio_bytes = f.read()

            print(f"[AvatarStudio] Audio loaded: {len(audio_bytes)} bytes from {abs_path}")

        elif data.get("audio_b64"):
            audio_bytes = base64.b64decode(data["audio_b64"])
            print(f"[AvatarStudio] Audio from base64: {len(audio_bytes)} bytes")

        if not audio_bytes:
            return jsonify({
                "ok": False,
                "error": "No audio provided. Supply audio_url or audio_b64."
            }), 400

        print(f"[AvatarStudio] POST /generate  avatar_id={avatar_id}  version={version}  "
              f"audio={len(audio_bytes)} bytes")
        result = start_generate(avatar_id, version, audio_bytes=audio_bytes)
        print(f"[AvatarStudio] Generate started: {result}")

        if result.get("ok"):
            return jsonify(result)
        else:
            return jsonify(result), 502

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[AvatarStudio] EXCEPTION in generate:\n{tb}")
        return jsonify({"ok": False, "error": str(exc)}), 500


def poll_job_handler(job_id):
    """GET /api/avatar_studio/job/<job_id>"""
    try:
        result = poll_generate(job_id)
        return jsonify(result)
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[AvatarStudio] EXCEPTION in poll_job:\n{tb}")
        return jsonify({"ok": False, "error": str(exc)}), 500


def artifact_handler():
    """GET /api/avatar_studio/artifact?avatar_id=...&version=...&file=video.mp4

    Proxies the file from R2 via Modal. Returns raw bytes with correct Content-Type.
    """
    try:
        avatar_id = flask_req.args.get("avatar_id", "").strip()
        version = flask_req.args.get("version", "").strip()
        filename = flask_req.args.get("file", "").strip()

        if not avatar_id or not version or not filename:
            return jsonify({"ok": False, "error": "avatar_id, version, and file are required"}), 400

        key = f"avatars/generated/{avatar_id}/{version}/{filename}"
        print(f"[AvatarStudio] GET /artifact  key={key}")

        result = download_artifact(key)
        if not result.get("ok"):
            return jsonify({"ok": False, "error": result.get("error", "not found")}), 404

        raw = base64.b64decode(result["data_b64"])
        ct = result.get("content_type", "application/octet-stream")

        # Set correct MIME types
        if filename.endswith(".mp4"):
            ct = "video/mp4"
        elif filename.endswith(".glb"):
            ct = "model/gltf-binary"

        return Response(raw, mimetype=ct, headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "public, max-age=3600",
        })

    except Exception as exc:
        tb = traceback.format_exc()
        print(f"[AvatarStudio] EXCEPTION in artifact:\n{tb}")
        return jsonify({"ok": False, "error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------

try:
    import joi_companion

    joi_companion.register_route(
        "/api/avatar_studio/upload_photo", ["POST"],
        upload_photo_handler, "avatar_upload_photo",
    )
    joi_companion.register_route(
        "/api/avatar_studio/upload_photos", ["POST"],
        upload_photos_handler, "avatar_upload_photos",
    )
    joi_companion.register_route(
        "/api/avatar_studio/list_versions", ["GET"],
        list_versions_handler, "avatar_list_versions",
    )
    joi_companion.register_route(
        "/api/avatar_studio/health", ["GET"],
        health_handler, "avatar_health",
    )
    joi_companion.register_route(
        "/api/avatar_studio/generate", ["POST"],
        generate_handler, "avatar_generate",
    )
    joi_companion.register_route(
        "/api/avatar_studio/job/<job_id>", ["GET"],
        poll_job_handler, "avatar_poll_job",
    )
    joi_companion.register_route(
        "/api/avatar_studio/artifact", ["GET"],
        artifact_handler, "avatar_artifact",
    )

    print("[OK] Avatar Studio API -- 7 routes registered (Wav2Lip pipeline)")

except Exception as exc:
    print(f"[WARN] Avatar Studio API failed to register routes: {exc}")
