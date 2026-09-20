"""COVERS [P3, §4] — DIMACS export of one core through the same build()."""
#!/usr/bin/env python3
"""
Export one audited core using the exact build() implementation in code/search_sixteen.py.

Required release files:
  code/search_sixteen.py
  data/eight_cores.jsonl
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
DATA = ROOT / "data"
OUT = ROOT / "certificates"

sys.path.insert(0, str(CODE))

try:
    from search_sixteen import build
except ImportError as e:
    raise SystemExit(
        "Missing code/search_sixteen.py. Copy the exact audited file from the local project."
    ) from e

if len(sys.argv) != 2:
    raise SystemExit("usage: python code/export_core_cnf.py CORE_ID")

core_id = int(sys.argv[1])
core_file = DATA / "eight_cores.jsonl"
if not core_file.exists():
    raise SystemExit(
        "Missing data/eight_cores.jsonl. Copy the exact audited canonical-core file."
    )

rows = [json.loads(line) for line in core_file.read_text().splitlines()]
if not 0 <= core_id < len(rows):
    raise SystemExit(f"core must be between 0 and {len(rows)-1}")

S = rows[core_id]["supports"]
cnf, nv, data, meta = build(S, symmetry=True)

max_var = max(abs(lit) for clause in cnf for lit in clause)
assert max_var <= nv

OUT.mkdir(exist_ok=True)
out = OUT / f"core_{core_id:03d}.cnf"
with out.open("w", newline="\n") as f:
    f.write(f"p cnf {nv} {len(cnf)}\n")
    for clause in cnf:
        f.write(" ".join(map(str, clause)) + " 0\n")

print(f"wrote: {out}")
print(f"variables: {nv}")
print(f"clauses: {len(cnf)}")
print(f"max literal: {max_var}")
print(f"meta: {meta}")
