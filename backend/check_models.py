# backend/check_models.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    print("✅ Available Models:")
    for m in models:
        # Filter for models that support 'generateContent'
        if "generateContent" in m.get("supportedGenerationMethods", []):
            print(f" - {m['name']}")
else:
    print(f"❌ Error fetching models: {response.status_code} - {response.text}")