# [P5] Lower bounds for g(r) at every r: 3r − 3, and 3r − 2 from r = 16

**Mohamed A. Osman** — ORCID 0009-0004-5912-999X

Research draft, 2 October 2026. Licence: CC BY 4.0.

## Abstract

Let $g(r)$ be the least number of hyperedges in an intersecting $r$-uniform hypergraph with transversal number $r$. Sivashankar [2] proved $g(r)\ge3r-4$ and asked whether his residual bound $4\tau\le q+r+4$ can be improved to $+3$. We give a proposed proof that it can (Theorem 1), so $g(r)\ge3r-3$ for every $r$; this is attained at $r=3$ and $r=4$. We then exclude equality for every $r\ge16$ (Theorem 2), so $g(r)\ge3r-2$ there. Every finite step is checked exhaustively by a named script. The asymptotic bound $g(r)\ge(3.1108-o(1))r$ is in the companion paper [P6].

## 1. Setting

### 1.1 The problem

A hypergraph $H$ is **intersecting** if any two hyperedges meet, and $\tau(H)$ is the least number of vertices meeting every hyperedge. Then
$$g(r)=\min\lbrace \lvert E(H)\rvert : H \text{ intersecting, } r\text{-uniform, } \tau(H)=r\rbrace .$$
The problem goes back to Erdős and Lovász [1], and Kahn [3] proved $g(r)=O(r)$. The known values are $g(3)=6$, $g(4)=9$, $g(5)=13$ [4] and $g(6)=17$ ([P1]–[P4] of this set). Against $3r$ these are $3r-3$, $3r-3$, $3r-2$ and $3r-1$.

**The reduction of [2].** Repeatedly take a vertex of degree at least four and delete the hyperedges through it. If this takes $k$ steps and leaves a family $J$ of $q$ hyperedges and maximum degree at most three, then
$$\lvert E(H)\rvert\ge q+4k,\qquad r\le k+\tau(J).$$
So a bound $4\tau(J)\le q+r+C_0$ gives $\lvert E(H)\rvert\ge3r-C_0$. Theorem 1 is this bound with $C_0=3$.

### 1.2 The remainder J

We use the dual picture: each hyperedge of $J$ is a **point**, and each vertex is a **block**, the set of points containing it. Since $J$ is intersecting, $r$-uniform and of maximum degree three:

- every block has at most three points, and every pair of points lies in some block;
- every point lies in exactly $r$ blocks (two vertices with the same block count twice).

A point $A$ meets the other $q-1$ points through its $r$ blocks, each of which reaches at most two of them. So
$$q-1\le\sum_{v\in A}(\deg_J v-1)\le2r.\tag{1.1}$$

**Triples, $W$ and $U$.** Fix a maximum family of pairwise disjoint 3-point blocks $M_1,\dots,M_t$. Let $W$ be their union ($3t$ points) and $U$ the other $u$ points, so $q=3t+u$. No 3-point block lies inside $U$, by maximality.

**The natural cover.** One vertex for each $M_i$, one common vertex for each pair of a pairing of $U$, and one more vertex if $u$ is odd, cover $J$. So
$$\tau(J)\le t+\lceil u/2\rceil.\tag{1.2}$$

**Witnesses.** For each pair $x,y\in U$ fix one common vertex $w_{xy}$, the *witness* of the pair. Its block is $\lbrace x,y\rbrace$ or $\lbrace x,y,z\rbrace$ with $z\in W$. Different pairs have different witnesses, since a repeated witness would give a block of four points or a 3-point block inside $U$.

**Local graphs.** For each $i$, the *local graph* $F_i$ is the graph on $U$ with an edge $xy$ of *colour* $z\in M_i$ whenever the witness block is $\lbrace x,y,z\rbrace$. Two disjoint edges of $F_i$ always have the same colour, since otherwise their blocks would replace $M_i$ by two disjoint triples.

**Notation used throughout.**

- For one colour: $e$ = its number of edges, $s$ = its support (vertices it touches).
- $S_i$ = sum of the three colour supports of $F_i$, and $S=\sum_iS_i$.
- $S_x$ = number of points of $W$ reached by the witnesses at $x\in U$; then $S=\sum_xS_x$.
- $d=2r-q+1$, the slack in (1.1).

