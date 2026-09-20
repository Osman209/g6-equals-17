"""COVERS [P3, §6] — DRAT generation and checking over the certificate archive."""
#!/usr/bin/env python3
"""
Generate DIMACS CNFs with the exact audited build(), prove UNSAT with standalone
CaDiCaL, and independently verify each DRAT proof with drat-trim.

Designed for Windows Python + WSL, matching the completed certification workflow.
"""
from pathlib import Path
import argparse
import json
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
DATA = ROOT / "data"
CERT = ROOT / "certificates"

sys.path.insert(0, str(CODE))
try:
    from search_sixteen import build
except ImportError as e:
    raise SystemExit(
        "Missing code/search_sixteen.py. Copy the exact audited file first."
    ) from e

CADICAL = "~/cadical/build/cadical"
DRATTRIM = "~/drat-trim/drat-trim"

def to_wsl(path):
    s = str(Path(path).resolve()).replace("\\", "/")
    if len(s) >= 3 and s[1] == ":":
        return f"/mnt/{s[0].lower()}/{s[3:]}"
    return s

def write_cnf(path, cnf, nv):
    with path.open("w", newline="\n") as f:
        f.write(f"p cnf {nv} {len(cnf)}\n")
        for clause in cnf:
            f.write(" ".join(map(str, clause)) + " 0\n")

def run_wsl(command):
    return subprocess.run(
        ["wsl", "bash", "-lc", command],
        text=True,
        capture_output=True,
    )

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--stop", type=int, default=463)
    args = ap.parse_args()

    CERT.mkdir(exist_ok=True)
    core_file = DATA / "eight_cores.jsonl"
    if not core_file.exists():
        raise SystemExit("Missing data/eight_cores.jsonl")

    rows = [json.loads(line) for line in core_file.read_text().splitlines()]
    summary = CERT / "certificate_summary.jsonl"

    verified = failed = skipped = 0

    for core_id in range(args.start, min(args.stop, len(rows))):
        tag = f"core_{core_id:03d}"
        cnf_path = CERT / f"{tag}.cnf"
        drat_path = CERT / f"{tag}.drat"
        cadical_log = CERT / f"{tag}.cadical.txt"
        verify_log = CERT / f"{tag}.verify.txt"
        marker = CERT / f"{tag}.verified"

        if marker.exists():
            print(f"[{core_id:03d}] already VERIFIED")
            skipped += 1
            continue

        print(f"[{core_id:03d}] building CNF...", flush=True)
        S = rows[core_id]["supports"]
        cnf, nv, data, meta = build(S, symmetry=True)

        max_var = max(abs(lit) for clause in cnf for lit in clause)
        assert max_var <= nv
        write_cnf(cnf_path, cnf, nv)

        wcnf, wdrat = to_wsl(cnf_path), to_wsl(drat_path)

        print(f"[{core_id:03d}] {nv} vars, {len(cnf)} clauses; running CaDiCaL...",
              flush=True)
        t0 = time.time()

        cad = run_wsl(f"{CADICAL} {shlex.quote(wcnf)} {shlex.quote(wdrat)}")
        cad_text = cad.stdout + cad.stderr
        cadical_log.write_text(cad_text, errors="replace")

        if "s UNSATISFIABLE" not in cad_text:
            print(f"[{core_id:03d}] FAILED: CaDiCaL did not prove UNSAT")
            failed += 1
            continue

        print(f"[{core_id:03d}] UNSAT; verifying DRAT...", flush=True)
        check = run_wsl(
            f"{DRATTRIM} {shlex.quote(wcnf)} {shlex.quote(wdrat)} -i"
        )
        check_text = check.stdout + check.stderr
        verify_log.write_text(check_text, errors="replace")

        elapsed = round(time.time() - t0, 3)
        ok = "s VERIFIED" in check_text
        rec = {
            "core": core_id,
            "verified": ok,
            "variables": nv,
            "clauses": len(cnf),
            "seconds": elapsed,
            **meta,
        }

        with summary.open("a") as f:
            f.write(json.dumps(rec) + "\n")

        if ok:
            marker.write_text(json.dumps(rec, indent=2) + "\n")
            verified += 1
            size_mb = drat_path.stat().st_size / (1024 * 1024)
            print(f"[{core_id:03d}] VERIFIED ({elapsed}s, DRAT {size_mb:.2f} MB)")
        else:
            failed += 1
            print(f"[{core_id:03d}] FAILED verification")

    print()
    print("=== RESULT ===")
    print("VERIFIED:", verified)
    print("SKIPPED :", skipped)
    print("FAILED  :", failed)

if __name__ == "__main__":
    main()
