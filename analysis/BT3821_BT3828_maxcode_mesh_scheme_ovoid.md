# Passes 3821–3828 — maximal-code census, exact adjacent mesh, holonomy scheme, Monster-pair census, and ovoid-flag completion

## Release status

`PASS_EXACT_EIGHT_FRONT_COMPONENT_SOURCE_MONSTER_EXTERNAL_RUNTIME_PENDING`

Semantic certificate:

```text
b141dd0f82e4a6b1ee62d1c57f0e92bdfc9f58d3b32515f9521a0175fdca88a1
```

The verifier is component-isolated. Five independently executable certificates cover the maximal-code, mesh, abstract-Monster, ovoid, and association-scheme computations. The top-level loader verifies a content-addressed source archive, recomputes the components separately, checks their canonical SHA-256 digests, and assembles the frozen aggregate certificate. This prevents the two separate 51,840-element permutation actions from competing for memory while retaining exact CI reproduction.

Local validation closed all five components, aggregate equality, two focused tests, and Python compilation. No GAP, `mmgroup`, remote-CI, PDF, hardware, or laboratory result is promoted.

## Result map

| front | exact result |
|---|---|
| maximal `[36,17,8]` codes | exact total census, orbit-explosion lower bound, and one explicit free `U4(2):2` orbit |
| adjacent multiport | exact 418-rotation nearest-neighbor mesh in 69 layers, improving the previous 512-rotation candidate |
| holonomy scheme | complete Krein table, four fusions, no Q-polynomial ordering, and exact Terwilliger dimensions 79 and 10 |
| compressed Monster search | all 51,840 ordered abstract standard pairs in two conjugacy orbits; external Monster runtime remains pending |
| quadratic parent plus ovoids | all 200 ovoids identified objectwise as 40 W33 points and 160 W33 flags |
| bonkers I | the 160 tripods are exactly the complete W33 point-line flag set |
| bonkers II | tripod port columns collapse four-to-one onto the 40 W33 line-versus-spread columns |
| bonkers III | the `1+27+36+40+160` carrier is one rank-48 `O_6^-(2)` orbital coherent configuration |

# I. Exact maximal-code census

Let `C` be the six-dimensional binary character code on the 36 nonsingular vectors of the minus-type quadratic space:

\[
C=[36,6,16],
\qquad
W_C(z)=1+27z^{16}+36z^{20}.
\]

The discriminant quadratic module `C^⊥/C` is the 24-dimensional minus-type orthogonal space `O^-_{24}(2)`, of Witt index eleven. Maximal doubly-even extensions correspond to maximal totally singular eleven-spaces. Their exact number is

\[
\boxed{
N=\prod_{i=2}^{12}(2^i+1)
=240137905387279785868125
}.
\]

Since `|U_4(2):2|=51,840`, the number of group orbits is at least

\[
\boxed{
\left\lceil\frac{N}{51840}\right\rceil
=4632289841575613440
}.
\]

A literal orbit-representative ledger is therefore not materialized. The exact census and orbit-explosion theorem are the complete feasible global classification result.

The verifier constructs one explicit maximal extension

\[
D=[36,17,8]
\]

with weight distribution

\[
1+225z^8+9555z^{12}+55755z^{16}+55755z^{20}
+9555z^{24}+225z^{28}+z^{36}.
\]

Its stabilizer in `U_4(2):2` is trivial, so its orbit has size 51,840. Its 225 weight-eight words have coordinate-degree profile

\[
42^5,\quad48^{15},\quad54^{15},\quad60^1.
\]

# II. Exact adjacent multiport mesh

For

\[
H=\frac{2A_{36}-J}{6},
\]

the exact symbolic adjacent Givens elimination uses the certified port permutation

```text
2,1,6,3,4,5,0,8,11,12,13,10,14,7,9,15,16,26,
28,18,31,21,24,34,17,27,35,25,19,29,22,30,20,32,23,33
```

and yields

\[
\boxed{418\text{ nontrivial adjacent rotations}}
\]

in

\[
\boxed{69\text{ disjoint-gate layers}},
\]

with 212 eliminations skipped because their entries vanish exactly. The residual diagonal is `diag(1,…,1,-1)`, so one terminal `π` phase completes the transform.

Every gate is frozen through exact rational squared parameters:

\[
c=\operatorname{sgn}(c)\sqrt{c^2},
\qquad
s=\operatorname{sgn}(s)\sqrt{s^2},
\qquad c^2+s^2=1.
\]

There are 144 distinct `c²` values and the largest denominator is 3,315,585. The parameter hash is

```text
5c933cc2e6d2484e97894f3ca1f71627214238e41a68cd59b7527993d2b06b6b
```

The proved intervals are

\[
35\le g\le418,
\qquad
6\le d\le69.
\]

The gate lower bound follows from connectedness of the interaction graph. The depth lower bound follows because a depth-`d` disjoint two-mode circuit spreads one input to at most `2^d` outputs, whereas each column of `H` has support 36. Global optimality is not claimed.

# III. Complete rank-five holonomy scheme

The 120 Fischer triples carry five Gram relations

\[
1,\quad-\frac12,\quad-\frac16,\quad0,\quad\frac13,
\]

with valencies

\[
1,2,54,36,27
\]

and primitive multiplicities

\[
1,20,24,60,15.
\]

