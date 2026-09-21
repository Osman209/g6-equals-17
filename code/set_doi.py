#!/usr/bin/env python3
"""Write one Zenodo DOI into every place in the repository that carries it.

COVERS the DOI, which appears in more than one file and must not drift between them.

Write the CONCEPT DOI, not a version DOI. The DOI goes inside the archive, so it must
exist before the archive does; a version DOI is minted only after the version is
published, and would in any case name a version that the next release supersedes. The
concept DOI is fixed and always resolves to the newest version.

    python code/set_doi.py 10.5281/zenodo.22863217

See RELEASING.md for the full procedure and for why the GitHub-to-Zenodo integration is
safe once the concept DOI is what gets archived.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

if len(sys.argv) != 2 or not re.fullmatch(r"10\.5281/zenodo\.\d+", sys.argv[1]):
    raise SystemExit("usage: python code/set_doi.py 10.5281/zenodo.NNNNNNNN")
doi = sys.argv[1]

changed = []

site = ROOT / "code" / "build_site.py"
text = site.read_text(encoding="utf-8")
new = re.sub(r'DOI = "[^"]*"', 'DOI = "%s"' % doi, text, count=1)
if new != text:
    site.write_text(new, encoding="utf-8")
    changed.append(site.name)

cff = ROOT / "CITATION.cff"
text = cff.read_text(encoding="utf-8")
if re.search(r"^doi: ", text, re.M):
    new = re.sub(r"^doi: .*$", "doi: %s" % doi, text, count=1, flags=re.M)
else:
    # anchor to the start of a line: a bare "version: " also matches inside "cff-version: "
    new = re.sub(r"^version: ", "doi: %s\nversion: " % doi, text, count=1, flags=re.M)
if new != text:
    cff.write_text(new, encoding="utf-8")
    changed.append(cff.name)

zen = ROOT / ".zenodo.json"
data = json.loads(zen.read_text(encoding="utf-8"))
if data.get("doi") != doi:
    data["doi"] = doi
    zen.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    changed.append(zen.name)

readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
line = "DOI: [%s](https://doi.org/%s)\n" % (doi, doi)
if "doi.org" in text:
    new = re.sub(r"DOI: \[[^\]]*\]\(https://doi\.org/[^)]*\)\n", line, text, count=1)
else:
    new = text.replace("## Citation\n\n", "## Citation\n\n" + line + "\n", 1)
if new != text:
    readme.write_text(new, encoding="utf-8")
    changed.append(readme.name)

print("DOI set to %s in: %s" % (doi, ", ".join(changed) or "nothing (already current)"))
print("Now rebuild the site: python code/build_site.py")
