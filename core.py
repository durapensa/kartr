import asyncio
from kartr.plugin_manager import PluginManager
from kartr.llm import LLMManager
from kartr.github_manager import GitHubManager

class Kartr:
    def __init__(self, debug=False):
        self.debug = debug
        self.plugin_manager = PluginManager()
        self.llm_manager = LLMManager()
        self.github_manager = GitHubManager()
        self.event_loop = asyncio.get_event_loop()

    async def process_command(self, command):
        if self.debug:
            print(f"Processing command: {command}")

        if command.startswith("llm:"):
            return await self.llm_manager.process(command[4:])
        elif command.startswith("plugin:"):
            plugin_name, plugin_command = command[7:].split(" ", 1)
            return await self.plugin_manager.execute(plugin_name, plugin_command)
        elif command.startswith("github:"):
            return await self.github_manager.process(command[7:])
        elif command == "improve":
            return await self.self_improve()
        else:
            return f"Unknown command: {command}"

    async def self_improve(self):
        issues = await self.github_manager.get_issues()
        improvements = await self.llm_manager.process(f"Analyze these GitHub issues and suggest improvements for kartr: {issues}")
        return f"Improvement suggestions based on GitHub issues:\n{improvements}"
