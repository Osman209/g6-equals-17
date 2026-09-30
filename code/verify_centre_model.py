#!/usr/bin/env python3
"""Checks of the centre model behind the coefficient route (to be written into [P5]).

COVERS three statements of the centre model; the proofs are in the text, these are checks:
  (a) the inclusion-exclusion formula for the reward, against direct enumeration, and the two
      fixed-bulk LP optima (1-2mu)(1-e^{-(1-2mu)})^2 and (sigma/2)(1-e^{-sigma/2})(1-e^{-(1-rho)/2})
      with their dual certificates (245 LPs; needs numpy and scipy);
  (b) the splitting lemma: overlap classes never lower the four-card reward in the Poisson
      limit (random overlap configurations);
  (c) the absorption step: pair-type Poisson hits of small centres, replaced by bulk with the
      same coverage, never raise the reward (random configurations with 0 to 3 large centres).
(b) and (c) are random tests of statements proved in the text, not proofs.

    python3 code/verify_centre_model.py        # about a minute
"""
import sys, itertools, random, math
from math import exp
if sys.flags.optimize:
    raise SystemExit('Run without -O.')
import numpy as np
from scipy.optimize import linprog

MASKS = [s for s in range(16) if bin(s).count('1') <= 2]
def rew(m): return max(bin(m).count('1') - 2, 0) / 2
def bulk_p(lam): return [np.prod([1 - exp(-lam[i]) if b >> i & 1 else exp(-lam[i]) for i in range(4)]) for b in range(16)]
def coeff(lam):
    bp = bulk_p(lam); return np.array([sum(bp[b] * rew(s | b) for b in range(16)) for s in MASKS])
def reward(lam, eta, centres):
    def Q(A):
        v = math.exp(-sum(lam[i] for i in range(4) if A >> i & 1) - sum(e for S, e in eta.items() if S & A))
        for c in centres: v *= sum(p for S, p in c.items() if not S & A)
        return v
    return 1 - .5 * sum(Q(1 << i) for i in range(4)) + .5 * sum(Q(s) for s in range(16) if bin(s).count('1') == 3) - Q(15)

rng = random.Random(20260930)
# (a) identity
worst = 0
for trial in range(100):
    K = 1 + trial % 4
    probs = []
    for _ in range(K):
        v = [rng.random() for _ in MASKS]; t = sum(v); probs.append({s: x / t for s, x in zip(MASKS, v)})
    lam = [rng.random() / 2 for _ in range(4)]
    dist = [0.0] * 16; dist[0] = 1.0
    for p in probs:
        nxt = [0.0] * 16
        for a in range(16):
            for s, x in p.items(): nxt[a | s] += dist[a] * x
        dist = nxt
    bp = bulk_p(lam)
    direct = sum(dist[a] * bp[b] * rew(a | b) for a in range(16) for b in range(16))
    worst = max(worst, abs(direct - reward(lam, {}, probs)))
assert worst < 1e-12
print('ok  (a) inclusion-exclusion formula: 100 cases, max error %.1e' % worst)
# (a) fixed-bulk LPs
A = np.array([[int(s >> i & 1) for s in MASKS] for i in range(4)] + [[int(bin(s).count('1') == 2) for s in MASKS]])
EQ = np.array([[1] * len(MASKS), [bin(s).count('1') for s in MASKS]])
n = 0; gap = 0
for rho in (.3, .49, .6, .7, .9):
    for mu in np.linspace(.25, .49, 49):
        if mu <= (1 + rho) / 4:
            v = 1 - 2 * mu; lam = [v, v, 0, 0]; cand = v * (1 - exp(-v)) ** 2
        else:
            sg = 2 - 4 * mu; lam = [sg / 2, (1 - rho) / 2, 0, 0]; cand = .5 * sg * (1 - exp(-sg / 2)) * (1 - exp(-(1 - rho) / 2))
        c = coeff(lam)
        res = linprog(c, A_ub=A, b_ub=[1 - 2 * x for x in lam] + [rho], A_eq=EQ, b_eq=[1, 4 * (1 - mu) - 2 * sum(lam)], bounds=(0, None), method='highs')
        assert res.success
        w = (1 - exp(-lam[0])) * (1 - exp(-lam[1])) / 2
        assert min(c - np.array([w * sum(s >> i & 1 for i in (2, 3)) for s in MASKS])) > -1e-12
        assert abs(cand - res.fun) < 1e-10
        n += 1; gap = max(gap, abs(cand - res.fun))
print('ok  (a) fixed-bulk LP optima and dual certificates: %d LPs, max gap %.1e' % (n, gap))

# (b) splitting lemma, four cards, Poisson limit
subsets = [S for k in range(1, 5) for S in itertools.combinations(range(4), k)]
def R4(alpha):
    def avoid(T): return math.exp(-sum(m for S, m in alpha.items() if set(S) & set(T)))
    def allhit(H): return sum((-1) ** len(K) * avoid(K) for k in range(len(H) + 1) for K in itertools.combinations(H, k))
    a4 = allhit((0, 1, 2, 3)); a3 = sum(allhit(H) for H in itertools.combinations(range(4), 3)) - 4 * a4
    return a4 + a3 / 2
worst = 9
for _ in range(50000):
    a = [rng.choice([.5, rng.uniform(.05, .5)]) for _ in range(4)]
    al = {S: 0.0 for S in subsets}; rem = a[:]
    for S in rng.sample([S for S in subsets if len(S) > 1], rng.randint(1, 6)):
        m = rng.random() * min(rem[i] for i in S)
        for i in S: rem[i] -= m
        al[S] += m
    for i in range(4): al[(i,)] = rem[i]
    base = R4({**{S: 0.0 for S in subsets}, **{(i,): a[i] for i in range(4)}})
    worst = min(worst, R4(al) - base)
assert worst > -1e-12
print('ok  (b) splitting: 50,000 overlap configurations, min(overlap - split) = %.1e' % worst)

# (c) absorption of small-centre Poisson hits into bulk
SUB = [s for s in range(16) if 0 < bin(s).count('1') <= 2]
worst = 9
for _ in range(50000):
    centres = []
    for _ in range(rng.randint(0, 3)):
        w = {S: rng.random() ** 3 for S in [0] + SUB}; t = sum(w.values()); centres.append({S: v / t for S, v in w.items()})
    lam = [rng.random() * .4 for _ in range(4)]
    eta = {S: (rng.random() * .3 if rng.random() < .5 else 0) for S in SUB}
    lam2 = lam[:]
    for S, e in eta.items():
        for i in range(4):
            if S >> i & 1: lam2[i] += e / 2
    worst = min(worst, reward(lam, eta, centres) - reward(lam2, {}, centres))
assert worst > -1e-12
print('ok  (c) absorption: 50,000 configurations, min(with pair hits - absorbed) = %.1e' % worst)
print('PASS')
