import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class GitHubManager:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = "durapensa/kartr"
        self.api_url = f"https://api.github.com/repos/{self.repo}"

    async def process(self, command):
        if command == "issues":
            return await self.get_issues()
        else:
            return f"Unknown GitHub command: {command}"

    async def get_issues(self):
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.api_url}/issues", headers=headers) as response:
                if response.status == 200:
                    issues = await response.json()
                    return "\n".join([f"#{issue['number']}: {issue['title']}" for issue in issues])
                else:
                    return f"Error fetching issues: {response.status}"
