# [P5] Lower bounds for g(r): 3r − 3 for every r, and 3.1024r for large r

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

Sivashankar [2] proved $g(r) \ge 3r-4$ for every r by deleting the cards of high-degree
symbols and bounding the cover number of what remains, a family of maximum degree three,
by $4\tau \le q+r+4$. He asked whether $+4$ can be replaced by $+3$. Theorem 1 gives a
proposed proof that it can, so $g(r) \ge 3r-3$ for every r. The residual constant $+3$
cannot be lowered [2], and $g(3) = 6$ and $g(4) = 9$ show that $3r-3$ is attained.

Theorem 2 excludes the equality case for every $r \ge 16$, so $g(r) \ge 3r-2$ there. Its
proof uses three tools in turn: a count of matching numbers for large remainders, a swap
lemma for the deleted cards, which rules out the rigid cases outright, and an anchor count
for the remaining ones. At $r = 15$ one case survives all three, and §4.5 says why.

Section 5 turns the exclusion of equality into a quantitative statement (Theorem 3),
with a gain linear in r when the remainder is large. Section 6 adds a second saving,
taken from the deleted cards, that is largest when the remainder is small. It uses a
bound on the deleted cards of the last steps of the peeling, a budget for the matching
numbers of their traces, and a rainbow matching theorem of Correia, Pokrovskiy and
Sudakov [5]. Together they give Theorem 4:
$\liminf g(r)/r \ge 3+(65-36\sqrt2)/138 = 3.1020\ldots$, above the constant
$(41-\sqrt{19})/12 \approx 3.0534$ of [2]. At the extreme point of that bound about half
of the deleted cards have traces with small matching number. Such cards still carry many
witnesses, and using them gives Theorem 5, $\liminf g(r)/r \ge 3.1024745$, where the final
minimisation is certified by interval arithmetic.

The proofs are proposed and have not been independently reviewed. Every finite step is
checked exhaustively by a script named in §7. No priority is claimed.

## 1. Setting

$g(r)$ is the least number of cards in a pairwise intersecting r-uniform family H with
$\tau(H) = r$. The known values are $g(3) = 6$, $g(4) = 9$, $g(5) = 13$ [4], and $g(6) = 17$
([P1]–[P4] of this set). Against $3r$ these are $3r-3$, $3r-3$, $3r-2$ and $3r-1$. So a
bound $g(r) \ge 3r-c$ valid for every r cannot have $c \lt 3$; a bound $3r-2$ can hold
only from $r = 5$ on, and $3r-1$ only from $r = 6$ on.

For large r, [2, §4] proves $g(r) \ge ((41-\sqrt{19})/12 - o(1))r$, about $3.053r$, for
r beyond a threshold that is not made explicit. Theorems 1 and 2 have coefficient 3 and
hold with explicit constants at every r. Theorem 4 is asymptotic, like [2], and raises
the coefficient to 3.1020 in closed form; Theorem 5 raises it to 3.1024.

**What is borrowed.** The peeling reduction, the dual triple system, the maximum matching,
the selected witnesses, the first local support bound, and the sharpness family are from
[2, §2–3]. They are recalled with proofs so that the argument can be read on its own.

**Peeling.** Delete the cards containing a symbol of current degree at least four, and
repeat until no such symbol is left. If k symbols are chosen and the remainder J has
q cards, then

$$\lvert H \rvert \ge q+4k, \qquad r \le k+\tau(J),$$

because the k chosen symbols together with any cover of J cover H. Hence a bound
$4\tau(J) \le q+r+C$ gives $\lvert H \rvert \ge 3r-C$.

**The dual view.** For a symbol v of J let $B_v$ be the set of cards containing it.
Regard the cards as points. The blocks $B_v$ have size at most three, cover every pair of
points, and every point lies in exactly r blocks. A cover of J is a set of blocks
meeting every point. For any card E,

$$q-1 \le \sum_{v \in E} (\deg v - 1) \le 2r, \qquad\text{(1.1)}$$

so $q \le 2r+1$.

Take a maximum matching $M_1, \dots, M_t$ among the distinct three-element blocks. Let C
be its union and U the other u points, so $q = 3t+u$; no three-element block lies
inside U. A defining symbol of each $M_i$ covers C, and pairing the points of U gives

$$\tau(J) \le t + \lceil u/2 \rceil . \qquad\text{(1.2)}$$

For each pair $x, y$ of U choose one symbol $w_{xy}$ in both, the *witness* of the pair.
Witnesses are distinct, since a repeated one would lie in four cards or in a triple inside
U. Each witness block is $\lbrace x,y \rbrace$ or $\lbrace x,y,z \rbrace$ with $z \in C$.

For each i let $F_i$ be the *local graph* on U whose edge $xy$ is present, with colour
z, when the witness block is $\lbrace x,y,z \rbrace$ and $z \in M_i$. The $F_i$ are simple
and edge-disjoint. Two disjoint edges of one $F_i$ never have different colours: their
blocks would replace $M_i$ by two disjoint triples. For each colour write e for its
number of edges and s for its support, and let $S_i$ be the sum of the three supports,
$S = \sum_i S_i$.

## 2. Theorem 1: the sharp residual bound

**Theorem 1 (proposed).** *Every intersecting r-uniform family J with q cards and
maximum degree at most three satisfies $4\tau(J) \le q+r+3$.*

**Corollary 1.** *$g(r) \ge 3r-3$ for every $r \ge 1$.*

*Proof.* Peeling and Theorem 1. $\square$

### 2.1 Three inequalities

*Capacity at U.* The witnesses use exactly $u(u-1)$ incidences on U. The other
$ur-u(u-1)$ incidences each reach at most two cards of C, and all $3tu$ pairs between
U and C must be met. Hence

$$3tu - S \le 2\bigl(ur-u(u-1)\bigr). \qquad\text{(2.1)}$$

*Capacity of a colour.* Fix $z \in M_i$, and let the edges of colour z in $F_i$ be e in
number, with support s. In the card z, the e witnesses cover s points of U, a
defining symbol of $M_i$ covers its other two points, and the remaining $q-3-s$ points
need the other $r-e-1$ symbols, at most two each. So

$$2e - s \le 2r - q + 1 =: d. \qquad\text{(2.2)}$$

*Local support* ([2] for the first bound).

**Lemma 1.** *Let F be a simple graph on u vertices with at most three colours, in
which disjoint edges always have the same colour. Then $S_F \le \max(12, u+4)$. If every
colour has $2e-s \le d$, then $S_F \le \max(12, u+2, d+8)$.*

*Proof.* Suppose a colour has two disjoint edges, on four vertices W. Every
other-colour edge lies in W. If no other colour is present, $S_F \le u$. If the
other-colour edges have no common vertex, every edge of the first colour meets all of them
and lies in W too, giving 12. Otherwise at most two other-colour edges exist, sharing a
vertex, with support contribution at most four, giving $u+4$. Fix one of them, g. Every
first-colour edge meets g, so $e \ge s-2$, and $2e-s \le d$ gives $s \le d+4$ and
$S_F \le d+8$.

If every colour is internally intersecting, each is a star or part of a triangle. With
all supports at most four, the sum is at most 12. Otherwise one colour is a star with at
least four leaves, every other-colour edge contains its centre, and simplicity gives
$S_F \le u+2$. $\square$

### 2.2 The preliminary inequality

**Lemma 2 ([2]).** *$r \ge u+t-2$.*

