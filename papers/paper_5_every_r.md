# [P5] Every r: the residual cover route from 3r − 3

Mohamed A. Osman — ORCID 0009-0004-5912-999X

Licence: CC BY 4.0. Research draft.

---

## Abstract

Sivashankar [2] proved $g(r) \ge 3r-4$ for every $r$ by deleting the cards of high-degree
symbols and bounding the cover number of what remains, a family of maximum degree three,
by $4\tau \le q+r+4$. He asked whether $+4$ can be replaced by $+3$. Theorem 1 gives a
proposed proof that it can, so $g(r) \ge 3r-3$ for every $r$. The residual constant $+3$
cannot be lowered [2], and $g(3) = 6$ and $g(4) = 9$ show that $3r-3$ is attained. Theorem 2 excludes
the equality case and gives $g(r) \ge 3r-2$ for every $r \ge 19$.

Section 4 turns the exclusion of equality into a quantitative statement: when the
remainder is large, the loss is linear in $r$, with a closed form at every remainder size.
Section 5 records an exact bookkeeping identity and a covering inequality, and sets out
where the route toward a coefficient above $3$ stands. No theorem is claimed in Section 5.

The proofs are proposed and have not been independently reviewed. Every finite step is
checked exhaustively by a script named in §6. No priority is claimed.

## 1. Setting

$g(r)$ is the least number of cards in a pairwise intersecting $r$-uniform family $H$ with
$\tau(H) = r$. The known values are $g(3) = 6$, $g(4) = 9$, $g(5) = 13$ [4], and $g(6) = 17$
([P1]–[P4] of this set). Against $3r$ these are $3r-3$, $3r-3$, $3r-2$ and $3r-1$. So a
bound $g(r) \ge 3r-c$ valid for every $r$ cannot have $c \lt 3$; a bound $3r-2$ can hold
only from $r = 5$ on, and $3r-1$ only from $r = 6$ on.

For large $r$, [2, §4] proves $g(r) \ge ((41-\sqrt{19})/12 - o(1))r$, about $3.053r$, for
$r$ beyond a threshold that is not made explicit. The bounds of this paper have
coefficient $3$ and are therefore weaker for large enough $r$. What they add is that they
hold, with explicit constants, at every $r$.

**What is borrowed.** The peeling reduction, the dual triple system, the maximum matching,
the selected witnesses, the first local support bound, and the sharpness family are from
[2, §2–3]. They are recalled with proofs so that the argument can be read on its own.

**Peeling.** Delete the cards containing a symbol of current degree at least four, and
repeat until no such symbol is left. If $k$ symbols are chosen and the remainder $J$ has
$q$ cards, then

$$\lvert H \rvert \ge q+4k, \qquad r \le k+\tau(J),$$

because the $k$ chosen symbols together with any cover of $J$ cover $H$. Hence a bound
$4\tau(J) \le q+r+C$ gives $\lvert H \rvert \ge 3r-C$.

**The dual view.** For a symbol $v$ of $J$ let $B_v$ be the set of cards containing it.
Regard the cards as points. The blocks $B_v$ have size at most three, cover every pair of
points, and every point lies in exactly $r$ blocks. A cover of $J$ is a set of blocks
meeting every point. For any card $E$,

$$q-1 \le \sum_{v \in E} (\deg v - 1) \le 2r, \qquad\text{(1.1)}$$

so $q \le 2r+1$.

Take a maximum matching $M_1, \dots, M_t$ among the distinct three-element blocks. Let $C$
be its union and $U$ the other $u$ points, so $q = 3t+u$; no three-element block lies
inside $U$. A defining symbol of each $M_i$ covers $C$, and pairing the points of $U$ gives

$$\tau(J) \le t + \lceil u/2 \rceil . \qquad\text{(1.2)}$$

