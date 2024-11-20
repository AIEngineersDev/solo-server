import typer
from subprocess import run, CalledProcessError
import os

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


            # Construct model URL and filename
            model_url = f"{base_url}/{username}/{repository}/resolve/main/{repository}.{quantization}"
            model_filename = f"{repository}.{quantization}"
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


# @app.command()
# def start(
#     tag: str,
#     model_url: str = typer.Option(
#         None,
#         "--model-url", "-u",
#         help="URL for the LLM model (only used with llm tag)"
#     ),
#     model_filename: str = typer.Option(
#         None,
#         "--model-filename", "-f",
#         help="Filename for the LLM model (only used with llm tag)"
#     )
# ):
#     """
#     🚀 Start the Solo Server for model inference.
#     """
#     typer.echo(f"🚀 Starting the Solo Server with tag: {tag}...")
    
#     if tag == "llm":
#         # Default values for llm tag
#         default_url = "https://huggingface.co/Mozilla/Llama-3.2-1B-Instruct-llamafile/resolve/main/Llama-3.2-1B-Instruct.Q6_K.llamafile"
#         default_filename = "Llama-3.2-1B-Instruct.Q6_K.llamafile"
        
#         # Use provided values or defaults
#         os.environ["MODEL_URL"] = model_url or default_url
#         os.environ["MODEL_FILENAME"] = model_filename or default_filename
#     elif (model_url or model_filename) and tag != "llm":
#         typer.echo("⚠️ Warning: model-url and model-filename are only used with the llm tag")
    
#     python_file = f"templates/{tag}.py"
#     os.environ["PYTHON_FILE"] = python_file
    
#     # Get the current file's directory and construct the full path
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     docker_compose_path = os.path.join(current_dir, "docker-compose.yml")
#     execute_command(["docker-compose", "-f", docker_compose_path, "up", "--build"])

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
