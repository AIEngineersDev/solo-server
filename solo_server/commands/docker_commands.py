import subprocess
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def build(template: str = typer.Argument(..., help="Template name (e.g., 'basic', 'huggingface')")):
    """Build the Docker image for Solo Server."""
    typer.echo(f"Building Docker image for template: {template}")
    try:
        template_path = Path(f"templates/{template}")
        if not template_path.exists():
            raise ValueError(f"Template '{template}' not found.")
        
        subprocess.run(["docker", "build", "-t", f"solo-server-{template}", str(template_path)], check=True)
        typer.echo(f"Docker image for {template} built successfully.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while building the Docker image: {e}")
    except ValueError as e:
        typer.echo(str(e))

@app.command()
def start(template: str = typer.Argument(..., help="Template name (e.g., 'basic', 'huggingface')")):
    """Start the Docker container for Solo Server."""
    typer.echo(f"Starting Docker container for template: {template}")
    try:
        subprocess.run([
            "docker", "run", "-d",
            "--name", f"solo-server-{template}-container",
            "-p", "8000:8000",
            "-p", "8501:8501",
            f"solo-server-{template}"
        ], check=True)
        typer.echo(f"Docker container for {template} started.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while starting the Docker container: {e}")

@app.command()
def stop(template: str = typer.Argument(..., help="Template name (e.g., 'basic', 'huggingface')")):
    """Stop the running Docker container."""
    typer.echo(f"Stopping Docker container for template: {template}")
    try:
        subprocess.run(["docker", "stop", f"solo-server-{template}-container"], check=True)
        typer.echo(f"Docker container for {template} stopped.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while stopping the Docker container: {e}")

@app.command()
def remove(template: str = typer.Argument(..., help="Template name (e.g., 'basic', 'huggingface')")):
    """Remove the Docker container."""
    typer.echo(f"Removing Docker container for template: {template}")
    try:
        subprocess.run(["docker", "rm", f"solo-server-{template}-container"], check=True)
        typer.echo(f"Docker container for {template} removed.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while removing the Docker container: {e}")

if __name__ == "__main__":
    app()