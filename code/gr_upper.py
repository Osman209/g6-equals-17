#!/usr/bin/env python3
"""g(r) upper bound by the kernel-plus-extension route.

COVERS the construction behind 4r-7 for r = 4, 5, 6 (it reproduces 17 at r = 6) and the
r = 7 attempt; a search, not a proof of any lower bound.

Reads only the standard library plus python-sat.

    python gr_upper.py 6      -> must reproduce 17 cards on 27 symbols
    python gr_upper.py 7      -> tests whether g(7) <= 21

The kernel is a linear r-uniform intersecting family on N = 3r-6 cards whose
symbols all have degree 2 or 3, built as a triangle decomposition of K_N minus a
perfect matching when N is even, and a Steiner triple system on N points when
N = 3 mod 6.  Cards are the N vertices; the symbols of a card are the blocks
through it.  tau(kernel) = r-1 holds exactly when no r-2 of the blocks partition
the N cards.

Then r-1 of the (r-1)-covers of the kernel are chosen so that every (r-1)-cover
of the kernel is disjoint from at least one chosen one, a fresh symbol z is added
to each of them, and the r-1 resulting cards are appended.  The finished family
is re-verified from scratch: r-uniform, pairwise intersecting, no (r-1)-cover.

Output is one line per stage.  Full detail goes to gr_upper_<r>.log.
"""
import sys, json, random, time
from itertools import combinations

LOG = None
def say(s):
    print(s, flush=True)
    if LOG: LOG.write(s + "\n"); LOG.flush()
def note(s):
    if LOG: LOG.write(s + "\n"); LOG.flush()


# ---------------------------------------------------------------- kernels

