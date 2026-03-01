"""
modal_worker_client.py  --  Client for calling Modal workers remotely.

Uses modal.Function.from_name() to reference deployed Modal functions.
Requires: modal package installed locally + authenticated (modal token set).
Does NOT require any R2/Cloudflare credentials locally.

All R2 operations happen inside Modal using the 'joi-storage-secret' secret.
"""

import base64
import threading
import uuid

_HAS_MODAL = False
_MODAL_VERSION = "not installed"
try:
    import modal
    _HAS_MODAL = True
    _MODAL_VERSION = getattr(modal, "__version__", "unknown")
except ImportError:
    pass

APP_NAME = "joi-avatar-studio"


def _get_fn(fn_name):
    """Return a lazy reference to a deployed Modal function.

    modal >= 1.0 uses Function.from_name() (lazy -- only errors on .remote()).
    """
    if not _HAS_MODAL:
        return None
    try:
        return modal.Function.from_name(APP_NAME, fn_name)
    except Exception as exc:
        print(f"[Modal] from_name({APP_NAME}::{fn_name}) failed: {exc}")
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def upload_photos(avatar_id: str, version: str, images: dict) -> dict:
    """Upload 3 photos to R2 via Modal (legacy).

    Args:
        avatar_id: Avatar identifier.
        version:   Version string.
        images:    {"front": <bytes>, "left": <bytes>, "right": <bytes>}

    Returns:
        Result dict from Modal function.
    """
    fn = _get_fn("avatar_upload_photos")
    if fn is None:
        return {"ok": False, "error": "Modal not available or function not deployed"}

    # Base64 encode for transport to Modal
    images_b64 = {}
    for angle, data in images.items():
        images_b64[angle] = base64.b64encode(data).decode("ascii")

    try:
        return fn.remote(avatar_id=avatar_id, version=version, images_b64=images_b64)
    except Exception as exc:
        return {"ok": False, "error": f"Modal call failed: {exc}"}


def upload_photo(avatar_id: str, version: str, photo_bytes: bytes) -> dict:
    """Upload a single portrait photo to R2 via Modal.

    Args:
        avatar_id: Avatar identifier.
        version:   Version string.
        photo_bytes: Raw image bytes.

    Returns:
        Result dict from Modal function.
    """
    fn = _get_fn("upload_single_photo")
    if fn is None:
        return {"ok": False, "error": "Modal not available or upload_single_photo not deployed"}

    photo_b64 = base64.b64encode(photo_bytes).decode("ascii")

    try:
        return fn.remote(avatar_id=avatar_id, version=version, photo_b64=photo_b64)
    except Exception as exc:
        return {"ok": False, "error": f"Modal call failed: {exc}"}


def health_check() -> dict:
    """Check R2 connectivity via Modal."""
    fn = _get_fn("r2_health_check")
    if fn is None:
        return {"ok": False, "error": "Modal not available or function not deployed"}

    try:
        return fn.remote()
    except Exception as exc:
        return {"ok": False, "error": f"Modal call failed: {exc}"}


def list_versions(avatar_id: str) -> dict:
    """List avatar versions in R2 via Modal."""
    fn = _get_fn("r2_list_versions")
    if fn is None:
        return {"ok": False, "error": "Modal not available or function not deployed"}

    try:
        return fn.remote(avatar_id=avatar_id)
    except Exception as exc:
        return {"ok": False, "error": f"Modal call failed: {exc}"}


def poll_job(job_id: str) -> dict:
    """Poll job status (not yet implemented)."""
    return {"ok": False, "status": "not_implemented", "job_id": job_id}


# ---------------------------------------------------------------------------
# Async generate job management
# ---------------------------------------------------------------------------

_jobs: dict = {}        # job_id -> {status, avatar_id, version, result?, error?}
_jobs_lock = threading.Lock()


def start_generate(avatar_id: str, version: str, audio_bytes: bytes = None) -> dict:
    """Start async Wav2Lip video generation on Modal GPU. Returns job_id for polling.

    Args:
        avatar_id: Avatar identifier.
        version:   Version string.
        audio_bytes: Raw audio bytes (MP3 or WAV). Required for Wav2Lip.
    """
    fn = _get_fn("generate_wav2lip_video")
    if fn is None:
        return {"ok": False, "error": "Modal not available or generate_wav2lip_video not deployed"}

    if not audio_bytes:
        return {"ok": False, "error": "audio_bytes is required for Wav2Lip video generation"}

    job_id = uuid.uuid4().hex[:12]
    audio_b64 = base64.b64encode(audio_bytes).decode("ascii")

    with _jobs_lock:
        _jobs[job_id] = {
            "status": "running",
            "avatar_id": avatar_id,
            "version": version,
        }

    def _run():
        try:
            print(f"[Generate] Job {job_id} calling Modal generate_wav2lip_video "
                  f"(avatar_id={avatar_id}, version={version}, "
                  f"audio={len(audio_bytes)} bytes)")
            result = fn.remote(
                avatar_id=avatar_id, version=version, audio_b64=audio_b64
            )
            with _jobs_lock:
                if result.get("ok"):
                    _jobs[job_id] = {
                        "status": "done",
                        "avatar_id": avatar_id,
                        "version": version,
                        "result": result,
                    }
                    print(f"[Generate] Job {job_id} DONE")
                else:
                    _jobs[job_id] = {
                        "status": "error",
                        "avatar_id": avatar_id,
                        "version": version,
                        "error": result.get("error", "unknown"),
                        "result": result,
                    }
                    print(f"[Generate] Job {job_id} FAILED: {result.get('error')}")
        except Exception as exc:
            with _jobs_lock:
                _jobs[job_id] = {
                    "status": "error",
                    "avatar_id": avatar_id,
                    "version": version,
                    "error": str(exc),
                }
            print(f"[Generate] Job {job_id} EXCEPTION: {exc}")

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

    return {"ok": True, "job_id": job_id, "avatar_id": avatar_id, "version": version}


def poll_generate(job_id: str) -> dict:
    """Poll status of an avatar generation job."""
    with _jobs_lock:
        job = _jobs.get(job_id)
    if job is None:
        return {"ok": False, "error": f"Unknown job_id: {job_id}"}
    return {"ok": True, **job}


def download_artifact(key: str) -> dict:
    """Download a file from R2 via Modal. Returns base64-encoded data."""
    fn = _get_fn("r2_download")
    if fn is None:
        return {"ok": False, "error": "Modal not available or r2_download not deployed"}

    try:
        return fn.remote(key=key)
    except Exception as exc:
        return {"ok": False, "error": f"Modal call failed: {exc}"}


print(f"[OK] Modal Worker Client loaded (modal {_MODAL_VERSION})"
      if _HAS_MODAL else
      "[OK] Modal Worker Client loaded (modal NOT installed)")
