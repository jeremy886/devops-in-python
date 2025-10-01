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