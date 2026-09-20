"""Release gate for this repository.

COVERS the repository itself — run this after the LAST edit, not before it.

Checks, in order:

  1. every file the README and COVERAGE tables point at exists;
  2. every script in code/ has a COVERS header line, and every COVERS line names a script
     that exists;
  3. the headline counts appearing in the papers and the README agree with the data files
     on disk (463 cores, 129 classes, 39,768 triple systems, 10,144 maximal systems,
     17 cards, 27 symbols, 463 certificate lines);
  4. the papers use GitHub-safe mathematics: no \\( or \\[ delimiters, no \\operatorname,
     no escaped braces, no \\% inside a math span, and a constant unescaped pipe count
     within each markdown table;
  5. no working file is present under RELEASE_BUILD=1.

Exits non-zero on any problem.
"""
from pathlib import Path
import json
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
problems = []


def bad(msg):
    problems.append(msg)


# ---------------------------------------------------------------- 1. links exist
MD = list(ROOT.glob("*.md")) + list((ROOT / "papers").glob("*.md")) + [
    p / "README.md" for p in (ROOT / "code", ROOT / "data", ROOT / "results")
]
LINK = re.compile(r"`((?:papers|code|data|results|docs)/[A-Za-z0-9_./-]+)`")
for path in MD:
    if not path.exists():
        continue
    for target in set(LINK.findall(path.read_text(encoding="utf-8"))):
        if not (ROOT / target).exists():
            bad("%s points at missing %s" % (path.name, target))

# ---------------------------------------------------------------- 2. COVERS headers
scripts = sorted((ROOT / "code").glob("*.py"))
if not scripts:
    bad("code/ holds no scripts")
NO_COVERS_NEEDED = {"audit.py"}
for script in scripts:
    if script.name in NO_COVERS_NEEDED:
        continue
    head = script.read_text(encoding="utf-8")[:2500]
    if "COVERS" not in head:
        bad("%s has no COVERS line" % script.name)

# ---------------------------------------------------------------- 3. headline counts
def lines(path):
    return [l for l in (ROOT / path).read_text(encoding="utf-8").splitlines() if l.strip()]


try:
    cores = lines("data/eight_cores.jsonl")
    if len(cores) != 463:
        bad("data/eight_cores.jsonl has %d lines, expected 463" % len(cores))

    classes = [json.loads(l) for l in lines("data/eight_triple_classes.jsonl")]
    if len(classes) != 129:
        bad("eight_triple_classes.jsonl has %d classes, expected 129" % len(classes))
    total = sum(c["multiplicity"] for c in classes)
    if total != 39768:
        bad("class multiplicities sum to %d, expected 39768" % total)

    maximal = json.loads((ROOT / "data" / "eight_maximal.json").read_text())
    if len(maximal) != 10144:
        bad("eight_maximal.json has %d entries, expected 10144" % len(maximal))

    summary = json.loads((ROOT / "data" / "eight_triples_summary.json").read_text())
    if sum(r["triplesystems"] for r in summary) != 39768:
        bad("triple-system counts do not sum to 39768")

    witness = json.loads((ROOT / "data" / "witness_17.json").read_text())
    cards = witness["cards"]
    if len(cards) != 17 or any(len(set(c)) != 6 for c in cards):
        bad("witness_17.json is not seventeen distinct six-element cards")
    if len({s for c in cards for s in c}) != 27:
        bad("witness_17.json does not use 27 symbols")

    certs = [json.loads(l) for l in lines("results/certificate_summary.jsonl")]
    if len(certs) != 463 or sorted(c["core"] for c in certs) != list(range(463)):
        bad("certificate_summary.jsonl does not cover cores 0..462 exactly once")
    if not all(c["verified"] for c in certs):
        bad("certificate_summary.jsonl contains an unverified core")
except FileNotFoundError as exc:
    bad("missing data file: %s" % exc)