*Proof.* Put $\alpha = r-u-t+2$. If $u = 0$, (1.1) gives $\alpha \ge (r+5)/3 \gt 0$.
Otherwise (1.1), (2.1) and Lemma 1, with $K = \max(12,u+4)$, give
$t \le u-3+2\alpha$ and $\alpha \ge 1 - (K-u)t/(2u)$. A negative integer $\alpha$ would give
$t \le u-5$ and then $\alpha \gt -1$: for $K = u+4$ the bound is $-1+10/u$, and for
$K = 12$ with $u \le 8$ the needed strict inequality is $u^2-13u+60 \gt 0$, whose
discriminant is negative. $\square$

### 2.3 The odd equality case

By (1.2) and Lemma 2, if u is even then $4\tau \le 4t+2u = q+(t+u) \le q+r+2$. If u is
odd, $4\tau \le q+(t+u)+2$. So Theorem 1 follows once *u odd implies $r \ge u+t-1$*.

Suppose u is odd and, by Lemma 2, $r = u+t-2$. Then $d = u-t-3 \ge 0$, and (2.1) becomes

$$S \ge u(t+2). \qquad\text{(2.3)}$$

If $u \ge 11$, (2.3) and Lemma 1 give $t \ge u/2$. Then $d+8 \le u+2$ and $12 \le u+2$, so
every $S_i \le u+2$ and $u(t+2) \le t(u+2)$, that is $u \le t$, against $t \le u-3$.

For odd $u \le 9$, the conditions $0 \le t \le u-3$ and $u(t+2) \le t \max(12,u+4)$ leave
exactly

$$(u,t) \in \lbrace (5,2), (7,3), (7,4), (9,5), (9,6) \rbrace ,$$

with $d = 0, 1, 0, 1, 0$ respectively.

**Lemma 3 (small excess).** *If every colour has $2e-s \le 1$ and F has more than one
colour, then $S_F \le 12$, $S_F \ne 11$, and $S_F = 12$ only when F is a properly
three-coloured $K_4$. If also $u \le 9$, the same holds when F has one colour.*

*Proof.* A connected component on $v \ge 2$ vertices has $2e-v \ge v-2$, so each colour is
a matching, or one path on three vertices plus a matching. A colour with a matching of size
three leaves the other colours empty, so F has one colour and $S_F \le u \le 9$. A colour
of support five is $P_3$ plus an edge, and the other colours are then confined to two
edges, giving at most 9. Otherwise every support is at most four. Support four forces two
disjoint edges, and two cross-intersecting two-edge matchings are two perfect matchings of
one $K_4$; a third colour must be the third. $\square$

*The cases $d = 1$.* For $(9,5)$, (2.3) asks $S \ge 63$ and Lemma 3 allows 60. For
$(7,3)$, (2.3) asks 35, so all three $S_i$ are 12: three edge-disjoint copies of $K_4$
on seven vertices. Two such copies meet in one vertex and leave $K_{3,3}$ plus an isolated
vertex, which holds no third $K_4$.

*The cases $d = 0$.* Now every colour is a matching and $q = 2r+1$, so (1.1) is an
equality for every card: every symbol has degree three and any two cards meet once. So
every witness block is a triple and the $F_i$ partition the edges of $K_u$. For $(5,2)$,
$qr = 55$ is not divisible by three. For $u \le 9$ a local graph has at most six edges: one
colour is a matching of at most four edges, and with several colours each is a matching of
at most two, since a third disjoint edge would meet no other-colour edge. Six edges occur
only as the three perfect matchings of a $K_4$, and five only as $K_4$ minus an edge. For
$(9,6)$ the 36 edges of $K_9$ would split into six copies of $K_4$, needing degree 8
divisible by three. For $(7,4)$ the 21 edges of $K_7$ split into four parts of size at
most six only as $6+6+6+3$, $6+6+5+4$ or $6+5+5+5$; two edge-disjoint $K_4$ leave $K_{3,3}$
plus a vertex, which excludes the first two. In the third, after one $K_4$ on four
vertices, each copy of $K_4$ minus an edge contains a triangle and so takes one of the three
edges among the other three vertices; it is then two of the four joined to two of the
three, plus that edge. The three pairs among the three are distinct and meet, so
edge-disjointness needs three disjoint pairs among four vertices, which is impossible.

This proves Theorem 1. $\square$

### 2.4 Sharpness, and degree four

For odd n take points $1, \dots, n$ and one symbol for each pair ([2]). Then $q = n$,
$r = n-1$, a cover is an edge cover of $K_n$, and $\tau = (n+1)/2$, so $4\tau = q+r+3$.

**Corollary 2.** *If J has maximum degree at most four, then $4\tau(J) \le q+r+3$.*

*Proof.* Take a maximal matching of a four-element blocks; their defining symbols cover
$4a$ cards and the rest has maximum degree three. $\tau \le a + (q-4a+r+3)/4$. $\square$

Peeling at degree five then gives $\lvert H \rvert \ge (15r-q-15)/4$ for the size q of
the remainder, which improves the additive term in the corresponding step of [2] but not
its coefficient.

## 3. The equality case

From here to §4, suppose $\lvert H \rvert = 3r-3$ and $\tau(H) = r$ with $r \ge 5$.

### 3.1 The parameters

If H had a symbol of degree at least five, peeling it first would give
$\lvert H \rvert \ge \lvert J \rvert + 4(r-\tau(J)) + 1 \ge 3r-2$ by Theorem 1. If every
degree were at most three, $3r-3 \le 2r+1$ would force $r \le 4$. So the maximum degree is
four. (At $r = 3$ and $r = 4$ the bound $3r-3$ is attained, and this is where the argument
stops.)

Take a maximum matching of a four-element blocks. Their $4a$ cards form a *groups* of
four, and each group has its *group symbol*. Delete them and let J be the rest, of maximum
degree three and $q = 3r-3-4a$ cards. The a group symbols and a cover of J cover H, so
$\tau(J) \ge r-a$, while Theorem 1 gives $4\tau(J) \le q+r+3 = 4(r-a)$. So Theorem 1 is an
equality for J, which by §2.3 forces u odd, $\tau(J) = r-a$, $r = u+t-1$ and
$q = 3t+u$. Consequently

$$u = 2a+3, \quad t = r-2a-2, \quad d = u-t-1 \ge 0, \quad r = 2u-2-d, \qquad\text{(3.1)}$$

and (2.1) becomes $S \ge ut$. Write $H_0 = (u-1)/2$.

The number $d = 2r-q+1$ measures the slack in (1.1). When $d = 0$ every symbol of a card of
J has degree three in J; as d grows, symbols of degree two and one are allowed.

### 3.2 Local bounds

**Lemma 4 (pointwise capacity).** *For $x \in U$ let $S_x$ be the number of cards of C
met by the witnesses at x. Then $S_x \ge t$. In one $F_i$, if x carries E edges in
k colours, then $E-k \le d$.*

*Proof.* The card x has exactly $u-1$ witnesses, so exactly $r-(u-1) = t$ other symbols.
They meet at most $2t$ cards of C, and all $3t$ must be met, so $3t-S_x \le 2t$. The
$u-1$ witnesses at x reach $S_x$ distinct cards of C, so the number of witnesses
"wasted" at x is $u-1-S_x \le u-1-t = d$. Edges of one colour at x reach one card, so
E edges in k colours waste $E-k$. $\square$

