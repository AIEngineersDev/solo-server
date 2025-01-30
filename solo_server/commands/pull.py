import typer
import subprocess

def pull(model: str):
    """
    Pulls a model using Ramalama registry.
    """
    typer.echo(f"🔄 Pulling model {model} from Ramalama registry...")

    try:
        command = ["ramalama", "pull", model]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Progress tracking
        for line in process.stdout:
            typer.echo(line.strip())

        process.wait()

        if process.returncode == 0:
            typer.echo(f"✅ Model {model} pulled successfully.")
        else:
            typer.echo(f"❌ Failed to pull model {model}.", err=True)

    except Exception as e:
        typer.echo(f"⚠️ Error pulling model {model}: {e}", err=True)
