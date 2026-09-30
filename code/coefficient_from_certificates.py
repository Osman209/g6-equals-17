#!/usr/bin/env python3
"""The coefficient that the one-centre certificates give, in the one-centre model.

COVERS the number 3.0588 of the coefficient route (to be written into [P5]).  This is a
NUMERICAL evaluation on a grid, not a proof, and it holds only inside the one-centre model:
the multi-centre step and the passage from the matching problem to the model are open.

Inputs, all from the text or from verified certificates:
  - the stability gain c(gamma) = ell/r of [P5, §5], closed form, at q = gamma r;
  - the clean-tail inequality E >= (B + 4C)/4 - 1;
  - B + 4C >= ell + 4 * (savings), savings >= (clean groups) * Phi(mu);
  - Phi = lower convex envelope of the certified step function: on (mu_prev, mu_max] the
    certificate for mu_max applies (certificates/one_centre, verified by
    verify_one_center_certificates.py);
  - mu <= (t + 3 ell)/(n - q - 5E), from M0 <= S + 3 u ell and S <= t(u + 4), t/r = (gamma-1+c)/2.
It minimises n/r over gamma in [1, 2] (below q = r the term B >= r - q + 1 alone gives more) and E >= 0 by a fixed-point iteration on a grid.

    python3 code/coefficient_from_certificates.py          # seconds
"""
from math import sqrt
from fractions import Fraction as F

def closed(d):                     # [P5, §5] stability gain at q = (2 - d) r
    b = 12 + 4 * d
    return (b - sqrt(b * b - 108 * (1 - d) ** 2)) / 54

DELTA = (41 - sqrt(19)) / 12 - 3   # Sivashankar's constant minus 3
CERT = [('1/20', '39/500'), ('1/10', '67/1000'), ('3/20', '11/200'), ('1/5', '21/500'),
        ('1/4', '29/1000'), ('3/10', '3/125'), ('7/20', '19/1000'), ('3/8', '23/2000'),
        ('2/5', '31/5000'), ('17/40', '27/10000'), ('9/20', '1/1250')]

def hull(pts):
    pts = sorted(pts); H = []
    for p in pts:
        while len(H) >= 2 and (H[-1][1] - H[-2][1]) * (p[0] - H[-2][0]) >= (p[1] - H[-2][1]) * (H[-1][0] - H[-2][0]):
            H.pop()
        H.append(p)
    def f(x):
        if x <= H[0][0]: return H[0][1]
        for (a, fa), (b, fb) in zip(H, H[1:]):
            if a <= x <= b: return fa + (fb - fa) * (x - a) / (b - a)
        return 0.0
    return f

pts = [(0.0, float(F(CERT[0][1])))]; prev = 0.0
for m, v in CERT:
    pts.append((prev, float(F(v)))); prev = float(F(m))
pts += [(prev, 0.0), (1.0, 0.0)]
Phi = hull(pts)

def implied(g):
    c = closed(2 - g); t = (g - 1 + c) / 2; best = 9
    for j in range(301):
        e = j / 2000; n = 3.0; ok = True
        for _ in range(300):
            Nc = n - g - 5 * e
            if Nc <= 1e-9: ok = False; break
            G = c + Phi((t + 3 * c) / Nc) * Nc
            n = 3 + e + G
        if ok and e >= G / 4 - 1e-12: best = min(best, n)
    return best

res = min((implied(1 + i / 200), 1 + i / 200) for i in range(201))
print('target 3 + Delta = %.4f' % (3 + DELTA))
for g in (1.0, 1.3, 1.5, 1.6, 1.7, 1.72, 1.8, 1.9):
    print('  q = %.2f r: n/r >= %.4f' % (g, implied(g)))
print('RESULT minimum over q/r in [1, 2]: %.4f at q/r = %.3f (one-centre model, numerical)' % res)
assert res[0] > 3 + DELTA