**Lemma 5.** *Every $F_i$ with more than one colour has $S_i \le \max(12, d+8)$ and
$S_i - e(F_i) \le 6$. A one-coloured $F_i$ has $S_i - e(F_i) \le H_0$.*

*Proof.* The first case of Lemma 1 already gives $\max(12,d+8)$. In the star case, $F_i$
is a star at one vertex with E edges in $k \le 3$ colours, and
$S_i = E+k \le d+2k \le d+6$ by Lemma 4. For the second bound: with two disjoint edges of
one colour on W, either every support lies in W and each colour has $s-e \le 2$, or at
most two other-colour edges exist, contributing at most two, while the first colour has
$e \ge s-2$. Otherwise every colour is a star or triangle with $s-e \le 1$. A one-coloured
graph has $s-e$ at most its number of components, at most $H_0$. $\square$

### 3.3 Two augmentation bounds

Call a one-coloured $F_i$ *large* if its matching number is at least four, and let m be
their number.

**Lemma 6.** *$2m \le t$.*

*Proof.* A large $F_i$ uses one colour $z_i$; its other two points of $M_i$ are met by no
witness. So every $x \in U$ must meet those $2m$ points with its t non-witness symbols. No
such symbol meets two of them. Within one $M_i$, its triple and an edge of $F_i$ avoiding
x would replace $M_i$ by two triples. Across $M_i$ and $M_j$, an edge of $F_i$ avoiding
x and an edge of $F_j$ avoiding x and those two endpoints, which matching number four
provides, give three triples in place of two. Either way the matching was not maximum.
$\square$

**Lemma 7.** *$u \le \max(12, d+8)$.*

*Proof.* Suppose not. By Lemma 5 every $F_i$ with more than one colour has $S_i \lt u$,
and a one-coloured $F_i$ has $S_i \le u$. Since $S \ge ut$, every $F_i$ is one-coloured
and spans U. Then $2e-u \le d$ gives $e \le (u+d)/2$, and its matching number is at least
$u-e \ge (u-d)/2 \gt 4$. So $m = t$, and Lemma 6 forces $t = 0$, whereas
$t = u-d-1 \ge 8$. $\square$

### 3.4 The swap lemma

The groups come from a *maximum* matching of four-element blocks. That alone constrains
every deleted card.

**Lemma 8 (swap).** *Let $A \ne A'$ be deleted cards of the same group. If $w \in A$ and
$w' \in A'$ are symbols of degree three in J, their sets of cards of J meet.*

*Proof.* w lies in A and in three cards of J, so it has degree four in H and its
block is $\lbrace A \rbrace \cup T$ with T three cards of J; likewise
$\lbrace A' \rbrace \cup T'$. Neither block meets another group. If $T \cap T' = \emptyset$,
the two blocks are disjoint, and putting them in place of the group's own block gives
$a+1$ disjoint four-element blocks, against maximality. $\square$

Call such T a *triple* of A. Every symbol that a deleted card shares with a card of J
is a symbol of J, so a deleted card meets J through triples and through symbols of
degree two or one in J.

**Proposition 1.** *In the equality setting $d \ne 0$, and $d \ne 1$ when $r \ge 11$.*

*Proof.* Take a group; it has four cards.

*$d = 0$.* By §2.3, $q = 2r+1$ and every symbol of a card of J has degree three in J.
So a deleted card A meets the $2r+1$ cards of J through at most $r-1$ triples. Fix one,
T. If the other at most $r-2$ all met T, they would reach at most $3 + 2(r-2) = 2r-1$
cards; so A has a triple $T'$ disjoint from T. By Lemma 8 every triple of a group-mate
$A'$ meets both T and $T'$, so reaches at most one of the $2r-5$ cards outside them. With
at most $r-1$ triples, $A'$ misses one, since $r-1 \lt 2r-5$ for $r \ge 5$.

*$d = 1$.* Now $q = 2r$, and (1.1) allows each card of J at most one symbol of degree two
and none of degree one. So J has at most $q/2 = r$ symbols of degree two, each in at most
two deleted cards, since degrees in H are at most four: at most $2r$ incidences with
deleted cards. A deleted card whose triples pairwise meet reaches at most $1 + 2n_3$ cards
through $n_3$ triples and two through each other symbol, at most $1 + 2(r-1) \lt 2r$ in
all; so every deleted card has two disjoint triples. For a group-mate $A'$ with $n_2$
symbols of degree two, the $2r-6$ cards outside those two triples are reached at most once
per triple and twice per symbol of degree two, so $2r-6 \le (r-1) + n_2$ and
$n_2 \ge r-5$. Every deleted card is such a group-mate, so the $4a \ge 4$ deleted cards need
at least $4(r-5)$ incidences, more than $2r$ when $r \ge 11$. $\square$

## 4. Theorem 2: excluding equality from r = 16

**Theorem 2 (proposed).** *$g(r) \ge 3r-2$ for every $r \ge 16$.*

### 4.1 The deleted cards and their matching numbers

For each of the $4a$ deleted cards A let $L_A$ be the graph on U whose edge $xy$ is
present when $w_{xy} \in A$; write $e_A$, $s_A$, $\nu_A$ for its edges, support and matching
number. Let $T = \sum_i e(F_i)$ and $D = S - T$.

A witness of degree two in J lies in at most two deleted cards, one of degree three in
at most one, since degrees in H are at most four; so $\sum_A e_A \le u(u-1) - T$. Let
$M = \sum_A (u - s_A)$. For $x \in U$ its t non-witness symbols have room for at most
$3t$ other cards of H; they must meet the $3t-S_x$ cards of C not met by witnesses, and
every deleted card A whose graph misses x. So at most $S_x$ deleted cards miss x, and
$M \le S$. Using $\nu_A \ge s_A - e_A$ and $4a = 2u-6$,

$$\sum_A \nu_A \ge u^2 - 5u - D. \qquad\text{(4.1)}$$

**Lemma 9.** *Within one group there are no three disjoint edges from three different
graphs $L_A$.*

*Proof.* Extend them to a matching of $H_0$ edges of the complete graph on U, leaving
one point x. The witnesses of these edges cover U except x and meet three cards of the
group; one symbol of x that lies in the fourth card covers both. With the t defining
symbols of C and the $a-1$ group symbols of the other groups this is a cover of H of
size $H_0 + 1 + t + a - 1 = r-1$. $\square$

**Lemma 10.** *Three graphs each with a matching of size four and a fourth nonempty graph
contain three disjoint edges from three different graphs.*

**Lemma 11.** *The same holds for four graphs with matching numbers at least
$3, 3, 4, 4$.*

*Proof of both.* Fix size-four matchings $P, Q$ in two of the graphs and suppose no such
triple exists. Call an edge e of another graph *blocked* if no two disjoint edges, one
from P and one from Q, avoid it; every edge of the other graphs is blocked. The edges
of P and of Q avoiding a blocked edge must cross-intersect. Each side keeps at least
two, and one edge cannot meet three disjoint edges, so exactly two survive on each side
and they form a four-cycle, which is a component of $P \cup Q$, with both ends of e in
both supports. The other graphs supply three disjoint blocked edges (a size-three matching
for Lemma 11, a size-four matching for Lemma 10). Their six endpoints lie in both supports,
and outside one such four-cycle there are at most four such vertices, so some of them
touches it and yields a second four-cycle. So $P \cup Q$ is two disjoint four-cycles on
the same eight vertices, and every blocked edge is a diagonal of one of them.

