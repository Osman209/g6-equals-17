# The six-card cover problem: an overview

*The case $r = 6$ of the Erdős–Lovász cover number problem.*

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## 1. The question

Erdős and Lovász asked in 1974, in the paper that introduced the local lemma, for the
minimum number of edges $g(r)$ in an $r$-uniform intersecting hypergraph whose cover
number is $r$. Erdős later called it one of his three favourite combinatorial problems and
offered \$500 for a linear upper bound; Kahn proved one in 1994 (*J. Amer. Math. Soc.* 7,
125–143). The exact values known are $g(3) = 6$, $g(4) = 9$ and $g(5) = 13$, the last due
to Barát (arXiv:2011.04444), and the strongest published general lower bound,
$g(r) \ge ((41-\sqrt{19})/12 - o(1))r$ (arXiv:2606.24878), gives only $g(6) \ge 14$. This overview concerns $r = 6$. What the literature does and does not
already settle is §6, and it should be read before the value here is quoted anywhere.
[P5] turns from $r = 6$ to every $r$.

A family of finite sets is **6-uniform** if every member has exactly six elements, and
**pairwise intersecting** if any two members share an element. We call a member a *card*
and an element a *symbol*.

A **transversal** (or cover) is a set of symbols meeting every card. The smallest size of
a transversal is the transversal number, written $\tau$.

In a pairwise intersecting 6-uniform family, the six symbols of any single card already
meet every other card. So $\tau \le 6$ always, and $\tau = 6$ is the same statement as
*no five symbols cover every card*.

The quantity studied here is

$$g(6) = \min \lbrace \lvert F \rvert : F \text{ is 6-uniform, pairwise intersecting, } \tau(F) = 6 \rbrace .$$

## 2. The chain

| stage | statement | where |
|---|---|---|
| at most 15 cards | impossible | [P1] and [P2], two independent routes |
| exactly 16 cards | impossible | [P3], computer-assisted |
| exactly 17 cards | an explicit family exists | [P4] |

The first two give $g(6) \ge 17$. The third gives $g(6) \le 17$. Together,

$$g(6) = 17 .$$

## 3. The papers

**[P1] Fifteen cards: the histogram route.** The original argument. Symbol degrees are
forced into $\lbrace 2,3,4 \rbrace$; a finite lemma about edge covers of $K_7$ is checked
exhaustively; a weighted counting inequality cuts the possible degree histograms down to
thirteen; each of the thirteen is then eliminated by hand.

**[P2] The eleven-card lemma.** A later and shorter route to the same place. It proves
that *every* pairwise intersecting 6-uniform family of eleven cards has a transversal of
size four, and then gets the fifteen-card exclusion in two lines. The eleven-card lemma
is also what forces the maximum degree to be exactly four in the sixteen-card stage, so
[P2] is used by [P3] while [P1] is not.

**[P3] Sixteen cards.** Deleting the four cards of a degree-four symbol leaves a
twelve-card kernel with $\tau = 5$. That kernel either has a second degree-four symbol or
does not, and the two cases are handled separately. If it does not, the kernel is one of
341 objects of maximum degree three, enumerated and excluded one by one. If it does,
deleting that symbol's cards leaves an eight-card core. The cores are enumerated up to relabelling — there are 463 — and for
each one the completion problem is written as a CNF formula. All 463 are unsatisfiable,
and each unsatisfiability has a DRAT certificate accepted by an independent checker.

**[P4] A seventeen-card witness.** Seventeen cards on 27 symbols, with all
$\binom{17}{2} = 136$ pairs intersecting and none of the $\binom{27}{5} = 80{,}730$
five-symbol sets a transversal. This is a direct finite check and needs nothing from the
other three papers.

**[P5] Every r.** Proposed proofs for every $r$, in the framework of Sivashankar
(arXiv:2606.24878): the residual cover bound with constant $+3$, which gives
$g(r) \ge 3r-3$; the exclusion of equality, which gives $g(r) \ge 3r-2$ for $r \ge 19$; a
quantitative form with a loss linear in $r$ when the remainder is large; and an account of
where the route toward a coefficient above $3$ stands. At $r = 6$ they give only
$g(6) \ge 15$, so [P5] adds nothing to the value above. Its finite steps are checked
exhaustively; its other steps are unreviewed.

## 4. What carries the weight

The two bounds are not of the same kind, and it is worth being plain about that.

The upper bound is a witness. Anyone can check it with a short script and no libraries:
seventeen sets, 136 pairs, 80,730 subsets. Nothing is trusted except arithmetic.

The lower bound is computer-assisted at two points. The $K_7$ lemma of [P1] and [P2] is
a finite exhaustive check (294,239,817 cases). The eleven-card lemma's third branch is
an exhaustive search over 5,373 instances. The sixteen-card exclusion rests on the
reduction to 463 cores and on 463 unsatisfiability results.

For the last of those, the solver's word is not the evidence. Each CNF has a DRAT proof,
and a DRAT proof checked by `drat-trim` removes the SAT solver from the trusted base.
What a DRAT proof does **not** establish is that the reduction reaches every possible
counterexample, or that the CNF says what the mathematics says. Those two obligations
live in the reduction source and the encoding source, and they are the parts a reader
should read rather than run. `AUDIT.md` records what an independent re-run did and did
not settle.

## 5. Citation convention

The papers of this set are cited as [P1] to [P5]. A bare bracketed number inside a
paper is an entry in that paper's own reference list. Each paper numbers its own results
from 1.

| tag | file |
|---|---|
| [P1] | `paper_1_fifteen_cards_histogram_route.md` |
| [P2] | `paper_2_eleven_card_lemma.md` |
| [P3] | `paper_3_sixteen_cards.md` |
| [P4] | `paper_4_seventeen_card_witness.md` |
| [P5] | `paper_5_every_r.md` |

## 6. Literature boundary

Two sources were reviewed: a general lower bound and an eighteen-card construction
(see the reference lists of [P1] and [P3]). Neither settles whether the value obtained
here is already known. A construction that is minimal inside a particular projective
plane is not the same thing as the unrestricted value of $g(6)$, and should not be
quoted as such. No priority claim is made from the computation alone; a proper
literature and priority review should come before any journal submission.

A wider search was made during the second verification pass and is recorded in
`AUDIT.md` §4.7. It found the exact values $g(3) = 6$, $g(4) = 9$ and $g(5) = 13$, and
no source determining $g(6)$; it also confirmed the distinction drawn above against the
primary text, since Barát's eighteen-edge example is the minimum inside $PG(2,5)$ and is
a value of the projective-plane restricted function, not of $g(6)$. That search was a
search. It cannot establish that nothing was missed, and the obligation stated in the
previous paragraph is unchanged.

## 7. Status, priority, and the use of AI assistance

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

**AI assistance was used throughout, including in the review.** Large language models were
used as tools: ChatGPT (OpenAI) for algebraic derivation, for much of the code in `code/`,
and for drafting; Claude (Anthropic) for independent re-running and auditing of the
computations, for the encoding controls, for the reconstruction of the lost enumeration
step, and for review and prose. Where the two disagreed, computation settled it and the
text records the resolution. The research direction, the objects studied, and the
responsibility for every claim are the author's.

The same tools were used to check the work, so the checking carries the same caveat as the
work. What the reader is asked to rely on is not any assurance about the tools but the
discipline behind them: **every number reported here is regenerated by a script in `code/`
or certified by a proof file in `results/`, and every script has been read.** No statement
in these papers rests on the assertion of a model. `AUDIT.md` records what an independent
re-run settled and what it could not.
