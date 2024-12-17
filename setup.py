from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solo-server",
    version="0.3.1",
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
            '__init__.py',
            'cli.py',
            'solo_server.log',
            'utils/*.py'
        ],
        'tags': [
            'toy-hello-world',
            'sample-tag',
            'test-model'
        ],
        'tests': [
            'test_server.py',
            'test_utils.py'
        ]
    },
    install_requires=[
        "typer>=0.4.0",
        "rich>=12.0.0",
        "psutil>=5.9.0",
        "requests>=2.28.0",
        "gputil>=1.4.0",  # Optional
        "litserve==0.1.0",
        "cog",
        "fastapi",
        "uvicorn",
        "pydantic",
        "torch==2.3",
        "locust",
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
            "solo-server=solo_server.cli:app",
        ],
    },
)