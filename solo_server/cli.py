import typer
from .commands import pull, serve, stop, status, benchmark
from .setup import interactive_setup    
app = typer.Typer()

# Commands
app.command()(pull.pull)
app.command()(serve.serve)
app.command()(stop.stop)
app.command()(status.status)
app.command()(benchmark.benchmark)
app.command()(interactive_setup)

if __name__ == "__main__":
    app()
