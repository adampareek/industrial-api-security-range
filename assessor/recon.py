from common import BASE_URL, finding, session

def run() -> dict:
    s = session()
    response = s.get(f"{BASE_URL}/openapi.json", timeout=5)
    response.raise_for_status()
    paths = sorted(response.json().get("paths", {}).keys())
    return finding("IASR-00", "API surface reconnaissance", "Informational", False, f"Discovered {len(paths)} documented paths: {', '.join(paths)}", "Maintain an accurate API inventory and restrict sensitive documentation in production.")

if __name__ == "__main__":
    print(run())
