"""COVERS [P3, §3] step 3 — canonicalisation of the 39,768 triple systems into 129 classes."""
from pathlib import Path
from itertools import permutations,product
from collections import defaultdict,Counter
import json,time
rows=[json.loads(l) for l in open(str(Path(__file__).resolve().parents[1]/'data'/'eight_triples.jsonl'))]
summary=json.load(open(str(Path(__file__).resolve().parents[1]/'data'/'eight_triples_summary.json')));assert len(summary)==7 and all(r['status']=='COMPLETE' for r in summary)
classes={};cache={};t0=time.monotonic()
for num,r in enumerate(rows,1):
 ts=r['triples'];original=tuple(sorted(sum(1<<v for v in t) for t in ts))
 if original in cache:key=cache[original]
 else:
  deg=[sum(v in t for t in ts) for v in range(8)];groups=defaultdict(list)
  for v,d in enumerate(deg):groups[d].append(v)
  lists=[groups[d] for d in sorted(groups)];best=None
  for permgroups in product(*(list(permutations(vs)) for vs in lists)):
   order=sum((list(g) for g in permgroups),[]);p=[0]*8
   for new,old in enumerate(order):p[old]=new
   key=tuple(sorted(sum(1<<p[v] for v in t) for t in ts))
   if best is None or key<best:best=key
  key=best;cache[original]=key
 classes[key]=classes.get(key,0)+1
 if num%10000==0:print('COUNT',num,'CLASSES',len(classes),'SECONDS',round(time.monotonic()-t0,1),flush=True)
with open(str(Path(__file__).resolve().parents[1]/'data'/'eight_triple_classes.jsonl'),'w') as f:
 for key,mult in sorted(classes.items()):f.write(json.dumps(dict(triples=[[v for v in range(8) if m>>v&1] for m in key],multiplicity=mult))+'\n')
print('TOTAL',len(rows),'CLASSES',len(classes),'SECONDS',round(time.monotonic()-t0,1),flush=True)
