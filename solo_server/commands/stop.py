# solo_server/commands/stop.py
import typer
import platform
import os

from rich.console import Console

from solo_server.utils.helpers import execute_command

console = Console()
app = typer.Typer(help="⏹ Stop the running Solo Server.")

@app.command()
def stop():
    """
    ⏹ Stop the running Solo Server.
    """
    console.print("[bold green]⏹ Stopping Solo Server...[/bold green]")
    if platform.system() == "Windows":
        # Use taskkill for Windows
        execute_command(["taskkill", "/F", "/IM", "python.exe"], "Failed to stop the server")
    else:
        # Use pkill for Unix-based systems
        execute_command(["pkill", "-f", "cog serve"], "Failed to stop the server")
