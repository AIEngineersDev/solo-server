import typer
from solo_server.commands import docker_commands

app = typer.Typer()

# Add other commands here...

# Add Docker commands
app.add_typer(docker_commands.app, name="docker", help="Docker-related commands")

if __name__ == "__main__":
    app()