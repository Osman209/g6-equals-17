# [P5] Lower bounds for the Erdős–Lovász cover number

**Mohamed A. Osman** — ORCID 0009-0004-5912-999X

Research draft, 2 October 2026. Licence: CC BY 4.0.

## Abstract

Let $g(r)$ be the minimum number of edges in an intersecting $r$-uniform hypergraph with transversal number $r$. We bound $g(r)$ by studying the incidences between a residual hypergraph of maximum degree three and groups of removed edges. A maximum matching of dual four-blocks restricts these incidences. Capacity estimates and rainbow matchings then give the proposed bound
$$\liminf_{r\to\infty}g(r)/r\ge3.1108.$$
An exact rational computation verifies the final minimization. The combinatorial inputs remain subject to independent review. Separate finite-parameter results are collected in the supplement.

## 1. The problem and the proof

A hypergraph is **intersecting** if every two edges meet. A **transversal** is a set of vertices meeting every edge; its minimum size is $\tau(H)$. We study
$$g(r)=\min\lbrace \lvert E(H)\rvert:H\text{ is intersecting and }r\text{-uniform},\ \tau(H)=r\rbrace .$$
An edge of an intersecting hypergraph is itself a transversal. A lower-bound proof therefore shows that a sufficiently small family has a transversal of size less than $r$.

Erdős and Lovász [1] proved $g(r)\ge8r/3-3$. Sivashankar [2] proved $g(r)\ge3r-4$ and
$$g(r)\ge\left(\frac{41-\sqrt{19}}{12}-o(1)\right)r.$$
Our proposed conclusion is $g(r)\ge(3.1108-o(1))r$. We obtain no explicit finite threshold. This is the fifth paper of a set whose first four determine $g(6)=17$.

The proof has two sources of gain. Residual stability increases the cost of covering the residual family. A residual transversal can also meet removed edges, reducing the number of additional vertices needed. Maximum four-block matchings constrain the incidences between these two parts.

The supplement, `papers/paper_5_finite_supplement.md`, treats $g(r)\ge3r-3$ for every $r$ and the proposed equality exclusion for $r\ge16$. Neither result is needed for the asymptotic argument.

## 2. Residual triples and a transversal

In the dual incidence system, hyperedges are points and vertices are blocks. Let $J$ have $q$ edges and maximum degree three. Its blocks have size at most three; every pair of points lies in a block; each point lies in exactly $r$ blocks. Distinct vertices defining the same block remain distinct incidences.

An edge $A$ meets the other $q-1$ edges through its $r$ vertices, so
$$q-1\le\sum_{v\in A}(\deg_J(v)-1)\le2r.\tag{1.1}$$
Choose a maximum matching of triple blocks $M_1,\ldots,M_t$. Let $W$ be their union and $U$ the remaining $u$ points. Then $q=3t+u$, and no triple lies entirely in $U$.

Choose one vertex for each $M_i$ and one common vertex for each pair in a pairing of $U$. An odd leftover point needs one more vertex. This gives
$$\tau(J)\le R:=t+\lceil u/2\rceil.\tag{1.2}$$

Fix a common vertex $w_{xy}$ for each pair $x,y\in U$. Its block is $\lbrace x,y\rbrace$ or $\lbrace x,y,z\rbrace$ with $z\in W$. These **witnesses** are distinct: otherwise a block would have size at least four or be a triple inside $U$.

For each $M_i$, form a graph $F_i$ on $U$: edge $xy$ has colour $z\in M_i$ if its witness block is $\lbrace x,y,z\rbrace$. Disjoint edges must have the same colour; otherwise two witness triples replace $M_i$. Write $S_i$ for the sum of the three colour supports, and $S=\sum_iS_i=\sum_xS_x$, where $S_x$ counts the distinct points of $W$ reached by witnesses at $x$.

### 2.1 Capacity and local support

We first compare the incidences needed to meet $W$ with those available in $U$.

*Capacity at U.* The witnesses use exactly $u(u-1)$ incidences on U. The other $ur-u(u-1)$ incidences each reach at most two hyperedges of W, and all $3tu$ pairs between U and W must be met. Hence

$$3tu - S \le 2\bigl(ur-u(u-1)\bigr). \qquad\text{(2.1)}$$

*Capacity of a colour.* Fix $z \in M_i$, and let the edges of colour z in $F_i$ be e in number, with support s. In the hyperedge z, the e witnesses cover s points of U, a defining vertex of $M_i$ covers its other two points, and the remaining $q-3-s$ points need the other $r-e-1$ vertices, at most two each. So

$$2e - s \le 2r - q + 1 =: d. \qquad\text{(2.2)}$$

*Local support* ([2] for the first bound).

**Lemma 1.** *Let F be a simple graph on u vertices with at most three colours, in which disjoint edges always have the same colour. Then $S_F \le \max(12, u+4)$. If every colour has $2e-s \le d$, then $S_F \le \max(12, u+2, d+8)$.*

*Proof.* Suppose a colour has two disjoint edges, on four vertices W. Every other-colour edge lies in W. If no other colour is present, $S_F \le u$. If the other-colour edges have no common vertex, every edge of the first colour meets all of them and lies in W too, giving 12. Otherwise at most two other-colour edges exist, sharing a vertex, with support contribution at most four, giving $u+4$. Fix one of them, g. Every first-colour edge meets g, so $e \ge s-2$, and $2e-s \le d$ gives $s \le d+4$ and $S_F \le d+8$.

