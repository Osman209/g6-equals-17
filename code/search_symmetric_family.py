"""COVERS the upper bound g(7) <= 21 — the generator of data/witness_r7_21.json.

Searches for an intersecting r-uniform family with tau = r that is invariant under a
cyclic group Z_m, by SAT with lazily added cover-blocking clauses.

    python3 code/search_symmetric_family.py R M CARD_ORBITS SYMBOL_ORBITS --degrees D [--seconds S] [--out FILE]

  g(7) <= 21:   python3 code/search_symmetric_family.py 7 7 7,7,7 7,7,7,7,7 --degrees 6,4,4,4,3
  calibration:  python3 code/search_symmetric_family.py 6 4 1,2,2,4,4,4 4,4,4,4,4,2,2,2,1 --degrees 4,4,4,4,3,4,5,2,4
                (the orbit type and degrees of the seventeen-card witness of [P4]; finds a
                 seventeen-card family with tau = 6 in seconds)

Orbit sizes must divide M. The generator cycles every orbit (position k -> k+1 mod size),
and the incidence is invariant: s in c if and only if g(s) in g(c). Card c of orbit o at
position k has index (sum of earlier orbit sizes) + k, and likewise for symbols.

Constraints: every card has exactly R symbols; every two cards meet; every symbol in orbit o
has degree D[o]; no symbol's support lies inside another's (true whenever tau = R, by the
argument of [P3, Lemma 3]). Then: solve, look for an (R-1)-cover, forbid it and all its
images under the group, repeat, until a family with no (R-1)-cover appears (WITNESS) or the
formula is UNSAT.

Only WITNESS answers are used. A witness is re-checked here by a second method (every
(R-1)-set of symbols), and independently by code/verify_witness_r7_21.py. An UNSAT answer
says only that no family of that orbit type and degree profile exists that also satisfies the
lexicographic ordering of interchangeable orbits added below; it is not used anywhere.
Needs python-sat.
"""
import sys, time, json, itertools
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

R, M = int(sys.argv[1]), int(sys.argv[2])
CO = [int(a) for a in sys.argv[3].split(',')]
SO = [int(a) for a in sys.argv[4].split(',')]
LIMIT = float(sys.argv[sys.argv.index('--seconds') + 1]) if '--seconds' in sys.argv else 1e18
assert all(M % a == 0 for a in CO + SO)

cards = [(o, k) for o, a in enumerate(CO) for k in range(a)]
syms = [(o, k) for o, a in enumerate(SO) for k in range(a)]
nc, ns = len(cards), len(syms)
cid = {c: i for i, c in enumerate(cards)}; sid = {s: i for i, s in enumerate(syms)}
gc = [cid[(o, (k + 1) % CO[o])] for o, k in cards]
gs = [sid[(o, (k + 1) % SO[o])] for o, k in syms]

# union-find over incidence cells, merging (c,s) with (g c, g s)
par = list(range(nc * ns))
def find(x):
    while par[x] != x:
        par[x] = par[par[x]]; x = par[x]
    return x
for c in range(nc):
    for s in range(ns):
        a, b = find(c * ns + s), find(gc[c] * ns + gs[s])
        if a != b: par[a] = b
P = IDPool()
X = [[P.id(('x', find(c * ns + s))) for s in range(ns)] for c in range(nc)]

cl = []
enc = EncType.seqcounter
for c in range(nc):
    cl += CardEnc.equals(X[c], R, vpool=P, encoding=enc).clauses
for s in range(ns):
    cl += CardEnc.atleast([X[c][s] for c in range(nc)], 2, vpool=P, encoding=enc).clauses
for c, d in itertools.combinations(range(nc), 2):
    lits = []
    for s in range(ns):
        w = P.id(('meet', c, d, s)); lits.append(w)
        cl += [[-w, X[c][s]], [-w, X[d][s]]]
    cl.append(lits)
for s, t in itertools.permutations(range(ns), 2):          # supp(s) not inside supp(t)
    lits = []
    for c in range(nc):
        w = P.id(('notin', s, t, c)); lits.append(w)
        cl += [[-w, X[c][s]], [-w, -X[c][t]]]
    cl.append(lits)

def lex_geq(A, B, tag):
    """clauses for vector A >=lex B (True > False)"""
    eq = P.id((tag, 'eq', 0)); out = [[eq]]
    for k, (a, b) in enumerate(zip(A, B)):
        nxt = P.id((tag, 'eq', k + 1))
        out.append([-eq, a, -b])                     # while equal, not (a=0, b=1)
        out += [[-nxt, eq], [-nxt, a, -b], [-nxt, -a, b], [-eq, a, b, nxt], [-eq, -a, -b, nxt]]
        eq = nxt
    return out

