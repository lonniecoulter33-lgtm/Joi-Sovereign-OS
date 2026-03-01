r"""
test_generate_avatar.py -- End-to-end test for Avatar Studio v1 (3D generation)

Usage:
    1. Deploy Modal app:   modal deploy cloud_workers/avatar_studio/modal_avatar_generate.py
    2. Start Joi server:   python joi_companion.py
    3. Run this test:      python tools/test_generate_avatar.py

Requires:
    - Joi server running on http://localhost:5000
    - Modal app 'joi-avatar-studio' deployed with GPU function
    - requests library: pip install requests
    - No local R2 credentials needed

What it does:
    1. Checks health
    2. Uploads 3 dummy test images (or reuses existing version)
    3. Starts avatar generation via POST /api/avatar_studio/generate
    4. Polls GET /api/avatar_studio/job/<job_id> until done/error
    5. Verifies model.glb is downloadable via /api/avatar_studio/artifact
"""

import sys
import os
import json
import time

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)

BASE_URL = os.environ.get("JOI_TEST_URL", "http://localhost:5000")
AVATAR_ID = "test_avatar_v1"
POLL_INTERVAL = 5       # seconds between polls
POLL_TIMEOUT = 300      # max seconds to wait for generation
PASSED = 0
FAILED = 0


def test(name, condition, detail=""):
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  [PASS] {name}")
    else:
        FAILED += 1
        print(f"  [FAIL] {name} -- {detail}")


def main():
    global PASSED, FAILED

    print("\n" + "=" * 65)
    print("  Avatar Studio v1 — 3D Generation End-to-End Test")
    print("=" * 65 + "\n")

    # ---- 1. Health check ----
    print("--- Health Check ---")
    try:
        r = requests.get(f"{BASE_URL}/api/avatar_studio/health", timeout=30)
        d = r.json()
        test("Health endpoint OK", d.get("ok"), d.get("error", ""))
    except requests.ConnectionError:
        test("Server reachable", False, f"Cannot connect to {BASE_URL}")
        print("  Start the server: python joi_companion.py")
        return
    except Exception as e:
        test("Health check", False, str(e))
        return

    if not d.get("ok"):
        print("  R2/Modal not healthy. Aborting.\n")
        return

    # ---- 2. Upload 3 dummy images ----
    print("\n--- Upload Test Images ---")
    dummy_front = b"\x89PNG\r\n\x1a\n" + b"\x00" * 200 + b"FRONT_V1_TEST"
    dummy_left  = b"\x89PNG\r\n\x1a\n" + b"\x00" * 200 + b"LEFT_V1_TEST"
    dummy_right = b"\x89PNG\r\n\x1a\n" + b"\x00" * 200 + b"RIGHT_V1_TEST"

    files = {
        "front": ("front.jpg", dummy_front, "image/jpeg"),
        "left":  ("left.jpg",  dummy_left,  "image/jpeg"),
        "right": ("right.jpg", dummy_right, "image/jpeg"),
    }

    upload_version = None
    try:
        r = requests.post(
            f"{BASE_URL}/api/avatar_studio/upload_photos",
            files=files, data={"avatar_id": AVATAR_ID}, timeout=60,
        )
        d = r.json()
        test("Upload OK", d.get("ok"), d.get("error", ""))
        upload_version = d.get("version")
        if upload_version:
            print(f"    Version: {upload_version}")
    except Exception as e:
        test("Upload", False, str(e))

    if not upload_version:
        print("  Upload failed, trying to use existing version...")
        try:
            r = requests.get(
                f"{BASE_URL}/api/avatar_studio/list_versions",
                params={"avatar_id": AVATAR_ID}, timeout=30,
            )
            d = r.json()
            versions = d.get("versions", [])
            if versions:
                upload_version = versions[-1]
                print(f"    Using existing version: {upload_version}")
            else:
                print("  No existing versions. Cannot proceed.\n")
                return
        except Exception as e:
            print(f"  Cannot list versions: {e}\n")
            return

    # ---- 3. Start generation ----
    print("\n--- Start 3D Generation ---")
    job_id = None
    gen_version = None
    try:
        r = requests.post(
            f"{BASE_URL}/api/avatar_studio/generate",
            json={"avatar_id": AVATAR_ID, "version": upload_version},
            timeout=30,
        )
        d = r.json()
        test("Generate endpoint responds", r.status_code == 200, f"status={r.status_code}")
        test("Generate started OK", d.get("ok"), d.get("error", ""))
        job_id = d.get("job_id")
        gen_version = d.get("version")
        if job_id:
            print(f"    Job ID: {job_id}")
            print(f"    Version: {gen_version}")
    except Exception as e:
        test("Generate request", False, str(e))

    if not job_id:
        print("  No job_id returned. Cannot poll.\n")
        return

    # ---- 4. Poll until done ----
    print(f"\n--- Polling (every {POLL_INTERVAL}s, timeout {POLL_TIMEOUT}s) ---")
    start_time = time.time()
    final_result = None

    while time.time() - start_time < POLL_TIMEOUT:
        time.sleep(POLL_INTERVAL)
        elapsed = int(time.time() - start_time)
        try:
            r = requests.get(f"{BASE_URL}/api/avatar_studio/job/{job_id}", timeout=30)
            d = r.json()
            status = d.get("status", "unknown")
            print(f"    [{elapsed}s] status={status}")

            if status == "done":
                final_result = d.get("result", {})
                break
            elif status == "error":
                err = d.get("error", "unknown")
                test("Generation succeeded", False, err)
                if d.get("result", {}).get("trace"):
                    print(f"    Trace: {d['result']['trace'][-200:]}")
                return
        except Exception as e:
            print(f"    [{elapsed}s] poll error: {e}")

    if final_result is None:
        test("Generation completed within timeout", False, f">{POLL_TIMEOUT}s")
        return

    test("Generation completed", final_result.get("ok", False),
         final_result.get("error", ""))

    meta = final_result.get("meta", {})
    if meta:
        print(f"    Pipeline: {meta.get('pipeline')}")
        print(f"    Vertices: {meta.get('vertices')}")
        print(f"    Faces: {meta.get('faces')}")
        print(f"    GLB size: {meta.get('glb_size_bytes', 0)} bytes")
        print(f"    Total time: {meta.get('total_time_s')}s")
        test("Has vertices", meta.get("vertices", 0) > 0, "0 vertices")
        test("Has faces", meta.get("faces", 0) > 0, "0 faces")
        test("GLB size > 0", meta.get("glb_size_bytes", 0) > 0, "0 bytes")

    # ---- 5. Download artifact ----
    print("\n--- Download Artifact ---")
    try:
        art_url = (f"{BASE_URL}/api/avatar_studio/artifact"
                   f"?avatar_id={AVATAR_ID}&version={gen_version}&file=model.glb")
        r = requests.get(art_url, timeout=60)
        test("Artifact download (200)", r.status_code == 200, f"status={r.status_code}")
        test("Artifact has content", len(r.content) > 100,
             f"got {len(r.content)} bytes")
        ct = r.headers.get("Content-Type", "")
        test("Content-Type is GLB", "gltf" in ct or "octet" in ct, f"got {ct}")
        print(f"    Downloaded {len(r.content)} bytes, Content-Type: {ct}")
    except Exception as e:
        test("Artifact download", False, str(e))

    # ---- Summary ----
    print("\n" + "=" * 65)
    total = PASSED + FAILED
    print(f"  Results: {PASSED}/{total} passed, {FAILED} failed")
    print("=" * 65 + "\n")

    sys.exit(1 if FAILED > 0 else 0)


if __name__ == "__main__":
    main()