If every colour is internally intersecting, each is a star or part of a triangle. With all supports at most four, the sum is at most 12. Otherwise one colour is a star with at least four leaves, every other-colour edge contains its centre, and simplicity gives $S_F \le u+2$. $\square$

### 2.2 A preliminary bound

**Lemma 2 ([2]).** *$r \ge u+t-2$.*

*Proof.* Put $\alpha = r-u-t+2$. If $u = 0$, (1.1) gives $\alpha \ge (r+5)/3 \gt 0$. Otherwise (1.1), (2.1) and Lemma 1, with $K = \max(12,u+4)$, give $t \le u-3+2\alpha$ and $\alpha \ge 1 - (K-u)t/(2u)$. A negative integer $\alpha$ would give $t \le u-5$ and then $\alpha \gt -1$: for $K = u+4$ the bound is $-1+10/u$, and for $K = 12$ with $u \le 8$ the needed strict inequality is $u^2-13u+60 \gt 0$, whose discriminant is negative. $\square$


### 2.3 Support minus edges

The following estimate will later control the matching numbers of witness traces.

**Lemma 3.** If a local graph has more than one colour, then $S_i-e(F_i)\le6$. A monochromatic graph satisfies $S_i-e(F_i)\le\lfloor u/2\rfloor$; if its matching number is at most three, the difference is at most three.

*Proof.* Suppose one colour has two disjoint edges. The other-colour edges lie on their four endpoints. If all supports lie there, each colour contributes at most two to support minus edges. Otherwise the other colours have at most two edges in total, and the first colour has $e\ge s-2$. This gives a total at most six. If no colour has two disjoint edges, each colour is a star or part of a triangle and contributes at most one.

For one colour, $s-e$ is at most the number of nonisolated components. Each such component contains an edge, so their number is at most both $\lfloor u/2\rfloor$ and the matching number. $\square$

## 3. Residual stability

When the remainder is large, its triple structure forces a positive cover deficit. The following estimate applies to any $J$ with maximum degree three. Put

$$\ell = r-u-t+1, \qquad h = t+\ell, \qquad d = 2r-q+1 ,$$

so that $d = u-t-1+2\ell$. Every $x \in U$ has exactly h non-witness vertices, and (1.2) gives $B := q+r+3-4\tau(J) \ge \ell$. With $L = \max(12, d+8)$, call a one-coloured local graph *large* if its matching number is at least four, and let m be their number.

**Lemma 4.** *In this general setting:*

*(a) $S_x \ge t-2\ell$ for every $x \in U$, so $S \ge u(t-2\ell)$ and $u-1-S_x \le d$.*

*(b) In every $F_i$, disjoint edges have the same colour, every colour has $2e-s \le d$, and a vertex carrying E edges in k colours has $E-k \le d$.*

*(c) Every $F_i$ that is not large has $S_i \le L$.*

*(d) $2m \le h$.*

*Proof.* (a) The h non-witness vertices of x have degree at most three in J, so each meets at most two further hyperedges, and all $3t$ hyperedges of W must be met: $3t-S_x \le 2h$.

(b) Two disjoint edges of different colours give two disjoint triples in place of $M_i$. A hyperedge c of $M_i$ meets the other $q-1$ hyperedges with r vertices of degree at most three, so its total over-coverage is at most $2r-(q-1) = d$; the witnesses through c cover $2e$ incidences on s vertices. The $u-1$ witnesses at x reach $S_x$ distinct hyperedges.

(c) If $F_i$ has more than one colour, Lemma 1 with (b) gives $\max(12, u+2, d+8)$, and in its star case every edge passes through one vertex p, so (b) at p gives $S_i = E+k \le d+2k \le d+6$. If $F_i$ has one colour and matching number at most three, a minimum edge cover of its support is a star forest with at most three components, so $e \ge s-3$ and $2e-s \le d$ gives $S_i = s \le d+6$.

(d) A large $F_i$ uses one colour, so its other two points of $M_i$ are met by no witness, and every x reaches these $2m$ points through its h non-witness vertices. A vertex reaching two points of one $M_i$, together with an edge of $F_i$ avoiding x, gives two triples in place of one; a vertex reaching points of $M_i$ and $M_j$, together with an edge of $F_i$ avoiding x and an edge of $F_j$ avoiding x and that edge, gives three triples in place of two. $\square$

**Proposition 1.** *If $u \gt L$ then*

$$\ell \ge \frac{(u-L)(u-d-1)}{3u+L}. \qquad\text{(3.1)}$$

*Proof.* By Lemma 4, $u(t-2\ell) \le S \le Lt + (u-L)m \le Lt + (u-L)(t+\ell)/2$, which rearranges to $(u-L)t \le (5u-L)\ell$; substitute $t = u-d-1+2\ell$. $\square$

**The gain at every remainder size.** Write $q = \gamma r$ with $1 \le \gamma \le 2$ and
$\lambda = \ell/r$. In a limiting sequence, put $v=u/r=(3-\gamma-3\lambda)/2$ and $\widehat d=2-\gamma$. When $u>L$, (3.1) gives $\lambda\ge(v-\widehat d)^2/(3v+\widehat d)$. Substitution and rearrangement yield
$$27\lambda^2-(20-4\gamma)\lambda+(\gamma-1)^2\le0.$$
Thus $\lambda$ is at least the smaller root, so $\lambda\ge c(\gamma)-o(1)$ before taking limits, where

