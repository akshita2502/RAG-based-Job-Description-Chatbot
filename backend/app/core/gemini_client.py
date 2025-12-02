import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
dev_dotenv = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dev_dotenv):
    load_dotenv(dev_dotenv)

_api_key = os.environ.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

class GeminiClient:
    # UPDATED: Using 'gemini-2.5-flash' which is the current active active model.
    # If this fails, try 'gemini-1.5-flash-001' or 'gemini-pro'.
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    def __init__(self):
        if not _api_key:
            raise ValueError("❌ GEMINI_API_KEY is not set! Check your .env file.")

    def _extract_text(self, data):
        """Safely extract text from the Gemini response."""
        try:
            # Navigate the response structure: candidates -> content -> parts -> text
            return data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError):
            print(f"⚠️ Unexpected response structure: {data}")
            return "I couldn't generate an answer. Please try again."

    def generate_answer(self, prompt: str) -> str:
        url = f"{self.BASE_URL}?key={_api_key}"
        
        # Correct Payload for Gemini API (generateContent)
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        resp = None
        try:
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status() # Raises HTTPError for 4xx/5xx codes
            
            data = resp.json()
            return self._extract_text(data)
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ Google API Error: {e}")
            if resp:
                print(f"Response Body: {resp.text}")
                return f"Error communicating with AI: {resp.status_code}"
            return "Error communicating with AI"
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return "An unexpected error occurred."

gemini_client = GeminiClient()