#!/usr/bin/env python3
"""
Solo Server CLI: Manage and Benchmark AI Models with Hardware Information.

This script provides a command-line interface (CLI) for managing AI model inference
servers using UV environment management. It includes functionalities to start, stop,
check status, test endpoints, benchmark servers, list available tags, and display
hardware information.

Dependencies:
    - typer
    - rich
    - psutil
    - GPUtil (optional)
    - requests

Usage:
    solo-server --help
"""
import typer
import os
import sys
import platform
import hashlib
from subprocess import run, CalledProcessError
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import box

# Initialize Typer app and Rich console
app = typer.Typer(help="🛠️ Solo Server CLI for managing and benchmarking AI models.")
console = Console()

# Try importing optional dependencies
try:
    import psutil
except ImportError:
    console.print("[red]❌ 'psutil' is not installed. Please install it using `pip install psutil`.[/red]")
    sys.exit(1)

try:
    import GPUtil
except ImportError:
    GPUtil = None
    console.print("[yellow]⚠️ 'GPUtil' is not installed. GPU information will be unavailable. Install it using `pip install gputil`.[/yellow]")

# Check for 'requests' library for testing endpoints
try:
    import requests
except ImportError:
    console.print("[red]❌ 'requests' is not installed. Please install it using `pip install requests`.[/red]")
    sys.exit(1)


def execute_command(command: List[str], error_message: str = "Command execution failed"):
    """
    Executes a system command and handles errors.

    Args:
        command (List[str]): The command to execute.
        error_message (str): Custom error message on failure.

    Raises:
        typer.Exit: Exits the application if the command fails.
    """
    try:
        run(command, check=True)
    except CalledProcessError as e:
        console.print(f"[bold red]❌ {error_message}: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Main entry point for the Solo Server CLI. If no subcommand is provided,
    it defaults to displaying hardware information.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(hardware_info)


@app.command()
def start(
    tag: str = typer.Argument(..., help="Tag of the AI model/template to start.")
):
    """
    🚀 Start the Solo Server for a specific tag using UV.
    """
    console.print(f"[bold green]🌟 Starting Solo Server with tag: {tag}[/bold green]")
    tag_dir = os.path.join("tags", tag)
    app_file = os.path.join(tag_dir, "app.py")
    requirements_file = os.path.join(tag_dir, "requirements.txt")

    if not os.path.exists(app_file):
        console.print(f"[bold red]❌ app.py not found in '{tag_dir}'.[/bold red]")
        raise typer.Exit(code=1)

    console.print("[bold green]🌐 Using UV to manage the environment...[/bold green]")

    # Construct the command for UV
    command = ["uv", "run", "--no-project", app_file]
    if os.path.exists(requirements_file):
        command.extend(["--with", f"requirements={requirements_file}"])

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Starting UV environment...", total=None)
        execute_command(command, f"Failed to start the server for tag '{tag}'")
        progress.update(task, description="UV environment started.")


@app.command()
def stop():
    """
    ⏹ Stop the running Solo Server.
    """
    console.print("[bold green]⏹ Stopping Solo Server...[/bold green]")
    execute_command(["pkill", "-f", "uv run"], "Failed to stop the server")


@app.command()
def status():
    """
    📈 Check the status of the Solo Server.
    """
    console.print("[bold green]📈 Checking Solo Server status...[/bold green]")
    try:
        output = run(["pgrep", "-fl", "uv run"], check=True, stdout=subprocess.PIPE, text=True)
        processes = output.stdout.strip().split('\n')
        if processes and processes[0]:
            console.print("[bold green]✅ Solo Server is running via UV.[/bold green]")
            for proc in processes:
                console.print(f"   - {proc}")
        else:
            console.print("[bold red]❌ Solo Server is not running via UV.[/bold red]")
    except CalledProcessError:
        console.print("[bold red]❌ Solo Server is not running via UV.[/bold red]")


@app.command()
def test(tag: str):
    """
    🧪 Test the endpoint for a specific tag.
    """
    console.print(f"[bold green]🧪 Testing endpoint for tag: {tag}...[/bold green]")
    try:
        response = requests.post(
            "http://localhost:5070/",
            json={"content": "Describe this image in detail please."}
        )
        response.raise_for_status()
        console.print(f"[bold green]✅ Test Passed. Response: {response.json()}[/bold green]")
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]❌ Test Failed: {e}[/bold red]")


@app.command()
def benchmark(tag: str):
    """
    🚦 Benchmark the server for a specific tag using Locust.
    """
    console.print(f"[bold green]🚦 Benchmarking server for tag: {tag}...[/bold green]")
    tag_dir = os.path.join("tags", tag)
    locust_file = os.path.join(tag_dir, "locustfile.py")

    if not os.path.exists(locust_file):
        console.print(f"[bold red]❌ locustfile.py not found in '{tag_dir}'.[/bold red]")
        raise typer.Exit(code=1)

    # Run Locust benchmark
    execute_command(["locust", "-f", locust_file, "--host=http://localhost:5070"], "Failed to run benchmark")


