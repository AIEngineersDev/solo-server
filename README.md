# Solo Server

[![PyPI version](https://badge.fury.io/py/solo-server.svg)](https://badge.fury.io/py/solo-server)

**Solo Server** is a command-line tool that simplifies the creation and management of AI model servers for various modalities such as text, images, audio, and video. It provides easy-to-use templates and an interactive setup to help you quickly start projects and deploy AI models without hassle.

## Features

- **Quick Project Initialization**: Start new AI server projects rapidly with built-in templates.
- **Multi-Modality Support**: Templates available for text (LLM), computer vision, audio processing, video processing, tabular data, and more.
- **Interactive CLI**: User-friendly prompts guide you through project setup.
- **Optional Components**: Install only the components you need using pip extras (e.g., `[llm]`, `[cv]`, `[all]`).
- **Simple Server Management**: Easily start, stop, and manage your server with straightforward commands.
- **Extensible Templates**: Customize existing templates or add new ones to suit your specific needs.
- **Deployment Ready**: Package your application into Docker containers for easy deployment.

## Installation

Solo Server requires Python 3.7 or higher.

### Install Core Package

```bash
pip install solo-server
```

### Install with Optional Components

If you need support for specific AI modalities, install the corresponding extras:

- **Language Models (LLM)**:

  ```bash
  pip install solo-server[llm]
  ```

- **Computer Vision (CV)**:

  ```bash
  pip install solo-server[cv]
  ```

- **Audio Processing**:

  ```bash
  pip install solo-server[audio]
  ```

- **All Components**:

  ```bash
  pip install solo-server[all]
  ```

## Getting Started

### Initialize a New Project

Run the `init` command to start a new project. This will guide you through an interactive setup.

```bash
solo-server init
```

**Example Interaction:**

```bash
Welcome to Solo Server Project Initialization!
----------------------------------------------
Enter your project name [my_project]: my_ai_project
Choose a project template [basic]: llm
Project 'my_ai_project' initialized successfully!
```

### Navigate to Your Project

```bash
cd my_ai_project
```

### Install Project Dependencies

```bash
pip install -r requirements.txt
```

### Run the Server

```bash
solo-server start
```

Your server should now be running at `http://localhost:8000`.

## Templates

Solo Server provides several templates to kickstart your project:

- **basic**: A minimal project setup.
- **llm**: Language models and text processing.
- **cv**: Computer vision projects.
- **audio**: Audio analysis and speech recognition.
- **multimodal**: Combining multiple data types (e.g., text and images).
- **tabular**: Data analysis on tabular datasets.
- **video**: Video processing and analysis.
- **compound**: Complex projects involving multiple AI components.

## Core Commands

- **`solo-server init`**: Initialize a new project with an interactive setup.
- **`solo-server start`**: Start the server for the current project.
- **`solo-server stop`**: Stop the running server.
- **`solo-server restart`**: Restart the server.
- **`solo-server status`**: Check the status of the server.
- **`solo-server install`**: Install project dependencies.
- **`solo-server config`**: Manage project configuration.
  - `solo-server config init`: Generate a default configuration file.
  - `solo-server config show`: Display the current configuration.
  - `solo-server config set <parameter> <value>`: Set a configuration parameter.
- **`solo-server generate`**: Generate code snippets or files based on templates.
  - `solo-server generate <type> <name>`: Generate a new component (e.g., `endpoint`, `model`).
- **`solo-server help`**: Display help information about commands.

## Examples

### Example: Creating a Language Model Server

1. **Initialize the Project**

   ```bash
   solo-server init
   ```

   Select the `llm` template.

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**

   ```bash
   solo-server start
   ```

4. **Test the Endpoint**

   Send a POST request to the server:

   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"prompt": "Hello, world!"}' \
        http://localhost:8000
   ```

### Example: Packaging Your Application into a Docker Container

1. **Create a Dockerfile**

   ```dockerfile
   # Dockerfile

   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .

   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["solo-server", "start"]
   ```

2. **Build the Docker Image**

   ```bash
   docker build -t my-ai-server .
   ```

3. **Run the Docker Container**

   ```bash
   docker run -p 8000:8000 my-ai-server
   ```

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
