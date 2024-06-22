import asyncio
from kartr.cli import CLI
from kartr.core import Kartr

async def main():
    kartr = Kartr()
    cli = CLI(kartr)
    await cli.run()

if __name__ == "__main__":
    asyncio.run(main())
