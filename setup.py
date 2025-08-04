#!/usr/bin/env python3
"""
Setup script for PyTo-Do
Allows creating distributable packages (.exe, .deb, etc.)
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
with open("README.MD", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements if any
def read_requirements():
    """Read requirements from requirements.txt if it exists"""
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return requirements

setup(
    name="pytodo-cli",
    version="1.1.0",
    author="mdnoyon9758",
    author_email="mdnoyon9758@gmail.com",
    description="A simple yet powerful task management app built with pure Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mdnoyon9758/PyTo-Do",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "pytodo=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "assets/*"],
    },
    keywords="todo, task-manager, cli, productivity",
    project_urls={
        "Bug Reports": "https://github.com/mdnoyon9758/PyTo-Do/issues",
        "Source": "https://github.com/mdnoyon9758/PyTo-Do",
        "Documentation": "https://github.com/mdnoyon9758/PyTo-Do#readme",
    },
)
