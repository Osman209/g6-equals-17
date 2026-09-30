"""Build or verify a global one-centre box certificate.

COVERS the one-centre reward bounds of the coefficient route (to be written into [P5]):
for one random centre Z with |Z| <= 2 and independent Poisson bulk, every model with
mean missing fraction at most mu_max has reward E R >= target, over the whole bulk box
[0, 1/2]^4 and every centre law.  Verification is exact rational arithmetic.
Build needs scipy; verification uses only the Python standard library.
The model and rigorous box relaxation are explained in README.md.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json
import sys
import time
from pathlib import Path

MASKS=tuple(s for s in range(16) if s.bit_count()<=2)
A=tuple(tuple(int(s>>i&1) for s in MASKS) for i in range(4)) + (
    tuple(int(s.bit_count()==2) for s in MASKS),
    tuple(-s.bit_count() for s in MASKS))

@lru_cache(None)
def exp_bounds(x):
    # Alternating Taylor series for exp(-x), 0 <= x <= 1/2.
    assert 0<=x<=F(1,2)
    term=F(1); total=F(1); even=None
    for k in range(1,16):
        term*= -x/k; total+=term
        if k==14:even=total
    assert 0<=total<=even<=1
    return total,even

def product(values):
    ans=F(1)
    for v in values:ans*=v
    return ans

@lru_cache(None)
def cost_lower(lo):
    eb=[exp_bounds(x) for x in lo]
    out=[]
    for mask in MASKS:
        rem=[i for i in range(4) if not(mask>>i&1)]
        if mask.bit_count()==2:
            val=(2-sum(eb[i][1] for i in rem))/2
        elif mask.bit_count()==1:
            val=(2-sum(eb[i][1] for i in rem)+product(eb[i][0] for i in rem))/2
        else:
            val=1-sum(v[1] for v in eb)/2
            val+=sum(product(eb[i][0] for i in inds) for inds in combinations(range(4),3))/2
            val-=product(v[1] for v in eb)
        out.append(max(F(0),val))
    return tuple(out)

def rhs(lo,hi,mass,rho):
    return tuple(1-2*x for x in lo)+(rho,-mass+2*sum(hi))

def empty_reason(lo,hi,mass,rho):
    # We only need the ordered sector lambda_0 <= ... <= lambda_3.
    if any(max(lo[:i+1])>hi[i] for i in range(4)):return 'order'
    required=mass-2*sum(hi)
    if required>1+rho:return 'pair_mass'
    if required>sum(1-2*x for x in lo):return 'card_mass'
    return None

def build(path,mu=F(2,5),rho=F(3,5),target=F(1,200)):
    import numpy as np
    from scipy.optimize import linprog
    mass=4*(1-mu); den=10**9
    matrix=np.array(A,dtype=float)
    stats={'LPs':0,'dual_leaves':0,'empty_leaves':0,'splits':0,'max_depth':0}
    minimum=None; start=time.time()
    def visit(lo,hi,depth):
        nonlocal minimum
        stats['max_depth']=max(stats['max_depth'],depth)
        reason=empty_reason(lo,hi,mass,rho)
        if reason:
            stats['empty_leaves']+=1;return {'empty':reason}
        c=cost_lower(lo); b=rhs(lo,hi,mass,rho)
        res=linprog([float(v) for v in c],A_ub=matrix,b_ub=[float(v) for v in b],
                    A_eq=np.ones((1,11)),b_eq=[1.0],bounds=(0,None),method='highs')
        stats['LPs']+=1
        if not res.success:raise RuntimeError('Uncertified LP failure: '+res.message)
        yi=[min(0,round(float(v)*den)) for v in res.ineqlin.marginals]
        y=[F(v,den) for v in yi]
        y0=min(c[j]-sum(A[i][j]*y[i] for i in range(6)) for j in range(11))
        lower=y0+sum(b[i]*y[i] for i in range(6))
        if lower>=target:
            stats['dual_leaves']+=1
            minimum=lower if minimum is None else min(minimum,lower)
            return {'dual':yi,'y0':str(y0)}
        if stats['LPs']%1000==0:
            print(json.dumps({'progress':stats,'seconds':round(time.time()-start,1)}),flush=True)
        if depth>=60 or stats['LPs']>=100000:
            raise RuntimeError('Resource limit; no complete certificate claimed.')
        dim=max(range(4),key=lambda i:hi[i]-lo[i]);mid=(lo[dim]+hi[dim])/2
        h=list(hi);h[dim]=mid;l=list(lo);l[dim]=mid
        stats['splits']+=1
        return {'split':dim,'left':visit(lo,tuple(h),depth+1),'right':visit(tuple(l),hi,depth+1)}
    tree=visit((F(0),)*4,(F(1,2),)*4,0)
    obj={'format':'one-centre-rational-box-v1','mu_max':str(mu),'rho_max':str(rho),
         'coverage_min':str(mass),'target':str(target),'dual_denominator':den,'tree':tree,
         'stats':stats,'minimum_certified_dual':str(minimum),'seconds':time.time()-start}
    Path(path).write_text(json.dumps(obj,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in obj.items() if k!='tree'},indent=2))

def verify(path):
    data=json.loads(Path(path).read_text())
    assert data['format']=='one-centre-rational-box-v1'
    mu=F(data['mu_max']);rho=F(data['rho_max']);mass=4*(1-mu);target=F(data['target'])
    assert mass==F(data['coverage_min']) and 0<=rho<=1 and 0<=mu<=1
    den=data['dual_denominator'];assert isinstance(den,int) and den>0
    counts={'dual_leaves':0,'empty_leaves':0,'splits':0};smallest=None
    def check(node,lo,hi):
        nonlocal smallest
        if 'empty' in node:
            assert empty_reason(lo,hi,mass,rho)==node['empty']
            counts['empty_leaves']+=1;return
        if 'dual' in node:
            assert len(node['dual'])==6 and all(isinstance(v,int) and v<=0 for v in node['dual'])
            y=[F(v,den) for v in node['dual']];y0=F(node['y0'])
            c=cost_lower(lo);b=rhs(lo,hi,mass,rho)
            assert all(y0+sum(A[i][j]*y[i] for i in range(6))<=c[j] for j in range(11))
            value=y0+sum(b[i]*y[i] for i in range(6))
            assert value>=target
            smallest=value if smallest is None else min(smallest,value)
            counts['dual_leaves']+=1;return
        dim=node['split'];assert type(dim) is int and 0<=dim<4
        mid=(lo[dim]+hi[dim])/2;h=list(hi);h[dim]=mid;l=list(lo);l[dim]=mid
        counts['splits']+=1
        check(node['left'],lo,tuple(h));check(node['right'],tuple(l),hi)
    check(data['tree'],(F(0),)*4,(F(1,2),)*4)
    print(json.dumps({'verified':True,'arithmetic':'exact rational; alternating-series exponential bounds',
        'mu_max':str(mu),'rho_max':str(rho),'lower_bound':str(target),
        'counts':counts,'minimum_dual_decimal_for_display':float(smallest)},indent=2))

if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Run without -O: assertions are certificate checks.')
    mode=sys.argv[1];path=sys.argv[2]
    if mode=='build':build(path,*(F(s) for s in sys.argv[3:]))
    elif mode=='verify':verify(path)
    else:raise SystemExit('Use build or verify')
