# solo_server/hardware.py
import typer
import os
import sys
import platform
import hashlib
from typing import List

from rich.console import Console
from rich.table import Table
from rich import box

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


def get_hardware_signature(cpu_info: dict, memory_info: dict, disk_info: dict, gpu_info: List[dict]) -> str:
    """
    Generates a unique hardware signature based on system details.

    Args:
        cpu_info (dict): CPU information.
        memory_info (dict): Memory information.
        disk_info (dict): Disk information.
        gpu_info (List[dict]): GPU information.

    Returns:
        str: MD5 hash as the hardware signature.
    """
    signature_data = (
        f"{cpu_info['Processor']}-"
        f"{memory_info['Total']}-"
        f"{disk_info['Total']}"
    )
    if GPUtil and gpu_info and gpu_info[0].get("Name"):
        signature_data += f"-{gpu_info[0]['Name']}"
    return hashlib.md5(signature_data.encode()).hexdigest()


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
    hardware_signature = get_hardware_signature(cpu_info, memory_info, disk_info, gpu_info)
    console.print(f"[bold key]🔑 Solo Server Hardware Signature: {hardware_signature}[/bold key]")
