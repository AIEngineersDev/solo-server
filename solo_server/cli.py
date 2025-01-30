import typer
from solo.setup import interactive_setup
from solo.commands import pull, serve, stop, status, benchmark

app = typer.Typer()

# Commands
app.command()(pull.pull)
app.command()(serve.serve)
app.command()(stop.stop)
app.command()(status.status)
app.command()(benchmark.benchmark)
app.command(name="setup")(interactive_setup)

if __name__ == "__main__":
    app()
