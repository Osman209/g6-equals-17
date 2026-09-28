"""The second branch of the sixteen-card reduction: kernels of maximum degree three.

COVERS [P3, §2a] — twelve-card kernels G with no degree-four symbol: the enumeration of
the three profiles, and the check that none of them admits a four-cover extension.

WHY THIS BRANCH EXISTS. [P3, §3] reduces a hypothetical sixteen-card counterexample to an
eight-card core H, obtained by deleting the four cards of x and then the four cards of a
second degree-four symbol y of the kernel G. That route needs y to exist. When G has no
degree-four symbol there is no y, no H, and no canonical core, so the 463 cores of
[P3, §3] cannot reach this case. It has to be closed on its own.

The branch is not empty: the twelve-card kernel of the seventeen-card witness of [P4] has
six degree-two symbols and twenty degree-three symbols, so its maximum degree is three.
`--witness` checks that this kernel really is one of the objects enumerated here.

THE ENUMERATION. Let G be a twelve-card pairwise intersecting 6-uniform family with
maximum symbol degree three and tau(G) = 5. Writing (t,b,s) for the numbers of symbols of
degree three, two and one in a card, we have t+b+s = 6, and the card must meet the other
eleven, so 2t+b >= 11. The only solutions are (5,1,0) and (6,0,0); degree-one symbols are
absent. Let c count the cards of the first type. Each such card holds exactly one
degree-two symbol and each degree-two symbol lies in two cards, so c is even and there are
c/2 of them; the degree-three incidences number 72-c and must be divisible by three. Hence
c is a multiple of six, c is 0, 6 or 12, and the profiles are

    c = 12 -> 6 degree-two symbols, 20 degree-three symbols
    c =  6 -> 3 degree-two symbols, 22 degree-three symbols
    c =  0 -> 0 degree-two symbols, 24 degree-three symbols

A (6,0,0) card meets eleven others through six degree-three symbols reaching twelve, so it
carries exactly one unit of intersection excess; a (5,1,0) card reaches exactly eleven and
carries none. So the excess graph is a perfect matching on the 12-c cards of type (6,0,0)
and the degree-two graph is a perfect matching on the c cards of type (5,1,0); together
they are one perfect matching on all twelve cards. The degree-three symbols therefore
decompose the pair multigraph

    M = K12 + E - F

into triangles, where F is the degree-two matching (those pairs are already served) and E
is the excess matching (those pairs are served twice). Up to relabelling M depends only on
c, so there are exactly three models, and a kernel is a triangle decomposition of one of
them. This script enumerates every such decomposition, reduces under Aut(M), keeps those
with tau(G) = 5, and runs the extension test of [P3, Prop 2] on each.

THE TEST. Four five-covers C1..C4 of G extend to a sixteen-card family with tau = 6 if and
only if every five-cover of G is disjoint from at least one of them, subject to the degree
caps d_G(z) + h(z) <= 4 of [P3, §1]. That is a set cover of the five-covers of G by four
disjointness-neighbourhoods, and it is solved exactly here.

Usage:
    python code/verify_degree3_kernels.py                 # check the shipped representatives
    python code/verify_degree3_kernels.py --witness       # plus the [P4] kernel check
    python code/verify_degree3_kernels.py --enumerate 12  # re-derive them from scratch

Re-deriving c = 6 and c = 0 in pure Python takes hours; code/fast_enumerate.c does the
same enumeration and orbit reduction in C and writes the same representative files.
"""
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import sys
import time

V = 12
TRI = list(combinations(range(V), 3))
TIDX = {t: i for i, t in enumerate(TRI)}
PAIRS = list(combinations(range(V), 2))
PI = {p: i for i, p in enumerate(PAIRS)}
TRI_PAIRS = [[PI[p] for p in combinations(t, 2)] for t in TRI]
PAIR_TRI = [[] for _ in range(len(PAIRS))]
for _i, _tp in enumerate(TRI_PAIRS):
    for _p in _tp:
        PAIR_TRI[_p].append(_i)
