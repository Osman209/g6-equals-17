"""COVERS [P3, §3] Lemma 1 by a second route — the 463 cores rebuilt straight from the
definition, and compared with data/eight_cores.jsonl.

The route of [P3, §3] goes through maximal intersecting triple systems, their seven orbits,
and a step-3 script that had to be reconstructed. This script uses none of them.

  1. code/enumerate_triples_direct.c enumerates every labelled multiset of triples on the
     eight core cards that satisfies the conditions of [P3, §3] (triples pairwise
     intersecting, multiplicity at most three, every card in a triple, enough room in every
     card for the degree-two symbols the uncovered pairs need), and keeps one
     representative per isomorphism class. Expected: 129 classes.
  2. Each class is completed here, independently of enumerate_eight_cores.py: one
     degree-two symbol on every uncovered pair, any further degree-two symbols the room
     allows, singletons for the rest, cards distinct. Expected: 772 completions.
  3. Every completion and every line of data/eight_cores.jsonl is put in canonical form
     under the FULL symmetric group on the eight cards (all 40,320 permutations), and the
     two sets are compared. Expected: the same 463 classes, nothing on either side only.

Exits non-zero on any disagreement. Needs numpy and a C compiler (cc). About one minute.
"""
from pathlib import Path
import itertools, json, subprocess, sys, tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

PERMS = np.array(list(itertools.permutations(range(8))), dtype=np.int64)
TAB = np.zeros((len(PERMS), 256), dtype=np.int64)
for m in range(256):
    acc = np.zeros(len(PERMS), dtype=np.int64)
    for v in range(8):
        if m >> v & 1:
            acc |= 1 << PERMS[:, v]
    TAB[:, m] = acc


def canon(masks):
    img = np.sort(TAB[:, list(masks)], axis=1)
    order = np.lexsort(img.T[::-1])
    return tuple(int(x) for x in img[order[0]])


def completions(T):
    deg = [sum(t >> v & 1 for t in T) for v in range(8)]
    cov = {(a, b) for t in T for a in range(8) for b in range(8) if a < b and t >> a & 1 and t >> b & 1}
    req = [(a, b) for a in range(8) for b in range(a + 1, 8) if (a, b) not in cov]
    slack = [6 - deg[v] - sum(v in p for p in req) for v in range(8)]
    assert min(slack) >= 0
    pairs = [(a, b) for a in range(8) for b in range(a + 1, 8)]
    out, extra = [], []

    def rec(k):
        if k == len(pairs):
            S = list(T) + [(1 << a) | (1 << b) for a, b in req + extra] \
                + [1 << v for v in range(8) for _ in range(slack[v])]
            cards = [tuple(i for i, s in enumerate(S) if s >> v & 1) for v in range(8)]
            assert all(len(c) == 6 for c in cards)
            if len(set(cards)) == 8:
                out.append(S)
            return
        a, b = pairs[k]
        rec(k + 1)
        n = 0
        while slack[a] > 0 and slack[b] > 0:
            slack[a] -= 1; slack[b] -= 1; extra.append((a, b)); n += 1
            rec(k + 1)
        for _ in range(n):
            slack[a] += 1; slack[b] += 1; extra.pop()

    rec(0)
    return out


def is_core(S):
    cards = [frozenset(i for i, s in enumerate(S) if s >> v & 1) for v in range(8)]
    ok = all(len(c) == 6 for c in cards) and all(a & b for a, b in itertools.combinations(cards, 2))
    tri = [s for s in S if bin(s).count("1") == 3]
    ok &= all(a & b for a, b in itertools.combinations(tri, 2))
    ok &= all(1 <= bin(s).count("1") <= 3 for s in S)
    ok &= not any(a | b | c == 255 for a, b, c in itertools.combinations(S, 3))
    return ok


def main():
    with tempfile.TemporaryDirectory() as d:
        exe = Path(d) / "triples"
        subprocess.run(["cc", "-O2", "-o", str(exe), str(ROOT / "code" / "enumerate_triples_direct.c")], check=True)
        res = subprocess.run([str(exe)], check=True, capture_output=True, text=True)
    classes = [tuple(map(int, l.split())) for l in res.stdout.splitlines() if l.strip()]
    print("step 1-3:", res.stderr.strip())

    mine, raw = set(), 0
    for T in classes:
        for S in completions(T):
            raw += 1
            assert is_core(S), "a completion is not a genuine core"
            mine.add(canon(S))

    theirs = set()
    rows = [json.loads(l) for l in (ROOT / "data" / "eight_cores.jsonl").read_text().splitlines()]
    for r in rows:
        S = [sum(1 << v for v in s) for s in r["supports"]]
        assert is_core(S), "a shipped core is not a genuine core"
        theirs.add(canon(S))

    tc = {canon(T) for T in classes}
    rc = {canon([sum(1 << v for v in t) for t in json.loads(l)["triples"]])
          for l in (ROOT / "data" / "eight_triple_classes.jsonl").read_text().splitlines()}

    print("RESULT triple classes %d (shipped %d), same set: %s" % (len(tc), len(rc), tc == rc))
    print("RESULT raw completions %d" % raw)
    print("RESULT cores %d, shipped lines %d, shipped distinct under S8 %d" % (len(mine), len(rows), len(theirs)))
    print("RESULT only here %d, only in the repository %d" % (len(mine - theirs), len(theirs - mine)))
    ok = (len(classes) == 129 and tc == rc and raw == 772 and len(mine) == 463
          and len(rows) == 463 and mine == theirs)
    if not ok:
        print("FAIL: the direct route does not reproduce the 463 cores")
        sys.exit(1)
    print("PASS: the direct route reproduces the 129 classes, 772 completions and the same 463 cores")


if __name__ == "__main__":
    main()
