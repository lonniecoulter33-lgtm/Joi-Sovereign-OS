import sys
from pathlib import Path
sys.path.insert(0, '.')
from modules.joi_tts_kokoro import generate_speech_kokoro

try:
    print("Starting generation...")
    audio = generate_speech_kokoro("Hello, this is a test of the Kokoro text to speech system.", voice="af_heart")
    print(f"Result: {audio}")
except Exception as e:
    print(f"Exception: {e}")
