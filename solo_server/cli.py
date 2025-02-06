import typer
from .commands import run, stop, status
from .start import start    
app = typer.Typer()

# Commands
app.command()(run.run)
app.command()(stop.stop)
app.command()(status.status)
app.command()(start)

if __name__ == "__main__":
    app()
