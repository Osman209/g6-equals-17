# [P1] Fifteen cards by hand: the histogram route

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

No pairwise intersecting 6-uniform family of fifteen cards has transversal number six.
Degree bounds force every symbol degree into $\lbrace 2,3,4 \rbrace$; a finite lemma
on edge covers of $K_7$ supplies the two hardest degree exclusions; a weighted counting
inequality reduces the possible degree histograms to thirteen; and the thirteen are
eliminated by incidence arguments. Hence $g(6) \ge 16$.

Every step is a hand argument: the $K_7$ lemma has a one-page proof (§3), and the
thirteen histograms come from a short deficit count (§6). The scripts of §9 check the
same statements independently. [P2] reaches the same conclusion through its
eleven-card lemma, one branch of which is a computer search; this paper gives a route
that does not need that search.

Not independently reviewed. No priority claimed. See the note at the end.

## 1. Setting

Let $H$ be an indexed pairwise intersecting family of fifteen six-element cards with
$\tau(H) = 6$. Repeated cards are allowed at the start, so that a smaller counterexample
could be padded up to fifteen without changing its transversal number; §2 shows repeats
are impossible anyway, which is what makes the padding legitimate.

For a symbol $x$, $d(x)$ is its degree, the number of cards containing it. Once degrees
are confined to $\lbrace 2,3,4 \rbrace$, write $n_2, n_3, n_4$ for how many symbols have
each degree, and set $t = n_4$. A symbol of degree four is called **high**.

For a card $A$: $q_A$ is the number of high symbols in $A$, and $\varepsilon_A$ the
number of degree-two symbols. Let $a_j$ count the cards with $q_A = j$.

A card with $q_A = 2$ is **small**; a card with $q_A = 6$ is **full**.

## 2. Degree bounds

**Degree one is impossible.** Delete the symbol from its only card. The other five
symbols of that card meet every other card, since every other card meets this one and
cannot do so through a symbol it does not contain. That is a five-cover.

**Degree at least seven is impossible.** Choose the symbol; at most eight cards remain;
pair them and take one shared symbol per pair. Total $1 + 4 = 5$.

**Degree six is impossible.** Choose the symbol $x$; nine cards remain. Suppose every
symbol has degree at most two among those nine. Each of the $\binom{9}{2} = 36$ pairs
needs a shared symbol, a symbol of degree two serves exactly one pair, and the nine cards
hold only $9 \times 6 = 54$ symbol slots, so at most $54/2 = 27$ pairs can be served.
Since $27 < 36$, some symbol $y$ has degree at least three among the nine. Then $x$ and
$y$ cover at least nine cards, at most six remain, and three more symbols finish them in
pairs: $1 + 1 + 3 = 5$.

**Lemma 1.** *Any pairwise intersecting 6-uniform family of ten cards with maximum symbol
degree at most three has a four-cover.*

*Proof.* Take a degree-three symbol and delete its three cards. If the remaining seven
contain a symbol of residual degree at least three, that symbol plus two pairwise-
intersection symbols finish the ten, for four in total. Otherwise every symbol of those
seven has residual degree exactly two and every pair of the seven meets in exactly one
symbol: the seven cards are the vertices of a $K_7$ and their 21 shared symbols are its
edges. Each of the three deleted cards, with the chosen symbol removed, induces an edge
cover of that $K_7$ of size at most five. Lemma 2 below gives a four-edge cover meeting
each of them, which is then a four-cover of all ten. $\square$

**Degree five is impossible.** If $d(x) = 5$, the remaining ten cards cannot have a
residual degree-four symbol (choose it and pair the remaining six: $1+1+3 = 5$). So their
maximum degree is at most three, Lemma 1 gives a four-cover, and with $x$ that is five.

Hence every degree lies in $\lbrace 2,3,4 \rbrace$.

