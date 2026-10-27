from common import BASE_URL, finding, session

def run() -> dict:
    s = session()
    target = "http://internal-console:3001/secret-status"
    create = s.post(f"{BASE_URL}/api/bookmarks", json={"url": target}, timeout=5)
    if create.status_code not in {200, 201}:
        return finding("IASR-06", "Server-side request forgery", "Critical", False, f"Internal target creation blocked with HTTP {create.status_code}: {create.text}", "Block private/internal address ranges and enforce egress controls.")
    bookmark_id = create.json()["id"]
    preview = s.get(f"{BASE_URL}/api/bookmarks/{bookmark_id}", timeout=5)
    vulnerable = preview.status_code == 200 and "ssrf-reached-internal-console" in preview.text
    evidence = f"API fetched Docker-internal service through URL preview: {preview.text}" if vulnerable else f"Internal fetch blocked or failed with HTTP {preview.status_code}: {preview.text}"
    return finding("IASR-06", "Server-side request forgery", "Critical", vulnerable, evidence, "Parse and validate URLs, resolve DNS before connecting, block private/loopback/link-local ranges, disable redirects, and enforce outbound network policy.")

if __name__ == "__main__":
    print(run())
