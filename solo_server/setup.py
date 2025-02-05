import typer
import subprocess
import shutil
import time
from .utils.hardware import display_hardware_info

def start():

    """Setup solo-server environment."""
    
    display_hardware_info(typer)
    typer.echo("\n🚀 Setting up Solo Server...")
    
    if not shutil.which("docker"):
        typer.echo("❌ Docker is not installed. Please install Docker first.", err=True)
        return

    try:
        # Check if Docker daemon is running
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        
        # Check if container exists (running or stopped)
        container_exists = subprocess.run(
            ["docker", "ps", "-aq", "-f", "name=ollama"], 
            capture_output=True, 
            text=True
        ).stdout.strip()

        if container_exists:
            # Check if container is running
            check_cmd = ["docker", "ps", "-q", "-f", "name=ollama"]
            is_running = subprocess.run(check_cmd, capture_output=True, text=True).stdout.strip()
            if not is_running:
                subprocess.run(["docker", "start", "ollama"], check=True, capture_output=True)
        else:
            # Pull Ollama image
            typer.echo("📥 Pulling Ollama Docker image...")
            subprocess.run(["docker", "pull", "ollama/ollama"], check=True)

            # Check if port is available
            try:
                subprocess.run(
                    ["docker", "run", "--rm", "-p", "11434:11434", "alpine", "true"], 
                    check=True, 
                    capture_output=True
                )
            except subprocess.CalledProcessError:
                typer.echo("❌ Port 11434 is already in use", err=True)
                return

            # Start Ollama container
            typer.echo("🚀 Starting Solo Server...")
            subprocess.run([
                "docker", "run", "-d",
                "--name", "solo",
                "-v", "ollama:/root/.ollama",
                "-p", "11434:11434",
                "ollama/ollama"
            ], check=True)

        # Wait for container to be ready with timeout
        timeout = 30
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                subprocess.run(
                    ["docker", "exec", "ollama", "ollama", "list"],
                    check=True,
                    stdout=subprocess.DEVNULL  # Only suppress stdout
                )
                typer.echo("✅ Solo server is ready!")
                return
            except subprocess.CalledProcessError:
                time.sleep(1)
        
        typer.echo("❌ Solo server failed to start within timeout", err=True)

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Docker command failed: {e}", err=True)
        # Cleanup on failure
        if container_exists:
            subprocess.run(["docker", "stop", "ollama"], check=False)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)

if __name__ == "__main__":
    start()
