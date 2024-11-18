import typer
from subprocess import run, CalledProcessError, DEVNULL
import os
import sys

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
def benchmark():
    """
    🏎️ Run a benchmark test on the Solo Server with TimescaleDB and Grafana integration.
    """
    check_docker_installation()
    typer.echo("🏎️ Starting benchmark test...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    
    # Start TimescaleDB and Grafana
    typer.echo("🛠️ Setting up Grafana and TimescaleDB...")
    execute_command(["docker-compose", "-f", docker_compose_path, "up", "-d"])

    # Run Locust benchmark
    locust_command = [
        "locust",
        "--headless",
        "--users", "10",
        "--spawn-rate", "2",
        "--run-time", "1m",
        "--host", "http://localhost:8000",
        "--timescale"
    ]

    try:
        execute_command(locust_command)
    except Exception as e:
        typer.echo(f"❌ Benchmark failed: {e}")
    else:
        typer.echo("✅ Benchmark test completed successfully.")
        typer.echo("📊 Visit Grafana at http://localhost:3000 to view the results.")

    # Teardown
    typer.echo("⏹ Stopping Grafana and TimescaleDB...")
    execute_command(["docker-compose", "-f", docker_compose_path, "down"])

if __name__ == "__main__":
    app()