## 2. Theorem 1: the sharp residual bound

**Theorem 1 (proposed).** *Every intersecting $r$-uniform family $J$ with $q$ hyperedges and maximum degree at most three satisfies $4\tau(J)\le q+r+3$.*

**Corollary 1.** *$g(r)\ge3r-3$ for every $r\ge1$.*

*Proof.* The reduction of §1.1 with Theorem 1. $\square$

### 2.1 Capacity and local support

**Capacity at $U$.** The witnesses use exactly $u(u-1)$ of the $ur$ incidences of points of $U$. Each of the other $ur-u(u-1)$ incidences reaches at most two points of $W$, and all $3tu$ pairs between $U$ and $W$ must be met. Hence
$$3tu-S\le2\bigl(ur-u(u-1)\bigr).\tag{2.1}$$

**Capacity of a colour.** Fix a colour $z\in M_i$ with $e$ edges and support $s$. In the point $z$, the $e$ witnesses cover $s$ points of $U$, the vertex of $M_i$ covers its two other points, and the remaining $q-3-s$ points need the other $r-e-1$ vertices, at most two each. So
$$2e-s\le2r-q+1=d.\tag{2.2}$$

**Lemma 1 ([2] for the first bound).** *Let $F$ be a simple graph on $u$ vertices with at most three colours, in which disjoint edges have the same colour. Then $S_F\le\max(12,u+4)$. If every colour has $2e-s\le d$, then $S_F\le\max(12,u+2,d+8)$.*

*Proof.* Suppose first that some colour has two disjoint edges, with endpoint set $Y$ of four vertices. Every edge of another colour meets both, so it lies in $Y$.

- If no other colour is present, $S_F\le u$.
- If the other-colour edges have no common vertex, every first-colour edge meets all of them, so it lies in $Y$ too, and $S_F\le12$.
- Otherwise there are at most two other-colour edges, sharing a vertex, contributing at most four: $S_F\le u+4$. Fix one of them, $g$. Every first-colour edge meets $g$, so $e\ge s-2$, and $2e-s\le d$ gives $s\le d+4$, hence $S_F\le d+8$.

Suppose next that no colour has two disjoint edges. Then each colour is a star or part of a triangle. If all supports are at most four, $S_F\le12$. Otherwise one colour is a star with at least four leaves; every other-colour edge contains its centre, and simplicity gives $S_F\le u+2$. $\square$

### 2.2 A preliminary bound

**Lemma 2 ([2]).** *$r\ge u+t-2$.*

*Proof.* Put $\alpha=r-u-t+2$. If $u=0$, (1.1) gives $\alpha\ge(r+5)/3\gt0$. Otherwise (1.1), (2.1) and Lemma 1, with $K=\max(12,u+4)$, give
$$t\le u-3+2\alpha,\qquad \alpha\ge1-\frac{(K-u)t}{2u}.$$
A negative integer $\alpha$ would give $t\le u-5$ and then $\alpha\gt-1$. For $K=u+4$ the bound is $-1+10/u$; for $K=12$ with $u\le8$ it needs $u^2-13u+60\gt0$, whose discriminant is negative. $\square$

### 2.3 The odd equality case

By (1.2) and Lemma 2:

- if $u$ is even, $4\tau\le4t+2u=q+(t+u)\le q+r+2$;
- if $u$ is odd, $4\tau\le q+(t+u)+2$.

So Theorem 1 follows once we show: *if $u$ is odd then $r\ge u+t-1$.* Suppose $u$ is odd and $r=u+t-2$. Then $d=u-t-3\ge0$, and (2.1) becomes
$$S\ge u(t+2).\tag{2.3}$$

*Large $u$.* If $u\ge11$, (2.3) and Lemma 1 give $t\ge u/2$. Then $d+8\le u+2$ and $12\le u+2$, so every $S_i\le u+2$ and $u(t+2)\le t(u+2)$, that is $u\le t$, against $t\le u-3$.

