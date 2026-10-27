import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import credential_leak_audit
import idor_audit
import jwt_none_demo
import recon
import ssrf_probe
import weak_secret_audit
CHECKS = [recon.run, credential_leak_audit.run, jwt_none_demo.run, weak_secret_audit.run, idor_audit.run, ssrf_probe.run]

def markdown_report(results: list[dict]) -> str:
    vulnerable_count = sum(1 for item in results if item["vulnerable"])
    lines = ["# Industrial API Security Range — Assessment Report", "", f"Checks executed: {len(results)}", f"Vulnerabilities confirmed: {vulnerable_count}", ""]
    for item in results:
        status = "CONFIRMED" if item["vulnerable"] else "NOT CONFIRMED"
        lines += [f"## {item['id']} — {item['title']}", "", f"- Severity: **{item['severity']}**", f"- Status: **{status}**", "", "### Evidence", "", item["evidence"], "", "### Remediation", "", item["remediation"], ""]
    return "\n".join(lines)

def main() -> int:
    results = []
    for check in CHECKS:
        try:
            results.append(check())
        except Exception as exc:
            results.append({"id": "ERROR", "title": check.__module__, "severity": "Informational", "vulnerable": False, "evidence": f"Check failed: {exc}", "remediation": "Confirm the Docker range is running and retry."})
    out = Path(__file__).resolve().parents[1] / "findings"
    out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    (out / "report.md").write_text(markdown_report(results), encoding="utf-8")
    for item in results:
        status = "CONFIRMED" if item["vulnerable"] else "not confirmed"
        print(f"{item['id']}: {item['title']} — {status}")
    print(f"\nWrote {out / 'report.md'}")
    print(f"Wrote {out / 'report.json'}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