MATCH = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)]
FULL = (1 << V) - 1
ROOT = Path(__file__).resolve().parents[1]
PROFILES = {12: (6, 20), 6: (3, 22), 0: (0, 24)}


def card_types():
    """Re-derive the two admissible card types and the three values of c."""
    types = [(t, b, 6 - t - b) for t in range(7) for b in range(7 - t) if 2 * t + b >= 11]
    cs = [c for c in range(13) if c % 2 == 0 and (72 - c) % 3 == 0]
    return types, cs


def model(c):
    """Capacities of M = K12 + E - F.  F is the first c/2 matching pairs, E the rest."""
    nF = c // 2
    cap = [1] * len(PAIRS)
    for k, e in enumerate(MATCH):
        cap[PI[e]] = 0 if k < nF else 2
    return cap


def decompositions(cap):
    """Every triangle decomposition of M, with the vertices labelled."""
    cap = cap[:]
    chosen = []
    out = []

    def dfs(left):
        if left == 0:
            out.append(tuple(sorted(chosen)))
            return
        best, bestn = -1, 1 << 30
        for p in range(len(PAIRS)):
            if cap[p]:
                n = sum(1 for i in PAIR_TRI[p] if all(cap[q] for q in TRI_PAIRS[i]))
                if n == 0:
                    return
                if n < bestn:
                    bestn, best = n, p
                if n == 1:
                    break
        for i in PAIR_TRI[best]:
            if not all(cap[q] for q in TRI_PAIRS[i]):
                continue
            for q in TRI_PAIRS[i]:
                cap[q] -= 1
            chosen.append(i)
            dfs(left - 3)
            chosen.pop()
            for q in TRI_PAIRS[i]:
                cap[q] += 1

    dfs(sum(cap))
    # A pair of capacity two can be served by its two triangles in either order, so the
    # search reaches such a decomposition once per order.  Deduplicate.
    return sorted(set(out))


def aut_perms(c):
    """Aut(M): permute F-pairs among themselves and E-pairs among themselves, and swap
       the two cards inside any pair.  Removed and doubled pairs cannot be exchanged."""
    nF = c // 2
    out = []
    for pf in permutations(range(nF)):
        for pe in permutations(range(nF, 6)):
            order = list(pf) + list(pe)
            for flip in range(1 << 6):
                p = [0] * V
                for k in range(6):
                    a, b = MATCH[k]
                    ta, tb = MATCH[order[k]]
                    if flip >> k & 1:
                        ta, tb = tb, ta
                    p[a], p[b] = ta, tb
                out.append(tuple(p))
    return out


def orbit_reduce(decs, perms):
    """One representative per orbit, by marking each orbit whole as it is met."""
    seen, reps = set(), []
    for key in decs:
        if key in seen:
            continue
        reps.append(key)
        verts = [TRI[i] for i in key]
        for p in perms:
            seen.add(tuple(sorted(TIDX[tuple(sorted((p[x], p[y], p[z])))] for x, y, z in verts)))
    return reps


def kernel(key, c):
    """Supports of the symbols: the triangles first, then the degree-two symbols."""
    nF = c // 2
    sup = [(1 << a) | (1 << b) | (1 << d) for a, b, d in (TRI[i] for i in key)]
    sup += [(1 << a) | (1 << b) for a, b in MATCH[:nF]]
    deg = [bin(s).count("1") for s in sup]
    cards = [[j for j, s in enumerate(sup) if s >> i & 1] for i in range(V)]
    return sup, deg, cards


def has_four_cover(sup):
    """Four symbols reach all twelve cards only as four disjoint triples that partition
       them, since 3+3+3+2 = 11 < 12 leaves no room for a degree-two symbol."""
    tri = [s for s in sup if bin(s).count("1") == 3]

    def go(covered, k, start):
        if k == 4:
            return covered == FULL
        for i in range(start, len(tri)):
            if not (tri[i] & covered) and go(covered | tri[i], k + 1, i + 1):
                return True
        return False

    return go(0, 0, 0)