**No card holds two degree-two symbols.** Suppose card $C$ holds degree-two symbols $x$
and $y$, appearing elsewhere in cards $D_x$ and $D_y$. Any card other than $C$, $D_x$,
$D_y$ must meet $C$, and it cannot do so through $x$ or $y$, so it meets one of the other
four symbols of $C$. Those four therefore cover everything except possibly $D_x$ and
$D_y$. If those two are distinct they share a symbol; if they coincide, take $x$. Either
way one more symbol finishes, for a total of five. So $\varepsilon_A \in \lbrace 0,1
\rbrace$ and $0 \le n_2 \le 7$.

**Local counts.** Counting intersections of a card $A$ with the other fourteen,

$$\sum_{B \ne A} \lvert A \cap B \rvert = 12 + q_A - \varepsilon_A \ge 14 ,$$

so $q_A \ge 2 + \varepsilon_A$, and in particular $q_A \in \lbrace 2,3,4,5,6 \rbrace$.
Subtracting fourteen,

$$\sum_{B \ne A} \bigl( \lvert A \cap B \rvert - 1 \bigr) = q_A - \varepsilon_A - 2 \le 4 .$$

A repeated card would contribute 5 to that sum on its own, so repeats are impossible and
the padding convention is justified.

## 3. The finite $K_7$ lemma

**Lemma 2.** *Given any four edge covers of $K_7$, each of size at most five, there is a
four-edge cover of $K_7$ meeting each of the four in an edge. Repetitions among the four
inputs are allowed.*

Write $V$ for the seven vertices and $T_1,\dots,T_4$ for the inputs. A four-edge cover of
$V$ is a vertex $x$, a perfect matching $M$ of $V\setminus\lbrace x\rbrace$, and one more
edge at $x$. Every $T_i$ has an edge at $x$, so it is enough to find $x$ and $M$ such that
$M$ meets three of the $T_i$: an edge of the fourth at $x$ completes the cover. Call such
a pair $(x,M)$ *good* and suppose there is none. Then:

**(B)** *If $i \ne j$ and $e \in T_i$, $f \in T_j$ are disjoint, then each other $T_k$
contains neither $e$ nor $f$, nor an edge inside the three vertices outside $e \cup f$.*

Indeed such an edge $g$ makes $(x,\lbrace e,f,g \rbrace)$ good, with $x$ the remaining
vertex. If instead $e \in T_k$, take for $g$ any edge on two of the three vertices
outside $e \cup f$ and for $x$ the third: then $\lbrace e,f,g \rbrace$ meets $T_i$,
$T_j$ and $T_k$. In particular no edge lies in three of the $T_i$.

**Two-stars.** A graph on seven vertices with at most five edges, no isolated vertex and
no three disjoint edges is two disjoint stars with five edges ($K_{1,3}+K_{1,2}$ or
$K_{1,4}+K_2$). Such a graph has at least two components, since a connected graph on
seven vertices has six edges. A component that is not a star is either a triangle or
contains a path with three edges. In the second case it has two disjoint edges, and an
edge of another component makes three. A triangle component leaves four vertices, which
need at least two more edges; with five edges in all these are two disjoint edges, and
again there are three disjoint edges. So all components are stars, $c$ of them with
$7-c \le 5$ edges, and three disjoint edges are absent only if $c = 2$.

*Case 1: no $T_i$ has three disjoint edges.* Then each $T_i$ is a two-star. For a graph
$T$ and a vertex $x$ let $h_T(x)$ be the number of the 15 perfect matchings of
$V\setminus\lbrace x\rbrace$ that meet $T$. An edge lies in three of them and two
disjoint edges in exactly one, and inclusion–exclusion gives:

- $K_{1,3}+K_{1,2}$ with centres $a$, $b$: $h = 6$ at $a$, 8 at each leaf of $a$, 9 at $b$
  and at each leaf of $b$; in all 57.
