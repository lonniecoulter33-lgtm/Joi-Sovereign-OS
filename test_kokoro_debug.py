import sys
import logging
from pathlib import Path

sys.path.insert(0, '.')
logging.basicConfig(filename='test_kokoro_log.txt', level=logging.DEBUG)

try:
    from modules.joi_tts_kokoro import generate_speech_kokoro
    audio = generate_speech_kokoro("Testing kokoro voice. This should work.")
    logging.info(f"Result: {audio}")
except Exception as e:
    logging.error(f"Exception: {e}", exc_info=True)