$$c(\gamma) = \frac{20-4\gamma-\sqrt{(20-4\gamma)^2-108(\gamma-1)^2}}{54}. \qquad\text{(3.2)}$$

If instead $u \le L$, then $\lambda \ge (\gamma-1)/3 - o(1)$, which is at least $c(\gamma)$: with $a = \gamma-1$, c is the smaller root of $27y^2-(16-4a)y+a^2$, whose value at $a/3$ is $\frac{16}{3}a(a-1) \le 0$. For $q \lt r$ the bound $t \ge 0$ gives $\lambda \ge 1-\gamma$ directly. 


## 4. A maximum matching of four-blocks

We choose the removed groups to permit exchanges. Their maximum cardinality constrains the clean incidences; counting the removed edges then gives the baseline for the final bound.

### 4.1 Selection and bookkeeping

Starting from $H$, repeatedly select a vertex of maximum current degree while that degree is at least five, and remove its incident edges. Let $b$ be the number of these steps. If their degrees are $d_1,\ldots,d_b$, put
$$E_0=\sum_{i=1}^b(d_i-4).$$
Then $E_0\ge b$, and the remaining hypergraph $H'$ has maximum degree at most four.

In the dual incidence system of $H'$, choose a maximum matching of four-element blocks. Its $k_c$ blocks are the **clean groups**; their $N_c=4k_c$ points are the **clean hyperedges**. Remove them and denote the remainder by $J$. A four-block contained in $J$ could be added to the matching, so $\Delta(J)\le3$. The selected groups are disjoint, and each defining group vertex occurs only in its own four clean hyperedges within $H'$. Residual degrees are taken to be zero for vertices with no incidence in $J$.

Set $k=b+k_c$, $q=\lvert E(J)\rvert$ and
$$B=q+r+3-4\tau(J),\qquad \xi=k+\tau(J)-r,\qquad G=B+4\xi.$$
The selected vertices, together with a transversal of $J$, cover $H$, so $\xi\ge0$. Direct counting gives
$$n:=\lvert E(H)\rvert=q+4k+E_0=3r-3+E_0+G,\tag{4.1}$$
$$N_c=3r-3-q+G-4b.\tag{4.2}$$
**Lemma 5 (incidence capacity).** If there is a clean hyperedge, then
$$N_c\le3r-q+1,\qquad \Omega:=3r-q-N_c+1=4+4b-G\ge0.$$

*Proof.* Fix a clean hyperedge $A$ with group vertex $g$. For $v\in A\setminus\lbrace g\rbrace$ write $j_v=\deg_J(v)$. Such a vertex meets at most $3-j_v$ other clean hyperedges. Since $A$ meets all residual hyperedges and all clean hyperedges outside its group,
$$q\le\sum_{v\ne g}j_v,\qquad N_c-4\le\sum_{v\ne g}(3-j_v).$$
Add the inequalities over the $r-1$ vertices other than $g$. The identity for $\Omega$ follows from (4.2). $\square$

### 4.2 Natural transversals and savings

A **natural transversal** of $J$ is obtained from the $t$ matched triples and a pairing of $U$, with one additional vertex for an odd leftover point. Its size is $R=t+\lceil u/2\rceil$. Put $s=R-\tau(J)\ge0$. Then
$$B=\ell+4s\quad(u\text{ odd}),\qquad B=\ell+2+4s\quad(u\text{ even}).$$

**Lemma 6 (group savings).** If a natural transversal hits all four hyperedges in $b_4$ clean groups and at least three in $b_3$ other clean groups, then
$$G\ge\ell+4\bigl(b_4+\lfloor b_3/2\rfloor\bigr).$$

*Proof.* The natural transversal and all $k$ selected group vertices form a transversal of $H$ of size $r+\xi+s$. Drop the vertices of fully hit groups. Pair groups with one missed hyperedge: the two missed hyperedges intersect, so one common vertex replaces their two group vertices. Since $\tau(H)=r$, the saving is at most $\xi+s$. Use $B\ge\ell+4s$. $\square$

### 4.3 Limiting parameters

To prove the main result, suppose that a sequence with $r\to\infty$ has limiting excess $x=n/r-3<0.1108$. Pass to a subsequence on which all required normalized counts converge. Use
$$\gamma=\lim q/r,\quad \lambda=\lim\ell/r,\quad z=\lim G/r,
\quad\sigma=\lim(4b-G)/r,\quad\delta=z-\lambda.$$
The symbol $\sigma$ is also the limit of $\Omega/r$. Write
$$v=\lim u/r=\frac{3-\gamma-3\lambda}{2},\quad
\widehat t=\lim t/r=\frac{\gamma-1+\lambda}{2},\quad
N=\lim N_c/r=3-\gamma-\sigma.$$

If $J$ is empty, the selected vertices cover $H$ and $n\ge4r$. Otherwise $\gamma\le2$ by (1.1), $\lambda\ge0$ by Lemma 2 and $z\ge\lambda$ by Lemma 6. Lemma 5 gives $\sigma\ge0$ when clean edges exist. If their normalized number vanishes, (4.2) gives $\sigma=3-\gamma\ge1$, and the baseline below contradicts $x<0.1108$. Thus the clean part is nonvanishing.