The first eigenmatrix is

\[
P=\begin{pmatrix}
1&2&54&36&27\\
1&-1&-9&0&9\\
1&2&-6&6&-3\\
1&-1&3&0&-3\\
1&2&6&-12&3
\end{pmatrix},
\]

and the second is

\[
Q=\begin{pmatrix}
1&20&24&60&15\\
1&-10&24&-30&15\\
1&-10/3&-8/3&10/3&5/3\\
1&0&4&0&-5\\
1&20/3&-8/3&-20/3&5/3
\end{pmatrix}.
\]

All Krein parameters are exact. Exhausting primitive-idempotent orders proves that no Q-polynomial ordering exists. Exhausting every partition of the four nontrivial relations gives exactly four fusion schemes: the full scheme, `[(0),(1),(2,4),(3)]`, `[(0),(1),(2,3,4)]`, and the complete rank-two fusion.

The automorphism group is `U_4(2):2`, of order 51,840. A point stabilizer has order 432, subdegrees `1,2,27,36,54`, and 83 orbitals on ordered pairs. The Terwilliger algebra has exact rational dimensions

\[
\boxed{\dim T=79},
\qquad
\boxed{\dim Z(T)=10}.
\]

The certificate contains 79 independent word matrices modulo 1,000,003, exact rational closure on all 83 stabilizer orbitals, and an exact ten-dimensional center nullspace satisfying every center constraint. The Wedderburn block decomposition remains open.

# IV. Complete internal standard-pair census

Inside exact `U_4(2)`, fix an involution `a` in the size-45 class. Its centralizer has order 576. Exactly 1,152 order-five elements `b` satisfy

\[
|a|=2,
\qquad |b|=5,
\qquad |ab|=9,
\qquad |[a,b]|=3.
\]

The centralizer splits them into two orbits of size 576. A representative from each orbit generates all 25,920 elements. Hence the complete ordered-pair census is

\[
\boxed{45\cdot1152=51840}.
\]

The two orbits land in the two distinct order-nine classes, each of size 2,880. This closes the abstract candidate search before any Monster calculation.

No GAP/CTblLib or `mmgroup` result artifact exists. The fail-closed promotion harness requires serialized runtime words, provenance, exact group and class relations, all 36 axes, 135 frames, 120 triples, the `[36,6]` code distribution, the `45+216+270+120` line split, and all frozen object hashes. No external Monster embedding or character restriction is claimed.

# V. The 64-point parent and all 200 ovoids

The verifier reconstructs all 200 ovoids of `GQ(4,2)`, split under the order-51,840 group as

\[
40+160.
\]

The 40-object orbit is the plane-ovoid orbit and the 160-object orbit is the tripod orbit. Combining zero, 27 singular points, 36 nonsingular ports, 40 plane ovoids, and 160 tripods gives

\[
1+27+36+40+160=264
\]

objects. Their complete `O_6^-(2)` orbital coherent configuration has

\[
\boxed{48\text{ relations}}.
\]

The nonsingular-point versus tripod action splits as `40+120`. Its narrow 40-orbit generates a `36×160` incidence matrix of row weight 40, column weight 9, and rational rank 16. Its Gram values are 40 on the diagonal, 16 for spread-adjacent pairs, and 4 for spread-nonadjacent pairs. The 160 columns collapse into 40 distinct columns, each repeated four times.

# Bonkers I — ovoids are W33 points and flags

Objectwise reconstruction proves

\[
\boxed{40\text{ plane ovoids}=40\text{ W33 points}},
\]

and

\[
\boxed{160\text{ tripods}=160\text{ incident W33 point-line flags}}.
\]

The special tripod-plane orbit is precisely flag incidence; every special pair consists of disjoint ovoids, and every W33 flag occurs once.

# Bonkers II — a fourfold cover of W33 lines

The 160 tripod port-incidence columns have exactly 40 distinct supports, each repeated four times. The quotient `36×40` matrix is objectwise equal to the independently reconstructed W33 line-versus-spread incidence matrix. Thus

\[
\boxed{160\text{ tripods}\longrightarrow40\text{ W33 lines}}
\]

is a canonical four-to-one quotient, with each line class containing its four incident W33 flags.

# Bonkers III — rank-48 coherent completion

The five fibers

\[
\boxed{1\;|\;27\;|\;36\;|\;40\;|\;160}
\]

close as one rank-48 orbital coherent configuration under `O_6^-(2)`. This places the zero vector, quadratic singular/nonsingular split, W33 points, W33 lines through tripod classes, and every W33 flag inside one exact finite action.

# Evidence boundary

Proved here:

- the exact maximal-extension census and orbit lower bound;
- one explicit free maximal-code orbit;
- an exact symbolic 418-rotation adjacent mesh in 69 layers;
- all Krein parameters, all fusions, no Q-polynomial ordering, and exact Terwilliger dimensions 79 and 10;
- the complete two-orbit abstract standard-pair census;
- all 200 ovoids and the exact W33 point-line-flag dictionary;
- the rank-48 combined coherent configuration.

Not proved here:

- a materialized representative from every one of at least 4.632 quintillion code orbits;
- global gate-count or depth optimality;
- serialized Monster words, a Monster embedding, or an executed character fusion;
- a Leech/rootless identification;
- hardware fabrication, laboratory performance, remote CI, or PDF success.
