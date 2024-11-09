import subprocess
import typer
import os
from pathlib import Path
from importlib import resources

app = typer.Typer()

def get_template_path(template: str) -> Path:
    """Get the path to a template directory from the installed package."""
    with resources.path('solo_server.templates', template) as template_path:
        return template_path

@app.command()
def build(template: str = typer.Argument(..., help="Template name (e.g., 'basic', 'huggingface')")):
    """Build the Docker image for Solo Server."""
    typer.echo(f"Building Docker image for template: {template}")
    try:
        template_path = get_template_path(template)
        
        if not template_path.exists():
            raise ValueError(f"Template '{template}' not found at {template_path}")
        
        original_dir = os.getcwd()
        try:
            os.chdir(template_path)
            subprocess.run(
                ["PYTHON_FILE=src/predict.py", "docker-compose", "up", "--build", "-d"],
                check=True,
                shell=True,
                env={**os.environ, "PYTHON_FILE": "src/predict.py"}
            )
            typer.echo(f"Docker image for {template} built successfully.")
        finally:
            os.chdir(original_dir)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Error while building the Docker image: {e}")
    except ValueError as e:
        typer.echo(str(e))