*Small $u$.* For odd $u\le9$, the conditions $0\le t\le u-3$ and $u(t+2)\le t\max(12,u+4)$ leave exactly
$$(u,t)\in\lbrace(5,2),(7,3),(7,4),(9,5),(9,6)\rbrace,$$
with $d=0,1,0,1,0$ respectively.

**Lemma 3 (small excess).** *If every colour has $2e-s\le1$ and $F$ has more than one colour, then $S_F\le12$, $S_F\ne11$, and $S_F=12$ only when $F$ is a properly three-coloured $K_4$. If also $u\le9$, the same holds when $F$ has one colour.*

*Proof.* A connected component on $v\ge2$ vertices has $2e-v\ge v-2$, so each colour is a matching, or one path on three vertices plus a matching.

- A colour with a matching of size three leaves the other colours empty, so $F$ has one colour and $S_F\le u\le9$.
- A colour of support five is $P_3$ plus an edge; the other colours are then confined to two edges, and $S_F\le9$.
- Otherwise every support is at most four. Support four forces two disjoint edges, and two cross-intersecting two-edge matchings are two perfect matchings of one $K_4$; a third colour must be the third. $\square$

*The cases $d=1$.*

- $(9,5)$: (2.3) asks $S\ge63$, and Lemma 3 allows $60$.
- $(7,3)$: (2.3) asks $35$, so all three $S_i$ are $12$, that is, three edge-disjoint copies of $K_4$ on seven vertices. Two such copies meet in one vertex and leave $K_{3,3}$ plus an isolated vertex, which holds no third $K_4$.

*The cases $d=0$.* Now every colour is a matching and $q=2r+1$, so (1.1) is an equality for every point: every vertex has degree three and any two points meet once. So every witness block is a triple, and the $F_i$ partition the edges of $K_u$.

- $(5,2)$: $qr=55$ is not divisible by three.
- For $u\le9$ a local graph has at most six edges: one colour is a matching of at most four edges, and with several colours each is a matching of at most two, since a third disjoint edge would meet no other-colour edge. Six edges occur only as the three perfect matchings of a $K_4$, and five only as $K_4$ minus an edge.
- $(9,6)$: the 36 edges of $K_9$ would split into six copies of $K_4$, which needs the degree 8 to be divisible by three.
- $(7,4)$: the 21 edges of $K_7$ split into four parts of size at most six only as $6+6+6+3$, $6+6+5+4$ or $6+5+5+5$. Two edge-disjoint $K_4$ leave $K_{3,3}$ plus a vertex, which excludes the first two. In the third, fix the $K_4$ on four vertices. Each copy of $K_4$ minus an edge contains a triangle, so it takes one of the three edges among the other three vertices; it is then two of the four joined to two of the three, plus that edge. The three pairs taken among the three are distinct and meet, so edge-disjointness needs three disjoint pairs among four vertices, which is impossible.

This proves Theorem 1. $\square$

### 2.4 Sharpness, and degree four

For odd $n$ take points $1,\dots,n$ and one vertex for each pair ([2]). Then $q=n$, $r=n-1$, a cover is an edge cover of $K_n$, and $\tau=(n+1)/2$, so $4\tau=q+r+3$.

**Corollary 2.** *If $J$ has maximum degree at most four, then $4\tau(J)\le q+r+3$.*

*Proof.* Take a maximal family of disjoint 4-point blocks, $a$ of them. Their vertices cover $4a$ points and the rest has maximum degree three, so $\tau\le a+(q-4a+r+3)/4$. $\square$

Peeling at degree five then gives $\lvert E(H)\rvert\ge(15r-q-15)/4$ for a remainder of size $q$. This improves the additive term in the corresponding step of [2], not its coefficient.

## 3. The equality case

In Sections 3 and 4 suppose $\lvert E(H)\rvert=3r-3$ and $\tau(H)=r$ with $r\ge5$. We write *deleted hyperedges* for the hyperedges removed in the reduction.

### 3.1 The parameters

The maximum degree of $H$ is four:

