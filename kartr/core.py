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

        command = command.strip()
        lower_command = command.lower()
    
        if lower_command == "help":
            return self.get_help_text()
        elif lower_command == "web":
            return "Starting web UI... (This message is a placeholder. The actual web UI start is handled in the CLI class.)"
        elif lower_command.startswith("llm:"):
            return await self.llm_manager.process(command[4:].strip())
        elif lower_command.startswith("plugin:"):
            plugin_name, plugin_command = command[7:].split(" ", 1)
            return await self.plugin_manager.execute(plugin_name, plugin_command)
        elif lower_command.startswith("github:"):
            return await self.github_manager.process(command[7:])
        elif lower_command == "improve":
            return await self.self_improve()
        else:
            return await self.handle_unknown_command(command)

    def get_help_text(self):
        return """
        Available commands:
        - help: Show this help message
        - web: Start the web UI
        - llm:<prompt>: Send a prompt to the LLM
        - plugin:<name> <command>: Execute a plugin command
        - github:issues: Fetch GitHub issues
        - improve: Get improvement suggestions based on GitHub issues
        - exit: Quit kartr
        
        For any other input, kartr will use the LLM to provide guidance and ideas.
        """

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

    async def self_improve(self):
        issues = await self.github_manager.get_issues()
        improvements = await self.llm_manager.process(f"Analyze these GitHub issues and suggest improvements for kartr: {issues}")
        return f"Improvement suggestions based on GitHub issues:\n{improvements}"
