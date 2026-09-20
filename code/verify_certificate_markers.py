"""COVERS [P3, §6] — presence and consistency of the certificate archive markers."""
#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates"

markers = sorted(CERT.glob("core_*.verified"))
if not markers:
    print("No core_*.verified files are present in certificates/.")
    print("Copy the 463 marker files from the completed local certification run.")
    sys.exit(2)

ids = []
for path in markers:
    try:
        core_id = int(path.stem.split("_")[1].split(".")[0])
    except Exception:
        raise SystemExit(f"bad marker name: {path.name}")
    obj = json.loads(path.read_text())
    assert obj["core"] == core_id, path
    assert obj["verified"] is True, path
    ids.append(core_id)

expected = list(range(463))
missing = sorted(set(expected) - set(ids))
extra = sorted(set(ids) - set(expected))

print("verified markers:", len(ids))
print("missing:", missing)
print("extra:", extra)

if ids != expected:
    raise SystemExit("FAIL: certificate marker set is not exactly cores 0..462")

print("PASS: 463/463 certificate markers are present and verified")
