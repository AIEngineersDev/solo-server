from setuptools import setup, find_packages

setup(
    name="solo-server",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "GPUtil",
        "psutil",
        "tqdm",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "solo-server = solo_server.main:app",
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