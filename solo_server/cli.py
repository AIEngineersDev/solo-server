import typer
from .commands import run, serve, stop, status
from .setup import start    
app = typer.Typer()

# Commands
app.command()(run.run)
app.command()(stop.stop)
app.command()(status.status)
app.command()(serve.serve)
app.command()(start)

if __name__ == "__main__":
    app()
