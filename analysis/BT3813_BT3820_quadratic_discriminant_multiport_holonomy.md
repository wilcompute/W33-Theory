# Passes 3813–3820 — quadratic parent, discriminant chain, two-mode compiler, holonomy scheme, and compressed descent

## Status

`PASS_EXACT_EIGHT_FRONT_SOURCE_MONSTER_WORDS_HARDWARE_CI_PDF_PENDING`

Semantic certificate:

```text
2b57dd96e94217573cf52a7031280ccbaaff8439ec86a3029d985723f10e6101
```

The verifier rebuilds the complete six-bit minus quadratic space, all 651 projective lines, the 36 nonsingular ports, 27 singular points, 45 singular lines, 120 all-nonsingular lines, and 135 Lagrangian three-spaces. Nothing in the internal theorem packet is imported as a numerical table.

Focused validation:

```text
PASS 2b57dd96e94217573cf52a7031280ccbaaff8439ec86a3029d985723f10e6101
2 passed
```

The active neighboring reservations are preserved: Passes 3787–3794 own the architecture packet and Passes 3795–3812 own the plane-ovoid/rootless/axial packet. This packet uses the disjoint range 3813–3820.

---

# Pass 3813 — the common six-bit parent is a 64-point bent Cayley graph

Let

\[
q(x)=x_0x_1+x_2x_3+x_4x_5+x_4+x_5
\]

on `F2^6`, and let

\[
\beta(x,y)=q(x+y)+q(x)+q(y).
\]

The nonzero vectors split into 27 singular and 36 nonsingular vectors. The 651 projective lines split exactly as

\[
45+216+270+120,
\]

according to whether they contain zero, one, two, or three nonsingular points.

Define the Cayley graph on all 64 vectors by

\[
x\sim y \iff q(x+y)=1.
\]

Its adjacency matrix satisfies the exact identity

\[
A_{64}^2=16I+20J.
\]

Hence it is

\[
\boxed{\operatorname{SRG}(64,36,20,20)}
\]

with spectrum

\[
36^1,\quad 4^{27},\quad (-4)^{36}.
\]

The neighborhood of zero is the 36-point nonsingular set. Its induced graph is the complement of the spread graph `SRG(36,15,6,6)`. The 27 nonzero nonneighbors induce the Schläfli graph, the complement of `SRG(27,10,1,5)`.

Thus the 27-point GQ carrier and 36-port Hadamard carrier are the two subconstituents of one explicit 64-point bent-function graph.

---

# Pass 3814 — the discriminant form and maximal even-overlattice chain

The six-dimensional code is

\[
C=\{(\beta(a,x))_{x\in N}:a\in\mathbf F_2^6\},
\]

with

\[
[36,6,16],\qquad W_C=1+27z^{16}+36z^{20}.
\]

For the rooted Construction-A lattice

\[
L(C)=2^{-1/2}\{z\in\mathbf Z^{36}:z\bmod2\in C\},
\]

the discriminant module is

\[
A_L\cong C^\perp/C\cong(\mathbf Z/2\mathbf Z)^{24},
\]

and its quadratic form is represented code-theoretically by

\[
q_L(c+C)=\frac{\operatorname{wt}(c)}2\pmod{2\mathbf Z}.
\]

Every even overlattice corresponds exactly to a doubly-even intermediate code

\[
C\subseteq D\subseteq C^\perp.
\]

An explicit eleven-step isotropic chain reaches a maximal doubly-even code

\[
\boxed{[36,17,8]}.
\]

Its complete weight enumerator is

\[
1+225z^8+9555z^{12}+55755z^{16}+55755z^{20}
 +9555z^{24}+225z^{28}+z^{36}.
\]

The associated maximal even overlattice has determinant

\[
\boxed{4}.
\]

The isotropic rank cannot reach twelve: that would produce an even unimodular lattice of rank 36, whereas an even unimodular integral lattice has rank divisible by eight. Therefore eleven is the global maximum, not merely the maximum reached by the explicit chain.

The determinant spectrum along the chain is

