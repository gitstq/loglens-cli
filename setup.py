"""
Setup script for LogLens-CLI.
"""

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent

long_description = ""
readme_path = here / "README.md"
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="loglens-cli",
    version="1.0.0",
    author="LogLens Team",
    author_email="loglens@example.com",
    description="A lightweight, intelligent terminal log analyzer with interactive TUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/loglens-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "textual>=0.50.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "loglens=loglens.cli:main",
        ],
    },
    keywords="log viewer analyzer terminal tui cli json logfmt debug monitoring",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/loglens-cli/issues",
        "Source": "https://github.com/gitstq/loglens-cli",
        "Documentation": "https://github.com/gitstq/loglens-cli#readme",
    },
)
