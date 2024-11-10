import typer
from solo_server.commands import docker_commands

app = typer.Typer()
app.add_typer(docker_commands.app, name="docker", help="Docker-related commands")

def main():
    app()

if __name__ == "__main__":
    main()