import sys
sys.path.insert(0, '.')
from modules.joi_avatar import generate_speech
from modules.joi_memory import set_preference

print("Setting legacy preference 'elevenlabs'...")
set_preference("tts_engine", "elevenlabs")

print("Generating speech...")
# Passing short text
audio = generate_speech("Testing one two three.")
print(f"Resulting audio path: {audio}")
if audio:
    print("SUCCESS: generate_speech routed to Kokoro correctly.")
else:
    print("FAIL: generate_speech returned None.")
