#!/usr/bin/env python3
"""Checks the algebra of Theorem 4 of [P5] ((5.2) and §6).

COVERS [P5, §5 and §6]: the budget identity of Lemma 19 and its normalised form; the
identity K = 2(N - 2M); the bound v/N >= 3/8 and theta <= 4/15; the second term of
Lemma 21 at theta = K/(20v); the reduction of both cases to (15 lambda + 7 - 3 gamma)/24;
the root argument for u <= L; convexity of c; c'(gamma_*) = 1/5, c(gamma_*), sigma_*,
and the constant 3 + x_*; a grid check of the minimum.   Needs sympy.
"""
import sympy as sp, math

# --- Lemma 19: the exact budget, before normalising -------------------------------
r, u, t, k0, G, Nc = sp.symbols('r u t k0 G N_c', real=True)
l = r - u + 1 - t                       # ell
q = 3*t + u
h = t + l
Nc_id = 3*r - 3 - q + G - 4*k0         # clean cards, from (6.1)
lhs = -Nc_id + 6*l + 2*(u - 1) + h/2    # after D <= u h / 4
assert sp.simplify(lhs - (3*l + 4 + 4*k0 - G + h/2)) == 0

# --- normalised quantities ---------------------------------------------------------
g, lam, sig, K = sp.symbols('gamma lambda sigma K', real=True)
v = (3 - g - 3*lam)/2
tr = (g - 1 + lam)/2
hr = tr + lam
# u + t + ell = r + 1 and q = 3t + u, in the limit:
assert sp.simplify(v + tr + lam - 1) == 0 and sp.simplify(3*tr + v - g) == 0
N = 3 - g - sig
M = sig + 3*lam + hr/2
assert sp.simplify(M - (sig + (g - 1 + 15*lam)/4)) == 0
Kexpr = 2*(N - 2*M)
assert sp.simplify(Kexpr - (7 - 3*g - 15*lam - 6*sig)) == 0

# --- the second term of Lemma 21 at theta = K/(20v), with 2M = N - K/2 --------------
Ns, vs = sp.symbols('N v', positive=True)
th = K/(20*vs)
second = Ns - (Ns - K/2)/(1 - 2*th)
assert sp.simplify(second - K*(sp.Rational(1, 2) - Ns/(10*vs))/(1 - K/(10*vs))) == 0
assert sp.simplify(sp.Rational(2, 3)*th*vs - K/30) == 0
assert sp.Rational(1, 2) - sp.Rational(8, 3)/10 == sp.Rational(7, 30)
# v/N >= 3/8 when lambda <= 1/12, gamma <= 2, sigma >= 0; then theta <= 2N/(20v) <= 4/15
from fractions import Fraction as Fr
assert Fr(1, 2) - Fr(3, 2)*Fr(1, 12) == Fr(3, 8)
assert Fr(2, 20)/Fr(3, 8) == Fr(4, 15) < Fr(1, 2)

# --- both cases give (15 lambda + 7 - 3 gamma)/24 ----------------------------------
target = (15*lam + 7 - 3*g)/24
caseA = sp.Rational(5, 4)*(lam + Kexpr/30) + sig/4               # K > 0
assert sp.simplify(caseA - target) == 0
caseB = sp.Rational(5, 4)*lam + ((7 - 3*g - 15*lam)/6)/4       # K <= 0, sigma at its floor
assert sp.simplify(caseB - target) == 0

# --- c(gamma) of (5.2) ----------------------------------------------------------------
a = sp.symbols('a', real=True)
c = lambda G_: (20 - 4*G_ - sp.sqrt((20 - 4*G_)**2 - 108*(G_ - 1)**2))/54
P = lambda y: 27*y**2 - (16 - 4*a)*y + a**2
assert sp.simplify(P(a/3) - sp.Rational(16, 3)*a*(a - 1)) == 0
assert sp.simplify(sp.expand(P(c(1 + a)))) == 0
# convexity: the square root is the geometric mean of two affine functions, both
# positive on [1, 2]
p = 20 - 4*g
assert sp.expand((p - sp.sqrt(108)*(g - 1))*(p + sp.sqrt(108)*(g - 1))
                 - ((20 - 4*g)**2 - 108*(g - 1)**2)) == 0
for G_ in (1, 2):
    assert float(20 - 4*G_ - math.sqrt(108)*(G_ - 1)) > 0

# --- the minimum --------------------------------------------------------------------
gs = (21 + 74*sp.sqrt(2))/69
cs = (24 - 14*sp.sqrt(2))/69
xs = (65 - 36*sp.sqrt(2))/138
ss = (10 - 2*sp.sqrt(2))/69
assert abs(sp.N(c(gs) - cs, 40)) < 1e-35
cp = sp.diff(c(g), g)
assert abs(sp.N(cp.subs(g, gs) - sp.Rational(1, 5), 40)) < 1e-35
assert sp.simplify((15*cs + 7 - 3*gs)/24 - xs) == 0
assert sp.simplify((7 - 3*gs - 15*cs)/6 - ss) == 0
assert sp.N(cp.subs(g, 1)) < sp.Rational(1, 5) < sp.N(cp.subs(g, 2))
assert 1 < float(gs) < 2
# gamma < 1: lambda >= 1 - gamma gives (22 - 18 gamma)/24 >= 1/6 > x_*
assert sp.simplify(target.subs(lam, 1 - g) - (22 - 18*g)/24) == 0
assert float(xs) < 1/6
# the range used in the proof: lambda <= z <= 4x/5 < 4x_*/5 < 1/12
assert 0.8*float(xs) < 1/12

# grid check of f(gamma) = (15 c(gamma) + 7 - 3 gamma)/24 on [1, 2]
cn = lambda G_: (20 - 4*G_ - math.sqrt((20 - 4*G_)**2 - 108*(G_ - 1)**2))/54
f = lambda G_: (15*cn(G_) + 7 - 3*G_)/24
assert min(f(1 + i/100000) for i in range(100001)) >= float(xs) - 1e-12

print("PASS: gamma_* = %.10f, c_* = %.10f, sigma_* = %.10f" % (float(gs), float(cs), float(ss)))
print("PASS: closed form checks; constant 3 + x_* = %.12f" % float(3 + xs))
