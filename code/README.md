# Scripts

Every script carries a `COVERS` line in its header naming the statement it verifies.
`COVERAGE.md` in the repository root holds the full table.

Do not run any verifier with `python -O`. The checks are written as assertions and `-O`
removes them, so an `-O` run can pass on material that fails.

## Standard library only

| script | runs | purpose |
|---|---|---|
| `verify_witness_17.py` | seconds | the seventeen-card witness, [P4] |
| `verify_k7.py` | seconds | the finite $K_7$ lemma, [P1, §3] |
| `verify_histograms.py` | seconds | the thirteen degree histograms, [P1, §6] |
| `verify_eleven_cards.py` | minutes | the eleven-card lemma, degree-three branch, [P2, §2] |
| `verify_degree3_kernels.py` | ~20 min | the second branch of the reduction: 341 maximum-degree-three kernels, none extending, [P3, §2a]. `--witness` also locates the [P4] kernel inside the enumeration; `--enumerate 12` re-derives a profile from scratch |
| `enumerate_eight_maximal.py` | seconds | step 1 of the reduction, [P3, §3] |
| `enumerate_eight_triples.py` | minutes | step 3 of the reduction; a reconstruction, see its header |
| `classify_eight_triples.py` | needs `eight_triples.jsonl` | step 3's canonicalisation |
| `enumerate_eight_cores.py` | seconds | step 4, produces `data/eight_cores.jsonl` |
| `verify_eight_orbits.py` | seconds | the seven orbits, and that every core is a genuine family |
| `verify_cnf_regeneration.py` | seconds | the shipped CNFs are what `build()` produces |
| `make_certificate_manifest.py` | seconds | SHA-256 manifest over the certificate archive |
| `verify_certificate_markers.py` | seconds | presence and consistency of the certificate archive markers, [P3, §6] |
| `verify_core.py` | seconds | a twelve-card family with tau = 5, showing the eleven-card lemma is sharp |
| `verify_p5_arithmetic.py` | seconds | every arithmetic step of [P5] |
| `verify_residual_bound.py` | ~3 min | [P5, Theorem 1] on every small configuration, and the sharpness family |
| `verify_local_graphs.py` | ~4 min; `--full` ~15 min | the local coloured-graph lemmas of [P5] |
| `verify_rainbow_lemmas.py` | under a minute | [P5, Lemmas 10 and 11]; compiles `verify_rainbow.c` with `cc` |
| `verify_anchor_count.py` | ~4 min | [P5, Lemma 13 and Proposition 2], the anchor count for u = 11 |
| `measure_matching_hits.py` | ~1 min | the measurement of [P5, §6.3]; not a proof |

The two certificate scripts read `certificates/`, which is a release asset rather than
repository content. Unpack `g6-certificates-463.zip` into the repository root first.

## Build and release

| script | needs | purpose |
|---|---|---|
| `build_pdfs.sh` | pandoc, pdflatex, lmodern | rebuild `docs/papers/*.pdf` from `papers/*.md` |
| `build_site.py` | none | rebuild `docs/` — the landing page and one abstract page per paper |
| `check_github_math.js` | `npm install katex` | render every math span through KaTeX and inspect the output |
| `audit.py` | none | the release gate. Run it after the LAST edit, not before it |
| `set_doi.py` | none | write one Zenodo DOI into `build_site.py`, `CITATION.cff`, `.zenodo.json` and the README at once |

`RELEASING.md` in the repository root holds the release procedure these scripts assume.

## Needs a C compiler

`fast_enumerate.c` is an optional accelerator for `verify_degree3_kernels.py`. Re-deriving
the c = 6 and c = 0 profiles in pure Python takes hours; in C it takes minutes, and it
writes the same kernel files.

```bash
cc -O2 -o fast_enumerate code/fast_enumerate.c
./fast_enumerate 0 > data/degree3_kernels_c0.json
```

## Needs python-sat

```bash
pip install python-sat
```

| script | purpose |
|---|---|
| `search_sixteen.py` | the encoding, `build()`, and the search over the 463 cores |
| `resolve_sixteen.py` | rerun of any core left UNKNOWN by a budget; never converts a budget exhaustion into UNSAT |
| `export_core_cnf.py` | write one core's CNF in DIMACS form |
| `certify_all.py` | drive the DRAT generation and checking batch |
| `verify_encoding_controls.py` | the positive and negative controls on the encoding |

## Needs drat-trim

Build it from https://github.com/marijnheule/drat-trim and run it directly:

```bash
drat-trim data/cnf/core_007.cnf data/cnf/core_007.drat
```
