# [P2] The eleven-card lemma

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

Every pairwise intersecting 6-uniform family of eleven cards has a transversal of size at
most four. The proof splits on the maximum symbol degree: degree five or more is closed by
pairing, degree four by the finite $K_7$ lemma, and degree at most three by an exhaustive
triangle-decomposition search over 5,373 instances. The fifteen-card exclusion of [P1]
then follows in two lines, and the same lemma pins the maximum degree at exactly four in
the sixteen-card stage of [P3].

Computer-assisted; not independently reviewed. No priority claimed. See the note at the end.

## 1. Why a second route

[P1] reaches $g(6) \ge 16$ through a degree histogram and thirteen hand eliminations. The
route works but it is long, and it does not generalise: at sixteen cards the histogram
stage needs an inequality whose right-hand side is no longer controlled, because the
disjointness count $D$ of high-symbol pairs has no usable upper bound there.

The eleven-card lemma avoids the histogram entirely. It is a statement about eleven cards
with nothing assumed about degrees, and everything else drops out of it.

## 2. The lemma

**Theorem 1.** *Every pairwise intersecting 6-uniform family of eleven cards has a
transversal of size at most four.*

Suppose not: eleven cards, pairwise intersecting, and $\tau > 4$.

### Branch A — some symbol has degree at least five

Choose it. At most six cards remain; pair them and take one shared symbol per pair, at
most three symbols. Total at most four, contradiction. So the maximum degree is at most
four.

### Branch B — some symbol has degree four

Let $y$ have degree four and delete its four cards, leaving seven cards $R$.

$\tau(R) > 3$, since otherwise $y$ together with a three-cover of $R$ is a four-cover.

Every symbol of $R$ has residual degree at most two: a symbol $z$ of residual degree at
least three would leave at most four cards, coverable by two more symbols, so $z$ plus
those two is a three-cover of $R$.

Each card of $R$ must meet the other six through its six symbols, and each symbol reaches
at most one other card. So every symbol of $R$ has residual degree exactly two and every
pair of cards of $R$ meets in exactly one symbol. The seven cards are therefore the
vertices of a $K_7$ and their 21 shared symbols are its edges.

Each of the four deleted cards contains $y$, which lies outside $R$, and must meet all
seven cards of $R$. Its remaining five symbols therefore induce an edge cover of that
$K_7$ of size at most five.

**Lemma 2 (computer-assisted, the $K_7$ lemma).** *Given any four edge covers of $K_7$,
each of size at most five, there is a four-edge cover of $K_7$ meeting each of them in an
edge. Repetitions among the inputs are allowed.*

The four symbols of that four-edge cover then cover all seven cards of $R$ (an edge cover
covers every vertex) and also the four cards of $y$ (each is met in an edge). That is a
four-cover of all eleven cards, contradiction.

The lemma is verified exhaustively: 840 inclusion-minimal inputs, 315 four-edge covers,
one fixed representative per isomorphism type, $294{,}239{,}817$ quadruples certified,
zero counterexamples. See `code/verify_k7.py` and [P1, §3] for the enumeration of the
three minimal types.

### Branch C — every symbol has degree at most three

Write $(t,b,s)$ for the numbers of symbols of residual degree three, two and one in a
card. Then $t + b + s = 6$, and since a card must meet the other ten,
$2t + b \ge 10$. The only solutions are

$$A = (4,2,0), \quad B = (5,0,1), \quad C = (5,1,0), \quad D = (6,0,0) .$$

Their excess degrees — the sum over other cards of intersection size minus one — are
$0, 0, 1, 2$. Let $a,b,c,d$ count them, so $a+b+c+d = 11$, $c$ is even, and
$4a + 5b + 5c + 6d$ is divisible by three.

Let $E$ be the multigraph on card pairs whose multiplicity is the intersection size minus
one, and $F$ the graph with one edge per degree-two symbol. Degrees of $E$ on types
$A,B,C,D$ are $0,0,1,2$; degrees of $F$ are $2,0,1,0$. $F$ is simple: a repeated $F$ edge
needs two endpoints of $F$-degree at least two, hence of type $A$, whose $E$-excess is
zero.

The degree-three symbols must decompose the pair multigraph

$$M = K_{11} + E - F$$

into triangles, repeats permitted. And that decomposition can contain no matching of size
three: three vertex-disjoint triangles cover nine cards with three symbols, and the
remaining pair is covered by one more, giving a four-cover.

