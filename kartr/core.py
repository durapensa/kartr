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
            return await self.handle_unknown_command(command)

    async def handle_unknown_command(self, command):
        prompt = f"""
        The user has entered the following command in kartr: "{command}"
        Kartr is an AI-driven development environment with the following features:
        - Local-first LLM processing with API fallback
        - Git-based version control and context management
        - Modular plugin architecture
        - Natural language programming and workflow definition
        - Web-based monitoring, control, and visualization
        - CLI interface for rapid interaction

        Please provide guidance on how to use kartr effectively, suggesting relevant commands or actions based on the user's input. If the input doesn't match any specific feature, provide general tips on using kartr for AI-driven development.
        """
        return await self.llm_manager.process(prompt)
