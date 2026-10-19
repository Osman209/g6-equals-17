"""COVERS the incidence matrices printed in [P4, §1] and [P5, §5] — standard library only.

Builds the incidence matrix of each witness from its data file (one row per symbol, in
order; one column per card, in order; 1 where the symbol lies in the card), the format used
by Barát and Wanless (arXiv:2011.04444), and checks that the matrix printed in the paper is
exactly that matrix. Exits non-zero on any difference.

    python code/verify_incidence_matrices.py           # check
    python code/verify_incidence_matrices.py --print   # also print both matrices
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ("data/witness_17.json", "papers/paper_4_seventeen_card_witness.md", 27, 17),
    ("data/witness_r7_21.json", "papers/paper_5_every_r.md", 35, 21),
]


def matrix(cards, nsym):
    return ["".join("1" if s in c else "0" for c in cards) for s in range(1, nsym + 1)]


def printed(md, ncols):
    """the first fenced block in the paper whose lines are all 0/1 strings of width ncols"""
    blocks, cur, inside = [], [], False
    for line in md.splitlines():
        if line.startswith("```"):
            if inside:
                blocks.append(cur)
            cur, inside = [], not inside
        elif inside:
            cur.append(line.strip())
    for b in blocks:
        if b and all(len(x) == ncols and set(x) <= {"0", "1"} for x in b):
            return b
    return None


bad = 0
for data, paper, nsym, ncards in CASES:
    cards = [set(c) for c in json.loads((ROOT / data).read_text())["cards"]]
    assert len(cards) == ncards
    M = matrix(cards, nsym)
    assert all(row.count("1") >= 1 for row in M)
    assert all(sum(row[j] == "1" for row in M) == len(cards[j]) for j in range(ncards))
    P = printed((ROOT / paper).read_text(), ncards)
    ok = P == M
    bad += not ok
    print("RESULT %s: %d x %d matrix, printed copy in %s %s"
          % (data, nsym, ncards, paper, "matches" if ok else "DIFFERS"))
    if "--print" in sys.argv:
        print("\n".join(M))
if bad:
    print("FAIL"); sys.exit(1)
print("PASS: both printed incidence matrices are exactly the matrices of the data files")
