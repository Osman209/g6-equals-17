# Independent re-verification log

This file records what was actually re-run against this material on a clean machine, by
someone other than the person who produced it, and — just as importantly — what was not.
It is not a second proof. It is a statement of which parts a reader can stop worrying
about and which parts still need reading rather than running.

Two passes are recorded. Sections 1 to 3 are the first pass; section 4 is a second pass
on a different operating system, which widened three of the checks from a sample to the
whole archive.

First pass: 20 September 2026. Environment: Linux, Python 3.12,
`python-sat` 1.9.dev15 (CaDiCaL 1.9.5 backend), `drat-trim` built from source at
`github.com/marijnheule/drat-trim` and checked against its own bundled examples before
use.

---

## 1. What was re-run and passed

### 1.1 The finite $K_7$ lemma — [P1, §3], [P2, §2]

`code/verify_k7.py` was run from scratch.

```text
status PASS, minimal_input_covers 840, output_covers 315,
representative_types 3, quadruples_certified 294,239,817, counterexamples 0
```

Separate controls were written against the batch method, since a search that always
returns "no counterexample" is indistinguishable from a search that never looks. The
script's own self-check compares the batch certification against literal enumeration on
nine bounded subcases; that comparison passed.

### 1.2 The thirteen histograms — [P1, §6]

`code/verify_histograms.py` was run, returning PASS with thirteen rows. The enumeration
was then re-derived from the stated conditions in independent code, which produced the
same thirteen rows in the same order.

### 1.3 The eleven-card lemma, degree-three branch — [P2, §2]

`code/verify_eleven_cards.py` was run in full: 5,373 instances across 58 non-empty
profiles, all UNSAT, matching the recorded per-profile counts line for line.

Four controls were run against the search engine itself, because UNSAT on every instance
is exactly what a broken solver also produces:

| input | expected | observed |
|---|---|---|
| one triangle | SAT | SAT |
| two disjoint triangles (allowed) | SAT | SAT |
| three mutually disjoint triangles (the forbidden configuration) | UNSAT | UNSAT |
| three triangles through one shared card | SAT | SAT |

The third row is the one that matters: it shows the matching-of-size-three ban is
actually firing, rather than the search failing for an unrelated reason.

The simplest profile, $(0,0,0,11)$, was also checked by hand. It should count the
partitions of 11 into parts of size at least 2, which is 14; the script reports 14.

### 1.4 The reduction to 463 cores — [P3, §3]

Every step of the chain was re-run.

| step | result | recorded |
|---|---|---|
| maximal intersecting triple systems on 8 points | 10,144, sizes {21:8, 16:336, 14:1680, 12:8120} | 10,144 |
| orbits under the symmetric group | 7 orbits, sizes 8, 280, 1680, 56, 560, 2520, 5040 | same |
| triple systems | 28329, 4932, 1526, 3858, 156, 535, 432 — total 39,768 | same |
| symmetry classes | 129, multiplicities summing to 39,768 | same |
| raw completions, canonical cores | 772 raw, 463 canonical | same |

The final step was re-run from `data/eight_triple_classes.jsonl` and its output compared
against `data/eight_cores.jsonl`. The two agree exactly; the only byte-level difference is
that the shipped file has CRLF line endings.

`code/verify_eight_orbits.py` additionally confirms that each of the 463 cores really is
eight distinct six-element cards, pairwise intersecting, with no three symbols covering
all eight.

**A reconstruction was needed here.** The archive copy of the step-3 enumerator, and its
5 MB output, were both unrecoverable — the files exist but are empty. That step was
rewritten from the definition and from the outputs on either side of it
(`code/enumerate_eight_triples.py`). It reproduces all seven recorded counts and their
total exactly. It is a reconstruction, not the original script, and it is labelled as one
in its own header.

### 1.5 The CNF is the one the code produces — [P3, §4]

This is the link that makes the certificates mean anything, and it had not been checked
before this pass.

`code/verify_cnf_regeneration.py` rebuilds each shipped CNF directly from
`data/eight_cores.jsonl` through the audited `build()` and compares byte for byte.

