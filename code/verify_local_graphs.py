#!/usr/bin/env python3
"""Exhaustive checks of the local coloured-graph lemmas of [P5].

COVERS [P5, Lemmas 2, 3, 6, 7 and the finite steps of §3.6 and §3.9]:

  L2   S <= max(12, u+4) for every multicoloured local graph; with colour capacity
       2e - s <= d also S <= max(12, u+2, d+8), and the refined bound
       S <= max(u, 12, min(u+4, d+8), min(u+2, 3d+6));
  L3   (small excess) u <= 9 and 2e - s <= 1 per colour give S <= 12, S != 11, and
       S = 12 only for the three perfect matchings of a K4;
  L6   sigma = S - (number of edges) <= 6 for every multicoloured local graph;
  L7   with the pointwise capacity  sum_c max(deg_c(x) - 1, 0) <= d  at every vertex as
       well, every multicoloured graph has S <= max(12, d+8);
  d0   u <= 9, every colour a matching: at most six edges, six only as a K4, five only
       as K4 minus an edge; and K7 does not split into four such graphs;
  s5   u = 13, d = 5, both capacities: a multicoloured graph with S = 13 has sigma <= 4;
  ep   u = 11, d = 1: at most three eligible pairs, an eligible pair forces S <= 6, and
       the number of eligible pairs is at most 12 - S; and Lemma 3 for multicoloured
       graphs at u = 11 (S <= 12, S != 11, S = 12 only as a K4).

A local graph is a simple graph on u vertices whose edges carry one of three colours,
two DISJOINT edges never having different colours.  Monochromatic graphs satisfy every
bound above trivially (S = s <= u), so only multicoloured ones are enumerated.  WLOG
(relabel colours and vertices) colour 2 contains the edge {0,1}; then every colour-1 and
colour-3 edge meets {0,1}, and edges avoiding {0,1} can only have colour 2.

    python3 code/verify_local_graphs.py          # about four minutes
    python3 code/verify_local_graphs.py --full   # u up to 12 and 13, about fifteen minutes

Exits non-zero on the first violated claim.
"""
import sys
import time
from itertools import combinations

FAIL = []


def fail(msg):
    if len(FAIL) < 5:
        print("  FAIL:", msg, flush=True)
    FAIL.append(msg)


def enumerate_multicoloured(u, d=None, pointwise=False, visit=None):
    """Visit every multicoloured local graph on u vertices (colour lists 1,2,3), with
    colour capacity 2e - s <= d and optionally the pointwise capacity."""
    T = [(0, v) for v in range(2, u)] + [(1, v) for v in range(2, u)]
    R = list(combinations(range(2, u), 2))
    col = {1: [], 2: [(0, 1)], 3: []}
    deg = {c: [0] * u for c in (1, 2, 3)}
    deg[2][0] = deg[2][1] = 1

    def meets(a, b):
        return a[0] in b or a[1] in b

    def exc(es):
        return 2 * len(es) - len({x for e in es for x in e}) if es else 0

    def add(e, c):
        col[c].append(e)
        deg[c][e[0]] += 1
        deg[c][e[1]] += 1

    def rem(e, c):
        col[c].pop()
        deg[c][e[0]] -= 1
        deg[c][e[1]] -= 1

    def ok(e, c):
        for c2 in (1, 2, 3):
            if c2 != c and any(not meets(e, f) for f in col[c2]):
                return False
        if d is None and not pointwise:
            return True
        add(e, c)
        good = (d is None or exc(col[c]) <= d) and (not pointwise or all(
            sum(max(deg[k][x] - 1, 0) for k in (1, 2, 3)) <= d for x in e))
        rem(e, c)
        return good

    def phase2(i, others):
        if i == len(R):
            visit([list(col[1]), list(col[2]), list(col[3])])
            return
        phase2(i + 1, others)
        e = R[i]
        if all(meets(e, f) for f in others) and ok(e, 2):
            add(e, 2)
            phase2(i + 1, others)
            rem(e, 2)

    def rec(i):
        if i == len(T):
            if col[1] or col[3]:
                phase2(0, col[1] + col[3])
            return
        rec(i + 1)
        for c in (1, 2, 3):
            if ok(T[i], c):
                add(T[i], c)
                rec(i + 1)
                rem(T[i], c)

    rec(0)


def sup(es):
    return len({x for e in es for x in e})


def exc(es):
    return 2 * len(es) - sup(es) if es else 0


def check_L2_L3_L6(u):
    st = dict(n=0, maxS=0, maxsig=0)

    def visit(F):
        st['n'] += 1
        S = sum(sup(c) for c in F)
        E = sum(len(c) for c in F)
        dd = max(exc(c) for c in F)
        st['maxS'] = max(st['maxS'], S)
        st['maxsig'] = max(st['maxsig'], S - E)
        if S > max(12, u + 4):
            fail("L2 u=%d S=%d" % (u, S))
        if S > max(12, u + 2, dd + 8):
            fail("L2 strengthened u=%d S=%d d=%d" % (u, S, dd))
        if S > max(u, 12, min(u + 4, dd + 8), min(u + 2, 3 * dd + 6)):
            fail("L2 refined u=%d S=%d d=%d" % (u, S, dd))
        if S - E > 6:
            fail("L6 u=%d sigma=%d" % (u, S - E))
        if u <= 9 and dd <= 1:
            if S > 12 or S == 11:
                fail("L3 u=%d S=%d" % (u, S))
            if S == 12:
                verts = {x for c in F for e in c for x in e}
                if not (all(len(c) == 2 for c in F) and len(verts) == 4):
                    fail("L3 S=12 is not a K4")

    enumerate_multicoloured(u, visit=visit)
    return st