For each pair $x, y$ of $U$ choose one symbol $w_{xy}$ in both, the *witness* of the pair.
Witnesses are distinct, since a repeated one would lie in four cards or in a triple inside
$U$. Each witness block is $\lbrace x,y \rbrace$ or $\lbrace x,y,z \rbrace$ with $z \in C$.

For each $i$ let $F_i$ be the graph on $U$ whose edge $xy$ is present, with colour $z$,
when the witness block is $\lbrace x,y,z \rbrace$ and $z \in M_i$. The $F_i$ are simple and
edge-disjoint. Two disjoint edges of one $F_i$ never have different colours: their blocks
would replace $M_i$ by two disjoint triples. For each colour write $e$ for its number of
edges and $s$ for its support, and let $S_i$ be the sum of the three supports,
$S = \sum_i S_i$.

## 2. Theorem 1: the sharp residual bound

**Theorem 1 (proposed).** *Every intersecting $r$-uniform family $J$ with $q$ cards and
maximum degree at most three satisfies $4\tau(J) \le q+r+3$.*

**Corollary 1.** *$g(r) \ge 3r-3$ for every $r \ge 1$.*

*Proof.* Peeling and Theorem 1. $\square$

### 2.1 Three inequalities

*Capacity at $U$.* The witnesses use exactly $u(u-1)$ incidences on $U$. The other
$ur-u(u-1)$ incidences each reach at most two cards of $C$, and all $3tu$ pairs between
$U$ and $C$ must be met. Hence

$$3tu - S \le 2\bigl(ur-u(u-1)\bigr). \qquad\text{(2.1)}$$

*Capacity of a colour.* Fix $z \in M_i$, and let the edges of colour $z$ in $F_i$ be $e$ in
number, with support $s$. In the card $z$, the $e$ witnesses cover $s$ points of $U$, a defining symbol
of $M_i$ covers its other two points, and the remaining $q-3-s$ points need the other
$r-e-1$ symbols, at most two each. So

$$2e - s \le 2r - q + 1 =: d. \qquad\text{(2.2)}$$

*Local support* ([2] for the first bound).

**Lemma 1.** *Let $F$ be a simple graph on $u$ vertices with at most three colours, in
which disjoint edges always have the same colour. Then $S_F \le \max(12, u+4)$. If every
colour has $2e-s \le d$, then $S_F \le \max(12, u+2, d+8)$.*

*Proof.* Suppose a colour has two disjoint edges, on four vertices $W$. Every
other-colour edge lies in $W$. If no other colour is present, $S_F \le u$. If the
other-colour edges have no common vertex, every edge of the first colour meets all of them
and lies in $W$ too, giving $12$. Otherwise at most two other-colour edges exist, sharing a
vertex, with support contribution at most four, giving $u+4$. Fix one of them, $g$. Every
first-colour edge meets $g$, so $e \ge s-2$, and $2e-s \le d$ gives $s \le d+4$ and
$S_F \le d+8$.

If every colour is internally intersecting, each is a star or part of a triangle. With
all supports at most four, the sum is at most $12$. Otherwise one colour is a star with at
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

By (1.2) and Lemma 2, if $u$ is even then $4\tau \le 4t+2u = q+(t+u) \le q+r+2$. If $u$ is
odd, $4\tau \le q+(t+u)+2$. So Theorem 1 follows once *$u$ odd implies $r \ge u+t-1$*.

Suppose $u$ is odd and, by Lemma 2, $r = u+t-2$. Then $d = u-t-3 \ge 0$, and (2.1) becomes

$$S \ge u(t+2). \qquad\text{(2.3)}$$

If $u \ge 11$, (2.3) and Lemma 1 give $t \ge u/2$. Then $d+8 \le u+2$ and $12 \le u+2$, so
every $S_i \le u+2$ and $u(t+2) \le t(u+2)$, that is $u \le t$, against $t \le u-3$.

For odd $u \le 9$, the conditions $0 \le t \le u-3$ and $u(t+2) \le t \max(12,u+4)$ leave
exactly

