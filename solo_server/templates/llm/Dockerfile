FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN uv venv
RUN . .venv/bin/activate && uv pip install -e .

EXPOSE 5010 8080

CMD [".venv/bin/python", "src/predict.py"]