from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solo-server",
    version="0.3.4",
    author="Dhruv Diddi",
    author_email="dhruv.diddi@gmail.com",
    description="Powering Physical AI.",
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
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "solo-server=solo_server.cli:app",
        ],
    },
)