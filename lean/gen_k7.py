"""Writes K7.lean: the K7 lemma of [P1, §3] / [P2, Lemma 2] as a Lean 4 theorem for bv_decide.

COVERS [P1, Lemma 2]. Edges of K7 are the bits 0..20 of a BitVec 21, in lexicographic order
of the pairs. Hypotheses: each of T0..T3 meets every vertex and has at most five edges.
Conclusion: for one of the 105 pairs (vertex x, perfect matching M of the other six), M meets
three of T0..T3; an edge of the fourth at x then completes a four-edge cover meeting all four.

  python3 gen_k7.py            writes K7.lean          (expected: proved)
  python3 gen_k7.py --control  writes K7_control.lean  (asks M to meet all four; expected:
                                                         bv_decide reports a counterexample)
"""
import itertools
import sys

control = "--control" in sys.argv
V = range(7)
E = list(itertools.combinations(V, 2))
idx = {e: i for i, e in enumerate(E)}


def mask(es):
    return sum(1 << idx[tuple(sorted(e))] for e in es)


def pms(W):
    if not W:
        yield []
        return
    a = W[0]
    for b in W[1:]:
        for r in pms([w for w in W if w not in (a, b)]):
            yield [(a, b)] + r


vm = [mask([e for e in E if v in e]) for v in V]
units = [mask(m) for x in V for m in pms([v for v in V if v != x])]
T = ["T0", "T1", "T2", "T3"]
need = 4 if control else 3
name = "k7_control" if control else "k7_lemma"


def hit(t, m):
    return f"({t} &&& {m}#21 != 0#21)"


def size(t):
    return " + ".join(f"(BitVec.zeroExtend 5 (BitVec.extractLsb' {k} 1 {t}))" for k in range(21))


L = ["import Std.Tactic.BVDecide", "", "set_option maxHeartbeats 0", "set_option maxRecDepth 100000", "",
     "/-- The K7 lemma of [P1, §3]: four edge covers of K7 with at most five edges each admit a",
     "vertex x and a perfect matching M of the other six vertices meeting %s of them." % ("all four" if control else "three"),
     "Edges of K7 are bits 0..20 (lexicographic pairs); each unit is the mask of one matching. -/",
     f"theorem {name} (T0 T1 T2 T3 : BitVec 21)"]
for t in T:
    for v in V:
        L.append(f"    (c{t}{v} : {t} &&& {vm[v]}#21 != 0#21)")
    L.append(f"    (s{t} : {size(t)} ≤ 5#5)")
L.append("    : " + " ∨\n      ".join(
    "(" + " || ".join("(" + " && ".join(f"decide {hit(t, u)}" for t in tri) + ")"
                      for tri in itertools.combinations(T, need)) + ") = true"
    for u in units) + " := by")
L.append("  bv_decide")
if not control:
    L.append(f"\n#print axioms {name}")
out = "K7_control.lean" if control else "K7.lean"
open(out, "w").write("\n".join(L) + "\n")
print("wrote", out, "with", len(units), "units")
