#!/usr/bin/env python3
"""Checks the algebra of Theorem 4 of [P5] ((5.2) and §6.5).

COVERS [P5, §5 and Theorem 4]: F equals the condition of Lemmas 18 and 20 at theta_0; dF/dz; F at z = lambda; gamma_* and c(gamma_*);
h(gamma) >= h(gamma_*) on [1, gamma_*]; c increasing; the value 3 + x_*.   Needs sympy.
"""
import sympy as sp, math
g,x,z,l=sp.symbols('gamma x z lambda',real=True)
v=(3-g-3*l)/2; t=(g-1+l)/2; m=3-g-4*x+5*z; th=3*(z-l)/(2*v)
cond=(m-(z-l))*(1-2*th)-(4*v+2*t+12*l-2*m)
F=4-2*g-12*x+14*z-6*l-3*(z-l)*(3-g-4*x+4*z+l)/v
assert sp.simplify(cond-F)==0
assert sp.simplify(sp.diff(F,z)-(8+(12*x-24*z)/v))==0
assert sp.simplify(F.subs(z,l)-(4-2*g-12*x+8*l))==0
c=lambda G:(20-4*G-sp.sqrt((20-4*G)**2-108*(G-1)**2))/54
gs=(69+2*sp.sqrt(3185))/101
assert sp.simplify(sp.expand(101*gs**2-138*gs-79))==0
assert abs(sp.N(c(gs)-(4-2*gs)/7,30))<1e-25
xs=5*(133-2*sp.sqrt(3185))/1414
assert abs(sp.N(sp.Rational(5,4)*c(gs)-xs,30))<1e-25
cn=lambda G:(20-4*G-math.sqrt((20-4*G)**2-108*(G-1)**2))/54
gsn=float(gs); h=lambda G:4-2*G+8*cn(G)
assert all(h(1+i*(gsn-1)/20000)>=h(gsn)-1e-12 for i in range(20001))
assert all(cn(1+i/2000)<cn(1+(i+1)/2000) for i in range(1999))
a=sp.symbols('a',real=True)
P=lambda y:27*y**2-(16-4*a)*y+a**2
assert sp.simplify(P(a/3)-sp.Rational(16,3)*a*(a-1))==0
assert sp.simplify(P(c(1+a)))==0
cp=lambda G:(4*cn(G)+2*(G-1))/(20-4*G-54*cn(G))
assert max(cp(1+i*(gsn-1)/20000) for i in range(20001))<915/4859<0.25
from fractions import Fraction as Fr
assert 8-24*Fr(57,1000)/Fr(514,1000)>0 and 3*Fr(57,1000)/(2*Fr(514,1000))<=Fr(171,1028)<Fr(1,2) and 0.8*float(xs)<0.057
print("PASS: closed form checks; constant 3 + x_* = %.12f" % float(3+xs))
