import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        
        # FIXED: Changed from 'gemini-2.5-pro' (doesn't exist) to 'gemini-1.5-flash'
        # You can also use 'gemini-1.5-pro' if you want higher quality but slower speed.
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def generate_text(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""