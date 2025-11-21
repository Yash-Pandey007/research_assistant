import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "https://github.com/Yash-Pandey007/research_assistant", # Optional: using repo name as referer
                "X-Title": "Research Assistant", # Optional: App name
            }
        )
        self.model = "x-ai/grok-4.1-fast:free"

    async def generate_text(self, prompt: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating text: {e}")
            return ""