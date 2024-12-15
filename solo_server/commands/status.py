# solo_server/commands/status.py
import typer
from subprocess import run, CalledProcessError
import platform

from rich.console import Console

console = Console()
app = typer.Typer(help="📈 Check the status of the Solo Server.")

@app.command()
def status():
    """
    📈 Check the status of the Solo Server.
    """
    console.print("[bold green]📈 Checking Solo Server status...[/bold green]")
    system = platform.system()
    try:
        if system == "Windows":
            # Use tasklist to find python processes
            output = run(["tasklist"], check=True, stdout=subprocess.PIPE, text=True)
            if "python.exe" in output.stdout:
                console.print("[bold green]✅ Solo Server is running via Cog and LitServe.[/bold green]")
            else:
                console.print("[bold red]❌ Solo Server is not running via Cog and LitServe.[/bold red]")
        else:
            # Use pgrep for Unix-based systems
            output = run(["pgrep", "-fl", "cog serve"], check=True, stdout=subprocess.PIPE, text=True)
            processes = output.stdout.strip().split('\n')
            if processes and processes[0]:
                console.print("[bold green]✅ Solo Server is running via Cog and LitServe.[/bold green]")
                for proc in processes:
                    console.print(f"   - {proc}")
            else:
                console.print("[bold red]❌ Solo Server is not running via Cog and LitServe.[/bold red]")
    except CalledProcessError:
        if system == "Windows":
            console.print("[bold red]❌ Solo Server is not running via Cog and LitServe.[/bold red]")
        else:
            console.print("[bold red]❌ Solo Server is not running via Cog and LitServe.[/bold red]")