- a vertex of degree at least five, peeled first, would give $\lvert E(H)\rvert\ge\lvert E(J)\rvert+4(r-\tau(J))+1\ge3r-2$ by Theorem 1;
- if every degree were at most three, $3r-3\le2r+1$ would force $r\le4$. (At $r=3$ and $r=4$ the bound $3r-3$ is attained.)

Take a maximum family of disjoint 4-point blocks, $a$ of them. Their $4a$ hyperedges form *groups* of four, each with its *group vertex*. Delete them and let $J$ be the rest: maximum degree three and $q=3r-3-4a$. The $a$ group vertices and a cover of $J$ cover $H$, so $\tau(J)\ge r-a$, while Theorem 1 gives $4\tau(J)\le q+r+3=4(r-a)$. So Theorem 1 is an equality for $J$, and §2.3 forces $u$ odd, $\tau(J)=r-a$, $r=u+t-1$ and $q=3t+u$. Consequently
$$u=2a+3,\qquad t=r-2a-2,\qquad d=u-t-1\ge0,\qquad r=2u-2-d,\tag{3.1}$$
and (2.1) becomes $S\ge ut$. Write $H_0=(u-1)/2$.

When $d=0$ every vertex of a point of $J$ has degree three in $J$; as $d$ grows, vertices of degree two and one are allowed.

### 3.2 Local bounds

**Lemma 4 (pointwise capacity).** *For every $x\in U$, $S_x\ge t$. In one $F_i$, if $x$ carries $E$ edges in $k$ colours, then $E-k\le d$.*

*Proof.* The point $x$ has exactly $u-1$ witnesses, so exactly $r-(u-1)=t$ other vertices. They meet at most $2t$ points of $W$, and all $3t$ must be met, so $3t-S_x\le2t$. The $u-1$ witnesses at $x$ reach $S_x$ distinct points of $W$, so the number of witnesses *wasted* at $x$ is $u-1-S_x\le u-1-t=d$. Edges of one colour at $x$ reach one point, so $E$ edges in $k$ colours waste $E-k$. $\square$

**Lemma 5.** *Every $F_i$ with more than one colour has $S_i\le\max(12,d+8)$ and $S_i-e(F_i)\le6$. A one-coloured $F_i$ has $S_i-e(F_i)\le H_0$.*

*Proof.* The first case of Lemma 1 gives $\max(12,d+8)$. In the star case, $F_i$ is a star at one vertex with $E$ edges in $k\le3$ colours, and Lemma 4 gives $S_i=E+k\le d+2k\le d+6$.

For $S_i-e(F_i)$: if a colour has two disjoint edges on $Y$, either every support lies in $Y$ and each colour has $s-e\le2$, or there are at most two other-colour edges, contributing at most two, while the first colour has $e\ge s-2$. Otherwise every colour is a star or a triangle, with $s-e\le1$. A one-coloured graph has $s-e$ at most its number of components, at most $H_0$. $\square$

### 3.3 Two augmentation bounds

Call a one-coloured $F_i$ *large* if its matching number is at least four, and let $m$ be the number of large ones.

**Lemma 6.** *$2m\le t$.*

*Proof.* A large $F_i$ uses one colour $z_i$, so the other two points of $M_i$ are met by no witness. Every $x\in U$ must therefore meet these $2m$ points through its $t$ non-witness vertices, and no such vertex meets two of them:

- within one $M_i$, its block and an edge of $F_i$ avoiding $x$ would replace $M_i$ by two triples;
- across $M_i$ and $M_j$, its block, an edge of $F_i$ avoiding $x$, and an edge of $F_j$ avoiding $x$ and that edge (matching number four provides both) would give three triples in place of two.

Either way the family of triples was not maximum. $\square$

**Lemma 7.** *$u\le\max(12,d+8)$.*

*Proof.* Suppose not. By Lemma 5 every multicoloured $F_i$ has $S_i\lt u$, and a one-coloured one has $S_i\le u$. Since $S\ge ut$, every $F_i$ is one-coloured and spans $U$. Then $2e-u\le d$ gives $e\le(u+d)/2$, so its matching number is at least $u-e\ge(u-d)/2\gt4$. So $m=t$, and Lemma 6 forces $t=0$, whereas $t=u-d-1\ge8$. $\square$

