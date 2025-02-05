import typer
import subprocess
from solo_server.utils.hardware import display_hardware_info

app = typer.Typer()

@app.command()
def status():
    """Check running models and system status."""
    display_hardware_info(typer)
    typer.echo("\n🔍 Running Models:")
    subprocess.run(["docker", "ps"], check=True)
