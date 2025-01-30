import typer
import os
import configparser
import platform
import subprocess

CONFIG_FILE = os.path.expanduser("~/.solo/solo.conf")

def detect_hardware():
    """
    Detects system hardware (CPU, GPU, RAM) and suggests optimal configurations.
    """
    typer.echo("🖥️ Detecting hardware specifications...")

    # Detect CPU
    cpu_model = "Unknown"
    cpu_cores = os.cpu_count() or 1

    if platform.system() == "Windows":
        cpu_model = platform.processor()
    elif platform.system() == "Linux":
        try:
            cpu_model = subprocess.check_output("lscpu | grep 'Model name'", shell=True, text=True).split(":")[1].strip()
        except:
            cpu_model = "Unknown Linux CPU"
    elif platform.system() == "Darwin":
        try:
            cpu_model = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True, text=True).strip()
        except:
            cpu_model = "Unknown Mac CPU"

    # Detect RAM
    memory_gb = "Unknown"
    if platform.system() == "Windows":
        try:
            memory_gb = int(subprocess.check_output("wmic ComputerSystem get TotalPhysicalMemory", shell=True, text=True).split("\n")[1].strip()) // (1024**3)
        except:
            memory_gb = "Unknown"
    elif platform.system() == "Linux":
        try:
            memory_gb = int(subprocess.check_output("free -g | awk '/^Mem:/{print $2}'", shell=True, text=True).strip())
        except:
            memory_gb = "Unknown"
    elif platform.system() == "Darwin":
        try:
            memory_gb = int(subprocess.check_output("sysctl -n hw.memsize", shell=True, text=True)) // (1024**3)
        except:
            memory_gb = "Unknown"

    # Detect GPU
    gpu_vendor = "None"
    gpu_model = "None"

    if platform.system() == "Windows":
        try:
            gpu_info = subprocess.check_output("wmic path win32_VideoController get Name", shell=True, text=True).split("\n")[1].strip()
            if "NVIDIA" in gpu_info:
                gpu_vendor = "NVIDIA"
            elif "AMD" in gpu_info:
                gpu_vendor = "AMD"
            elif "Intel" in gpu_info:
                gpu_vendor = "Intel"
            gpu_model = gpu_info
        except:
            gpu_vendor = "Unknown"
            gpu_model = "Unknown"
    elif platform.system() == "Linux":
        try:
            if subprocess.run("nvidia-smi", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                gpu_vendor = "NVIDIA"
                gpu_model = subprocess.check_output("nvidia-smi --query-gpu=name --format=csv,noheader", shell=True, text=True).split("\n")[0]
            elif subprocess.run("rocm-smi", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                gpu_vendor = "AMD"
                gpu_model = subprocess.check_output("rocm-smi --showproductname | awk -F ': ' '{print $2}'", shell=True, text=True).strip()
            elif subprocess.run("lspci | grep -i vga", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                gpu_vendor = "Intel"
                gpu_model = subprocess.check_output("lspci | grep -i vga | awk -F ': ' '{print $2}'", shell=True, text=True).strip()
        except:
            gpu_vendor = "Unknown"
            gpu_model = "Unknown"
    elif platform.system() == "Darwin":
        try:
            gpu_vendor = "Apple Silicon"
            gpu_model = "Integrated GPU"
        except:
            gpu_vendor = "Unknown"
            gpu_model = "Unknown"

    typer.echo(f"🖥️ CPU: {cpu_model} ({cpu_cores} cores)")
    typer.echo(f"💾 RAM: {memory_gb} GB")
    typer.echo(f"🎮 GPU: {gpu_vendor} - {gpu_model}")

    # Recommend Compute Backend
    if gpu_vendor == "NVIDIA":
        compute_backend = "CUDA"
    elif gpu_vendor == "AMD":
        compute_backend = "HIP"
    elif gpu_vendor == "Intel":
        compute_backend = "SYCL"
    elif gpu_vendor == "Apple Silicon":
        compute_backend = "Metal"
    else:
        compute_backend = "CPU"

    typer.echo(f"⚙️ Recommended Compute Backend: {compute_backend}")

    return cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, compute_backend

def interactive_setup():
    """
    Runs an interactive setup to configure Solo CLI with hardware detection.
    """
    typer.echo("🔧 Welcome to Solo Setup!")
    typer.echo("Let'sconfigure your settings and API keys.")

    # Ensure config directory exists
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

    config = configparser.ConfigParser()
    config["DEFAULT"] = {}

    # Detect hardware
    cpu_model, cpu_cores, memory_gb, gpu_vendor, gpu_model, compute_backend = detect_hardware()

    # User Inputs
    config["DEFAULT"]["MODEL_REGISTRY"] = typer.prompt("🌍 Model registry (ramalama/ollama)", default="ramalama")
    config["DEFAULT"]["MODEL_PATH"] = typer.prompt("📂 Model storage path", default=os.path.expanduser("~/solo/models"))
    config["DEFAULT"]["COMPUTE_BACKEND"] = typer.prompt(f"⚙️ Compute backend (CPU/CUDA/HIP/SYCL/Vulkan) [Recommended: {compute_backend}]", default=compute_backend)
    config["DEFAULT"]["SERVER_PORT"] = typer.prompt("🌐 Server port", default="5070")
    config["DEFAULT"]["LOG_LEVEL"] = typer.prompt("🔍 Logging level (INFO/DEBUG/ERROR)", default="INFO")

    # API Keys
    typer.echo("🔑 Enter API keys (leave blank to skip).")
    config["DEFAULT"]["NGROK_API_KEY"] = typer.prompt("Ngrok API Key", default="", show_default=False)
    config["DEFAULT"]["REPLICATE_API_KEY"] = typer.prompt("Replicate API Key", default="", show_default=False)
    
    # Store detected hardware details
    config["DEFAULT"]["CPU_MODEL"] = cpu_model
    config["DEFAULT"]["CPU_CORES"] = str(cpu_cores)
    config["DEFAULT"]["MEMORY_GB"] = str(memory_gb)
    config["DEFAULT"]["GPU_VENDOR"] = gpu_vendor
    config["DEFAULT"]["GPU_MODEL"] = gpu_model

    # Save to file
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)

    typer.echo("✅ Setup complete! Run `solo --help` to get started.")

if __name__ == "__main__":
    interactive_setup()
