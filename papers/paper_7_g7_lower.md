# [P7] Seven: no family of eighteen cards, so $19 \le g(7) \le 21$

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

No pairwise intersecting 7-uniform family of eighteen cards has transversal number seven.
With the 21-card family of [P5, §5] this gives $19 \le g(7) \le 21$. The argument deletes the
cards of a symbol of degree four and splits into two branches. In one, the twelve-card
picture of [P3, §2a] reappears on fourteen cards, and every candidate kernel turns out to
contains four disjoint triples, and four disjoint triples give a cover of size five. In the other,
a second deletion leaves a ten-card core, and no core exists. Both finite steps were
computed twice, by separately written programs, and the programs reproduce the counts of
[P3] at $r = 6$.

The argument is elementary counting plus computation; it does not use the proposed
proofs of [P5]. Nothing here has been reviewed by a human referee or a proof assistant. No priority is claimed. See the note at
the end.

## 1. Setting

Let $H$ be a pairwise intersecting family of eighteen cards, each a set of seven symbols,
with $\tau(H) = 7$. We show that no such $H$ exists.

**Theorem 1 (computer-assisted).** *There is no pairwise intersecting
7-uniform family of eighteen cards with transversal number seven. Hence $g(7) \ge 19$, and
with [P5, §5], $19 \le g(7) \le 21$.*

As in [P3], it helps to read the cards as points and the symbols as blocks: a symbol is the
set of cards that contain it, and its size is its degree.

## 2. Degree four

**Lemma 1.** *The maximum degree of $H$ is exactly four.*

*Proof.* If every degree were at most three, a card would meet the other seventeen through
seven symbols reaching at most two cards each, and $17 \le 14$ is false.

Suppose a symbol $x$ has degree $d \ge 5$. Delete its cards and call the remaining
$m = 18 - d$ cards $F$. A cover of $F$ together with $x$ covers $H$, so $\tau(F) \ge 6$. We
show $\tau(F) \le 5$.

- $m \le 10$: pair the cards; each pair shares a symbol.
- $m = 11$: a symbol meeting three cards, with a pairing of the other eight, gives five.
  If every symbol meets at most two cards, the 55 pairs need 55 different symbols, but the
  77 incidences allow at most 38.
- $m = 12$ or $13$: a symbol meeting four or more cards leaves at most nine, and those have
  a cover of size four (pair them if there are fewer than nine; for nine, argue as for
  eleven, with 36 pairs against at most 31 symbols), so the total is at most five. Otherwise every symbol meets at most three cards
  of $F$, and Lemma 2 gives three disjoint triples. They meet nine cards; the other three
  or four pair off through two more symbols, five in all. $\square$

**Lemma 2 (computer-assisted).** *Let $F$ be twelve or thirteen pairwise intersecting
cards of size seven in which every symbol meets at most three cards. Then the symbols
meeting three cards contain three pairwise disjoint triples.*

*How it was checked.* As in Lemma 6 below, each card $p$ needs room: the triples at $p$,
plus the cards sharing no triple with $p$ (each needs its own symbol of size two), number
at most seven. Removing repeated copies of a triple keeps this condition and does not
change which triples are disjoint, so it is enough to consider sets of triples. If the
largest number of disjoint triples is $k$, fix $k$ disjoint ones (all such placements are
equivalent); no other triple avoids them all. A SAT model shows that $k = 1$ and $k = 2$
are impossible for twelve and for thirteen cards, with two solvers (CaDiCaL, Glucose) and
two cardinality encodings. As controls, the same model is satisfiable with $k = 3$ (twelve
and thirteen cards) and $k = 4$ (twelve).

## 3. The first deletion

Fix a symbol $x$ of degree four and let $G$ be the other fourteen cards. A cover of $G$
together with $x$ covers $H$, so $\tau(G) \ge 6$. Every symbol has degree at most four in
$G$. Either $G$ has a symbol of degree four (§5) or it does not (§4).