- $K_{1,4}+K_2$ with centre $a$ and edge $bc$: $h = 3$ at $a$, 9 at each leaf of $a$, 12 at
  $b$ and at $c$; in all 63.

So $\sum_x \sum_i h_{T_i}(x) \ge 4 \cdot 57 = 228 > 7 \cdot 30$, and some $x$ has
$\sum_i h_{T_i}(x) \ge 31$. Then one of the 15 matchings of $V\setminus\lbrace x\rbrace$
meets three of the $T_i$, which is a good pair.

*Case 2: $T_1$ has three disjoint edges $e_1,e_2,e_3$.* Let $x$ be the seventh vertex.
For a vertex $q$ in $e_s$ write $\bar q$ for the other end of $e_s$. Applying (B) to the
pairs $(xq, e_t)$, $t \ne s$, gives:

**(C)** *If $xq \in T_j$, $j \ne 1$, $q \in e_s$, then each $T_k$ with
$k \notin \lbrace 1,j \rbrace$ avoids $xq$ and the two $e_t$ with $t \ne s$, and has no
edge from $\bar q$ to those two $e_t$.*

*Step 1. The edges of $T_2,T_3,T_4$ at $x$ all go into one $e_s$.* If not, there are two
such edges into different $e_s$ that belong to different graphs: if both belong to one
$T_j$, an edge of another $T_k$ at $x$ goes into a different $e_s$ from one of them. After
renaming, $xq \in T_j$, $xr \in T_k$ with $j \ne k$, $q \in e_1$, $r \in e_2$; let $m$ be the third
index. By (C) for $xq$ and for $xr$, $T_m$ has no edge from $\bar q$ into $e_2 \cup e_3$
and avoids $e_1$, so $x\bar q \in T_m$; likewise $x\bar r \in T_m$. Now (C) for $x\bar q$
gives that $T_k$ has no edge from $q$ into $e_2 \cup e_3$, (C) for $x\bar r$ that $T_k$
avoids $e_1$, and (C) for $xq$ that $T_k$ avoids $xq$. So $q$ is isolated in $T_k$, which
is impossible.

Rename so that $s = 1$ and $e_1 = p\bar p$, and put $W = e_2 \cup e_3$. For $j = 2,3,4$ let
$P_j \subseteq \lbrace p, \bar p \rbrace$ be the set of neighbours of $x$ in $T_j$. By (C),
$T_2, T_3, T_4$ avoid $e_2$ and $e_3$, and

**(D)** *if $q \in P_j$ and $k \notin \lbrace 1,j \rbrace$, then $T_k$ has no edge from
$\bar q$ into $W$.*

Call an edge between $e_2$ and $e_3$ a cross edge. For a cross edge $h$ in some $T_m$,
$m \ne 1$, (B) for the pair $(h, e_1)$ gives:

**(O)** *the other two of $T_2,T_3,T_4$ avoid $h$ and the cross edge disjoint from $h$.*

So in $T_2,T_3,T_4$ a vertex of $W$ is joined only to $p$, to $\bar p$, or by cross edges.

*Step 2.* If $P_2 = P_3 = P_4 = \lbrace p \rbrace$, then by (D) no $T_k$ joins $\bar p$ to
$W$, and $x\bar p \notin T_k$; so $e_1$ lies in $T_2$, $T_3$ and $T_4$, against (B). The
same holds with $\bar p$. So both $p$ and $\bar p$ occur among $P_2,P_3,P_4$, and since
each $P_j$ is non-empty there are $j \ne k$ with $p \in P_j$ and $\bar p \in P_k$; let
$m$ be the third index.

*Step 3.* By (D), $T_k$ and $T_m$ do not join $\bar p$ to $W$, and $T_j$ and $T_m$ do not
join $p$ to $W$. So $T_m$ covers $W$ by cross edges alone, and contains a perfect
matching $h_1 = w_1w_1'$, $h_2 = w_2w_2'$ of the 4-cycle of cross edges, where
$e_2 = w_1w_2$ and $e_3 = w_1'w_2'$. By (O), $T_j$ and $T_k$ contain neither.