Consequently
$$x\ge\frac54z+\frac\sigma4
 =\frac54(\lambda+\delta)+\frac\sigma4,
\qquad \delta\ge0.\tag{4.3}$$
In particular
$$0\le\lambda<0.0887,\quad0\le\sigma<0.4432,\quad v>0,\quad N>0.$$
Section 3 gives $\lambda\ge c(\gamma)$ on $[1,2]$, and $\lambda\ge1-\gamma$ when $\gamma<1$. The remaining arguments concern limits; statements involving $o(1)$ refer to the original sequence before taking those limits.

## 5. Witness traces and rainbow savings

A matching of witness pairs can hit prescribed clean edges without increasing the residual cover size. For a clean hyperedge $A$, its **witness trace** $L_A$ is the graph on $U$ with edge $xy$ when $w_{xy}\in A$. Let $s_A$ be its support and $\nu_A$ its matching number. The minimum-edge-cover identity on its nonisolated vertices gives
$$\nu_A\ge s_A-e(L_A),\qquad\nu_A\le\lfloor u/2\rfloor.$$
We reserve $\mu_A$ for the matching number of residual triples attached to $A$.

### 5.1 The trace budget

**Lemma 7.** With $M_0=\sum_A(u-s_A)$, summed over clean hyperedges,
$$M_0\le S+3u\ell.$$

*Proof.* Fix $x\in U$. A clean hyperedge whose trace misses $x$ still intersects the original hyperedge $x$ through one of its $h=t+\ell$ non-witness vertices. A vertex of residual degree $j$ occurs in at most $4-j$ clean hyperedges. These non-witness vertices must reach the $3t-S_x$ points of $W$ missed by witnesses, so the total clean capacity is at most $3h-(3t-S_x)=S_x+3\ell$. Sum over $x$. $\square$

Put $T=\sum_i e(F_i)$ and $D=S-T$. Here $T$ is exactly the number of witnesses of residual degree three.

**Lemma 8.** We have $D\le6t+u(t+\ell)/4$.

*Proof.* The multicoloured bound $S_i-e(F_i)\le6$ uses only the disjoint-edge condition in Lemma 3. A monochromatic graph with matching number at most three has $s-e\le3$; any monochromatic graph has $s-e\le\lfloor u/2\rfloor$, by counting nonisolated components. With $m$ large graphs,
$$D\le6(t-m)+m\lfloor u/2\rfloor\le6t+u(t+\ell)/4,$$
using $2m\le t+\ell$. $\square$

**Lemma 9 (effective missing budget).**
$$\sum_A\left(1-\frac{2\nu_A}{u}\right)
\le3\ell+4+4b-G+\frac{t+\ell}{2}+\frac{12t}{u}.$$

*Proof.* A witness of residual degree two occurs in at most two clean hyperedges, and one of degree three in at most one. Therefore
$$\sum_A e(L_A)\le u(u-1)-T.$$
Combine this with $\nu_A\ge s_A-e(L_A)$ and Lemma 7 to obtain
$$\sum_A(u-2\nu_A)\le2D+6u\ell+2u(u-1)-N_cu.$$
Divide by $u$, insert Lemma 8 and (4.2), and use $r=u+t+\ell-1$. $\square$

In the limiting domain $u$ is linear in $r$, so this gives
$$\limsup\frac1r\sum_A\left(1-\frac{2\nu_A}{u}\right)
\le M:=\sigma+\frac{\gamma-1+15\lambda}{4}.$$
Define
$$K=2(N-2M)=7-3\gamma-15\lambda-6\sigma,\qquad K_-=\max(0,-K).$$

### 5.2 Rainbow matchings

We use Correia, Pokrovskiy and Sudakov [5, Theorem 1.2 in the journal version]: for sufficiently large $m$, $m$ colour classes that are matchings of size at least $m+20m^{15/16}$ admit a full rainbow matching.

**Lemma 10.** For fixed $\theta>0$, any prescribed set of at most $\theta u-o(r)$ clean hyperedges with $\nu_A\ge\theta u$ can be hit by one natural transversal.

*Proof.* Colour a maximum matching of $L_A$ by $A$ and apply the cited theorem. Parallel edges of different colours are permitted. Extend the rainbow matching to a pairing of $U$. Each selected witness lies in its prescribed hyperedge. An odd leftover point requires one additional vertex. The $O(r^{15/16})$ allowance is absorbed by $o(r)$. $\square$

**Lemma 11 (allocation).** If $b_0$ clean hyperedges have trace matching number below $\theta u$, then a natural transversal saves at least
$$\min\left(\frac{\theta u}{6},\frac{N_c}{4}-\frac{b_0}{2}\right)-o(r)$$
group vertices.

*Proof.* Let $g_4$ groups have no such hyperedge and $g_3$ have exactly one. Then $g_3\ge N_c/2-b_0-2g_4$. If $g_4$ is sufficiently large, hit four hyperedges per selected group. Otherwise hit all four in the $g_4$ groups and three in the remaining selected groups. Lemma 6 gives at least the stated minimum, with bounded rounding errors and the rainbow allowance. If fewer than the prescribed number of eligible hyperedges exist, use the smaller set. $\square$