$$(u,t) \in \lbrace (5,2), (7,3), (7,4), (9,5), (9,6) \rbrace ,$$

with $d = 0, 1, 0, 1, 0$ respectively.

**Lemma 3 (small excess).** *If every colour has $2e-s \le 1$ and $F$ has more than one
colour, then $S_F \le 12$, $S_F \ne 11$, and $S_F = 12$ only when $F$ is a properly
three-coloured $K_4$. If also $u \le 9$, the same holds when $F$ has one colour.*

*Proof.* A connected component on $v \ge 2$ vertices has $2e-v \ge v-2$, so each colour is
a matching, or one path on three vertices plus a matching. A colour with a matching of size
three leaves the other colours empty, so $F$ has one colour and $S_F \le u \le 9$. A colour of support five is
$P_3$ plus an edge, and the other colours are then confined to two edges, giving at most
$9$. Otherwise every support is at most four. Support four forces two disjoint edges, and
two cross-intersecting two-edge matchings are two perfect matchings of one $K_4$; a third
colour must be the third. $\square$

*The cases $d = 1$.* For $(9,5)$, (2.3) asks $S \ge 63$ and Lemma 3 allows $60$. For
$(7,3)$, (2.3) asks $35$, so all three $S_i$ are $12$: three edge-disjoint copies of $K_4$
on seven vertices. Two such copies meet in one vertex and leave $K_{3,3}$ plus an isolated
vertex, which holds no third $K_4$.

*The cases $d = 0$.* Now every colour is a matching and $q = 2r+1$, so (1.1) is an
equality for every card: every symbol has degree three and any two cards meet once. So
every witness block is a triple and the $F_i$ partition the edges of $K_u$. For
$(5,2)$, $qr = 55$ is not divisible by three. For $u \le 9$ a local graph has at most six
edges: one colour is a matching of at most four edges, and with several colours each is a
matching of at most two, since a third disjoint edge would meet no other-colour edge. Six
edges occur only as the three perfect matchings of a $K_4$, and five only as $K_4$ minus an
edge.
For $(9,6)$ the $36$ edges of $K_9$ would split into six copies of $K_4$, needing degree
$8$ divisible by three. For $(7,4)$ the $21$ edges of $K_7$ split into four parts of size at
most six only as $6+6+6+3$, $6+6+5+4$ or $6+5+5+5$; two edge-disjoint $K_4$ leave
$K_{3,3}$ plus a vertex, which excludes the first two. In the third, after one $K_4$ on
four vertices, each copy of $K_4$ minus an edge contains a triangle and so takes one of the
three edges among the other three vertices; it is then two of the four joined to two of
the three, plus that edge. The three pairs among the three are distinct and meet, so
edge-disjointness needs three disjoint pairs among four vertices, which is impossible.

This proves Theorem 1. $\square$

### 2.4 Sharpness, and degree four

For odd $n$ take points $1, \dots, n$ and one symbol for each pair ([2]). Then $q = n$,
$r = n-1$, a cover is an edge cover of $K_n$, and $\tau = (n+1)/2$, so $4\tau = q+r+3$.

**Corollary 2.** *If $J$ has maximum degree at most four, then $4\tau(J) \le q+r+3$.*

*Proof.* Take a maximal matching of $a$ four-element blocks; their defining symbols cover
$4a$ cards and the rest has maximum degree three. $\tau \le a + (q-4a+r+3)/4$. $\square$

Peeling at degree five then gives $\lvert H \rvert \ge (15r-q-15)/4$ for the size $q$ of
the remainder, which improves the additive term in the corresponding step of [2] but not
its coefficient.

## 3. Theorem 2: excluding equality

**Theorem 2 (proposed).** *$g(r) \ge 3r-2$ for every $r \ge 19$.*

Suppose $\lvert H \rvert = 3r-3$ and $\tau(H) = r$ with $r \ge 5$. We derive $r \le 18$.

### 3.1 The equality parameters

