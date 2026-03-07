"""
joi_context_cache.py — Gemini Context Caching (Paid Tier 1)
=============================================================
Automatically caches large prompts with the Gemini Cached Content API.
When Joi is working on a book, large codebase, or any file > 32k tokens,
she pays once to "upload" the content, then every follow-up question is
up to 90% cheaper in both cost and latency.

Configuration (via .env):
  JOI_GEMINI_CONTEXT_CACHE=1         # 1 = enabled, 0 = disabled
  JOI_GEMINI_CACHE_TTL=3600          # Cache lifetime in seconds (default 1hr)
  JOI_GEMINI_CACHE_MIN_TOKENS=32768  # Only cache prompts larger than this

Usage:
  from modules.joi_context_cache import maybe_cache_content, release_cache
  cached_name = maybe_cache_content(client, model, large_text)
  # pass cached_name to generate_content as cached_content=cached_name

  # When done with a project:
  release_cache(cached_name)
"""

import os
import time
import hashlib
import datetime
import threading
from typing import Optional, Dict, Any

# ── Config from env ───────────────────────────────────────────────────────────
CACHE_ENABLED      = os.getenv("JOI_GEMINI_CONTEXT_CACHE", "1").strip() == "1"
CACHE_TTL_SECS     = int(os.getenv("JOI_GEMINI_CACHE_TTL", "3600"))
CACHE_MIN_TOKENS   = int(os.getenv("JOI_GEMINI_CACHE_MIN_TOKENS", "32768"))

# Rough chars-per-token estimate for size check (Google uses ~4 chars/token for English)
_CHARS_PER_TOKEN   = 4
CACHE_MIN_CHARS    = CACHE_MIN_TOKENS * _CHARS_PER_TOKEN  # ~131k chars ≈ 32k tokens

# ── In-memory registry ────────────────────────────────────────────────────────
# Maps content_hash -> {name, expires_at, model, created_at}
_cache_registry: Dict[str, Dict[str, Any]] = {}
_registry_lock  = threading.Lock()


def _content_hash(text: str) -> str:
    """SHA-256 fingerprint of the content — reuse cache for identical content."""
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:32]


def _is_expired(entry: Dict[str, Any]) -> bool:
    return time.time() > entry["expires_at"]


def maybe_cache_content(
    client,
    model: str,
    content: str,
    display_name: str = "Joi_Project_Memory",
    force: bool = False,
) -> Optional[str]:
    """
    Creates or reuses a Gemini Cached Content for `content`.

    Returns the cache resource name (e.g. 'cachedContents/abc123') to pass
    as `cached_content=` in a generate_content call, or None if:
      - caching is disabled
      - content is below the min-token threshold
      - the SDK call fails (graceful fallback to uncached)

    Args:
        client:       The google.genai Client instance.
        model:        Gemini model name (must match what will call generate_content).
        content:      The large text to cache (system prompt + docs + files etc.)
        display_name: Human-readable label in Google AI Studio.
        force:        Cache regardless of size threshold (e.g., for explicit 'Deep Context' mode).
    """
    if not CACHE_ENABLED:
        return None

    content_len = len(content)
    if not force and content_len < CACHE_MIN_CHARS:
        return None  # Below threshold — not worth caching

    key = _content_hash(content)

    # Check in-memory registry first — avoid re-creating existing live caches
    with _registry_lock:
        if key in _cache_registry:
            entry = _cache_registry[key]
            if not _is_expired(entry) and entry.get("model") == model:
                print(f"  [CACHE] Reusing Gemini cache '{entry['name']}' "
                      f"(~{content_len // 1000}k chars, expires in "
                      f"{int((entry['expires_at'] - time.time()) / 60)}min)")
                return entry["name"]
            else:
                # Expired or wrong model — remove stale entry
                del _cache_registry[key]

    # Create new cache via Gemini API
    try:
        from google import genai
        from google.genai import types

        ttl = datetime.timedelta(seconds=CACHE_TTL_SECS)

        cache = client.caches.create(
            model=model,
            config=types.CreateCachedContentConfig(
                display_name=display_name,
                contents=[types.Content(
                    parts=[types.Part(text=content)],
                    role="user",
                )],
                ttl=ttl,
            ),
        )

        cache_name = cache.name
        expires_at = time.time() + CACHE_TTL_SECS

        with _registry_lock:
            _cache_registry[key] = {
                "name":       cache_name,
                "model":      model,
                "expires_at": expires_at,
                "created_at": time.time(),
                "chars":      content_len,
            }

        print(f"  [CACHE] Created Gemini context cache '{cache_name}' "
              f"(~{content_len // 1000}k chars, TTL={CACHE_TTL_SECS // 3600}hr). "
              f"Future calls save up to 90% on this content.")
        return cache_name

    except Exception as e:
        # Graceful fallback — caching failed but Joi should still work uncached
        print(f"  [CACHE] Could not create context cache ({type(e).__name__}: {e}). "
              f"Proceeding uncached.")
        return None


def release_cache(cache_name: Optional[str], client=None) -> bool:
    """
    Explicitly deletes a cached content resource (e.g., when a project session ends).
    Also removes it from the in-memory registry.

    Returns True if deleted from API, False otherwise.
    """
    if not cache_name:
        return False

    # Remove from registry
    with _registry_lock:
        to_remove = [k for k, v in _cache_registry.items() if v.get("name") == cache_name]
        for k in to_remove:
            del _cache_registry[k]

    # Delete from Gemini API if client provided
    if client is not None:
        try:
            client.caches.delete(name=cache_name)
            print(f"  [CACHE] Released Gemini context cache '{cache_name}'.")
            return True
        except Exception as e:
            print(f"  [CACHE] Could not delete cache '{cache_name}': {e}")
    return False


def purge_expired_caches(client=None) -> int:
    """
    Removes all expired entries from the in-memory registry.
    Optionally also calls the API to delete them server-side.
    Returns the number of entries purged.
    """
    now = time.time()
    purged = 0
    with _registry_lock:
        expired_keys = [k for k, v in _cache_registry.items() if now > v["expires_at"]]
        for k in expired_keys:
            entry = _cache_registry.pop(k)
            if client is not None:
                try:
                    client.caches.delete(name=entry["name"])
                except Exception:
                    pass
            purged += 1
    if purged:
        print(f"  [CACHE] Purged {purged} expired Gemini context cache(s).")
    return purged


def get_cache_status() -> Dict[str, Any]:
    """Returns a summary of all active caches for diagnostics / HUD display."""
    now = time.time()
    with _registry_lock:
        active = [
            {
                "name":       v["name"],
                "model":      v["model"],
                "chars":      v["chars"],
                "expires_in": f"{max(0, int((v['expires_at'] - now) / 60))}min",
                "created":    datetime.datetime.fromtimestamp(v["created_at"]).strftime("%H:%M:%S"),
            }
            for v in _cache_registry.values()
            if now <= v["expires_at"]
        ]
    return {
        "enabled":      CACHE_ENABLED,
        "min_tokens":   CACHE_MIN_TOKENS,
        "ttl_seconds":  CACHE_TTL_SECS,
        "active_count": len(active),
        "caches":       active,
    }
