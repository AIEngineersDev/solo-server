import typer
import subprocess

app = typer.Typer()

@app.command()
def status():
    """Check running models."""
    typer.echo("Checking running model containers...")
    subprocess.run(["podman", "ps", "--filter", "name=solo-container"], check=True)
