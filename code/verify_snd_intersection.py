#!/usr/bin/env python3
"""Exact rational certificate for the final minimization of [P5] (Theorem 1, Appendix A).

COVERS [P5, §7 and Appendix A]: on 1 <= gamma <= 2, c(gamma) <= lambda <= (4/5) X_T,
0 <= sigma <= 4 X_T, every point that satisfies the necessary constraints (A)-(F) and
the kappa interval (G) has (5/4)(lambda + max(R_rat, W_tr)) + sigma/4 >= X_T = 0.1108.
Exact Fraction interval arithmetic; boxes are removed only when a proved constraint
fails on the whole box, and accepted only when the lower bound reaches X_T exactly.
It checks arithmetic only; the lemmas that supply the inequalities are in the paper.

    python3 -S code/verify_snd_intersection.py      # do not use -O
"""

from fractions import Fraction as F
from functools import lru_cache
import time
TARGET=F(1108,10000)  # .1108
class I:
 def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b)
 def __add__(self,o):
  if not isinstance(o,I):o=I(o)
  return I(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return I(-self.b,-self.a)
 def __sub__(self,o):return self+-o if isinstance(o,I) else self+I(-o)
 def __rsub__(self,o):return I(o)+-self
 def __mul__(self,o):
  if not isinstance(o,I):o=I(o)
  p=[self.a*o.a,self.a*o.b,self.b*o.a,self.b*o.b]
  return I(min(p),max(p))
 __rmul__=__mul__
 def __truediv__(self,o):
  if not isinstance(o,I):o=I(o)
  assert o.a>0
  return self*I(1/o.b,1/o.a)
@lru_cache(None)
def root_lower(g):
 lo=F(0);hi=F(1,9)
 # At g=2 the root is 1/9; P decreases on this interval.
 for _ in range(32):
  m=(lo+hi)/2;p=27*m*m-(20-4*g)*m+(g-1)**2
  if p>0:lo=m
  else:hi=m
 return lo

def bound(box):
 gl,gh,cl,ch,sl,sh=box
 cl=max(cl,root_lower(gl))
 ch=min(ch,F(4,5)*(TARGET-sl/4))
 sh=min(sh,4*(TARGET-F(5,4)*cl))
 if cl>ch or sl>sh:return None,None
 g=I(gl,gh);c=I(cl,ch);sig=I(sl,sh)
 v=(3-g-3*c)/2;t=(g-1+c)/2;N=3-g-sig
 assert v.a>0 and N.a>0
 # Alternative-block necessary inequality, both branches retained.
 left=N*(g-1-sig)/2
 branch1=(g+sig)/3;branch2=4*sig
 upper=I(max(branch1.a,branch2.a),max(branch1.b,branch2.b))
 right=g*(2-g)/2+N*upper/4
 if (left-right).a>0:return None,None
 # Strong/weak alternative-block constraint, valid on both old branches.
 strong_left=N*(g*g+6*g-9-(9+g)*sig)
 strong_right=9*g*(2-g)
 if (strong_left-strong_right).a>0:return None,None
 slot_left=N*(5*g-6-6*sig)
 slot_right=5*g*(2-g)
 if (slot_left-slot_right).a>0:return None,None
 # sigma<gamma throughout the root box for this target.
 assert sig.b<g.a
 snd_left=(21*g-18*sig)*(N*(g-1-sig)-g*(2-g))
 snd_right=2*g*g*N
 if (snd_left-snd_right).a>0:return None,None
 # Each B2 symbol has at most one SND clean endpoint.
 # Dropping remaining singleton terms requires sigma<=4*gamma/9.
 assert 9*sig.b<4*g.a
 global_left=9*(g-2*sig)*(N*(g-1-sig)-g*(2-g))
 global_right=2*g*g*(2-g)
 if (global_left-global_right).a>0:return None,None
 # Summed unused degree-two slots, after eliminating kappa_s.
 # The discarded singleton coefficient is nonnegative only if gamma>=3sigma.
 if 3*sig.b<g.a:
  gap=g-2*sig
  used_left=3*N*gap*gap
  used_right=g*(2-g)*(7*g-12*sig)
  if (used_left-used_right).a>0:return None,None
 # Retain an existential interval for kappa_s. All discarded terms are nonnegative.
 d=2-g
 kap_lo=max(F(0), ((I(3)/g)*(left-g*d/2)).a, ((N*(g-2*sig)-2*g*d)/g).a)
 kap_hi=min((N/4).b,(d/3).b,(N*(3-g+sig)/6).b)
 if kap_lo>kap_hi:return None,None
 K=7-3*g-15*c-6*sig;d=2-g
 S_upper=t.b
 if v.a>d.b:
  loc=(d*t+(v-d)*(t+c)/2)/v
  S_upper=min(S_upper,loc.b)
 Qlo=N.a/2-3*c.b-S_upper
 w=min(v.a/16,v.a/(1+7*v.b+9*N.b)*max(F(0),Qlo-max(F(0),-K.a)))
 rain=max(F(0),K.a)*v.a/(2*(v.b+3*N.b))
 low=F(5,4)*(c.a+max(w,rain))+sig.a/4
 return low,(gl,gh,cl,ch,sl,sh)

def main():
 if not __debug__:raise RuntimeError('Run without -O: assertions are part of this verifier.')
 root=(F(1),F(2),F(0),F(4,5)*TARGET,F(0),4*TARGET)
 stack=[root];leaves=empty=splits=0;lowest=None;start=time.time()
 while stack:
  original=stack.pop();low,box=bound(original)
  if box is None:empty+=1;continue
  if low>=TARGET:
   leaves+=1;lowest=low if lowest is None else min(lowest,low);continue
  scores=[box[1]-box[0],15*(box[3]-box[2]),6*(box[5]-box[4])]
  axis=max(range(3),key=lambda j:scores[j]);j=2*axis;m=(box[j]+box[j+1])/2
  a=list(box);b=list(box);a[j+1]=m;b[j]=m
  stack.extend([tuple(a),tuple(b)]);splits+=1
  if splits%5000==0:print('progress',splits,'pending',len(stack),'seconds',round(time.time()-start,1),flush=True)
  if splits>400000:raise RuntimeError('Resource limit; no certificate claimed')
 print('VERIFIED',float(TARGET),'rational_leaves',leaves,'empty',empty,'splits',splits,'minimum_leaf_lower',str(lowest),'seconds',round(time.time()-start,2),flush=True)
if __name__=='__main__':main()
