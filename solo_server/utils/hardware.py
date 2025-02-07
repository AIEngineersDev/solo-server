import platform
import psutil
import GPUtil
import subprocess
from typing import Tuple

def detect_hardware() -> Tuple[str, int, float, str, str, float, str, str]:
    #OS Info
    os = platform.system()
    
    # CPU Info
    cpu_model = "Unknown"
    cpu_cores = psutil.cpu_count(logical=False)
    
    if os == "Windows":
        cpu_model = platform.processor()
    elif os == "Linux":
        try:
            cpu_model = subprocess.check_output("lscpu | grep 'Model name'", shell=True, text=True).split(":")[1].strip()
        except:
            cpu_model = "Unknown Linux CPU"
    elif platform.system() == "Darwin":
        try:
            cpu_model = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True, text=True).strip()
        except:
            cpu_model = "Unknown Mac CPU"
    
    # Memory Info
    memory_gb = round(psutil.virtual_memory().total / (1024**3), 2)
    
    # GPU Info
    gpu_vendor = "None"
    gpu_model = "None"
    compute_backend = "CPU"
    gpu_memory = 0

    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]  # Get first GPU
        gpu_model = gpu.name
        gpu_memory = round(gpu.memoryTotal, 2)  # GPU memory in GB
        if "NVIDIA" in gpu_model:
            gpu_vendor = "NVIDIA"
            compute_backend = "CUDA"
        elif "AMD" in gpu_model:
            gpu_vendor = "AMD"
            compute_backend = "HIP"
        elif "Intel" in gpu_model:
            gpu_vendor = "Intel"
            compute_backend = "OpenCL"
        elif "Apple Silicon" in gpu_model:
            gpu_vendor = "Apple Silicon"
            compute_backend = "Metal"
        else:
            gpu_vendor = "Unknown"
            compute_backend = "CPU"

    return cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, gpu_memory, compute_backend, os

def display_hardware_info(typer):
    cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, gpu_memory, compute_backend, os = detect_hardware()
    
    typer.echo("------------------------------->")
    typer.echo("🖥️  System Information")
    typer.echo(f"Operating System: {os}")
    typer.echo(f"CPU: {cpu_model}")
    typer.echo(f"CPU Cores: {cpu_cores}")
    typer.echo(f"Memory: {memory_gb}GB")
    typer.echo(f"GPU: {gpu_vendor}")
    typer.echo(f"GPU Model: {gpu_model}")
    typer.echo(f'GPU Memory: {gpu_memory}GB')
    typer.echo(f"Compute Backend: {compute_backend}")
    