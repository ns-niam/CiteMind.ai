"""List all Gemini models available to your API key."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import google.generativeai as genai
from src.utils.config import config

genai.configure(api_key=config.GOOGLE_API_KEY)

print("=" * 60)
print("Available Gemini Models for generateContent:")
print("=" * 60)
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(f"  ✅ {m.name}")
print("=" * 60)