| core | variables | clauses | result |
|---|---|---|---|
| 7 | 40,583 | 210,333 | byte-identical |
| 239 | 38,280 | 199,136 | byte-identical |
| 342 | 36,922 | 190,406 | byte-identical |

The variable and clause counts are the ones quoted in [P3, §5].

### 1.6 DRAT certification — [P3, §6]

`drat-trim` was built from source, checked against its bundled examples, and then run on
the three shipped pairs.

| core | DRAT bytes | result | time (s) |
|---|---|---|---|
| 7 | 10,110,384 | s VERIFIED | 9.0 |
| 239 | 5,858,286 | s VERIFIED | 3.9 |
| 342 | 7,661,933 | s VERIFIED | 10.8 |

`results/certificate_summary.jsonl` was checked for completeness: 463 entries, covering
core ids 0 to 462 with no gap and no repeat, every one marked verified.

The SAT records were cross-read against the retry chain.
`results/sat_results_cadical195_0.jsonl` holds 463 rows: 460 UNSAT and 3 UNKNOWN, the
three being cores 7, 239 and 342. Those are precisely the three reported as hard, and
precisely the three reran without a budget. The retry files resolve them to UNSAT. No
UNKNOWN was ever counted as an exclusion.

### 1.7 Controls on the encoding — new in this pass

`code/verify_encoding_controls.py`. On a sample of forty cores, with the clauses
forbidding a five-cover dropped and everything else kept:

- 18 of 40 became satisfiable, and every model decoded into a family that passes an
  independent re-check — sixteen distinct cards, six symbols each, all 120 pairs meeting;
- 22 of 40 remained unsatisfiable on the structural constraints alone;
- with the five-cover clauses restored, all 40 were unsatisfiable.

The first line is the important one. It shows the encoding is not contradictory on its
own: for nearly half the cores a genuine sixteen-card intersecting family with the right
degrees does exist, and what removes it is the transversal condition and nothing else. Had
every core come back unsatisfiable in control 1, the 463 UNSAT answers would have carried
no information.

### 1.8 The seventeen-card witness — [P4]

`code/verify_witness_17.py` was run.

```text
cards 17, symbols 27, pair intersections 136/136,
five-subsets checked 80,730, five-covers found 0,
degree histogram {2:2, 3:4, 4:19, 5:2}, deletion checks 17/17
PASS: 17-card witness has tau = 6
```

The witness was also checked independently of the shipped verifier, in code written from
the table in [P4, §1] alone, with the same outcome. The two witness files distributed with
this project — `data/witness_17.json` and the earlier standalone package — carry the same
seventeen cards.

---

## 2. What was not settled by this pass

These are open obligations, not suspicions. Nothing below is a defect that was found; each
is a claim that running things cannot decide.

**The reduction is complete.** That every hypothetical sixteen-card counterexample is
represented by one of the 463 cores is a mathematical claim about [P3, §1 to §3]. The
counts were reproduced, and each core was checked to be a genuine object, but "these 463
are all of them" is an argument in the text and in the four enumeration scripts. It has to
be read.

**The encoding is faithful.** The controls of §1.7 rule out the cheap failure — an
encoding contradictory on its own — and the decoded families show that the structural
clauses describe real objects. They do not prove that every clause family means what
[P3, §4] says it means. In particular the following were read but not independently
re-derived: the antichain and support-containment clauses, the exact form of the
five-cover clauses over the pre-computed four- and five-element covering sets, and the
justification that the lexicographic chain breaks only genuine symmetries. On the last of
those: the eight positions index the new cards, four holding $x$ and four holding $y$, and
those are interchangeable within each block with the two blocks exchangeable, so the chain
appears sound; that reading was checked against the decoder in `audit()` and is consistent
with it, but it is a reading.

**The hand eliminations of [P1, §7].** Thirteen incidence arguments, worked through on
paper during this pass and found to hold, but not machine-checked. They are also no longer
load-bearing: [P2] reaches the same conclusion by a different route.

**Branches A and B of [P2, §2].** Hand arguments on top of the $K_7$ lemma. Checked by
reading.