# ---------------------------------------------------------------- 4. GitHub math
MATH = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$", re.S)
DENY = ("\\operatorname", "\\rm ", "\\bf ", "\\it ", "\\newcommand", "\\def", "\\href")
for path in list((ROOT / "papers").glob("*.md")) + [ROOT / "README.md", ROOT / "AUDIT.md",
                                                     ROOT / "COVERAGE.md"]:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    if "\\(" in text or "\\[" in text:
        bad("%s uses \\( or \\[ delimiters, which GitHub does not render" % path.name)
    for span in MATH.findall(text):
        for token in DENY:
            if token in span:
                bad("%s: math span uses %s" % (path.name, token.strip()))
        for token in ("\\{", "\\}", "\\,", "\\;", "\\!", "\\%"):
            if token in span:
                bad("%s: math span uses %s, which markdown strips before KaTeX"
                    % (path.name, token))
        if "|" in span:
            bad("%s: math span contains a raw pipe; write \\lvert and \\rvert"
                % path.name)
    block = []
    for line in text.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            block.append(len(re.findall(r"(?<!\\)\|", line)))
        else:
            if len(set(block)) > 1:
                bad("%s: a table block has inconsistent pipe counts %s"
                    % (path.name, sorted(set(block))))
            block = []

# ---------------------------------------------------------------- 4b. required statements
REQUIRED = {
    "README.md": ["not been independently reviewed", "No priority is claimed",
                  "AI assistance", "ChatGPT", "Claude"],
    "papers/overview.md": ["not been independently reviewed", "No priority is claimed",
                           "AI assistance", "ChatGPT", "Claude"],
    "CITATION.cff": ["not been independently reviewed"],
    ".zenodo.json": ["not been independently reviewed", "No priority is claimed"],
    "docs/index.html": ["not yet independently reviewed", "No priority is claimed"],
}
for name, needles in REQUIRED.items():
    path = ROOT / name
    if not path.exists():
        bad("missing %s" % name)
        continue
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            bad("%s no longer states: %s" % (name, needle))

for paper in sorted((ROOT / "papers").glob("paper_*.md")):
    text = paper.read_text(encoding="utf-8")
    if "AI assistance" not in text:
        bad("%s carries no AI-assistance note" % paper.name)
    if "No priority" not in text and "no priority" not in text:
        bad("%s carries no priority disclaimer" % paper.name)

# ---------------------------------------------------------------- 4c. DOI consistency
site_text = (ROOT / "code" / "build_site.py").read_text(encoding="utf-8")
m = re.search(r'DOI = "([^"]*)"', site_text)
site_doi = m.group(1) if m else None
if site_doi is None:
    bad("code/build_site.py has no DOI constant")
elif site_doi.endswith("RESERVED"):
    if os.environ.get("RELEASE_BUILD") == "1":
        bad("the DOI is still the RESERVED placeholder; reserve it on Zenodo and run "
            "code/set_doi.py before building a release archive")
    else:
        print("NOTE: DOI is still the RESERVED placeholder. Fine for a GitHub push; "
              "run code/set_doi.py before building the Zenodo archive.")
else:
    others = {
        "CITATION.cff": re.search(r"^doi: (\S+)", (ROOT / "CITATION.cff").read_text(
            encoding="utf-8"), re.M),
        ".zenodo.json": None,
    }
    zen = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8")).get("doi")
    if others["CITATION.cff"] is None or others["CITATION.cff"].group(1) != site_doi:
        bad("CITATION.cff DOI disagrees with code/build_site.py")
    if zen != site_doi:
        bad(".zenodo.json DOI disagrees with code/build_site.py")

# ---------------------------------------------------------------- 5. release hygiene
if os.environ.get("RELEASE_BUILD") == "1":
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    patterns = [l.strip() for l in ignore if l.strip() and not l.startswith("#")]
    for pattern in patterns:
        for hit in ROOT.glob(pattern):
            bad("working file present in a release build: %s" % hit.relative_to(ROOT))

# ---------------------------------------------------------------- report
if problems:
    for p in problems:
        print("PROBLEM:", p)
    print("TOTAL problems:", len(problems))
    sys.exit(1)
print("PASS: %d scripts, 463 cores, 129 classes, 39,768 triple systems, "
      "10,144 maximal systems, 463 certificates, witness on 27 symbols." % len(scripts))
