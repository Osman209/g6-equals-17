# The six-card cover problem

*The case r = 6 of the Erdős–Lovász cover number problem.*

A reproducible, computer-assisted determination of $g(6)$, the smallest number of blocks
in a pairwise intersecting 6-uniform family whose transversal number is 6.

$$g(6) = 17 .$$

This is the case $r = 6$ of a question Erdős and Lovász asked in 1974, in the paper that
introduced the local lemma: what is the minimum number of edges $g(r)$ in an $r$-uniform
intersecting hypergraph with cover number $r$? Erdős described it as one of his three
favourite combinatorial problems and offered \$500 for a linear upper bound, which Kahn
proved in 1994. The exact values known are $g(3) = 6$, $g(4) = 9$ and $g(5) = 13$, the
last due to Barát [arXiv:2011.04444]; the strongest published general lower bound,
$g(r) \ge ((41-\sqrt{19})/12 - o(1))r$ [arXiv:2606.24878], gives $g(6) \ge 14$. See
[section 6 of the overview](papers/overview.md) for what that does and does not settle about
the value determined here.

A fifth paper, [P5], turns to every $r$. It gives proposed proofs that
$g(r) \ge 3r-3$ for every $r$, answering the question in [arXiv:2606.24878] of whether the
residual constant $+4$ can be $+3$, and that $g(r) \ge 3r-2$ for every $r \ge 16$. It
also gives a proposed proof of a new asymptotic lower bound for the Erdős–Lovász problem,
$\liminf g(r)/r \ge 3+5(133-2\sqrt{3185})/1414 = 3.0711\ldots$, above the constant
$3.0534$ of the same preprint. These proofs are unreviewed; their finite steps are checked
by the scripts listed in [P5, §7].

> **Status.** Research draft. The upper bound is an explicit witness anyone can check in
> seconds. The lower bound is computer-assisted and **has not been independently reviewed
> by a human or a proof assistant**; two obligations are open by construction and are named
> below. No priority is claimed. AI tools were used throughout the work and its review.

**Start with [`papers/overview.md`](papers/overview.md).**

---

## The question

Every card has six symbols; every two cards share a symbol. A *transversal* is a set of
symbols meeting every card, and $\tau$ is the smallest size of one. The six symbols of any
single card already meet every other card, so $\tau \le 6$ always, and $\tau = 6$ is the
statement that no five symbols cover everything.

$$g(6) = \min \lbrace \lvert F \rvert : F \text{ is 6-uniform, pairwise intersecting, } \tau(F) = 6 \rbrace .$$

## The chain

| stage | result | consequence |
|---|---|---|
| at most 15 cards | excluded, by two independent routes | $g(6) \ge 16$ |
| exactly 16 cards | two branches: 341 maximum-degree-three kernels, none extending; and 463/463 canonical instances UNSAT, all DRAT-verified | $g(6) \ge 17$ |
| exactly 17 cards | explicit family; 136/136 pairs meet; 0 of 80,730 five-sets cover | $g(6) \le 17$ |

## The papers

| tag | file | contents |
|---|---|---|
| [P1] | [`papers/paper_1_fifteen_cards_histogram_route.md`](papers/paper_1_fifteen_cards_histogram_route.md) | fifteen cards, via a weighted inequality and thirteen degree histograms |
| [P2] | [`papers/paper_2_eleven_card_lemma.md`](papers/paper_2_eleven_card_lemma.md) | every eleven-card family has a four-cover; fifteen cards in two lines |
| [P3] | [`papers/paper_3_sixteen_cards.md`](papers/paper_3_sixteen_cards.md) | sixteen cards, via 463 cores, SAT, and DRAT certificates |
| [P4] | [`papers/paper_4_seventeen_card_witness.md`](papers/paper_4_seventeen_card_witness.md) | the explicit seventeen-card family |
| [P5] | [`papers/paper_5_every_r.md`](papers/paper_5_every_r.md) | every $r$: $g(r) \ge 3r-3$, $3r-2$ for $r \ge 16$, and $\liminf g(r)/r \ge 3.0711$ (proposed, not reviewed) |

The papers are cited as [P1] to [P5]. A bare bracketed number inside a paper is an
entry in that paper's own reference list. Each paper numbers its own results from 1.

## What is trusted, and what is not

The two bounds are not evidence of the same kind, and the repository is organised around
that difference.

