# Solo Server

<div align="center">

<img src="assets/logo/logo.png" alt="Solovision Logo" width="200"/>

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/pypi/l/solo-server)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/solo-server)](https://pypi.org/project/solo-server/)
[![PyPI - Version](https://img.shields.io/pypi/v/solo-server)](https://pypi.org/project/solo-server/)

</div>

Solo Server is a lightweight platform that enables users to manage and monitor AI models on their hardware.

<div align="center">
  <img src="assets/logo/solostart.gif" alt="SoloStart">
</div>

## Features

- **Seamless Setup:** Manage your on device AI with a simple CLI and HTTP servers
- **Open Model Registry:** Pull models from registries like Hugging Face and Ollama
- **Lean Load Testing:** Built-in commands to benchmark endpoints
- **Cross-Platform Compatibility:** Deploy AI models effortlessly on your hardware
- **Configurable Framework:** Auto-detect hardware (CPU, GPU, RAM) and sets configs

## Supported Models
Solo Server supports **multiple model sources**, including **Ollama, Hugging Face, and Ramalama**.

| **Model Name**         | **Source**                                                |
|------------------------|----------------------------------------------------------|
| **DeepSeek R1**        | `ollama://deepseek-r1`                                   |
| **IBM Granite 3.1**    | `ollama://granite3.1-dense`                              |
| **Granite Code 8B**    | `hf://ibm-granite/granite-8b-code-base-4k-GGUF`          |
| **Granite Code 20B**   | `hf://ibm-granite/granite-20b-code-base-8k-GGUF`         |
| **Granite Code 34B**   | `hf://ibm-granite/granite-34b-code-base-8k-GGUF`         |
| **Mistral 7B**         | `hf://TheBloke/Mistral-7B-Instruct-v0.2-GGUF`            |
| **Mistral 7B v3**      | `hf://MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF`       |
| **Hermes 2 Pro**       | `hf://NousResearch/Hermes-2-Pro-Mistral-7B-GGUF`        |
| **Cerebrum 1.0 7B**    | `hf://froggeric/Cerebrum-1.0-7b-GGUF`                    |
| **Dragon Mistral 7B**  | `hf://llmware/dragon-mistral-7b-v0`  

## Table of Contents

- [Features](#-features)
- [Supported Models](#supported-models)
- [Installation](#installation)
- [Commands](#commands)
- [Configuration](#configuration)
- [Project Inspiration](#project-inspiration)

## Installation

### **🔹 Install via PyPI**
```sh
pip install solo-server
```

### **🔹 Install with `uv` (Recommended)**
```sh
curl -sSL https://getsolo.tech/install.sh | bash
```
Creates an isolated environment using `uv` for performance and stability.  

Run the **interactive setup** to configure Solo Server:
```sh
solo setup
```
### **🔹 Setup Features**
✔️ **Detects CPU, GPU, RAM** for **hardware-optimized execution**  
✔️ **Auto-configures `solo.conf` with optimal settings**  
✔️ **Requests API keys for Ngrok and Replicatea**  
✔️ **Recommends the compute backend OCI (CUDA, HIP, SYCL, Vulkan, CPU, Metal)**  

---

## **Commands**
### **1️⃣ Pull a Model**
```sh
solo pull llama3
```
 

---

### **2️⃣ Serve a Model**
```sh
solo serve llama3
```

**Access the UI at:**  
```sh
http://127.0.0.1:5070  #SOLO_SERVER_PORT
```

---

### **3️⃣ Benchmark a Model**
```sh
solo benchmark llama3
```


**Example Output:**
```sh
Running benchmark for llama3...
🔹 Model Size: 7B
🔹 Compute Backend: CUDA
🔹 Prompt Processing Speed: 1450 tokens/s
🔹 Text Generation Speed: 135 tokens/s

Running classification accuracy test...
🔹 Batch 0 Accuracy: 0.7300
🔹 Batch 1 Accuracy: 0.7520
🔹 Batch 2 Accuracy: 0.7800
🔹 Overall Accuracy: 0.7620

Running additional benchmarks...
🔹 F1 Score: 0.8150
🔹 Confusion Matrix:
tensor([[10,  2,  1,  0,  0],
        [ 1, 12,  0,  0,  0],
        [ 0,  0, 11,  0,  1],
        [ 0,  0,  0, 13,  0],
        [ 0,  0,  0,  0, 15]])
Benchmarking complete!
```

---

### **4️⃣ Check Model Status**
```sh
solo status
```
**Example Output:**
```sh
🔹 Running Models:
-------------------------------------------
| Name      | Model   | Backend | Port |
|----------|--------|---------|------|
| llama3   | Llama3 | CUDA    | 8080 |
| gptj     | GPT-J  | CPU     | 8081 |
-------------------------------------------
```

---

### **5️⃣ Stop a Model**
```sh
solo stop llama3
```
**Example Output:**
```sh
Stopping llama3...
llama3 stopped successfully.
```

---

## **⚙️ Configuration (`solo.conf`)**
After setup, all settings are stored in:
```sh
~/.solo/solo.conf
```
Example:
```ini
# Solo Server Configuration

MODEL_REGISTRY=ramalama
MODEL_PATH=/home/user/solo/models
COMPUTE_BACKEND=CUDA
SERVER_PORT=5070
LOG_LEVEL=INFO

# Hardware Detection
CPU_MODEL="Intel i9-13900K"
CPU_CORES=24
MEMORY_GB=64
GPU_VENDOR="NVIDIA"
GPU_MODEL="RTX 3090"

# API Keys
NGROK_API_KEY="your-ngrok-key"
REPLICATE_API_KEY="your-replicate-key"
```
✅ **Modify this file anytime and run:**
```sh
solo setup
```

---

## 📝 Project Inspiration 

This project wouldn't be possible without the help of other projects like:

* uv
* llama.cpp
* ramalama
* ollama
* whisper.cpp
* vllm
* podman
* huggingface
* llamafile
* cog

Like using Solo, consider leaving us a ⭐ on GitHub
