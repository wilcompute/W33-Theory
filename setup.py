#!/usr/bin/env python3
"""Setup script for W33 Theory of Everything package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="w33-theory",
    version="1.0.0",
    author="Wil Dahn",
    description="A Complete Mathematical Framework Unifying All of Physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wilcompute/W33-Theory",
    packages=find_packages(include=["src", "src.*", "scripts", "scripts.*"]),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "sympy>=1.9",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-json-report>=1.5.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="physics mathematics theory finite-fields algebraic-geometry",
)