### 3.4 The swap lemma

The groups come from a *maximum* family of 4-point blocks. That alone constrains every deleted hyperedge.

**Lemma 8 (swap).** *Let $A\ne A'$ be deleted hyperedges of the same group. If $w\in A$ and $w'\in A'$ are vertices of degree three in $J$, their sets of points of $J$ meet.*

*Proof.* The vertex $w$ lies in $A$ and in three points of $J$, so its block is $\lbrace A\rbrace\cup T$ with $T$ three points of $J$; likewise $\lbrace A'\rbrace\cup T'$. Neither block meets another group. If $T\cap T'=\emptyset$, the two blocks are disjoint, and putting them in place of the group's own block gives $a+1$ disjoint 4-point blocks, against maximality. $\square$

Call such a $T$ a *triple of $A$*. A deleted hyperedge meets $J$ through its triples and through vertices of degree two or one in $J$.

**Proposition 1.** *In the equality setting $d\ne0$, and $d\ne1$ when $r\ge11$.*

*Proof.* Fix a group of four deleted hyperedges.

*$d=0$.* By §2.3, $q=2r+1$ and every vertex of a point of $J$ has degree three in $J$. So a deleted hyperedge $A$ meets the $2r+1$ points of $J$ through at most $r-1$ triples. Fix one, $T$. If the other at most $r-2$ triples all met $T$, they would reach at most $3+2(r-2)=2r-1$ points; so $A$ has a triple $T'$ disjoint from $T$. By Lemma 8 every triple of a group-mate $A'$ meets both $T$ and $T'$, so it reaches at most one of the $2r-5$ points outside them. With at most $r-1$ triples, $A'$ misses one, since $r-1\lt2r-5$ for $r\ge5$.

*$d=1$.* Now $q=2r$, and (1.1) allows each point of $J$ at most one vertex of degree two and none of degree one. So $J$ has at most $q/2=r$ vertices of degree two, each in at most two deleted hyperedges: at most $2r$ incidences with deleted hyperedges.

- A deleted hyperedge whose triples pairwise meet reaches at most $1+2n_3$ points through its $n_3$ triples and two through each other vertex, at most $1+2(r-1)\lt2r$ in all. So every deleted hyperedge has two disjoint triples.
- For a group-mate $A'$ with $n_2$ vertices of degree two, the $2r-6$ points outside those two triples are reached at most once per triple and twice per vertex of degree two, so $2r-6\le(r-1)+n_2$ and $n_2\ge r-5$.

Every deleted hyperedge is such a group-mate, so the $4a\ge4$ deleted hyperedges need at least $4(r-5)$ incidences, more than $2r$ when $r\ge11$. $\square$

## 4. Theorem 2: excluding equality from r = 16

**Theorem 2 (proposed).** *$g(r)\ge3r-2$ for every $r\ge16$.*

### 4.1 Traces of the deleted hyperedges

For a deleted hyperedge $A$, its *trace* $L_A$ is the graph on $U$ with an edge $xy$ whenever $w_{xy}\in A$. Write $e_A$, $s_A$, $\nu_A$ for its number of edges, its support and its matching number. Put
$$T=\sum_ie(F_i),\qquad D=S-T,\qquad M=\sum_A(u-s_A).$$

- A witness of degree two in $J$ lies in at most two deleted hyperedges, and one of degree three in at most one, since degrees in $H$ are at most four. So $\sum_Ae_A\le u(u-1)-T$.
- For $x\in U$, its $t$ non-witness vertices have room for at most $3t$ further hyperedges. They must meet the $3t-S_x$ points of $W$ missed by the witnesses, and every deleted $A$ whose trace misses $x$. So at most $S_x$ deleted hyperedges miss $x$, and $M\le S$.

With $\nu_A\ge s_A-e_A$ and $4a=2u-6$ this gives
$$\sum_A\nu_A\ge u^2-5u-D.\tag{4.1}$$

**Lemma 9.** *Within one group there are no three disjoint edges from three different traces.*

