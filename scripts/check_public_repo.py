from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_NAMES = {".env", "google-services.json", "service-account.json", "id_rsa"}
PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)(?:api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{16,}['\"]"),
]

errors = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.name in FORBIDDEN_NAMES:
        errors.append(f"forbidden file: {path.relative_to(ROOT)}")
        continue
    if path.suffix.lower() not in {".py", ".md", ".txt", ".yml", ".yaml", ".json"}:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pattern in PATTERNS:
        if pattern.search(text):
            errors.append(f"possible credential material: {path.relative_to(ROOT)}")

if errors:
    print("\n".join(errors))
    sys.exit(1)

required = [
    ROOT / "production-safe/app/security.py",
    ROOT / "production-safe/app/referral_tiers.py",
    ROOT / "SOURCE_MANIFEST.md",
]
missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
if missing:
    print("missing required public files: " + ", ".join(missing))
    sys.exit(1)

print("public repository guard passed")