By Lemma 9, $b_0(1-2\theta)$ is at most the effective missing budget. Consequently
$$\delta\ge\min\left(\frac{2\theta v}{3},\ N-\frac{2M}{1-2\theta}\right).$$
Balancing the two terms, or taking a limit at $\theta=1/2$, proves
$$\delta\ge R_{\mathrm{rat}}:=\frac{K_+v}{2(v+3N)}.\tag{5.1}$$

### 5.3 Recovering savings from light traces

The local support estimates give $S\le(\bar s+o(1))ur$, where
$$\bar s=\min\left(\widehat t,\ \frac{(2-\gamma)\widehat t+(v-2+\gamma)(\widehat t+\lambda)/2}{v}\right)\quad\text{if } v\gt 2-\gamma,\qquad \bar s=\widehat t\quad\text{otherwise.}$$
Indeed ordinary local graphs have support at most $\max(12,d+8)$, large monochromatic graphs have support at most $u$, and $2m\le t+\ell$. Put $Q=N/2-3\lambda-\bar s$.

**Lemma 12 (light-trace recovery).**
$$\delta\ge W_{\mathrm{tr}}:=
\min\left(\frac v{16},\frac{v(Q-K_-)_+}{1+7v+9N}\right).\tag{5.2}$$

*Proof.* Assume $\delta<v/16$. Fix $\alpha>2\delta/v$ with $\alpha<1/8$. Call a trace light if $\nu_A<\alpha u$, and heavy if $\nu_A\ge u/4$. Call a group regular if it has two heavy and two light traces. If $J_3r$ groups contain at least three traces that are not light, Lemmas 10 and 6 give $\delta\ge2\min(J_3,\alpha v/3)-o(1)$, hence $J_3\le\delta/2+o(1)$.

Every other group has total matching number at most $(1+2\alpha)u$; a nonregular one has at most $(3/4+2\alpha)u$. Groups counted by $J_3$ have at most $2u$. The effective missing budget supplies $\sum_A\nu_A/(ur)\ge N/4+K/8-o(1)$. Thus the normalized number $Z$ of nonregular groups satisfies
$$Z\le2N\alpha+\frac52\delta+\frac12K_-+o(1).$$
The two light traces of each regular group together contain at least $(Q-2Z-\alpha N/2-o(1))ur$ edge occurrences, by Lemma 7 and $e(L_A)\ge s_A-\nu_A$.

Colour these occurrences by their group, retaining parallel copies when both traces contain the same edge. Each colour has at most $2r$ occurrences and the total degree of a vertex, including multiplicity, is at most $2(u-1)$. A maximal rainbow matching of $L_w$ edges therefore satisfies
$$\text{total occurrences}\le(2r+4u)L_w.$$

Retain at most $u/32$ selected weak edges. Their endpoints remove at most $2L'$ edges from each heavy matching; the remaining size is at least $3u/16$, while only $2L'\le u/16$ heavy colours require completion. The rainbow theorem supplies two further hit hyperedges per chosen group. Lemma 6 then gives $\delta\ge2L'/r-o(1)$.

Let $\alpha$ decrease to $2\delta/v$. The truncation would give $\delta\ge v/16$, contrary to the assumption, so
$$\delta\ge\frac{v}{1+2v}\left(Q-K_--\delta\left(5+\frac{9N}{v}\right)\right)_+.$$
Rearrangement gives (5.2). At $\delta=0$, let $\alpha\downarrow0$ after taking limits. If $\delta\ge v/16$, (5.2) is immediate. $\square$

## 6. Incidence constraints from alternative four-blocks

We now use exchanges of four-blocks to compare the clean edges’ demand for residual incidences with the available supply.

### 6.1 Exact overlap and unused capacity

For a clean hyperedge $A$ with group vertex $g$, define
$$R_A=\sum_{v\in A\setminus\lbrace g\rbrace }\deg_J(v)-q,\qquad
P_A=\sum_{v\in A\setminus\lbrace g\rbrace }(3-\deg_J(v))-(N_c-4).$$
Both quantities are nonnegative by intersectingness and degree-four capacity, and
$$R_A+P_A=\Omega.\tag{6.1}$$
Thus $R_A$ measures repeated residual incidences, while $P_A$ measures unused clean incidence capacity.

Let $p_A$ count vertices of residual degree three in $A$, and let $\mu_A$ be the matching number of their triples in $J$.

**Lemma 13 (alternative triples).**
$$\mu_A\ge p_A-R_A,\qquad 3p_A\le q+R_A.$$
Triple families associated with different clean hyperedges of one group are cross-intersecting.

*Proof.* If the $p_A$ triples have support $s$, then $3p_A-s\le R_A$. A maximal disjoint subfamily of size $m$ has support at most $3m+2(p_A-m)=2p_A+m$, because every other triple meets its union. Hence $m\ge p_A-R_A$. The second inequality follows from the total residual incidence count. Disjoint triples associated with two different hyperedges of the same group define two disjoint four-blocks replacing that group, contradicting maximum cardinality. $\square$

Call a clean group **strong** if some distinguished hyperedge $D$ has $\mu_D\ge10$; call it weak otherwise. Let their counts be $k_s,k_w$, with $k_s+k_w=N_c/4$. In a strong group only $D$ can have $p_A>0$: a triple meets at most three of ten disjoint triples. Every hyperedge of a weak group satisfies $p_A\le R_A+9$.

