#!/usr/bin/env python3
"""Exact rational certificate for the minimisation in Theorem 5 of [P5].

COVERS [P5, Theorem 5]: over gamma in [1, 2], c(gamma) <= lambda <= (4/5) X_T,
0 <= sigma <= 4 X_T, the lower bound

    x >= (5/4) (lambda + max(delta_1, delta_2)) + sigma/4,
    delta_1 = max(K, 0) v / (2 (v + 3N))                      (Lemma 22)
    delta_2 = min(v/16, v (Q - K_-)_+ / (2 + 9v + 9N))        (Lemma 23)

is at least X_T = 0.1024745 everywhere.  Branch and bound with exact Fraction
interval arithmetic: every accepted box is compared to X_T as an exact rational.
It checks arithmetic only; the lemmas that supply the inequalities are in the paper.

Adapted from the rational verifier written by the author for the bound 0.1024
(quantitative_weak_bound_3_1024), with the target raised and the root enclosure
made finer.  Standard library only.  Do not run with python -O.

    python3 code/verify_weak_trace_bound.py            # certifies 0.1024745 (a few minutes)
    python3 code/verify_weak_trace_bound.py --target=1024746/10000000 --limit=200000
                                                        # above the minimum: must fail
"""
from fractions import Fraction as F
from functools import lru_cache
import sys, time

X_T = F(1024745, 10**7)
LIMIT = 6_000_000
for a in sys.argv[1:]:
    if a.startswith("--target="):
        p, q = a.split("=")[1].split("/")
        X_T = F(int(p), int(q))
    if a.startswith("--limit="):
        LIMIT = int(a.split("=")[1])


class I:
    def __init__(self, a, b=None):
        self.a = F(a); self.b = F(a if b is None else b)
    def __add__(self, o):
        o = o if isinstance(o, I) else I(o); return I(self.a + o.a, self.b + o.b)
    __radd__ = __add__
    def __neg__(self): return I(-self.b, -self.a)
    def __sub__(self, o): return self + (-o if isinstance(o, I) else I(-o))
    def __rsub__(self, o): return I(o) + (-self)
    def __mul__(self, o):
        o = o if isinstance(o, I) else I(o)
        p = [self.a*o.a, self.a*o.b, self.b*o.a, self.b*o.b]
        return I(min(p), max(p))
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = o if isinstance(o, I) else I(o)
        assert o.a > 0
        return self * I(1/o.b, 1/o.a)


@lru_cache(None)
def root_lower(g):
    """A lower enclosure of c(g), the smaller root of 27y^2-(20-4g)y+(g-1)^2.
    On [0, 1/9] the polynomial is positive below the root and not positive above it
    (at g = 2 the root is exactly 1/9), so bisection keeps lo <= c(g)."""
    lo, hi = F(0), F(1, 9)
    for _ in range(48):
        m = (lo + hi)/2
        if 27*m*m - (20 - 4*g)*m + (g - 1)**2 > 0:
            lo = m
        else:
            hi = m
    return lo


def bound(box):
    gl, gh, cl, ch, sl, sh = box
    cl = max(cl, root_lower(gl))                 # c increasing in gamma
    ch = min(ch, F(4, 5)*(X_T - sl/4))           # x >= 5c/4 + sigma/4
    sh = min(sh, 4*(X_T - F(5, 4)*cl))
    if cl > ch or sl > sh:
        return None, None
    g = I(gl, gh); c = I(cl, ch); sig = I(sl, sh)
    v = (3 - g - 3*c)/2; t = (g - 1 + c)/2; N = 3 - g - sig
    assert v.a > 0 and N.a > 0
    K = 7 - 3*g - 15*c - 6*sig; d = 2 - g
    s_upper = t.b
    if v.a > d.b:
        s_upper = min(s_upper, ((d*t + (v - d)*(t + c)/2)/v).b)
    q_lower = N.a/2 - 3*c.b - s_upper
    w = min(v.a/16, v.a/(2 + 9*v.b + 9*N.b)*max(F(0), q_lower - max(F(0), -K.a)))
    rain = max(F(0), K.a)*v.a/(2*(v.b + 3*N.b))
    return F(5, 4)*(c.a + max(w, rain)) + sig.a/4, (gl, gh, cl, ch, sl, sh)


def main():
    if not __debug__:
        raise RuntimeError("run without -O: the assertions are part of the check")
    stack = [(F(1), F(2), F(0), F(4, 5)*X_T, F(0), 4*X_T)]
    leaves = empty = splits = 0; start = time.time()
    while stack:
        low, box = bound(stack.pop())
        if box is None:
            empty += 1; continue
        if low >= X_T:
            leaves += 1; continue
        score = [box[1] - box[0], 15*(box[3] - box[2]), 6*(box[5] - box[4])]
        j = 2*max(range(3), key=lambda k: score[k]); m = (box[j] + box[j + 1])/2
        a = list(box); b = list(box); a[j + 1] = m; b[j] = m
        stack += [tuple(a), tuple(b)]; splits += 1
        if splits > LIMIT:
            print("FAIL: split limit reached, no certificate for %s" % X_T); return 1
    print("PASS: x >= %s = %.7f on the whole domain; %d rational leaves, %d empty, %d splits, %.0fs"
          % (X_T, float(X_T), leaves, empty, splits, time.time() - start))
    return 0


if __name__ == "__main__":
    sys.exit(main())
