import typer
import subprocess

def stop(name: str):
    """
    Stops a running model container using Ramalama.
    """
    typer.echo(f"🛑 Stopping {name} using Ramalama...")

    try:
        subprocess.run(["ramalama", "stop", name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        typer.echo(f"✅ {name} stopped successfully.")

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to stop {name}: {e.stderr}", err=True)
    except Exception as e:
        typer.echo(f"⚠️ Unexpected error: {e}", err=True)