The roles of $(p,j)$ and $(\bar p,k)$ are symmetric, so let $xp \in T_m$. By (D), $T_j$
does not join $\bar p$ to $W$ either, so it covers $W$ by the cross edges
$h_3 = w_1w_2'$ and $h_4 = w_2w_1'$. By (O), $T_k$ avoids $h_3$ and $h_4$ too. Since
$p \in P_j$, (D) says $T_k$ does not join $\bar p$ to $W$; so every vertex of $W$ is
joined to $p$ in $T_k$, in particular $pw_1 \in T_k$.

Finally $T_m$ covers $\bar p$, not from $W$, so $x\bar p \in T_m$ or $p\bar p \in T_m$. In
the first case $pw_1 \in T_k$, $h_4 \in T_j$ and $x\bar p \in T_m$ are disjoint, against
(B). In the second $e_1 \in T_1 \cap T_m$ and $h_3 \in T_j$ are disjoint, against (B).
$\square$

**Computer check.** It is enough to test inclusion-minimal inputs. A minimal edge cover is
a spanning star forest, and on seven vertices with at most five edges the component
patterns are $(3,2,2)$, $(5,2)$ and $(4,3)$: 840 labelled minimal covers (315 of type
$P_3 + 2K_2$, 105 of type $K_{1,4} + K_2$, 420 of type $K_{1,3} + K_{1,2}$) and 315
four-edge covers. `code/verify_k7.py` fixes one representative of each type as the first
input and certifies every choice of the remaining three, $294{,}239{,}817$ quadruples
with no counterexample. The values of $h$ used in Case 1 are checked by
`code/verify_p1_hand_steps.py`.

## 4. High symbols and overlap excess

**Lemma 3.** *Every two high symbols occur together in at least one card.*

*Proof.* Suppose high symbols $x, y$ have disjoint supports; delete their eight cards.
If the remaining seven hold a symbol of residual degree at least three, then $x$, $y$,
that symbol and two pairwise-intersection symbols give a five-cover. Otherwise the seven
carry the $K_7$ structure of Lemma 1. Each of the four cards containing $y$, with $y$
removed, induces an edge cover of that $K_7$ of size at most five. Lemma 2 gives a
four-edge cover meeting all four; those four symbols cover the seven residual cards (they
are an edge cover) and also the four cards of $y$ (each is met in an edge). With $x$ that
is a five-cover. $\square$

For high symbols $x,y$ let $\lambda_{xy}$ be the number of cards holding both. Lemma 3
gives $\lambda_{xy} \ge 1$; and $\lambda_{xy} = 4$ would make the supports identical,
allowing one of the two to be deleted from a card and leaving a five-cover, so
$1 \le \lambda_{xy} \le 3$.

Define the total excess

$$e = \sum_{x < y} (\lambda_{xy} - 1) = \sum_A \binom{q_A}{2} - \binom{t}{2} .$$

Since a high symbol meets every other high symbol,

$$\sum_{A \ni x} (q_A - 1) \ge t - 1 . \qquad\text{(P)}$$

## 5. The weighted repetition inequality

Inside a card $A$, build a graph on its $q_A$ high symbols, joining a pair when
$\lambda \ge 2$. Let $r_A$ be its number of edges and

$$w_A = \sum_{\lbrace x,y \rbrace \subseteq A} (\lambda_{xy} - 1) .$$

That graph has no independent four-set: four high symbols with no repeated meeting cover
exactly $1 + 4 \cdot 3 = 13$ cards, and one shared symbol covers the remaining two, which
is a five-cover. A graph on $q$ vertices with $r$ edges has an independent set of size at
least $q - r$, so

$$r_A \ge \max(q_A - 3, 0), \qquad w_A \ge r_A .$$