## 4. Branch A: the kernel has maximum degree three

### 4.1 The three profiles

Each card of $G$ meets the other thirteen through its seven symbols, and each symbol
reaches at most two of them. Writing $(t, b, s)$ for the numbers of its symbols of degree
three, two and one in $G$, we need $t + b + s = 7$ and $2t + b \ge 13$. So every card has
profile $(7,0,0)$ or $(6,1,0)$, and there are no symbols of degree one.

This is the situation of [P3, §2a] with fourteen cards in place of twelve. A $(6,1,0)$ card
meets every other card exactly once, and a $(7,0,0)$ card meets exactly one other card
twice. So the degree-two symbols form a matching $F$ on the $c$ cards of type $(6,1,0)$,
the doubled pairs form a matching $E$ on the others, and the degree-three symbols are the
triangles of a decomposition of the pair multigraph

$$M = K_{14} + E - F .$$

The number of triangles is $(98 - c)/3$, and $c$ is even, so $c \in \lbrace 2, 8, 14 \rbrace$.
A triangle holds at most one edge of $E$, so no triangle occurs twice.

### 4.2 The obstruction

**Lemma 3.** *If $\tau(G) \ge 6$, the triangles of $G$ contain no four that are pairwise
disjoint.*

*Proof.* Four disjoint triangles meet twelve cards through four symbols. The two cards
left meet each other, through a fifth symbol. That is a cover of size five. $\square$

**Lemma 4 (computer-assisted).** *For each $c \in \lbrace 2, 8, 14 \rbrace$, every triangle
decomposition of $M$ contains four pairwise disjoint triangles.*

*How it was checked.* Let $\nu$ be the largest number of pairwise disjoint triangles.

- $\nu \le 2$ is impossible for all three profiles, by a plain exhaustive search
  (13,614,095, 26,427,987 and 193,839,399 search nodes for $c = 14, 8, 2$).
- $\nu = 3$. Fix three disjoint triangles. The five cards outside them hold no triangle,
  since that would be a fourth. The placements of the three triangles fall into orbits
  under the automorphisms of $M$, which permute the pairs of $F$ and of $E$ and swap the two
  cards inside a pair. There are 266,560, 367,696 and 505,120 placements, in 6, 122 and 60
  orbits for $c = 14, 8, 2$. From one placement in each orbit, the rest of the decomposition
  is searched to exhaustion. None completes.

The $\nu = 3$ step was done twice, with no code in common. The first route takes the orbits
from nauty and completes each one with a search tree. The second takes the orbits by
union-find under explicit generators of the automorphism group, and completes each one with
a SAT solver, forbidding any four disjoint triangles that appear. Both give the same orbit
counts, and neither finds a decomposition. For $c = 14$ a third check, a plain exhaustive
search of the whole profile (600,808,145 nodes), also finds none.

By Lemmas 3 and 4, $\tau(G) \le 5$ in every case, so branch A is empty.

## 5. Branch B: a second symbol of degree four

Let $y$ have degree four in $G$. Its cards are not cards of $x$. Delete them as well, and
let $K$ be the remaining ten cards, the **core**.

**Lemma 5.** *In the core:*

1. *every symbol meets at most three cards;*
2. *any two symbols of size three meet;*
3. *every card lies in a symbol of size three;*
4. *for every card $p$, the number of size-three symbols at $p$, counted with repetition,
   plus the number of cards that share no size-three symbol with $p$, is at most seven.*

*Proof.*

1. A symbol meeting four cards of $K$: delete them; the six cards left pair off, and each
   pair shares a symbol. With $x$, $y$ and that symbol this is a cover of size six.
2. Two disjoint triples meet six cards through two symbols; the other four cards pair off
   through two more; with $x$ and $y$ that is six.
3. A card meets nine others through seven symbols. With no symbol of size three, each
   reaches at most one, and $7 \lt 9$.
