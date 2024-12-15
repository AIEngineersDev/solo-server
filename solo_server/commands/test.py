# solo_server/commands/test.py
import typer
import requests
import json

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
app = typer.Typer(help="🧪 Test the endpoint for a specific tag.")

@app.command()
def test(tag: str):
    """
    🧪 Test the endpoint for a specific tag.
    """
    console.print(f"[bold green]🧪 Testing endpoint for tag: {tag}...[/bold green]")
    url = "http://localhost:5070/predictions"

    payload = {
        "input": {
            "image": "https://path_to_input_image.jpg"  # Replace with actual image URL or path
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Sending test request...", total=None)
            response = requests.post(url, headers=headers, data=json.dumps(payload), stream=True)
            progress.update(task, description="Receiving response...")
        
        if response.status_code == 200:
            # Handle streaming response if supported
            description = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    description += chunk.decode('utf-8')
            console.print(f"[bold green]✅ Test Passed. Response: {description}[/bold green]")
        else:
            console.print(f"[bold red]❌ Test Failed with status code {response.status_code}: {response.text}[/bold red]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]❌ Test Failed: {e}[/bold red]")