def check_L7(u, d):
    st = dict(n=0, maxS=0)

    def visit(F):
        st['n'] += 1
        S = sum(sup(c) for c in F)
        st['maxS'] = max(st['maxS'], S)
        if S > max(12, d + 8):
            fail("L7 u=%d d=%d S=%d" % (u, d, S))

    enumerate_multicoloured(u, d=d, pointwise=True, visit=visit)
    return st


def check_s5():
    st = dict(n=0, n13=0, maxsig=-1)

    def visit(F):
        st['n'] += 1
        S = sum(sup(c) for c in F)
        if S == 13:
            st['n13'] += 1
            st['maxsig'] = max(st['maxsig'], S - sum(len(c) for c in F))

    enumerate_multicoloured(13, d=5, pointwise=True, visit=visit)
    if st['maxsig'] > 4:
        fail("s5: sigma %d > 4" % st['maxsig'])
    return st


def check_ep():
    st = dict(n=0, maxA=0)

    def visit(F):
        st['n'] += 1
        S = sum(sup(c) for c in F)
        A = 0
        for x in range(11):
            for c in range(3):
                if any(x in e for e in F[c]):
                    continue
                if all(x in e for j in range(3) if j != c for e in F[j]):
                    A += 1
        st['maxA'] = max(st['maxA'], A)
        if A > 3 or (A and S > 6) or A > 12 - S:
            fail("ep: A=%d S=%d" % (A, S))
        # Lemma 3 for multicoloured graphs at u = 11 (the r = 19 step uses it there)
        if S > 12 or S == 11:
            fail("L3 at u=11: S=%d" % S)
        if S == 12 and not (all(len(col) == 2 for col in F)
                            and len({x for col in F for e in col for x in e}) == 4):
            fail("L3 at u=11: S=12 is not a K4")

    enumerate_multicoloured(11, d=1, visit=visit)
    return st


def d0_pieces(u, maxe=8):
    """edge sets on u vertices admitting a colouring with every colour a matching and
    disjoint edges always the same colour"""
    allE = list(combinations(range(u), 2))

    def colourable(E):
        col = [0] * len(E)

        def go(i):
            if i == len(E):
                return True
            for c in (1, 2, 3):
                good = True
                for j in range(i):
                    meet = bool(set(E[i]) & set(E[j]))
                    if (col[j] == c and meet) or (col[j] != c and not meet):
                        good = False
                        break
                if good:
                    col[i] = c
                    if go(i + 1):
                        return True
            return False

        return go(0)

    out = []

    def rec(start, cur):
        out.append(tuple(cur))
        if len(cur) == maxe:
            return
        for i in range(start, len(allE)):
            cur.append(allE[i])
            if colourable(cur):
                rec(i + 1, cur)
            cur.pop()

    rec(0, [])
    return out


def check_d0():
    for u in range(4, 10):
        P = d0_pieces(u)
        m = max(len(p) for p in P)
        six = all(len({x for e in p for x in e}) == 4 for p in P if len(p) == 6)
        five = all(len({x for e in p for x in e}) == 4 for p in P if len(p) == 5)
        if m > 6 or not six or not five:
            fail("d0 u=%d" % u)
        print("d0 u=%d: %d graphs, at most %d edges, six only as K4: %s, five only as K4-e: %s"
              % (u, len(P), m, six, five), flush=True)
    P = [frozenset(p) for p in d0_pieces(7) if p]
    allE = frozenset(combinations(range(7), 2))
    byedge = {e: [p for p in P if e in p] for e in allE}

    def cover(left, k):
        if not left:
            return True
        if k == 4 or len(left) > 6 * (4 - k):
            return False
        e = min(left, key=lambda x: len(byedge[x]))
        return any(p <= left and cover(left - p, k + 1) for p in byedge[e])

    split = cover(allE, 0)
    if split:
        fail("d0: K7 splits into four graphs")
    print("d0 (u,t)=(7,4): K7 splits into four such graphs: %s" % split, flush=True)


def main():
    full = "--full" in sys.argv
    top2 = 12 if full else 11
    for u in range(3, top2 + 1):
        t0 = time.time()
        st = check_L2_L3_L6(u)
        print("L2/L3/L6 u=%d: multicoloured graphs %d, max S %d, max sigma %d  [%.0fs]"
              % (u, st['n'], st['maxS'], st['maxsig'], time.time() - t0), flush=True)
    top7 = 13 if full else 12
    for u in range(4, top7 + 1):
        for d in range(0, 6):
            t0 = time.time()
            st = check_L7(u, d)
            print("L7 u=%d d=%d: graphs %d, max S %d, bound %d  [%.0fs]"
                  % (u, d, st['n'], st['maxS'], max(12, d + 8), time.time() - t0), flush=True)
    check_d0()
    t0 = time.time()
    st = check_ep()
    print("ep u=11 d=1: graphs %d, max eligible pairs %d  [%.0fs]"
          % (st['n'], st['maxA'], time.time() - t0), flush=True)
    if full:
        t0 = time.time()
        st = check_s5()
        print("s5 u=13 d=5: graphs %d, with S=13: %d, max sigma %d  [%.0fs]"
              % (st['n'], st['n13'], st['maxsig'], time.time() - t0), flush=True)
    if FAIL:
        print("FAIL: %d violations" % len(FAIL))
        sys.exit(1)
    print("PASS: every local lemma holds on every configuration checked.")


if __name__ == "__main__":
    main()