For a full card every symbol is high, so $w_A = \sum_{B \ne A} \binom{|A \cap B|}{2} \ge
\sum_{B \ne A} (|A \cap B| - 1) = 4$, giving $w_A + 2r_A \ge 10$ there. A pair with
$\lambda = 2$ contributes 6 to $\sum_A (w_A + 2r_A)$ and a pair with $\lambda = 3$
contributes 12, so

$$6e = \sum_A (w_A + 2r_A) \ge 3(a_4 + 2a_5 + 3a_6) + a_6 . \qquad\text{(W)}$$

Equivalently, in the $a_j$ alone,

$$6a_2 + 18a_3 + 33a_4 + 54a_5 + 80a_6 \ge 6\binom{t}{2} . \qquad\text{(S)}$$

**Equality structure**, used in §7. If (W) is tight then every full card has $r_A = 3$
and $w_A = 4$; its three repeated pairs form a perfect matching, since two edges sharing
an endpoint would leave a vertex cover of size two and hence an independent four-set; and
exactly one of those three pairs has $\lambda = 3$. Every $q_A = 5$ card then has
$r_A = w_A = 2$, and cards with $q_A \in \lbrace 2,3 \rbrace$ have $r_A = w_A = 0$. So in
the equality cases a $\lambda = 3$ pair occurs only inside full cards.

## 6. The thirteen histograms

The necessary numerical conditions are

- $a_2 + a_3 + a_4 + a_5 + a_6 = 15$;
- $\sum_j j a_j = 4t$;
- $2n_2 + 3n_3 + 4t = 90$ with $0 \le n_2 \le 7$ and $n_3 \ge 0$;
- $a_3 + a_4 + a_5 \ge 2n_2$, because each of the $2n_2$ cards holding a degree-two symbol
  has $q_A \in \lbrace 3,4,5 \rbrace$;
- inequality (S).

They leave thirteen rows. By hand: put $c_A = q_A - 2 \in \lbrace 0,\dots,4 \rbrace$, so
$\sum_A c_A = 4t - 30$. Card by card, the left side of (S) is
$\sum_A (6 + 18.5 c_A - \delta(c_A))$, where the *deficit* $\delta(c_A)$ is
$0, 6.5, 10, 7.5, 0$ for $c_A = 0,1,2,3,4$. So (S) says

$$\sum_A \delta(c_A) \le B(t) := -3t^2 + 77t - 465 .$$

Call a card *middle* if $q_A \in \lbrace 3,4,5 \rbrace$. Only middle cards have positive
deficit, at least 6.5 each, and the other cards have $c_A \in \lbrace 0,4 \rbrace$, so the
values of $c_A$ on the middle cards add up to $4t - 30 \equiv 2 \pmod 4$.

- $B(t) \lt 0$ for $t \le 9$ and $t \ge 16$, and $B(10) = 5$ leaves no middle card, against
  the congruence. For $t = 11,\dots,15$, $B = 19, 27, 29, 25, 15$.
- Modulo 3, $2n_2 \equiv 90 - 4t$. At $t = 11$ and $t = 14$ this forces $n_2 \ge 2$, hence
  at least four middle cards and deficit at least $26 \gt B$. At $t = 12$ and $t = 15$ it
  gives $n_2 \in \lbrace 0,3,6 \rbrace$, and $n_2 \ge 3$ would need six middle cards (deficit at least 39),
  so $n_2 = 0$. At $t = 13$ it gives $n_2 = 1$, since $n_2 \ge 4$ needs eight middle cards (deficit
  at least 52).
- The multisets of values $c_A$ on the middle cards with sum $\equiv 2 \pmod 4$ and deficit at most 29 are
  $\lbrace 2 \rbrace$ (10), $\lbrace 1,1 \rbrace$ (13), $\lbrace 3,3 \rbrace$ (15),
  $\lbrace 1,2,3 \rbrace$ (24), $\lbrace 1,1,1,3 \rbrace$ (27) and
  $\lbrace 1,3,3,3 \rbrace$ (29); any other has deficit at least 30.
