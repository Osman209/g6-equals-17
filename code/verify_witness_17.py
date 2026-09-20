"""COVERS [P4] — the seventeen-card witness: pairs, five-subsets, degrees, deletions."""
#!/usr/bin/env python3
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "witness_17.json"

obj = json.loads(DATA.read_text())
cards = [set(card) for card in obj["cards"]]
symbols = sorted(set().union(*cards))

assert len(cards) == 17
assert len({tuple(sorted(card)) for card in cards}) == 17
assert all(len(card) == 6 for card in cards)
assert symbols == list(range(1, 28))

pairs = list(combinations(range(17), 2))
bad_pairs = [(i + 1, j + 1) for i, j in pairs if not (cards[i] & cards[j])]
assert not bad_pairs, bad_pairs
assert len(pairs) == 136

def is_cover(T, family):
    return all(card & T for card in family)

five_cover = None
checked = 0
for comb in combinations(symbols, 5):
    checked += 1
    if is_cover(set(comb), cards):
        five_cover = comb
        break

assert checked == math.comb(27, 5)
assert five_cover is None

deg = Counter()
for card in cards:
    deg.update(card)
hist = Counter(deg.values())
assert hist == Counter({4: 19, 3: 4, 5: 2, 2: 2}), hist

# Any card is a 6-transversal because the family is pairwise intersecting.
assert is_cover(cards[0], cards)

# Inclusion-minimality: validate the recorded 5-cover after deleting each card.
deletion = obj["deletion_five_covers"]
for i in range(17):
    T = set(deletion[str(i + 1)])
    assert len(T) == 5
    rest = cards[:i] + cards[i + 1:]
    assert is_cover(T, rest), (i + 1, sorted(T))

print("cards:", len(cards))
print("symbols:", len(symbols))
print("pair intersections:", len(pairs), "/", len(pairs))
print("five-subsets checked:", checked)
print("five-covers found:", 0)
print("degree histogram:", dict(sorted(hist.items())))
print("deletion checks:", 17, "/ 17")
print("PASS: 17-card witness has tau = 6")