If $H$ had a symbol of degree at least five, peeling it first would give
$\lvert H \rvert \ge \lvert J \rvert + 4(r-\tau(J)) + 1 \ge 3r-2$ by Theorem 1. If every
degree were at most three, $3r-3 \le 2r+1$ would force $r \le 4$. So the maximum degree is
four. (At $r = 3$ and $r = 4$ the bound $3r-3$ is attained, and this is where the argument
stops.)

Take a maximum matching of $a$ four-element blocks, delete its $4a$ cards, and let $J$ be
the rest, of maximum degree three and $q = 3r-3-4a$ cards. The $a$ defining symbols and a
cover of $J$ cover $H$, so $\tau(J) \ge r-a$, while Theorem 1 gives
$4\tau(J) \le q+r+3 = 4(r-a)$. So Theorem 1 is an equality for $J$, which by §2.3 forces $u$ odd, $\tau(J) = r-a$,
$r = u+t-1$ and $q = 3t+u$. Consequently

$$u = 2a+3, \quad t = r-2a-2, \quad d = u-t-1 \ge 0, \quad r = 2u-2-d, \qquad\text{(3.1)}$$

and (2.1) becomes $S \ge ut$. Write $H_0 = (u-1)/2$.

### 3.2 Pointwise capacity

**Lemma 4.** *For $x \in U$ let $S_x$ be the number of cards of $C$ met by the witnesses at
$x$. Then $S_x \ge t$. In one $F_i$, if $x$ carries $E$ edges in $k$ colours, then
$E-k \le d$.*

*Proof.* The card $x$ has exactly $u-1$ witnesses, so exactly $r-(u-1) = t$ other symbols.
They meet at most $2t$ cards of $C$, and all $3t$ must be met, so $3t-S_x \le 2t$. The
$u-1$ witnesses at $x$ reach $S_x$ distinct cards of $C$, so the number of witnesses
"wasted" at $x$ is $u-1-S_x \le u-1-t = d$. Edges of one colour at $x$ reach one card, so
$E$ edges in $k$ colours waste $E-k$. $\square$

**Lemma 5.** *In the equality setting every $F_i$ with more than one colour has
$S_i \le \max(12, d+8)$ and $S_i - e(F_i) \le 6$. A one-coloured $F_i$ has
$S_i - e(F_i) \le H_0$.*

*Proof.* The first case of Lemma 1 already gives $\max(12,d+8)$. In the star case, $F_i$
is a star at one vertex with $E$ edges in $k \le 3$ colours, and
$S_i = E+k \le d+2k \le d+6$ by Lemma 4. For the second bound: with two disjoint edges of one colour on $W$, either
every support lies in $W$ and each colour has $s-e \le 2$, or at most two other-colour
edges exist, contributing at most two, while the first colour has $e \ge s-2$. Otherwise
every colour is a star or triangle with $s-e \le 1$. A one-coloured graph has $s-e$ at most
its number of components, at most $H_0$. $\square$

### 3.3 Two augmentation bounds

Call a one-coloured $F_i$ *large* if its matching number is at least four, and let $m$ be
their number.

**Lemma 6.** *$2m \le t$.*

*Proof.* A large $F_i$ uses one colour $z_i$; its other two points of $M_i$ are met by no
witness. So every $x \in U$ must meet those $2m$ points with its $t$ non-witness symbols. No
such symbol meets two of them. Within one $M_i$, its triple and an edge of $F_i$ avoiding
$x$ would replace $M_i$ by two triples. Across $M_i$ and $M_j$, an edge of $F_i$ avoiding
$x$ and an edge of $F_j$ avoiding $x$ and those two endpoints, which matching number four
provides, give three triples in place of two. Either way the matching was not maximum.
$\square$

**Lemma 7.** *$u \le \max(12, d+8)$.*

