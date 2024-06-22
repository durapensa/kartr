import aiohttp

class LLMManager:
    def __init__(self):
        self.api_url = "http://localhost:11434/api/generate"  # Ollama API URL

    async def process(self, prompt):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json={"prompt": prompt, "model": "llama2"}) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['response']
                else:
                    return f"Error processing LLM request: {response.status}"