\[
2^{24},2^{22},\ldots,2^4,2^2.
\]

This classifies every even overlattice parametrically by a totally isotropic subspace of `C^perp/C`, and supplies an explicit maximal representative.

---

# Pass 3815 — exact two-mode compilation

Let

\[
H=\frac{2A_{36}-J}{6}.
\]

The verifier reconstructs the 21-dimensional `-1` eigenspace and performs exact rational Gram–Schmidt to obtain 21 pairwise orthogonal primitive integer vectors.

For each vector, a balanced binary tree of exact two-mode Givens rotations maps the vector to one mode. Every coefficient is specified as a signed square root of a rational number. A single `pi` phase on that mode, followed by the inverse tree, implements the Householder reflection exactly.

The complete proof-carrying compilation has

```text
21 integer reflections
944 two-mode rotations
21 single-mode pi phases
sequential balanced-tree depth 221
maximum single-reflection depth 13
```

Compiler SHA-256:

```text
e43cf1932b966481c42dadd5346fb0f163f31be9efcac97d1b51ab33ad228a54
```

An independent adjacent QR pass exploits exact zeros in the W33 matrix and reduces the candidate topology to

```text
512 nearest-neighbor rotations
69 layers
one terminal sign
```

with rational-square parameter hash

```text
a042de7d5bc6f202adde35736484129a9638fa6fcf7a5ecf346f88280c3ea92b
```

The 944-gate tree construction is the exact proof-carrying result. The 512-gate adjacent mesh is a deterministic algebraic/numerical optimization candidate and is not promoted as the globally optimal exact circuit.

A universal lower bound follows from support growth. A depth-`d` circuit of disjoint two-mode gates can spread one input to at most `2^d` outputs. Every column of `H` has support 36, so

\[
\boxed{d\ge \lceil\log_2 36\rceil=6}.
\]

---

# Pass 3816 — the four-angle holonomy frame closes to a rank-five association scheme

The 120 Fischer triples form the share-a-port graph of degree 27. Its forty intrinsic distance-three fibers have size three.

Let

\[
F=3I-J_{\rm fiber},
\qquad
Q_{20}=FAF+9F.
\]

Then

\[
Q_{20}^2=108Q_{20},
\qquad \operatorname{rank}Q_{20}=20.
\]

The normalized Gram entries are

\[
1,-\frac12,-\frac16,0,\frac13.
\]

These five values are not merely angles: their relation matrices close exactly under multiplication. The valencies are

