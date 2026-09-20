"""Exhaustive necessary histograms, cross-checked by dynamic programming.

COVERS [P1, §6] — the exact enumeration leaving thirteen degree histograms.
"""
from itertools import combinations_with_replacement
from math import comb
import json

EXPECTED = {
    ((0,10,15),(6,2,0,0,7)), ((0,10,15),(7,0,0,2,6)),
    ((0,10,15),(7,0,1,0,7)),
    ((1,12,13),(7,3,0,1,4)), ((1,12,13),(8,1,0,3,3)),
    ((1,12,13),(8,1,1,1,4)), ((1,12,13),(8,2,0,0,5)),
    ((1,12,13),(9,0,0,2,4)),
    ((0,14,12),(8,3,0,1,3)), ((0,14,12),(9,1,1,1,3)),
    ((0,14,12),(9,2,0,0,4)), ((0,14,12),(10,0,0,2,3)),
    ((0,14,12),(10,0,1,0,4)),
}

def score(k):
    return 6*comb(k,2)-3*max(k-3,0)-(k==6)

def enumerate_histograms():
    rows = set()
    for qs in combinations_with_replacement(range(2,7),15):
        if sum(qs)%4:
            continue
        t=sum(qs)//4
        if sum(map(score,qs)) < 6*comb(t,2):
            continue
        ns=tuple(qs.count(k) for k in range(2,7))
        for a in range(8):
            b,rem=divmod(90-4*t-2*a,3)
            if not rem and b>=0 and sum(ns[1:4])>=2*a:
                rows.add(((a,b,t),ns))
    return rows

def dp_profiles():
    """Independent card-by-card maximum; mark exactly 2a binary cards."""
    surviving=set()
    maxima={}
    for a in range(8):
        dp={(0,0):0}  # (high appearances, binary-card count) -> best score
        for _ in range(15):
            nxt={}
            for (total,marked),val in dp.items():
                for q in range(2,7):
                    for binary in (0,1):
                        if binary and q not in (3,4,5):
                            continue
                        if marked+binary>2*a:
                            continue
                        key=(total+q,marked+binary)
                        nxt[key]=max(nxt.get(key,-1),val+score(q))
            dp=nxt
        for t in range(23):
            b,rem=divmod(90-4*t-2*a,3)
            if rem or b<0:
                continue
            best=dp.get((4*t,2*a),-1)
            maxima[f'{a},{b},{t}']=best
            if best>=6*comb(t,2):
                surviving.add((a,b,t))
    return surviving,maxima

def main():
    rows=enumerate_histograms()
    if rows!=EXPECTED:
        raise AssertionError({'unexpected': sorted(rows-EXPECTED),
                              'missing': sorted(EXPECTED-rows)})
    profiles,maxima=dp_profiles()
    if profiles!={p for p,_ in rows}:
        raise AssertionError('Independent DP disagrees with enumeration')
    print(json.dumps({'status':'PASS','histogram_count':len(rows),
        'profiles':sorted(profiles),'histograms':sorted(rows),
        'method':'exact enumeration + independent integer DP',
        'scope':'necessary numerical conditions; manual exclusions are in papers/'},indent=2))

if __name__=='__main__':
    main()
