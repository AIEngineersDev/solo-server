# solo_server/commands/benchmark.py
import typer
import os

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from solo_server.utils.helpers import execute_command

console = Console()
app = typer.Typer(help="🚦 Benchmark the server for a specific tag using Locust.")

@app.command()
def benchmark(tag: str):
    """
    🚦 Benchmark the server for a specific tag using Locust.
    """
    console.print(f"[bold green]🚦 Benchmarking server for tag: {tag}...[/bold green]")
    tag_dir = os.path.join("tags", tag)
    locust_file = os.path.join(tag_dir, "locustfile.py")

    if not os.path.exists(locust_file):
        console.print(f"[bold red]❌ locustfile.py not found in '{tag_dir}'.[/bold red]")
        raise typer.Exit(code=1)

    # Run Locust benchmark targeting port 5070
    command = ["locust", "-f", locust_file, "--host=http://localhost:5070"]

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Running Locust benchmark...", total=None)
        execute_command(command, "Failed to run benchmark", cwd=tag_dir)
        progress.update(task, description="Locust benchmark completed.")
