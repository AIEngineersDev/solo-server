from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solo-server",
    version="0.3.0",
    author="Dhruv Diddi",
    author_email="dhruv.diddi@gmail.com",
    description="A simple server for compound AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIEngineersDev/solo-server",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'solo_server': [
            'templates/*.py',
            'gui.py',
            'grafana_setup.sh',
            'locustfile.py',
            'Dockerfile',
            'docker-compose.yml',
            'docker-compose-benchmark.yml',
            'requirements.txt',
            'utils.py',
            'base.py',
        ],
    },
    data_files=[
        ('solo_server', [
            'solo_server/Dockerfile',
            'solo_server/docker-compose.yml',
            'solo_server/requirements.txt'
        ]),
    ],
    install_requires=[
        "typer",
    ],
    extras_require={
        "dev": ["pytest", "black", "isort"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "solo-server=solo_server.base:app",
        ],
    },
)