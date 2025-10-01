# Step 3: Type Checking & Security Scanning

## Overview

In this step, we add type checking with mypy and security scanning with bandit to catch bugs and security issues early.

## What Are We Adding?

**mypy** - Checks if you're using the correct data types in your code
- Catches bugs before runtime (e.g., passing a string when a number is expected)
- Makes code easier to understand and maintain
- Optional: you can add types gradually

**bandit** - Scans for common security issues
- Finds hardcoded passwords, insecure functions, SQL injection risks
- Checks against OWASP Top 10 security issues
- Fast and easy to run

## Installing the Tools

Add mypy and bandit as development dependencies:

```bash
uv add --dev mypy bandit
```

Some libraries (like `requests`) don't include type hints, so we need to install type stubs:

```bash
uv add --dev types-requests
```

Your `pyproject.toml` will be updated:

```toml
[dependency-groups]
dev = [
    "ruff>=0.13.2",
    "mypy>=1.13.0",
    "bandit>=1.8.0",
    "types-requests>=2.32.0",
]
```

**Note:** If mypy complains about missing stubs for other libraries, install them with `uv add --dev types-<library-name>`.

## Configuring mypy

Add mypy configuration to your `pyproject.toml`:

```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false  # Set to true when you're ready for strict typing
```

**What this means:**
- `python_version` - Check code for Python 3.12
- `warn_return_any` - Warn when functions return `Any` type (too vague)
- `warn_unused_configs` - Tell us if we have unused settings
- `disallow_untyped_defs = false` - Allow functions without type hints (good for learning)

## Configuring bandit

Add bandit configuration to your `pyproject.toml`:

```toml
[tool.bandit]
exclude_dirs = ["tests", "venv", ".venv", "__pycache__", "build", "dist"]
```

## Adding Type Hints to Your Code

Here's how to add type hints to your existing code:

**Before (no types):**
```python
def check_url(url, timeout):
    response = requests.get(url, timeout=timeout)
    return response.status_code
```

**After (with types):**
```python
def check_url(url: str, timeout: int) -> int:
    response = requests.get(url, timeout=timeout)
    return response.status_code
```

**Start simple** - Add types to new code first, then gradually add to existing code.

## Running Checks Locally

**Type checking:**
```bash
uv run mypy src/
```

**Security scanning:**
```bash
uv run bandit -r src/
```

**Run all checks together:**
```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy src/ && uv run bandit -r src/
```

## Updating the CI/CD Workflow

Update `.github/workflows/python-ci.yml` to include the new checks:

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

      - name: Run mypy type checking
        run: |
          uv run mypy src/

      - name: Run bandit security scan
        run: |
          uv run bandit -r src/
```

## Understanding the Results

### mypy Output

**Success:**
```
Success: no issues found in 3 source files
```

**Type error example:**
```
src/simple_http_checker/checker.py:10: error: Argument 1 to "get" has incompatible type "int"; expected "str"
```
This tells you exactly where the problem is and what's wrong.

### bandit Output

**No issues:**
```
Run started
Test results:
    No issues identified.
```

**Security issue example:**
```
>> Issue: [B105:hardcoded_password_string] Possible hardcoded password: 'mysecret123'
   Severity: Low   Confidence: Medium
```

## What Happens When You Push

GitHub Actions will now run 4 checks:
1. ✅ Ruff linting
2. ✅ Ruff formatting
3. ✅ mypy type checking
4. ✅ bandit security scanning

All must pass (green ✅) before your code is considered good to merge.

## Common Issues You Might See

**mypy: "Library stubs not installed for X"**
- Some libraries don't include type hints
- Install the type stubs: `uv add --dev types-<library-name>`
- Example: `uv add --dev types-requests`

**bandit: False positives**
- Sometimes bandit flags safe code
- Review the issue and decide if it's real
- You can skip specific checks if needed (add to `skips` in config)

## Why This Matters

**Type checking catches:**
- Passing wrong types to functions
- Typos in variable names
- Using methods that don't exist

**Security scanning catches:**
- Hardcoded passwords or secrets
- Using insecure functions (like `eval()`)
- SQL injection vulnerabilities
- Weak cryptography

Both help you write better, safer code!

## Next Steps

- Add unit tests with pytest
- Add test coverage reporting
- Learn more about Python type hints

## Resources

- [mypy Documentation](https://mypy.readthedocs.io/)
- [bandit Documentation](https://bandit.readthedocs.io/)
- [Python Type Hints Guide](https://docs.python.org/3/library/typing.html)

---

**Last Updated:** October 2025