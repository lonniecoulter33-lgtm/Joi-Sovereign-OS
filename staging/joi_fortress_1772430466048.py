import os
import time
from collections import defaultdict
from flask import Blueprint, request, jsonify, abort, after_this_request

# Enable fortress_mode feature flag safely
try:
    from modules.joi import ENABLED_FEATURES
    ENABLED_FEATURES['fortress_mode'] = True
except ImportError:
    ENABLED_FEATURES = {'fortress_mode': True}

# Configuration from environment
JOI_FORTRESS_MODE = os.getenv('JOI_FORTRESS_MODE', 'false').lower() == 'true'
_allowed = os.getenv('JOI_ALLOWED_ORIGINS')
if _allowed:
    ALLOWED_ORIGINS = {o.strip() for o in _allowed.split(',') if o.strip()}
else:
    ALLOWED_ORIGINS = None

CHAT_LIMIT = int(os.getenv('JOI_RATE_LIMIT_CHAT', 20))
LOGIN_LIMIT = int(os.getenv('JOI_RATE_LIMIT_LOGIN', 5))

# In-memory rate limit store per IP
_rate_timestamps = {
    'chat': defaultdict(list),
    'login': defaultdict(list),
}

# Blueprint for fortress module
fortress = Blueprint('fortress', __name__)

@fortress.before_app_request
def _fortress_before_request():
    if not JOI_FORTRESS_MODE:
        return
    # CORS origin check for /api/*
    if request.path.startswith('/api/'):
        origin = request.headers.get('Origin')
        if ALLOWED_ORIGINS is not None and origin not in ALLOWED_ORIGINS:
            abort(403)
    # Rate limiting for /chat and /login
    ip = request.remote_addr or request.environ.get('REMOTE_ADDR')
    now = time.time()
    for key, limit, prefix in [('chat', CHAT_LIMIT, '/chat'), ('login', LOGIN_LIMIT, '/login')]:
        if request.path.startswith(prefix):
            times = _rate_timestamps[key][ip]
            times = [t for t in times if now - t < 60]
            if len(times) >= limit:
                abort(429)
            times.append(now)
            _rate_timestamps[key][ip] = times
    # Attach security headers to response
    @after_this_request
    def _set_security_headers(response):
        response.headers.setdefault('Content-Security-Policy', "default-src 'self'")
        response.headers.setdefault('X-Frame-Options', 'DENY')
        response.headers.setdefault('Referrer-Policy', 'no-referrer')
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('Cross-Origin-Opener-Policy', 'same-origin')
        response.headers.setdefault('Cross-Origin-Embedder-Policy', 'require-corp')
        secure = request.is_secure or os.getenv('JOI_FORCE_HSTS', 'false').lower() == 'true'
        if secure:
            response.headers.setdefault('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload')
        return response

@fortress.route('/status/fortress', methods=['GET'])
def _status_fortress():
    return jsonify({
        'ok': True,
        'config': {
            'enabled': JOI_FORTRESS_MODE,
            'allowed_origins': list(ALLOWED_ORIGINS) if ALLOWED_ORIGINS is not None else None,
            'chat_limit': CHAT_LIMIT,
            'login_limit': LOGIN_LIMIT,
            'force_hsts': os.getenv('JOI_FORCE_HSTS', 'false').lower() == 'true',
            'trusted_plugins': os.getenv('JOI_TRUSTED_PLUGINS')
        }
    })

# Whitelist-aware plugin loader override
from modules.plugins import load_plugin as _base_load_plugin

def load_plugin(name):
    trusted = os.getenv('JOI_TRUSTED_PLUGINS')
    if trusted:
        stems = {s.strip() for s in trusted.split(',') if s.strip()}
        if not any(name.startswith(s) for s in stems):
            raise ImportError(f"Plugin {name} not trusted")
    return _base_load_plugin(name)
