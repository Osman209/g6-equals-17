# Release procedure

This file holds the operational rules the build scripts assume. They were learned the
expensive way and are not derivable from the code, so they live here rather than in a
commit message.

## The DOI must be reserved before the archive is built

The DOI is written *inside* the archive, so it has to exist before the archive exists.

1. Open the Zenodo upload form and **reserve** the DOI there.
2. Run `python code/set_doi.py <doi>`, which writes that one DOI into
   `code/build_site.py`, `CITATION.cff`, `.zenodo.json` and `README.md` together.
3. Rebuild the site and the PDFs.
4. Run `python code/audit.py` as the last step.

**Do not use the GitHub-to-Zenodo webhook.** It snapshots the repository *before*
minting the DOI, so the archived copy would carry a dead link, and it appends to
whichever record it happens to be bound to.

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
