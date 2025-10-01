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