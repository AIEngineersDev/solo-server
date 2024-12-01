import typer
from subprocess import run, CalledProcessError, DEVNULL
import os
import sys
import time

app = typer.Typer(help="🛠️ Solo Server CLI for managing edge AI model inference using UV or Docker commands.")

def execute_command(command: list):
    """
    Executes a system command and handles errors.
    """
    try:
        run(command, check=True)
    except CalledProcessError as e:
        typer.echo(f"❌ Error: {e}")
        raise typer.Exit(code=1)

@app.command()
def start(
    tag: str,
    hf_model: str = typer.Option(
        None,
        "--hf-model", "-m",
        help="Hugging Face model in the format hf.co/{username}/{repository}:{quantization} (for 'llm' tag only)."
    ),
    use_uv: bool = typer.Option(
        False, "--uv", "-u", help="Run the script using UV environment management instead of Docker."
    )
):
    """
    🚀 Start the Solo Server for model inference.
    """
    if use_uv:
        typer.echo("🌐 Using UV to manage the environment...")
        dependencies = []
        if tag == "llm" and hf_model:
            typer.echo("⚠️ UV does not automatically fetch Hugging Face models.")
            dependencies = ["transformers", "torch"]  # Add relevant dependencies for Hugging Face models.

        # Construct the command for UV
        command = ["uv", "run", "--no-project", f"templates/{tag}.py"]
        for dep in dependencies:
            command.extend(["--with", dep])

        execute_command(command)
    else:
        typer.echo("🐳 Using Docker for environment management...")
        if tag == "llm" and hf_model:
            hf_model = hf_model or "hf.co/Mozilla/Llama-3.2-1B-Instruct-llamafile:Q6_K"
            username, repository, quantization = parse_hf_model(hf_model)
            model_name = repository.replace("llamafile", "").strip("-")
            model_filename = f"{model_name}.{quantization}.llamafile"
            model_url = f"https://huggingface.co/{username}/{repository}/resolve/main/{model_filename}"

            os.environ["MODEL_URL"] = model_url
            os.environ["MODEL_FILENAME"] = model_filename
            typer.echo(f"🌐 Model URL: {model_url}")
            typer.echo(f"📁 Model Filename: {model_filename}")

        python_file = f"templates/{tag}.py"
        os.environ["PYTHON_FILE"] = python_file
        docker_compose_path = os.path.join(os.getcwd(), "docker-compose.yml")
        execute_command(["docker-compose", "-f", docker_compose_path, "up", "--build"])

@app.command()
def stop(use_uv: bool = typer.Option(False, "--uv", "-u", help="Stop environments managed by UV instead of Docker.")):
    """
    ⏹ Stop the running Solo Server.
    """
    if use_uv:
        typer.echo("⏹ Stopping UV-managed environment...")
        # Since UV doesn't have a built-in stop mechanism, the user might need to manually terminate processes.
        typer.echo("⚠️ Use system tools to terminate the process if necessary.")
    else:
        typer.echo("⏹ Stopping Docker containers...")
        docker_compose_path = os.path.join(os.getcwd(), "docker-compose.yml")
        execute_command(["docker-compose", "-f", docker_compose_path, "down"])

@app.command()
def status(use_uv: bool = typer.Option(False, "--uv", "-u", help="Check the status of UV environments.")):
    """
    📈 Check the status of the Solo Server.
    """
    if use_uv:
        typer.echo("📈 Checking UV-managed environment status...")
        typer.echo("✅ If the script runs with 'uv run', the environment is active.")
    else:
        typer.echo("📈 Checking Docker container status...")
        docker_compose_path = os.path.join(os.getcwd(), "docker-compose.yml")
        execute_command(["docker-compose", "-f", docker_compose_path, "ps"])

@app.command()
def gen(tag: str):
    """
    🖌️ Generate a code base template for a specific tag.
    """
    typer.echo(f"🖌️ Generating code base template for tag: {tag}...")
    os.makedirs(f"templates/{tag}", exist_ok=True)
    with open(f"templates/{tag}/main.py", "w") as file:
        file.write("# Template code\n")

def parse_hf_model(hf_model: str):
    """
    Parses the Hugging Face model string in the format hf.co/{username}/{repository}:{quantization}.
    Returns username, repository, and quantization as a tuple.
    """
    if not hf_model.startswith("hf.co/"):
        raise ValueError("Model string must start with 'hf.co/'")
    username, repo_quantization = hf_model.split("hf.co/")[1].split("/", 1)
    repository, quantization = repo_quantization.rsplit(":", 1)
    return username, repository, quantization

if __name__ == "__main__":
    app()
