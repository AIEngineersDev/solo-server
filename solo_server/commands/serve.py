import typer
import subprocess

def serve(name: str, model: str):
    """
    Serves a model using Ramalama.
    """
    typer.echo(f"🚀 Starting model {model} as {name}...")

    try:
        command = ["ramalama", "serve", model]
        process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        typer.echo(f"✅ Model {model} is now running as {name}.")
        typer.echo(f"🌐 Access the UI at: http://127.0.0.1:5070")

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to serve model {model}: {e.stderr}", err=True)
    except Exception as e:
        typer.echo(f"⚠️ Unexpected error: {e}", err=True)
