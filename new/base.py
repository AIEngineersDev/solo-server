import typer
from subprocess import run, CalledProcessError

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
def start(tag: str):
    """
    🚀 Start the Solo Server for model inference.
    """
    typer.echo(f"🚀 Starting the Solo Server with tag: {tag}...")
    execute_command(["docker-compose", "-f", "docker-compose.yml", "up", "-d", "--build"])

# Command to stop the Solo Server
@app.command()
def stop():
    """
    ⏹ Stop the running Solo Server.
    """
    typer.echo("⏹ Stopping the Solo Server...")
    execute_command(["docker-compose", "-f", "docker-compose.yml", "down"])

# Command to check the status of the Solo Server
@app.command()
def status():
    """
    📈 Check the status of the Solo Server.
    """
    typer.echo("📈 Checking Solo Server status...")
    execute_command(["docker-compose", "-f", "docker-compose.yml", "ps"])

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
