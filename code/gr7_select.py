#!/usr/bin/env python3
"""Exact selection step of gr_upper.py at r = 7, by a SAT solver instead of plain search.

COVERS the r = 7 attempt of gr_upper.py: for each of the 38 kernels with tau = 6, either a
21-card witness (g(7) <= 21) or UNSAT (no selection for that kernel).

For each kernel (seed) with tau = 6, decide whether 6 of its 6-covers can be chosen so that
every 6-cover of the kernel is block-disjoint from at least one chosen cover.
Counterexample-guided: solve on a growing set of covers, add the ones the current choice leaves
unserved.  Each kernel ends in one of two exact answers:
  WITNESS  -> the 21-card family is written to gr_witness_7_seed<s>.json and re-checked,
              so g(7) <= 21;
  UNSAT    -> no selection exists for this kernel (a proof for this kernel, not a timeout).

Needs gr_upper.py in the same folder and python-sat.

    python gr7_select.py                    # all 38 kernels with tau = 6 from seeds 0..399
    python gr7_select.py 7 24 43            # only these seeds
"""
import random, time, sys, json
ARGS = sys.argv[1:]; sys.argv = ['x']
import gr_upper as g
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

N, r = 15, 7
ALL38 = [7, 24, 43, 44, 76, 78, 86, 88, 104, 114, 119, 122, 150, 154, 160, 178, 193, 195, 205,
         206, 207, 215, 224, 230, 241, 242, 245, 247, 250, 251, 277, 279, 281, 319, 360, 369, 370, 374]
seeds = [int(a) for a in ARGS] or ALL38
log = open('gr7_select.log', 'a')
def say(m):
    print(m, flush=True); log.write(m + '\n'); log.flush()

for s in seeds:
    blocks, cards = g.kernel(N, r, random.Random(s))
    masks = [sum(1 << v for v in b) for b in blocks]
    assert g.tau(masks, N, r - 1) == r - 1, "seed %d: tau is not 6" % s
    cov = g.covers(masks, r - 1, N); sv = g.served_sets(cov); n = len(cov)
    servers = [[j + 1 for j in range(n) if sv[j] >> i & 1] for i in range(n)]
    card = CardEnc.atmost(lits=list(range(1, n + 1)), bound=r - 1, top_id=n, encoding=EncType.totalizer)
    S = Cadical153(bootstrap_with=card.clauses); t0 = time.time(); added = 0
    while True:
        if not S.solve():
            say("seed %d: UNSAT, no selection exists (%d covers, %d constraints used)  [%.0fs]"
                % (s, n, added, time.time() - t0)); break
        mdl = S.get_model(); pick = [j for j in range(n) if mdl[j] > 0]
        u = 0
        for j in pick: u |= sv[j]
        miss = [i for i in range(n) if not u >> i & 1]
        if not miss:
            ch = [cov[j] for j in pick]; m, ns = g.check(blocks, cards, ch, r)
            say("seed %d: WITNESS, %d cards on %d symbols, tau = 7, so g(7) <= %d  [%.0fs]"
                % (s, m, ns, m, time.time() - t0))
            json.dump({"r": r, "seed": s,
                       "cards": [sorted(c) for c in cards] + [sorted(set(d) | {len(blocks)}) for d in ch]},
                      open("gr_witness_7_seed%d.json" % s, "w"))
            sys.exit(0)
        for i in miss[:5]:
            S.add_clause(servers[i]); added += 1
        if added % 100 == 0:
            say("  seed %d: %d constraints, current choice misses %d  [%.0fs]" % (s, added, len(miss), time.time() - t0))
