import base64
import json
from urllib.parse import urlparse
import requests
BASE_URL = "http://localhost:8080"

def enforce_local_target(base_url: str) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"}:
        raise SystemExit("Assessment target must use http or https.")
    if parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise SystemExit("Safety guard: this assessment toolkit only runs against localhost.")

def session() -> requests.Session:
    enforce_local_target(BASE_URL)
    s = requests.Session()
    s.headers.update({"User-Agent": "industrial-api-security-range-assessor/1.0"})
    return s

def get_demo_token(s: requests.Session) -> str:
    response = s.post(f"{BASE_URL}/api/auth/token", json={"username": "field_tech", "password": "training-only"}, timeout=5)
    response.raise_for_status()
    return response.json()["access_token"]

def b64url_json(data: dict) -> str:
    raw = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

def finding(finding_id: str, title: str, severity: str, vulnerable: bool, evidence: str, remediation: str) -> dict:
    return {"id": finding_id, "title": title, "severity": severity, "vulnerable": vulnerable, "evidence": evidence, "remediation": remediation}
