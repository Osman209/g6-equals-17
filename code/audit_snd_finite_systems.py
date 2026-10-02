#!/usr/bin/env python3
"""Finite sanity checks of the incidence lemmas of [P6, §6] (needs scipy).

COVERS [P6, §6]: on 1,200 random intersecting uniform dual block systems (300 with a
prescribed strong group carrying ten disjoint triples) it checks Lemma 13, Lemma 14,
(6.2)-(6.10), the SND vertex capacities and Lemma 15 with its summed form.
A finite sanity check, not a proof of the lemmas.
"""
import random,itertools,math
from collections import Counter
from scipy.optimize import differential_evolution,NonlinearConstraint
rng=random.Random(20261002)
def pack(edges):
 best=[]
 def rec(i,used,out):
  nonlocal best
  if len(out)+len(edges)-i<=len(best):return
  if i==len(edges):best=out[:];return
  if not edges[i]&used:rec(i+1,used|edges[i],out+[i])
  rec(i+1,used,out)
 rec(0,set(),[]);return best
strong_total=0
for trial in range(1200):
 n=rng.randrange(20,45);blocks=[]
 if trial%4==0:
  # All four-blocks share marked card 0. Prescribed group is a maximum.
  blocks.append(frozenset(range(4)))
  for i in range(10):blocks.append(frozenset((0,4+3*i,5+3*i,6+3*i)))
  n=max(n,34);groups=[blocks[0]];selected=[0]
 else:
  for _ in range(rng.randrange(1,13)):blocks.append(frozenset(rng.sample(range(n),4)))
  groups=None
 for _ in range(rng.randrange(0,12)):blocks.append(frozenset(rng.sample(range(n),3)))
 for x,y in itertools.combinations(range(n),2):
  if not any(x in b and y in b for b in blocks):blocks.append(frozenset((x,y)))
 deg=Counter(x for b in blocks for x in b);r=max(deg.values())
 for x in range(n):blocks.extend([frozenset((x,))]*(r-deg[x]))
 four=[i for i,b in enumerate(blocks) if len(b)==4]
 if groups is None:
  selected=[four[i] for i in pack([blocks[i] for i in four])];groups=[blocks[i] for i in selected]
 else:assert len(pack([blocks[i] for i in four]))==1
 clean=set().union(*groups);J=set(range(n))-clean;q=len(J);Nc=len(clean)
 Omega=3*r-q-Nc+1;Rtot=0;Rs=0;marked=set();weak=set();ks=0;B3s=0;B3w=0
 for group,gi in zip(groups,selected):
  cards=[]
  for A in group:
   bs=[b for i,b in enumerate(blocks) if A in b and i!=gi]
   triples=[b&J for b in bs if len(b&J)==3]
   p=len(triples);R=sum(len(b&J) for b in bs)-q
   nu=len(pack(triples));assert nu>=p-R
   Rtot+=R;cards.append((A,p,R,nu))
  strong=[x for x in cards if x[3]>=10]
  if strong:
   assert len(strong)==1
   A,p,R,nu=strong[0];ks+=1;marked.add(A);Rs+=R;B3s+=p
   assert all(p2==0 for A2,p2,R2,nu2 in cards if A2!=A)
  else:
   weak.update(group);B3w+=sum(x[1] for x in cards)
   assert sum(x[1] for x in cards)<=sum(x[2] for x in cards)+36
 kw=len(groups)-ks;eligible=weak|marked;strong_total+=ks
 B2=0;B3=0
 for b in blocks:
  j=len(b&J);c=len(b&clean)
  if j==2 and c==2:B2+=1;assert b&eligible
  if j==3 and c==1:B3+=1;assert b&eligible
 assert B3==B3s+B3w
 assert B3<=q*ks/3+Rtot-2*Rs/3+36*kw+1e-8
 assert B2+B3<=(4*kw+ks)*(r-1)
 L=Nc*(q-r+1-Omega)/2;d=2*r-q+1
 N1=sum(len(b&J)==1 for b in blocks)
 assert L+Rtot<=B2+B3
 assert L+N1<=q*d/2+q*ks/3-2*Rs/3+36*kw+1e-8
 assert 3*ks*(r-1)<=Nc*(r-1)-L-Rtot+1e-8
 assert (1+q/(9*(r-1)))*L+q*Rtot/(9*(r-1))+N1+2*Rs/3<=q*d/2+q*Nc/9+36*kw+1e-8
 RE=sum(sum(len(b&J) for b in blocks if A in b)-q for A in eligible)
 IE=sum(len(b&J)==1 for A in eligible for b in blocks if A in b)
 SND=clean-eligible
 RN=Rtot-RE
 IN=sum(len(b&J)==1 for A in SND for b in blocks if A in b)
 assert IE+IN<=3*N1
 assert 2*B2+3*B3<=q*len(eligible)+RE-IE
 outgoing=sum(len(b&J)==2 and len(b&clean)==2 for A in SND for b in blocks if A in b)
 slots=sum(len(b&J)==2 for A in eligible for b in blocks if A in b)
 assert outgoing<=slots
 assert outgoing<=B2
 n2all=sum(len(b&J)==2 for A in clean for b in blocks if A in b)
 assert n2all-2*B2<=Omega*Nc-Rtot
 assert 4*B2+3*B3>=Nc*(q-2*Omega)+3*Rtot-3*N1
 assert Nc*(q-2*Omega)+N1+3*RN+2*Rs<=2*q*d+q*ks+108*kw+1e-8
 assert outgoing>=3*ks*(q/2-Omega)+1.5*RN-.5*IN-1e-8
 assert 6*(q-Omega)*ks+3*B3<=q*Nc+Rtot-4*RN+IN-IE+1e-8
 assert 12*L+2*Rtot+10*RN+6*Rs+10*N1+IE<=q*Nc+5*q*d+324*kw+1e-8
 for A in SND:
  RA=sum(len(b&J) for b in blocks if A in b)-q
  assert 3*ks-1<=2*r-q-RA
  for b in blocks:
   if A not in b:continue
   j=len(b&J)
   assert j<=2
   assert len((b&SND)-{A})<=2-j
 assert 3*ks*(3*ks-1)+RN<=3*ks*(2*r-q)
print('FINITE_SYSTEMS_VERIFIED' ,1200,'STRONG_GROUPS_TESTED',strong_total)
