# Passes 1537–1541 — five exact frame-dual continuations

## Executive result

This packet executes the five continuations opened by Pass 1536. It rebuilds
`W(3,3)`, the canonical `540 x 240` frame/edge matrix `M`, and the intrinsic
`45 x 240` K4,4 octet matrix `K` from projective coordinates. The frozen worker
passes **54/54** checks.

The exact conclusions are:

1. the octet Gram image is an absolutely irreducible `14` over `F2`, literally
   equal—after the natural octet-to-edge map—to the Pass-1416 signed-turn image;
2. over `F3`, the apparent `15` is **not** irreducible but splits as `1 + 14`;
3. the integral octet lattice has Smith form `1^44,3`, with saturation obtained
   by adjoining the all-ones edge vector;
4. the natural oriented K4,4 lift realizes the coexact degree-`30` constituent,
   not either degree-`45` constituent;
5. the 45 octets yield 405 exact-8 resolution cuts and add 240 independent XOR
   directions to the global Hoffman-coloring system;
6. codeword weight obeys an exact three-body formula. The ordinary 45-point SRG
   association algebra alone is insufficient to determine the enumerator;
7. exact syndrome decoding corrects every single edge error and uniquely
   identifies `25440/28680 = 212/239` of all double-edge errors, while the
   remaining ambiguity is exactly controlled by the 540 frame words.

The global nine-cover resolution and the full `2^45` weight enumerator remain
open. The min-sum table is a fixed-seed finite experiment, not a threshold.

---

## Pass 1537 — modular Gram intertwiners

Let

\[
G_K=KK^{\mathsf T}=16I+A_{45}.
\]

The exact modular facts are

\[
\operatorname{rank}_{2}G_K=14,
\qquad
\operatorname{rank}_{3}G_K=15,
\qquad
G_K^2=0\pmod 2,
\qquad
G_K^2=0\pmod 3.
\]

### Characteristic two

Set

\[
J_2=K^{\mathsf T}(G_K\bmod2).
\]

Then `rank(J2)=14`. If `F_1416` is the integral signed-turn bridge from
Pass 1416, the verifier proves in the common 240-edge coordinates

\[
\boxed{\operatorname{im}J_2=\operatorname{im}(F_{1416}\bmod2).}
\]

This equality is equivariant: in characteristic two, signed and unsigned edge
permutations coincide. Restricting the four symplectic generators to the
14-space generates the full matrix algebra

\[
M_{14}(\mathbb F_2),
\]

of dimension `196`. Thus the module is absolutely irreducible.

### Characteristic three

The 15-dimensional image contains the constant vector. Its fixed space has
dimension one, and the invariant dual functional

```text
(2,1,1,1,1,1,1,1,1,1,1,1,1,1,1)
```

is nonzero on that fixed vector. Therefore the extension splits. The quotient
action generates `M_14(F3)`, again of dimension `196`:

\[
\boxed{\operatorname{im}(G_K\bmod3)\cong\mathbf1\oplus V_{14}.}
\]

This corrects the tempting but false reading that rank 15 automatically means a
15-dimensional irreducible.

---

## Pass 1538 — integral/ternary lift and the coexact 30

Over the integers,

\[
\boxed{\operatorname{SNF}(K)=\operatorname{diag}(1^{44},3).}
\]

The proof is explicit:

- `rank_F2(K)=45`, `rank_F3(K)=44`;
- the unique ternary row dependency is the all-ones coefficient vector;
- each W33 edge belongs to three octets, so
  \(\sum_{o=1}^{45}K_o=3\mathbf1_{240}\);
- adjoining \(\mathbf1_{240}\) gives the saturated lattice;
- an original maximal minor is `-19683 = -3^9`;
- a saturated maximal minor is `5120 = 2^10*5`;
- the saturated matrix has full rank modulo both 2 and 5.

Hence

