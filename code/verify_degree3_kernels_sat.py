"""COVERS [P3, Lemma 2] by a second method — the extension test on the 341 shipped
maximum-degree-three kernels, decided by SAT instead of the exhaustive set-cover search of
verify_degree3_kernels.py.

For each kernel G in data/degree3_kernels_c{12,6,0}.json:
  * G is re-checked: twelve distinct six-element cards, pairwise intersecting, maximum
    degree three, no four-cover (so tau(G) = 5);
  * every five-cover of G is listed;
  * SAT: choose AT MOST K five-covers (repeats not excluded — a relaxation of "four distinct
    new cards"), with d_G(z) + (number of chosen covers containing z) <= K for every symbol,
    such that every five-cover of G is disjoint from some chosen cover [P3, Prop 2].

    python code/verify_degree3_kernels_sat.py            # K = 4 on all 341: must be UNSAT
    python code/verify_degree3_kernels_sat.py --control  # K = 5 on the two c = 12 kernels:
                                                         # the [P4] witness kernel must extend

The kernel files themselves come from verify_degree3_kernels.py / fast_enumerate.c; this
script checks the extension step only. Needs python-sat. A few minutes.
"""
from pathlib import Path
import itertools, json, sys
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

ROOT = Path(__file__).resolve().parents[1]
V = 12
TRI = list(itertools.combinations(range(V), 3))
MATCH = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)]


def decode(key, c):
    sup = [(1 << a) | (1 << b) | (1 << d) for a, b, d in (TRI[i] for i in key)]
    sup += [(1 << a) | (1 << b) for a, b in MATCH[:c // 2]]
    return sup


def covers(sup, k):
    out, full = [], (1 << V) - 1

    def go(start, chosen, acc):
        if len(chosen) == k:
            if acc == full:
                out.append(tuple(chosen))
            return
        for i in range(start, len(sup)):
            go(i + 1, chosen + [i], acc | sup[i])
    go(0, [], 0)
    return out


def extends(sup, K):
    cards = [frozenset(i for i, s in enumerate(sup) if s >> v & 1) for v in range(V)]
    assert all(len(c) == 6 for c in cards) and len(set(cards)) == V
    assert all(a & b for a, b in itertools.combinations(cards, 2))
    assert max(bin(s).count("1") for s in sup) == 3
    assert not covers(sup, 4), "tau(G) <= 4"
    C5 = covers(sup, 5)
    deg = [bin(s).count("1") for s in sup]
    P = IDPool(); cl = []
    sel = [P.id(i) for i in range(len(C5))]
    cl += CardEnc.atmost(sel, K, vpool=P, encoding=EncType.totalizer).clauses
    for z in range(len(sup)):
        lits = [sel[i] for i, T in enumerate(C5) if z in T]
        cap = K - deg[z]
        if cap <= 0:
            cl += [[-l] for l in lits]
        elif lits:
            cl += CardEnc.atmost(lits, cap, vpool=P, encoding=EncType.totalizer).clauses
    sets = [set(T) for T in C5]
    for T in sets:
        cl.append([sel[i] for i, U in enumerate(sets) if not (T & U)])
    with Solver(name="glucose4", bootstrap_with=cl) as s:
        return bool(s.solve()), len(C5)


def main():
    control = "--control" in sys.argv
    K, profiles = (5, [12]) if control else (4, [12, 6, 0])
    total = ext = 0
    which = []
    for c in profiles:
        reps = json.loads((ROOT / "data" / ("degree3_kernels_c%d.json" % c)).read_text())
        lo, hi = 10 ** 9, 0
        for idx, key in enumerate(reps):
            r, n5 = extends(decode(key, c), K)
            total += 1; ext += r; lo = min(lo, n5); hi = max(hi, n5)
            if r:
                which.append((c, idx))
        print("RESULT c=%d kernels %d five-covers %d-%d" % (c, len(reps), lo, hi), flush=True)
    print("RESULT K=%d kernels %d with an extension %d" % (K, total, ext))
    if control:
        # the [P4] witness kernel is representative #0 of profile (6,20); see
        # verify_degree3_kernels.py --witness
        if which != [(12, 0)]:
            print("FAIL: the control should find exactly the witness kernel, found", which); sys.exit(1)
        print("PASS: with five covers allowed, exactly one c = 12 kernel extends (the [P4] kernel)")
    else:
        if total != 341 or ext:
            print("FAIL"); sys.exit(1)
        print("PASS: none of the 341 kernels admits four covers satisfying the extension criterion")


if __name__ == "__main__":
    main()