*Proof.* Extend them to a matching of $H_0$ edges of the complete graph on $U$, leaving one point $x$. The witnesses of these edges cover $U$ except $x$ and meet three hyperedges of the group; one vertex of $x$ that lies in the fourth covers both. With the $t$ vertices of the triples and the $a-1$ other group vertices this is a cover of $H$ of size $H_0+1+t+a-1=r-1$. $\square$

**Lemma 10.** *Three traces each with a matching of size four, and a fourth nonempty trace, contain three disjoint edges from three different traces.*

**Lemma 11.** *The same holds for four traces with matching numbers at least $3,3,4,4$.*

*Proof of both.* Fix size-four matchings $P,Q$ in two of the traces and suppose no such triple exists. Call an edge $e$ of another trace *blocked* if no two disjoint edges, one from $P$ and one from $Q$, avoid it; every edge of the other traces is blocked.

*Step 1: each blocked edge sits on a four-cycle.* The edges of $P$ and of $Q$ avoiding a blocked edge must cross-intersect. Each side keeps at least two, and one edge cannot meet three disjoint edges, so exactly two survive on each side. They form a four-cycle, which is a component of $P\cup Q$ (counting an edge twice if it is in both). Both endpoints of $e$ lie in both supports, since $e$ removes exactly two edges from each matching.

*Step 2: two disjoint four-cycles.* The other traces supply three disjoint blocked edges (a size-three matching for Lemma 11, size four for Lemma 10). Their six endpoints lie in both supports, and outside one such four-cycle there are at most four such vertices, so another blocked edge touches it. The four-cycle of that edge avoids it, so it is a second, disjoint four-cycle. Hence $P\cup Q$ is two disjoint four-cycles on the same eight vertices, and every blocked edge is a diagonal of one of them.

*Step 3: a rainbow triple.* For Lemma 11, the two size-three matchings each consist of three of the four diagonals. The first has both diagonals of one cycle and the second at least one of them; take that one for the second, the other for the first, and an edge of $P$ in the other cycle. For Lemma 10, the three size-four matchings are the three perfect matchings of each of the two copies of $K_4$. Take an edge $f$ of the fourth trace. If $f$ removes two vertices of one copy, the edge on its other two vertices and an edge of a different matching in the other copy avoid $f$. If $f$ removes at most one vertex of each copy, each copy keeps a triangle or all of $K_4$, so two edges of different matchings avoid $f$. $\square$

Order the matching numbers of one group as $\nu_1\le\nu_2\le\nu_3\le\nu_4$. Greedy choice gives a rainbow triple when $\nu_2\ge1$, $\nu_3\ge3$ and $\nu_4\ge5$. With Lemmas 9–11, every group has $\nu_2=0$, or $\nu_3\le2$, or all $\nu_i\le4$ with neither $\nu_1\ge1,\ \nu_2=\nu_3=\nu_4=4$ nor $\nu_1,\nu_2\ge3,\ \nu_3=\nu_4=4$. So the sum over one group is at most $\max(2H_0,H_0+6,13)$, and with (4.1)
$$D\ge\frac{u^2-6u-3}{2}\quad(u\ge15),\qquad D\ge39\quad(u=13).\tag{4.2}$$

### 4.2 Large remainders: u is at most 11

*$u\ge15$.* By Lemma 7, $d\ge u-8$ and $t=u-d-1\le7$. By Lemma 5, $D\le7H_0=7(u-1)/2$. With (4.2) this gives $u^2-13u+4\le0$, false for $u\ge13$.

*$u=13$.* Lemma 7 gives $d\ge5$.

- If $d\ge6$ then $t\le6$ and $D\le6t\le36$, against (4.2).
- If $d=5$ then $t=7$ and every $S_i\le13$, so $S\ge91$ forces every $S_i=13$. A one-coloured $F_i$ then has $e\le9$ and matching number at least four, so it is large and $S_i-e\le6$. A multicoloured $F_i$ cannot be the star case of Lemma 5 (which gives at most $d+6=11$), so $S_i=13=d+8$ is the extremal case of Lemma 1: two other-colour edges $pa$, $pb$, and a first colour made of $ab$ and six edges at $p$, so $S_i-e=13-9=4$. Lemma 6 gives $m\le3$, so $D\le6\cdot3+4\cdot4=34$, against (4.2).

