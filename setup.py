from setuptools import setup, find_packages

setup(
    name="solo-server",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "typer",
        "litserve",
    ],
    entry_points={
        "console_scripts": [
            "solo-server=solo_server.cli:main",
        ],
    },
    package_data={
        "solo_server": ["templates/**/*"],
    },
    python_requires=">=3.8",
)