- The middle cards fix the histogram: $(4t - 30 - \sum c_{\mathrm{middle}})/4$ cards are
  full and the rest have $q_A = 2$. At $t = 15$ the first three multisets are allowed, at
  $t = 12$ the first five, and at $t = 13$ (at least two middle cards) the five from
  $\lbrace 1,1 \rbrace$ on.

This gives the thirteen rows below. `code/verify_histograms.py` enumerates the same
conditions directly, with no assumed bound on $t$ or $a_2$, and `code/verify_p1_hand_steps.py`
checks that the count above reproduces its list.

| $(n_2,n_3,n_4)$ | $(a_2,a_3,a_4,a_5,a_6)$ |
|---|---|
| (0, 10, 15) | (6, 2, 0, 0, 7) |
| (0, 10, 15) | (7, 0, 0, 2, 6) |
| (0, 10, 15) | (7, 0, 1, 0, 7) |
| (1, 12, 13) | (7, 3, 0, 1, 4) |
| (1, 12, 13) | (8, 1, 0, 3, 3) |
| (1, 12, 13) | (8, 1, 1, 1, 4) |
| (1, 12, 13) | (8, 2, 0, 0, 5) |
| (1, 12, 13) | (9, 0, 0, 2, 4) |
| (0, 14, 12) | (8, 3, 0, 1, 3) |
| (0, 14, 12) | (9, 1, 1, 1, 3) |
| (0, 14, 12) | (9, 2, 0, 0, 4) |
| (0, 14, 12) | (10, 0, 0, 2, 3) |
| (0, 14, 12) | (10, 0, 1, 0, 4) |

Passing these conditions is necessary, not sufficient: none of the thirteen is claimed to
be realizable.

## 7. Eliminating the thirteen

Throughout, (P) is the tool: a high symbol in two small cards has at most
$1 + 1 + 5 + 5 = 12$ high meetings, so at $t = 15$ (which needs 14) it cannot occur in
two small cards at all.

### $t = 15$

**(6, 2, 0, 0, 7).** Twelve high symbols lie in small cards and three do not. A high
symbol in a $q = 3$ card cannot also lie in a small card, since $1 + 2 + 5 + 5 = 13 < 14$.
So both $q = 3$ cards contain exactly the same three absent high symbols. Their
intersection then has size at least three, contributing at least two to the local excess,
while a $q = 3$ card has excess exactly one.

**(7, 0, 1, 0, 7).** Fourteen high symbols lie in small cards and one does not. A high
symbol lying in both the $q = 4$ card and a small card has at most
$1 + 3 + 5 + 5 = 14$ high meetings, so it has no repeated partner. At least three of the
four high symbols of the $q = 4$ card are of that kind, so its repeated-pair graph has no
edge, contradicting $r_A \ge 1$.

**(7, 0, 0, 2, 6).** Here $e = 12$ and (W) is tight. Each of the six full cards carries
exactly one $\lambda = 3$ pair and such pairs occur only in full cards, so there are
exactly two of them, each on three full cards. The three full cards on a fixed
$\lambda = 3$ pair $\lbrace x,y \rbrace$ meet pairwise exactly in that pair — a third
common symbol would make a triangle in a graph that must be a matching — so their union
holds 14 high symbols. If $x$ also lies in a small card $\lbrace x,z,\dots \rbrace$ then
$z$ lies outside that union, and its high-meeting total $5+5+5+1 = 16$ has exactly two
surplus meetings, both already used by $y$. If $y$ also lies in a small card, its partner
there must be that same unique outside symbol, which would put that symbol in two small
cards. So every $\lambda = 3$ pair contains the unique high symbol absent from all seven
small cards. Both pairs would then share that symbol; their triples of full cards are
disjoint, because a full card's repeated pairs form a matching; and the shared symbol
would lie in six cards, contradicting degree four.

