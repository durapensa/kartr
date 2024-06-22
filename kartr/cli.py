import asyncio
import webbrowser
from kartr.web import start_web_server
import aiohttp

class CLI:
    def __init__(self, kartr):
        self.kartr = kartr
        self.web_url = None
        self.ws = None

    async def run(self):
        print("Welcome to kartr! Type 'help' for available commands.")
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, input, "kartr> ")
            if command.lower() == 'exit':
                break
            elif command.lower() == 'web':
                await self.start_web_ui()
            else:
                result = await self.kartr.process_command(command)
                print(result)
                if self.ws:
                    await self.ws.send_json({'command': command, 'result': result})

    async def start_web_ui(self):
        if not self.web_url:
            try:
                self.web_url = await start_web_server(self.kartr)
                print(f"Web UI is running at: {self.web_url}")
                webbrowser.open(self.web_url)
                await self.connect_websocket()
            except Exception as e:
                print(f"Error starting web UI: {e}")
        else:
            print(f"Web UI is already running at: {self.web_url}")

    # ... (rest of the methods remain the same)
