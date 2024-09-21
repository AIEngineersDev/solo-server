from setuptools import setup, find_packages
import os 
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('solo_server/templates')


setup(
    name="solo-server",
    version="0.1.4",
    packages=find_packages(include=['solo_server', 'solo_server.*']),
    include_package_data=True,
    package_data={
        'solo_server': extra_files,
    },
    install_requires=[
        "typer",
        "GPUtil",
        "psutil",
        "tqdm",
        "requests",
        "argparse"  # Added this as it's used in cli.py
    ],
    entry_points={
        "console_scripts": [
            "solo-server = solo_server.cli:main",  # Updated this line
        ],
    },
    author="Dhruv Diddi",
    author_email="dhruv.diddi@gmail.com",
    description="Simple server to manage compound AI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AIEngineersDev/solo-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)