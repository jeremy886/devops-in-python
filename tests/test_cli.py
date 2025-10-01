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