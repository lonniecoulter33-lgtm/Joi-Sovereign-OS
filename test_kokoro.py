import sys
import json
from flask import Flask
sys.path.insert(0, '.')
from modules.joi_tts_kokoro import kokoro_voices_route, kokoro_settings_route

app = Flask(__name__)
with app.test_request_context('/kokoro/voices', method='GET'):
    # Setup dummy session for require_user()
    from flask import request
    request.cookies = {'joi_session': 'dummy'}
    try:
        from modules import joi_memory
        # Monkeypatch require_user just for this test
        joi_memory.require_user = lambda: None
    except Exception as e:
        print("Mock err", e)

    res = kokoro_voices_route()
    print("Voices:", res.get_data(as_text=True))
