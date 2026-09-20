"""Exact K7 verification using only Python's standard library and integer bitsets.

For fixed a,b,c, an output meeting those inputs rules out every fourth input
that it also meets. Intersect the masks of fourth inputs missed by each such
output. An empty intersection certifies all remaining fourth inputs at once.

COVERS [P1, §3] and [P2, §2] — the finite K7 edge-cover lemma, all 294,239,817 quadruples.
"""
from itertools import combinations
from collections import Counter
from math import comb
import json


def universe():
    edges=list(combinations(range(7),2))
    covers=[]
    minimal=[]
    signatures={}
    types=Counter()
    for k in (4,5):
        for choice in combinations(range(21),k):
            degrees=[0]*7
            for i in choice:
                x,y=edges[i]
                degrees[x]+=1
                degrees[y]+=1
            if not all(degrees):
                continue
            mask=sum(1<<i for i in choice)
            if k==4:
                covers.append(mask)
            if all(min(degrees[edges[i][0]],degrees[edges[i][1]])==1 for i in choice):
                signature=tuple(sorted(degrees))
                minimal.append(mask)
                signatures[mask]=signature
                types[signature]+=1
    covers.sort()
    minimal.sort(key=lambda mask:(mask.bit_count(),mask))
    expected={(1,1,1,1,1,1,2):315,
              (1,1,1,1,1,1,4):105,
              (1,1,1,1,1,2,3):420}
    if dict(types)!=expected or len(covers)!=315 or len(minimal)!=840:
        raise AssertionError('Unexpected K7 universe')
    representatives={}
    for i,mask in enumerate(minimal):
        representatives.setdefault(signatures[mask],i)
    return covers,minimal,[representatives[s] for s in sorted(representatives)]


def incidence(covers,inputs):
    good=[0]*len(inputs)
    missed_by=[0]*len(covers)
    for i,f in enumerate(inputs):
        for j,g in enumerate(covers):
            if f&g:
                good[i]|=1<<j
            else:
                missed_by[j]|=1<<i
    return good,missed_by


def check_representative(good,missed_by,a):
    n=len(good)
    all_inputs=(1<<n)-1
    allowed=all_inputs^(1<<a)
    certified=0
    batches=0
    for b in range(n):
        if b==a:
            continue
        first_two=good[a]&good[b]
        for c in range(b+1,n):
            if c==a:
                continue
            # Exactly the fourth indices d>c, excluding the fixed a.
            candidates=allowed & ~((1<<(c+1))-1)
            if not candidates:
                continue
            size=candidates.bit_count()
            outputs=first_two&good[c]
            while outputs and candidates:
                bit=outputs&-outputs
                candidates &= missed_by[bit.bit_length()-1]
                outputs ^= bit
            batches+=1
            if candidates:
                bit=candidates&-candidates
                return (a,b,c,bit.bit_length()-1),certified,batches
            certified+=size
    return None,certified,batches


def self_check(covers,inputs):
    """Compare bulk certification with literal enumeration on bounded subcases."""
    # Sparse output sets force counterexamples; all outputs exercise success.
    pool=inputs[:8]+inputs[315:319]
    for outputs in (covers[:1],covers[:4],covers):
        good,missed=incidence(outputs,pool)
        for a in (0,5,11):
            literal=None
            for b,c,d in combinations([i for i in range(len(pool)) if i!=a],3):
                if not (good[a]&good[b]&good[c]&good[d]):
                    literal=(a,b,c,d)
                    break
            packed,count,_=check_representative(good,missed,a)
            if packed!=literal:
                raise AssertionError('Bulk search disagrees with literal enumeration')
            if packed is None and count!=comb(len(pool)-1,3):
                raise AssertionError('Wrong subcase coverage count')


def main():
    covers,inputs,reps=universe()
    self_check(covers,inputs)
    good,missed=incidence(covers,inputs)
    results=[]
    for a in reps:
        counterexample,certified,batches=check_representative(good,missed,a)
        if counterexample is not None:
            raise AssertionError({'counterexample_indices':counterexample,
                                  'input_edge_masks':[inputs[i] for i in counterexample]})
        if certified!=comb(839,3):
            raise AssertionError('Incomplete quadruple coverage')
        results.append({'representative':a,'quadruples_certified':certified,
                        'batches_checked':batches,'counterexamples':0})
    print(json.dumps({'status':'PASS','minimal_input_covers':840,'output_covers':315,
        'representative_types':3,'quadruples_certified':sum(x['quadruples_certified'] for x in results),
        'counterexamples':0,'method':'exact Python integer-bitset batch certification',
        'self_check':'matched literal enumeration on nine bounded subcases',
        'representatives':results,'scope':'full four-input-cover K7 lemma, not a sample'},indent=2))

if __name__=='__main__':
    main()