### $t = 13$

First, $a_2 \le 7$. By (P) a high symbol in two small cards has its other two appearances
in full cards, since $1+1+4+5 = 11 < 12$; hence a high symbol in a card that is neither
full nor small lies in at most one small card. The unique degree-two symbol lies in two
cards with $q = k \in \lbrace 3,4,5 \rbrace$ and in no small card. Such a card meets at
most $k + 2(5-k) = 10 - k \le 7$ small cards. So $a_2 \le 7$, which removes the four rows
with $a_2 \in \lbrace 8,9 \rbrace$.

**(7, 3, 0, 1, 4).** Let $h$ count high symbols lying in two small cards. The numbers
lying in two, one and zero small cards are $h$, $14-2h$, $h-1$. A double-small high symbol
has exactly $1+1+5+5 = 12$ high meetings, so no repeated partner, and its two full cards
meet only in it.

For a full card write $b_i$ for the number of its high symbols lying in $i$ small cards.
It meets each of the seven small cards exactly once, so $2b_2 + b_1 = 7$, and
$b_2 + b_1 + b_0 = 6$, hence $b_2 = b_0 + 1$. Summing over the four full cards, the
zero-small high symbols have $2h - 4$ appearances in full cards. Each zero-small high
symbol must appear in some full card, since without one its meeting total is at most
$2+2+2+4 = 10 < 12$. Hence $2h - 4 \ge h - 1$, i.e. $h \ge 3$.

The $h$ double-small symbols mark distinct pairs of full cards, each marked intersection
having size one. If $h \ge 5$ then five of the six pairs have intersection one and the
last at most five, so the pairwise intersections sum to at most 10; but four sets of size
six inside thirteen symbols force that sum to be at least $24 - 13 = 11$. So
$h \in \lbrace 3,4 \rbrace$.

A zero-small high symbol lying in one full card must also lie in the $q = 5$ card $F$ and
in two of the three $q = 3$ cards; its meeting total is $5+4+2+2 = 13$, allowing exactly
one repeat.

*Case $h = 3$.* Two zero-small symbols $u,v$, each in exactly one full card, both in $F$
and each in two of the three $q = 3$ cards, so they share $F$ and at least one $q = 3$
card: that uses the single repeat each is allowed. So they lie in different full cards and
repeat nothing else. The three marked pairs give the four full cards degrees $1,2,2,1$,
a path $A - B - C - D$, with $u \in B$ and $v \in C$. The eight single-small high symbols
have 16 appearances in full cards, and none can lie in three full cards, since every
triple of $\lbrace A,B,C,D \rbrace$ contains a marked pair; so each lies in exactly two.
The allowed pairs $AC$, $AD$, $BD$ then carry $3, 2, 3$ of them. But $F$ holds $u, v$ and
three further high symbols, which cannot be double-small and cannot lie in $B$ or $C$
without repeating a meeting with $u$ or $v$; they would all have to come from the $AD$
group, which has two members.

*Case $h = 4$.* Two pairs of full cards are unmarked. Their excess over one must total at
least five, since the pairwise intersections sum to at least 11; and they cannot share a
full card, whose total intersection excess with all others is only four. So they are
disjoint, say $AB$ and $CD$, and the marked pairs form a four-cycle. Each full card then
holds two double-small symbols, one zero-small symbol and three single-small symbols.
There are three zero-small symbols with four full-card appearances, so one, $w$, lies in
$A$ and $B$, and the others $u,v$ lie in $C$ and $D$ respectively. The six single-small
symbols cannot lie in three full cards and have twelve appearances, so each lies in two:
three shared by $A,B$ and three by $C,D$. Thus $w$ already repeats meetings with three
symbols. If its other two cards were both $q = 3$, its meeting total would be
$5+5+2+2 = 14$, allowing only two surplus meetings. So $w$ lies in $F$ and one $q = 3$
card. But $u$ and $v$ each lie in $F$ and in two of the three $q = 3$ cards, and each has
used its single allowed repeat on the other; their $q = 3$ supports overlap in exactly one
card and together cover all three. So whichever $q = 3$ card holds $w$ also holds $u$ or
$v$, repeating that meeting on top of the $u,v$ repeat.

