"""COVERS [P7, Lemma 2]: twelve or thirteen cards of size 7 whose symbols each meet at most
three of them always contain three pairwise disjoint triples. Run through code/verify_g7_lower.py.

m cards of size r, every symbol of degree <= 3 (room model as in [P7, Lemma 4]).
Is the largest number of pairwise disjoint triangles exactly k possible?
Fix k disjoint triangles {0,1,2},{3,4,5},... (one orbit under S_m); every other triangle must
meet them (else k+1 disjoint); forbid any k+1 pairwise disjoint triangles.
Every card must reach the other m-1 cards: each point p has
(triangles at p) + (points sharing no triangle with p) <= r.
usage: r7_small_families.py m r k [solver]  (glucose4 also switches to the sequential-counter encoding)   -> SAT means such a family of blocks exists."""
import sys, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
m, r, k = map(int, sys.argv[1:4])
W = (1 << (3 * k)) - 1
T = [t for t in itertools.combinations(range(m), 3)]
mask = {t: sum(1 << v for v in t) for t in T}
P = IDPool(); X = {t: P.id(t) for t in T}; cl = []
fixed = [tuple(range(3 * i, 3 * i + 3)) for i in range(k)]
for t in fixed: cl.append([X[t]])
for t in T:
    if not mask[t] & W: cl.append([-X[t]])
def rec(start, used, ch):
    if len(ch) == k + 1:
        cl.append([-X[t] for t in ch]); return
    for i in range(start, len(T)):
        if not mask[T[i]] & used: rec(i + 1, used | mask[T[i]], ch + [T[i]])
rec(0, 0, [])
cov = {}
for p, q in itertools.combinations(range(m), 2):
    v = P.id(('c', p, q)); cov[p, q] = cov[q, p] = v
    ts = [X[t] for t in T if p in t and q in t]
    cl.append([-v] + ts); cl += [[v, -x] for x in ts]
for p in range(m):
    lits = [X[t] for t in T if p in t] + [-cov[p, q] for q in range(m) if q != p]
    enc = EncType.seqcounter if len(sys.argv) > 4 and sys.argv[4] == 'glucose4' else EncType.totalizer
    cl += CardEnc.atmost(lits, r, vpool=P, encoding=enc).clauses
SOLVER = sys.argv[4] if len(sys.argv) > 4 else 'cadical195'
with Solver(name=SOLVER, bootstrap_with=cl) as S:
    ok = S.solve()
    out = "SAT" if ok else "UNSAT"
    if ok:
        mod = set(l for l in S.get_model() if l > 0)
        out += " " + str([t for t in T if X[t] in mod])
    print("RESULT m=%d r=%d matching number exactly %d: %s" % (m, r, k, out), flush=True)
