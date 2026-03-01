"""
scripts/benchmark_performance.py
================================
Headless latency benchmark for Joi companion.

Sends 5 "casual" and 5 "complex math" messages to the local joi_companion
with X-Benchmark: 1, then reports:
  - Time to response (response_time_ms from server)
  - Whether use_heavy_reasoning was toggled correctly (False for casual, True for complex)

Usage:
  Ensure server is running: python joi_companion.py
  Run: python scripts/benchmark_performance.py
"""

import os
import sys
import time

# Allow importing from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────────
BASE_URL = os.getenv("JOI_BENCHMARK_URL", "http://127.0.0.1:5001")
PASSWORD = os.getenv("JOI_PASSWORD", "joi2049")
CASUAL_MESSAGES = [
    "Hey, what's up?",
    "How's it going?",
    "Good morning!",
    "Quick hi",
    "You there?",
]
COMPLEX_MATH_MESSAGES = [
    "Solve step by step: (2^10 - 1) / 17 and prove it's an integer.",
    "Find the smallest n such that n! is divisible by 2^20. Show reasoning.",
    "Prove that the sum 1 + 2 + ... + n = n(n+1)/2 using induction.",
    "What is the GCD of 12345 and 67890? Show the Euclidean algorithm steps.",
    "How many ways can you partition 7 into positive integers? List and count.",
]
BENCHMARK_HEADERS = {"X-Benchmark": "1", "Content-Type": "application/json"}


def login(session: requests.Session) -> bool:
    r = session.post(
        f"{BASE_URL}/login",
        json={"password": PASSWORD},
        timeout=10,
    )
    if r.status_code != 200 or not r.json().get("ok"):
        print(f"Login failed: {r.status_code} {r.text}")
        return False
    return True


def send_chat(session: requests.Session, message: str) -> dict:
    """POST /chat with X-Benchmark: 1. Returns parsed JSON or error dict."""
    try:
        t0 = time.perf_counter()
        r = session.post(
            f"{BASE_URL}/chat",
            json={"message": message},
            headers=BENCHMARK_HEADERS,
            timeout=120,
        )
        elapsed_wall = int((time.perf_counter() - t0) * 1000)
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        if r.status_code != 200:
            return {"ok": False, "error": f"{r.status_code} {r.text[:200]}", "response_time_ms": elapsed_wall}
        data["_wall_ms"] = elapsed_wall
        return data
    except requests.RequestException as e:
        return {"ok": False, "error": str(e), "response_time_ms": None}
    except Exception as e:
        return {"ok": False, "error": str(e), "response_time_ms": None}


def main():
    print("Joi latency benchmark")
    print(f"  Base URL: {BASE_URL}")
    print()

    session = requests.Session()
    if not login(session):
        sys.exit(1)

    results = []  # (label, message, response_time_ms, use_heavy_reasoning, routing_ok)

    for label, messages, expect_heavy in [
        ("casual", CASUAL_MESSAGES, False),
        ("complex_math", COMPLEX_MATH_MESSAGES, True),
    ]:
        for msg in messages:
            out = send_chat(session, msg)
            rt = out.get("response_time_ms") or out.get("_wall_ms")
            routing = out.get("routing") or {}
            heavy = routing.get("use_heavy_reasoning", None)
            routing_ok = heavy is expect_heavy if heavy is not None else None  # None = unknown
            results.append((label, msg[:50], rt, heavy, routing_ok))
            if not out.get("ok") and out.get("error"):
                print(f"  [WARN] {label}: {out['error'][:80]}")

    # Table
    print()
    print(f"{'Type':<12} {'Latency (ms)':>14} {'Heavy?':>8} {'OK':>4}  Message preview")
    print("-" * 70)
    casual_ok = complex_ok = 0
    casual_rt = []
    complex_rt = []
    for label, preview, rt, heavy, ok in results:
        rt_s = str(rt) if rt is not None else "N/A"
        heavy_s = "yes" if heavy else "no"
        ok_s = "yes" if ok else ("no" if ok is False else "?")
        if label == "casual":
            if ok:
                casual_ok += 1
            if rt is not None:
                casual_rt.append(rt)
        else:
            if ok:
                complex_ok += 1
            if rt is not None:
                complex_rt.append(rt)
        print(f"{label:<12} {rt_s:>14} {heavy_s:>8} {ok_s:>4}  {preview}")

    print("-" * 70)
    avg_casual = sum(casual_rt) / len(casual_rt) if casual_rt else None
    avg_complex = sum(complex_rt) / len(complex_rt) if complex_rt else None
    if avg_casual is not None:
        print(f"Casual avg latency: {avg_casual:.0f} ms  (routing OK: {casual_ok}/{len(CASUAL_MESSAGES)})")
    if avg_complex is not None:
        print(f"Complex avg latency: {avg_complex:.0f} ms  (routing OK: {complex_ok}/{len(COMPLEX_MATH_MESSAGES)})")
    print()
    if casual_ok == len(CASUAL_MESSAGES) and complex_ok == len(COMPLEX_MATH_MESSAGES):
        print("PASS: use_heavy_reasoning was correctly toggled for all messages.")
    else:
        print("FAIL: some messages had unexpected routing (casual should be light, complex should be heavy).")
    return 0 if (casual_ok == len(CASUAL_MESSAGES) and complex_ok == len(COMPLEX_MATH_MESSAGES)) else 1


if __name__ == "__main__":
    sys.exit(main())
