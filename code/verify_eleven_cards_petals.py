"""COVERS [P2, §2] branch C, short form — the petal statement, plus a control.

Statement checked (Lemma 3 of [P2]): let H be a set of 3-element subsets of an
11-element set in which every point is the centre of four petals (four members of H
through it that pairwise meet only there), and let x be a point in at most six members.
Then for some petal P of x there are two disjoint members of H disjoint from P; so H
contains three pairwise disjoint members.

The point x is fixed as 0 with petals {0,1,2}, {0,3,4}, {0,5,6}, {0,7,8}; every
configuration is of this form after relabelling.  Expected: UNSAT with the bound 6.
Controls: with the bound 7 the same model is SAT, and on ten points (bound 6) it is SAT,
so both parameters are used and the encoding is not vacuous.  Exits non-zero if any outcome differs.

Needs python-sat (pip install python-sat).  Runs in a few seconds.
"""
import itertools
import sys

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

PETALS_X = [frozenset(s) for s in [(0, 1, 2), (0, 3, 4), (0, 5, 6), (0, 7, 8)]]


def solve(bound, n=11):
    POINTS = range(n)
    pool = IDPool()
    triples = [frozenset(s) for s in itertools.combinations(POINTS, 3)]
    e = {t: pool.id(('e', tuple(sorted(t)))) for t in triples}
    cl = [[e[p]] for p in PETALS_X]
    for y in POINTS:                                    # four petals at every point
        pairs = list(itertools.combinations([p for p in POINTS if p != y], 2))
        s = {q: pool.id(('pet', y, q)) for q in pairs}
        for q in pairs:
            cl.append([-s[q], e[frozenset((y,) + q)]])
        for a, b in itertools.combinations(pairs, 2):
            if set(a) & set(b):
                cl.append([-s[a], -s[b]])
        cl += CardEnc.atleast(list(s.values()), 4, vpool=pool,
                              encoding=EncType.seqcounter).clauses
    cl += CardEnc.atmost([e[t] for t in triples if 0 in t], bound, vpool=pool,
                         encoding=EncType.seqcounter).clauses
    for a, b, c in itertools.combinations(triples, 3):  # no petal of x with two disjoint others
        if a & b or a & c or b & c:
            continue
        if a in PETALS_X or b in PETALS_X or c in PETALS_X:
            cl.append([-e[a], -e[b], -e[c]])
    with Cadical153(bootstrap_with=cl) as sat:
        return sat.solve()


main = solve(6)
control = solve(7)
ten = solve(6, n=10)
if main or not control or not ten:
    print("FAIL: bound 6 ->", "SAT" if main else "UNSAT", "; bound 7 ->", "SAT" if control else "UNSAT",
          "; ten points ->", "SAT" if ten else "UNSAT")
    sys.exit(1)
print("PASS: bound 6 UNSAT (the statement holds); controls SAT: bound 7, and ten points")
