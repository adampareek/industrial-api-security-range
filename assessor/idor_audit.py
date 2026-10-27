from common import BASE_URL, finding, session

def run() -> dict:
    s = session()
    response = s.get(f"{BASE_URL}/api/profiles/1002", timeout=5)
    vulnerable = response.status_code == 200
    evidence = f"Unauthenticated object retrieval succeeded: {response.text}" if vulnerable else f"Object retrieval blocked with HTTP {response.status_code}"
    return finding("IASR-04", "Broken object-level authorization", "High", vulnerable, evidence, "Authorize every object access against the authenticated subject and requested object.")

if __name__ == "__main__":
    print(run())
