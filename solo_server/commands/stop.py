import typer
import subprocess

def stop(name: str = ""):
    """
    Stops the Ollama Docker container and any running models.
    """
    typer.echo("🛑 Stopping Solo Server...")

    try:
        # Stop the Docker container
        subprocess.run(
            ["docker", "stop", "ollama"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        typer.echo("✅ Solo server stopped successfully.")

        # # Remove the container
        # subprocess.run(
        #     ["docker", "rm", "ollama"],
        #     check=True,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE,
        #     text=True
        # )
        # typer.echo("🗑️ Ollama container removed.")

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to stop Solo Server: {e.stderr}", err=True)
    except Exception as e:
        typer.echo(f"⚠️ Unexpected error: {e}", err=True)
