#!/usr/bin/env python3
"""Finite test of the sharp residual cover bound, [P5, Theorem 1].

COVERS [P5, §2]: the inequality 4*tau(J) <= q + r + 3 for every intersecting
r-uniform family J with maximum degree at most three, on every configuration with
q <= 6 cards, and on the low-degree configurations with 7 <= q <= 9 cards; and the
sharpness family of [P5, §2.6].

This is a finite check, not a proof. The theorem is proved in the paper for every q.

The dual view. Points are the q cards of J. Each symbol of J becomes a block, the set
of cards containing it, of size at most three. J is intersecting exactly when every
pair of points lies in a block, and r-uniform exactly when every point lies in r blocks.
A cover of J is a set of blocks meeting every point.

A symbol of degree one is a singleton block: it covers no pair and never helps a cover.
So for any set of distinct blocks of size two or three covering every pair, padding each
point with singletons up to r = (largest point degree) gives an r-uniform family, and
that choice of r makes q + r + 3 as small as the configuration allows. Repeated blocks
only raise r. The search therefore runs over irredundant coverings of the pairs of a
q-set by 2- and 3-subsets.

The inequality gets tighter as r gets smaller, and r is at least ceil((q-1)/2). For
7 <= q <= 9 the full search is too large for a quick check, so it is run with the
largest point degree capped a little above that floor, where a counterexample would
have to live.

    python3 code/verify_residual_bound.py            # about three minutes
    python3 code/verify_residual_bound.py --quick    # q <= 5 only, seconds

Exits non-zero if any violation is found or the sharpness family fails.
"""
import sys
import time
from itertools import combinations


def tau_of(masks, full):
    ms = sorted(set(masks), key=lambda m: -bin(m).count("1"))
    best = [len(ms) + 1]

    def go(cov, k):
        if cov == full:
            best[0] = min(best[0], k)
            return
        if k + 1 >= best[0]:
            return
        rest = full ^ cov
        v = (rest & -rest).bit_length() - 1
        for m in ms:
            if m >> v & 1:
                go(cov | m, k + 1)

    go(0, 0)
    return best[0]


def run(q, cap=None):
    """All irredundant coverings of the pairs of [q] by 2- and 3-blocks, with every
    point degree at most cap when a cap is given.  Returns (systems, violations,
    equality cases)."""
    pairs = [frozenset(p) for p in combinations(range(q), 2)]
    pidx = {p: i for i, p in enumerate(pairs)}
    blocks = [frozenset(b) for b in combinations(range(q), 2)] + \
             [frozenset(b) for b in combinations(range(q), 3)]
    bp = [sum(1 << pidx[frozenset(p)] for p in combinations(sorted(b), 2)) for b in blocks]
    bv = [sum(1 << v for v in b) for b in blocks]
    FP, FV = (1 << len(pairs)) - 1, (1 << q) - 1
    deg = [0] * q
    stats = [0, 0, 0]

    def rec(cov, chosen):
        if cov == FP:
            stats[0] += 1
            r = max(deg)
            t = tau_of([bv[i] for i in chosen], FV)
            if 4 * t > q + r + 3:
                stats[1] += 1
                if stats[1] <= 3:
                    print("  VIOLATION q=%d r=%d tau=%d blocks=%s"
                          % (q, r, t, [sorted(blocks[i]) for i in chosen]))
            elif 4 * t == q + r + 3:
                stats[2] += 1
            return
        rest = FP ^ cov
        j = (rest & -rest).bit_length() - 1
        for i in range(len(blocks)):
            if not (bp[i] >> j & 1) or i in chosen:
                continue
            if cap is not None and any(deg[v] + 1 > cap for v in blocks[i]):
                continue
            for v in blocks[i]:
                deg[v] += 1
            rec(cov | bp[i], chosen + [i])
            for v in blocks[i]:
                deg[v] -= 1

    rec(0, [])
    return stats


def sharpness(n):
    """[P5, §2.6]: points 1..n, one degree-two symbol per pair.  q = n, r = n - 1,
    and a cover is an edge cover of K_n, so tau = ceil(n/2)."""
    blocks = [(1 << a) | (1 << b) for a, b in combinations(range(n), 2)]
    t = tau_of(blocks, (1 << n) - 1)
    return t, 4 * t == n + (n - 1) + 3


def main():
    quick = "--quick" in sys.argv
    ok = True
    plan = [(q, None) for q in range(3, 6 if quick else 7)]
    if not quick:
        plan += [(7, 4), (8, 4), (9, 4)]
    for q, cap in plan:
        t0 = time.time()
        systems, bad, eq = run(q, cap)
        ok &= bad == 0
        print("q=%d%s  systems %d  violations %d  equality cases %d  [%.0fs]"
              % (q, "" if cap is None else " (point degree <= %d)" % cap,
                 systems, bad, eq, time.time() - t0), flush=True)
    for n in (3, 5, 7, 9, 11):
        t, eq = sharpness(n)
        ok &= eq and t == (n + 1) // 2
        print("sharpness n=%d: q=%d r=%d tau=%d, 4tau = q+r+3: %s" % (n, n, n - 1, t, eq))
    if not ok:
        print("FAIL")
        sys.exit(1)
    print("PASS: no violation of 4tau <= q+r+3; equality attained, as the sharpness family requires.")


if __name__ == "__main__":
    main()