**The literature question.** Whether the value is already known was not investigated at
all. See the overview, §6.

---

## 3. Summary

| layer | status after this pass |
|---|---|
| 17-card upper bound | independently reproduced; nothing but arithmetic is trusted |
| $K_7$ lemma | independently re-run, with controls |
| 11-card lemma, degree-3 branch | independently re-run, with controls |
| reduction counts, all five steps | independently reproduced, one step from a reconstruction |
| CNF matches the code | newly established, byte-identical |
| 463 unsatisfiability results | independently certified on three, summary complete on all |
| encoding is non-trivial | newly established by control |
| reduction is complete | open, to be read |
| encoding is faithful | partly open, to be read |

The computational layer of the lower bound came through this pass without a discrepancy.
The obligations that remain are the two that certificates cannot discharge, and they are
the two the papers already name.

---

## 4. Second pass — 21 September 2026

Environment: Windows 11, Python 3.11.9, `python-sat` 1.9.dev15 (CaDiCaL 1.9.5 backend),
`drat-trim` built from source at commit `2e3b2dc` with the two Windows portability fixes
recorded in §4.5. A different operating system and a different Python from the first
pass; the same data.

This pass was carried out with the assistance of an AI agent (Claude, Anthropic) driving
the scripts and writing the cross-checks. Every number below is the output of a command,
not a summary of one.

### 4.1 The standard-library verifiers — all re-run

`verify_witness_17.py`, `verify_k7.py`, `verify_histograms.py`, `verify_eleven_cards.py`,
`enumerate_eight_maximal.py`, `enumerate_eight_triples.py`, `enumerate_eight_cores.py`,
`verify_eight_orbits.py`, `verify_cnf_regeneration.py` and `verify_encoding_controls.py`
were run. All returned PASS, and every reported count matched §1 line for line: 294,239,817
quadruples with 0 counterexamples; thirteen histograms; 5,373 eleven-card instances over
58 non-empty profiles, all UNSAT; 10,144 maximal systems; 39,768 triple systems; 772 raw
and 463 canonical cores; seven orbits; 18/22/40 on the encoding controls.

Three of those numbers were also recomputed without using the repository's own scripts:
the per-profile instance counts in the eleven-card log sum to 5,373; the profile
$(0,0,0,11)$ should count the partitions of 11 into parts of size at least 2, which an
independent implementation confirms is 14, as the script reports; and the records in
`results/` hold 463 rows with ids 0 to 462, no gap and no repeat, 460 UNSAT and 3 UNKNOWN,
the three being cores 7, 239 and 342, each resolved to UNSAT by the retry chain.

### 4.2 CNF regeneration widened from 3 cores to 463

§1.5 rebuilt the three CNFs shipped in `data/cnf/`. This pass pointed the same `build()`
at the full release archive and rebuilt every one.

| | |
|---|---|
| archived CNFs regenerated | 463 |
| byte-identical | **463** |
| differing | 0 |
| missing from the archive | 0 |
| metadata disagreeing with `certificate_summary.jsonl` | 0 |

The variable count, clause count, symbol count and the two covering-set counts were
compared per core as well, not only the bytes.

### 4.3 The SAT sweep widened from 3 cores to 463

The full budgeted search was re-run and compared row by row against the shipped
`results/sat_results_cadical195_0.jsonl`.

| | this pass | recorded |
|---|---|---|
| rows | 463 | 463 |
| UNSAT | 460 | 460 |
| UNKNOWN | 3 | 3 |
| which cores are UNKNOWN | 7, 239, 342 | 7, 239, 342 |
| status disagreements | **none** | **none** |

`variables`, `clauses`, `symbols`, `covers4` and `covers5` agreed on all 463 cores.
No instance came back SAT in any run. The three budgeted-out cores were then rerun with
`--budget 0` and returned UNSAT in 11.5, 15.5 and 18.0 seconds.

### 4.4 DRAT certification widened from 3 proofs to 463

§1.6 verified the three shipped pairs. This pass verified the whole archive.

