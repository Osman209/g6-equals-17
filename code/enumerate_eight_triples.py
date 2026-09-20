"""Step 3 of the eight-card core reduction: enumerate the triple systems.

COVERS [P3, §3] step 3 — 39,768 triple systems over the seven orbit representatives.

For each orbit representative M (a maximal intersecting triple system on the eight card
indices, from enumerate_eight_maximal.py), a *triple system* is a multiset T of triples
drawn from M such that

  1. every card lies in at least one triple of T;
  2. writing deg(v) for the number of triples of T containing v, and F for the pairs of
     cards covered by no triple of T, every card has 6 - deg(v) - |F at v| >= 0.

Condition 2 is the statement that the card has room: it has six symbol slots, each triple
through it is a degree-three symbol and each uncovered pair at it must be served by its
own degree-two symbol.

PROVENANCE. The original script for this step was lost. This file is a reconstruction
written from the definition above and from the outputs on either side of it. It is not a
copy of the original, and it is kept in the repository on the strength of the check in
main(): run against data/eight_triples_summary.json it must reproduce all seven recorded
counts exactly,

    28329, 4932, 1526, 3858, 156, 535, 432   (total 39,768)

and it does. The script exits non-zero if any count disagrees.

Usage:
    python code/enumerate_eight_triples.py            # check the seven counts
    python code/enumerate_eight_triples.py --write    # also write data/eight_triples.jsonl
"""
from pathlib import Path
from itertools import combinations
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "eight_triples_summary.json"
OUT = ROOT / "data" / "eight_triples.jsonl"

ALL_PAIRS = list(combinations(range(8), 2))
MAX_MULTIPLICITY = 3


def systems(maximal, collect=False):
    """Enumerate the triple systems inside one maximal family.

    Returns (count, nodes, rows). rows is empty unless collect is set, because the full
    list over all seven representatives is about 5 MB.
    """
    M = [tuple(t) for t in maximal]
    n = len(M)
    deg = [0] * 8
    mult = [0] * n
    rows = []
    state = {"count": 0, "nodes": 0}

    def leaf():
        if min(deg) == 0:
            return
        covered = set()
        for k in range(n):
            if mult[k]:
                for p in combinations(sorted(M[k]), 2):
                    covered.add(p)
        free = [p for p in ALL_PAIRS if p not in covered]
        for v in range(8):
            if 6 - deg[v] - sum(v in p for p in free) < 0:
                return
        state["count"] += 1
        if collect:
            triples = []
            for k in range(n):
                triples.extend([list(M[k])] * mult[k])
            rows.append(triples)

    def dfs(i):
        state["nodes"] += 1
        if i == n:
            leaf()
            return
        t = M[i]
        for m in range(MAX_MULTIPLICITY + 1):
            if m:
                for v in t:
                    deg[v] += 1
                # a card has only six slots, so its triple-degree can never exceed six
                if max(deg[v] for v in t) > 6:
                    for v in t:
                        deg[v] -= 1
                    break
            mult[i] = m
            dfs(i + 1)
        for _ in range(mult[i]):
            for v in t:
                deg[v] -= 1
        mult[i] = 0

    dfs(0)
    return state["count"], state["nodes"], rows


def main():
    write = "--write" in sys.argv
    summary = json.loads(SUMMARY.read_text())
    assert len(summary) == 7 and all(r["status"] == "COMPLETE" for r in summary)

    total = 0
    bad = []
    out_rows = []
    for row in summary:
        count, nodes, rows = systems(row["maximal"], collect=write)
        want = row["triplesystems"]
        ok = count == want
        if not ok:
            bad.append((row["rep"], count, want))
        total += count
        print(
            "rep %d  maximal %2d  systems %6d  recorded %6d  %s  nodes %d"
            % (row["rep"], len(row["maximal"]), count, want, "OK" if ok else "MISMATCH", nodes),
            flush=True,
        )
        if write:
            for triples in rows:
                out_rows.append({"rep": row["rep"], "triples": triples})

    print("TOTAL %d  recorded 39768" % total)
    if write:
        with OUT.open("w", newline="\n") as f:
            for r in out_rows:
                f.write(json.dumps(r) + "\n")
        print("wrote", OUT)

    if bad or total != 39768:
        print("FAIL: reconstruction does not reproduce the recorded counts:", bad)
        raise SystemExit(1)
    print("PASS: reconstruction reproduces all seven recorded counts and their total.")


if __name__ == "__main__":
    main()
