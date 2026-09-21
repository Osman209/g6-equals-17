"""COVERS [P3, §3] step 4 — 772 raw completions reduced to the 463 canonical cores."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import defaultdict
import argparse,json,time
_ap=argparse.ArgumentParser();_ap.add_argument('--out',default=None,help='write the cores here instead of over data/eight_cores.jsonl')
_out=_ap.parse_args().out
rows=[json.loads(l) for l in open(str(Path(__file__).resolve().parents[1]/'data'/'eight_triple_classes.jsonl'))];classes={};raw=0;t0=time.monotonic()
for ri,row in enumerate(rows):
 T=[tuple(t) for t in row['triples']];degree=[sum(v in t for t in T) for v in range(8)]
 covered={tuple(sorted(p)) for t in T for p in combinations(t,2)}
 F=[p for p in combinations(range(8),2) if p not in covered]
 slack=[6-degree[v]-sum(v in p for p in F) for v in range(8)]
 assert min(slack)>=0
 positive=[v for v in range(8) if slack[v]];pairs=list(combinations(positive,2));chosen=[]
 groups=defaultdict(list)
 for v,d in enumerate(degree):groups[d].append(v)
 maps=[]
 for pieces in product(*(list(permutations(groups[d])) for d in sorted(groups))):
  order=sum((list(p) for p in pieces),[]);mp=[0]*8
  for new,old in enumerate(order):mp[old]=new
  maps.append(mp)
 def dfs(k):
  global raw
  if k==len(pairs):
   S=T+F+chosen+[(v,) for v,s in enumerate(slack) for _ in range(s)]
   cards=[tuple(i for i,s in enumerate(S) if v in s) for v in range(8)]
   if len(set(cards))!=8:return
   assert all(len(c)==6 for c in cards)
   raw+=1;best=None
   for p in maps:
    key=tuple(sorted(sum(1<<p[v] for v in s) for s in S))
    if best is None or key<best:best=key
   classes[best]=classes.get(best,0)+1;return
  a,b=pairs[k];cap=min(slack[a],slack[b]);dfs(k+1)
  for j in range(cap):
   chosen.append((a,b));slack[a]-=1;slack[b]-=1;dfs(k+1)
  for j in range(cap):chosen.pop();slack[a]+=1;slack[b]+=1
 dfs(0)
with open(_out or str(Path(__file__).resolve().parents[1]/'data'/'eight_cores.jsonl'),'w') as f:
 for key,mult in sorted(classes.items()):
  S=[[v for v in range(8) if mask>>v&1] for mask in key]
  f.write(json.dumps(dict(supports=S,multiplicity=mult))+'\n')
print('RAW',raw,'CORES',len(classes),'SECONDS',round(time.monotonic()-t0,2),flush=True)
