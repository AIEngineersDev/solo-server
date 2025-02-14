import argparse
import time
from typing import List
from datetime import datetime
from llama_cpp import Llama
from pydantic import BaseModel, Field, field_validator
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import typer

console = Console()

class Message(BaseModel):
    role: str
    content: str

class LlamaResponse(BaseModel):
    model: str
    created_at: datetime
    message: Message
    done: bool
    total_duration: float
    load_duration: float = 0.0
    prompt_eval_count: int = Field(-1, validate_default=True)
    prompt_eval_duration: float = 0.0
    eval_count: int
    eval_duration: float

    @field_validator("prompt_eval_count")
    @classmethod
    def validate_prompt_eval_count(cls, value: int) -> int:
        if value == -1:
            console.print("\n[bold red]Warning:[/] prompt token count was not provided, potentially due to prompt caching.\n")
            return 0
        return value

def load_model(model_path: str) -> (Llama, float):
    console.print(Panel.fit(f"[cyan]Loading model: {model_path}[/]", title="[bold magenta]Solo Server[/]"))
    start_time = time.time()
    model = Llama(model_path=model_path)
    load_duration = time.time() - start_time
    return model, load_duration

def run_benchmark(model: Llama, model_name: str, prompt: str) -> LlamaResponse:
    start_time = time.time()
    response = model(prompt, stop=["\n"], echo=False)
    eval_duration = time.time() - start_time

    message = Message(role="assistant", content=response["choices"][0]["text"])

    return LlamaResponse(
        model=model_name,
        created_at=datetime.now(),
        message=message,
        done=True,
        total_duration=eval_duration,
        eval_count=len(response["choices"][0]["text"].split()),
        eval_duration=eval_duration,
    )

def inference_stats(model_response: LlamaResponse):
    response_ts = model_response.eval_count / model_response.eval_duration
    total_ts = model_response.eval_count / model_response.total_duration

    console.print(
        Panel.fit(
            f"[bold magenta]{model_response.model}[/]\n"
            f"[green]Response:[/] {response_ts:.2f} tokens/s\n"
            f"[blue]Total:[/] {total_ts:.2f} tokens/s\n\n"
            f"[yellow]Stats:[/]\n"
            f" - Response tokens: {model_response.eval_count}\n"
            f" - Model load time: {model_response.load_duration:.2f}s\n"
            f" - Response time: {model_response.eval_duration:.2f}s\n"
            f" - Total time: {model_response.total_duration:.2f}s",
            title="[bold cyan]Benchmark Results[/]",
        )
    )

def average_stats(responses: List[LlamaResponse]):
    if len(responses) == 0:
        console.print("[red]No stats to average.[/]")
        return

    avg_response = LlamaResponse(
        model=responses[0].model,
        created_at=datetime.now(),
        message=Message(role="system", content=f"Average stats across {len(responses)} runs"),
        done=True,
        total_duration=sum(r.total_duration for r in responses) / len(responses),
        load_duration=sum(r.load_duration for r in responses) / len(responses),
        eval_count=sum(r.eval_count for r in responses) // len(responses),
        eval_duration=sum(r.eval_duration for r in responses) / len(responses),
    )
    inference_stats(avg_response)

def benchmark(
    model_path: str = typer.Option("Llama-3.2-1B-Instruct-Q4_K_M.gguf", "-m", help="Path to the Llama model file."),
    prompts: List[str] = typer.Option(["Why is the sky blue?", "Write a report on the financials of Apple Inc."], "-p", help="List of prompts to use for benchmarking."),
):
    console.print("\n[bold cyan]Starting Solo Server Benchmark...[/]")
    model, load_duration = load_model(model_path)
    model_name = model_path.split("/")[-1]
    
    responses: List[LlamaResponse] = []
    for prompt in track(prompts, description="[cyan]Running benchmarks..."):
        response = run_benchmark(model, model_name, prompt)
        responses.append(response)
        inference_stats(response)
    
    average_stats(responses)
