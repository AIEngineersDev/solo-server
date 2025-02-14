import typer
import subprocess
import shutil
import time
import platform
from enum import Enum
from typing import Optional
from pathlib import Path
from solo_server.utils.hardware import detect_hardware, display_hardware_info
from solo_server.utils.nvidia import check_nvidia_toolkit, install_nvidia_toolkit_linux, install_nvidia_toolkit_windows
from solo_server.utils.server_utils import start_docker_engine, setup_vllm_server, setup_ollama_server

class ServerType(str, Enum):
    OLLAMA = "ollama"
    VLLM = "vllm"
    LLAMACPP = "llama.cpp"
    CUSTOM = "custom api"

def setup():
    """Interactive setup for Solo Server environment"""
    # Display hardware info
    display_hardware_info(typer)
    cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, gpu_memory, compute_backend, os_name = detect_hardware()
    
    typer.echo("\n🔧 Starting Solo Server Setup...\n")
    
    # Check Docker installation
    if not shutil.which("docker"):
        typer.echo("❌ Docker is not installed. Please install Docker first.\n", err=True)
        typer.secho("Install Here: https://docs.docker.com/get-docker/", fg=typer.colors.GREEN)
        raise typer.Exit(code=1)
    
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        typer.echo("Docker daemon is not running. Attempting to start Docker...", err=True)
        if not start_docker_engine(os_name):
            raise typer.Exit(code=1)
        # Re-check if Docker is running
        try:
            subprocess.run(["docker", "info"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            typer.echo("Try running the terminal with admin privileges.", err=True)
            raise typer.Exit(code=1)
        
    # Server Selection
    typer.echo("📊 Available Server Options:")
    for server in ServerType:
        typer.echo(f"  • {server.value}")
    
    def server_type_prompt(value: str) -> ServerType:
        try:
            return ServerType(value.lower())
        except ValueError:
            raise typer.BadParameter(f"Invalid server type: {value}")

    server_choice = typer.prompt(
        "\nChoose server",
        type=server_type_prompt,
        default="ollama",
    )
    
    # GPU Configuration
    use_gpu = False
    if gpu_vendor in ["NVIDIA", "AMD"]:
        if gpu_vendor == "NVIDIA" and check_nvidia_toolkit(os_name):
            use_gpu = typer.confirm(
                f"\n🎮 {gpu_vendor} GPU detected ({gpu_model}). Use GPU acceleration?",
                default=True
            )
            if use_gpu and not check_nvidia_toolkit(os_name):
                if typer.confirm("NVIDIA toolkit not found. Install now?", default=True):
                    if os_name == "Linux":
                        install_nvidia_toolkit_linux()
                    elif os_name == "Windows":
                        install_nvidia_toolkit_windows()
                    else:
                        typer.echo("Unsupported OS for automated NVIDIA toolkit installation.")
                        use_gpu = False
        else:
            typer.echo(f"\n⚠️  {gpu_vendor} GPU detected but drivers not installed.")
            use_gpu = False
    
    # Server specific setup
    try:
        if server_choice == ServerType.VLLM:
            setup_success = setup_vllm_server(use_gpu, cpu_model, gpu_vendor)
            if setup_success:
                typer.secho(
                    "Access the API at: http://localhost:8000\n",
                    fg=typer.colors.BLUE
                )
            
        elif server_choice == ServerType.OLLAMA:
            setup_success = setup_ollama_server(use_gpu, gpu_vendor)
            if setup_success:
                typer.secho(
                    "Access the API at: http://localhost:11434\n",
                    fg=typer.colors.BLUE
                )
            
        elif server_choice == ServerType.LLAMACPP:
            typer.echo("\n🚧 Llama.cpp server setup not implemented yet")
            # TODO: Implement Llama.cpp setup
            
        elif server_choice == ServerType.CUSTOM:
            api_url = typer.prompt("Enter your custom API endpoint")
            api_key = typer.prompt("Enter your API key (optional)", default="")
            
            # Save custom configuration
            config_dir = Path.home() / ".solo"
            config_dir.mkdir(exist_ok=True)
            
            with open(config_dir / "config.ini", "w") as f:
                f.write(f"[custom]\napi_url={api_url}\napi_key={api_key}\n")
            
            typer.secho("\n✅ Custom API configuration saved!", fg=typer.colors.BRIGHT_GREEN)
    
    except subprocess.CalledProcessError as e:
        typer.echo(f"\n❌ Setup failed: {e}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"\n❌ Unexpected error: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    typer.run(setup)