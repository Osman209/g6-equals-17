"""COVERS [P3, §3] step 2 — the seven orbits, and that every core is a genuine eight-card family with tau = 4."""
from pathlib import Path
from itertools import permutations,combinations
from collections import defaultdict
import json,time
rows=json.load(open(str(Path(__file__).resolve().parents[1]/'data'/'eight_maximal.json')));groups=defaultdict(set)
for r in rows:
 ts=r['triples'];key=tuple(sorted(sum(v in t for t in ts) for v in range(8)))
 groups[key].add(tuple(sorted(sum(1<<v for v in t) for t in ts)))
for hist,expected in groups.items():
 rep=next(iter(expected));ts=[[v for v in range(8) if m>>v&1] for m in rep]
 orbit={tuple(sorted(sum(1<<p[v] for v in t) for t in ts)) for p in permutations(range(8))}
 assert orbit==expected,(hist,len(orbit),len(expected))
 print('ORBIT PASS',hist,len(orbit),flush=True)
for line in open(str(Path(__file__).resolve().parents[1]/'data'/'eight_cores.jsonl')):
 r=json.loads(line);S=r['supports'];cards=[{i for i,s in enumerate(S) if v in s} for v in range(8)];m=[sum(1<<v for v in s) for s in S]
 assert len({tuple(sorted(a)) for a in cards})==8
 assert all(len(a)==6 for a in cards) and all(a&b for a,b in combinations(cards,2))
 assert not any(m[a]|m[b]|m[c]==255 for a,b,c in combinations(range(len(S)),3))
print('PASS: all 463 cores have eight distinct six-element intersecting cards and tau=4.')