*Proof.* Suppose not. By Lemma 5 every $F_i$ with more than one colour has $S_i \lt u$,
and a one-coloured $F_i$ has $S_i \le u$. Since $S \ge ut$, every $F_i$ is one-coloured
and spans $U$. Then $2e-u \le d$ gives $e \le (u+d)/2$, and its matching number is at least
$u-e \ge (u-d)/2 \gt 4$. So $m = t$, and Lemma 6 forces $t = 0$, whereas
$t = u-d-1 \ge 8$. $\square$

### 3.4 The deleted cards

For each of the $4a$ deleted cards $A$ let $L_A$ be the graph on $U$ whose edge $xy$ is
present when $w_{xy} \in A$; write $e_A$, $s_A$, $\nu_A$ for its edges, support and matching
number. Let $T = \sum_i e(F_i)$ and $D = S - T$.

A witness of degree two in $J$ lies in at most two deleted cards, one of degree three in
at most one, since degrees in $H$ are at most four; so $\sum_A e_A \le u(u-1) - T$. Let
$M = \sum_A (u - s_A)$. For $x \in U$ its $t$ non-witness symbols have room for at most
$3t$ other cards of $H$; they must meet the $3t-S_x$ cards of $C$ not met by witnesses, and
every deleted card $A$ whose graph misses $x$. So at most $S_x$ deleted cards miss $x$, and
$M \le S$. Using $\nu_A \ge s_A - e_A$ and $4a = 2u-6$,

$$\sum_A \nu_A \ge u^2 - 5u - D. \qquad\text{(3.2)}$$

**Lemma 8.** *Within one group of four deleted cards there are no three disjoint edges
from three different graphs $L_A$.*

*Proof.* Extend them to a matching of $H_0$ edges of the complete graph on $U$, leaving
one point $x$. The witnesses of these edges cover $U$ except $x$ and meet three cards of the
group; one symbol of $x$ that lies in the fourth card covers both. With the $t$ defining
symbols of $C$ and the $a-1$ symbols of the other groups this is a cover of $H$ of size
$H_0 + 1 + t + a - 1 = r-1$. $\square$

**Lemma 9.** *Three graphs each with a matching of size four and a fourth nonempty graph
contain three disjoint edges from three different graphs.*

**Lemma 10.** *The same holds for four graphs with matching numbers at least
$3, 3, 4, 4$.*

*Proof of both.* Fix size-four matchings $P, Q$ in two of the graphs and suppose no such
triple exists. Call an edge $e$ of another graph *blocked* if no two disjoint edges, one
from $P$ and one from $Q$, avoid it; every edge of the other graphs is blocked. The edges
of $P$ and of $Q$ avoiding a blocked edge must cross-intersect. Each side keeps at least
two, and one edge cannot meet three disjoint edges, so exactly two survive on each side
and they form a four-cycle, which is a component of $P \cup Q$, with both ends of $e$ in
both supports. The other graphs supply three disjoint blocked edges (a size-three matching
for Lemma 10, a size-four matching for Lemma 9). Their six endpoints lie in both supports,
and outside one such four-cycle there are at most four such vertices, so some of them
touches it and yields a second four-cycle. So $P \cup Q$ is two disjoint four-cycles on
the same eight vertices, and every blocked edge is a diagonal of one of them.

For Lemma 10 the two size-three matchings each consist of three of the four diagonals.
The first has both diagonals of one cycle and the second at least one of them; take that
one for the second, the other for the first, and an edge of $P$ in the other cycle. For
Lemma 9 the three size-four matchings are the three perfect matchings of each of the two
copies of $K_4$. Take an edge $f$ of the fourth graph. If $f$ removes two vertices of one
copy, the edge on its other two vertices and an edge of a different matching in the other
copy avoid $f$. If $f$ removes at most one vertex of each copy, each copy keeps a triangle
or all of $K_4$, which contains all three matchings, so two edges of different matchings
avoid $f$. In every case a rainbow triple exists. $\square$

