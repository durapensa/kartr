import asyncio
from kartr.plugin_manager import PluginManager
from kartr.llm import LLMManager

class Kartr:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.llm_manager = LLMManager()
        self.event_loop = asyncio.get_event_loop()

    async def process_command(self, command):
        # Basic command processing logic
        if command.startswith("llm:"):
            return await self.llm_manager.process(command[4:])
        elif command.startswith("plugin:"):
            plugin_name, plugin_command = command[7:].split(" ", 1)
            return await self.plugin_manager.execute(plugin_name, plugin_command)
        else:
            return f"Unknown command: {command}"
