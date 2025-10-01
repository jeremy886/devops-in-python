# Step 4: Testing with pytest

## Overview

Now we'll add tests for our URL checker. We'll test three things:
1. HTTP status codes (200, 404, etc.)
2. Timeout handling
3. CLI behaviour
4. Logging output

Before starting, read [pytest.md](./pytest.md) to understand the basics.

## Installing pytest

```bash
uv add --dev pytest
```

## Project Structure

Create a `tests` directory:

```
devops-in-python/
├── src/
│   └── simple_http_checker/
├── tests/
│   ├── __init__.py
│   ├── test_checker.py
│   ├── test_cli.py
│   └── test_logging.py
└── pyproject.toml
```

## Our Tests

### Test 1: HTTP Status Codes

We use [httpbin.org](https://httpbin.org) - a free testing service that returns any HTTP status code you request.

Create `tests/test_checker.py`:

```python
import pytest
from simple_http_checker.checker import check_urls

@pytest.mark.parametrize(
    "url, expected_prefix",
    [
        ("https://httpbin.org/status/200", "200 OK"),
        ("https://httpbin.org/status/404", "404"),
    ],
)
def test_check_urls_status_codes(url, expected_prefix):
    res = check_urls([url])
    assert res[url].startswith(expected_prefix)

def test_check_urls_timeout():
    slow = "https://httpbin.org/delay/3"
    res = check_urls([slow], timeout=1)
    assert res[slow] == "TIMEOUT"
```

**What we're testing:**
- `/status/200` returns a 200 OK response
- `/status/404` returns a 404 response
- `/delay/3` waits 3 seconds, should timeout at 1 second

### Test 2: CLI Behaviour

Create `tests/test_cli.py`:

```python
from click.testing import CliRunner
from simple_http_checker.cli import main

def test_cli_no_args_shows_usage():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "Usage: check-urls" in result.output

def test_cli_with_url():
    runner = CliRunner()
    result = runner.invoke(main, ["https://httpbin.org/status/200"])
    assert result.exit_code == 0
    assert "Results" in result.output
```

**What we're testing:**
- Running with no arguments shows usage help
- Running with a URL produces results

### Test 3: Logging

Create `tests/test_logging.py`:

```python
from simple_http_checker.checker import check_urls

def test_logging_messages(caplog):
    import logging
    
    # Capture logs from our specific logger at INFO level
    caplog.set_level(logging.INFO, logger="simple_http_checker.checker")
    
    url = "https://httpbin.org/status/200"
    check_urls([url])
    
    # Check the messages
    messages = [rec.message for rec in caplog.records]
    assert any("URL check finished." in m for m in messages)
```

**What we're testing:**
- Our checker logs the completion message

## Running Your Tests

```bash
# Run all tests
uv run pytest

# Run with details
uv run pytest -v

# Run a specific test file
uv run pytest tests/test_checker.py
```

For more pytest commands, see [pytest.md](./pytest.md).

## Why These Tests?

**Real HTTP calls first** - We use actual web requests to httpbin.org because:
- You see real results immediately
- It's concrete and motivating
- You understand what your code actually does

**Later: mocking** - In the future, you'll learn to "mock" these HTTP calls for faster tests. But start with real calls to understand the behaviour first.

## Adding Tests to CI/CD

Now add pytest to your GitHub Actions workflow. Update `.github/workflows/python-ci.yml`:

```yaml
      - name: Run pytest
        run: |
          uv run pytest -v
```

Add this as the last step in your workflow, after the bandit security scan.

**Your complete pipeline now runs:**
1. ✅ Linting (Ruff)
2. ✅ Formatting (Ruff)
3. ✅ Type checking (mypy)
4. ✅ Security (bandit)
5. ✅ Tests (pytest)

Push your code and check the Actions tab on GitHub to see all checks running automatically!

## Next Steps
- Learn about test coverage
- Learn about mocking for faster tests

## Resources

- [pytest.md](./pytest.md) - Your pytest cheatsheet
- [pytest Documentation](https://docs.pytest.org/)
- [Click Testing](https://click.palletsprojects.com/en/stable/testing/)
- [httpbin.org](https://httpbin.org) - HTTP testing service

---

**Last Updated:** October 2025