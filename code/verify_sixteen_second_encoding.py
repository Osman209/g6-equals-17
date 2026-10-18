"""COVERS [P3, §4 and §5] by a second encoding — all 463 completion problems written again
from scratch and solved without any symmetry breaking.

Differences from build() in code/search_sixteen.py:
  * the cardinality constraints use the totalizer encoding, not the sequential counter;
  * there are NO lexicographic symmetry-breaking clauses, so that chain is not trusted;
  * the antichain clauses are written straight from [P3, Lemma 3] (no symbol's support lies
    inside another's), for every fresh support, with no length shortcut;
  * a different solver (CaDiCaL 1.5.3 through python-sat) is used.

Modes:
    python code/verify_sixteen_second_encoding.py              # all 463, about 3 hours
    python code/verify_sixteen_second_encoding.py 7 8          # cores 7..7 only
    python code/verify_sixteen_second_encoding.py --control    # cover clauses dropped on 21
                                                               # sample cores: must be SAT on
                                                               # exactly the cores where build()
                                                               # without covers is SAT
Exits non-zero if any core is SAT, or if the control disagrees. Needs python-sat.
The recorded run is results/second_encoding_cadical153.txt.
"""
from pathlib import Path
import itertools, json, sys, time
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]
X, Y = range(4), range(4, 8)
FRESH = [b for k in (2, 3, 4) for b in itertools.combinations(range(8), k)
         if set(b) & set(X) and set(b) & set(Y)]


def encode(S, covers=True):
    P = IDPool(); C = []
    n = len(S); mask = [sum(1 << v for v in s) for s in S]
    m = [[P.id(("m", v, j)) for j in range(8)] for v in range(n)]
    f = {b: P.id(("f", b)) for b in FRESH}
    tot = EncType.totalizer
    for v, s in enumerate(S):                         # final degree at most four
        C += CardEnc.atmost(m[v], 4 - len(s), vpool=P, encoding=tot).clauses
        if len(s) == 1:                               # degree one is impossible
            C.append(list(m[v]))
    for j in range(8):                                # five more symbols per new card
        lits = [m[v][j] for v in range(n)] + [f[b] for b in FRESH if j in b]
        C += CardEnc.equals(lits, 5, vpool=P, encoding=tot).clauses
        for a in range(8):                            # the new card meets core card a
            C.append([m[v][j] for v in range(n) if mask[v] >> a & 1])
    for j in X:                                       # every x-card meets every y-card
        for k in Y:
            lits = [f[b] for b in FRESH if j in b and k in b]
            for v in range(n):
                w = P.id(("both", v, j, k)); lits.append(w)
                C += [[-w, m[v][j]], [-w, m[v][k]]]
            C.append(lits)
    # [P3, Lemma 3]: no support inside another (equal supports included)
    for b, c in itertools.permutations(FRESH, 2):
        if set(b) <= set(c):
            C.append([-f[b], -f[c]])
    for b in FRESH:
        for v in range(n):
            C.append([-f[b]] + [-m[v][j] for j in b])
    for v, w in itertools.permutations(range(n), 2):
        if mask[v] & ~mask[w] == 0:
            wit = []
            for j in range(8):
                q = P.id(("wit", v, w, j)); wit.append(q)
                C += [[-q, m[v][j]], [-q, -m[w][j]]]
            C.append(wit)
    assert not any((mask[a] | mask[b] | mask[c]) == 255 for a, b, c in itertools.combinations(range(n), 3))
    cov4 = cov5 = []
    if covers:
        # a five-cover of the sixteen cards uses at least four core symbols that cover the
        # core, since x, y and fresh symbols miss every core card and three cannot cover it
        cov4 = [t for t in itertools.combinations(range(n), 4) if (mask[t[0]] | mask[t[1]] | mask[t[2]] | mask[t[3]]) == 255]
        cov5 = [t for t in itertools.combinations(range(n), 5) if (mask[t[0]] | mask[t[1]] | mask[t[2]] | mask[t[3]] | mask[t[4]]) == 255]

    def hits(t, tag):
        hv = []
        for j in range(8):
            q = P.id((tag, t, j)); hv.append(q)
            C.append([-q] + [m[v][j] for v in t])
            C.extend([q, -m[v][j]] for v in t)
        return hv
    for t in cov4:
        hv = hits(t, "h4")
        C.append([-hv[j] for j in X])                 # t + y misses an x-card
        C.append([-hv[j] for j in Y])                 # t + x misses a y-card
        for b in FRESH:                               # t + fresh b misses a card outside b
            C.append([-f[b]] + [-hv[j] for j in range(8) if j not in b])
    for t in cov5:
        hv = hits(t, "h5")
        C.append([-hv[j] for j in range(8)])          # t misses a new card
    return C, P.top, len(cov4), len(cov5)


def control(rows):
    sys.path.insert(0, str(ROOT / "code"))
    from search_sixteen import build
    sample = list(range(0, 463, 23))
    mine, theirs = [], []
    for i in sample:
        S = rows[i]["supports"]
        with Solver(name="cadical153", bootstrap_with=encode(S, covers=False)[0]) as s:
            mine.append(bool(s.solve()))
        with Solver(name="cadical153", bootstrap_with=build(S, cover=False)[0]) as s:
            theirs.append(bool(s.solve()))
    print("RESULT control: SAT here at", [i for i, x in zip(sample, mine) if x])
    print("RESULT control: SAT for build() at", [i for i, x in zip(sample, theirs) if x])
    if mine != theirs or not any(mine):
        print("FAIL: control disagrees"); sys.exit(1)
    print("PASS: both encodings, cover clauses dropped, are SAT on exactly the same cores")


def main():
    rows = [json.loads(l) for l in (ROOT / "data" / "eight_cores.jsonl").read_text().splitlines()]
    if "--control" in sys.argv:
        return control(rows)
    nums = [int(a) for a in sys.argv[1:]]
    lo, hi = (nums + [0, 463])[:2] if nums else (0, 463)
    bad = 0
    for i in range(lo, min(hi, len(rows))):
        t0 = time.time()
        C, nv, c4, c5 = encode(rows[i]["supports"])
        with Solver(name="cadical153", bootstrap_with=C) as s:
            r = s.solve()
            st = s.accum_stats()
        bad += bool(r)
        print("RESULT core %d %s vars %d clauses %d cov4 %d cov5 %d conflicts %d sec %.2f"
              % (i, "SAT" if r else "UNSAT", nv, len(C), c4, c5, st.get("conflicts", -1), time.time() - t0), flush=True)
    if bad:
        print("FAIL: %d cores SAT" % bad); sys.exit(1)
    print("PASS: cores %d..%d all UNSAT under the second encoding" % (lo, min(hi, len(rows)) - 1))


if __name__ == "__main__":
    main()
