# [P4] A seventeen-card witness

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

An explicit pairwise intersecting 6-uniform family of seventeen cards on 27 symbols with
transversal number six. All 136 card pairs intersect, and none of the 80,730 five-symbol
subsets is a transversal. Hence $g(6) \le 17$. This paper uses nothing from [P1], [P2] or
[P3]; it can be checked on its own.

This is a witness: it is checked directly and depends on nothing else in the set. No priority
is claimed. See the note at the end.

## 1. The family

Symbols $1,\dots,27$.

| | | | |
|---|---|---|---|
| $A_1$ | 1, 2, 3, 4, 5, 21 | $A_{10}$ | 4, 8, 10, 18, 20, 25 |
| $A_2$ | 6, 10, 14, 16, 17, 21 | $A_{11}$ | 4, 9, 11, 17, 19, 26 |
| $A_3$ | 5, 6, 7, 8, 9, 22 | $A_{12}$ | 5, 12, 15, 16, 20, 26 |
| $A_4$ | 1, 13, 15, 17, 18, 22 | $A_{13}$ | 2, 10, 12, 19, 22, 27 |
| $A_5$ | 1, 7, 10, 11, 12, 23 | $A_{14}$ | 3, 8, 17, 23, 26, 27 |
| $A_6$ | 2, 6, 13, 19, 20, 23 | $A_{15}$ | 4, 9, 15, 16, 23, 27 |
| $A_7$ | 2, 8, 11, 14, 15, 24 | $A_{16}$ | 5, 14, 18, 23, 26, 27 |
| $A_8$ | 3, 7, 16, 18, 19, 24 | $A_{17}$ | 7, 11, 13, 20, 21, 27 |
| $A_9$ | 3, 9, 12, 13, 14, 25 | | |

Machine-readable copy: `data/witness_17.json`.

## 2. The verification

**Proposition 1.** *The family above is pairwise intersecting, 6-uniform, and has
$\tau = 6$. Hence $g(6) \le 17$.*

*Proof.* Seventeen distinct cards, each of six distinct symbols, is read off the table.
All $\binom{17}{2} = 136$ pairs are checked and every intersection is non-empty. All
$\binom{27}{5} = 80{,}730$ five-symbol subsets are checked and none meets all seventeen
cards, so $\tau \ge 6$. Since the family is pairwise intersecting, the six symbols of
$A_1$ already meet every card, so $\tau \le 6$. A cover of size below five would extend to
one of size five, so those are excluded too. $\square$

`code/verify_witness_17.py` performs the check in two independent ways — by unions of
support bitmasks and by direct set intersection — and needs only the Python standard
library. No SAT solver, compiler or external binary is involved.

Do not run the verifier with `python -O`, which disables the assertions it relies on.

## 3. Structure

The symbol degrees are

$$n_2 = 2, \quad n_3 = 4, \quad n_4 = 19, \quad n_5 = 2 .$$

The two degree-five symbols are 23 (in cards 5, 6, 14, 15, 16) and 27 (in cards 13, 14,
15, 16, 17).

The presence of degree-five symbols matters. The sixteen-card search of [P3] imposes a
degree-four cap, which is correct there because [P2, Cor 2] forces it at sixteen cards.
Imposing the same cap on a seventeen-card search would wrongly discard this family.

The witness is also inclusion-minimal for the property $\tau = 6$: deleting any single
card leaves a family with a five-cover. The seventeen deletion covers are stored in
`data/witness_17.json` and are checked by the verifier. That is a property of this
particular family; it is not a proof that all sixteen-card families fail, which is what
[P3] is for.

## 4. How it was found

The first twelve cards form a kernel with six degree-two symbols and twenty degree-three
symbols, and $\tau = 5$. List all of its five-covers. Introduce a Boolean variable for
each, and ask for a selection of at most five of them such that every five-cover of the
kernel is disjoint from at least one selected cover — the extension criterion of
[P3, Prop 2] with five covers in place of four. Adding a new common symbol, here 27, to
each of five selected covers produces five new cards.

The search used Glucose 4 through `python-sat` and returned a selection of five. The
verification of the resulting object is independent of that solver: `verify_witness_17.py`
re-checks the finished family from scratch.

The search record, with symbols indexed from 0, is kept in `results/search_record.json`.
The shift to symbols $1,\dots,27$ changes no intersection and no cover number.

## 5. Verification

| claim | script |
|---|---|
| 17 distinct cards, all of size 6 | `code/verify_witness_17.py` |
| all 136 pairs intersect | same |
| none of the 80,730 five-sets covers | same, by two independent methods |
| degree histogram | same |
| inclusion-minimal, with an explicit five-cover per deletion | same |

---

*This work was prepared with AI assistance (ChatGPT, OpenAI; Claude, Anthropic), used for algebraic derivation, for drafting and rewriting code and text, for running and re-running the computations, and for auditing the papers against their own scripts. The same tools were used in the review, so the review carries the same caveat. All statements were checked by the author, who is responsible for them. No priority is claimed and the result has not been independently reviewed by a human or a proof assistant; the repository README sets out the division of labour and the open obligations in full.*
