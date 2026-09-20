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
| `enumerate_eight_maximal.py` | seconds | step 1 of the reduction, [P3, §3] |
| `enumerate_eight_triples.py` | minutes | step 3 of the reduction; a reconstruction, see its header |
| `classify_eight_triples.py` | needs `eight_triples.jsonl` | step 3's canonicalisation |
| `enumerate_eight_cores.py` | seconds | step 4, produces `data/eight_cores.jsonl` |
| `verify_eight_orbits.py` | seconds | the seven orbits, and that every core is a genuine family |
| `verify_cnf_regeneration.py` | seconds | the shipped CNFs are what `build()` produces |
| `make_certificate_manifest.py` | seconds | SHA-256 manifest over the certificate archive |
| `verify_core.py` | seconds | a twelve-card family with tau = 5, showing the eleven-card lemma is sharp |

## Build

| script | needs | purpose |
|---|---|---|
| `build_pdfs.sh` | pandoc, pdflatex, lmodern | rebuild `docs/papers/*.pdf` from `papers/*.md` |
| `build_site.py` | none | rebuild `docs/` — the landing page and one abstract page per paper |
| `check_github_math.js` | `npm install katex` | render every math span through KaTeX and inspect the output |
| `audit.py` | none | the release gate. Run it after the LAST edit, not before it |
| `set_doi.py` | none | write one Zenodo DOI into `build_site.py`, `CITATION.cff`, `.zenodo.json` and the README at once |

The DOI must be **reserved on the Zenodo upload form before the archive is built**, because
it is written inside the archive. Do not use the GitHub-to-Zenodo webhook: it snapshots the
repository before minting the DOI, so the archived copy would carry a dead link, and it
appends to whichever record it is bound to. `audit.py` only warns about the `RESERVED`
placeholder for an ordinary push, and refuses it under `RELEASE_BUILD=1`.

`build_site.py` holds the site's own copy of every title, subtitle and abstract. Editing a
paper does not change the site text; change it there as well.

`check_github_math.js` refuses to run with no files and exits 2, because a checker that
can silently pass by being invoked wrongly is worse than no checker.
| `verify_certificate_markers.py` | seconds | certificate archive markers |

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