\[
\operatorname{sat}(\operatorname{row}_{\mathbb Z}K)
=
\operatorname{row}_{\mathbb Z}K+\mathbb Z\mathbf1_{240},
\qquad
\operatorname{sat}/\operatorname{row}_{\mathbb Z}K\cong\mathbb Z/3.
\]

Over `F3`, the map `K^T:F3^45 -> F3^240` has kernel exactly the constants and
image dimension 44.

### The requested 45+45 fusion test

Choose the canonical bipartition of every K4,4 octet. Let `S` be its signed
point incidence and `U` its consistently oriented edge incidence. The exact
identities are

\[
S^{\mathsf T}S=8I-4A+J,
\qquad
dU^{\mathsf T}=-4S^{\mathsf T}.
\]

Define

\[
V=4U+Sd.
\]

Then

\[
dV^{\mathsf T}=0,
\qquad
L_1V^{\mathsf T}=4V^{\mathsf T},
\qquad
\operatorname{rank}_{\mathbb Q}V=30.
\]

The map is equivariant for the signed octet and signed edge actions. Its
restricted group algebra is the full `M_30(F_1000003)`, dimension `900`.
Therefore:

\[
\boxed{\operatorname{im}V\text{ is the absolutely irreducible coexact }30.}
\]

So the natural oriented-octet construction does **not** split the two degree-45
constituents fused by `PGSp(4,3)` into degree 90. It geometrically identifies the
remaining degree-30 constituent instead.

---

## Pass 1539 — exact-8 octet cuts for the resolution problem

Every frame matching intersects every octet edge set in either zero or two
edges. For each octet, exactly 72 frames have intersection two. If `x_fc`
indicates that frame `f` has color `c`, every resolution must satisfy

\[
\boxed{
\sum_{f:\,|f\cap o|=2}x_{fc}=8
\quad
(o=1,\ldots,45;\ c=1,\ldots,9).
}
\]

There are 405 such exact cardinality equations, each supported on 72 variables.
Over the rationals each is one-half the sum of the 16 edge/color equations in
that octet, so the LP row space does not grow.

Modulo two, division by two exposes new parity information:

```text
per color:       195 -> 225     (+30)
global system:  2100 -> 2340    (+240)
K9-fixed system:2109 -> 2349    (+240)
```

The deterministic XOR-support hash is

```text
f7d6cdf48d72cf35ef6ba9dd29d1ea99cb0ab171f98e8409366db17807e3dc69
```

These are valid parity-strengthening cuts. They do not decide whether the
Hoffman 9-coloring exists.

---

## Pass 1540 — weight-enumerator programme and shortcut falsifier

For a message subset `X` of the 45 octets, let

- `e(X)` be the number of edges induced by `X` in `SRG(45,32,22,24)`;
- `t(X)` be the number of the 240 distinguished edge-signature triples fully
  contained in `X`.

Every W33 edge belongs to a unique distinguished triple of octets. Counting
hyperedges meeting `X` in one, two, or three vertices gives the exact identity

\[
\boxed{w(X)=16|X|-2e(X)+4t(X).}
\]

This immediately falsifies an SRG-only association-algebra shortcut. There are
ordinary and distinguished triangles with the same values

\[
|X|=3,
\qquad
e(X)=3,
\]

but weights 42 and 46 respectively. The three-body orbit `t(X)` is essential.

The worker exhausts message layers 0 through 6 and, using the all-ones codeword,
the complementary layers 39 through 45. Globally, Pass 1536 plus complementation
give the exact coefficients

\[
A_0=1,
\quad A_{16}=45,
\quad A_{224}=45,
\quad A_{240}=1.
\]

The exhaustive two-generator layer contributes exactly

\[
720\text{ words of weight }30,
\qquad
270\text{ words of weight }32,
\]

and the complementary 43-generator layer contributes the corresponding weights
210 and 208. These are exact layer contributions, not claims that the global
coefficients $A_{30},A_{32},A_{208},A_{210}$ receive no contributions from other
message layers.

