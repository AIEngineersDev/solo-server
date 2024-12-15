# solo_server/utils/helpers.py
import typer
from subprocess import run, CalledProcessError
from typing import List, Optional

from rich.console import Console
import logging

console = Console()

# Configure logging
logging.basicConfig(
    filename='solo_server.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

logger = logging.getLogger(__name__)

def execute_command(command: List[str], error_message: str = "Command execution failed", cwd: Optional[str] = None):
    """
    Executes a system command and handles errors.

    Args:
        command (List[str]): The command to execute.
        error_message (str): Custom error message on failure.
        cwd (Optional[str]): Directory to execute the command in.

    Raises:
        typer.Exit: Exits the application if the command fails.
    """
    try:
        run(command, check=True, cwd=cwd)
        logger.info(f"Successfully executed command: {' '.join(command)}")
    except CalledProcessError as e:
        logger.error(f"{error_message}: {e}")
        console.print(f"[bold red]❌ {error_message}: {e}[/bold red]")
        raise typer.Exit(code=1)
