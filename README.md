<div align='center'>

# Simple server for compound AI    

<img alt="Lightning" src="assets/SoloServerBanner.png" width="800px" style="max-width: 100%;">

&nbsp;

Simple. Private. Effective.    
</div>

----

Solo Server is a flexible and privacy-first server framework designed for hosting AI models locally and securely. Built with on-device model deployment in mind, Solo Server allows you to set up, manage, and serve AI-powered endpoints with ease, whether you're working with language models, computer vision, audio processing, or multimodal applications.

## Features

- **Seamless Setup:** Manage your server, initialize projects, install dependencies, and configure settings with CLI.
- **Ready-to-Use Templates:** Pre-built for language models, computer vision, audio, tabular data, and more.
- **Cross-Platform Compatibility:** Effortlessly deploy across any platform, handling a wide range of AI workloads.
- **Extensible Framework:** Easily expand to support new AI models and workflows.

## Quickstart

Requires Python 3.7 or higher.

1. Install Core Package

```bash
pip install solo-server
```

2. Initialize a New Project

Run the `init` command to start a new project. This will guide you through an interactive setup.

```bash
solo-server init
```


<details>
  <summary>Example Interaction</summary>

```bash
Welcome to Solo Server Project Initialization!
----------------------------------------------
Enter your project name [my_project]: solo_project
Choose a project template [basic]: llm
Project 'solo_project' initialized successfully!
```
</details>




3. Navigate to Your Project, Install Dependencies, and Run the Server


```bash
solo-server start
```


Your server should now be running at `http://localhost:5070`.

<details>
  <summary>Test the Server</summary>

Send a POST request to the server or use client.py to test:

   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"prompt": "Hello, world!"}' \
        http://localhost:5070
   ```
</details>


## Templates

Solo Server provides several templates to kickstart your project:

- **basic**: A minimal project setup.
- **llm**: Language models and text processing.
- **vision**: Computer vision projects.
- **audio**: Audio analysis and speech recognition.
- **nlp**: Language analysis (e.g., NER and sentiment analysis).
- **tabular**: Data analysis on tabular datasets.
- **tools**: Tool calling for AI agents such as search, database and cmd execution.
- **compound**: Complex projects involving multiple AI components.

## Use Cases

<details>
  <summary> Dockerizing Solo Server</summary>

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
   docker run -p 5070:5070 my-ai-server
   ```
</details>


<details>
  <summary> NotebookLM (Langauge Model + RAG + Tools)</summary>
  Coming Soon
</details>

<details>
  <summary> Roadio (Vision + Langauge Model + Audio)</summary>
  Coming Soon
</details>

<details>
  <summary> PII Router (Local Langauge Model + Cloud Language Model)</summary>
  Coming Soon
</details>

<details>
  <summary> Llama FS (Langauge Model + Tools)</summary>
   Coming Soon
</details>



## Docs

### Core Commands

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
- **`solo-server help`**: Display help information about commands.


## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