def decompose(N, rng, node_limit=200000):
    """blocks of the kernel on N cards: triangles, plus matching edges if N is even.
    Randomised backtracking exact cover of the pairs by triangles; a greedy pass
    fails often at N = 15, backtracking does not."""
    match = [frozenset((2 * i, 2 * i + 1)) for i in range(N // 2)] if N % 2 == 0 else []
    pairs = [(a_, b_) for a_ in range(N) for b_ in range(a_ + 1, N)]
    PI = {}
    for i, (x, y) in enumerate(pairs):
        PI[(x, y)] = PI[(y, x)] = i
    used = [False] * len(pairs)
    for m in match:
        x, y = sorted(m)
        used[PI[(x, y)]] = True
    tri = []
    budget = [node_limit]

    def go():
        budget[0] -= 1
        if budget[0] < 0:
            return False
        try:
            i = used.index(False)
        except ValueError:
            return True
        x, y = pairs[i]
        cand = [c for c in range(N) if c != x and c != y
                and not used[PI[(x, c)]] and not used[PI[(y, c)]]]
        rng.shuffle(cand)
        for c in cand:
            ix = (PI[(x, y)], PI[(x, c)], PI[(y, c)])
            for k in ix:
                used[k] = True
            tri.append(frozenset((x, y, c)))
            if go():
                return True
            tri.pop()
            for k in ix:
                used[k] = False
        return False

    return (tri + match) if go() else None


def kernel(N, r, rng):
    blocks = decompose(N, rng)
    if blocks is None:
        return None
    cards = [frozenset(j for j, s in enumerate(blocks) if v in s) for v in range(N)]
    if any(len(c) != r for c in cards):
        return None
    if any(not (a & b) for a, b in combinations(cards, 2)):
        return None
    return blocks, cards


# ---------------------------------------------------------- covers of a kernel

def covers(masks, k, N, limit=None):
    """every k-subset of the blocks whose supports meet all N cards"""
    full = (1 << N) - 1
    order = sorted(range(len(masks)), key=lambda i: -bin(masks[i]).count("1"))
    m = [masks[i] for i in order]
    top = bin(m[0]).count("1")
    out = []
    n = len(m)

    def go(i, cov, pick):
        left = k - len(pick)
        if left == 0:
            if cov == full:
                out.append(tuple(sorted(order[j] for j in pick)))
            return
        if bin(full ^ cov).count("1") > top * left:
            return
        if limit and len(out) > limit:
            return
        for j in range(i, n - left + 1):
            go(j + 1, cov | m[j], pick + [j])

    go(0, 0, [])
    return out


def tau(masks, N, cap):
    for k in range(2, cap + 2):
        if covers(masks, k, N, limit=1):
            return k
    return None


# --------------------------------------------------------------- the selection

def served_sets(covs):
    """candidate j serves every i whose cover is disjoint from cover j, as a bitmask"""
    S = [frozenset(c) for c in covs]
    n = len(S)
    return [sum(1 << i for i in range(n) if not (S[i] & S[j])) for j in range(n)]


def feasible(served, need):
    n = len(served)
    sizes = sorted((bin(x).count("1") for x in served), reverse=True)
    reach = sum(sizes[:need])
    return reach >= n, reach, n, (sizes[0] if sizes else 0)


def greedy(served, covs, need, rng, restarts=60):
    n = len(served)
    full = (1 << n) - 1
    for t in range(restarts):
        left = full
        pick = []
        while left and len(pick) < need:
            gains = [(bin(served[j] & left).count("1"), j) for j in range(n)]
            gains.sort(reverse=True)
            if gains[0][0] == 0:
                break
            band = [j for g, j in gains[:8] if g >= gains[0][0] - (1 if t else 0)]
            j = rng.choice(band) if t else gains[0][1]
            pick.append(j)
            left &= ~served[j]
        if not left:
            return [covs[j] for j in pick]
    return None


def exact(served, covs, need, budget=120.0):
    """exact set cover of the covers by the covers, at size `need`.
    Branch on the uncovered element with the fewest servers; depth is `need`,
    so this is a complete search and needs no solver."""
    n = len(served)
    full = (1 << n) - 1
    servers = [[j for j in range(n) if served[j] >> i & 1] for i in range(n)]
    if any(not sv for sv in servers):
        note("some cover meets every cover, so no selection can exist")
        return None
    sizes = [bin(x).count("1") for x in served]
    best_gain = max(sizes)
    pick = []
    stop = time.time() + budget
    out_of_time = [False]

    def go(left, depth):
        if left == 0:
            return True
        if depth == need:
            return False
        if time.time() > stop:
            out_of_time[0] = True
            return False
        if bin(left).count("1") > best_gain * (need - depth):
            return False
        # the uncovered element that is hardest to serve
        hard, hn = -1, 1 << 30
        x = left
        while x:
            i = (x & -x).bit_length() - 1
            x &= x - 1
            c = len(servers[i])
            if c < hn:
                hn, hard = c, i
                if c == 1:
                    break
        for j in sorted(servers[hard], key=lambda j: -bin(served[j] & left).count("1")):
            pick.append(j)
            if go(left & ~served[j], depth + 1):
                return True
            pick.pop()
        return False

    if go(full, 0):
        return [covs[j] for j in pick]
    note("exact search %s" % ("ran out of its %.0fs budget" % budget
                              if out_of_time[0] else "is complete: no selection exists"))
    return None


# ------------------------------------------------------------- final check

def check(blocks, cards, chosen, r):
    z = len(blocks)
    fam = [set(c) for c in cards] + [set(d) | {z} for d in chosen]
    assert all(len(c) == r for c in fam), "not r-uniform"
    assert len(set(map(frozenset, fam))) == len(fam), "repeated card"
    for a, b in combinations(fam, 2):
        assert a & b, "two cards miss each other"
    used = sorted({x for c in fam for x in c})
    full = (1 << len(fam)) - 1
    ms = [sum(1 << i for i, c in enumerate(fam) if x in c) for x in used]
    ms.sort(key=lambda x: -bin(x).count("1"))
    top = bin(ms[0]).count("1")

    def go(cov, k):
        if cov == full:
            return True
        if k == r - 1:
            return False
        rest = full ^ cov
        if k + -(-bin(rest).count("1") // top) > r - 1:
            return False
        v = (rest & -rest).bit_length() - 1
        for x in ms:
            if (x >> v & 1) and go(cov | x, k + 1):
                return True
        return False

    assert not go(0, 0), "the family has an (r-1)-cover, so tau < r"
    # tau <= r is automatic: any card's r symbols meet every card
    return len(fam), len(used)


# ------------------------------------------------------------------- driver

def run(r, seeds, fast=False, budget=120.0):
    N = 3 * r - 6
    say("r = %d, kernel target N = 3r-6 = %d, family target 4r-7 = %d"
        % (r, N, 4 * r - 7))
    t0 = time.time()
    tried = nokernel = badtau = nosel = 0
    for s in range(seeds):
        k = kernel(N, r, random.Random(s))
        if k is None:
            nokernel += 1
            continue
        blocks, cards = k
        tried += 1
        masks = [sum(1 << v for v in b) for b in blocks]
        t = tau(masks, N, r - 1)
        if t != r - 1:
            badtau += 1
            note("seed %d: tau(kernel) = %s, wanted %d" % (s, t, r - 1))
            continue
        cov = covers(masks, r - 1, N)
        sv = served_sets(cov)
        ok, reach, total, big = feasible(sv, r - 1)
        note("seed %d: tau = %d, %d covers, largest candidate serves %d, "
             "best %d candidates reach %d of %d -> %s"
             % (s, t, len(cov), big, r - 1, reach, total,
                "possible" if ok else "IMPOSSIBLE"))
        if not ok:
            nosel += 1
            continue
        ch = greedy(sv, cov, r - 1, random.Random(s))
        if ch is None and not fast:
            ch = exact(sv, cov, r - 1, budget=budget)
        if ch is None:
            nosel += 1
            note("seed %d: no selection of %d" % (s, r - 1))
            continue
        m, ns = check(blocks, cards, ch, r)
        say("RESULT r=%d: %d cards on %d symbols, tau = %d, so g(%d) <= %d   [%.0fs]"
            % (r, m, ns, r, r, m, time.time() - t0))
        say("        kernel %d cards, %d blocks, %d covers of size %d"
            % (N, len(blocks), len(cov), r - 1))
        fam = [sorted(c) for c in cards] + [sorted(set(d) | {len(blocks)}) for d in ch]
        json.dump({"r": r, "cards": fam,
                   "kernel_blocks": [sorted(b) for b in blocks],
                   "chosen_covers": [list(c) for c in ch]},
                  open("gr_witness_%d.json" % r, "w"), indent=1)
        say("        written to gr_witness_%d.json" % r)
        return m
    say("FAIL r=%d: no witness of this shape in %d seeds "
        "(%d kernels built, %d wrong tau, %d no selection)   [%.0fs]"
        % (r, seeds, tried, badtau, nosel, time.time() - t0))
    return None


if __name__ == "__main__":
    r = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    seeds = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    fast = "--fast" in sys.argv
    budget = 120.0
    for a in sys.argv:
        if a.startswith("--budget="):
            budget = float(a.split("=")[1])
    LOG = open("gr_upper_%d%s.log" % (r, "_fast" if fast else ""), "w")
    say("mode: %s, %d seeds%s"
        % ("greedy only" if fast else "greedy then complete search",
           seeds, "" if fast else ", %.0fs budget per kernel" % budget))
    run(r, seeds, fast=fast, budget=budget)
