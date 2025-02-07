import typer
import subprocess

def run(model: str):
    """
    Serves a model using Ollama and enables interactive chat.
    """
    typer.echo(f"🚀 Starting model {model}...")

    # Check if Docker container is running
    try:
        check_cmd = ["docker", "ps", "-q", "-f", "name=solo"]
        if not subprocess.run(check_cmd, capture_output=True, text=True).stdout:
            typer.echo("❌ Solo server is not active. Please start solo server first.", err=True)
            return

        command = ["docker", "exec", "-it", "solo", "ollama", "run", model]
        
        # Use subprocess.run with shell=True for interactive terminal
        process = subprocess.run(
            " ".join(command),
            shell=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ An error occurred: {e}", err=True)