4. Each card that shares no triple with $p$ needs its own symbol of size two with $p$.
   These symbols, and the triples at $p$, are all different symbols of $p$, which has
   seven. $\square$

**Lemma 6 (computer-assisted).** *No multiset of 3-subsets of ten points satisfies 2, 3
and 4 of Lemma 5.*

*How it was checked.* Twice. A SAT model of conditions 2 to 4, with each triple allowed up
to seven times (condition 4 bounds the repetition by seven), is unsatisfiable. A separate
enumeration of intersecting triple systems, using the bound of three repetitions (a card
holding a triple $m$ times reaches two cards through it, and $2 + 2(7 - m) \ge 9$), finds
none that leaves room in every card. The same enumeration program, run at $r = 6$ on eight
points, returns the 463 cores of [P3, §3].

So branch B is empty, and Theorem 1 is proved. $\square$

## 6. Calibration

Each program was run at $r = 6$ before it was used at $r = 7$, where the answers are known:

| program | at $r = 6$ | known value |
|---|---|---|
| exhaustive kernel search, profiles 12 and 6 | 69,120 and 558,672 | [P3, §2a] |
| kernel search with a fixed matching, both routes | finds kernels | they exist |
| core enumeration, eight points | 463 cores | [P3, §3] |
| core SAT model, eight points | satisfiable | cores exist |

## 7. Verification

| claim | script |
|---|---|
| Lemma 2, twelve and thirteen cards | `code/r7_small_families.py` |
| Lemma 4, $\nu \le 2$; plain search of $c = 14$ | `code/r7_kernel_exhaustive.c` |
| Lemma 4, $\nu = 3$, first route | `code/r7_kernel_matched.c` (needs nauty) |
| Lemma 4, $\nu = 3$, second route | `code/r7_kernel_sat.py` |
| Lemma 6, enumeration | `code/r7_cores.c` (needs nauty) |
| Lemma 6, SAT | `code/r7_cores_sat.py` |
| all of the above with expected answers | `code/verify_g7_lower.py` |
| the recorded runs | `results/g7_lower_checks.txt` |
| the upper bound $g(7) \le 21$ | `code/verify_witness_r7_21.py` |

## 8. What is and is not established

- Nothing from [P5] is used. An earlier version of this paper excluded degree five and more
  through [P5, Theorem 1]; Lemma 2 now does it directly.
- The arguments of Lemma 1, §3, §4.1, Lemma 3 and Lemma 5 are short and elementary; they have been read,
  not reviewed.
- Lemmas 2, 4 and 6 are computations. Each was done by two programs with no code in common,
  and each program reproduces known counts at $r = 6$. They carry no proof certificates.
- Whether $g(7) \ge 19$ or $g(7) \le 21$ is already known has not been checked beyond a short
  search.

---

*This work was prepared with AI assistance (ChatGPT, OpenAI; Claude, Anthropic), used for algebraic derivation, for drafting and rewriting code and text, for running and re-running the computations, and for auditing the papers against their own scripts. The same tools were used in the review, so the review carries the same caveat. All statements were checked by the author, who is responsible for them. No priority is claimed and the result has not been independently reviewed by a human or a proof assistant; the repository README sets out the division of labour and the open obligations in full.*

## References

1. P. Erdős and L. Lovász, *Problems and results on 3-chromatic hypergraphs and some related
   questions*, in **Infinite and Finite Sets** (Keszthely, 1973), Colloq. Math. Soc. János
   Bolyai 10, North-Holland, 1975, 609–627.
2. B. D. McKay and A. Piperno, *Practical graph isomorphism, II*, J. Symbolic Comput. 60
   (2014), 94–112. The nauty package.
3. A. Ignatiev, A. Morgado and J. Marques-Silva, *PySAT: A Python toolkit for prototyping
   with SAT oracles*, SAT 2018, LNCS 10929, 428–437.
