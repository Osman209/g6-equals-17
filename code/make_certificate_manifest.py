"""COVERS [P3, §6] — SHA-256 manifest over the CNF, DRAT and marker files."""
#!/usr/bin/env python3
from pathlib import Path
import argparse
import csv
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates"

ap = argparse.ArgumentParser()
ap.add_argument("--strict", action="store_true",
                help="require all 463 CNF, DRAT and .verified files")
args = ap.parse_args()

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

rows = []
for core in range(463):
    tag = f"core_{core:03d}"
    for ext in ("cnf", "drat", "verified"):
        p = CERT / f"{tag}.{ext}"
        if p.exists():
            rows.append({
                "core": core,
                "kind": ext,
                "filename": p.name,
                "bytes": p.stat().st_size,
                "sha256": sha256(p),
            })
        elif args.strict:
            raise SystemExit(f"missing: {p}")

out = CERT / "certificate_manifest.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["core","kind","filename","bytes","sha256"])
    w.writeheader()
    w.writerows(rows)

print("wrote:", out)
print("manifest rows:", len(rows))
if args.strict:
    assert len(rows) == 463 * 3
    print("PASS: strict archive contains 463 CNF + 463 DRAT + 463 markers")
