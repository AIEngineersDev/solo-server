import typer
from subprocess import run, CalledProcessError, DEVNULL
import os
import sys
import time
import requests
import subprocess

app = typer.Typer(help="🛠️ Solo Server CLI for managing edge AI model inference using Docker-style commands.")

def execute_command(command: list):
    try:
        run(command, check=True)
    except CalledProcessError as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)

# Recurring prompt to ask for the next command
@app.command()
def prompt():
    """
    🔄 Recurring prompt for managing the Solo Server.
    """
    while True:
        typer.echo("\nWhat would you like to do?")
        typer.echo("1. 🚀 Start the Solo Server")
        typer.echo("2. ⏹ Stop the Solo Server")
        typer.echo("3. 📈 Check the Solo Server status")
        typer.echo("4. 🖌️ Generate a code base template")
        typer.echo("5. ❌ Exit")
        choice = typer.prompt("Enter the number of your choice")

        if choice == "1":
            tag = typer.prompt("Enter the tag name to start the server with")
            start(tag)
        elif choice == "2":
            stop()
        elif choice == "3":
            status()
        elif choice == "4":
            tag = typer.prompt("Enter the tag name for the code base template")
            gen(tag)
        elif choice == "5":
            typer.echo("❌ Exiting the Solo Server CLI. Goodbye!")
            break
        else:
            typer.echo("⚠️ Invalid choice. Please try again.")

# Command to start the Solo Server, expects a tag name

@app.command()
def gui():
    print("Running GUI now!")
    execute_command(["streamlit", "run", "gui.py"])

@app.command()
def start(
    tag: str,
    hf_model: str = typer.Option(
        None,
        "--hf-model", "-m",
        help="Hugging Face model in the format hf.co/{username}/{repository}:{quantization} (currently supports only llamafile and gguf models)"
    )
):
    """
    🚀 Start the Solo Server for model inference.
    """
    typer.echo(f"🚀 Starting the Solo Server with tag: {tag}...")
    
    if tag == "llm":
        # Default Hugging Face model details
        default_model = "hf.co/Mozilla/Llama-3.2-1B-Instruct-llamafile:Q6_K"

        # Use provided Hugging Face model or the default
        hf_model = hf_model or default_model

        # Parse the Hugging Face model format
        try:
            base_url = "https://huggingface.co"
            username, repository, quantization = parse_hf_model(hf_model)
            print(repository)

            # Validate supported formats
            if "llamafile" not in repository and "gguf" not in repository:
                typer.echo("❌ Unsupported model format. Currently, only repositories containing 'llamafile' or 'gguf' are supported.")
                raise typer.Exit(code=1)

            # Extract model name from repository
            model_name = repository.replace("llamafile", "").strip("-")  # Remove 'llamafile' suffix and clean up

            # Construct model URL and filename
            model_filename = f"{model_name}.{quantization}.llamafile"
            model_url = f"{base_url}/{username}/{repository}/resolve/main/{model_filename}"
        except ValueError as e:
            typer.echo(f"❌ Invalid Hugging Face model format: {e}")
            raise typer.Exit(code=1)

        # Store in environment variables
        os.environ["MODEL_URL"] = model_url
        os.environ["MODEL_FILENAME"] = model_filename
        typer.echo(f"🌐 Model URL set to: {model_url}")
        typer.echo(f"📁 Model filename set to: {model_filename}")
    elif hf_model and tag != "llm":
        typer.echo("⚠️ Warning: hf-model is only used with the llm tag")
    
    python_file = f"templates/{tag}.py"
    os.environ["PYTHON_FILE"] = python_file
    typer.echo(f"📂 Python file set to: {python_file}")
    
    # Get the current file's directory and construct the full path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "up", "--build"])

def parse_hf_model(hf_model: str):
    """
    Parses the Hugging Face model string in the format hf.co/{username}/{repository}:{quantization}.
    Returns username, repository, and quantization as a tuple.
    """
    if not hf_model.startswith("hf.co/"):
        raise ValueError("Model string must start with 'hf.co/'")

    try:
        # Strip the "hf.co/" prefix
        _, path = hf_model.split("hf.co/", 1)

        # Split into username and the rest of the path
        username, repo_quantization = path.split("/", 1)

        # Split repository and quantization by the last ':'
        if ":" not in repo_quantization:
            raise ValueError("Model string must include a quantization specifier, e.g., ':Q6_K'")

        repository, quantization = repo_quantization.rsplit(":", 1)  # Use rsplit to handle repository names with colons
        return username, repository, quantization
    except ValueError:
        raise ValueError("Model string must be in the format 'hf.co/{username}/{repository}:{quantization}'")


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
def benchmark(
    tag: str,
    hf_model: str = typer.Option(
        None,
        "--hf-model", "-m",
        help="Hugging Face model in the format hf.co/{username}/{repository}:{quantization} (currently supports only llamafile and gguf models)"
    )
):
    """
    🏎️ Run a benchmark test on the Solo Server with TimescaleDB and Grafana integration.
    """
    check_docker_installation()

    typer.echo(f"🚀 Starting the Solo Server with tag: {tag}...")
    
    if tag == "llm":
        # Default Hugging Face model details
        default_model = "hf.co/Mozilla/Llama-3.2-1B-Instruct-llamafile:Q6_K"

        # Use provided Hugging Face model or the default
        hf_model = hf_model or default_model

        # Parse the Hugging Face model format
        try:
            base_url = "https://huggingface.co"
            username, repository, quantization = parse_hf_model(hf_model)
            print(repository)

            # Validate supported formats
            if "llamafile" not in repository and "gguf" not in repository:
                typer.echo("❌ Unsupported model format. Currently, only repositories containing 'llamafile' or 'gguf' are supported.")
                raise typer.Exit(code=1)

            # Extract model name from repository
            model_name = repository.replace("llamafile", "").strip("-")  # Remove 'llamafile' suffix and clean up

            # Construct model URL and filename
            model_filename = f"{model_name}.{quantization}.llamafile"
            model_url = f"{base_url}/{username}/{repository}/resolve/main/{model_filename}"
        except ValueError as e:
            typer.echo(f"❌ Invalid Hugging Face model format: {e}")
            raise typer.Exit(code=1)

        # Store in environment variables
        os.environ["MODEL_URL"] = model_url
        os.environ["MODEL_FILENAME"] = model_filename
        typer.echo(f"🌐 Model URL set to: {model_url}")
        typer.echo(f"📁 Model filename set to: {model_filename}")

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

        result = run(
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
            run(["docker", "logs", "solo-api"])
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

# Command to stop the Solo Server
@app.command()
def stop():
    """
    ⏹ Stop the running Solo Server.
    """
    typer.echo("⏹ Stopping the Solo Server...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "down"])

# Command to check the status of the Solo Server
@app.command()
def status():
    """
    📈 Check the status of the Solo Server.
    """
    typer.echo("📈 Checking Solo Server status...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
    execute_command(["docker-compose", "-f", docker_compose_path, "ps"])

# Command to generate a code base template related to the tag
@app.command()
def gen(tag: str):
    """
    🖌️ Generate a code base template related to the tag.
    """
    typer.echo(f"🖌️ Generating code base template for tag: {tag}...")
    # Add logic to generate a template based on the provided tag

if __name__ == "__main__":
    app()