For Lemma 11 the two size-three matchings each consist of three of the four diagonals.
The first has both diagonals of one cycle and the second at least one of them; take that
one for the second, the other for the first, and an edge of P in the other cycle. For
Lemma 10 the three size-four matchings are the three perfect matchings of each of the two
copies of $K_4$. Take an edge f of the fourth graph. If f removes two vertices of one
copy, the edge on its other two vertices and an edge of a different matching in the other
copy avoid f. If f removes at most one vertex of each copy, each copy keeps a triangle
or all of $K_4$, which contains all three matchings, so two edges of different matchings
avoid f. In every case a rainbow triple exists. $\square$

Order the matching numbers of one group as $v_1 \le v_2 \le v_3 \le v_4$. Greedy choice
gives a rainbow triple when $v_2 \ge 1$, $v_3 \ge 3$ and $v_4 \ge 5$. With Lemmas 9–11,
every group has $v_2 = 0$, or $v_3 \le 2$, or all $v_i \le 4$ with neither $v_1 \ge 1$ and
$v_2 = v_3 = v_4 = 4$ nor $v_1, v_2 \ge 3$ and $v_3 = v_4 = 4$. So the sum is at most
$\max(2H_0, H_0+6, 13)$, and with (4.1):

$$D \ge \frac{u^2-6u-3}{2} \quad (u \ge 15), \qquad D \ge 39 \quad (u = 13). \qquad\text{(4.2)}$$

### 4.2 Large remainders: u is at most 11

*$u \ge 15$.* By Lemma 7, $d \ge u-8$ and $t = u-d-1 \le 7$. By Lemma 5,
$D \le 7H_0 = 7(u-1)/2$. With (4.2) this gives $u^2-13u+4 \le 0$, false for $u \ge 13$.

*$u = 13$.* Lemma 7 gives $d \ge 5$. If $d \ge 6$ then $t \le 6$ and $D \le 6t \le 36$,
against (4.2). If $d = 5$ then $t = 7$ and every $S_i \le 13$, so $S \ge 91$ forces every
$S_i = 13$. A one-coloured $F_i$ then has $e \le 9$ and matching number at least four, so it
is large and $S_i - e \le 6$. A multicoloured $F_i$ cannot be the star case of Lemma 5,
which gives at most $d+6 = 11$, so $S_i = 13 = d+8$ is the extremal case of Lemma 1: two
other-colour edges $pa$, $pb$, and a first colour made of $ab$ and six edges at p, so
$S_i - e = 13 - 9 = 4$. Lemma 6 gives $m \le 3$, so $D \le 6 \cdot 3 + 4 \cdot 4 = 34$,
against (4.2).

So $u \le 11$.

### 4.3 u = 11: the anchor count

Call $(x, c)$ *open* in a local graph $F_j$ if no edge of colour c meets x and every
edge of the other two colours does. Let $A_j$ be the number of open pairs of $F_j$.

For a local graph $F_i$ and $x \in U$, let $P_x$ be the set of colours of $F_i$ with no
edge at x; their points of $M_i$ are not reached by the witnesses at x. Call a pair of
colours in $P_x$ *forbidden* if $F_i$ has an edge of the third colour avoiding x, and
call $c \in P_x$ *good* if, for every pair f of U that avoids x and is not an edge of
$F_i$, some edge of $F_i$ of a colour other than c avoids both x and f. For a set
$R \subseteq P_x$ whose pairs are all forbidden, put $g_x$ equal to the size of R, minus
the number of colours of $P_x$ outside R, minus the number of colours of R that are
not good; take the best R, and let $G = \sum_x \max(g_x, 0)$, the *anchor value* of
$F_i$.

**Lemma 12 (demand).** *If $F_i$ has anchor value G, the other local graphs have at
least $tu + G - S$ open pairs in all.*

*Proof.* Fix x and R. The t non-witness symbols of x must reach the $3t - S_x$
cards of C that its witnesses miss, among them the points of R. No symbol reaches two
points of R: its block and an edge of the third colour avoiding x would replace $M_i$
by two triples. So $\lvert R \rvert$ distinct symbols reach the points of R, each
reaching at most one further card, and the other $t - \lvert R \rvert$ reach at most two
each. The $\lvert R \rvert$ symbols therefore reach at least $t + \lvert R \rvert - S_x$
further cards missed by the witnesses, of which at most one per colour of $P_x$ outside
R lies in $M_i$.

