#!/usr/bin/env python3
"""The anchor count of [P5, §4.3]: the finite facts behind the exclusion of u = 11.

COVERS [P5, Lemmas 12 and 13 and Proposition 2]: for u = 11 and each d = 1, 2, 3, 4,
over every multicoloured local graph that satisfies both capacities (colour: 2e - s <= d;
pointwise: sum over colours of max(deg_c(x) - 1, 0) <= d at every vertex),

  (a) the number A of open pairs is at most 12 - S          (the supply side);
  (b) every such graph with S >= 11 has anchor value G >= 16  (the demand side);

and then the resulting inequality 11t + 16 > 12t + 1 for t = 10 - d.  For d = 5 (the open
case at r = 15) it reports the smallest anchor value, which is 0: a star reaches S = 11
and forces nothing.  That run is informational and does not affect the exit code.

Definitions, as in the paper.  (x, c) is OPEN in F if no edge of colour c meets x and
every edge of the other two colours meets x.  For an anchor F and x in U, P_x is the set
of colours with no edge at x.  A pair of colours in P_x is FORBIDDEN if F has an edge of
the third colour avoiding x.  A colour c in P_x is GOOD if for every pair f of U with
x not in f and f not an edge of F, F has an edge of a colour other than c avoiding x
and f.  For R contained in P_x with all its pairs forbidden,
    g_x = |R| - |P_x minus R| - (number of colours in R that are not good),
maximised over R, and G = sum over x of max(g_x, 0).

    python3 code/verify_anchor_count.py      # about four minutes

Exits non-zero if (a) or (b) fails for some d <= 4, or the inequality fails.
"""
import sys
import time
from itertools import combinations

sys.path.insert(0, __import__("os").path.dirname(__file__))
import verify_local_graphs as V  # noqa: E402


def open_pairs(F, u):
    A = 0
    for x in range(u):
        for c in range(3):
            if any(x in e for e in F[c]):
                continue
            if all(x in e for j in range(3) if j != c for e in F[j]):
                A += 1
    return A


def anchor_value(F, u):
    M = [[(1 << a) | (1 << b) for a, b in col] for col in F]
    alle = [(1 << a) | (1 << b) for a, b in combinations(range(u), 2)]
    inF = {e for col in M for e in col}
    G = 0
    for x in range(u):
        bx = 1 << x
        P = [c for c in range(3) if not any(e & bx for e in M[c])]
        if not P:
            continue
        fs = [f for f in alle if not (f & bx) and f not in inF]

        def forbidden(c1, c2):
            return any(not (e & bx) for e in M[3 - c1 - c2])

        def good(c):
            E = [e for j in range(3) if j != c for e in M[j] if not (e & bx)]
            return all(any(not (e & f) for e in E) for f in fs)

        best = 0
        for k in range(1, len(P) + 1):
            for R in combinations(P, k):
                if all(forbidden(a, b) for a, b in combinations(R, 2)):
                    best = max(best, len(R) - (len(P) - len(R))
                               - sum(1 for c in R if not good(c)))
        G += best
    return G


def run(u, d):
    st = dict(n=0, bad_supply=0, n_anchor=0, Gmin=None, shapes={})

    def visit(F):
        st['n'] += 1
        S = sum(len({x for e in c for x in e}) for c in F)
        if open_pairs(F, u) > 12 - S:
            st['bad_supply'] += 1
        if S >= 11:
            st['n_anchor'] += 1
            G = anchor_value(F, u)
            if st['Gmin'] is None or G < st['Gmin']:
                st['Gmin'] = G
            verts = len({x for c in F for e in c for x in e})
            key = (S, verts, tuple(sorted(len(c) for c in F)))
            st['shapes'][key] = min(st['shapes'].get(key, 99), G)

    V.enumerate_multicoloured(u, d=d, pointwise=True, visit=visit)
    return st


def main():
    u = 11
    ok = True
    for d in (1, 2, 3, 4, 5):
        t0 = time.time()
        st = run(u, d)
        t = u - d - 1
        shapes = ", ".join("S=%d on %d vertices %s: G=%d" % (k[0], k[1], k[2], g)
                           for k, g in sorted(st['shapes'].items()))
        print("u=11 d=%d (r=%d, t=%d): %d multicoloured graphs; supply A <= 12-S violated %d "
              "times; anchors with S >= 11: %d, smallest G = %s  [%.0fs]"
              % (d, 2 * u - 2 - d, t, st['n'], st['bad_supply'], st['n_anchor'],
                 st['Gmin'], time.time() - t0), flush=True)
        print("      shapes: %s" % shapes, flush=True)
        if d <= 4:
            closes = 11 * t + 16 > 12 * t + 1
            print("      11t + 16 = %d > 12t + 1 = %d: %s" % (11 * t + 16, 12 * t + 1, closes))
            ok &= st['bad_supply'] == 0 and st['Gmin'] is not None and st['Gmin'] >= 16 and closes
        else:
            print("      d = 5 is the open case: a graph with S >= 11 and G = %s exists, so the "
                  "anchor count gives nothing there." % st['Gmin'])
    if not ok:
        print("FAIL")
        sys.exit(1)
    print("PASS: for u = 11 and 1 <= d <= 4 every configuration has an anchor with G >= 16, "
          "and the count excludes it.")


if __name__ == "__main__":
    main()