@app.command()
def list_tags():
    """
    📋 List all available tagged templates.
    """
    console.print("[bold green]📋 Available Tags:[/bold green]")
    tags_dir = "tags"
    if not os.path.exists(tags_dir):
        console.print(f"[bold red]❌ Tags directory '{tags_dir}' not found.[/bold red]")
        raise typer.Exit(code=1)

    tags = [tag for tag in os.listdir(tags_dir) if os.path.isdir(os.path.join(tags_dir, tag))]
    if not tags:
        console.print("[bold red]❌ No tags found in the 'tags' directory.[/bold red]")
    else:
        table = Table(title="Available Tags", box=box.SIMPLE_HEAVY)
        table.add_column("Tag", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")
        # Assuming each tag directory has a description.txt file
        for tag in tags:
            description_file = os.path.join(tags_dir, tag, "description.txt")
            if os.path.exists(description_file):
                with open(description_file, "r") as f:
                    description = f.read().strip()
            else:
                description = "No description available."
            table.add_row(tag, description)
        console.print(table)


@app.command()
def hardware_info():
    """
    🖥️ Display comprehensive hardware information.
    """
    console.print("[bold green]🖥️ Retrieving hardware information...[/bold green]")

    # CPU Information
    cpu_info = {
        "Processor": platform.processor() or platform.machine(),
        "Physical Cores": str(psutil.cpu_count(logical=False)),
        "Total Cores": str(psutil.cpu_count(logical=True)),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f} Mhz" if psutil.cpu_freq() else "N/A",
        "Min Frequency": f"{psutil.cpu_freq().min:.2f} Mhz" if psutil.cpu_freq() else "N/A",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f} Mhz" if psutil.cpu_freq() else "N/A",
        "CPU Usage": f"{psutil.cpu_percent()}%",
    }

    # Memory Information
    virtual_mem = psutil.virtual_memory()
    memory_info = {
        "Total": f"{virtual_mem.total / (1024 ** 3):.2f} GB",
        "Available": f"{virtual_mem.available / (1024 ** 3):.2f} GB",
        "Used": f"{virtual_mem.used / (1024 ** 3):.2f} GB",
        "Percentage": f"{virtual_mem.percent}%",
    }

    # Disk Information
    disk = psutil.disk_usage("/")
    disk_info = {
        "Total": f"{disk.total / (1024 ** 3):.2f} GB",
        "Free": f"{disk.free / (1024 ** 3):.2f} GB",
        "Used": f"{disk.used / (1024 ** 3):.2f} GB",
        "Percentage": f"{disk.percent}%",
    }

    # GPU Information
    gpu_info = []
    if GPUtil:
        gpus = GPUtil.getGPUs()
        if gpus:
            for gpu in gpus:
                gpu_info.append({
                    "Name": gpu.name,
                    "Load": f"{gpu.load * 100:.2f}%",
                    "Free Memory": f"{gpu.memoryFree} MB",
                    "Used Memory": f"{gpu.memoryUsed} MB",
                    "Total Memory": f"{gpu.memoryTotal} MB",
                    "Temperature": f"{gpu.temperature} °C" if gpu.temperature else "N/A",
                })
        else:
            gpu_info.append({"Name": "No GPUs detected.", "Load": "-", "Free Memory": "-", "Used Memory": "-", "Total Memory": "-", "Temperature": "-"})
    else:
        gpu_info.append({"Name": "GPUtil not installed.", "Load": "-", "Free Memory": "-", "Used Memory": "-", "Total Memory": "-", "Temperature": "-"})

    # Display CPU Information
    cpu_table = Table(title="🖥️ CPU Information", box=box.ROUNDED, style="cyan")
    cpu_table.add_column("Attribute", style="magenta", no_wrap=True)
    cpu_table.add_column("Details", style="green")
    for key, value in cpu_info.items():
        cpu_table.add_row(key, value)
    console.print(cpu_table)

    # Display Memory Information
    memory_table = Table(title="💾 Memory Information", box=box.ROUNDED, style="cyan")
    memory_table.add_column("Attribute", style="magenta", no_wrap=True)
    memory_table.add_column("Details", style="green")
    for key, value in memory_info.items():
        memory_table.add_row(key, value)
    console.print(memory_table)

    # Display Disk Information
    disk_table = Table(title="📀 Disk Information", box=box.ROUNDED, style="cyan")
    disk_table.add_column("Attribute", style="magenta", no_wrap=True)
    disk_table.add_column("Details", style="green")
    for key, value in disk_info.items():
        disk_table.add_row(key, value)
    console.print(disk_table)

    # Display GPU Information
    gpu_table = Table(title="🎮 GPU Information", box=box.ROUNDED, style="cyan")
    gpu_table.add_column("Attribute", style="magenta", no_wrap=True)
    gpu_table.add_column("Details", style="green")
    for gpu in gpu_info:
        for key, value in gpu.items():
            gpu_table.add_row(key, value)
    console.print(gpu_table)

    # Generate Hardware Signature
    signature_data = (
        f"{cpu_info['Processor']}-"
        f"{memory_info['Total']}-"
        f"{disk.total}"
    )
    if GPUtil and gpu_info and gpu_info[0].get("Name"):
        signature_data += f"-{gpu_info[0]['Name']}"
    hardware_signature = hashlib.md5(signature_data.encode()).hexdigest()
    console.print(f"[bold key]🔑 Solo Server Hardware Signature: {hardware_signature}[/bold key]")


if __name__ == "__main__":
    app()