| | |
|---|---|
| certificates checked | 463 |
| `s VERIFIED` | **463** |
| `s NOT VERIFIED` | 0 |
| proof bytes read by the checker | 614,975,086 |
| proof bytes present on disk | 614,975,086 |
| total checking time | 5.4 minutes, slowest proof 9.2 s |

The two byte counts are reported together deliberately. A proof checker that stops early
still prints a verdict, so "every byte was consumed" is part of the result and not a
footnote — see §4.5.

The archive markers were audited independently of the repository's own script: 463
`.verified` files with ids exactly 0 to 462 and none malformed, 463 `verify.txt` files
containing `s VERIFIED`, all four artefacts present for every core, and no DRAT file
small enough to be suspicious.

### 4.5 Two Windows defects in `drat-trim`, and what they would have cost

Neither is a defect in this project. Both matter to anyone checking it on Windows.

`getc_unlocked` is POSIX and absent on Windows, so the build fails outright. That one is
loud and harmless.

The second is not. `drat-trim.c` opens the proof file in text mode, where Windows treats
a `0x1A` byte inside binary proof data as end-of-file. Parsing then stops early and the
checker prints `s NOT VERIFIED` with no warning. On an unpatched build, `core_003.drat`
had its first `0x1A` at byte 644 and 645 of its 37,410 bytes were read before the checker
gave up. **A reviewer following the README on Windows would have seen this archive fail.**
Opening the proof file in binary mode fixes it; the counts in §4.4 are from the fixed
build. `README.md` now carries both fixes.

### 4.6 Controls on the checker

A checker that answers `VERIFIED` to everything proves nothing, so the patched binary was
tested against bad input before its verdicts were used.

| input | expected | observed |
|---|---|---|
| the ten bundled `drat-trim` examples | VERIFIED | VERIFIED |
| an empty proof | NOT VERIFIED | NOT VERIFIED |
| a proof from a different instance | NOT VERIFIED | NOT VERIFIED |
| a bare empty-clause claim | NOT VERIFIED | NOT VERIFIED |

A valid proof with its last line removed still verified. That is expected: backward
checking can reach a conflict before the final line, so the truncation is not always
load-bearing.

### 4.7 The literature question — partly addressed, not closed

§2 recorded that this was not investigated at all. It has now been looked at, and the
distinction the overview draws in §6 holds up against the primary sources.

The known exact values are $g(3) = 6$, $g(4) = 9$ and $g(5) = 13$, the last due to Barát
[arXiv:2011.04444]. The strongest published general lower bound, $g(r) \ge ((41-\sqrt{19})/12
- o(1))r \approx 3.053r$ [arXiv:2606.24878, June 2026], gives only $g(6) \ge 14$.

The eighteen-edge construction in Barát §7 is a value of a **different** function: the
minimum inside a projective plane, there computed in $PG(2,5)$ on 31 points. It bounds
$g(6) \le 18$ and is not a determination of $g(6)$. No source was found that determines
$g(6)$.

This is a search, not a literature review. It cannot establish that nothing was missed,
and the obligation stated in the overview stands.

### 4.8 What this pass did not touch

The two open obligations are untouched and remain exactly as §2 states them: that the
reduction reaches every sixteen-card counterexample, and that each CNF clause family
means what [P3, §4] says it means. Both are arguments to be read. Widening a certificate
check from three instances to 463 does not move either one.

### 4.9 Summary after the second pass

| layer | status |
|---|---|
| 17-card upper bound | reproduced on a second platform |
| $K_7$ lemma | re-run |
| 11-card lemma, degree-3 branch | re-run; two counts re-derived independently |
| reduction counts, all five steps | reproduced |
| CNF matches the code | **463 of 463**, byte-identical |
| SAT results | **463 of 463** reproduced, exact agreement |
| DRAT certification | **463 of 463** verified, every byte consumed |
| encoding is non-trivial | control reproduced |
| literature | searched; no determination of $g(6)$ found |
| reduction is complete | open, to be read |
| encoding is faithful | partly open, to be read |

The computational layer came through a second time, on a different platform, without a
discrepancy. What remains open is what was open before, and it is what the papers say.
