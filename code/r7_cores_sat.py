"""COVERS [P7, Lemma 5], second route (SAT). Calibration: r = 6, n = 8 is SAT.
"""
"""Second method for the core step: is there an intersecting multiset of triangles on n
points (multiplicity <= m) with every point in a triangle and room in every card,
i.e. (triangles at p) + (points not sharing a triangle with p) <= r ?   usage: core_sat.py r n m"""
import sys, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
r, n, m = map(int, sys.argv[1:4])
T = list(itertools.combinations(range(n), 3))
P = IDPool(); cl = []
X = {(t, k): P.id((t, k)) for t in T for k in range(m)}
for t in T:
    for k in range(1, m):
        cl.append([-X[t, k], X[t, k - 1]])            # copies used in order
for t, u in itertools.combinations(T, 2):
    if not set(t) & set(u):
        cl.append([-X[t, 0], -X[u, 0]])              # pairwise intersecting
cov = {}
for p, q in itertools.combinations(range(n), 2):
    v = P.id(('cov', p, q)); cov[p, q] = cov[q, p] = v
    ts = [X[t, 0] for t in T if p in t and q in t]
    cl.append([-v] + ts)
    for x in ts: cl.append([v, -x])
for p in range(n):
    cl.append([X[t, 0] for t in T if p in t])
    lits = [X[t, k] for t in T if p in t for k in range(m)] + [-cov[p, q] for q in range(n) if q != p]
    cl += CardEnc.atmost(lits, r, vpool=P, encoding=EncType.totalizer).clauses
with Solver(name='cadical195', bootstrap_with=cl) as S:
    print("RESULT r=%d n=%d m=%d: %s" % (r, n, m, "SAT" if S.solve() else "UNSAT"))
