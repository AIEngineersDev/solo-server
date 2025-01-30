import typer
import subprocess

app = typer.Typer()

@app.command()
def check():
    """Check running models."""
    typer.echo("Checking running model containers...")
    subprocess.run(["docker", "ps", "--filter", "name=solo-container"], check=True)
