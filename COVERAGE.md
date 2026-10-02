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
| the three maximum-degree-three profiles, and 341 kernels | `code/verify_degree3_kernels.py`, `data/degree3_kernels_c*.json` | the card types (5,1,0) and (6,0,0) and c in {0,6,12} are re-derived; every triangle decomposition of each of the three models M = K12+E-F is enumerated, filtered to tau(G)=5, and reduced under Aut(M) |
| no maximum-degree-three kernel extends | same | the extension criterion of [P3, Prop 2] solved exactly on all 341, under the degree caps; zero admit four covers |
| the [P4] witness kernel is one of them | `code/verify_degree3_kernels.py --witness` | the twelve-card kernel of the seventeen-card witness is located inside the enumeration, as representative #0 of profile (6,20) |
| the same enumeration, in C | `code/fast_enumerate.c` | re-derives the identical kernel files in minutes rather than hours |
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
| [P5, Theorem 1] on small configurations | `code/verify_residual_bound.py` | every irredundant covering of the pairs of a q-set by 2- and 3-blocks for q <= 6 (7,124,433 at q = 6), and the low-degree ones for q = 7, 8, 9; no violation of 4 tau <= q + r + 3; the sharpness family for n = 3 to 11 |
| [P5] local lemmas | `code/verify_local_graphs.py --full` | every multicoloured local graph up to u = 12 (Lemmas 1, 3 and sigma <= 6), up to u = 13 with d <= 5 under both capacities (Lemma 5), the d = 0 structure up to u = 9, K7 not splitting into four, and the u = 13, d = 5 step of §4.2 |
| [P5, Lemma 13 and Proposition 2] | `code/verify_anchor_count.py` | every multicoloured local graph on 11 vertices for d = 1 to 5 under both capacities: at most 12 - S open pairs and anchor value at least 16 when S >= 11, for d <= 4; at d = 5 both fail, which is the open case of §4.5 |
| [P5, Lemmas 10 and 11] | `code/verify_rainbow_lemmas.py`, `code/verify_rainbow.c` | exhaustive on 8, 9 and 10 vertices; the obstructions are the same 12 and 192 configurations at every size |
| [P5] arithmetic | `code/verify_p5_arithmetic.py` | the five cases, the exclusion arithmetic of §4, the swap-lemma counts for d = 0 and d = 1, the cases left at r = 15 to 21, the dense-remainder corollary over integer tuples, the closed form of §5 against the exact minimum at r = 3200, and the constant of arXiv:2606.24878 |
| [P6, §3 and §5] algebra | `code/verify_rainbow_constant.py` | the budget identity of Lemma 9, K = 2(N - 2M), the allocation terms and bound (5.1), the root argument for u <= L, convexity of c, the rearrangement of Lemma 12; symbolic, with sympy |
| [P6, Theorem 1] certified minimum | `code/verify_snd_intersection.py` | branch and bound with exact Fraction interval arithmetic over 1 <= gamma <= 2, c(gamma) <= lambda <= 0.08864, 0 <= sigma <= 0.4432, pruned by constraints (A)-(G): the objective is at least 0.1108 everywhere; does not close at 0.11081, above the numerical minimum 0.110802 |
| [P6, §6] incidence lemmas, finite sanity check | `code/audit_snd_finite_systems.py` | 1,200 random intersecting uniform dual block systems, 300 with a prescribed strong group: Lemmas 13-15, (6.2)-(6.10) and the SND capacities. Needs scipy. A check, not a proof |
| earlier probabilistic route (not in [P5]; for a separate note) | `code/measure_matching_hits.py` | worst probability that a random perfect matching meets four edge covers; exhaustive at u = 8 and 10, searched at 12, 16, 24. A measurement, not a proof |
| earlier centre route (not in [P5]; for a separate note): one-centre reward bounds | `code/verify_one_center_certificates.py` with `code/one_center_certificate.py` | seventeen box certificates over the whole bulk cube, exact rational dual checks; reads the release asset `certificates/one_centre/` |
| earlier centre route (not in [P5]): the centre model | `code/verify_centre_model.py` | the reward formula, the two fixed-bulk LP optima with dual certificates, and random tests of the splitting and absorption steps proved in the text |
| earlier centre route (not in [P5]): 3.0588 in the one-centre model | `code/coefficient_from_certificates.py` | a numerical grid evaluation from the certified bounds; not a proof, and only inside the one-centre model |
| g(7) by kernel plus extension | `code/gr_upper.py`, `code/gr7_select.py` | the construction that gives 4r-7 for r = 4, 5, 6; at r = 7 the SAT selection decides each of the 38 kernels with tau = 6 |

## Not covered by any script

These are arguments, not computations, and the table does not pretend otherwise.

| claim | where |
|---|---|
| degree bounds and the no-two-degree-two-symbols lemma | [P1, §2] |
| elimination of the thirteen histograms | [P1, §7] |
| branches A and B of the eleven-card lemma | [P2, §2] |
| the reduction reaches every sixteen-card counterexample | [P3, §1, §2, §2a, §3] |
| each CNF clause family means what it is said to mean | [P3, §4] |
| [P5]: the capacity inequalities (2.1), (2.2), the pointwise capacity (Lemma 4), $M \le S$, the swap lemma (Lemma 8), and the augmentation arguments of Lemmas 6, 9 and 12 | [P5, §2 to §4] |

`AUDIT.md` records which of these were checked by reading during the independent pass, and
which parts of the encoding were read but not re-derived.