### 6.2 Residual degree-two vertices and eligible hyperedges

Let $B_2$ count vertices with two residual and two clean incidences, and $B_3$ those with three residual and one clean incidence. Define the **eligible hyperedges** $\mathcal E$ to be all weak-group hyperedges together with the distinguished hyperedge of each strong group. Its complement among the clean hyperedges is $\mathcal N$, the unmarked strong hyperedges (SND in the working notes).

**Lemma 14 (eligible incidences).** Every vertex counted by $B_2$ has a clean incidence in $\mathcal E$. Every vertex counted by $B_3$ has its unique clean incidence there.

*Proof.* The assertion for $B_3$ follows from Lemma 13. Suppose a $B_2$ block $\lbrace A,B,x,y\rbrace$ uses two hyperedges of $\mathcal N$. Within one strong group, a triple of its distinguished hyperedge avoiding $x,y$ gives two disjoint four-blocks replacing one. Across two strong groups, choose such a triple in the first. The pair $\lbrace x,y\rbrace$ and this triple have five residual points, so one of the ten disjoint triples in the second group avoids all of them. The three resulting four-blocks replace the two groups. Both cases contradict maximum cardinality. $\square$

Write $R_{\mathrm{tot}}=\sum_A R_A$, $R_s=\sum_D R_D$, $R_n=\sum_{A\in\mathcal N}R_A$ and $R_e=R_{\mathrm{tot}}-R_n$. Let $I_e,I_n$ count residual degree-one incidences on $\mathcal E,\mathcal N$. If $N_j$ counts vertices of degree $j$ in $J$, then
$$I_e+I_n\le3N_1,\qquad B_2\le N_2\le qd/2-N_1.\tag{6.2}$$
For the last estimate, sum $2r-\sum_{v\in x}(\deg_J(v)-1)\le d$ over residual hyperedges $x$. Vertices of residual degree one and two contribute two each; degree-three vertices contribute zero.

Let $b_A$ count residual degree-two vertices of $A$ that occur in a second clean hyperedge. An unused additional incidence consumes one unit of $P_A$. Since $n_{2,A}+2p_A\ge q-r+1+R_A$, we obtain
$$b_A+2p_A\ge q-r+1-\Omega+2R_A.$$
Summing gives
$$B_2+B_3\ge L+R_{\mathrm{tot}},\qquad L=\frac{N_c}{2}(q-r+1-\Omega).\tag{6.3}$$
Moreover, summing Lemma 13 over strong and weak groups gives
$$B_3\le\frac q3k_s+R_{\mathrm{tot}}-R_n-\frac23R_s+36k_w.\tag{6.4}$$

### 6.3 Counting only admissible incidences

Assign each $B_2$ vertex one eligible clean incidence, and each $B_3$ vertex its unique clean incidence. Distinct vertices use distinct incidences. Thus
$$B_2+B_3\le(N_c-3k_s)(r-1).\tag{6.5}$$
The assignment actually uses only residual degree-two or degree-three incidences. For $A\in\mathcal E$,
$$q+R_A=n_{1,A}+2n_{2,A}+3p_A.$$
All degree-three clean incidences lie in $\mathcal E$, so their sum is $B_3$. Consequently
$$2B_2+3B_3\le q(N_c-3k_s)+R_e-I_e.\tag{6.6}$$

An unmarked strong hyperedge has $p_A=0$. Its demand for used degree-two incidences is therefore
$$b_A\ge\frac q2-\Omega+\frac32R_A-\frac12n_{1,A}.\tag{6.7}$$
Each of these incidences leads to $\mathcal E$ by Lemma 14. Comparing the total demand with the degree-two capacity of $\mathcal E$ gives
$$6(q-\Omega)k_s+3B_3\le qN_c+R_{\mathrm{tot}}-4R_n+I_n-I_e.\tag{6.8}$$
Here the eligible degree-two capacity is $[q(N_c-3k_s)+R_e-I_e-3B_3]/2$, which explains the coefficient $3B_3$.

There is also a global bound: a $B_2$ vertex has at most one endpoint in $\mathcal N$, so $\sum_{A\in\mathcal N}b_A\le B_2$. Use (6.2), (6.7) and $I_e+I_n\le3N_1$ to obtain
$$3(q-2\Omega)k_s+3R_n+I_e-N_1\le qd.\tag{6.9}$$

Finally, sum unused degree-two capacity over **all** clean hyperedges:
$$\sum_A n_{2,A}-2B_2\le\sum_A P_A=\Omega N_c-R_{\mathrm{tot}}.$$
The total residual incidence identity implies
$$4B_2+3B_3\ge N_c(q-2\Omega)+3R_{\mathrm{tot}}-(I_e+I_n).$$
Insert (6.2) and (6.4) to conclude
$$N_c(q-2\Omega)+N_1+3R_n+2R_s\le2qd+qk_s+108k_w.\tag{6.10}$$

### 6.4 The limiting constraints

Divide the preceding inequalities by $r^2$. Denote the limits of $R_{\mathrm{tot}}/r^2,R_s/r^2,R_n/r^2,I_e/r^2,N_1/r^2$ by $\rho,\rho_s,\rho_n,\iota_e,n_1$, and write $\kappa=k_s/r$ and $L_0=N(\gamma-1-\sigma)/2$. All are nonnegative. The triple bound and (6.2)–(6.3) give
$$\beta_3\le\gamma\kappa/3+\rho-\rho_n-2\rho_s/3,
\qquad \beta_3\ge L_0+\rho+n_1-\gamma(2-\gamma)/2,$$
where $\beta_3$ is the limit of $B_3/r^2$.

