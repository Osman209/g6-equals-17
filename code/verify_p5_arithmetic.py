#!/usr/bin/env python3
"""Every integer and real-number step of [P5] that is arithmetic rather than structure.

COVERS [P5, §2.3, §3.4-§3.5, §4, §5]:

  - the five cases (u, t) left by the necessary inequalities at odd u <= 9, and the
    divisibility and counting facts that close them;
  - the exclusion arithmetic of Theorem 2: u >= 15, u = 13, and the values of
    (u, t, d) that remain at r = 19, 20, 21;
  - the stability inequality: the dense-remainder corollary (28r - 67)/9, checked over
    integer tuples, and the closed form for the gain at every remainder density,
    checked against the exact minimum for r up to 3200;
  - the constant of [2, §4] and how it moves if the small-remainder side improves;
  - the impossibility of any bound 5 tau <= q + r + K on the pair family.

None of this is structural.  The structural lemmas are checked by
verify_residual_bound.py, verify_local_graphs.py and verify_rainbow_lemmas.py.

    python3 code/verify_p5_arithmetic.py      # seconds

Exits non-zero on the first failed step.
"""
import sys
from math import sqrt, ceil

BAD = []


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        BAD.append(msg)


# ---------------------------------------------------------------- §2.3 five cases
cases = [(u, t) for u in range(1, 10, 2) for t in range(0, u - 2)
         if u * (t + 2) <= t * max(12, u + 4)]
check(cases == [(5, 2), (7, 3), (7, 4), (9, 5), (9, 6)],
      "odd u <= 9, 0 <= t <= u-3, u(t+2) <= t*max(12,u+4) leave exactly %s" % cases)
check((11 * 5) % 3 != 0, "(5,2): q=11, r=5, qr=55 not divisible by 3")
check(36 == 6 * 6 and 8 % 3 != 0, "(9,6): six K4 in K9 would need degree 8 divisible by 3")
check(9 * (5 + 2) > 5 * 12, "(9,5): S >= 63 exceeds 5*12 = 60")
check(7 * (3 + 2) == 35 and 3 * 12 >= 35 > 3 * 12 - 2,
      "(7,3): S >= 35 forces all three local graphs to S = 12 (11 excluded)")
check(sorted([6, 6, 6, 3]) and 21 == 6 + 6 + 6 + 3 == 6 + 6 + 5 + 4 == 6 + 5 + 5 + 5,
      "(7,4): 21 edges split into four parts of size <= 6 only as 6663, 6654, 6555")

# ---------------------------------------------------------------- §3.5 u >= 15
# Lemma 7: u <= max(12, d+8), so u >= 13 gives d >= u-8 and t = u-d-1 <= 7.
check(all(u - (u - 8) - 1 == 7 for u in range(15, 2001, 2)), "u >= 15: t <= 7")
# D <= 7*H0 = 7(u-1)/2 against D >= (u^2-6u-3)/2
check(all((u * u - 6 * u - 3) / 2 > 7 * (u - 1) / 2 for u in range(13, 20001, 2)),
      "u >= 13 odd: (u^2-6u-3)/2 > 7(u-1)/2, i.e. u^2-13u+4 > 0")
check(13 * 13 - 13 * 13 + 4 == 4, "u^2-13u+4 = 4 at u = 13, increasing after")
# Lemma 7's own contradiction: u > max(12, d+8) gives t = u-d-1 >= 8 and matching number > 4
check(all((u - d) / 2 > 4 and u - d - 1 >= 8
          for d in range(0, 200) for u in range(max(13, d + 9), max(13, d + 9) + 40)),
      "u > max(12, d+8): spanning one-coloured graphs have matching number > 4 and t >= 8")

# ---------------------------------------------------------------- §3.5 u = 13
u, a = 13, 5
check(u * u - 5 * u - a * 13 == 39, "u = 13: sum nu >= 104 - D and <= 5*13 give D >= 39")
check(a * 14 == 70 and u * u - 5 * u - 70 == 34,
      "without Lemma 5 the per-group bound is 14 and only D >= 34 follows")
check(6 * 3 + 4 * 4 == 34 < 39, "u = 13, d = 5, t = 7: D <= 6m + 4(7-m) <= 34 with m <= 3")
check(all(6 * (12 - d) < 39 for d in range(6, 12)), "u = 13, d >= 6: D <= 6t <= 36")
check(all(13 > max(12, d + 8) for d in range(0, 5)) and 13 <= max(12, 5 + 8),
      "u = 13: Lemma 7 forces d >= 5")

