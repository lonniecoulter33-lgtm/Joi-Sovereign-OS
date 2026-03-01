r"""
test_r2_avatar_upload.py -- End-to-end test for Avatar Studio (Modal-backed R2)

Usage:
    1. Start Joi server:  python joi_companion.py
    2. Run this test:     python tools/test_r2_avatar_upload.py

Requires:
    - Joi server running on http://localhost:5000
    - Modal app 'joi-avatar-studio' deployed with 'joi-storage-secret'
    - requests library: pip install requests
    - No local R2 credentials needed
"""

import sys
import os
import json

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

BASE_URL = os.environ.get("JOI_TEST_URL", "http://localhost:5000")
AVATAR_ID = "test_avatar"
PASSED = 0
FAILED = 0


def test(name, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name} — {detail}")


def main():
    global PASSED, FAILED

    print("\n" + "=" * 60)
    print("  Avatar Studio End-to-End Test (Modal-backed R2)")
    print("=" * 60 + "\n")

    # ---- 1. Health check ----
    print("--- Health Check ---")
    health_ok = False
    try:
        r = requests.get(f"{BASE_URL}/api/avatar_studio/health", timeout=30)
        d = r.json()
        test("Health endpoint responds (200)", r.status_code == 200,
             f"status={r.status_code}")
        test("R2 health OK via Modal", d.get("ok"), d.get("error", ""))
        health_ok = d.get("ok", False)
    except requests.ConnectionError:
        test("Server reachable", False,
             f"Cannot connect to {BASE_URL}. Is joi_companion.py running?")
        print("\n  Start the server first: python joi_companion.py")
        print("  Aborting remaining tests.\n")
        return
    except Exception as e:
        test("Health endpoint reachable", False, str(e))

    if not health_ok:
        print("\n  R2 health check failed. Possible causes:")
        print("    - Modal app not deployed: modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py")
        print("    - Modal secret missing: modal secret create joi-storage-secret CLOUDFLARE_ACCESS_KEY_ID=... ...")
        print("  Aborting remaining tests.\n")
        return

    # ---- 2. Upload 3 dummy images ----
    print("\n--- Upload Test ---")
    dummy_front = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100 + b"FRONT_TEST_DATA"
    dummy_left  = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100 + b"LEFT_TEST_DATA"
    dummy_right = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100 + b"RIGHT_TEST_DATA"

    files = {
        "front": ("front.jpg", dummy_front, "image/jpeg"),
        "left":  ("left.jpg",  dummy_left,  "image/jpeg"),
        "right": ("right.jpg", dummy_right, "image/jpeg"),
    }
    form_data = {"avatar_id": AVATAR_ID}

    upload_version = None
    try:
        r = requests.post(
            f"{BASE_URL}/api/avatar_studio/upload_photos",
            files=files, data=form_data, timeout=60,
        )
        d = r.json()
        test("Upload endpoint responds (200)", r.status_code == 200,
             f"status={r.status_code}")
        test("Upload result OK", d.get("ok"), d.get("error", ""))

        if d.get("ok"):
            upload_version = d.get("version")
            test("Version returned", bool(upload_version), "no version in response")
            keys = d.get("keys", {})
            test("3 keys returned", len(keys) == 3,
                 f"expected 3 keys, got {len(keys)}: {keys}")
            print(f"    Version: {upload_version}")
            for angle, key in keys.items():
                print(f"    {angle}: {key}")
    except Exception as e:
        test("Upload endpoint reachable", False, str(e))

    # ---- 3. List versions ----
    print("\n--- List Versions Test ---")
    try:
        r = requests.get(
            f"{BASE_URL}/api/avatar_studio/list_versions",
            params={"avatar_id": AVATAR_ID}, timeout=30,
        )
        d = r.json()
        test("List versions responds (200)", r.status_code == 200,
             f"status={r.status_code}")
        test("List versions OK", d.get("ok"), d.get("error", ""))

        versions = d.get("versions", [])
        test("At least 1 version found", len(versions) >= 1,
             f"got {len(versions)} versions")

        if upload_version:
            test(f"Uploaded version '{upload_version}' in list",
                 upload_version in versions,
                 f"versions: {versions}")

        if versions:
            print(f"    Versions: {versions}")
    except Exception as e:
        test("List versions reachable", False, str(e))

    # ---- Summary ----
    print("\n" + "=" * 60)
    total = PASSED + FAILED
    print(f"  Results: {PASSED}/{total} passed, {FAILED} failed")
    print("=" * 60 + "\n")

    sys.exit(1 if FAILED > 0 else 0)


if __name__ == "__main__":
    main()
