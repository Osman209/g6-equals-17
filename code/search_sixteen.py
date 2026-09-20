"""Exact SAT model for each eight-card core. Requires python-sat.
UNKNOWN is never an exclusion. Run with --budget 0 for unlimited conflicts.

COVERS [P3, §4] — the CNF encoding build() and the search over the 463 cores.
"""
from pathlib import Path
from itertools import combinations
import json,time,argparse
from pysat.solvers import Solver
from pysat.card import CardEnc,EncType
from pysat.formula import IDPool

def build(S,cover=True,symmetry=True):
 pool=IDPool();cnf=[];n=len(S);M=[sum(1<<v for v in s) for s in S]
 h=[[pool.id(('h',v,j)) for j in range(8)] for v in range(n)]
 Bs=[b for k in (2,3,4) for b in combinations(range(8),k) if any(j<4 for j in b) and any(j>=4 for j in b)]
 z=[pool.id(('b',i)) for i in range(len(Bs))]
 for v,s in enumerate(S):
  cnf+=CardEnc.atmost(h[v],4-len(s),vpool=pool,encoding=EncType.seqcounter).clauses
  if len(s)==1:cnf.append(h[v][:])
 for j in range(8):
  lits=[h[v][j] for v in range(n)]+[z[i] for i,b in enumerate(Bs) if j in b]
  cnf+=CardEnc.equals(lits,5,vpool=pool,encoding=EncType.seqcounter).clauses
  for a in range(8):cnf.append([h[v][j] for v,s in enumerate(S) if a in s])
 for j in range(4):
  for k in range(4,8):
   common=[]
   for v in range(n):
    w=pool.id(('pair',v,j,k));cnf.extend([[-w,h[v][j]],[-w,h[v][k]],[w,-h[v][j],-h[v][k]]]);common.append(w)
   cnf.append(common+[z[i] for i,b in enumerate(Bs) if j in b and k in b])
 for i,a in enumerate(Bs):
  for k,b in enumerate(Bs):
   if i<k and (set(a)<=set(b) or set(b)<=set(a)):cnf.append([-z[i],-z[k]])
 for i,b in enumerate(Bs):
  for v,s in enumerate(S):
   if len(b)<=4-len(s):cnf.append([-z[i]]+[-h[v][j] for j in b])
 for v,a in enumerate(S):
  for w,b in enumerate(S):
   if v==w or not set(a)<=set(b):continue
   witnesses=[]
   for j in range(8):
    q=pool.id(('notcontained',v,w,j));cnf.extend([[-q,h[v][j]],[-q,-h[w][j]]]);witnesses.append(q)
   cnf.append(witnesses)
 if symmetry:
  for a,b in [(0,1),(1,2),(2,3),(4,5),(5,6),(6,7),(0,4)]:
   eq=pool.id(('lex',a,b,0));cnf.append([eq])
   for v in range(n):
    x,y=h[v][a],h[v][b];nxt=pool.id(('lex',a,b,v+1))
    cnf.append([-eq,-x,y])
    cnf.extend([[-nxt,eq],[-nxt,-x,y],[-nxt,x,-y],[-eq,x,y,nxt],[-eq,-x,-y,nxt]])
    eq=nxt
 C4=[];C5=[]
 if cover:
  C4=[t for t in combinations(range(n),4) if M[t[0]]|M[t[1]]|M[t[2]]|M[t[3]]==255]
  C5=[t for t in combinations(range(n),5) if M[t[0]]|M[t[1]]|M[t[2]]|M[t[3]]|M[t[4]]==255]
  for t in C4:
   miss=[pool.id(('miss4',t,j)) for j in range(8)]
   for j,q in enumerate(miss):
    for v in t:cnf.append([-q,-h[v][j]])
   cnf.append(miss[:4]);cnf.append(miss[4:])
   for zi,b in zip(z,Bs):cnf.append([-zi]+[miss[j] for j in range(8) if j not in b])
  for t in C5:
   miss=[pool.id(('miss5',t,j)) for j in range(8)];cnf.append(miss)
   for j,q in enumerate(miss):
    for v in t:cnf.append([-q,-h[v][j]])
 return cnf,pool.top,(h,z,Bs),dict(symbols=n,covers4=len(C4),covers5=len(C5))

def audit(S,model,data,require_tau6):
 h,z,Bs=data;positive=set(x for x in model if x>0)
 support=[set(s)|{8+j for j in range(8) if h[v][j] in positive} for v,s in enumerate(S)]
 support += [{8+j for j in b} for zi,b in zip(z,Bs) if zi in positive]
 support += [set(range(8,12)),set(range(12,16))]
 cards=[{i for i,s in enumerate(support) if v in s} for v in range(16)]
 assert all(len(a)==6 for a in cards) and all(a&b for a,b in combinations(cards,2))
 assert all(2<=len(s)<=4 for s in support)
 if require_tau6:
  sm=[sum(1<<v for v in s) for s in support]
  assert not any(sm[a]|sm[b]|sm[c]|sm[d]|sm[e]==65535 for a,b,c,d,e in combinations(range(len(sm)),5))
 return [sorted(a) for a in cards]

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--start',type=int,default=0);ap.add_argument('--stop',type=int,default=463);ap.add_argument('--budget',type=int,default=50000);ap.add_argument('--solver',default='cadical195');ap.add_argument('--no-symmetry',action='store_true');args=ap.parse_args()
 root=Path(__file__).resolve().parents[1];rows=[json.loads(l) for l in (root/'data'/'eight_cores.jsonl').read_text().splitlines()]
 output=root/'results'/('sat_results_%s_%s.jsonl'%(args.solver,args.start))
 with output.open('w') as f:
  for i in range(args.start,min(args.stop,len(rows))):
   S=rows[i]['supports'];start=time.monotonic();cnf,nv,data,meta=build(S,symmetry=not args.no_symmetry)
   with Solver(name=args.solver,bootstrap_with=cnf) as solver:
    if args.budget:solver.conf_budget(args.budget);ans=solver.solve_limited()
    else:ans=solver.solve()
    rec=dict(core=i,status='UNSAT' if ans is False else 'SAT' if ans else 'UNKNOWN',variables=nv,clauses=len(cnf),seconds=round(time.monotonic()-start,3),stats=solver.accum_stats(),**meta)
    if ans:
     rec['cards']=audit(S,solver.get_model(),data,True)
     (root/'results'/'SIXTEEN_EXAMPLE.json').write_text(json.dumps(rec,indent=2))
   f.write(json.dumps(rec)+'\n');f.flush();print({k:v for k,v in rec.items() if k!='cards'},flush=True)
   if ans:break