A Gray-code prefix-shard engine is also executed on the canonical 25-zero prefix,
exhausting its `2^20` suffix words and freezing the shard histogram/hash. The
complete `2^45` census is not claimed; the packet explicitly records that as an
open computational frontier.

---

## Pass 1541 — exact decoder and explicit noise falsifier

Use `K` as the parity-check matrix of the `[240,195,4]` frame code.

### Exact syndrome facts

The 240 columns are distinct nonzero triples, so every single edge error has a
unique syndrome. Among the `C(240,2)=28680` double errors:

```text
25440 pairs have unique syndromes,
 3240 pairs lie in ambiguous buckets,
```

hence an ambiguity-declaring exact table corrects the fraction

\[
\boxed{\frac{25440}{28680}=\frac{212}{239}}
\]

of all weight-two errors.

There are exactly 1620 ambiguous syndrome buckets, each containing two pairs.
Their symmetric differences give exactly 540 weight-four codewords, and those
supports are exactly the 540 canonical frame matchings. Equivalently, every BEC
erasure pattern of size at most three is uniquely recoverable; the first minimal
dependencies have size four and are precisely the frames.

### Explicit BSC model

The separate falsifier uses:

- independent W33-edge flips with probability `p`;
- perfect syndrome readout;
- the all-zero codeword;
- normalized min-sum (`0.8`) for at most 30 iterations;
- seed `1541`, 200 trials at each of `p=0.002,0.005,0.01,0.02`.

The finite sample shows that naive min-sum convergence is not equivalent to
correct decoding: at several points it converges to a wrong codeword. The table
is therefore kept as a decoder falsifier, not advertised as a threshold. Exact
closed-form success probabilities are reported separately for the guaranteed
`t=1` decoder and the unique-weight-two table.

---

## External anchors

- J. MacWilliams, “A theorem on the distribution of weights in a systematic
  code,” *Bell System Technical Journal* **42** (1963), 79–94 — dual weight
  enumerators and the MacWilliams transform.
- R. G. Gallager, “Low-density parity-check codes,” *IEEE Transactions on
  Information Theory* **8** (1962), 21–28 — the original LDPC/message-passing
  framework.
- T. Richardson and R. Urbanke, *Modern Coding Theory*, Cambridge University
  Press — finite-length message passing and the distinction between experiments,
  ensemble density evolution, and thresholds.

## Parallel-frontier reconciliation

Passes 1601--1605 landed after this namespace was reserved and before release.
They own the integral Smith form of the frame matrix `M`, the Bockstein exact
sequence, and the half-incidence matrix

\[
J=\frac12 MK^{\mathsf T}\in\{0,1\}^{540\times45}.
\]

In particular, Pass 1603 already owns the row-degree `6`, column-degree `72`,
and thirty-dimensional half-incidence/Bockstein quotient. Pass 1539 does not
relabel those facts as new. Its additional result is the colored lift: the
405 exact-8 equations and the exact global XOR-rank calculation
`2100 -> 2340` (`2109 -> 2349` after the standard symmetry fixing).

Pass 1604 also owns the integral Smith data of the earlier `C` and `F` bridges.
Pass 1537 adds the missing equivariant module certificate: the mod-2 octet-Gram
image is literally the Pass-1416 image and absolutely irreducible, while the
mod-3 rank-15 image splits as `1+14`. Pass 1538's oriented map `V=4U+Sd` is a
different construction and supplies the explicit degree-30 coexact carrier.

## Evidence boundary

All module, lattice, rank, cut, low-layer enumerator, syndrome, and dependency
claims are exact and deterministically rebuilt. The min-sum results are seeded
finite experiments. No quantum-code parameter, optical threshold, detector-loss
threshold, global resolution verdict, or complete `2^45` weight enumerator is
inferred.
