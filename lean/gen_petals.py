"""Writes the Lean 4 form of [P2, Lemma 3] for bv_decide.

COVERS [P2, Lemma 3]. Triples of the n points are the bits of H (lexicographic). S y is a
choice of four petals at the point y: bit k of S y is the k-th pair of the other points.
Hypotheses: the petals of x = 0 are {0,1,2}, {0,3,4}, {0,5,6}, {0,7,8}; every point has four
petals in H (each other point in at most one chosen pair); x lies in at most `bound` triples.
Conclusion: some petal of x and two further triples are pairwise disjoint.

  python3 gen_petals.py 11 6 Petals         the lemma (expected: proved)
  python3 gen_petals.py 11 7 Petals_ctl7    control (expected: counterexample)
"""
import itertools, sys
n = int(sys.argv[1]); bound = int(sys.argv[2]); name = sys.argv[3]
P = range(n); T = list(itertools.combinations(P, 3)); ti = {t: i for i, t in enumerate(T)}; NT = len(T)
pet = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (0, 7, 8)]
NP = (n - 1) * (n - 2) // 2


def h(t):
    return f"H.getLsbD {ti[tuple(sorted(t))]}"


def bal(xs, op):
    if len(xs) == 1:
        return xs[0]
    m = len(xs) // 2
    return f"({bal(xs[:m], op)} {op} {bal(xs[m:], op)})"


def popsum(bits_expr, idxs, w):
    return bal([f"(BitVec.zeroExtend {w} (BitVec.extractLsb' {k} 1 {bits_expr}))" for k in idxs], "+")


L = ["import Std.Tactic.BVDecide", "", "set_option maxHeartbeats 0", "set_option maxRecDepth 100000", "",
     f"/-- [P2, Lemma 3] on {n} points, the centre x = 0 in at most {bound} triples.",
     "Triples are the bits of H in lexicographic order. S y is a choice of four petals at y:",
     "bit k of S y is the k-th pair of the other points, in lexicographic order. -/",
     f"theorem petals_{n}_{bound} (H : BitVec {NT}) (S : Fin {n} → BitVec {NP})"]
hy = []
for p in pet:
    hy.append(f"{h(p)} = true")
for y in P:
    others = [p for p in P if p != y]
    prs = list(itertools.combinations(others, 2))
    for k, pq in enumerate(prs):
        hy.append(f"((S {y}).getLsbD {k} = true → {h((y,) + pq)} = true)")
    for z in others:
        m = sum(1 << k for k, pq in enumerate(prs) if z in pq)
        hy.append(f"(S {y} &&& {m}#{NP}) &&& ((S {y} &&& {m}#{NP}) - 1#{NP}) = 0#{NP}")
    hy.append(f"{popsum(f'(S {y})', range(NP), 6)} ≥ 4#6")
xs = [ti[t] for t in T if 0 in t]
hy.append(f"{popsum('H', xs, 6)} ≤ {bound}#6")
for i, x in enumerate(hy):
    L.append(f"    (h{i} : {x})")
pets = set(pet); concl = []
for a, b, c in itertools.combinations(T, 3):
    if set(a) & set(b) or set(a) & set(c) or set(b) & set(c):
        continue
    if a in pets or b in pets or c in pets:
        concl.append(f"({h(a)} && {h(b)} && {h(c)})")
L.append(f"    : {bal(concl, '||')} = true := by")
L.append("  bv_decide")
L.append(f"\n#print axioms petals_{n}_{bound}")
open(f"{name}.lean", "w").write("\n".join(L) + "\n")
print(len(hy), len(concl))
