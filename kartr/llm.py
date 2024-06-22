import os
import json
import aiohttp
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def process(self, prompt):
        try:
            return await self.process_ollama(prompt)
        except Exception as e:
            print(f"Ollama error: {e}. Falling back to Claude-3.")
            return await self.process_claude(prompt)

    async def process_ollama(self, prompt):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.ollama_url, json={"prompt": prompt, "model": "llama2"}) as response:
                if response.status == 200:
                    full_response = ""
                    async for line in response.content:
                        if line:
                            data = json.loads(line)
                            if 'response' in data:
                                full_response += data['response']
                    return full_response
                else:
                    raise Exception(f"Ollama API error: {response.status}")

    async def process_claude(self, prompt):
        try:
            message = await self.anthropic_client.completions.create(
                model="claude-3-sonnet-20240229",
                max_tokens_to_sample=1000,
                prompt=f"Human: {prompt}\n\nAssistant:"
            )
            return message.completion
        except Exception as e:
            return f"Error processing with Claude: {str(e)}"
