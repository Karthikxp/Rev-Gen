#!/usr/bin/env python3
"""
Setup script for RevGen - Reverse Shell Genie
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="revgen",
    version="1.0.0",
    author="Karthik M",
    author_email="karthik@example.com",  # Replace with actual email
    description="🧞‍♂️ Reverse Shell Genie - Your magical spellbook for terminal takeovers",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/karthikm/revgen",  # Replace with actual repo URL
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["shells.json", "*.md", "*.txt"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Penetration Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "optional": [
            "qrcode[pil]>=7.0",  # For QR code generation
            "requests>=2.25.0",  # For enhanced web features
        ],
    },
    entry_points={
        "console_scripts": [
            "revgen=revgen:main",
        ],
    },
    keywords=[
        "security", "penetration-testing", "reverse-shell", "payload", 
        "cli", "hacking", "cybersecurity", "red-team", "ctf"
    ],
    project_urls={
        "Bug Reports": "https://github.com/karthikm/revgen/issues",
        "Source": "https://github.com/karthikm/revgen",
        "Documentation": "https://github.com/karthikm/revgen#readme",
    },
    zip_safe=False,
)
