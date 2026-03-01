import os
from dotenv import load_dotenv
import requests

load_dotenv()

def check_connections():
    print("--- Joi Connection Check ---")
    
    # 1. Check LM Studio
    try:
        lm_resp = requests.get("http://localhost:1234/v1/models", timeout=2)
        print("✅ LM Studio: Connected!")
    except:
        print("❌ LM Studio: Not found. (Is the server running on port 1234?)")

    # 2. Check Gemini Key
    key = os.getenv("GEMINI_API_KEY")
    if key and len(key) > 10:
        print(f"✅ Gemini API Key: Found (Ends in ...{key[-4:]})")
    else:
        print("❌ Gemini API Key: Missing or too short in .env file")

if __name__ == "__main__":
    check_connections()