"""COVERS [P7]: every computation behind g(7) >= 19, with the expected answer for each step.

    NAUTY=/path/to/nauty2_8_8 python code/verify_g7_lower.py            # quick, ~10 min
    NAUTY=/path/to/nauty2_8_8 python code/verify_g7_lower.py --full     # everything, hours

NAUTY is a nauty source directory after `./configure && make nauty.a` (nauty.h and nauty.a).
The C programs are compiled into a temporary directory and run there; the resumable runs
leave their logs in that directory. Needs python-sat for the two SAT routes.

Quick mode: Lemma 2 for twelve cards, the calibrations at r = 6, the c = 14 profile by both routes, matching number at
most 2 for c = 14, and the core step by SAT. Full mode adds Lemma 2 for thirteen cards and with a second solver, its controls, the c = 8 and c = 2 profiles by
both routes, matching number at most 2 for c = 8 and c = 2, the plain exhaustive search of
c = 14, and the core enumeration at r = 7. The recorded full run is
results/g7_lower_checks.txt.

Exits non-zero if any answer differs from the expected one.
"""
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
FULL = "--full" in sys.argv
NAUTY = os.environ.get("NAUTY")
if not NAUTY or not (Path(NAUTY) / "nauty.a").is_file():
    sys.exit("set NAUTY to a built nauty source directory (with nauty.h and nauty.a)")

bad = 0


def run(cmd, cwd, expect, label):
    global bad
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True).stdout
    lines = [l for l in out.splitlines() if l.startswith("RESULT")]
    text = lines[-1] if lines else "(no RESULT line)"
    ok = re.search(expect, text) is not None
    bad += not ok
    print("%s  %s\n      %s" % ("PASS" if ok else "FAIL", label, text), flush=True)


with tempfile.TemporaryDirectory() as d:
    for src, exe, nauty in (("r7_kernel_exhaustive.c", "exhaustive", False),
                            ("r7_kernel_matched.c", "matched", True),
                            ("r7_cores.c", "cores", True)):
        cmd = ["cc", "-O2", "-o", str(Path(d) / exe), str(CODE / src)]
        if nauty:
            cmd[2:2] = ["-I", NAUTY]
            cmd.append(str(Path(NAUTY) / "nauty.a"))
        subprocess.run(cmd, check=True)
    E, M, C = str(Path(d) / "exhaustive"), str(Path(d) / "matched"), str(Path(d) / "cores")
    py = [sys.executable]

    # calibrations at r = 6
    run([E, "12", "12", "4"], d, r": 69120 decompositions", "r = 6 kernels, c = 12 ([P3, §2a]: 69,120)")
    run([E, "12", "6", "4"], d, r": 558672 decompositions", "r = 6 kernels, c = 6 ([P3, §2a]: 558,672)")
    run([M, "12", "12"], d, r"FOUND", "r = 6, matched route finds a kernel")
    run(py + [str(CODE / "r7_kernel_sat.py"), "12", "12"], d, r"FOUND", "r = 6, SAT route finds a kernel")
    run(py + [str(CODE / "r7_cores_sat.py"), "6", "8", "3"], d, r": SAT", "r = 6 cores exist (SAT route)")
    if FULL:
        run([C, "6", "8"], d, r"cores up to isomorphism 463 ", "r = 6 cores: the 463 of [P3, §3]")

    # r = 7, [P7, Lemma 2]: twelve and thirteen cards
    for m_, k_ in ((12, 1), (12, 2)) + (((13, 1), (13, 2)) if FULL else ()):
        for solver in ("cadical195", "glucose4") if FULL else ("cadical195",):
            run(py + [str(CODE / "r7_small_families.py"), str(m_), "7", str(k_), solver], d, r": UNSAT",
                "%d cards: at most %d disjoint triples impossible (%s)" % (m_, k_, solver))
    if FULL:
        for m_, k_ in ((13, 3), (12, 3), (12, 4)):
            run(py + [str(CODE / "r7_small_families.py"), str(m_), "7", str(k_)], d, r": SAT", "control: %d cards, %d disjoint triples" % (m_, k_))

    # r = 7, the core step
    run(py + [str(CODE / "r7_cores_sat.py"), "7", "10", "7"], d, r": UNSAT", "r = 7: no core (SAT route)")
    if FULL:
        run([C, "7", "10"], d, r"triangle systems 0, raw cores 0, cores up to isomorphism 0 ",
            "r = 7: no core (enumeration route)")

    # r = 7, the kernels
    profiles = (14, 8, 2) if FULL else (14,)
    for c in profiles:
        run([E, "14", str(c), "3"], d, r": 0 decompositions", "r = 7, c = %d: matching number <= 2 impossible" % c)
        run([M, "14", str(c)], d, r"NO decomposition with matching number 3", "r = 7, c = %d: matched route" % c)
        run(py + [str(CODE / "r7_kernel_sat.py"), "14", str(c)], d, r"none found",
            "r = 7, c = %d: SAT route" % c)
    if FULL:
        run([E, "14", "14", "4"], d, r": 0 decompositions", "r = 7, c = 14: plain exhaustive search")

if bad:
    print("FAIL: %d step(s) disagree" % bad)
    sys.exit(1)
print("PASS: every step gives its expected answer%s" % ("" if FULL else " (quick mode)"))