def five_covers(sup):
    """Every five-element transversal, found by always hitting the lowest uncovered card."""
    n = len(sup)
    out = set()
    by = [[i for i in range(n) if sup[i] >> v & 1] for v in range(V)]

    def go(covered, chosen):
        if covered == FULL:
            out.add(tuple(sorted(chosen)))
            return
        if len(chosen) == 5:
            return
        rest = ~covered & FULL
        v = (rest & -rest).bit_length() - 1
        for i in by[v]:
            if i in chosen:
                continue
            chosen.append(i)
            go(covered | sup[i], chosen)
            chosen.pop()

    go(0, [])
    return [t for t in sorted(out) if len(t) == 5]


def extension_exists(covers, deg):
    """Four five-covers obeying d_G(z)+h(z) <= 4 whose disjointness-neighbourhoods cover
       every five-cover of G.  Returns the four indices, or None."""
    n = len(covers)
    if n == 0:
        return None
    sets = [frozenset(c) for c in covers]
    cap = [4 - d for d in deg]
    tri = [0] * n
    binaries = [[] for _ in range(n)]
    for i, c in enumerate(covers):
        for z in c:
            if cap[z] == 1:
                tri[i] |= 1 << z
            else:
                binaries[i].append(z)
    N = [0] * n
    for i in range(n):
        si = sets[i]
        for j in range(i, n):
            if not (si & sets[j]):
                N[i] |= 1 << j
                N[j] |= 1 << i
    universe = (1 << n) - 1
    size = [bin(x).count("1") for x in N]
    mx = max(size)
    options = [sorted((i for i in range(n) if N[i] >> t & 1), key=lambda i: -size[i])
               for t in range(n)]
    for t in range(n):
        if not options[t]:
            return None                       # this five-cover can never be missed

    def dfs(covered, chosen, tri_used, bcount):
        if covered == universe:
            return list(chosen)
        d = len(chosen)
        if d == 4:
            return None
        rem = universe & ~covered
        if bin(rem).count("1") > (4 - d) * mx:
            return None
        bt, bn, r, t = -1, 1 << 30, rem, 0
        while r:
            if r & 1:
                k = len(options[t])
                if k < bn:
                    bn, bt = k, t
                if k <= 1:
                    break
            r >>= 1
            t += 1
        for i in options[bt]:
            if tri_used & tri[i]:
                continue
            if any(bcount.get(z, 0) >= cap[z] for z in binaries[i]):
                continue
            nb = dict(bcount)
            for z in binaries[i]:
                nb[z] = nb.get(z, 0) + 1
            chosen.append(i)
            res = dfs(covered | N[i], chosen, tri_used | tri[i], nb)
            chosen.pop()
            if res is not None:
                return res
        return None

    return dfs(0, [], 0, {})


def reps_path(c):
    return ROOT / "data" / f"degree3_kernels_c{c}.json"


def check(c, reps):
    """Run the whole test on one profile's representatives."""
    nb, nt = PROFILES[c]
    t0 = time.time()
    kept, ext, ncov = 0, [], []
    for key in reps:
        sup, deg, cards = kernel(key, c)
        assert all(len(x) == 6 for x in cards), "a card does not hold six symbols"
        assert all(set(a) & set(b) for a in cards for b in cards), "not pairwise intersecting"
        assert not has_four_cover(sup), "tau(G) <= 4: not a kernel"
        kept += 1
        cov = five_covers(sup)
        assert cov, "tau(G) > 5"
        ncov.append(len(cov))
        if extension_exists(cov, deg) is not None:
            ext.append(key)
    print(f"  profile ({nb} degree-two, {nt} degree-three): kernels {kept}, "
          f"five-covers per kernel "
          f"{min(ncov) if ncov else 0}-{max(ncov) if ncov else 0}, "
          f"four-cover extensions {len(ext)}   [{time.time()-t0:.0f}s]", flush=True)
    return dict(c=c, degree_two=nb, degree_three=nt, representatives=len(reps),
                tau5=kept, five_cover_range=[min(ncov), max(ncov)] if ncov else None,
                extensions=len(ext)), ext