\[
\boxed{1,2,54,36,27}.
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

with multiplicities

\[
\boxed{1,20,24,60,15}.
\]

The exact second eigenmatrix is

\[
Q=\begin{pmatrix}
1&20&24&60&15\\
1&-10&24&-30&15\\
1&-10/3&-8/3&10/3&5/3\\
1&0&4&0&-5\\
1&20/3&-8/3&-20/3&5/3
\end{pmatrix}.
\]

The rank-20 vectors are centered and tight, so they form a spherical 2-design. Their cubic fixed-vector moment is `3/2`, not zero, so they are not a spherical 3-design.

The forty-fiber quotient is W33. For its 240 edges, every `3x3` cross-block lies in the zero-inner-product relation. For its 540 nonedges, the cross-block splits into one perfect matching in the `1/3` relation and its six-entry complement in the `-1/6` relation.

---

# Pass 3817 — compress the Monster descent to one 36-vertex seed

The 36-vertex spread graph alone reconstructs the finite fingerprint tower.

1. Its graph-theoretic `K4`s are exactly the 135 Lagrangian frames.
2. Its rank-15 Norton product reconstructs exactly 120 triples.
3. The binary left kernel of the axis–triple incidence has dimension six.
4. Its nonzero words split into 27 words of weight 16 and 36 words of weight 20.
5. The 651 abstract projective lines of this code split as `45+216+270+120`.

The weight-20 codewords are canonically the complement-neighborhood rows of the original graph. Therefore the 36 axes are recovered inside their own code, rather than inserted by an external labeling.

Frozen hashes:

```text
135 K4 frames:
9c59605c3da8d39651555da942133650977b9c9b22135a3993c78b993bbaaf39

120 Norton triples:
cf12c3080fb3673b64aad5e339df2eaee3f2d16a8932fbc4662bef67e81da398

651 abstract lines:
a8dc7bd4fa3079c95ddf029131a94840daf6222f3701d92254ff7ef192b354d9
```

The fail-closed promotion harness

`analysis/w33_pass3817_monster_seed_compression_harness.py`

accepts an aligned 36-point candidate action, verifies the exact graph, optionally verifies a generated permutation group of order 25,920 or 51,840, and then regenerates all downstream finite fingerprints. Passing it is not a Monster embedding: serialized Monster words and character fusion remain separately required.

---

# Pass 3818 — Bonkers I: frames and triples resolve every port pair

Let `F` be the 36 by 135 port–frame incidence matrix and `T` the 36 by 120 port–triple incidence matrix. Then

\[
FF^{\mathsf T}=15I+3A,
\]

because every orthogonal pair occurs in exactly three frames, while

\[
TT^{\mathsf T}=9I+J-A,
\]

because every nonorthogonal pair occurs in exactly one triple.

The graph terms cancel:

\[
\boxed{FF^{\mathsf T}+3TT^{\mathsf T}=42I+3J}.
\]

Therefore the weighted incidence carrier `[F | sqrt(3)T]` has squared singular values

\[
150^1,\qquad42^{35}.
\]

After removing the all-ones mode, the combined 135-frame plus 120-triple system is an exact tight resolution of the full 35-dimensional port-contrast space.

---

# Pass 3819 — Bonkers II: three odd unimodular neighbors

The maximal `[36,17,8]` doubly-even code has a two-dimensional quotient

\[
D^\perp/D\cong\mathbf F_2^2.
\]

Its three nonzero cosets give three singly-even self-dual `[36,18]` extensions. Construction A therefore produces three canonical odd unimodular rank-36 neighbors of the determinant-four maximal even lattice.

The three neighbors fall into two weight-enumerator types. Two have 16 words of weight six; the third has 10. Their distinct enumerators prove at least two inequivalent code/lattice neighbor types.

No claim is made that the two repeated-enumerator neighbors are equivalent merely because their enumerators agree.

---

# Pass 3820 — Bonkers III: exact discrete S3 curvature

On every nonedge of the W33 quotient, the `1/3` relation is a perfect matching between the two three-point fibers. Treat these matchings as an `S3` transport connection.

The complement of W33 has exactly 3,240 triangles. Their holonomy census is

```text
identity       1,080
transposition  2,160
three-cycle        0
```

Thus precisely one third of base triangles are flat and two thirds carry reflection curvature.

For all 59,670 simple four-cycles, the census is

```text
identity       11,070
transposition  29,160
three-cycle    19,440
```

Three-cycles first occur on length-four loops. Since triangle loops generate transpositions and four-cycles generate three-cycles, the exact holonomy group is the full

\[
\boxed{S_3}.
\]

This is a finite connection theorem, not a spacetime-curvature or physical gauge-field claim.

---

# Evidence boundary

Proved in the executable certificate:

- the 64-point `SRG(64,36,20,20)` quadratic parent and its two local subconstituents;
- the discriminant form model, maximal isotropic rank eleven, determinant-four maximal even chain, and three singly-even self-dual neighbors;
- the exact 21-reflection two-mode tree compiler and deterministic adjacent optimization candidate;
- the complete rank-five holonomy association scheme and both eigenmatrices;
- reconstruction of the 135/120/27/36/45 line tower from the 36-graph seed;
- the complementary design resolution and exact `S3` curvature census.

Not promoted:

- serialized Monster words, a Monster subgroup embedding, or Monster character restriction;
- Leech, rootless, or even-unimodular rank-36 identification;
- globally optimal two-mode gate count or depth;
- optical fabrication, detector, loss, or laboratory performance;
- remote CI or PDF success before it is observed.
