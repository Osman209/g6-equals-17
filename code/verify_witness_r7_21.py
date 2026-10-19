"""COVERS g(7) <= 21 — the twenty-one-card witness for r = 7, standard library only.

Checks on data/witness_r7_21.json: 21 distinct cards of size 7 on the symbols 1..35; all
210 pairs meet; none of the 1,623,160 six-element sets of symbols meets every card, by two
methods (all six-sets, and a branching search on an uncovered card); the degree histogram;
that the stated Z_7 map preserves the family; and minimality (deleting any card leaves a six-cover,
which is found and printed). It prints the cards, the degrees and those covers. Since any single card meets every card,
tau = 7 exactly. The generator is code/search_symmetric_family.py (needs python-sat); this
script needs nothing but Python. About half a minute.
"""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
obj = json.loads((ROOT / "data" / "witness_r7_21.json").read_text())
cards = [frozenset(c) for c in obj["cards"]]
symbols = sorted(set().union(*cards))

assert len(cards) == 21 and len(set(cards)) == 21, "not 21 distinct cards"
assert all(len(c) == 7 for c in cards), "a card is not of size 7"
assert symbols == list(range(1, 36)), "symbols are not 1..35"
pairs = list(combinations(range(21), 2))
assert len(pairs) == 210 and all(cards[i] & cards[j] for i, j in pairs), "two cards miss"

mask = {s: sum(1 << i for i, c in enumerate(cards) if s in c) for s in symbols}
full = (1 << 21) - 1

# method 1: every six-element set of symbols
checked = 0
for T in combinations(symbols, 6):
    checked += 1
    m = 0
    for s in T:
        m |= mask[s]
    assert m != full, "six-cover %s" % (T,)
assert checked == math.comb(35, 6) == 1623160

# method 2: branch on the first card not yet met
def cover(left, met):
    if met == full:
        return True
    if left == 0:
        return False
    i = ((full & ~met) & -(full & ~met)).bit_length() - 1
    return any(cover(left - 1, met | mask[s]) for s in cards[i])
assert not cover(6, 0), "six-cover found by branching"

deg = Counter(bin(mask[s]).count("1") for s in symbols)
assert dict(deg) == {6: 7, 4: 21, 3: 7}, deg

# the Z_7 symmetry stated in the data file
def g_sym(s):
    o, k = divmod(s - 1, 7)
    return 7 * o + (k + 1) % 7 + 1
for idx, c in enumerate(cards):
    o, k = divmod(idx, 7)
    assert frozenset(g_sym(s) for s in c) == cards[7 * o + (k + 1) % 7], "not Z_7-invariant"

# minimality: after deleting any one card, the other 20 have a six-cover (found here)
def find_cover(fam_masks, left, met, full_):
    if met == full_:
        return []
    if left == 0:
        return None
    rest = full_ & ~met
    i = (rest & -rest).bit_length() - 1
    for s in sorted(fam_masks):
        if fam_masks[s] >> i & 1:
            r = find_cover(fam_masks, left - 1, met | fam_masks[s], full_)
            if r is not None:
                return [s] + r
    return None
deletion = []
for i in range(21):
    keep = [j for j in range(21) if j != i]
    m2 = {s: sum(1 << a for a, j in enumerate(keep) if s in cards[j]) for s in symbols}
    T = find_cover(m2, 6, 0, (1 << 20) - 1)
    assert T is not None and len(T) <= 6, "deleting card %d leaves tau = 7" % (i + 1)
    deletion.append(T)

meet = Counter(len(cards[i] & cards[j]) for i, j in pairs)
orbits = [[7 * o + k + 1 for k in range(7)] for o in range(5)]
orbit_deg = [bin(mask[o[0]]).count("1") for o in orbits]

print("The 21 cards (card number: its 7 symbols)")
for i, c in enumerate(cards):
    print("  card %2d:" % (i + 1), " ".join("%2d" % s for s in sorted(c)))
print("Degree of each symbol (symbol: number of cards containing it)")
for o, d in zip(orbits, orbit_deg):
    print("  symbols %2d-%2d: degree %d each" % (o[0], o[-1], d))
print("cards:", len(cards), " symbols:", len(symbols))
print("pairs of cards that meet:", sum(meet.values()), "/", len(pairs))
print("size of the meeting of two cards:", ", ".join("%d in %d pairs" % (k, v) for k, v in sorted(meet.items())))
print("six-symbol sets checked:", checked, " six-covers found:", 0, "(two methods)")
print("degree histogram:", ", ".join("degree %d: %d symbols" % (k, v) for k, v in sorted(deg.items())))
print("Z_7 symmetry: 3 card orbits of 7, 5 symbol orbits of 7, family invariant")
print("minimality: deleting any one card leaves a six-cover of the other 20:")
for i, T in enumerate(deletion):
    print("  without card %2d:" % (i + 1), " ".join("%2d" % s for s in sorted(T)))
print("PASS: tau = 7 and every proper subfamily has tau <= 6, so g(7) <= 21")
