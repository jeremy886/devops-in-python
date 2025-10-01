# Step 2: Development Environment & CI/CD Setup

## Overview

In this step, we set up the development environment with code quality tools and configure continuous integration/continuous deployment (CI/CD) pipelines using GitHub Actions.

## Development Environment Setup

### Installing Development Dependencies

Add Ruff as a development dependency:

```bash
uv add --dev ruff
```

This updates your `pyproject.toml`:

```toml
[dependency-groups]
dev = [
    "ruff>=0.13.2",
]
```

### Current pyproject.toml

Here's our complete `pyproject.toml` configuration:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "devops-in-python"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "click>=8.3.0",
    "requests>=2.32.5",
]

[project.scripts]
check-urls = "simple_http_checker.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/simple_http_checker"]

[dependency-groups]
dev = [
    "ruff>=0.13.2",
]
```

We're using Ruff's default configuration for linting and formatting. For Ruff commands and usage, see [ruff.md](./ruff.md).

## CI/CD with GitHub Actions

### Setting Up the Workflow

Create `.github/workflows/python-ci.yml`:

```yaml
name: CI/CD for simple-http-checker

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  lint-static-checks:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Display Python and uv versions
        run: |
          python --version
          uv --version

      - name: Install dependencies
        run: |
          uv sync --all-extras --dev

      - name: Run Ruff linter
        run: |
          uv run ruff check .

      - name: Run Ruff formatter check
        run: |
          uv run ruff format --check .
```

### Workflow Breakdown

**Triggers:**
- `push` - Runs on every push to `main` branch
- `pull_request` - Runs on every pull request targeting `main`
- `workflow_dispatch` - Allows manual triggering from GitHub UI

**Job: lint-static-checks**

| Step | Action | Purpose |
|------|--------|---------|
| Check out repo | `actions/checkout@v5` | Clones the repository |
| Set up Python | `actions/setup-python@v5` | Installs Python 3.12 |
| Install uv | `astral-sh/setup-uv@v4` | Installs uv with caching enabled |
| Display versions | `python --version`, `uv --version` | Shows versions for debugging |
| Install dependencies | `uv sync --all-extras --dev` | Installs all dependencies including dev |
| Run Ruff linter | `uv run ruff check .` | Checks code quality |
| Check formatting | `uv run ruff format --check .` | Verifies code formatting |

### Key Features

**Caching:**
- `enable-cache: true` in the uv setup caches dependencies between runs
- Significantly speeds up workflow execution (typically 30-60 seconds)
- Cache is automatically invalidated when `uv.lock` changes

**Why uv?**
- Extremely fast dependency resolution (10-100x faster than pip)
- Deterministic builds with `uv.lock`
- Built-in virtual environment management
- Better integration with modern Python packaging

**Why Ruff?**
- Written in Rust - 10-100x faster than traditional Python linters
- Combines linting and formatting in one tool
- Compatible with Black formatting style
- Supports over 700 lint rules

## Viewing Workflow Results

### On GitHub

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Click on a workflow run to see details
4. Each step shows logs and execution time

### Understanding Results

**✅ Green checkmark** - All checks passed
**❌ Red X** - One or more checks failed
**🟡 Yellow dot** - Workflow is running

If checks fail:
1. Click on the failed job to see which step failed
2. Expand the failed step to see the error details
3. Fix the issues locally and push again

## What Happens When You Push Code

When you push to GitHub:
1. GitHub Actions automatically runs your workflow
2. It checks your code for quality issues
3. You'll see a ✅ or ❌ in the Actions tab
4. If it fails, read the error message - it tells you exactly what to fix

## Next Steps

- Add automated testing with pytest
- Add test coverage reporting
- Set up deployment workflows

## Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Cheatsheet](./ruff-cheatsheet.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Last Updated:** October 2025