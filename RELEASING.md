# Release procedure

This file holds the operational rules the build scripts assume. They were learned the
expensive way and are not derivable from the code, so they live here rather than in a
commit message.

## The DOI written into the archive is the concept DOI

The DOI is written *inside* the archive, so it has to exist before the archive exists.
A version DOI does not: Zenodo mints it only once the version is published. That is the
whole difficulty, and the concept DOI is the way out of it.

**Concept DOI: `10.5281/zenodo.22863217`.** It is fixed, it exists already, and it
always resolves to the newest version. It is what `code/set_doi.py` writes and what
`CITATION.cff` carries, so a citation never points at a superseded version.

| DOI | points at |
|---|---|
| `10.5281/zenodo.22863217` | **concept** — always the latest version |
| `10.5281/zenodo.22863218` | version 1.0.0, permanently |
| `10.5281/zenodo.22863582` | version 1.0.1, permanently |

Do not write a version DOI into the archive. It is wrong the moment the next version
exists, and under the GitHub release integration it cannot be known in advance anyway.

## Releasing through the GitHub-to-Zenodo integration

The repository is synced, so publishing a GitHub release creates the next Zenodo
version automatically.

1. Run `python code/set_doi.py 10.5281/zenodo.22863217` if the concept DOI is not
   already in place.
2. Bump `version` and `date-released` in `CITATION.cff` and `.zenodo.json`.
3. Rebuild the site and the PDFs.
4. Run `python code/audit.py` as the last step, then tag and publish the release.

The integration archives **the source tree of the tag only**. Release assets are not
copied, so `g6-certificates-463.zip` stays on GitHub and never reaches Zenodo. The
Zenodo description says so, and the three hardest CNF/DRAT pairs in `data/cnf/` keep
the certification step reproducible from the deposit alone. Upload the archive to the
Zenodo record by hand if a deposit complete on its own is ever wanted.

An earlier version of this file said to avoid the integration entirely, because it
snapshots the repository *before* minting the version DOI and so bakes in a dead link.
Writing the concept DOI removes that failure: the link inside the archive does not name
a version and cannot go stale. The other caution still holds — the integration appends
to whichever record it is bound to, so check that a release landed under concept record
22863217 and not a new one.

`audit.py` only warns about the `RESERVED` placeholder on an ordinary push, and
refuses it under `RELEASE_BUILD=1`. Set that variable for a real release so the
placeholder cannot escape:

```bash
RELEASE_BUILD=1 python code/audit.py
```

## The site text is a separate copy

`code/build_site.py` holds the site's own copy of every title, subtitle and abstract.
Editing a paper does **not** change the site text. Change it in both places.

## The maths checker must be given files

`code/check_github_math.js` refuses to run with no files and exits 2, because a checker
that can silently pass by being invoked wrongly is worse than no checker.

```bash
node code/check_github_math.js papers/*.md README.md
```

## The certificate archive is a release asset

`certificates/` is not repository content. The full 463 CNF and DRAT pairs ship as
`g6-certificates-463.zip` on the release, about 534 MB. Three representative pairs —
the three hardest instances — are in `data/cnf/` so the certification step can be
reproduced without downloading the archive.

## Order of operations

```text
reserve DOI  ->  set_doi.py  ->  build_pdfs.sh  ->  build_site.py
             ->  check_github_math.js  ->  audit.py  ->  tag  ->  upload archive
```

`audit.py` is the gate. Run it after the last edit, not before it.
