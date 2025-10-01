# Pytest Cheatsheet

## What is pytest?

A testing framework for Python that makes it easy to write and run tests.

## Installation

```bash
uv add --dev pytest pytest-mock
```

## Running Tests

| Command | What it does |
|---------|-------------|
| `uv run pytest` | Run all tests |
| `uv run pytest -v` | Run with more detail (verbose) |
| `uv run pytest -vv` | Even more detail |
| `uv run pytest tests/test_file.py` | Run one test file |
| `uv run pytest tests/test_file.py::test_name` | Run one specific test |
| `uv run pytest -k "timeout"` | Run tests matching "timeout" in name |
| `uv run pytest -x` | Stop on first failure |
| `uv run pytest --lf` | Run only last failed tests |

## Writing a Basic Test

```python
def test_addition():
    result = 1 + 1
    assert result == 2
```

**Rules:**
- Test files must be named `test_*.py` or `*_test.py`
- Test functions must start with `test_`
- Use `assert` to check results

## Assertions

```python
# Equality
assert x == y
assert x != y

# Comparisons
assert x > y
assert x < y
assert x >= y
assert x <= y

# Contains
assert "hello" in text
assert item in list

# Boolean
assert condition
assert not condition

# Exceptions
with pytest.raises(ValueError):
    some_function()
```

## Parametrize - Run Same Test with Different Inputs

```python
import pytest

@pytest.mark.parametrize("url, expected", [
    ("https://httpbin.org/status/200", "200 OK"),
    ("https://httpbin.org/status/404", "404"),
])
def test_status_codes(url, expected):
    result = check_url(url)
    assert expected in result
```

**Why use this:** Write one test, run it with many different inputs.

## Test Organization

```python
# tests/test_checker.py
def test_feature_one():
    pass

def test_feature_two():
    pass

# tests/test_cli.py  
def test_cli_usage():
    pass
```

**Best practice:** Group related tests in the same file.

## Common Patterns

### Testing That Code Raises Errors

Sometimes you want to check that your code **correctly raises an error** when given bad input.

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError):
        divide(10, 0)
```

**What this tests:** When you call `divide(10, 0)`, it should raise a `ValueError`. The test passes if the error happens.

### Skipping Tests

Sometimes you want to skip a test temporarily:

```python
import pytest

@pytest.mark.skip
def test_send_email():
    # Skip this - email feature not built yet
    pass

@pytest.mark.skip(reason="Database not set up")
def test_database_connection():
    # Skip this - we'll test it later
    pass
```

**When to use:** When a feature isn't ready yet, or you want to focus on other tests first.

### Setup and Teardown

As you write more tests, you'll learn about setting up test data before tests run and cleaning up afterwards. Don't worry about this for now - we'll cover it when you need it.

## Understanding Test Output

### Command: `uv run pytest`

**All tests pass:**
```
======================== test session starts =========================
collected 3 items

tests/test_checker.py ..                                       [ 66%]
tests/test_cli.py .                                            [100%]

========================= 3 passed in 1.23s ==========================
```

Each dot (`.`) represents one passing test.

### Command: `uv run pytest -v`

**All tests pass (with details):**
```
======================== test session starts =========================
collected 3 items

tests/test_checker.py::test_status_code_200 PASSED            [ 33%]
tests/test_checker.py::test_timeout PASSED                    [ 66%]
tests/test_cli.py::test_cli_help PASSED                       [100%]

========================= 3 passed in 1.23s ==========================
```

Now you see each test name.

### When a test fails (any command)

Let's say you have this test code:

```python
def test_addition():
    result = 1 + 1
    assert result == 3  # Wrong! Should be 2
```

**Running `uv run pytest -v` produces:**
```
tests/test_checker.py::test_addition FAILED                   [100%]

========================== FAILURES ===============================
___________________________ test_addition __________________________

    def test_addition():
        result = 1 + 1
>       assert result == 3
E       AssertionError: assert 2 == 3

tests/test_checker.py:3: AssertionError
========================= 1 failed in 0.12s =======================
```

The output tells you:
- ❌ Which test failed: `test_addition`
- 📍 Which file and line: `tests/test_checker.py:3`
- 🔍 What went wrong: `assert 2 == 3`
- 💡 What the actual value was: `2`

## Tips

1. **Test file structure mirrors source code:**
   ```
   src/my_module/checker.py  →  tests/test_checker.py
   src/my_module/cli.py      →  tests/test_cli.py
   ```

2. **Test one thing per test** - Makes failures easier to understand

3. **Use descriptive test names:**
   - Good: `test_timeout_returns_error_message`
   - Bad: `test1`

4. **Test the happy path first** - Make sure normal usage works

5. **Run tests frequently** - Catch problems early

## Quick Reference

```bash
# Install
uv add --dev pytest

# Run all tests
uv run pytest

# Run with details
uv run pytest -v

# Run specific test
uv run pytest tests/test_file.py::test_name

# Stop on first failure
uv run pytest -x
```

---

**Further Reading:**
- [pytest Documentation](https://docs.pytest.org/)
- [pytest Good Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)