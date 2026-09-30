#!/usr/bin/env python3
"""Verify every one-centre certificate tree in certificates/one_centre/.

COVERS the one-centre reward bounds of the coefficient route (to be written into [P5]); the
checking logic is one_center_certificate.verify, exact rational arithmetic, standard library.

The trees are a release asset (certificates/ is not repository content).  Their SHA-256
values and the commands that generated them are in results/one_centre_manifest.txt.

    python3 code/verify_one_center_certificates.py      # about 15 seconds

Do not run with -O.
"""
import sys, io, json, contextlib
from fractions import Fraction
from pathlib import Path
if sys.flags.optimize:
    raise SystemExit('Run without -O: assertions are the checks.')
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'code'))
from one_center_certificate import verify
trees = sorted((ROOT / 'certificates' / 'one_centre').glob('allrho*.json'))
if not trees:
    raise SystemExit('certificates/one_centre/ is empty: unpack the release asset first')
rows = []
for t in trees:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        verify(t)
    d = json.loads(buf.getvalue())
    assert d['verified'] is True
    rows.append((Fraction(d['mu_max']), d['mu_max'], d['rho_max'], d['lower_bound'], t.name))
for _, mu, rho, lb, name in sorted(rows):
    print('verified  mu <= %-5s  rho_max = %s  E R >= %-9s %s' % (mu, rho, lb, name))
print('PASS: %d certificate trees verified' % len(rows))
