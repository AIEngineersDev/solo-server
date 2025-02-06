import typer
import subprocess
from solo_server.utils.hardware import display_hardware_info
from tabulate import tabulate
import json

app = typer.Typer()

@app.command()
def status():
    """Check running models and system status."""
    display_hardware_info(typer)
    
    # Check for running solo container
    container_result = subprocess.run(["docker", "ps", "-f", "name=solo", "--format", "{{json .}}"],
                                    capture_output=True, text=True, check=True)
    
    if container_result.stdout.strip():
        # Container is running, show available models
        typer.echo("\n🔍 Available Models:")
        models_result = subprocess.run(["docker", "exec", "solo", "ollama", "list"], 
                                     capture_output=True, text=True, check=True)
        models = []
        for line in models_result.stdout.strip().split('\n'):
            parts = line.split()
            if len(parts) >= 7:
                size = f"{parts[2]} {parts[3]}"
                modified = f"{parts[4]} {parts[5]} {parts[6]}"
                models.append([parts[0], parts[1], size, modified])

        if models:
            print(tabulate(models, headers=['NAME', 'ID', 'SIZE', 'MODIFIED'], tablefmt='grid'))
    
    # Show running containers section (will be empty if none running)
    typer.echo("\n🔍 Running Containers:")
    containers = []
    if container_result.stdout.strip():
        for line in container_result.stdout.strip().split('\n'):
            container = json.loads(line)
            containers.append([
                container['Names'],
                container['Status'],
                container['Ports']
            ])
    
    print(tabulate(containers, headers=['NAME', 'STATUS', 'PORTS'], tablefmt='grid'))