### $t = 12$

A high symbol in a $q = 3$ or $q = 4$ card cannot lie in two small cards, since
$1 + 1 + 3 + 5 = 10 < 11$.

**(9, 1, 1, 1, 3) and (10, 0, 1, 0, 4).** The $q = 4$ card holds four high symbols, each
in at most one small card, and two degree-three symbols, each in at most two; so it meets
at most $4 + 2 \cdot 2 = 8$ small cards, fewer than the nine or ten required.

**(9, 2, 0, 0, 4).** A $q = 3$ card meets at most $3 + 3 \cdot 2 = 9$ small cards, so
equality is forced everywhere. The two $q = 3$ cards cannot share a degree-three symbol
(not enough remaining appearances) nor a high symbol (its meeting total would be at most
$1+2+2+5 = 10 < 11$), so they would be disjoint.

**(10, 0, 0, 2, 3).** Each $q = 5$ card must hold at least three double-small high symbols
to meet all ten small cards; otherwise its five high symbols and one degree-three symbol
reach at most $5 + 2 + 2 = 9$. Each double-small high symbol in it has its fourth
appearance in a full card and meeting total $1+1+4+5 = 11$, so that full card meets the
$q = 5$ card only in it. With three full cards there are exactly three such symbols, one
per full card; the other two high symbols lie in one small card each and the degree-three
symbol in two. The two $q = 5$ cards cannot share their degree-three symbol or a
double-small symbol, and a shared single-small high symbol would add a second symbol to an
intersection already forced to be a singleton. So they would be disjoint.

**(8, 3, 0, 1, 3).** Here $e = 6$ and (W) is tight, so each full card has a repeated-pair
matching of size three with exactly one $\lambda = 3$ pair, and non-full cards hold no
$\lambda = 3$ pair. So there is exactly one such pair, shared by all three full cards. As
in $t = 15$, two full cards cannot share a third symbol, so their union holds
$2 + 3 \cdot 4 = 14$ high symbols, while only twelve exist.

## 8. Conclusion

**Theorem 1.** *No pairwise intersecting 6-uniform family of fifteen cards has
transversal number six. Since repeats were shown impossible after padding was allowed,
the same holds for every family of at most fifteen cards. Hence $g(6) \ge 16$.*

## 9. Verification

| claim | script |
|---|---|
| Lemma 2, all 294,239,817 quadruples | `code/verify_k7.py` |
| the values of $h$ in §3 and the deficit count of §6 | `code/verify_p1_hand_steps.py` |
| the thirteen histograms | `code/verify_histograms.py` |

The proofs of §3 and §6 are hand arguments; the scripts check the same statements
independently. The eliminations of §7 are hand arguments and are not machine-checked.

---

*This work was prepared with AI assistance (ChatGPT, OpenAI; Claude, Anthropic), used for algebraic derivation, for drafting and rewriting code and text, for running and re-running the computations, and for auditing the papers against their own scripts. The same tools were used in the review, so the review carries the same caveat. All statements were checked by the author, who is responsible for them. No priority is claimed and the result has not been independently reviewed by a human or a proof assistant; the repository README sets out the division of labour and the open obligations in full.*

## References

1. J. Barát and I. M. Wanless, *Intersecting and 2-intersecting hypergraphs with maximal
   covering number: the Erdős–Lovász theme revisited*, J. Combin. Des. 29 (2021), 260–286;
   arXiv:2011.04444.
2. V. Sivashankar, *An Improved Lower Bound for the Erdős–Lovász Cover Number Problem*,
   arXiv:2606.24878v2.
