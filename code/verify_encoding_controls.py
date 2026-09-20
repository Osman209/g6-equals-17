"""Controls on the sixteen-card SAT encoding.

COVERS [P3, §8] — the encoding is not trivially over-constrained, and the contradiction
comes from the transversal condition.

Four hundred and sixty-three UNSAT answers prove nothing if the formula is unsatisfiable
for the wrong reason. An encoding with one broken clause family is unsatisfiable
everywhere and would look exactly like a theorem. These are the controls that separate
the two cases.

CONTROL 1 (positive). build() takes a flag that drops the clauses forbidding a five-cover
and leaves the structural ones: card sizes, degree caps, intersections, supports,
symmetry. With those clauses dropped the formula should often be satisfiable, and any
model should decode into a genuine sixteen-card family. The script decodes each model and
re-checks it from scratch: sixteen distinct cards, six symbols each, every pair meeting.
If this control comes back UNSAT everywhere, the encoding is broken and the theorem is an
artefact.

CONTROL 2 (negative). The same cores with the five-cover clauses restored must be UNSAT.

The gap between the two is the mathematical content: for the cores where control 1 is SAT,
a sixteen-card intersecting family with the right degrees does exist, and it is only the
requirement that no five symbols cover that kills it.

Usage:
    python code/verify_encoding_controls.py            # 40-core sample, fixed seed
    python code/verify_encoding_controls.py --all      # all 463 cores, slow
    python code/verify_encoding_controls.py --n 100
"""
from pathlib import Path
from itertools import combinations
import argparse
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from search_sixteen import build, audit  # noqa: E402

try:
    from pysat.solvers import Solver
except ImportError:  # pragma: no cover
    raise SystemExit("this control needs python-sat: pip install python-sat")

CORES = ROOT / "data" / "eight_cores.jsonl"


def recheck(cards):
    """Independent re-check of a decoded family, not reusing audit()'s own assertions."""
    sets = [set(c) for c in cards]
    if len(sets) != 16:
        return "not sixteen cards"
    if any(len(c) != 6 for c in sets):
        return "a card does not have six symbols"
    if len({frozenset(c) for c in sets}) != 16:
        return "cards are not distinct"
    for a, b in combinations(sets, 2):
        if not a & b:
            return "two cards do not meet"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--solver", default="cadical195")
    args = ap.parse_args()

    rows = [json.loads(line) for line in CORES.read_text().splitlines()]
    if args.all:
        sample = list(range(len(rows)))
    else:
        random.seed(args.seed)
        sample = sorted(random.sample(range(len(rows)), min(args.n, len(rows))))

    open_cores = 0
    closed_cores = 0
    bad = []

    for core_id in sample:
        supports = rows[core_id]["supports"]

        cnf, _nv, data, _meta = build(supports, cover=False, symmetry=True)
        with Solver(name=args.solver, bootstrap_with=cnf) as solver:
            satisfiable = solver.solve()
            model = solver.get_model() if satisfiable else None

        if satisfiable:
            open_cores += 1
            cards = audit(supports, model, data, require_tau6=False)
            problem = recheck(cards)
            if problem:
                bad.append((core_id, "control 1 decoded a bad family: " + problem))
        else:
            closed_cores += 1

        cnf, _nv, _data, _meta = build(supports, cover=True, symmetry=True)
        with Solver(name=args.solver, bootstrap_with=cnf) as solver:
            if solver.solve():
                bad.append((core_id, "control 2: full encoding is SATISFIABLE"))

    print("cores tested: %d" % len(sample))
    print("control 1, five-cover clauses dropped:")
    print("  satisfiable, decoded family valid : %d" % open_cores)
    print("  unsatisfiable on structure alone  : %d" % closed_cores)
    print("control 2, full encoding: unsatisfiable on all %d" % (len(sample) - len(
        [b for b in bad if "control 2" in b[1]])))

    if bad:
        for core_id, message in bad:
            print("FAIL core %d: %s" % (core_id, message))
        raise SystemExit(1)
    if open_cores == 0:
        print(
            "FAIL: no core was satisfiable without the five-cover clauses. The encoding "
            "would be contradictory on its own and the UNSAT results would say nothing."
        )
        raise SystemExit(1)
    print(
        "PASS: the encoding admits genuine sixteen-card families when the transversal "
        "condition is dropped, and admits none when it is imposed."
    )


if __name__ == "__main__":
    main()
