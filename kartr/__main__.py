import asyncio
import click
from kartr.cli import CLI
from kartr.core import Kartr

@click.command()
@click.option('--debug', is_flag=True, help='Enable debug mode')
def main(debug):
    """Run the kartr AI-driven development environment."""
    kartr = Kartr(debug=debug)
    cli = CLI(kartr)
    asyncio.run(cli.run())

if __name__ == "__main__":
    main()