The certificate uses the following necessary constraints:

$$\frac N2(\gamma-1-\sigma)
\le\frac{\gamma(2-\gamma)}{2}
 +\frac N4\max\left(\frac{\gamma+\sigma}{3},4\sigma\right).\tag{A}$$
$$N[\gamma^2+6\gamma-9-(9+\gamma)\sigma]
\le9\gamma(2-\gamma).\tag{B}$$
$$N(5\gamma-6-6\sigma)\le5\gamma(2-\gamma).\tag{C}$$
$$ (21\gamma-18\sigma)[N(\gamma-1-\sigma)-\gamma(2-\gamma)]
\le2\gamma^2N.\tag{D}$$
$$9(\gamma-2\sigma)[N(\gamma-1-\sigma)-\gamma(2-\gamma)]
\le2\gamma^2(2-\gamma).\tag{E}$$
$$3N(\gamma-2\sigma)^2
\le\gamma(2-\gamma)(7\gamma-12\sigma),
\qquad\sigma\le\gamma/3.\tag{F}$$

The eliminations below use only nonnegative overlap counts. For (A), Lemma 13 implies the group bound $\sum p_A\le\max((q+\Omega)/3,4\Omega+12)$: if $p_A\ge\Omega+4$, it has four disjoint triples and its group-mates have no triples; otherwise all four counts are at most $\Omega+3$. Combine with (6.2)–(6.3).

For (B), (6.3) and (6.5) imply $\kappa\le N(3-\gamma+\sigma)/6$. Combining this with the two displayed bounds on $\beta_3$ cancels $\rho$ and proves (B).

For (C), use (6.3), (6.6) and the $\beta_3$ upper bound, then insert its lower bound. The unreduced conclusion is
$$N(5\gamma-6-6\sigma)+2\rho+10\rho_n+6\rho_s+10n_1+\iota_e
\le5\gamma(2-\gamma).$$

For (D), normalize (6.8) and use $I_e+I_n\le3N_1$. Insert the lower bound on $\kappa$ supplied by the $\beta_3$ upper bound, and then the $\beta_3$ lower bound. This gives (D) plus the nonnegative terms
$$4\gamma\rho+(44\gamma-36\sigma)\rho_n
 +24(\gamma-\sigma)\rho_s+36(\gamma-\sigma)n_1+4\gamma\iota_e,$$
provided $\sigma<\gamma$.

For (E), normalize (6.9) and insert
$$\kappa\ge\frac3\gamma\left(L_0+n_1-\frac{\gamma(2-\gamma)}{2}
 +\rho_n+\frac23\rho_s\right).$$
The total overlap $\rho$ has canceled. The unreduced inequality adds
$$ (16\gamma-36\sigma)n_1+(24\gamma-36\sigma)\rho_n
 +12(\gamma-2\sigma)\rho_s+2\gamma\iota_e$$
to the left of (E). These terms are nonnegative when $\sigma\le4\gamma/9$.

For (F), (6.10) and (6.9) give complementary lower and upper bounds on $\kappa$. Eliminating it yields
$$3N(\gamma-2\sigma)^2+(2\gamma-6\sigma)n_1
 +(12\gamma-18\sigma)\rho_n+6(\gamma-2\sigma)\rho_s+\gamma\iota_e
\le\gamma(2-\gamma)(7\gamma-12\sigma).$$
Dropping the nonnegative terms proves (F) only in its stated region. The code respects that condition.

The terms $36k_w,108k_w$ and all bounded corrections are $O(r)$ in the attempted low-coefficient domain, so they vanish after division by $r^2$.

### 6.5 Intersections of unmarked strong hyperedges

The unmarked hyperedges of strong groups must meet one another, and their vertices have little room to do so.

**Lemma 15.** For every $A\in\mathcal N$,
$$3k_s-1\le2r-q-R_A.$$

*Proof.* Let $v\in A$ have residual degree $j$. If $v$ lies in more than $2-j$ other hyperedges of $\mathcal N$, then, since its degree in $H'$ is at most four, its block consists of $j$ residual points and $4-j$ hyperedges of $\mathcal N$, and contains no distinguished hyperedge. Let $m\le4-j$ be the number of strong groups it meets. Remove these $m$ group blocks. In each of their distinguished hyperedges choose a residual triple disjoint from the block of $v$ and from the triples already chosen; at most $j+3(m-1)\le9$ points are forbidden, so one of the ten disjoint triples is free. The block of $v$ and these $m$ triple blocks are $m+1$ disjoint four-blocks, contradicting maximum cardinality.

So a vertex of residual degree $j$ meets at most $2-j$ other hyperedges of $\mathcal N$; the group vertex, with $j=0$, meets exactly two. Since $p_A=0$, write $n_j$ for the number of vertices of $A$ of residual degree $j\le2$. Then $n_0+n_1+n_2=r$ and $n_1+2n_2=q+R_A$. The other $3k_s-1$ hyperedges of $\mathcal N$ meet $A$, so $3k_s-1\le2n_0+n_1=2r-q-R_A$. $\square$

