import base64
import binascii
import re
from common import BASE_URL, finding, session
B64 = re.compile(r"\b[A-Za-z0-9+/]{16,}={0,2}\b")

def printable_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    return sum(32 <= byte <= 126 for byte in data) / len(data)

def run() -> dict:
    s = session()
    response = s.get(f"{BASE_URL}/api/assets", timeout=5)
    response.raise_for_status()
    hits = []
    for asset in response.json():
        note = asset.get("maintenance_note", "")
        for candidate in B64.findall(note):
            try:
                decoded = base64.b64decode(candidate, validate=True)
            except (binascii.Error, ValueError):
                continue
            if printable_ratio(decoded) > 0.9:
                hits.append({"asset_id": asset.get("asset_id"), "encoded": candidate, "decoded": decoded.decode(errors="replace")})
    return finding("IASR-01", "Sensitive information exposed in asset metadata", "High", bool(hits), f"Decoded Base64-like operational values: {hits}" if hits else "No decodable credential-like values found.", "Do not return secrets in asset metadata; redact sensitive notes and move credentials to a secret manager.")

if __name__ == "__main__":
    print(run())
