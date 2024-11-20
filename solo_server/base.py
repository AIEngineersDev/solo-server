import typer
from subprocess import run, CalledProcessError, DEVNULL
import os
import sys
import time
import requests
import subprocess

app = typer.Typer(help="🛠️ Solo Server CLI for managing edge AI model inference using Docker-style commands.")

def execute_command(command: list):
    """Utility function to execute shell commands."""
    try:
        run(command, check=True)
    except CalledProcessError as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)

def check_docker_installation():
    """Ensure Docker and Docker Compose are installed and user has necessary permissions."""
    typer.echo("🔍 Checking Docker and Docker Compose installation...")

    # Check Docker
    try:
        run(["docker", "--version"], stdout=DEVNULL, stderr=DEVNULL, check=True)
    except FileNotFoundError:
        typer.echo("❌ Docker is not installed. Installing Docker...")
        execute_command([
            "curl", "-fsSL", "https://get.docker.com", "|", "sh"
        ])
    except CalledProcessError:
        typer.echo("❌ Docker is installed but not accessible. Please ensure you have the correct permissions.")
        typer.echo("🔑 Run the following to add your user to the Docker group:")
        typer.echo("   sudo usermod -aG docker $USER && newgrp docker")
        sys.exit(1)

    # Check Docker Compose
    try:
        run(["docker-compose", "--version"], stdout=DEVNULL, stderr=DEVNULL, check=True)
    except FileNotFoundError:
        typer.echo("❌ Docker Compose is not installed. Installing Docker Compose...")
        execute_command([
            "curl", "-L", "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)",
            "-o", "/usr/local/bin/docker-compose"
        ])
        execute_command(["chmod", "+x", "/usr/local/bin/docker-compose"])
    except CalledProcessError:
        typer.echo("❌ Docker Compose is installed but not accessible.")
        sys.exit(1)

    typer.echo("✅ Docker and Docker Compose are installed and accessible.")

@app.command()
def start(tag: str):
    """
    🚀 Start the Solo Server for model inference.
    """
    check_docker_installation()
    typer.echo(f"🚀 Starting the Solo Server with tag: {tag}...")
    python_file = f"templates/{tag}.py"
    os.environ["PYTHON_FILE"] = python_file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "up", "-d"])

@app.command()
def stop():
    """
    ⏹ Stop the running Solo Server.
    """
    check_docker_installation()
    typer.echo("⏹ Stopping the Solo Server...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "down"])

@app.command()
def status():
    """
    📈 Check the status of the Solo Server.
    """
    check_docker_installation()
    typer.echo("📈 Checking Solo Server status...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "ps"])

@app.command()
def benchmark(
    model_url: str = typer.Option(..., help="URL of the model to benchmark"),
    model_filename: str = typer.Option(..., help="Filename for the downloaded model"),
    template: str = typer.Option("llm", help="Template to use for benchmarking")
):
    """
    🏎️ Run a benchmark test on the Solo Server with TimescaleDB and Grafana integration.
    """
    check_docker_installation()
    
    # First start the Solo Server with the specified template
    typer.echo(f"🚀 Starting the Solo Server with template: {template}...")
    python_file = f"templates/{template}.py"
    os.environ["PYTHON_FILE"] = python_file
    os.environ["MODEL_URL"] = model_url
    os.environ["MODEL_FILENAME"] = model_filename
    
    # Start the main server
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "up", "-d"])

    # Wait for container to be healthy
    typer.echo("⏳ Waiting for LLM server to be ready...")
    start_time = time.time()
    timeout = 300  # 5 minutes timeout
    
    while True:
        if time.time() - start_time > timeout:
            typer.echo("❌ LLM server startup timed out")
            execute_command(["docker-compose", "-f", docker_compose_path, "down"])
            return

        result = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Health.Status}}", "solo-api"],
            capture_output=True,
            text=True
        )
        status = result.stdout.strip()
        
        if status == "healthy":
            typer.echo("✅ LLM server is ready!")
            break
        elif status == "unhealthy":
            # Print the container logs to help debug
            typer.echo("Checking container logs:")
            subprocess.run(["docker", "logs", "solo-api"])
            typer.echo("❌ LLM server failed to start")
            execute_command(["docker-compose", "-f", docker_compose_path, "down"])
            return
        
        typer.echo("⏳ Waiting for LLM server to initialize... (Status: " + status + ")")
        time.sleep(5)

    # Now start the benchmark tools
    typer.echo("🏎️ Starting benchmark tools...")
    benchmark_compose_path = os.path.join(current_dir, "docker-compose-benchmark.yml")
    execute_command(["docker-compose", "-f", benchmark_compose_path, "up", "-d", "timescale", "grafana", "locust"])

    try:
        # Wait for Grafana to be ready
        typer.echo("⏳ Waiting for Grafana to be ready...")
        time.sleep(10)

        # Configure Grafana
        typer.echo("🔧 Configuring Grafana...")
        grafana_setup_path = os.path.join(current_dir, "grafana_setup.sh")
        os.chmod(grafana_setup_path, 0o755)
        execute_command([grafana_setup_path])

        typer.echo("✅ Benchmark environment is ready!")
        typer.echo("📊 Visit:")
        typer.echo("   - Grafana: http://localhost:3000 (admin/admin)")
        typer.echo("   - Locust: http://localhost:8089")
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        typer.echo("\n⏹ Stopping all services...")
    finally:
        # Stop both compose files
        execute_command(["docker-compose", "-f", docker_compose_path, "down"])
        execute_command(["docker-compose", "-f", benchmark_compose_path, "down"])

@app.command()
def gui():
    """
    🖥️ Launch the Streamlit GUI for Solo Server.
    """
    typer.echo("🖥️ Launching Streamlit app...")
    
    # Run Streamlit
    streamlit_command = [
        "streamlit", 
        "run", 
        "templates/streamlit_llm.py"
    ]

    try:
        print(execute_command(streamlit_command))
    except Exception as e:
        typer.echo(f"❌ Failed to launch Streamlit app: {e}")
    else:
        typer.echo("✅ Streamlit app launched successfully.")

if __name__ == "__main__":
    app()