Order the matching numbers of one group as $v_1 \le v_2 \le v_3 \le v_4$. Greedy choice
gives a rainbow triple when $v_2 \ge 1$, $v_3 \ge 3$ and $v_4 \ge 5$. With Lemmas 8–10,
every group has $v_2 = 0$, or $v_3 \le 2$, or all $v_i \le 4$ with neither $v_1 \ge 1$ and
$v_2 = v_3 = v_4 = 4$ (Lemma 9) nor $v_1, v_2 \ge 3$ and $v_3 = v_4 = 4$ (Lemma 10). So
the sum is at most $\max(2H_0, H_0+6, 13)$, and with (3.2):

$$D \ge \frac{u^2-6u-3}{2} \quad (u \ge 15), \qquad D \ge 39 \quad (u = 13). \qquad\text{(3.3)}$$

### 3.5 Finishing

*$u \ge 15$.* By Lemma 7, $d \ge u-8$ and $t = u-d-1 \le 7$. By Lemma 5,
$D \le 7H_0 = 7(u-1)/2$. With (3.3) this gives $u^2-13u+4 \le 0$, false for $u \ge 13$.

*$u = 13$.* Lemma 7 gives $d \ge 5$. If $d \ge 6$ then $t \le 6$ and $D \le 6t \le 36$,
against (3.3). If $d = 5$ then $t = 7$ and every $S_i \le 13$, so $S \ge 91$ forces every
$S_i = 13$. A one-coloured $F_i$ then has $e \le 9$ and matching number at least four, so it
is large and $S_i - e \le 6$. A multicoloured $F_i$ cannot be the star case of Lemma 5,
which gives at most $d+6 = 11$, so $S_i = 13 = d+8$ is the extremal case of Lemma 1: two other-colour edges $pa$, $pb$, and a first colour made of
$ab$ and six edges at $p$, so $S_i - e = 13 - 9 = 4$. Lemma 6 gives $m \le 3$, so
$D \le 6 \cdot 3 + 4 \cdot 4 = 34$, against (3.3).

So $u \le 11$ and $r = 2u-2-d \le 20$.

*$r = 20$.* Then $u = 11$, $d = 0$, $t = 10$, $q = 41 = 2r+1$. As in §2.3 every symbol of
$J$ has degree three, but $qr = 820$ is not divisible by three.

*$r = 19$.* Then $u = 11$, $d = 1$, $t = 9$. By Lemma 3 a multicoloured $F_i$ has
$S_i \le 10$ unless it is a $K_4$ with $S_i = 12$. A one-coloured one has $S_i \le 11$, and
$S_i \le 7$ unless it is large, since matching number at most three and $2e-s \le 1$ allow
support at most seven. Lemma 6 gives $m \le 4$. Without a $K_4$,
$S \le 11 \cdot 4 + 10 \cdot 5 = 94 \lt 99 = ut$. So some $F_i$ is a $K_4$, on four points
$W$.

For a local graph $F_j$ call $(x, c)$ *eligible* if no edge of colour $c$ meets $x$ and
every edge of the other two colours does. Put $\delta_j = 12 - S_j \ge 0$; then
$\sum_j \delta_j = 108 - S \le 9$. A multicoloured $F_j$ has at most three eligible pairs,
and any eligible pair forces $S_j \le 6$, so its count is at most $\delta_j$. A one-coloured
$F_j$ of support $s$ has $11-s = \delta_j - 1$ eligible pairs, or $13-s = \delta_j + 1$ if it
is a path on three vertices; such a path has $\delta_j = 9$, so at most one occurs. The total
number of eligible pairs is therefore at most $9+1 = 10$.

