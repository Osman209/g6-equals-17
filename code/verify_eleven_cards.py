"""COVERS [P2, §2] branch C — 5,373 triangle-decomposition instances, all UNSAT."""
from itertools import combinations
from functools import lru_cache
import time,json
from pathlib import Path
P=list(combinations(range(11),2)); PI={p:i for i,p in enumerate(P)}
T=list(combinations(range(11),3));TM=[sum(1<<v for v in t) for t in T]
TP=[[PI[p] for p in combinations(t,2)] for t in T]
TH=[sum(1<<i for i,x in enumerate(TP) if p in x) for p in range(55)]
ALL=(1<<165)-1
@lru_cache(None)
def ban(mask):return sum(1<<i for i,m in enumerate(TM) if not m&mask)
def parts(n,low):
 if n==0:yield ();return
 for j in range(low,n+1):
  for p in parts(n-j,j):yield (j,)+p
def comp(n,k):
 if k==0:
  if n==0:yield ()
  return
 for j in range(n+1):
  for rest in comp(n-j,k-1):yield (j,)+rest
def match(C):
 if not C:yield ();return
 for j in range(1,len(C)):
  for rest in match(C[1:j]+C[j+1:]):yield ((C[0],C[j]),)+rest
def edges(paths,lengths,cycles,start):
 out=[];v=start
 for (x,y),k in zip(paths,lengths):
  seq=[x]+list(range(v,v+k))+[y];v+=k
  out+=list(zip(seq,seq[1:]))
 for k in cycles:
  seq=list(range(v,v+k));v+=k
  out+=list(zip(seq,seq[1:]+seq[:1]))
 return out

def instances(a,b,c,d):
 C=list(range(c)); fixed=tuple(zip(C[::2],C[1::2]));k=c//2
 for u in range(a+1):
  for lens in comp(u,k):
   if tuple(sorted(lens))!=lens:continue
   for cyc in parts(a-u,3):
    F=edges(fixed,lens,cyc,c)
    for pairing in match(C):
     for v in range(d+1):
      for elens in comp(v,k):
       for ecyc in parts(d-v,2):
        E=edges(pairing,elens,ecyc,c+a+b)
        rem=[1]*55
        for x,y in F:rem[PI[tuple(sorted((x,y)))]]-=1
        for x,y in E:rem[PI[tuple(sorted((x,y)))]]+=1
        yield rem,{'F':F,'E':E}

def solve(rem,limit=None):
 rem=rem[:];av=ALL
 for p,r in enumerate(rem):
  if not r:av&=~TH[p]
 nodes=0;t0=time.monotonic();chosen=[]
 def dfs(av,left):
  nonlocal nodes
  nodes+=1
  if limit is not None and nodes%10000==0 and time.monotonic()-t0>limit:raise TimeoutError
  if not left:return chosen[:]
  best=166;opts=0
  for p,r in enumerate(rem):
   if r:
    cand=av&TH[p];n=cand.bit_count()
    if not n:return None
    if n<best:best=n;opts=cand
    if n==1:break
  while opts:
   bit=opts&-opts;opts-=bit;i=bit.bit_length()-1;nxt=av
   for p in TP[i]:
    rem[p]-=1
    if not rem[p]:nxt&=~TH[p]
   for j in chosen:
    if not TM[i]&TM[j]:nxt&=~ban(TM[i]|TM[j])
   chosen.append(i);ans=dfs(nxt,left-3);chosen.pop()
   for p in TP[i]:rem[p]+=1
   if ans is not None:return ans
  return None
 try:
  ans=dfs(av,sum(rem));status='UNSAT' if ans is None else 'SAT'
 except TimeoutError:status='TIMEOUT';ans=None
 return status,nodes,round(time.monotonic()-t0,3),ans

def main():
 total=0;t0=time.monotonic()
 with open(Path(__file__).resolve().parents[1]/'results'/'g11_results.jsonl','w') as f:
  for a in range(12):
   for b in range(12-a):
    for c in range(12-a-b):
     d=11-a-b-c
     if c%2 or (4*a+5*b+5*c+6*d)%3:continue
     profile=(a,b,c,d);stats={};cnt=0
     for rem,shape in instances(*profile):
      assert sum(rem)%3==0 and min(rem)>=0
      status,nodes,secs,ans=solve(rem)
      record=dict(profile=profile,shape=shape,status=status,nodes=nodes,seconds=secs,solution=ans)
      f.write(json.dumps(record)+'\n');f.flush()
      stats[status]=stats.get(status,0)+1;cnt+=1;total+=1
      if status!='UNSAT':raise RuntimeError(record)
     print(profile,cnt,stats,'elapsed',round(time.monotonic()-t0,1),flush=True)
 assert total==5373
 print('TOTAL',total,flush=True)
if __name__=='__main__':main()
