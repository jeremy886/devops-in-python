# Ruff Cheatsheet

## What is Ruff?

- A fast **Python linter + formatter** tool
- Its formatter (`ruff format`) aims to be a drop-in replacement for Black
- Written in Rust - extremely fast!

## Basic Commands

| Command | What it does |
|---------|-------------|
| `ruff format .` | Format all Python files in the current folder in place |
| `ruff format --check .` | Check if files would be formatted (don't write changes) |
| `ruff check .` | Run the linter (detect errors, style issues) |
| `ruff check . --fix` | Run linter + auto-fix what can be fixed |
| `ruff check . --watch` | Run linter in watch mode (re-check on file changes) |

## Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 88

[tool.ruff.format]
quote-style = "double"     # or "single"

[tool.ruff.lint]
select = ["E", "F", "I"]   # Enable specific rule categories
ignore = ["E501"]          # Ignore specific rules
```

**Common configurations:**
- `line-length` controls maximum line length
- `quote-style` picks single vs double quotes
- `select` enables rule categories (E=pycodestyle errors, F=pyflakes, I=isort)
- `ignore` disables specific rules you don't want

## Key Differences vs Black

- Ruff's formatter is **faster** and integrated with linting
- While Ruff mimics Black's style closely, **minor differences exist** (trailing comments, blank lines, multiline strings)
- Ruff's linter + formatter are separate: use **both** (formatter for style, linter for code issues)

## Typical Workflow (with uv)

1. **Add Ruff to your project (dev dependencies):**
   ```bash
   uv add --dev ruff
   ```

2. **Format code:**
   ```bash
   uv run ruff format .
   ```

3. **Check + fix linter problems:**
   ```bash
   uv run ruff check . --fix
   ```

4. **Run both in sequence:**
   ```bash
   uv run ruff check . --fix && uv run ruff format .
   ```

## Common Rule Categories

- `E` - pycodestyle errors
- `F` - Pyflakes (unused imports, variables)
- `I` - isort (import sorting)
- `N` - pep8-naming
- `W` - pycodestyle warnings
- `UP` - pyupgrade (modernise Python code)

## Ignoring Specific Issues

**In code:**
```python
# ruff: noqa: E501
very_long_line = "This line is too long but we want to ignore it"

# Or ignore all issues on a line
bad_code = "something"  # noqa
```

**In pyproject.toml:**
```toml
[tool.ruff.lint]
ignore = ["E501", "F401"]  # Ignore line length and unused imports
```

## Integration with GitHub Actions

See Step 2 documentation for CI/CD integration examples.

---

**Further Reading:**
- [Official Ruff Documentation](https://docs.astral.sh/ruff/)
- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)