In particular $k_s\le(2r-q+1)/3$, so $\kappa\le(2-\gamma)/3$. The two lower bounds on $\kappa$ used for (B) and (F) remain valid when the nonnegative terms are dropped. Together with $k_s\le N_c/4$ and the bound $\kappa\le N(3-\gamma+\sigma)/6$ from (B), the certificate uses the necessary condition

$$\max\left(0,\ \frac3\gamma\Bigl(L_0-\frac{\gamma(2-\gamma)}{2}\Bigr),\ \frac{N(\gamma-2\sigma)-2\gamma(2-\gamma)}{\gamma}\right)
\le\min\left(\frac N4,\ \frac{2-\gamma}{3},\ \frac{N(3-\gamma+\sigma)}{6}\right).\tag{G}$$

## 7. The asymptotic bound

**Theorem 1 (proposed asymptotic result).** Subject to the mathematical lemmas above,
$$\liminf_{r\to\infty}\frac{g(r)}r\ge3.1108.$$

*Proof.* Suppose there is a sequence with limiting excess $x<0.1108$. Section 4 supplies (4.3), the parameter domain, and the stability estimate. The sparse case $\gamma<1$ is excluded as follows. Since $\lambda<0.0887$,
$$\frac vN\ge\frac{3-\gamma-3\lambda}{2(3-\gamma)}
\ge\frac12-\frac{3\lambda}{4}\ge0.433>3/14.$$
Thus (5.1) implies $\delta\ge K_+/30$. The same baseline handles $K\le0$, giving
$$x\ge\frac{15\lambda+7-3\gamma}{24}
\ge\frac{22-18\gamma}{24}>1/6>0.1108.$$
Therefore $1\le\gamma\le2$.

The remaining necessary inequalities are
$$\lambda\ge c(\gamma),\quad (A)\text{–}(G),\quad
x\ge\frac54\bigl(\lambda+\max(R_{\mathrm{rat}},W_{\mathrm{tr}})\bigr)+\frac\sigma4.$$
The program `code/verify_snd_intersection.py` proves that the last right-hand side is at least $0.1108$ throughout the feasible part of
$$1\le\gamma\le2,\quad0\le\lambda\le0.08864,\quad0\le\sigma\le0.4432.$$
Here $\sigma<\gamma$ and $9\sigma<4\gamma$, so the sign requirements for (D) and (E) hold. Constraint (F) is applied only to interval boxes wholly inside $\sigma<\gamma/3$; the rest are handled by the other constraints or subdivision. This contradicts $x<0.1108$. $\square$

The numerical minimum of the same system is about $0.110802$, at $\gamma\approx1.681$, $\lambda=c(\gamma)\approx0.0379$, $\sigma\approx0.254$. The certificate therefore gives four decimals; it does not compute the minimum exactly.

## Verification status

The final minimization is checked with exact rational arithmetic (Appendix A). The incidence lemmas of Section 6 were also tested on 1,200 random finite block systems by `code/audit_snd_finite_systems.py`; these tests do not replace their proofs. The algebra of Sections 3 and 5 is checked symbolically by `code/verify_rainbow_constant.py`. Independent review of the combinatorial chain remains pending.

## Appendix A. The arithmetic certificate

The code's variable `c` denotes $\lambda$; the function `root_lower` computes a rational lower enclosure of $c(\gamma)$ by 32 bisection steps. All interval pruning and acceptance use exact `Fraction` arithmetic. A box is removed only if a proved necessary condition among (A)–(G) fails on the whole box; it is accepted only if its objective lower bound is at least $0.1108$. Remaining boxes are split at rational midpoints. A resource limit causes failure, never acceptance.

The run gives
```text
VERIFIED 0.1108
rational_leaves 1996
empty 1276
splits 3271
```
The smallest accepted rational lower bound is
$$\frac{5042199332941370088036015839}{45507211152329020245278720000}>0.1108.$$
The verifier uses the standard library only and is run with `python3 -S`; optimized Python is rejected because its assertions are part of the check.

## Acknowledgements and research status

AI assistance (ChatGPT, OpenAI; Claude, Anthropic) was used for algebra, drafting, programming and internal review. The author is responsible for the mathematical claims. No priority is claimed.


## References

1. P. Erdős and L. Lovász, *Problems and results on 3-chromatic hypergraphs and some related questions*, in **Infinite and Finite Sets** (Keszthely, 1973), Colloq. Math. Soc. János Bolyai 10, North-Holland, 1975, 609–627.
2. V. Sivashankar, *An Improved Lower Bound for the Erdős–Lovász Cover Number Problem*, arXiv:2606.24878v2, 2026. https://arxiv.org/abs/2606.24878
3. J. Kahn, *On a problem of Erdős and Lovász. II: n(r)=O(r)*, Journal of the American Mathematical Society **7** (1994), 125–143.
4. J. Barát, *Intersecting and 2-intersecting hypergraphs with maximal covering number: the Erdős–Lovász theme revisited*, arXiv:2011.04444.
5. D. Munhá Correia, A. Pokrovskiy and B. Sudakov, *Short Proofs of Rainbow Matchings Results*, International Mathematics Research Notices **2023**, no. 14, 12441–12476. https://doi.org/10.1093/imrn/rnac180. Journal-version Theorem 1.2: https://people.math.ethz.ch/~sudakovb/rainbow-matchings-short-proofs.pdf
