import asyncio

class CLI:
    def __init__(self, kartr):
        self.kartr = kartr

    async def run(self):
        print("Welcome to kartr! Type 'exit' to quit.")
        while True:
            command = await asyncio.get_event_loop().run_in_executor(None, input, "kartr> ")
            if command.lower() == 'exit':
                break
            result = await self.kartr.process_command(command)
            print(result)