Now take $x \notin W$; there are seven. No witness at $x$ meets the triple $M_i$ of the
$K_4$. The card $x$ has nine non-witness symbols and $S_x \le 10$, so they must meet at least
$17$ cards of $C$ that the witnesses miss. No symbol joins $x$ to two points of $M_i$, by
augmentation with an edge of the $K_4$. So three distinct symbols meet the three points of
$M_i$, and since the other six meet at most $12$ new cards, these three reach at least two
further new cards $q' \in M_j$. For such a block $\lbrace x, p, q' \rbrace$, an edge $f$ of
$F_j$ of another colour avoiding $x$ would give three disjoint triples in place of
$M_i, M_j$: the block itself, $f$ with its colour, and an edge of the four-cycle of the
$K_4$ in the two colours other than $p$ that avoids $f$. So $(x, q')$ is eligible. That is
at least $7 \cdot 2 = 14$ eligible pairs, against $10$.

This proves Theorem 2. $\square$

## 4. A quantitative form: loss linear in r

Drop the equality assumption. For the remainder $J$ of degree-four peeling put

$$\ell = r-u-t+1, \qquad h = t+\ell, \qquad d = 2r-q+1 .$$

Every $x \in U$ has $h$ non-witness symbols, and (1.2) gives
$B := q+r+3-4\tau(J) \ge \ell$. The argument of Lemma 4 gives $S_x \ge t-2\ell$, so
$S \ge u(t-2\ell)$, and $u-1-S_x \le d$ still holds, so Lemma 5 holds. With
$L = \max(12, d+8)$, every multicoloured $F_i$, and every one-coloured $F_i$ that is not large, has
$S_i \le L$. The argument of Lemma 6 gives $2m \le h$.

**Theorem 3 (proposed).** *If $u \gt L$ then*

$$\ell \ge \frac{(u-L)(u-d-1)}{3u+L}. \qquad\text{(4.1)}$$

*Proof.* $u(t-2\ell) \le S \le Lt + (u-L)m \le Lt + (u-L)(t+\ell)/2$, which rearranges to
$(u-L)t \le (5u-L)\ell$; substitute $t = u-d-1+2\ell$. $\square$

**Corollary 3.** *If the degree-four peeling of $H$ leaves a remainder with
$q \ge 2r-3$, then $\lvert H \rvert \ge \lceil (28r-67)/9 \rceil$.*

*Proof.* Here $d \le 4$ and $L = 12$. For $u \gt 12$, (4.1) gives $\ell \ge (u-21)/3$, and
with $r = 2u-d-2+3\ell$ this is $\ell \ge (r-40)/9$. For $u \le 12$, $r \le 22+3\ell$ gives
the same for $r \ge 13$, and for smaller $r$ the bound is negative. So
$B \ge (r-40)/9$, and $\lvert H \rvert = 3r-3+E+B+4C$ (§5.1) gives the claim. $\square$

The coefficient here is $28/9 \approx 3.111$, but only under the hypothesis on $q$, which
nothing here forces.

**The gain at every remainder size.** (4.1) holds for every $d$, not only $d \le 4$. Writing
$q = (2-\delta)r$ and minimising $\ell$ over $u$, the guaranteed gain is, to leading
order in $r$,

$$\frac{\ell}{r} \ge \frac{(12+4\delta) - \sqrt{(12+4\delta)^2 - 108(1-\delta)^2}}{54} ,$$

which is $1/9$ at $q = 2r$, about $0.048$ at $q = 1.75r$, about $0.019$ at $q = 1.5r$,
about $0.004$ at $q = 1.25r$, and $0$ at $q = r$. It is positive for every remainder
larger than $r$ by a fixed fraction. For remainders smaller than $r$ by a fixed fraction the
gain is immediate: $\tau(J) \le \lceil q/2 \rceil$ gives $B \ge r-q+1$. What is not covered
is a remainder of size close to $r$, which is where the pair family of §2.4 lives.

## 5. The route toward a coefficient above 3

No theorem is claimed in this section.

### 5.1 Bookkeeping

For the degree-four peeling of $H$, with $n = \lvert H \rvert$, put

$$E = n-q-4k, \qquad B = q+r+3-4\tau(J), \qquad C = k+\tau(J)-r .$$

$E$ and $C$ are non-negative, and $B$ is by Theorem 1. Then exactly

$$n = 3r-3+E+B+4C. \qquad\text{(5.1)}$$

A coefficient above $3$ needs $E+B+4C \ge \varepsilon r - O(1)$ for every $H$. §4 gives it
through $B$ except near $q = r$. Near $q = r$ a lemma about $J$ alone cannot give it,
because the pair family has $B = 0$. For the same reason no bound $5\tau \le q+r+K$ holds
for maximum degree four: the pair family of §2.4 on $N$ points forces $K \ge (N+7)/2$.

### 5.2 A covering inequality

Every deleted card $A$ meets every card of $J$, so the symbols of $A$ that occur in $J$ form
a cover of $J$ of size at most $r-1$. If a cover of $J$ of size $\tau(J)+s$, together with
a set $X$ of further symbols, meets every card of $g$ deleted groups, then it replaces those
groups' symbols in a cover of $H$, and

$$C \ge g - s - \lvert X \rvert . \qquad\text{(5.2)}$$

The question near $q = r$ is therefore about $J$ and the covers of $J$ that the deleted
cards contain.

### 5.3 A measurement in the cleanest case

Take $J$ to be exactly the pair family on $u$ points, so that each deleted card contains an
edge cover of $K_u$. A near-perfect matching of $K_u$ is a minimum cover of $J$. If it meets
all four edge covers of a group, that group costs nothing in (5.2).

`code/measure_matching_hits.py` searches for the four edge covers that make this least
likely for a random perfect matching. The worst probability found is $0$ at $u = 8$ (the
configuration of two copies of $K_4$ that appears in Lemmas 9 and 10),
$7/945 \approx 0.0074$ at $u = 10$ (the exhaustive value), about $0.012$ at $u = 12$, about $0.017$ at
$u = 16$ and about $0.020$ at $u = 24$. These rise toward $(1-e^{-1/2})^4 \approx 0.024$,
the value for independent events. If a positive lower bound of this kind holds for all $u$,
then (5.2) gives $C$ linear in $r$ in this case. This is a measurement on a model; it is
not a proof, and the model leaves out the triples and the non-witness symbols that a real
remainder near $q = r$ has.

### 5.4 Where it stands

Put together, the three cases give a positive $\varepsilon$ in principle. As the pieces
stand, the weakest point is a window of remainders just above $r$: there §4 gives only
about $\eta^2 r/16$ for $q = (1+\eta)r$, while the covering argument has to pay for
non-witness symbols whose number grows like $\eta r$. The constant that results is far
below $0.053$ and is not stated as a result. One observation may help: in that window the
non-witness symbols at $x$ are mostly blocks $\lbrace x, c, c' \rbrace$ with $c, c' \in C$,
and when $c$ and $c'$ lie in the same $M_i$ such a block can replace $M_i$ in the maximum
matching at no cost. When they lie in different triples, the same augmentation arguments
as in Lemmas 6–10 constrain them.

## 6. Verification

| claim | script |
|---|---|
| Theorem 1 on every configuration with at most six cards, and at low degree up to nine; the sharpness family | `code/verify_residual_bound.py` |
| Lemmas 1, 3, 5 and the $d = 0$ structure of §2.3; the $u = 13$, $d = 5$ step; the eligible-pair bounds | `code/verify_local_graphs.py` |
| Lemmas 9 and 10 on 8, 9 and 10 vertices | `code/verify_rainbow_lemmas.py`, `code/verify_rainbow.c` |
| every arithmetic step of §2.3, §3.5, §4 and §5, and the constant of [2] | `code/verify_p5_arithmetic.py` |
| the measurement of §5.3 | `code/measure_matching_hits.py` |

The runs are recorded in `results/p5_checks.txt`. These are finite checks of the finite
lemmas. The steps that are not finite, namely (2.1), (2.2), Lemma 4, the inequality
$M \le S$, and the augmentation arguments of Lemmas 6 and 8 and of §3.5, have been read but
not independently reviewed.

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
