from unittest.mock import patch
from api.app.security import validate_external_url

@patch("api.app.security.host_resolves_private", return_value=True)
def test_internal_destination_blocked(mock_private):
    allowed, reason = validate_external_url("http://internal.example/secret")
    assert allowed is False
    assert "blocked" in reason.lower()

@patch("api.app.security.host_resolves_private", return_value=False)
def test_public_https_destination_allowed(mock_private):
    allowed, reason = validate_external_url("https://example.com/resource")
    assert allowed is True
    assert reason == "ok"

def test_non_http_scheme_blocked():
    allowed, reason = validate_external_url("file:///etc/passwd")
    assert allowed is False
    assert "http" in reason.lower()
