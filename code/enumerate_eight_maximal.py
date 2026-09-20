"""COVERS [P3, §3] step 1 — the 10,144 maximal intersecting triple systems on eight points."""
from pathlib import Path
from itertools import combinations
import json,time
T=list(combinations(range(8),3));M=[sum(1<<v for v in t) for t in T];N=len(T)
A=[sum(1<<j for j,m in enumerate(M) if i!=j and m&M[i]) for i in range(N)]
rows=[];t0=time.monotonic()
def dfs(R,P,X):
 if not P and not X:
  ids=[i for i in range(N) if R>>i&1];union=0;common=255
  for i in ids:union|=M[i];common&=M[i]
  if union==255:rows.append(dict(triples=[T[i] for i in ids],common=common))
  return
 ux=P|X;best=-1;u=0
 while ux:
  bit=ux&-ux;ux-=bit;i=bit.bit_length()-1;s=(P&A[i]).bit_count()
  if s>best:best=s;u=i
 cand=P&~A[u]
 while cand:
  bit=cand&-cand;cand-=bit;i=bit.bit_length()-1
  dfs(R|bit,P&A[i],X&A[i]);P-=bit;X|=bit
dfs(0,(1<<N)-1,0)
print('maximal families covering8',len(rows),'stars',sum(bool(r['common']) for r in rows),'seconds',round(time.monotonic()-t0,2),flush=True)
from collections import Counter
print('sizes',dict(Counter(len(r['triples']) for r in rows)),flush=True)
json.dump(rows,open(str(Path(__file__).resolve().parents[1]/'data'/'eight_maximal.json'),'w'))
