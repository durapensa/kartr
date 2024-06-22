import asyncio
import webbrowser
from kartr.web import start_web_server

class CLI:
    def __init__(self, kartr):
        self.kartr = kartr
        self.web_url = None

    async def run(self):
        print("Welcome to kartr! Type 'help' for available commands.")
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, input, "kartr> ")
            if command.lower() == 'exit':
                break
            elif command.lower() == 'help':
                await self.show_help()
            elif command.lower() == 'web':
                await self.start_web_ui()
            else:
                result = await self.kartr.process_command(command)
                print(result)

    async def show_help(self):
        help_text = """
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
        print(help_text)

    async def start_web_ui(self):
        if not self.web_url:
            try:
                self.web_url = await start_web_server(self.kartr)
                print(f"Web UI is running at: {self.web_url}")
                webbrowser.open(self.web_url)
            except Exception as e:
                print(f"Error starting web UI: {e}")
        else:
            print(f"Web UI is already running at: {self.web_url}")

