"""Checks the numbers used in the hand proofs of [P1].

COVERS [P1, §3, Case 1]: the matching counts h and their sums s = 57 (K_{1,3}+K_{1,2})
and s = 63 (K_{1,4}+K_2), and the bound 4 x 57 = 228 > 210.
COVERS [P1, §6]: the deficit identity f(2+e) = 6 + 18.5 e - delta(e), the bound B(t),
and the thirteen histograms obtained from the middle-card rule (compared with
code/verify_histograms.py).

Standard library only. Exits non-zero if any check fails.
"""
import itertools
import sys
from fractions import Fraction as F

from verify_histograms import EXPECTED

fails = []


def check(cond, name):
    if not cond:
        fails.append(name)


# ---- §3, Case 1: perfect matchings of the six points other than x ----------------
V = range(7)


def pms(W):
    if not W:
        yield []
        return
    a = W[0]
    for b in W[1:]:
        for rest in pms([w for w in W if w not in (a, b)]):
            yield [frozenset((a, b))] + rest


def h(T, x):
    return sum(1 for M in pms([v for v in V if v != x]) if set(M) & T)


e = lambda a, b: frozenset((a, b))
S = {e(0, 1), e(0, 2), e(0, 3), e(4, 5), e(4, 6)}          # K_{1,3} + K_{1,2}
Fk = {e(0, 1), e(0, 2), e(0, 3), e(0, 4), e(5, 6)}         # K_{1,4} + K_2
check([h(S, x) for x in V] == [6, 8, 8, 8, 9, 9, 9], "h values of K13+K12")
check([h(Fk, x) for x in V] == [3, 9, 9, 9, 9, 12, 12], "h values of K14+K2")
check(sum(h(S, x) for x in V) == 57 and sum(h(Fk, x) for x in V) == 63, "sums 57, 63")
check(4 * 57 > 7 * 30, "228 > 210")

# ---- §6: deficits and the thirteen histograms -------------------------------------
f = {2: 6, 3: 18, 4: 33, 5: 54, 6: 80}
delta = {0: F(0), 1: F(13, 2), 2: F(10), 3: F(15, 2), 4: F(0)}
for ee in range(5):
    check(f[2 + ee] == 6 + F(37, 2) * ee - delta[ee], f"deficit identity e={ee}")


def B(t):
    return F(37, 2) * (4 * t - 30) - 3 * t * (t - 1) + 90


check(all(B(t) == -3 * t * t + 77 * t - 465 for t in range(40)), "B(t) closed form")
check([B(t) for t in range(10, 16)] == [5, 19, 27, 29, 25, 15], "B(10..15)")
check(all(B(t) < 0 for t in list(range(8, 10)) + list(range(16, 40))), "B < 0 outside")

rows = set()
for t in range(8, 40):
    s = 4 * t - 30
    for n2 in range(8):
        r = 90 - 4 * t - 2 * n2
        if r < 0 or r % 3:
            continue
        for k in range(0, 15):
            for mid in itertools.combinations_with_replacement((1, 2, 3), k):
                if k < 2 * n2 or sum(delta[x] for x in mid) > B(t) or (s - sum(mid)) % 4:
                    continue
                n6 = (s - sum(mid)) // 4
                n2c = 15 - k - n6
                if n6 < 0 or n2c < 0:
                    continue
                rows.add(((n2, r // 3, t), (n2c, mid.count(1), mid.count(2), mid.count(3), n6)))
check(rows == EXPECTED, "middle-card rule gives the thirteen histograms")

if fails:
    print("FAIL:", "; ".join(fails))
    sys.exit(1)
print("PASS: h sums 57 and 63; deficit rule reproduces the 13 histograms of verify_histograms.py")
