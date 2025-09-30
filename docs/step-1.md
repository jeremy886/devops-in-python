# Step 1: Building a Simple HTTP URL Checker

## What We Built

A command-line tool that checks the HTTP status of URLs using Python, Click, and Requests.

## Project Structure

```
devops-in-python/
├── src/
│   └── simple_http_checker/
│       ├── __init__.py
│       ├── checker.py    # Core HTTP checking logic
│       └── cli.py        # Click-based CLI interface
├── docs/
├── pyproject.toml        # Project configuration
└── README.md
```

## Setup

### Prerequisites
- Python 3.12+
- uv (Python package manager)

### Installation

```bash
# Install dependencies and the package in editable mode
uv pip install -e .
```

## Usage

### Basic URL Check
```bash
uv run check-urls https://www.google.com
```

### Check Multiple URLs
```bash
uv run check-urls https://www.google.com https://github.com https://example.com
```

### With Custom Timeout
```bash
uv run check-urls https://www.google.com --timeout 10
```

### Verbose Mode
```bash
uv run check-urls https://www.google.com -v
```

## Key Configuration: pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "devops-in-python"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "click>=8.3.0",
    "requests>=2.32.5",
]

[project.scripts]
check-urls = "simple_http_checker.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/simple_http_checker"]
```

## Key Learnings

1. **Package Structure**: Using `src/` layout keeps source code organised and separate from tests/docs
2. **Entry Points**: `[project.scripts]` creates console commands that can be run after installation
3. **Hatchling Configuration**: The `[tool.hatch.build.targets.wheel]` section tells the build system where to find packages
4. **uv Workflow**: `uv run` automatically manages the virtual environment - no need to activate/deactivate

## Common Issues

### Command Not Found
If `check-urls` alone doesn't work, use `uv run check-urls` instead. This ensures the command runs in the correct virtual environment.

### Build Errors
Make sure `[tool.hatch.build.targets.wheel]` points to your actual package location in the `src/` directory.

