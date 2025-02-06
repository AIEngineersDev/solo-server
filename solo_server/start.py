import typer
import subprocess
import shutil
import time
from .utils.hardware import detect_hardware, display_hardware_info

def check_nvidia_toolkit() -> bool:
    """
    Checks if Docker can actually run a GPU container using the NVIDIA runtime.
    """
    try:
        test_cmd = [
            "docker", "run", "--rm", "--gpus", "all",
            "nvidia/cuda:11.0.3-base-ubuntu20.04", "nvidia-smi"
        ]
        subprocess.run(test_cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False
    

def install_nvidia_toolkit_linux():
    """
    Installs the NVIDIA Container Toolkit on Linux (Debian & Ubuntu).
    """
    typer.echo("Configuring the repository")
    try:
        subprocess.run("curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg", shell=True, check=True)
        subprocess.run("curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list", shell=True, check=True)
        subprocess.run("sudo apt-get update", shell=True, check=True)

        typer.echo("Installing Nvidia Container Toolkit")
        subprocess.run("sudo apt-get install -y nvidia-container-toolkit", shell=True, check=True)
        subprocess.run("sudo nvidia-ctk runtime configure --runtime=docker", shell=True, check=True)
        subprocess.run("sudo systemctl restart docker", shell=True, check=True)

        typer.echo("NVIDIA Container Toolkit installed successfully on Linux.")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Failed to install NVIDIA Container Toolkit on Linux. Error: {e}", err=True)


def install_nvidia_toolkit_windows():
    """
    Provide a structured step-by-step guide for Windows users to configure
    their system for NVIDIA GPU support, including driver & CUDA installation.
    """
    # Step-by-step instructions
    typer.secho("\n========================================", fg=typer.colors.CYAN)
    typer.secho(" Windows NVIDIA GPU Setup ", fg=typer.colors.CYAN, bold=True)
    typer.secho("========================================\n", fg=typer.colors.CYAN)

    typer.echo("Follow these steps to enable NVIDIA GPU support on Windows:\n")

    steps = [
        ("Step 1: Install or Update NVIDIA Drivers", "https://www.nvidia.com/Download/index.aspx"),
        ("Step 2: Install the NVIDIA CUDA Toolkit", "https://developer.nvidia.com/cuda-downloads")
    ]
    for step_num, (step_title, link) in enumerate(steps, start=1):
        typer.secho(f"{step_title}", fg=typer.colors.BRIGHT_GREEN)
        typer.echo(f"   Link: {link}\n")

    typer.echo("Once you've completed the above steps:")
    typer.echo(" - Ensure Docker Desktop is installed and running.")
    typer.echo(" - Enable 'Use the WSL 2 based engine' in Docker Desktop settings.\n")
    
    typer.secho("⚠️  Please restart Solo Server after installing the required tools.", fg=typer.colors.YELLOW)
    raise typer.Exit(1)

def start():

    """Setup solo-server environment."""
    
    display_hardware_info(typer)
    typer.echo("\n🚀 Setting up Solo Server...")
    
    if not shutil.which("docker"):
        typer.echo(
            "❌ Docker is not installed. Please install Docker first.\n"
            "Link: https://docs.docker.com/get-docker/\n",
            err=True
        )
        raise typer.Exit(code=1)
    
    try:
        # Check if Docker daemon is running
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, gpu_memory, compute_backend, os = detect_hardware()
        use_gpu = False

        if gpu_vendor == "NVIDIA":
            if check_nvidia_toolkit():
                typer.echo("✅ NVIDIA Docker Toolkit is already installed.\n")
                use_gpu = True
            else:
                if typer.confirm("NVIDIA GPU detected but Toolkit is not installed. Do you want to install it?", default=False):
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
            if use_gpu:
                docker_run_cmd += ["--gpus", "all"]
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
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {e}", err=True)

if __name__ == "__main__":
    start()
