"""
modules/joi_server_guard.py

WinError 10038 Guard — Graceful Socket Shutdown Before Werkzeug Reloader Restart
==================================================================================

Problem:
  Werkzeug's watchdog-based reloader signals the child process to restart when a
  file change is detected.  While in-flight request threads are still running,
  Windows invalidates their sockets (WSAENOTSOCK = 10038).  Python then raises
  OSError(10038) from inside recv()/send(), which Werkzeug's default handler does
  NOT catch (it only catches ConnectionError and socket.timeout).  This produces a
  noisy secondary crash and occasionally a broken response to the client.

Fix (three layers):
  1. Patch WSGIRequestHandler.handle() — catch OSError[10038] and ConnectionResetError
     exactly like Werkzeug already catches ConnectionError (calls connection_dropped).
  2. Patch BaseWSGIServer.server_close() — silence the 10038 that fires when Werkzeug
     closes its own listening socket during shutdown.
  3. atexit + SIGTERM handler — gracefully shutdown() all active connections so threads
     drain before the OS nukes the fds.

This module is auto-loaded by joi_companion.load_modules() because it matches joi_*.py.
It patches Werkzeug *before* app.run() is called, so the patches are always active.
"""

from __future__ import annotations

import atexit
import os
import signal
import socket
import sys
import threading
import time
from typing import Set

# ── Active-connection tracker ─────────────────────────────────────────────────
_tracked_socks: Set[socket.socket] = set()
_track_lock = threading.Lock()
_shutting_down = threading.Event()


def _track(sock: socket.socket) -> None:
    with _track_lock:
        _tracked_socks.add(sock)


def _untrack(sock: socket.socket) -> None:
    with _track_lock:
        _tracked_socks.discard(sock)


def graceful_shutdown(timeout: float = 1.5) -> None:
    """
    Shutdown and close all tracked sockets.
    Called from atexit and SIGTERM handler so active request threads
    have a chance to drain before the reloader kills the process.
    """
    if _shutting_down.is_set():
        return
    _shutting_down.set()

    with _track_lock:
        socks = list(_tracked_socks)

    if socks:
        print(f"  [GUARD] Closing {len(socks)} active connection(s) before restart…")

    for sock in socks:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            sock.close()
        except OSError:
            pass

    with _track_lock:
        _tracked_socks.clear()

    # Brief pause so threads that read from sockets can exit their loops cleanly
    time.sleep(min(timeout, 0.4))


atexit.register(graceful_shutdown)


# ── SIGTERM handler (Werkzeug reloader sends SIGTERM to child on Windows too) ─
_orig_sigterm = signal.getsignal(signal.SIGTERM)


def _sigterm_handler(signum: int, frame) -> None:
    print("  [GUARD] SIGTERM — closing sockets before reloader restart…")
    graceful_shutdown()
    # Re-invoke original handler (usually SIG_DFL which exits)
    if callable(_orig_sigterm):
        _orig_sigterm(signum, frame)
    else:
        sys.exit(0)


try:
    signal.signal(signal.SIGTERM, _sigterm_handler)
except (OSError, ValueError):
    # signal.signal() can only be called from the main thread
    pass


# ── Layer 1: Patch WSGIRequestHandler.handle() ───────────────────────────────
try:
    from werkzeug.serving import WSGIRequestHandler as _Handler

    _orig_handle = _Handler.handle

    def _patched_handle(self: _Handler) -> None:
        """
        Extend Werkzeug's handle() to also catch:
          - OSError with winerror 10038 (WSAENOTSOCK — socket already closed by OS)
          - ConnectionResetError (client reset during restart)
        Both are treated as dropped connections, identical to how Werkzeug
        already handles ConnectionError/socket.timeout.
        """
        # Track the underlying socket so we can close it on SIGTERM
        raw_sock = getattr(self, "connection", None) or getattr(self, "request", None)
        if raw_sock is not None:
            _track(raw_sock)
        try:
            _orig_handle(self)
        except OSError as exc:
            winerr = getattr(exc, "winerror", None)
            if winerr == 10038 or isinstance(exc, ConnectionResetError):
                # Treat exactly like a dropped connection — no traceback
                self.connection_dropped(exc)
            else:
                raise
        except ConnectionResetError as exc:
            self.connection_dropped(exc)
        finally:
            if raw_sock is not None:
                _untrack(raw_sock)

    _Handler.handle = _patched_handle
    print("  [GUARD] WSGIRequestHandler.handle patched (OSError 10038 + ConnectionResetError)")

except Exception as _patch_err:
    print(f"  [GUARD] handle patch skipped: {_patch_err}")


# ── Layer 2: Patch BaseWSGIServer.server_close() ────────────────────────────
try:
    from werkzeug.serving import BaseWSGIServer as _Server

    _orig_server_close = _Server.server_close

    def _patched_server_close(self: _Server) -> None:
        """Silently absorb WinError 10038 when Werkzeug closes its own listening socket."""
        try:
            _orig_server_close(self)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 10038:
                pass  # Socket already gone — expected during reloader restart
            else:
                raise

    _Server.server_close = _patched_server_close
    print("  [GUARD] BaseWSGIServer.server_close patched (WinError 10038 on shutdown)")

except Exception as _patch_err:
    print(f"  [GUARD] server_close patch skipped: {_patch_err}")


# ── Layer 3: Suppress 10038 in Werkzeug's error logger ───────────────────────
try:
    from werkzeug.serving import WSGIRequestHandler as _Handler2

    _orig_log_error = _Handler2.log_error

    def _patched_log_error(self, fmt: str, *args) -> None:
        """Don't flood logs with expected socket-closed noise during restart."""
        joined = " ".join(str(a) for a in args)
        if "10038" in joined or "WinError" in joined and "10038" in joined:
            return
        _orig_log_error(self, fmt, *args)

    _Handler2.log_error = _patched_log_error

except Exception:
    pass


# ── Flask teardown: catch ConnectionResetError in request context ─────────────
try:
    from modules.core.runtime import app

    @app.teardown_request
    def _teardown_socket_errors(exc):
        """
        If a ConnectionResetError or OSError 10038 reaches Flask's teardown
        (e.g., the response write failed after the route returned), swallow it
        gracefully instead of letting it trigger Flask's error handler and an
        unwanted 500 page.
        """
        if exc is None:
            return None
        if isinstance(exc, (ConnectionResetError, BrokenPipeError)):
            return None
        if isinstance(exc, OSError) and getattr(exc, "winerror", None) == 10038:
            return None
        return exc

    print("  [GUARD] Flask teardown_request handler registered for socket errors")

except Exception as _flask_err:
    print(f"  [GUARD] Flask teardown hook skipped: {_flask_err}")


print("    [OK] joi_server_guard (WinError 10038 protection, 3 layers + graceful shutdown)")
