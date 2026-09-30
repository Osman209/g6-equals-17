#!/usr/bin/env python3
"""A measurement, not a proof: the clean model of [P5, §6.3].

COVERS [P5, §6.3]: the worst-case probability that a uniformly random perfect matching
of K_u shares an edge with each of four given edge covers, for u = 8, 10, 12 (exact over
all perfect matchings) and u = 16, 24 (sampled, with the adversarial optimum re-evaluated
on a fresh sample to remove the bias of searching on the sample it is scored on).

The four edge covers stand for the pair-symbols inside the four cards of one peeled
group, when the remainder is exactly the pair family.  Perfect matchings are the
sparsest edge covers, and the search is restricted to them.  The search is a local
search: it finds bad configurations but cannot certify that nothing worse exists,
except at u = 8 and u = 10, where the exhaustive values are known (0 and 7/945).

    python3 code/measure_matching_hits.py           # about ten minutes
    python3 code/measure_matching_hits.py --quick   # u = 8, 10 only

Exits non-zero only if the u = 8 and u = 10 values differ from the exhaustive ones,
which would mean the search code is wrong.
"""
import itertools
import random
import sys


def setup(u):
    edges = list(itertools.combinations(range(u), 2))
    eid = {}
    for i, (a, b) in enumerate(edges):
        eid[(a, b)] = eid[(b, a)] = i
    return edges, eid


def all_pms(u, eid):
    out = []

    def go(rem, cur):
        if not rem:
            out.append(cur)
            return
        a = rem[0]
        for b in rem[1:]:
            go([x for x in rem if x not in (a, b)], cur | 1 << eid[(a, b)])

    go(list(range(u)), 0)
    return out


def rand_pm(u, eid, rng):
    v = list(range(u))
    rng.shuffle(v)
    return sum(1 << eid[(v[i], v[i + 1])] for i in range(0, u, 2))


def switch(m, edges, eid, rng):
    E = [e for e in range(len(edges)) if m >> e & 1]
    a, b = rng.sample(E, 2)
    (x, y), (z, w) = edges[a], edges[b]
    m &= ~((1 << a) | (1 << b))
    if rng.random() < .5:
        return m | 1 << eid[(x, z)] | 1 << eid[(y, w)]
    return m | 1 << eid[(x, w)] | 1 << eid[(y, z)]


def prob(Es, P):
    return sum(1 for p in P if all(p & e for e in Es)) / len(P)


def search(u, P, steps, restarts, seed):
    edges, eid = setup(u)
    rng = random.Random(seed)
    best, bestEs = 1.0, None
    for _ in range(restarts):
        Es = [rand_pm(u, eid, rng) for _ in range(4)]
        cur = prob(Es, P)
        for _ in range(steps):
            i = rng.randrange(4)
            old = Es[i]
            Es[i] = switch(Es[i], edges, eid, rng)
            new = prob(Es, P)
            if new <= cur:
                cur = new
            else:
                Es[i] = old
        if cur < best:
            best, bestEs = cur, list(Es)
    return best, bestEs


def exhaustive_min(u):
    """u = 8: minimum over all quadruples with the first matching fixed."""
    edges, eid = setup(u)
    P = all_pms(u, eid)
    best = 1.0
    for x in range(len(P)):
        for y in range(x, len(P)):
            for z in range(y, len(P)):
                best = min(best, prob([P[0], P[x], P[y], P[z]], P))
                if best == 0:
                    return best
    return best


def main():
    quick = "--quick" in sys.argv
    ok = True
    m8 = exhaustive_min(8)
    print("u=8   exhaustive worst probability %.4f" % m8, flush=True)
    ok &= m8 == 0
    _, eid = setup(10)
    P10 = all_pms(10, eid)
    b10, _ = search(10, P10, 300, 6, 1)
    print("u=10  search worst %.4f (exhaustive value 7/945 = %.4f)" % (b10, 7 / 945), flush=True)
    ok &= abs(b10 - 7 / 945) < 1e-9
    if not quick:
        _, eid = setup(12)
        b12, _ = search(12, all_pms(12, eid), 150, 6, 1)
        print("u=12  search worst %.4f (exact over all 10,395 perfect matchings)" % b12, flush=True)
        for u in (16, 24):
            _, eid = setup(u)
            rng = random.Random(1)
            sample = [rand_pm(u, eid, rng) for _ in range(4000)]
            b, Es = search(u, sample, 250, 6, 1)
            rng2 = random.Random(7)
            fresh = [rand_pm(u, eid, rng2) for _ in range(30000)]
            print("u=%d  search worst on its own sample %.4f, same configuration on a fresh "
                  "sample of 30,000: %.4f" % (u, b, prob(Es, fresh)), flush=True)
    print("independent-Poisson value (1 - e^(-1/2))^4 = %.4f" % ((1 - 2.718281828 ** -0.5) ** 4))
    if not ok:
        print("FAIL: the search disagrees with the exhaustive values")
        sys.exit(1)
    print("DONE: measurement recorded; this is not a proof of any bound.")


if __name__ == "__main__":
    main()
