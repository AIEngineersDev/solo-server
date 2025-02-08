import typer
import subprocess
import shutil
import time
import platform
from solo_server.utils.hardware import detect_hardware, display_hardware_info
from solo_server.utils.nvidia import check_nvidia_toolkit, install_nvidia_toolkit_linux, install_nvidia_toolkit_windows

def start_docker_engine(os_name):
    """
    Attempts to start the Docker engine based on the OS.
    """
    typer.echo("Starting the Docker engine...")
    try:
        if os_name == "Windows":
            try:
                subprocess.run(["sc", "start", "docker"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                typer.echo("Docker service is not registered. Trying to start Docker Desktop...", err=True)

                # Run PowerShell command to get Docker path
                result = subprocess.run(
                    ["powershell", "-Command", "(Get-Command docker | Select-Object -ExpandProperty Source)"],
                    capture_output=True,
                    text=True
                )

                docker_path = result.stdout.strip()
                if "Docker" in docker_path:
                    # Find the second occurrence of 'Docker'
                    parts = docker_path.split("\\")
                    docker_index = [i for i, part in enumerate(parts) if part.lower() == "docker"]

                    if len(docker_index) >= 2:
                        docker_desktop_path = "\\".join(parts[:docker_index[1] + 1]) + "\\Docker Desktop.exe"

                        typer.echo(f"Starting Docker Desktop from: {docker_desktop_path}")
                        subprocess.run(["powershell", "-Command", f"Start-Process '{docker_desktop_path}' -Verb RunAs"], check=True)
                    else:
                        typer.echo("❌ Could not determine Docker Desktop path.", err=True)
                else:
                    typer.echo("❌ Docker is not installed or incorrectly configured.", err=True)

        elif os_name == "Linux":
            try:
                # First try systemctl for system Docker service
                subprocess.run(["sudo", "systemctl", "start", "docker"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                try:
                    # If systemctl fails, try starting Docker Desktop
                    subprocess.run(["systemctl", "--user", "start", "docker-desktop"], check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    typer.echo("❌ Failed to start Docker. Please start manually", err=True)

        elif os_name == "Darwin":  # macOS
            subprocess.run(["open", "/Applications/Docker.app"], check=True, capture_output=True)
        time.sleep(5) # Wait for Docker to start
    except subprocess.CalledProcessError:
        typer.echo("❌ Failed to start Docker. Please start Docker with admin privileges manually.", err=True)
        return False
    return True

def start():
    """Setup solo-server environment."""
    display_hardware_info(typer)
    cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, gpu_memory, compute_backend, os = detect_hardware()
    use_gpu = False
    typer.echo("\n🚀 Setting up Solo Server...")

    # Initialize container_exists flag
    container_exists = False
    
    if not shutil.which("docker"):
        typer.echo(
            "❌ Docker is not installed. Please install Docker first.\n",
            err=True
        )
        typer.secho(
            "Install Here: https://docs.docker.com/get-docker/",
            fg=typer.colors.GREEN
        )
        raise typer.Exit(code=1)
    
    try:
        # Check if Docker daemon is running
        try:
            subprocess.run(["docker", "info"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            typer.echo("Docker daemon is not running. Attempting to start Docker...", err=True)
            if not start_docker_engine(os):
                raise typer.Exit(code=1)
            # Re-check if Docker is running
            try:
                subprocess.run(["docker", "info"], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                typer.echo("❌ Docker commands are not working as expected.", err=True)
                typer.echo("Try running the terminal with admin privileges.", err=True)
                raise typer.Exit(code=1)

        # Check for NVIDIA GPU
        if gpu_vendor == "NVIDIA":
            if check_nvidia_toolkit(os):
                typer.echo("✅ NVIDIA Toolkit is already installed.\n")
                use_gpu = True
            else:
                typer.echo("NVIDIA GPU detected but drivers are not installed.")
                if typer.confirm("Would you like to install NVIDIA drivers?", default=False):
                    if os == "Linux":
                        install_nvidia_toolkit_linux()
                    elif os == "Windows":
                        install_nvidia_toolkit_windows()
                    else:
                        typer.echo("Unsupported OS for automated NVIDIA toolkit installation.")
                else:
                    typer.echo("⚠️  Falling back to CPU.\n")

        # Check if container exists (running or stopped)
        container_exists = subprocess.run(
            ["docker", "ps", "-aq", "-f", "name=solo"], 
            capture_output=True, 
            text=True
        ).stdout.strip()

        if container_exists:
            # Check if container is running
            check_cmd = ["docker", "ps", "-q", "-f", "name=solo"]
            is_running = subprocess.run(check_cmd, capture_output=True, text=True).stdout.strip()
            if not is_running:
                subprocess.run(["docker", "start", "solo"], check=True, capture_output=True)
        else:
            # Pull Ollama image
            typer.echo("📥 Pulling Ollama Registry...")
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
            docker_run_cmd = ["docker", "run", "-d", "--name", "solo", "-v", "ollama:/root/.ollama", "-p", "11434:11434"]
            if gpu_vendor == "NVIDIA" and use_gpu:
                docker_run_cmd += ["--gpus", "all"]
                docker_run_cmd.append("ollama/ollama")
            elif gpu_vendor == "AMD":
                docker_run_cmd += ["--device", "/dev/kfd", "--device", "/dev/dri"]
                docker_run_cmd.append("ollama/ollama:rocm")
            else:
                docker_run_cmd.append("ollama/ollama")

            typer.echo("🚀 Starting Solo Server...")
            subprocess.run(docker_run_cmd, check=True)

        # Wait for container to be ready with timeout
        timeout = 30
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                subprocess.run(
                    ["docker", "exec", "solo", "ollama", "list"],
                    check=True,
                    stdout=subprocess.DEVNULL  # Only suppress stdout
                )
                typer.secho(
                "✅ Solo server is ready!\nYou can now access the UI at: https://solo-chatbot.vercel.app/",
                fg=typer.colors.BRIGHT_CYAN,
                bold=True
                )

                return
            except subprocess.CalledProcessError:
                time.sleep(1)
        
        typer.echo("❌ Solo server failed to start within timeout", err=True)

    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Docker command failed: {e}", err=True)
        # Cleanup on failure
        if container_exists:
            subprocess.run(["docker", "stop", "solo"], check=False)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)

if __name__ == "__main__":
    start()