The upper bound is a witness. Seventeen sets, 136 pairs, 80,730 subsets, standard library
only. Nothing is trusted except arithmetic.

The lower bound is computer-assisted at three points: the finite $K_7$ lemma, the
eleven-card lemma's third branch, and the sixteen-card exclusion. For the last of those the
solver's word `UNSAT` is not the evidence — every CNF has a DRAT proof accepted by
`drat-trim`, which removes the SAT solver from the trusted base.

What a certificate cannot establish is that the reduction reaches every counterexample, or
that the CNF means what the mathematics means. Those two obligations live in the source
and are named as open in [P3, §7]. [`AUDIT.md`](AUDIT.md) records an independent re-run:
what it settled, and what it could not.

## Contents

```text
papers/         the overview and the five papers
code/           enumeration, verification, SAT and certification scripts
data/           the canonical cores, the reduction data, the witness, three CNF/DRAT pairs
results/        SAT run records, retry chain, certificate summary
docs/           GitHub Pages site: landing page, one abstract page and one PDF per paper
AUDIT.md        independent re-verification log
COVERAGE.md     one row per measured claim, pointing at the artifact that produces it
RELEASING.md    the release procedure, and which DOI goes inside the archive
```

The full archive of 463 CNF and DRAT pairs is large. Three representative pairs — the
three hardest instances — ship in `data/cnf/`; the rest are published as a release
asset, [`g6-certificates-463.zip`](https://github.com/Osman209/g6-equals-17/releases),
about 534 MB, holding all 463 CNF files, all 463 DRAT proofs, and the per-core
`drat-trim` output and `.verified` markers.

## Running the checks

No libraries are needed for the two that matter most:

```bash
python code/verify_witness_17.py
python code/verify_k7.py
```

The rest of the standard-library checks:

```bash
python code/verify_histograms.py
python code/verify_eleven_cards.py
python code/verify_degree3_kernels.py --witness
python code/enumerate_eight_maximal.py
python code/enumerate_eight_triples.py
python code/enumerate_eight_cores.py
python code/verify_eight_orbits.py
python code/verify_cnf_regeneration.py
```

The checks of [P5], standard library except for one C file and `sympy` for the last one:

```bash
python code/verify_p5_arithmetic.py
python code/verify_residual_bound.py
python code/verify_local_graphs.py
python code/verify_rainbow_lemmas.py     # compiles code/verify_rainbow.c with cc
python code/verify_anchor_count.py
python code/verify_rainbow_constant.py  # the algebra of Theorem 4
```

To rebuild the PDFs and the site:

```bash
sh code/build_pdfs.sh      # needs pandoc, pdflatex and lmodern
python code/build_site.py
node code/check_github_math.js papers/*.md README.md
python code/audit.py       # the release gate; run it after the last edit
```

`verify_eleven_cards.py` takes a few minutes. Do not run any verifier with `python -O`,
which disables the assertions they rely on.

Two scripts regenerate files that are also shipped, and by default write over them:
`enumerate_eight_cores.py` rewrites `data/eight_cores.jsonl`, and `search_sixteen.py`
rewrites `results/sat_results_<solver>_<start>.jsonl`. That is intended — regenerating
in place is what makes the diff meaningful — but it leaves a working tree that `git
status` reports as dirty. Pass `--out` to write somewhere else and leave the checkout
untouched:

```bash
python code/enumerate_eight_cores.py --out /tmp/cores.jsonl
python code/search_sixteen.py --start 0 --stop 5 --out /tmp/sat.jsonl
```

Regenerating `data/eight_cores.jsonl` in place produces a file whose content is
identical to the shipped one. The repository stores it with LF endings; Python's text
mode writes CRLF on Windows, so a regenerated copy there differs from the stored blob
by one byte per line and by nothing else. Compare with line endings normalised before
concluding anything from a diff.

Two checks need `python-sat` (`pip install python-sat`):

```bash
python code/verify_encoding_controls.py
python code/search_sixteen.py --start 0 --stop 5
```

To re-check a certificate you need `drat-trim`, built from
[its source](https://github.com/marijnheule/drat-trim):

```bash
drat-trim data/cnf/core_007.cnf data/cnf/core_007.drat
```

The expected last lines are `s VERIFIED`.

### Checking certificates on Windows

The DRAT files are in the binary proof format. Two portability problems make an
out-of-the-box Windows build report a **false** `s NOT VERIFIED`, and only one of
them announces itself:

```bash
gcc drat-trim.c -std=c99 -O2 -Dgetc_unlocked=getc -o drat-trim.exe
```

1. `getc_unlocked` is POSIX and absent on Windows, so the build fails. The define
   above is enough; it changes no checking logic.
2. `drat-trim.c` opens the proof file in text mode (`fopen (argv[2], "r")`). On
   Windows a byte `0x1A` inside binary proof data is treated as end-of-file, so
   parsing stops early and the checker reports `s NOT VERIFIED` **without any
   warning**. Change both proof-file opens to binary mode (`"rb"`).

Without fix 2 the archive appears to fail: `core_003.drat`, for example, has its
first `0x1A` at byte 644, and an unpatched Windows build reads 645 of its 37,410
bytes before giving up. After the fix every proof is read in full and verifies.

Confirm the checker still rejects bad proofs before trusting a `VERIFIED`: an empty
proof, a proof from a different instance, and a bare empty-clause claim must all
return `s NOT VERIFIED`.

## Reproducing the sixteen-card search

`code/search_sixteen.py` and `data/eight_cores.jsonl` are the two files the whole stage
rests on. Use the copies in this repository; do not reconstruct either from prose.
`code/verify_cnf_regeneration.py` checks that the shipped CNFs are exactly what that
script produces from that data.

The tested toolchain was CaDiCaL and `drat-trim`. Budget exhaustion is never treated as
exclusion: the three instances that first hit the 50,000-conflict limit — cores 7, 239 and
342 — were rerun without a budget and proved UNSAT before certification.
`code/resolve_sixteen.py` carries that rule in its first line.

## Literature and priority

Two sources were reviewed: a general lower bound and an eighteen-card construction. They
do not settle whether the value obtained here is already known, and an eighteen-card
minimum inside a particular projective plane is not the unrestricted value of $g(6)$. No
priority claim is made from the computation. A literature and priority review should come
before any submission.

## Status, priority, and the use of AI assistance

**This is a research draft, not a settled result.** No priority is claimed for the value
obtained here, or for any lemma in this set. The literature was reviewed only as far as the
two sources named in the reference lists, which do not settle whether the value is already
known.

**The lower bound has not been independently reviewed.** It is computer-assisted at three
points, and while DRAT certification removes the SAT solver from the trusted base, two
obligations remain open by construction: that the finite reduction reaches every possible
counterexample, and that the CNF encoding means what the mathematics means. Neither is
discharged by any certificate. No human referee and no proof assistant has checked this
work. Until one has, the right reading of the lower bound is *a reproducible computation
whose reductions are written down and open to review*, not *a theorem*. The upper bound is
different in kind: it is a witness, and anyone can check it in a few seconds.

The results of [P5] for every $r$ are proposed proofs. Their finite steps are checked
exhaustively; the steps that are not finite have been read but not independently
reviewed, and [P5, §7] lists them.

**AI assistance was used throughout, including in the review.** Large language models were
used as tools: ChatGPT (OpenAI) for algebraic derivation, for much of the code in `code/`,
and for drafting; Claude (Anthropic) for independent re-running and auditing of the
computations, for the encoding controls, for the reconstruction of the lost enumeration
step, and for review and prose. For [P5], the proofs were first drafted with ChatGPT in
sessions the author directed; Claude checked every finite step exhaustively, re-derived the
arithmetic, shortened the exclusion of the large cases, extended the exclusion from
$r \ge 19$ to $r \ge 16$ with the swap lemma and the anchor count, and wrote the text. Where the two disagreed, computation settled it and the
text records the resolution. The research direction, the objects studied, and the
responsibility for every claim are the author's.

The same tools were used to check the work, so the checking carries the same caveat as the
work. What the reader is asked to rely on is not any assurance about the tools but the
discipline behind them: **every number reported here is regenerated by a script in `code/`
or certified by a proof file in `results/`, and every script has been read.** No statement
in these papers rests on the assertion of a model. `AUDIT.md` records what an independent
re-run settled and what it could not.

## Licence

- Code: MIT, see [`LICENSE`](LICENSE).
- Papers and documentation: CC BY 4.0, see [`LICENSE-CONTENT`](LICENSE-CONTENT).

## Citation

DOI: [10.5281/zenodo.22883809](https://doi.org/10.5281/zenodo.22883809)

See [`CITATION.cff`](CITATION.cff).