Let $\lbrace x, c, q' \rbrace$ be such a symbol with $c \in R$ good and $q' \in M_j$,
$j \ne i$. No edge of colour $q'$ in $F_j$ meets x, since the witnesses at x miss $q'$.
If an edge f of $F_j$ of another colour avoided x, goodness gives an edge e of $F_i$
of a colour other than c avoiding x and f, and the blocks of
$\lbrace x, c, q' \rbrace$, e and f are three disjoint triples in place of $M_i$ and
$M_j$. So $(x, q')$ is open in $F_j$. Distinct $q'$ give distinct pairs, and each colour of
R that is not good spoils at most one. So at least $t + g_x - S_x$ open pairs come from
x. Summing over the x with $g_x \gt 0$ and using $S_x \ge t$ for the rest gives
$tu + G - S$. $\square$

Three anchors matter. A properly three-coloured $K_4$ on W has $G = 3(u-4)$: for
$x \notin W$ all three colours are missing, every pair is forbidden, and every colour is
good, since the other two colours form a four-cycle on W and a pair f outside $F_i$
meets W in at most one point. A spanning one-coloured large $F_i$ has $G = 2u$: for every
x its two unused colours are missing, forbidden together, and good, since a matching of
size four leaves an edge avoiding x and f. The graph $Y_k$, with edges $pa$ and $pb$ of
two colours and a third colour made of $ab$ and k edges at p, has $G = 2(u-3)$.

**Lemma 13 (finite check).** *Let $u = 11$ and $1 \le d \le 4$. Every local graph with more
than one colour has at most $12 - S_j$ open pairs, and every one with $S_j \ge 11$ has
anchor value at least 16. A one-coloured graph of support s has $11 - s$ open pairs,
plus two for each vertex common to all its edges.*

The one-coloured count is direct. The rest is checked over every multicoloured local graph
on eleven vertices that satisfies (2.2) and Lemma 4: those with $S_j \ge 11$ are the $K_4$
and $Y_4$, and at $d = 4$ also $Y_5$, with anchor values 21, 16 and 16.

**Proposition 2.** *In the equality setting, $u = 11$ with $1 \le d \le 4$ is impossible.*

*Proof.* Here $t = 10-d$, every $S_j \le 12$ by Lemma 5, and $S \ge 11t$. So
$\sum_j (12 - S_j) \le t \le 9$ and some $S_j \ge 11$. That $F_j$ is an anchor with
$G \ge 16$: by Lemma 13 if it has several colours, and otherwise it spans U with at most
$(11+d)/2 \le 7$ edges, hence matching number at least four and $G = 22$. By Lemma 12 the
other local graphs carry at least $11t + 16 - S$ open pairs.

By Lemma 13 a local graph carries at most $12 - S_j$ open pairs, except a one-coloured one
whose edges share a vertex. A star with k leaves has $12 - S_j = 11 - k$ and carries one
more; a single edge or an empty graph would need $12 - S_j \ge 10 \gt t$. A star needs
$11 - k \le t$ and, by (2.2), $k \le d+1$, so $k = d+1$ and it uses the whole budget; at
most one occurs. So the local graphs carry at most $12t - S + 1$ open pairs, and
$11t + 16 \le 12t + 1$ would need $t \ge 15$. $\square$

### 4.4 Proof of Theorem 2

Suppose $r \ge 16$ and $\lvert H \rvert = 3r - 3$ with $\tau(H) = r$. By §4.2, $u \le 11$,
and $r = 2u - 2 - d$. If $u \le 9$ then $r \le 16 - d$, so $r = 16$, $u = 9$ and $d = 0$,
excluded by Proposition 1. If $u = 11$ then $d = 20 - r \le 4$: $d = 0$ is excluded by
Proposition 1 and $1 \le d \le 4$ by Proposition 2. So $\lvert H \rvert \ge 3r - 2$ by
Corollary 1. $\square$

### 4.5 What stops at r = 15

At $r = 15$ the cases are $(u,d,t) = (9,1,7)$ and $(11,5,5)$. The first is excluded by
Proposition 1. The second is open, and both tools lose their grip on it for the same
reason.

At $d = 5$ a local graph can be a star, all its edges at one vertex in three colours, with
$S_j = 11 = u$. A star forces nothing: an edge through its centre meets every edge of it,
so no colour is good and its anchor value is 0. The supply bound of Lemma 13 also fails
there, for $4{,}536$ multicoloured graphs.

The swap lemma fails for a similar reason. With $d = 5$ each card of J may carry up to
five units of slack, so J may have up to 65 symbols of degree two, with up to 130
incidences with deleted cards. Lemma 8 makes each group need at least 18 of them, 72
in all, which the supply covers. A deleted card can also meet J as a star, all its
triples through one card of J, and stars at a common centre always meet.

So Theorem 1 gives only $g(15) \ge 42$. Together with [4] and [P1]–[P4], the bound
$g(r) \ge 3r-2$ is known for $r = 5$, 6 and $r \ge 16$, and open for $7 \le r \le 15$.

## 5. Theorem 3: a gain linear in r

Drop the equality assumption. For the remainder J of degree-four peeling put

$$\ell = r-u-t+1, \qquad h = t+\ell, \qquad d = 2r-q+1 ,$$

so that $d = u-t-1+2\ell$. Every $x \in U$ has exactly h non-witness symbols, and (1.2)
gives $B := q+r+3-4\tau(J) \ge \ell$. With $L = \max(12, d+8)$, call a one-coloured local
graph *large* if its matching number is at least four, and let m be their number.

**Lemma 14.** *In this general setting:*

*(a) $S_x \ge t-2\ell$ for every $x \in U$, so $S \ge u(t-2\ell)$ and $u-1-S_x \le d$.*

*(b) In every $F_i$, disjoint edges have the same colour, every colour has $2e-s \le d$,
and a vertex carrying E edges in k colours has $E-k \le d$.*

*(c) Every $F_i$ that is not large has $S_i \le L$.*

*(d) $2m \le h$.*

*Proof.* (a) The h non-witness symbols of x have degree at most three in J, so each
meets at most two further cards, and all $3t$ cards of C must be met: $3t-S_x \le 2h$.

(b) Two disjoint edges of different colours give two disjoint triples in place of $M_i$.
A card c of $M_i$ meets the other $q-1$ cards with r symbols of degree at most three,
so its total over-coverage is at most $2r-(q-1) = d$; the witnesses through c cover
$2e$ incidences on s vertices. The $u-1$ witnesses at x reach $S_x$ distinct cards.

(c) If $F_i$ has more than one colour, Lemma 1 with (b) gives $\max(12, u+2, d+8)$, and in
its star case every edge passes through one vertex p, so (b) at p gives
$S_i = E+k \le d+2k \le d+6$. If $F_i$ has one colour and matching number at most three,
a minimum edge cover of its support is a star forest with at most three components, so
$e \ge s-3$ and $2e-s \le d$ gives $S_i = s \le d+6$.

(d) The argument of Lemma 6 uses only the maximality of the triples. A large $F_i$ uses
one colour, so its other two points of $M_i$ are met by no witness, and every x reaches
these $2m$ points through its h non-witness symbols. A symbol reaching two points of one
$M_i$, together with an edge of $F_i$ avoiding x, gives two triples in place of one; a
symbol reaching points of $M_i$ and $M_j$, together with an edge of $F_i$ avoiding x and
an edge of $F_j$ avoiding x and that edge, gives three triples in place of two. $\square$

**Theorem 3.** *If $u \gt L$ then*

$$\ell \ge \frac{(u-L)(u-d-1)}{3u+L}. \qquad\text{(5.1)}$$

*Proof.* By Lemma 14, $u(t-2\ell) \le S \le Lt + (u-L)m \le Lt + (u-L)(t+\ell)/2$, which
rearranges to $(u-L)t \le (5u-L)\ell$; substitute $t = u-d-1+2\ell$. $\square$

**Corollary 3.** *If the degree-four peeling of H leaves a remainder with
$q \ge 2r-3$, then $\lvert H \rvert \ge \lceil (28r-67)/9 \rceil$.*

*Proof.* Here $d \le 4$ and $L = 12$. For $u \gt 12$, (5.1) gives $\ell \ge (u-21)/3$, and
with $r = 2u-d-2+3\ell$ this is $\ell \ge (r-40)/9$. For $u \le 12$, $r \le 22+3\ell$ gives
the same for $r \ge 13$, and for smaller r the bound is negative. So
$B \ge (r-40)/9$, and $\lvert H \rvert = 3r-3+E+B+4C$ (6.1) gives the claim. $\square$

**The gain at every remainder size.** Write $q = \gamma r$ with $1 \le \gamma \le 2$ and
$\lambda = \ell/r$. Minimising (5.1) over u, with $r = 2u-d-2+3\ell$, gives
$\lambda \ge c(\gamma) - o(1)$, where

$$c(\gamma) = \frac{20-4\gamma-\sqrt{(20-4\gamma)^2-108(\gamma-1)^2}}{54}. \qquad\text{(5.2)}$$

If instead $u \le L$, then $\lambda \ge (\gamma-1)/3 - o(1)$, which is at least $c(\gamma)$:
with $a = \gamma-1$, c is the smaller root of $27y^2-(16-4a)y+a^2$, whose value at $a/3$
is $\frac{16}{3}a(a-1) \le 0$. The gain is $1/9$ at $q = 2r$, about 0.057 at $q = 1.8r$,
about 0.019 at $q = 1.5r$ and 0 at $q = r$. For $q \lt r$ the bound $t \ge 0$ gives
$\lambda \ge 1-\gamma$ directly. Differentiating the quadratic,
$c'(\gamma) = (4c+2(\gamma-1))/(20-4\gamma-54c)$, which is positive, and below $1/4$ for
$1 \le \gamma \le 1.81$.

## 6. Theorems 4 and 5: a coefficient above 3.0534

Stability alone gives nothing near $q = r$. This section adds a second saving, taken from
the deleted cards, which is largest exactly there. Together they give Theorem 4.

### 6.1 Bookkeeping and the clean tail

From here on the peeling always deletes a symbol of **maximum** current degree. For the
resulting peeling, with $n = \lvert H \rvert$ and k steps, put

$$E = n-q-4k, \qquad B = q+r+3-4\tau(J), \qquad C = k+\tau(J)-r .$$

E and C are non-negative, and so is B, by Theorem 1. Then exactly

$$n = 3r-3+E+B+4C. \qquad\text{(6.1)}$$

The maximum degree never increases, so after the last step that deletes five or more cards
every step deletes exactly four. Call these the *clean* steps, their cards the clean
cards, $N_c$ in number, and each step's four cards a clean *group*. Let $k_0$ be the
number of the other steps. Each of them deletes at least five cards, so $E \ge k_0$, and
all of the excess E falls in them, so they delete $4k_0+E$ cards. With (6.1) and
$G := B+4C$ this gives

$$N_c = 3r-3-q+G-4k_0. \qquad\text{(6.2)}$$

Let $H'$ be J together with the clean cards; it has maximum degree at most four.

**Lemma 15 (clean tail).** $N_c \le 3r-q+1$. *Hence $G \le 4k_0+4$.*

*Proof.* Let A be a clean card with group symbol g. Every other symbol v of A has
some degree $j_v$ in J, and $j_v+1 \le 4$. The card A meets all q cards of J, so
$\sum_{v \ne g} j_v \ge q$. It meets the $N_c-4$ clean cards outside its group, never
through g, and v lies in at most $3-j_v$ clean cards other than A. Adding,
$q+N_c-4 \le 3(r-1)$. The second claim is (6.2). $\square$

### 6.2 Saving group symbols

A *natural cover* of J is made of the t triples of the maximum matching and the
witnesses of a pairing of U, plus one symbol for the leftover point when u is odd. It
has $t+\lceil u/2 \rceil = \tau(J)+s$ symbols, $s \ge 0$, and $B = \ell+4s$ for odd u,
$B = \ell+2+4s$ for even u.

**Lemma 16 (saving).** *If a natural cover meets every card of $b_4$ clean groups and all
but one card of $b_3$ others, then $C+s \ge b_4+\lfloor b_3/2 \rfloor$.*

*Proof.* The cover and the k group symbols cover H with $r+C+s$ symbols. Drop the
symbols of the $b_4$ groups. Pair the $b_3$ others: their two missed cards meet, so one
common symbol replaces two group symbols. The result still covers H, so it has at least
r symbols. $\square$

So $G \ge \ell+4(b_4+\lfloor b_3/2 \rfloor)$, and in particular $G \ge \ell$.

### 6.3 Traces and the budget

For a clean card A its *trace* $L_A$ is the graph on U with an edge $xy$ whenever the
witness $w_{xy}$ lies in A. Let $s_A$ be its number of non-isolated vertices and $\nu_A$
its matching number. A minimum edge cover of the non-isolated vertices is a star forest,
and one edge from each star is a matching, so $\nu_A \ge s_A-e(L_A)$. Also
$\nu_A \le \lfloor u/2 \rfloor$. Let $M_0 = \sum_A (u-s_A)$ count the missed vertices.

**Lemma 17.** $M_0 \le S+3u\ell$.

*Proof.* Fix x. A clean card A with x isolated in $L_A$ still meets x, through one
of its h non-witness symbols v; a group symbol lies in no card of J. Such v has
$j_v \ge 1$ and lies in at most $4-j_v$ clean cards. These symbols reach the $3t-S_x$ cards
of C that the witnesses miss, so $\sum_v (j_v-1) \ge 3t-S_x$, and the number of such A
is at most $\sum_v (4-j_v) \le 3h-(3t-S_x) = S_x+3\ell$. $\square$

Let $T = \sum_i e(F_i)$ and $D = S-T = \sum_i (S_i-e(F_i))$.

**Lemma 18.** $D \le 6t+uh/4$.

*Proof.* An $F_i$ with more than one colour has $S_i-e(F_i) \le 6$: the proof of the
second bound of Lemma 5 uses only that disjoint edges have the same colour, which
Lemma 14(b) gives here. A one-coloured $F_i$ has $S_i-e(F_i) = s-e$, at most its number
of components, which is at most its matching number: at most three if it is not large,
and at most $\lfloor u/2 \rfloor$ if it is. With m large graphs,
$D \le 6(t-m)+m\lfloor u/2 \rfloor$, and $2m \le h$ by Lemma 14(d). $\square$

**Lemma 19 (budget).** *Summed over the clean cards,*

$$\sum_A \left(1-\frac{2\nu_A}{u}\right) \le 3\ell+4+4k_0-G+\frac h2+\frac{12t}{u}.$$

*Proof.* By $\nu_A \ge s_A-e(L_A)$, the sum of $u-2\nu_A$ is at most
$2M_0-N_cu+2\sum_A e(L_A)$. A witness of degree j in J lies in at most $4-j$ clean
cards. The witnesses of degree three are exactly the edges of the $F_i$, T in number, so
$\sum_A e(L_A) \le u(u-1)-T$. With Lemma 17 the sum is at most
$2D+6u\ell+2u(u-1)-N_cu$. Divide by u, use Lemma 18, and substitute (6.2) with
$q = 3t+u$ and $t = r-u+1-\ell$. $\square$

Every term on the left lies in $[0,1]$.

### 6.4 Hitting many cards at once

**Theorem ([5], Theorem 1.2).** *For all sufficiently large N, an N-edge-coloured
multigraph in which every colour class is a matching of at least $N+20N^{15/16}$ edges has
a rainbow matching using every colour.*

**Lemma 20.** *Let N be large and let $\mathcal A$ be a set of N clean cards with
$\nu_A \ge N+20N^{15/16}$ for each. Then one natural cover meets every card of
$\mathcal A$.*

*Proof.* Give a maximum matching of each $L_A$ the colour A; a pair that serves two cards
becomes two parallel edges. The rainbow matching gives disjoint pairs, one per card, and
the witness of the pair coloured A lies in A. Extend to a pairing of U. $\square$

**Lemma 21 (allocation).** *Fix $0 \lt \theta \lt 1/2$ and call a clean card good if
$\nu_A \ge \theta u$. Let b be the number of the others. Then $b(1-2\theta)$ is at most
the right side of Lemma 19, and if any N good cards can be met at once, some natural
cover has*

$$b_4+\lfloor b_3/2 \rfloor \ge \min\left(\frac N6,\ \frac{N_c}{4}-\frac b2\right)-1.$$

*Proof.* A card that is not good has $1-2\nu_A/u \gt 1-2\theta$; use Lemma 19. For the
second claim let $g_4$ groups have no bad card and $g_3$ exactly one, so
$b \ge g_3+2(N_c/4-g_4-g_3)$. If $g_4 \ge N/4$, meet all four cards of
$\lfloor N/4 \rfloor$ such groups. Otherwise meet all cards of the $g_4$ groups and three
good cards of $\min(g_3, \lfloor (N-4g_4)/3 \rfloor)$ others. Since
$g_3 \ge N_c/2-b-2g_4$, this saves at least $g_4+\frac12\min(N_c/2-b-2g_4,\ (N-4g_4)/3)-1$,
which is at least $\min(N_c/4-b/2,\ N/6+g_4/3)-1$. $\square$

### 6.5 The theorem

$$x_* = \frac{65-36\sqrt2}{138} = 0.10208921\ldots$$

**Theorem 4.** $\displaystyle \liminf_{r \to \infty} \frac{g(r)}{r} \ge 3+x_* = 3.10208921\ldots$

As a decimal coefficient this is 3.1020, rounded down. It improves the constant
$(41-\sqrt{19})/12 \approx 3.0534$ of [2].

*Proof.* Suppose not. Take $\varepsilon \gt 0$ and families with $r \to \infty$ and
$n/r \le 3+x_*-\varepsilon$, and pass to a subsequence along which the normalised
quantities below converge. If J is empty the group symbols cover H, so $n \ge 4r$. Write

$$x = \frac nr-3,\quad z = \frac Gr,\quad \lambda = \frac{\ell}{r},\quad \gamma = \frac qr,\quad \sigma = \frac{4k_0-G}{r},\quad v = \frac ur = \frac{3-\gamma-3\lambda}{2},$$

and $t/r = (\gamma-1+\lambda)/2$, $h/r = (\gamma-1+3\lambda)/2$. In the limit:

- $\sigma \ge 0$ (Lemma 15), $x = E/r+z \ge k_0/r+z$, so $x \ge \frac54 z+\frac14\sigma$;
- $z \ge \lambda$ (Lemma 16), and so $\lambda \le z \le \frac45 x \lt \frac1{12}$;
- $\lambda \ge c(\gamma)$ for $1 \le \gamma \le 2$ and $\lambda \ge 1-\gamma$ for
  $\gamma \lt 1$ (§5; $\gamma \le 2$ since $d \ge 0$);
- by (6.2), $N_c/r$ tends to $N := 3-\gamma-\sigma$;
- by Lemma 19, $\frac1r\sum_A(1-2\nu_A/u)$ has limit at most
  $M := \sigma+\frac14(\gamma-1+15\lambda)$.

Since $\lambda \lt 1/12$, $\gamma \le 2$ and $\sigma \ge 0$, we have $v \gt 0.37$ and
$v/N \ge 3/8$. Put

$$K = 2(N-2M) = 7-3\gamma-15\lambda-6\sigma .$$

We show $x \ge (15\lambda+7-3\gamma)/24$.

*If $K \le 0$*, then $\sigma \ge (7-3\gamma-15\lambda)/6$, and $x \ge \frac54\lambda+\frac14\sigma$
gives the claim.

*If $K \gt 0$*, fix $\theta = K/(20v)$. Since the left side of Lemma 19 is non-negative,
$M \ge 0$, so $K \le 2N$ and $\theta \le 2N/(20v) \le 4/15$. Apply Lemma 20 with
$N' = \lfloor \theta u-20(\theta u)^{15/16} \rfloor$, which tends to infinity, and then
Lemmas 21 and 16. Dividing by r, and writing $2M = N-K/2$,

$$z-\lambda \ge \min\left(\frac{2\theta v}{3},\ N-\frac{2M}{1-2\theta}\right)-o(1).$$

The first term equals $K/30$. The second equals

$$\frac{K\left(\frac12-\frac{N}{10v}\right)}{1-\frac{K}{10v}} \ge \frac{7K}{30},$$

since $N/v \le 8/3$ and the denominator lies in $(0,1]$. So $z \ge \lambda+K/30$, and

$$x \ge \frac54\left(\lambda+\frac{K}{30}\right)+\frac{\sigma}{4} = \frac{15\lambda+7-3\gamma}{24}.$$

In both cases $\sigma$ has dropped out. The coefficient of $\lambda$ is positive, so:

- If $1 \le \gamma \le 2$: $x \ge f(\gamma) := (15c(\gamma)+7-3\gamma)/24$. The square root
  in (5.2) is the geometric mean of $20-4\gamma \pm \sqrt{108}(\gamma-1)$, two affine
  functions positive on $[1,2]$, so it is concave and c is convex. Hence f is convex,
  and its minimum is where $c'(\gamma) = 1/5$, namely at
  $\gamma_* = (21+74\sqrt2)/69 = 1.82104\ldots$, with $c(\gamma_*) = (24-14\sqrt2)/69$
  and $f(\gamma_*) = x_*$.
- If $\gamma \lt 1$: $\lambda \ge 1-\gamma$ gives $x \ge (22-18\gamma)/24 \ge 1/6 \gt x_*$.

Either way $x \ge x_*$, against $x \le x_*-\varepsilon$. $\square$

At the minimum $K = 0$, that is $\sigma = (10-2\sqrt2)/69$ and $M = N/2$: the bound on
the good cards gives nothing there, and about half of the clean cards have traces with
small matching number, two in each group. Section 6.6 shows that such cards still carry
many witnesses, and uses them.

### 6.6 The weak traces

Keep the setting and the limits of the proof of Theorem 4, and put

$$\delta = z-\lambda, \qquad K_- = \max(0,-K).$$

So $\delta \ge 0$ and $x \ge \frac54(\lambda+\delta)+\frac14\sigma$.

**Lemma 22 (the best $\theta$).** *If $K \gt 0$ then*

$$\delta \ge R(K) := \frac{v+3N-\sqrt{(v+3N)^2-6vK}}{6} = \frac{vK}{v+3N+\sqrt{(v+3N)^2-6vK}} \ge \frac{vK}{2(v+3N)} \ge \frac{K}{18}.$$

*Proof.* At any fixed $\theta \lt 1/2$ the proof of §6.5 gives
$\delta \ge \min\left(2\theta v/3,\ (K/2-2N\theta)/(1-2\theta)\right)-o(1)$, since
$2M = N-K/2$. The two terms are equal when $P(\theta) = 4v\theta^2-(2v+6N)\theta+3K/2$
vanishes. Here $P(0) = 3K/2 \gt 0$ and $P(1/2) = 3(K/2-N) \le 0$, because $M \ge 0$ gives
$K \le 2N$. So the smaller root
$\theta_* = \left(v+3N-\sqrt{(v+3N)^2-6vK}\right)/(4v)$ lies in $(0, 1/2]$, and there both
terms equal $R(K)$; if $\theta_* = 1/2$, let $\theta$ increase to it. The last inequality
uses $v/N \ge 3/8$. $\square$

With $\lambda = c(\gamma)$ and $\sigma$ as in §6.5 this already gives
$x \ge (15\lambda+7-3\gamma)/24+K/36$ for $K \gt 0$, so a value of x near $x_*$ forces
$K$ near 0.

Next, a bound on S that does not assume equality in §5. Write $\hat t = t/r$ and

$$\bar s = \min\left(\hat t,\ \frac{(2-\gamma)\hat t+(v-2+\gamma)(\hat t+\lambda)/2}{v}\right) \quad (v \gt 2-\gamma), \qquad \bar s = \hat t \quad (v \le 2-\gamma).$$

Then $S \le (\bar s+o(1))ur$: a large $F_i$ has $S_i \le u$, the others have
$S_i \le L$ (Lemma 14(c)), $2m \le h$, every $S_i \le u+4$ (Lemma 1), and
$L/r \to 2-\gamma$. Put

$$Q = \frac N2-3\lambda-\bar s .$$

**Lemma 23 (weak traces).**

$$\delta \ge \min\left(\frac v{16},\ \frac{v(Q-K_-)_+}{2+9v+9N}\right).$$

*Proof.* We may assume $\delta \lt v/16$. Fix $\alpha \gt 2\delta/v$ with $\alpha \lt 1/8$
(when $\delta = 0$, any small $\alpha$, and let $\alpha \to 0$ at the end). Call a clean card
*weak* if $\nu_A \lt \alpha u$ and *strong* if $\nu_A \ge u/4$.

*Groups with three cards that are not weak.* Let $J_3 r$ be their number. Meeting three
such cards in each of $\min(J_3 r, \alpha u/3)$ of these groups by Lemma 20, Lemma 16 gives
$\delta \ge 2\min(J_3, \alpha v/3)-o(1)$. As $2\alpha v/3 \gt \delta$, $J_3 \le \delta/2+o(1)$.

*Groups of the wrong shape.* Call a group *good* if it has two strong cards and two weak
ones. A group with at most two cards that are not weak has $\sum \nu_A/u \le 1+2\alpha$ if
it is good and at most $\frac34+2\alpha$ if not; a group with three such cards has at most
2. Lemma 19 gives $\frac1r\sum_A \nu_A/u \ge \frac N4+\frac K8-o(1)$. There are $Nr/4$ groups,
so the number $Zr$ of groups that are not good satisfies

$$Z \le 2N\alpha+\frac52\delta+\frac12 K_{-}+o(1).$$

*The witnesses of the weak cards.* By Lemma 17 the weak cards of the good groups, $(N/2-2Z)r$
of them, miss at most $S+3u\ell$ vertices in all. Each has $e(L_A) \ge s_A-\nu_A \ge s_A-\alpha u$.
So their traces have at least $(Q-2Z-\alpha N/2-o(1))ur$ edges in all.

*One weak card per good group.* Give each good group one colour, carried by the union of
the traces of its two weak cards. A colour has at most $2r$ edges, and at most $2(u-1)$
coloured edges meet a vertex, since a witness lies in at most two clean cards. Take a
maximal set of disjoint edges of distinct colours, $L_w$ of them. Every edge of an unused
colour meets one of their $2L_w$ vertices, so the number of coloured edges, at least half
the total above, is at most $2rL_w+4uL_w$.

*The strong cards.* Keep $L' = \min(L_w, \lfloor u/32 \rfloor)$ of these edges. Remove
their $2L'$ vertices from the traces of the $2L'$ strong cards of the same groups; each
keeps a matching of at least $u/4-2L' \ge 2L'+20(2L')^{15/16}$ edges for large r. Lemma 20
meets all of them with disjoint pairs, which together with the $L'$ edges extend to one
pairing of U. Its natural cover meets three cards in each of $L'$ groups, and Lemma 16
gives $\delta \ge 2L'/r-o(1)$.

Putting the steps together, with $\alpha \downarrow 2\delta/v$,

$$\delta \ge \min\left(\frac v{16},\ \frac{v}{2+4v}\left(Q-K_--\delta\left(5+\frac{9N}{v}\right)\right)_+\right),$$

and moving the $\delta$ term to the left gives the lemma. $\square$

**Theorem 5.** $\displaystyle \liminf_{r \to \infty} \frac{g(r)}{r} \ge 3.1024745 .$

*Proof.* Suppose not, and take the limits of §6.5 with $x \lt 0.1024745$. Then
$1 \le \gamma \le 2$ (for $\gamma \lt 1$, §6.5 gives $x \ge 1/6$), $c(\gamma) \le \lambda \le 0.082$ and
$0 \le \sigma \le 0.41$, and

$$x \ge \frac54(\lambda+\max(\delta_1,\delta_2))+\frac\sigma4,$$

where $\delta_1$ is the bound of Lemma 22 (0 when $K \le 0$) and $\delta_2$ that of Lemma 23.
The script `code/verify_weak_trace_bound.py` shows, by branch and bound over this box with
exact rational interval arithmetic, that the right side is at least 0.1024745 everywhere,
with $\delta_1$ taken as the simpler bound $vK/(2(v+3N))$. This is a contradiction. $\square$

The numerical minimum of the right side is $0.10247456\ldots$ with this $\delta_1$, and
$0.10247458\ldots$ with $R(K)$, at $\gamma \approx 1.85698$, $\lambda = c(\gamma) \approx 0.068491$,
$\sigma \approx 0.066398$, where $\delta_1 = \delta_2 \approx 0.00020866$. There $K \gt 0$ and
$Q \gt 0$: neither saving is zero, and the two are in balance. The constant has no closed
form that we know of. The certificate gives seven decimals; it does not compute the minimum
exactly.

The proofs of Theorems 4 and 5 use [5] and give no explicit threshold in r, like [2].

## 7. Verification

| claim | script |
|---|---|
| Theorem 1 on every configuration with at most six cards, and at low degree up to nine; the sharpness family | `code/verify_residual_bound.py` |
| Lemmas 1, 3 and 5, the $d = 0$ structure of §2.3, and the $u = 13$, $d = 5$ step | `code/verify_local_graphs.py` |
| Lemmas 10 and 11 on 8, 9 and 10 vertices | `code/verify_rainbow_lemmas.py`, `code/verify_rainbow.c` |
| Lemma 13, the anchor values, and the failure at $d = 5$ reported in §4.5 | `code/verify_anchor_count.py` |
| every arithmetic step of §2.3, §3.4, §4, §5 and §6, and the constant of [2] | `code/verify_p5_arithmetic.py` |
| the algebra of Lemma 19 and Theorem 4: the budget identity, $K = 2(N-2M)$, the second term of Lemma 21, the reduction of both cases, the root argument for $u \le L$, convexity of c, $c'(\gamma_*) = 1/5$, $c(\gamma_*)$, $\sigma_*$ and the constant; the optimal $\theta$ and $R(K) \ge K/18$ of Lemma 22; the counts of Lemma 23 | `code/verify_rainbow_constant.py` |
| Theorem 5: the lower bound 0.1024745 over the whole domain, by branch and bound with exact rational interval arithmetic | `code/verify_weak_trace_bound.py` |

The runs are recorded in `results/p5_checks.txt`. These are finite checks of the finite
lemmas. The steps that are not finite, namely (2.1), (2.2), Lemma 4, the inequality
$M \le S$, the swap lemma, the augmentation arguments of Lemmas 6, 9, 12 and 14, and
Lemmas 15 to 23, have been read, Lemmas 15 to 21 in a separate review session, but
not independently reviewed. Theorems 4 and 5 also rest on the published theorem of [5].

---

*This work was prepared with AI assistance (ChatGPT, OpenAI; Claude, Anthropic), used for algebraic derivation, for drafting and rewriting code and text, for running and re-running the computations, and for auditing the papers against their own scripts. The same tools were used in the review, so the review carries the same caveat. All statements were checked by the author, who is responsible for them. No priority is claimed and the result has not been independently reviewed by a human or a proof assistant; the repository README sets out the division of labour and the open obligations in full.*

## References

1. P. Erdős, L. Lovász, *Problems and results on 3-chromatic hypergraphs and some related
   questions*, in: Infinite and Finite Sets (Keszthely, 1973), Colloq. Math. Soc. János
   Bolyai 10, North-Holland, 1975, 609–627.
2. V. Sivashankar, *An Improved Lower Bound for the Erdős–Lovász Cover Number Problem*,
   arXiv:2606.24878v2.
3. J. Kahn, *On a problem of Erdős and Lovász. II: n(r) = O(r)*, J. Amer. Math. Soc. 7
   (1994), 125–143.
4. J. Barát, *Intersecting and 2-intersecting hypergraphs with maximal covering number:
   the Erdős–Lovász theme revisited*, arXiv:2011.04444.
5. D. Munhá Correia, A. Pokrovskiy, B. Sudakov, *Short proofs of rainbow matching
   results*, Int. Math. Res. Not. IMRN 2023, no. 14, 12441–12476.
