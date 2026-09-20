"""Check that the shipped CNF files are the ones search_sixteen.build() produces.

COVERS [P3, §8] — the CNF a reviewer checks with drat-trim is the CNF the search used.

A DRAT certificate proves that *some* formula is unsatisfiable. It is worth nothing to the
mathematics unless that formula is the one the encoding produces from the canonical core
data. This script closes that link: it rebuilds the CNF for each shipped core directly
from data/eight_cores.jsonl through the audited build() and compares byte for byte.

It also prints the variable and clause counts, which are the numbers quoted in [P3, §5].

Usage:
    python code/verify_cnf_regeneration.py
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from search_sixteen import build  # noqa: E402

CORES = ROOT / "data" / "eight_cores.jsonl"
CNFDIR = ROOT / "data" / "cnf"


def dimacs(cnf, nv):
    out = ["p cnf %d %d\n" % (nv, len(cnf))]
    for clause in cnf:
        out.append(" ".join(map(str, clause)) + " 0\n")
    return "".join(out).encode()


def main():
    rows = [json.loads(line) for line in CORES.read_text().splitlines()]
    if len(rows) != 463:
        raise SystemExit("expected 463 canonical cores, found %d" % len(rows))
    print("canonical cores: %d" % len(rows))

    shipped = sorted(CNFDIR.glob("core_*.cnf"))
    if not shipped:
        raise SystemExit("no CNF files in data/cnf/")

    failures = []
    for path in shipped:
        core_id = int(path.stem.split("_")[1])
        cnf, nv, _data, meta = build(rows[core_id]["supports"], symmetry=True)
        rebuilt = dimacs(cnf, nv)
        original = path.read_bytes()
        same = rebuilt == original
        if not same:
            failures.append(core_id)
        print(
            "core %3d  variables %6d  clauses %7d  symbols %2d  covers4 %4d  covers5 %5d  %s"
            % (
                core_id,
                nv,
                len(cnf),
                meta["symbols"],
                meta["covers4"],
                meta["covers5"],
                "IDENTICAL" if same else "DIFFERS",
            )
        )

    if failures:
        raise SystemExit("FAIL: regenerated CNF differs for cores %s" % failures)
    print("PASS: every shipped CNF is byte-identical to the one build() produces.")


if __name__ == "__main__":
    main()
