"""
cloud_r2_client.py - Cloudflare R2 storage client (S3-compatible via boto3)

Utility module for uploading/downloading objects to the "joi-superai" R2 bucket.
Uses lazy-init pattern: the boto3 client is created on first use, not at import time.

Environment variables required:
    R2_ACCOUNT_ID          - Cloudflare account ID
    R2_ACCESS_KEY_ID       - R2 API token access key
    R2_SECRET_ACCESS_KEY   - R2 API token secret key
"""

import os

# ---------------------------------------------------------------------------
# boto3 import guard
# ---------------------------------------------------------------------------
try:
    import boto3
    from botocore.exceptions import ClientError, BotoCoreError
    _HAS_BOTO3 = True
except ImportError:
    _HAS_BOTO3 = False
    print("[R2] WARNING: boto3 is not installed. R2 operations will be unavailable.")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BUCKET_NAME = "joi-superai"

# ---------------------------------------------------------------------------
# Lazy-init singleton
# ---------------------------------------------------------------------------
_client = None


def _get_client():
    """Return the cached boto3 S3 client, creating it on first call."""
    global _client

    if _client is not None:
        return _client

    if not _HAS_BOTO3:
        return None

    account_id = os.environ.get("R2_ACCOUNT_ID", "").strip()
    access_key = os.environ.get("R2_ACCESS_KEY_ID", "").strip()
    secret_key = os.environ.get("R2_SECRET_ACCESS_KEY", "").strip()

    if not account_id or not access_key or not secret_key:
        print("[R2] WARNING: Missing one or more R2 credentials "
              "(R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY). "
              "Client will not be initialised.")
        return None

    endpoint_url = f"https://{account_id}.r2.cloudflarestorage.com"

    print(f"[R2] Initialising client -> {endpoint_url}  bucket={BUCKET_NAME}")
    _client = boto3.client(
        "s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )
    return _client


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def upload_bytes(
    key: str,
    data: bytes,
    content_type: str = "application/octet-stream",
) -> dict:
    """Upload raw bytes to R2.

    Returns:
        {"ok": True, "key": <key>, "size": <len(data)>}  on success
        {"ok": False, "error": <message>}                 on failure
    """
    client = _get_client()
    if client is None:
        msg = "boto3 not installed" if not _HAS_BOTO3 else "R2 credentials not configured"
        print(f"[R2] upload_bytes failed: {msg}")
        return {"ok": False, "error": msg}

    try:
        client.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
        print(f"[R2] Uploaded {key} ({len(data)} bytes, {content_type})")
        return {"ok": True, "key": key, "size": len(data)}
    except (ClientError, BotoCoreError) as exc:
        error_msg = str(exc)
        print(f"[R2] upload_bytes error: {error_msg}")
        return {"ok": False, "error": error_msg}
    except Exception as exc:
        error_msg = str(exc)
        print(f"[R2] upload_bytes unexpected error: {error_msg}")
        return {"ok": False, "error": error_msg}


def download_bytes(key: str) -> bytes:
    """Download an object from R2 and return raw bytes.

    Returns:
        bytes on success, or b"" if the client is unavailable / an error occurs.
    """
    client = _get_client()
    if client is None:
        msg = "boto3 not installed" if not _HAS_BOTO3 else "R2 credentials not configured"
        print(f"[R2] download_bytes failed: {msg}")
        return b""

    try:
        response = client.get_object(Bucket=BUCKET_NAME, Key=key)
        data = response["Body"].read()
        print(f"[R2] Downloaded {key} ({len(data)} bytes)")
        return data
    except (ClientError, BotoCoreError) as exc:
        print(f"[R2] download_bytes error: {exc}")
        return b""
    except Exception as exc:
        print(f"[R2] download_bytes unexpected error: {exc}")
        return b""


def list_prefix(prefix: str) -> list:
    """List all object keys under *prefix* in the bucket.

    Returns:
        List of key strings, or an empty list on failure.
    """
    client = _get_client()
    if client is None:
        msg = "boto3 not installed" if not _HAS_BOTO3 else "R2 credentials not configured"
        print(f"[R2] list_prefix failed: {msg}")
        return []

    keys: list[str] = []
    try:
        paginator = client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
            for obj in page.get("Contents", []):
                keys.append(obj["Key"])
        print(f"[R2] list_prefix('{prefix}') -> {len(keys)} key(s)")
        return keys
    except (ClientError, BotoCoreError) as exc:
        print(f"[R2] list_prefix error: {exc}")
        return []
    except Exception as exc:
        print(f"[R2] list_prefix unexpected error: {exc}")
        return []


def health_check() -> dict:
    """Quick connectivity check: try listing the 'avatars/' prefix.

    Returns:
        {"ok": True}                  on success
        {"ok": False, "error": ...}   on failure
    """
    client = _get_client()
    if client is None:
        msg = "boto3 not installed" if not _HAS_BOTO3 else "R2 credentials not configured"
        print(f"[R2] health_check failed: {msg}")
        return {"ok": False, "error": msg}

    try:
        client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="avatars/", MaxKeys=1)
        print("[R2] health_check OK")
        return {"ok": True}
    except (ClientError, BotoCoreError) as exc:
        error_msg = str(exc)
        print(f"[R2] health_check error: {error_msg}")
        return {"ok": False, "error": error_msg}
    except Exception as exc:
        error_msg = str(exc)
        print(f"[R2] health_check unexpected error: {error_msg}")
        return {"ok": False, "error": error_msg}
