#!/usr/bin/env python
"""
Setup script for Code Index MCP Server
"""

from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
def read_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README
def read_readme():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "Code Index MCP Server"

setup(
    name="code-index-mcp",
    version="1.0.0",
    description="A Model Context Protocol (MCP) server for code indexing and analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/apermatigari/code-index-mcp",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "code-index-mcp=code_index_mcp.server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="mcp, model-context-protocol, code-indexing, code-analysis",
    project_urls={
        "Bug Reports": "https://github.com/apermatigari/code-index-mcp/issues",
        "Source": "https://github.com/apermatigari/code-index-mcp",
    },
) 