So $u\le11$.

### 4.3 u = 11: the anchor count

**Open pairs.** A pair $(x,c)$ is *open* in a local graph $F_j$ if no edge of colour $c$ meets $x$ and every edge of the other two colours does.

**Anchor value.** For a local graph $F_i$ and $x\in U$, let $P_x$ be the set of colours of $F_i$ with no edge at $x$; their points of $M_i$ are not reached by the witnesses at $x$.

- A pair of colours in $P_x$ is *forbidden* if $F_i$ has an edge of the third colour avoiding $x$.
- A colour $c\in P_x$ is *good* if, for every pair $f$ of $U$ that avoids $x$ and is not an edge of $F_i$, some edge of $F_i$ of a colour other than $c$ avoids both $x$ and $f$.

For a set $R\subseteq P_x$ whose pairs are all forbidden, let $g_x$ be $\lvert R\rvert$, minus the number of colours of $P_x$ outside $R$, minus the number of colours of $R$ that are not good; take the best $R$. The *anchor value* of $F_i$ is $G=\sum_x\max(g_x,0)$.

**Lemma 12 (demand).** *If $F_i$ has anchor value $G$, the other local graphs have at least $tu+G-S$ open pairs in all.*

*Proof.* Fix $x$ and $R$. The $t$ non-witness vertices of $x$ must reach the $3t-S_x$ points of $W$ that its witnesses miss, among them the points of $R$. No vertex reaches two points of $R$: its block and an edge of the third colour avoiding $x$ would replace $M_i$ by two triples. So $\lvert R\rvert$ distinct vertices reach the points of $R$, each reaching at most one further point, and the other $t-\lvert R\rvert$ reach at most two each. The $\lvert R\rvert$ vertices therefore reach at least $t+\lvert R\rvert-S_x$ further points missed by the witnesses, of which at most one per colour of $P_x$ outside $R$ lies in $M_i$.

Let $\lbrace x,c,q'\rbrace$ be the block of such a vertex, with $c\in R$ good and $q'\in M_j$, $j\ne i$. No edge of colour $q'$ in $F_j$ meets $x$, since the witnesses at $x$ miss $q'$. If an edge $f$ of $F_j$ of another colour avoided $x$, goodness would give an edge $e$ of $F_i$ of a colour other than $c$ avoiding $x$ and $f$, and the blocks of $\lbrace x,c,q'\rbrace$, $e$ and $f$ would be three disjoint triples in place of $M_i$ and $M_j$. So $(x,q')$ is open in $F_j$. Distinct $q'$ give distinct pairs, and each colour of $R$ that is not good spoils at most one. So at least $t+g_x-S_x$ open pairs come from $x$. Summing over the $x$ with $g_x\gt0$, and using $S_x\ge t$ for the rest, gives $tu+G-S$. $\square$

**Three anchors.**

- A properly three-coloured $K_4$ on a set $Y$ has $G=3(u-4)$: for $x\notin Y$ all three colours are missing, every pair is forbidden, and every colour is good, since the other two colours form a four-cycle on $Y$ and a pair $f$ outside $F_i$ meets $Y$ in at most one point.
- A spanning one-coloured large $F_i$ has $G=2u$: for every $x$ its two unused colours are missing, forbidden together, and good, since a matching of size four leaves an edge avoiding $x$ and $f$.
- The graph $Y_k$, with edges $pa$ and $pb$ of two colours and a third colour made of $ab$ and $k$ edges at $p$, has $G=2(u-3)$.

**Lemma 13 (finite classification; `code/verify_anchor_count.py`).** *Let $u=11$ and $1\le d\le4$. Every local graph with more than one colour has at most $12-S_j$ open pairs, and every one with $S_j\ge11$ has anchor value at least 16. A one-coloured graph of support $s$ has $11-s$ open pairs, plus two for each vertex common to all its edges.*

