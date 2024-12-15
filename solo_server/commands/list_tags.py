# solo_server/commands/list_tags.py
import typer
import os

from rich.console import Console
from rich.table import Table

from solo_server.utils.helpers import execute_command

console = Console()
app = typer.Typer(help="📋 List all available tagged templates.")

@app.command()
def list_tags():
    """
    📋 List all available tagged templates.
    """
    console.print("[bold green]📋 Available Tags:[/bold green]")
    tags_dir = "tags"
    if not os.path.exists(tags_dir):
        console.print(f"[bold red]❌ Tags directory '{tags_dir}' not found.[/bold red]")
        raise typer.Exit(code=1)

    tags = [tag for tag in os.listdir(tags_dir) if os.path.isdir(os.path.join(tags_dir, tag))]
    if not tags:
        console.print("[bold red]❌ No tags found in the 'tags' directory.[/bold red]")
    else:
        table = Table(title="Available Tags", box=box.SIMPLE_HEAVY)
        table.add_column("Tag", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        # Assuming each tag directory has a description.txt file
        for tag in tags:
            description_file = os.path.join(tags_dir, tag, "description.txt")
            if os.path.exists(description_file):
                with open(description_file, "r") as f:
                    description = f.read().strip()
            else:
                description = "No description available."
            table.add_row(tag, description)
        console.print(table)
