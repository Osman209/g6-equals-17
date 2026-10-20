"""COVERS [P7, Lemma 4], second route: matching number exactly 3, orbits by union-find
under explicit generators of Aut(M) (no nauty), completion by SAT.

Second, independent check of branch (i): no triangle decomposition of M = K_n + E - F
with matching number 3 (F = first c/2 matching pairs, unserved; E = the others, served
twice).

Shares no code with matched.c:
  * orbits of placements of three disjoint triangles are computed by union-find under
    explicit generators of Aut(M) (swaps inside an F-pair or E-pair, and transpositions of
    neighbouring F-pairs and of neighbouring E-pairs) -- no nauty;
  * each representative is completed by a SAT solver (CaDiCaL) instead of a search tree:
    the three triangles are fixed, triangles inside the other points are forbidden, every
    pair is served exactly as often as M asks, and any four pairwise disjoint triangles in
    a model are forbidden and the solver is asked again, until UNSAT or a model with
    matching number 3 appears.

usage: python3 second_route.py n c
"""
import sys, itertools, time
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

n, c = int(sys.argv[1]), int(sys.argv[2])
cap = {p: 1 for p in itertools.combinations(range(n), 2)}
Fp = [(2 * k, 2 * k + 1) for k in range(n // 2) if 2 * k < c]
Ep = [(2 * k, 2 * k + 1) for k in range(n // 2) if 2 * k >= c]
for p in Fp: cap[p] = 0
for p in Ep: cap[p] = 2
tris = [t for t in itertools.combinations(range(n), 3) if all(cap[q] for q in itertools.combinations(t, 2))]
mask = {t: sum(1 << v for v in t) for t in tris}

# generators of Aut(M), as permutations of the points
def perm_from_swaps(swaps):
    p = list(range(n))
    for a, b in swaps: p[a], p[b] = p[b], p[a]
    return p
gens = []
for grp in (Fp, Ep):
    for a, b in grp: gens.append(perm_from_swaps([(a, b)]))
    for (a, b), (x, y) in zip(grp, grp[1:]): gens.append(perm_from_swaps([(a, x), (b, y)]))

def key(ts): return tuple(sorted(ts))
placements = []
for t1, t2, t3 in itertools.combinations(tris, 3):
    if mask[t1] & mask[t2] or mask[t1] & mask[t3] or mask[t2] & mask[t3]: continue
    placements.append(key((mask[t1], mask[t2], mask[t3])))
index = {pl: i for i, pl in enumerate(placements)}
parent = list(range(len(placements)))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
def img(m, p): return sum(1 << p[v] for v in range(n) if m >> v & 1)
for i, pl in enumerate(placements):
    for g in gens:
        j = index[key(tuple(img(m, g) for m in pl))]
        a, b = find(i), find(j)
        if a != b: parent[a] = b
reps = sorted({find(i) for i in range(len(placements))})
print("placements %d, orbits under Aut(M) %d" % (len(placements), len(reps)), flush=True)

def solve(pl):
    P = IDPool(); X = {t: P.id(t) for t in tris}; cl = []
    W = pl[0] | pl[1] | pl[2]; U = ((1 << n) - 1) & ~W
    for t in tris:
        if mask[t] & U == mask[t]: cl.append([-X[t]])          # nothing inside U
    for m in pl:
        cl.append([X[tuple(v for v in range(n) if m >> v & 1)]])
    for q, k in cap.items():
        if k: cl += CardEnc.equals([X[t] for t in tris if set(q) <= set(t)], k, vpool=P, encoding=EncType.seqcounter).clauses
    blocked = 0
    with Solver(name='cadical195', bootstrap_with=cl) as S:
        while S.solve():
            on = [t for t in tris if S.get_model()[X[t] - 1] > 0]
            four = None
            for a, b, cc, d in itertools.combinations(on, 4):
                if not (mask[a] & mask[b] or mask[a] & mask[cc] or mask[a] & mask[d] or mask[b] & mask[cc] or mask[b] & mask[d] or mask[cc] & mask[d]):
                    four = (a, b, cc, d); break
            if four is None: return on, blocked
            S.add_clause([-X[t] for t in four]); blocked += 1
    return None, blocked

import os
START = int(sys.argv[3]) if len(sys.argv) > 3 else 0
STEP = int(sys.argv[4]) if len(sys.argv) > 4 else 1
logname = "second_route_n%d_c%d.log" % (n, c)
done = set()
if os.path.exists(logname):
    done = {int(l.split()[1]) for l in open(logname) if l.startswith("orbit")}
log = open(logname, "a")
t0 = time.time(); total_blocked = 0
for i, r in enumerate(reps):
    if i in done or i % STEP != START: continue
    sol, b = solve(placements[r]); total_blocked += b
    if sol is None:
        log.write("orbit %d UNSAT blocked %d\n" % (i, b)); log.flush()
    if sol is not None:
        print("RESULT n=%d c=%d: FOUND a decomposition with matching number 3 (orbit %d): %s" % (n, c, i, sol)); sys.exit(0)
nd = len({int(l.split()[1]) for l in open(logname) if l.startswith("orbit")})
print("RESULT n=%d c=%d: %d orbits, %d recorded UNSAT in %s, none found (%.0fs this run)" % (n, c, len(reps), nd, logname, time.time() - t0))