if '--degrees' in sys.argv:
    DEG = [int(a) for a in sys.argv[sys.argv.index('--degrees') + 1].split(',')]
    assert len(DEG) == len(SO)
    for s_ in range(ns):
        cl += CardEnc.equals([X[c][s_] for c in range(nc)], DEG[syms[s_][0]], vpool=P, encoding=enc).clauses

if '--nosym' not in sys.argv:
    # symbol orbits of equal size are interchangeable: order their representative columns
    reps = {}
    for o, a in enumerate(SO): reps.setdefault((a, DEG[o] if '--degrees' in sys.argv else 0), []).append(sid[(o, 0)])
    for a, lst in reps.items():
        for u, v in zip(lst, lst[1:]):
            cl += lex_geq([X[c][u] for c in range(nc)], [X[c][v] for c in range(nc)], ('ls', u, v))
    creps = {}
    for o, a in enumerate(CO): creps.setdefault(a, []).append(cid[(o, 0)])
    for a, lst in creps.items():
        for u, v in zip(lst, lst[1:]):
            cl += lex_geq(X[u], X[v], ('lc', u, v))

if '--eager' in sys.argv:
    # tau >= R written out: every (R-1)-set of symbols misses some card; by invariance one
    # set per group orbit is enough
    seen = set(); neager = 0
    for T in itertools.combinations(range(ns), R - 1):
        if T in seen: continue
        U = T
        for k in range(M):
            seen.add(tuple(sorted(U))); U = [gs[u] for u in U]
        lits = []
        for c in range(nc):
            z = P.id(('avoidE', T, c)); lits.append(z)
            for t in T: cl.append([-z, -X[c][t]])
        cl.append(lits); neager += 1
    print("eager tau clauses: %d orbit representatives" % neager, flush=True)

S = Solver(name='cadical195', bootstrap_with=cl)

def gpow_sym(s, k):
    for _ in range(k): s = gs[s]
    return s

def find_cover(masks, k, full):
    """an index set of at most k symbols whose card masks cover every card, or None"""
    order = list(range(len(masks)))
    def go(cov, pick):
        if cov == full: return list(pick)
        if len(pick) == k: return None
        rest = full & ~cov
        v = (rest & -rest).bit_length() - 1
        for s in order:
            if masks[s] >> v & 1:
                r = go(cov | masks[s], pick + [s])
                if r is not None: return r
        return None
    return go(0, [])

blocked = set(); it = 0; t0 = time.time()
full = (1 << nc) - 1
while True:
    if time.time() - t0 > LIMIT:
        print("RESULT TIMEOUT after %d covers blocked [%.0fs]" % (len(blocked), time.time() - t0)); break
    if not S.solve():
        print("RESULT UNSAT: no Z_%d-invariant family of this orbit type (%d covers blocked) [%.0fs]"
              % (M, len(blocked), time.time() - t0)); break
    mdl = set(l for l in S.get_model() if l > 0)
    masks = [sum(1 << c for c in range(nc) if X[c][s] in mdl) for s in range(ns)]
    T = find_cover(masks, R - 1, full)
    if T is None:
        fam = [sorted(s for s in range(ns) if masks[s] >> c & 1) for c in range(nc)]
        # independent re-check
        assert all(len(f) == R for f in fam)
        assert all(set(a) & set(b) for a, b in itertools.combinations(fam, 2))
        # brute force over every (R-1)-set of symbols, a different method from find_cover
        def brute():
            for U in itertools.combinations(range(ns), R - 1):
                acc = 0
                for u in U: acc |= masks[u]
                if acc == full: return True
            return False
        assert not brute(), "cover found by brute force"
        assert len(set(map(tuple, fam))) == nc, "repeated card"
        print("RESULT WITNESS: %d cards, %d symbols, tau = %d, Z_%d-invariant [%.0fs]" % (nc, ns, R, M, time.time() - t0))
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else "witness_r%d_n%d.json" % (R, nc)
        json.dump({"r": R, "cards": fam}, open(out, "w"))
        print("wrote", out)
        break
    for k in range(M):                                     # block the cover and all its images
        Tk = tuple(sorted(gpow_sym(s, k) for s in T))
        if Tk in blocked: continue
        blocked.add(Tk)
        lits = []
        for c in range(nc):
            z = P.id(('avoid', Tk, c)); lits.append(z)
            for s in Tk:
                S.add_clause([-z, -X[c][s]])
        S.add_clause(lits)
    it += 1
    if it % 200 == 0:
        print("  progress: %d covers blocked [%.0fs]" % (len(blocked), time.time() - t0), flush=True)
