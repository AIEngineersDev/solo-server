# solo_server/commands/download.py
import typer
import os
import requests
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from solo_server.utils.helpers import execute_command

console = Console()
app = typer.Typer(help="⬇️ Download model weights for a specific tag.")

@app.command()
def download(
    tag: str = typer.Argument(..., help="Tag of the AI model/template to download."),
    url: str = typer.Option(..., "--url", "-u", help="URL to download the model weights from.")
):
    """
    ⬇️ Download model weights for a specific tag and save them into the models directory.
    """
    console.print(f"[bold green]⬇️ Downloading model weights for tag: {tag} from {url}...[/bold green]")
    tag_dir = os.path.join("tags", tag)
    models_dir = os.path.join(tag_dir, "models")
    weights_path = os.path.join(models_dir, "weights.pth")

    # Create models directory if it doesn't exist
    Path(models_dir).mkdir(parents=True, exist_ok=True)

    # Download the weights file
    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Downloading weights...", total=None)
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(weights_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            progress.update(task, description="Download completed.")
        console.print(f"[bold green]✅ Model weights downloaded and saved to '{weights_path}'.[/bold green]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]❌ Failed to download weights: {e}[/bold red]")
        raise typer.Exit(code=1)