Every $F$ component is a path with $C$ endpoints and $A$ interiors, or a cycle of $A$
vertices of length at least three. Every $E$ component is a path with $C$ endpoints and
$D$ interiors, or a cycle of $D$ vertices of length at least two, a two-cycle being a
double edge. Type $B$ is isolated in both.

`code/verify_eleven_cards.py` generates every relative arrangement of $F$ and $E$ by
labelling the $C$ vertices first, fixing their pairing in $F$, distributing $A$ interiors
in nondecreasing numbers along the paths, partitioning the remaining $A$ vertices into
cycles of length at least three, and then enumerating every $E$ pairing of the $C$
vertices, every allocation of $D$ interiors and every partition of the remaining $D$
vertices into cycles of length at least two. Duplicates are harmless.

That gives 5,373 instances across 58 non-empty profiles. Each one is searched exactly:
at each step the solver takes a pair with positive remaining multiplicity, branches over
every triangle containing it with positive capacity, and forbids a triangle that would
complete a matching of size three with the triangles already chosen. All 5,373 return
UNSAT.

Branches A, B and C are exhaustive, so Theorem 1 holds. $\square$

## 3. Fifteen cards, in two lines

**Corollary 1.** *No pairwise intersecting 6-uniform family of at most fifteen cards has
transversal number six. Hence $g(6) \ge 16$.*

*Proof.* Suppose fifteen cards with $\tau = 6$. If every degree were at most three, a
fixed card's six symbols would meet at most $6 \cdot 2 = 12$ other cards, while fourteen
must be met. So some symbol $x$ has degree at least four. Delete its cards: at most eleven
remain, padded up to eleven by repeating existing cards if necessary, which changes no
transversal number. Theorem 1 gives a four-cover of them, and with $x$ that is a
five-cover. Smaller families are handled by the same padding. $\square$

Compare [P1], where the same statement costs a weighted inequality, an exact enumeration
of thirteen histograms, and nine pages of incidence arguments.

## 4. What the lemma gives the sixteen-card stage

**Corollary 2.** *In a pairwise intersecting 6-uniform family of sixteen cards with
$\tau = 6$, the maximum symbol degree is exactly four.*

*Proof.* The same local count gives a symbol of degree at least four, since a card must
meet fifteen others and six symbols of degree at most three reach only twelve. A symbol of
degree at least five would leave at most eleven cards, which Theorem 1 covers with four
symbols, giving a five-cover. $\square$

That is the hypothesis [P3] starts from.

## 5. Scope

Theorem 1 is sharp at eleven. `code/verify_core.py` (working directory, not part of the
release checks) exhibits a twelve-card pairwise intersecting 6-uniform family with
$\tau = 5$, so the lemma does not extend to twelve by raising the count alone.

An eight-card analogue does not hold either. There is an explicit eight-card pairwise
intersecting 6-uniform family with maximum degree three and $\tau = 4$: take card 7 as the
centre of four triangles $\lbrace 7,0,1 \rbrace$, $\lbrace 7,0,2 \rbrace$,
$\lbrace 7,3,4 \rbrace$, $\lbrace 7,5,6 \rbrace$, give card 7 two pendant symbols, and
join every remaining pair of cards directly by a degree-two symbol. All 1,330 three-symbol
subsets fail to cover, and the four triangle symbols cover. This is why [P3] must
enumerate eight-card cores rather than exclude them, and it is the reason the sixteen-card
stage needs a SAT layer at all.

## 6. Verification

| claim | script |
|---|---|
| Lemma 2, all 294,239,817 quadruples | `code/verify_k7.py` |
| Branch C, all 5,373 instances UNSAT | `code/verify_eleven_cards.py` |

Branches A and B are hand arguments on top of Lemma 2.

---

*This work was prepared with AI assistance (ChatGPT, OpenAI; Claude, Anthropic), used for algebraic derivation, for drafting and rewriting code and text, for running and re-running the computations, and for auditing the papers against their own scripts. The same tools were used in the review, so the review carries the same caveat. All statements were checked by the author, who is responsible for them. No priority is claimed and the result has not been independently reviewed by a human or a proof assistant; the repository README sets out the division of labour and the open obligations in full.*

## References

1. J. Barát, *Intersecting and 2-intersecting hypergraphs with maximal covering number:
   the Erdős–Lovász theme revisited*, arXiv:2011.04444. Lemma 2.2 there is the standard
   "choose a high-degree symbol and pair the rest" step used in Branch A.
