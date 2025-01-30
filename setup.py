from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solo-server",
    version="0.3.5",
    author="Dhruv Diddi",
    author_email="dhruv.diddi@gmail.com",
    description="AIOps for the Physical World.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIEngineersDev/solo-server",
    packages=find_packages(include=["solo_server", "solo_server.*"]),
    include_package_data=True,
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