def witness_check():
    """The twelve-card kernel of the [P4] witness must be one of the enumerated objects."""
    w = json.loads((ROOT / "data" / "witness_17.json").read_text())["cards"]
    G = [set(c) for c in w[:12]]
    syms = sorted(set().union(*G))
    deg = {s: sum(1 for c in G if s in c) for s in syms}
    binaries = [s for s in syms if deg[s] == 2]
    triples = [s for s in syms if deg[s] == 3]
    assert max(deg.values()) == 3, "the witness kernel is not a maximum-degree-three kernel"
    assert (len(binaries), len(triples)) == PROFILES[12]
    pairs = [tuple(sorted(i for i in range(12) if s in G[i])) for s in binaries]
    assert sorted(x for p in pairs for x in p) == list(range(12)), "not a perfect matching"
    lab = {}
    for k, (a, b) in enumerate(pairs):
        lab[a], lab[b] = MATCH[k]
    key = tuple(sorted(TIDX[tuple(sorted(lab[i] for i in range(12) if s in G[i]))]
                       for s in triples))
    reps = [tuple(r) for r in json.loads(reps_path(12).read_text())]
    perms = aut_perms(12)
    which = None
    for ri, r in enumerate(reps):
        verts = [TRI[i] for i in r]
        for p in perms:
            if tuple(sorted(TIDX[tuple(sorted((p[x], p[y], p[z])))] for x, y, z in verts)) == key:
                which = ri
                break
        if which is not None:
            break
    assert which is not None, "the witness kernel is NOT in the enumeration"
    sup, dg, _ = kernel(key, 12)
    cov = five_covers(sup)
    print(f"  the [P4] witness kernel is representative #{which} of profile (6, 20); "
          f"tau(G)=5 {not has_four_cover(sup)}, five-covers {len(cov)}, "
          f"four-cover extension {extension_exists(cov, dg) is not None}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enumerate", type=int, choices=[0, 6, 12], default=None,
                    help="re-derive one profile's representatives from scratch")
    ap.add_argument("--witness", action="store_true")
    args = ap.parse_args()

    types, cs = card_types()
    assert types == [(5, 1, 0), (6, 0, 0)], types
    assert cs == [0, 6, 12], cs
    print(f"card types forced to {types}; c forced to {cs}")

    if args.enumerate is not None:
        c = args.enumerate
        t0 = time.time()
        decs = decompositions(model(c))
        n_all = len(decs)
        decs = [k for k in decs if not has_four_cover(kernel(k, c)[0])]
        perms = aut_perms(c)
        reps = orbit_reduce(decs, perms)
        print(f"  c={c}: distinct decompositions {n_all}, of which tau(G)=5 {len(decs)}, "
              f"|Aut(M)|={len(perms)}, kernels up to isomorphism {len(reps)}  "
              f"[{time.time()-t0:.0f}s]")
        reps_path(c).write_text(json.dumps([list(r) for r in reps]) + "\n")
        check(c, reps)
        return

    summary = []
    bad = []
    for c in (12, 6, 0):
        reps = [tuple(r) for r in json.loads(reps_path(c).read_text())]
        row, ext = check(c, reps)
        summary.append(row)
        bad += ext
    if args.witness:
        witness_check()
    total = sum(r["tau5"] for r in summary)
    if bad:
        print(f"FAIL: {len(bad)} kernels admit a four-cover extension")
        raise SystemExit(1)
    print(f"PASS: {total} maximum-degree-three kernels, none admits a four-cover "
          f"extension, so no sixteen-card counterexample has a kernel of this kind.")


if __name__ == "__main__":
    main()
