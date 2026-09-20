# Verification coverage

One row per measured or machine-decided claim, pointing at the artifact that computes or
certifies it. The column that matters is *what is actually checked*, not which section the
claim appears in: a script that verifies a weaker statement than the paper asserts is the
failure this table exists to catch.

The same rule is used in the author's other reproducibility repositories: file the
generator, not the number. A figure kept without the script or the citation that produces
it is a memory, not a measurement.

| claim | artifact | what is checked |
|---|---|---|
| $K_7$ lemma, all four-input quadruples | `code/verify_k7.py` | 840 minimal inputs, 315 targets, 294,239,817 quadruples, 0 counterexamples; batch method compared against literal enumeration on nine bounded subcases |
| thirteen degree histograms | `code/verify_histograms.py` | exact integer enumeration of the five necessary conditions, plus an independent integer dynamic program |
| eleven-card lemma, degree-three branch | `code/verify_eleven_cards.py` | 5,373 generated instances over 58 profiles, exact triangle-decomposition search with the size-three matching ban, all UNSAT |
| maximal intersecting triple systems on 8 points | `code/enumerate_eight_maximal.py` | 10,144 families covering all eight points, sizes {21:8, 16:336, 14:1680, 12:8120} |
| the seven orbits | `code/verify_eight_orbits.py` | each observed class is rebuilt as a full orbit from one representative; sizes 8, 280, 1680, 56, 560, 2520, 5040 |
| 39,768 triple systems | `code/enumerate_eight_triples.py` | per-representative counts against `data/eight_triples_summary.json`; exits non-zero on any disagreement. **Reconstruction** — see the header of that file |
| 129 symmetry classes | `code/classify_eight_triples.py`, `data/eight_triple_classes.jsonl` | canonical form under the degree-preserving relabellings; multiplicities sum to 39,768 |
| 772 raw, 463 canonical cores | `code/enumerate_eight_cores.py` | completion of each class by forced degree-two symbols and slack, then canonicalisation; output is `data/eight_cores.jsonl` |
| every core is a genuine eight-card family | `code/verify_eight_orbits.py` | eight distinct six-element cards, pairwise intersecting, no three symbols covering |
| the shipped CNF is what the encoder produces | `code/verify_cnf_regeneration.py` | rebuild from `data/eight_cores.jsonl` through `build()`, byte-for-byte comparison |
| the encoding is not contradictory on its own | `code/verify_encoding_controls.py` | with the five-cover clauses dropped, models exist and decode into genuine sixteen-card families; with them restored, none do |
| 463/463 UNSAT | `results/sat_results_cadical195_0.jsonl`, `results/sat_retry*.jsonl` | 460 in the budgeted pass, cores 7, 239, 342 rerun without a budget; no UNKNOWN counted as an exclusion |
| 463/463 DRAT-verified | `results/certificate_summary.jsonl`, `data/cnf/` | one entry per core id 0 to 462, all verified; three CNF/DRAT pairs shipped so the step can be reproduced without a solver |
| DRAT archive integrity | `code/make_certificate_manifest.py`, `code/verify_certificate_markers.py` | SHA-256 over the CNF, DRAT and marker files |
| 17-card witness, $\tau = 6$ | `code/verify_witness_17.py`, `data/witness_17.json` | 17 distinct cards of size 6; 136/136 pairs; all 80,730 five-subsets by two independent methods; degree histogram; an explicit five-cover after each deletion |

## Not covered by any script

These are arguments, not computations, and the table does not pretend otherwise.

| claim | where |
|---|---|
| degree bounds and the no-two-degree-two-symbols lemma | [P1, §2] |
| elimination of the thirteen histograms | [P1, §7] |
| branches A and B of the eleven-card lemma | [P2, §2] |
| the reduction reaches every sixteen-card counterexample | [P3, §1 to §3] |
| each CNF clause family means what it is said to mean | [P3, §4] |

`AUDIT.md` records which of these were checked by reading during the independent pass, and
which parts of the encoding were read but not re-derived.