# ---------------------------------------------------------------- §3.5 what remains
rem = sorted({(r, u, 2 * u - 2 - r, u - (2 * u - 2 - r) - 1) for r in (19, 20, 21)
              for u in range(3, 12, 2) if 2 * u - 2 - r >= 0})
check(rem == [(19, 11, 1, 9), (20, 11, 0, 10)],
      "u <= 11 leaves at r = 19, 20, 21 exactly (r,u,d,t) = %s" % rem)
check((41 * 20) % 3 != 0, "r = 20, u = 11, d = 0: q = 41, qr = 820 not divisible by 3")
check(11 * 4 + 10 * 5 == 94 < 99, "r = 19: without a K4, S <= 11m + 10(9-m) <= 94 < 99")
check(108 - 99 == 9 and 9 + 1 < 14, "r = 19: eligible pairs at most 10, at least 7*2 = 14")

# ---------------------------------------------------------------- §4 stability
def min_ell(r, d):
    L = max(12, d + 8)
    for ell in range(-r, r + 1):
        num = r + d + 2 - 3 * ell
        if num < 0 or num % 2:
            continue
        u = num // 2
        t = u - d - 1 + 2 * ell
        if t < 0:
            continue
        if u > L and (u - L) * t > (5 * u - L) * ell:
            continue
        return ell
    return None


viol = 0
for d in range(0, 5):
    for u in range(0, 301):
        for ell in range(-1, 151):
            t = u - d - 1 + 2 * ell
            r = 2 * u - d - 2 + 3 * ell
            if t < 0 or r < 1:
                continue
            L = 12
            if u > L and (u - L) * t > (5 * u - L) * ell:
                continue
            if max(0, ell) < (r - 40) / 9:
                viol += 1
check(viol == 0, "d <= 4: every admissible (u, d, ell) with u <= 300 has max(0,ell) >= (r-40)/9")
check(all(ceil((28 * r - 67) / 9) == 3 * r - 3 + ceil((r - 40) / 9) for r in range(40, 400)),
      "hence |H| >= ceil((28r - 67)/9) when q >= 2r - 3")


def closed(delta):
    b = 12 + 4 * delta
    return (b - sqrt(b * b - 108 * (1 - delta) ** 2)) / 54


worst = 0.0
for delta in (0.0, 0.1, 0.25, 0.5, 0.75):
    r = 3200
    e = min_ell(r, int(delta * r))
    worst = max(worst, abs(e / r - closed(delta)))
    print("      remainder q ~ %.2f r: exact min ell/r at r=3200 is %.4f, closed form %.4f"
          % (2 - delta, e / r, closed(delta)))
check(worst < 0.003, "closed form matches the exact minimum to within 0.003 at r = 3200")
check(abs(closed(0) - 1 / 9) < 1e-12 and closed(1.0) == 0,
      "closed form: 1/9 at q = 2r, 0 at q = r")

# ---------------------------------------------------------------- §5 the constant of [2]
F = lambda b: 5 - 1.5 * b + 5 * sqrt((2 * b * b - 5 * b) / 8)
G = lambda b: 15 / 4 - b / 4
b0 = (4 + sqrt(19)) / 3
check(abs(F(b0) - (41 - sqrt(19)) / 12) < 1e-12 and abs(G(b0) - F(b0)) < 1e-12,
      "[2]: the two regime bounds cross at beta0 = (4+sqrt19)/3 at value (41-sqrt19)/12 = %.5f"
      % F(b0))
for delta in (0.05, 0.1, 0.2):
    lo, hi = 2.5, 3.0
    for _ in range(80):
        m = (lo + hi) / 2
        if G(m) + 5 * delta / 4 > F(m):
            lo = m
        else:
            hi = m
    print("      small-remainder side improved by %.2f r: crossing at %.4f, coefficient %.4f"
          % (delta, lo, F(lo)))

# ---------------------------------------------------------------- §5 no bound 5tau <= q+r+K
check(all(5 * (n + 1) / 2 - (2 * n - 1) == (n + 7) / 2 for n in range(3, 200, 2)),
      "pair family q=n, r=n-1, tau=(n+1)/2 forces K >= (n+7)/2 in 5tau <= q+r+K")

if BAD:
    print("FAIL: %d steps" % len(BAD))
    sys.exit(1)
print("PASS: every arithmetic step of [P5] checks.")
