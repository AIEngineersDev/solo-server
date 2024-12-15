# solo_server/cli.py

import typer
from rich.console import Console

from .commands.start import app as start_app
from .commands.stop import app as stop_app
from .commands.status import app as status_app
from .commands.test import app as test_app
from .commands.benchmark import app as benchmark_app
from .commands.list_tags import app as list_tags_app
from .commands.download import app as download_app
from .hardware import hardware_info

app = typer.Typer(help="🛠️ Solo Server CLI for managing and benchmarking AI models.")
console = Console()

# Register sub-commands
app.add_typer(start_app, name="start")
app.add_typer(stop_app, name="stop")
app.add_typer(status_app, name="status")
app.add_typer(test_app, name="test")
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(list_tags_app, name="list_tags")
app.add_typer(download_app, name="download")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Main entry point for the Solo Server CLI. If no subcommand is provided,
    it defaults to displaying hardware information.
    """
    if ctx.invoked_subcommand is None:
        hardware_info()

if __name__ == "__main__":
    app()
