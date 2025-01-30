import typer
import subprocess
import json

def benchmark(model: str, output_format: str = "md"):
    """
    Runs Llama-Bench with specified parameters.
    """
    typer.echo(f"⏳ Running Llama-Bench for model: {model}")

    command = [
        "./llama-bench",
        "-m", model,
        "-o", output_format
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        typer.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Benchmark failed: {e.stderr}", err=True)
