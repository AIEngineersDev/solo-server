# solo_server/commands/start.py

import typer
import os
from typing import List

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from solo_server.utils.helpers import execute_command

console = Console()
app = typer.Typer(help="🚀 Start the Solo Server for a specific tag using LitServe and Cog.")

@app.command(name="")
def start(tag: str = typer.Argument(..., help="Tag of the AI model/template to start.")):
    """
    🚀 Start the Solo Server for a specific tag using LitServe and Cog.
    """
    console.print(f"[bold green]🌟 Starting Solo Server with tag: {tag}[/bold green]")
    tag_dir = os.path.join("tags", tag)
    cog_yaml = os.path.join(tag_dir, "cog.yaml")

    if not os.path.exists(cog_yaml):
        console.print(f"[bold red]❌ cog.yaml not found in '{tag_dir}'.[/bold red]")
        raise typer.Exit(code=1)

    console.print("[bold green]🌐 Using Cog and LitServe to manage the environment...[/bold green]")

    # Construct the command for Cog
    command = ["cog", "serve", "-p", "5070"]

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Starting LitServe server...", total=None)
        execute_command(command, f"Failed to start the server for tag '{tag}'", cwd=tag_dir)
        progress.update(task, description="LitServe server started on port 5070.")
