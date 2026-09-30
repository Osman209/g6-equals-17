#!/usr/bin/env python3
"""Certified lower bound for the minimisation of [P5, §6.6] (Theorem 5).

COVERS [P5, Theorem 5]: over 1 <= gamma <= 2, c(gamma) <= lambda <= 0.082,
0 <= sigma <= 0.41, the quantity
    x = (5/4)(lambda + delta) + sigma/4,   delta = max(delta_1, delta_2),
with delta_1 the rainbow bound of Lemma 21 at the optimal theta (K > 0) and
delta_2 the weak-trace bound of Lemma 22, is at least X_T.  Branch and bound with
outward-rounded interval arithmetic (math.nextafter after every operation).
Also reports the numerical minimum.   Standard library only.
"""
import math, sys, time
X_T = 0.1024745          # the constant certified: liminf g(r)/r >= 3 + X_T
up = lambda a: math.nextafter(a, math.inf)
dn = lambda a: math.nextafter(a, -math.inf)

class I:
    __slots__ = ("lo", "hi")
    def __init__(s, lo, hi=None):
        s.lo = lo; s.hi = lo if hi is None else hi
    def __add__(a, b):
        b = b if isinstance(b, I) else I(b); return I(dn(a.lo + b.lo), up(a.hi + b.hi))
    __radd__ = __add__
    def __sub__(a, b):
        b = b if isinstance(b, I) else I(b); return I(dn(a.lo - b.hi), up(a.hi - b.lo))
    def __rsub__(a, b): return I(b) - a
    def __mul__(a, b):
        b = b if isinstance(b, I) else I(b)
        p = [a.lo*b.lo, a.lo*b.hi, a.hi*b.lo, a.hi*b.hi]
        return I(dn(min(p)), up(max(p)))
    __rmul__ = __mul__
    def __truediv__(a, b):
        b = b if isinstance(b, I) else I(b)
        assert b.lo > 0, "division by an interval that may be non-positive"
        p = [a.lo/b.lo, a.lo/b.hi, a.hi/b.lo, a.hi/b.hi]
        return I(dn(min(p)), up(max(p)))
    def __rtruediv__(a, b): return I(b) / a
    def sqrt(a):
        return I(dn(math.sqrt(max(a.lo, 0.0))), up(math.sqrt(max(a.hi, 0.0))))
def imax(a, b): return I(max(a.lo, b.lo), max(a.hi, b.hi))
def imin(a, b): return I(min(a.lo, b.lo), min(a.hi, b.hi))

def c_of(g):   # c(gamma) of (5.2), increasing; interval in, interval out (monotone ends)
    def cf(x):
        return (20 - 4*x - math.sqrt((20 - 4*x)**2 - 108*(x - 1)**2))/54
    return I(dn(dn(cf(g.lo)) - 1e-15), up(up(cf(g.hi)) + 1e-15))

def lower_x(g, l, s):
    v = (3 - g - 3*l)/2
    N = 3 - g - s
    t = (g - 1 + l)/2
    K = 7 - 3*g - 15*l - 6*s
    # upper bound on sbar
    d = 2 - g
    if v.lo > d.hi:
        sb = imin(t, (d*t + (v - d)*(t + l)/2)/v)
    else:
        sb = t
    Q = N/2 - 3*l - sb            # lower end uses the upper end of sbar
    # delta_1
    d1 = 0.0
    if K.lo > 0:
        A = v + 3*N
        disc = A*A - 6*v*K
        if disc.lo > 0:
            R = (6*v*K) / (6*(A + disc.sqrt()))   # = (A - sqrt(disc))/6
            th = (3*R) / (2*v)
            if th.hi < 0.5:
                d1 = max(d1, R.lo)
        d1 = max(d1, (K/30).lo)
    # delta_2
    Km = I(max(0.0, -K.hi), max(0.0, -K.lo))
    W = (v*(Q - Km)) / (2 + 9*v + 9*N)
    d2 = min((v/16).lo, max(0.0, W.lo))
    x = 1.25*(l + max(d1, d2)) + s/4
    return x.lo

def run():
    t0 = time.time()
    stack = [(1.0, 2.0, 0.0, 0.082, 0.0, 0.41)]
    boxes = 0; maxdepth = 0
    while stack:
        g0, g1, l0, l1, s0, s1 = stack.pop()
        boxes += 1
        if boxes > 30_000_000:
            print("FAIL: box budget exhausted"); return False
        g = I(g0, g1)
        cl = c_of(g)
        if l1 < cl.lo:            # below the stability curve: infeasible
            continue
        l0e = max(l0, cl.lo)
        lb = lower_x(g, I(l0e, l1), I(s0, s1))
        if lb >= X_T:
            continue
        w = [(g1 - g0), (l1 - l0)*10, (s1 - s0)*4]
        if max(w) < 1e-13:
            print("FAIL: cannot separate near gamma=%.12f lambda=%.12f sigma=%.12f, bound %.15f"
                  % (g0, l0, s0, lb)); return False
        k = w.index(max(w))
        if k == 0:
            m = (g0 + g1)/2; stack += [(g0, m, l0, l1, s0, s1), (m, g1, l0, l1, s0, s1)]
        elif k == 1:
            m = (l0 + l1)/2; stack += [(g0, g1, l0, m, s0, s1), (g0, g1, m, l1, s0, s1)]
        else:
            m = (s0 + s1)/2; stack += [(g0, g1, l0, l1, s0, m), (g0, g1, l0, l1, m, s1)]
    print("PASS: x >= %.7f on the whole domain, %d boxes, %.0fs" % (X_T, boxes, time.time() - t0))
    return True

if __name__ == "__main__":
    ok = run()
    sys.exit(0 if ok else 1)
