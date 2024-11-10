<div align='center'>

# Simple server for compound AI    

<img alt="Lightning" src="assets/SoloServerBanner.png" width="800px" style="max-width: 100%;">

&nbsp;

Simple. Private. Effective.    
</div>

----

Solo Server is a flexible and privacy-first server framework designed for hosting AI models locally and securely. Built with on-device model deployment in mind, Solo Server allows you to set up, manage, and serve AI-powered endpoints with ease, whether you're working with language models, computer vision, audio processing, or multimodal applications.

## Features

- **Seamless Setup:** Manage your server and configure settings with CLI.
- **Ready-to-Use Templates:** Pre-built for language models, computer vision, audio, tabular data, and more.
- **Cross-Platform Compatibility:** Effortlessly deploy across any platform.
- **Extensible Framework:** Easily expand to support new AI models and workflows.

## Quickstart

Requires Python 3.8 or higher.

1. Install Core Package

```bash
pip install solo-server
```

2. Start the Server with a Template

```bash
solo-server start llm  # For language model template
solo-server start vision  # For computer vision template
solo-server start basic  # For basic template
```

Your server should now be running at `http://localhost:8000`.

## Templates

Solo Server provides several templates to kickstart your project:

- **basic**: A minimal project setup with simple mathematical operations.
- **llm**: Language models using Llama 3.2B Instruct model.
- **vision**: Computer vision using ViT model for image classification.
- **huggingface**: Direct integration with Hugging Face models.
- **compound**: Multi-modal setup combining text, vision, and audio capabilities.

## Core Commands

- **`solo-server start [template]`**: Start the server with specified template.
- **`solo-server stop`**: Stop the running server.
- **`solo-server status`**: Check server status.
- **`solo-server --help`**: Display help information.

## Docker Support

Run the server using Docker:

```bash
PYTHON_FILE=templates/llm.py docker-compose up --build
```

The server will be available at `http://localhost:8000` and logs will be displayed automatically.

## Development

For local development:

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
solo-server start [template]
```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Development

For local development, we recommend using `uv` for dependency management:

1. Install `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv pip install -e .
   ```

3. Activate the virtual environment:
   ```bash
   . .venv/bin/activate
   ```

4. Run the server:
   ```bash
   solo-server start
   ```