The one-coloured count is direct. The script checks every multicoloured local graph on eleven vertices that satisfies (2.2) and Lemma 4: those with $S_j\ge11$ are $K_4$ and $Y_4$, and at $d=4$ also $Y_5$, with anchor values 21, 16 and 16.

**Proposition 2.** *In the equality setting, $u=11$ with $1\le d\le4$ is impossible.*

*Proof.* Here $t=10-d$, every $S_j\le12$ by Lemma 5, and $S\ge11t$. So $\sum_j(12-S_j)\le t\le9$, and some $S_j\ge11$. That $F_j$ is an anchor with $G\ge16$: by Lemma 13 if it has several colours; otherwise it spans $U$ with at most $(11+d)/2\le7$ edges, so its matching number is at least four and $G=22$. By Lemma 12 the other local graphs carry at least $11t+16-S$ open pairs.

By Lemma 13 a local graph carries at most $12-S_j$ open pairs, except a one-coloured one whose edges share a vertex. A star with $k$ leaves has $12-S_j=11-k$ and carries one more; a single edge or an empty graph would need $12-S_j\ge10\gt t$. A star needs $11-k\le t$ and, by (2.2), $k\le d+1$, so $k=d+1$ and it uses the whole budget; at most one occurs. So the local graphs carry at most $12t-S+1$ open pairs, and $11t+16\le12t+1$ would need $t\ge15$. $\square$

### 4.4 Proof of Theorem 2

Suppose $r\ge16$, $\lvert E(H)\rvert=3r-3$ and $\tau(H)=r$. By §4.2, $u\le11$, and $r=2u-2-d$ by (3.1).

- If $u\le9$, then $r\le16-d$, so $r=16$, $u=9$, $d=0$, excluded by Proposition 1.
- If $u=11$, then $d=20-r\le4$: $d=0$ is excluded by Proposition 1, and $1\le d\le4$ by Proposition 2.

So $\lvert E(H)\rvert\ge3r-2$ by Corollary 1. $\square$

### 4.5 The remaining finite case

At $r=15$ the parameter choices are $(u,d,t)=(9,1,7)$ and $(11,5,5)$. Proposition 1 excludes the first. The second remains open: at $d=5$ multicoloured stars can have support $u=11$ with zero anchor value, and the count of Lemma 13 no longer applies. So the argument stops at $r\ge16$ and does not settle $7\le r\le15$.

## 5. Verification

- Theorem 1 on every configuration with at most six hyperedges, and at low degree up to nine, and the sharpness family: `code/verify_residual_bound.py`.
- Lemmas 1, 3 and 5, the $d=0$ structure of §2.3, and the $u=13$, $d=5$ step: `code/verify_local_graphs.py`.
- Lemmas 10 and 11 on 8, 9 and 10 vertices: `code/verify_rainbow_lemmas.py` and `code/verify_rainbow.c`.
- Lemma 13, the anchor values, and the failure at $d=5$ in §4.5: `code/verify_anchor_count.py`.
- The arithmetic of §2.3, §3.4 and §4: `code/verify_p5_arithmetic.py`.

The runs are recorded in `results/p5_checks.txt`. The steps that are not finite have been read but not independently reviewed.

## Acknowledgements and research status

AI assistance (ChatGPT, OpenAI; Claude, Anthropic) was used for algebra, drafting, programming and internal review. The author is responsible for the mathematical claims. No priority is claimed.

## References

1. P. Erdős and L. Lovász, *Problems and results on 3-chromatic hypergraphs and some related questions*, in **Infinite and Finite Sets** (Keszthely, 1973), Colloq. Math. Soc. János Bolyai 10, North-Holland, 1975, 609–627.
2. V. Sivashankar, *An Improved Lower Bound for the Erdős–Lovász Cover Number Problem*, arXiv:2606.24878v2, 2026. https://arxiv.org/abs/2606.24878
3. J. Kahn, *On a problem of Erdős and Lovász. II: n(r)=O(r)*, Journal of the American Mathematical Society **7** (1994), 125–143.
4. J. Barát, *Intersecting and 2-intersecting hypergraphs with maximal covering number: the Erdős–Lovász theme revisited*, arXiv:2011.04444.
