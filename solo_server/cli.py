# solo_server/cli.py

import typer
from rich.console import Console
from rich.table import Table
from rich import box
import requests
from pathlib import Path
import sys

app = typer.Typer(help="🛠️ Solo Server CLI: Manage and Benchmark AI Models")
console = Console()

# Sample tags for demonstration purposes
AVAILABLE_TAGS = ["toy-hello-world", "sample-tag", "test-model"]

@app.command()
def start(tag: str):
    """
    🚀 Start the Solo Server for a specific tag.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    console.print(f"[bold green]🚀 Starting Solo Server with tag: {tag}[/bold green]")
    # Placeholder for actual start logic
    console.print(f"[bold blue]✅ Solo Server for '{tag}' started successfully![/bold blue]")

@app.command()
def stop(tag: str):
    """
    ⏹ Stop the Solo Server for a specific tag.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    console.print(f"[bold green]⏹ Stopping Solo Server with tag: {tag}[/bold green]")
    # Placeholder for actual stop logic
    console.print(f"[bold blue]✅ Solo Server for '{tag}' stopped successfully![/bold blue]")

@app.command()
def status(tag: str):
    """
    📈 Check the status of the Solo Server for a specific tag.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    # Placeholder for actual status check logic
    console.print(f"[bold green]📈 Solo Server for '{tag}' is running.[/bold green]")

@app.command()
def test(tag: str):
    """
    🧪 Test the Solo Server endpoint for a specific tag.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    console.print(f"[bold yellow]🧪 Testing Solo Server for tag: {tag}...[/bold yellow]")
    # Placeholder for actual test logic (e.g., sending a request)
    # Simulate a successful test
    try:
        # Simulated response
        response = {"status": "success", "message": f"Test for '{tag}' passed!"}
        console.print(f"[bold green]✅ {response['message']}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Test failed: {e}[/bold red]")
        raise typer.Exit(code=1)

@app.command()
def benchmark(tag: str):
    """
    🚦 Benchmark the Solo Server for a specific tag.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    console.print(f"[bold magenta]🚦 Benchmarking Solo Server for tag: {tag}...[/bold magenta]")
    # Placeholder for actual benchmarking logic
    console.print(f"[bold blue]✅ Benchmarking for '{tag}' completed successfully![/bold blue]")

@app.command()
def list_tags():
    """
    📋 List all available tags.
    """
    console.print("[bold green]📋 Available Tags:[/bold green]")
    table = Table(show_header=True, header_style="bold cyan", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Tag", style="dim", width=20)
    table.add_column("Description", style="magenta")
    for tag in AVAILABLE_TAGS:
        description = f"Description for {tag}"
        table.add_row(tag, description)
    console.print(table)

@app.command()
def download(tag: str, url: str):
    """
    ⬇️ Download model weights for a specific tag from a given URL.
    """
    if tag not in AVAILABLE_TAGS:
        console.print(f"[bold red]❌ Tag '{tag}' not found.[/bold red]")
        raise typer.Exit(code=1)
    console.print(f"[bold green]⬇️ Downloading model weights for tag: {tag} from {url}...[/bold green]")
    # Define the download path
    download_path = Path(f"models/{tag}_weights.pth")
    download_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        console.print(f"[bold blue]✅ Model weights downloaded and saved to '{download_path}'.[/bold blue]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]❌ Failed to download weights: {e}[/bold red]")
        raise typer.Exit(code=1)

@app.callback()
def main():
    """
    Solo Server CLI: Manage and Benchmark AI Models.
    """
    if len(sys.argv) == 1:
        console.print("[bold magenta]Welcome to Solo Server CLI! Use --help to see available commands.[/bold magenta]")

if __name__ == "__main__":
    app()
