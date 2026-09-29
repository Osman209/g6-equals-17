#!/usr/bin/env python3
"""Driver for code/verify_rainbow.c.

COVERS [P5, Lemmas 4 and 5]: the two four-family matching lemmas, exhaustively on 8, 9
and 10 vertices.  Compiles the C file with the system compiler, runs it, and checks that
both counterexample counts are zero.  It also checks the structural prediction of the
proofs: the configurations of three size-four matchings with no rainbow triple are the
same twelve at every size (two disjoint copies of K4), so adding vertices creates none.

    python3 code/verify_rainbow_lemmas.py      # under a minute

Exits non-zero on any counterexample, a changed count, or a compile failure.
"""
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    exe = os.path.join(tempfile.mkdtemp(), "verify_rainbow")
    subprocess.run(["cc", "-O2", "-o", exe, os.path.join(HERE, "verify_rainbow.c")],
                   check=True)
    ok = True
    for n in (8, 9, 10):
        out = subprocess.run([exe, str(n)], capture_output=True, text=True).stdout
        print(out.strip())
        norb = int(re.search(r"without-rainbow (\d+)", out).group(1))
        bad = [int(x) for x in re.findall(r"counterexamples (\d+)", out)]
        cfg = int(re.search(r"all-edges-safe (\d+)", out).group(1))
        ok &= bad == [0, 0] and norb == 12 and cfg == 192
    if not ok:
        print("FAIL")
        sys.exit(1)
    print("PASS: both four-family lemmas hold on 8, 9 and 10 vertices; the obstructions "
          "are the same 12 and 192 configurations at every size.")


if __name__ == "__main__":
    main()
