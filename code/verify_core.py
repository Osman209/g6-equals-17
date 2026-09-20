"""COVERS [P2, §5] — an explicit twelve-card pairwise intersecting family with tau = 5, showing the eleven-card lemma is sharp at eleven."""
from itertools import combinations
import json
from pathlib import Path
T=[(0,2,4),(0,3,6),(0,5,8),(0,7,10),(0,9,11),(1,2,7),(2,6,8),(2,5,11),(2,9,10),(3,5,7),(4,7,9),(1,3,9),(5,6,9),(1,5,10),(4,6,10),(1,6,11),(1,4,8),(3,4,11),(3,8,10),(7,8,11)]
supports=T+[(i,i+1) for i in range(0,12,2)]
sm=[sum(1<<v for v in s) for s in supports]
cards=[{j for j,s in enumerate(supports) if v in s} for v in range(12)]
assert all(len(c)==6 for c in cards)
assert all(len(a&b)==1 for a,b in combinations(cards,2))
assert not any(sm[a]|sm[b]|sm[c]|sm[d]==4095 for a,b,c,d in combinations(range(26),4))
covers=[c for c in combinations(range(26),5) if sm[c[0]]|sm[c[1]]|sm[c[2]]|sm[c[3]]|sm[c[4]]==4095]
assert covers
cm=[sum(1<<s for s in c) for c in covers]
dis=[sum(not m&n for n in cm) for m in cm]
print('12 cards; all size 6; all pair intersections 1; tau=5')
print('5-cover count',len(covers),'maximum disjoint 5-covers',max(dis),'four times maximum',4*max(dis))
print('first 5-cover',covers[0]);print('cards',cards)
json.dump(dict(supports=supports,cards=[sorted(c) for c in cards],cover=covers[0],five_cover_count=len(covers),max_disjoint_five_covers=max(dis)),open(Path(__file__).with_name('twelve_witness.json'),'w'),indent=2)

# Independently certify a six-card extension (18 cards total), not a 16-card example.
new_covers=[(0,9,15,24,25),(1,8,19,20,22),(3,5,12,17,24),(3,6,11,22,25),(4,7,16,18,23),(6,10,13,17,20)]
assert all(c in covers for c in new_covers)
assert all(any(not set(t)&set(c) for c in new_covers) for t in covers)
full=cards+[set(c)|{26} for c in new_covers]
assert len({tuple(sorted(c)) for c in full})==18
assert all(len(a&b)>=1 for a,b in combinations(full,2))
fs=[sum(1<<j for j,card in enumerate(full) if v in card) for v in range(27)]
assert not any(fs[a]|fs[b]|fs[c]|fs[d]|fs[e]==(1<<18)-1 for a,b,c,d,e in combinations(range(27),5))
print('PASS: explicit 18-card extension has tau=6; no 16-card extension certified.')
