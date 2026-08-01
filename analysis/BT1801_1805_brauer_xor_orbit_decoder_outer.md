# Passes 1801–1805 — Brauer refinement, bounded XOR attack, three-body transfer algebra, exact syndrome decoding, and the coexact outer extension

## Executive result

This packet executes the five continuations opened after Passes 1537–1541 while preserving the results that landed concurrently in Passes 1606–1616, 1611–1615, and 1701–1705. The original local namespace collided during publication, so the release was moved intact to the reserved range **1801–1805** rather than overwriting another agent's files.

The deterministic verifier rebuilds from projective coordinates:

- the 40-point symplectic generalized quadrangle `W(3,3)`;
- its 240 edges and 40 isotropic lines;
- the 540 canonical line-pair frame matchings;
- the frame/edge matrix `M in {0,1}^{540 x 240}`;
- the 45 intrinsic induced `K4,4` octets and their matrix `K in {0,1}^{45 x 240}`;
- the half-incidence matrix `J=(1/2) M K^T`;
- the inner `PSp(4,3)` action and the canonical multiplier-minus-one similitude.

The aggregate certificate passes and has SHA-256

```text
0e79393320a6e50e5f2f9e4e0ff4982d8fb211b13951781ab4e0be4ba5adfec7
```

The exact conclusions are:

1. the known 30-dimensional binary Bockstein module has Brauer composition factors
   
   `1, {4a,4b}, 1, 6, 14`,
   
   where the pair `{4a,4b}` descends to one irreducible 8-dimensional `F2`-module with endomorphism field `F4`; the outer similitude acts on that field by Frobenius and exchanges the two four-dimensional constituents;
2. the complete resolution parity system has exact ranks `2100 -> 2340`, or `2109 -> 2349` after symmetry fixing, and the frozen XOR basis has a deterministic hash; an independently executable 4,860-variable HiGHS model with all 405 exact-eight cuts reached its 20-second bound without an incumbent, which is recorded only as a bounded falsifier;
3. the three-body octet hypergraph has exactly six `PSp(4,3)` orbits on triples and twenty on four-subsets, with exact up/down transfer matrices satisfying the orbit double-counting identity;
4. the ambiguity-declaring minimum-weight syndrome decoder has exact coefficients through error weight three
   
   `1, 240, 25440, 1576000`,
   
   and the weight-three syndrome set splits into exactly 110 inner-group orbits;
5. the canonical coexact degree-30 carrier extends to the multiplier-minus-one outer element with trace `+2`, eigenspaces `16+14`, and determinant `+1`; its sign twist has trace `-2`.

The global Hoffman nine-cover resolution, unrestricted maximum-likelihood decoding problem, complete `2^45` weight enumerator, and ATLAS class fusion of the outer element remain open.

---

## Pass 1801 — Brauer refinement and outer Frobenius on the Bockstein module

Passes 1606, 1611, and 1701 already established that the elementary two-torsion

\[
T=\operatorname{Tor}_2(\operatorname{coker}M)\cong\mathbb F_2^{30}
\]

is nonsemisimple and has composition-factor dimensions

\[
1,8,1,6,14.
\]

Pass 1801 independently rebuilds the Bockstein quotient and verifies

\[
\operatorname{rank}_{2}\beta=30,
\]

with exact kernel

\[
\boxed{
\ker\beta=\langle\mathbf1_{45}\rangle
\oplus\operatorname{im}(KK^{\mathsf T}\bmod2),
}
\]

of dimension 15.

A compatible invariant filtration has dimensions

\[
\boxed{1<9<10<16<30}
\]

and successive `F2`-factor dimensions

\[
\boxed{1,8,1,6,14}.
\]

### Density and commutant certificates

The restricted generated algebras and commutants are

| factor | generated algebra dimension | commutant dimension |
|---|---:|---:|
| 8 over `F2` | 32 | 2 |
| 6 | 36 | 1 |
| 14 | 196 | 1 |

Thus the 6- and 14-dimensional factors generate the full matrix algebras `M_6(F2)` and `M_14(F2)` and are absolutely irreducible. The 8-dimensional factor has a two-dimensional endomorphism field. A non-scalar centralizer element `z` satisfies

\[
\boxed{z^2+z+I=0,}
\]

so

\[
\operatorname{End}_{PSp(4,3)}(V_8)\cong\mathbb F_4,
\qquad
\operatorname{im}\mathbb F_2[PSp(4,3)]\cong M_4(\mathbb F_4).
\]

Over an algebraic closure the factor therefore splits into a Galois-conjugate pair of four-dimensional simples. The RWTH/MOC decomposition matrix for `U4(2)` in characteristic two lists precisely the simple degrees

\[
1,4,4,6,14,20,20,64.
\]

Consequently the algebraic-closure factors are identified, up to ordering of the conjugate pair, as

\[
\boxed{1,4a,4b,1,6,14.}
\]

This is a dimension-and-endomorphism-field identification. No uncomputed Brauer character values are claimed.

### Exact outer action

Let `s` be the canonical multiplier-minus-one similitude. On the `F4` centralizer,

\[
\boxed{s z s^{-1}=z^2.}
\]

This is the nontrivial Galois automorphism of `F4/F2`, so the full outer extension exchanges the unordered pair

\[
\boxed{4a\longleftrightarrow4b.}
\]

The complete 30-space has one-dimensional fixed space and zero-dimensional dual fixed space. The result refines, rather than replaces, the unlabeled composition series owned by the parallel packets.

---

## Pass 1802 — exact XOR rank and a reproducible bounded solver attack

For frame/color variables `x_fc`, the base parity system consists of:

- 540 one-color-per-frame equations;
- 2,160 edge/color equations.

The 45 octets provide 405 exact cardinality laws

\[
\sum_{f:J_{fo}=1}x_{fc}=8,
\qquad o=1,\ldots,45,
\quad c=1,\ldots,9.
\]

The exact binary ranks are

\[
\begin{array}{c|c|c}
\text{system} & \operatorname{rank}_{2} & \text{nullity}\\
\hline
\text{base} & 2100 & 2760\\
\text{base + symmetry} & 2109 & 2751\\
\text{base + octets} & 2340 & 2520\\
\text{base + octets + symmetry} & 2349 & 2511
\end{array}
\]

Hence the octet cuts add exactly

\[
\boxed{240}
\]

independent global XOR directions. The symmetry-fixed augmented reduced basis has hash

```text
1c1cdfce0dfc432f7a83faeccb08cabd0cb24330bbe4ee7d5bf154d1136aa532
```

The solver-neutral XOR compiler and this rank gain were already owned by Passes 1607, 1612, and 1702. Pass 1802 adds a separate executable MILP falsifier that literally builds:

```text
binary variables                    4860
frame/color equalities               540
edge/color equalities               2160
octet exact-eight equalities         405
total equality constraints          3105
fixed symmetry variables               9
constraint-matrix nonzeros         53460
```

The complete model hash is

```text
dac90bab2946d49d77680444f751c162f029896db7b90ecc4c55c91e81d1ece2
```

On the frozen local run, `scipy.optimize.milp`/HiGHS reached its 20-second limit without an incumbent:

```text
status code: 1
message: Time limit reached
incumbent: false
```

This is **not** SAT or UNSAT evidence. The deterministic theorem artifact checks the model structure and hashes; the bounded solver outcome is retained as an explicitly versioned experiment.

---

## Pass 1803 — three-body octet orbit-transfer algebra

Pass 1540 proved that codeword weight for an octet subset `X` is

\[
w(X)=16|X|-2e(X)+4t(X),
\]

where `e(X)` is the number of induced edges in `SRG(45,32,22,24)` and `t(X)` counts the 240 distinguished octet triples arising from W33 edges. The term `t(X)` showed that the ordinary rank-three association scheme is insufficient.

Pass 1803 computes the missing low-rank transfer algebra under `PSp(4,3)`.

### Triple orbits

There are exactly six inner-group orbits on three-subsets:

| orbit size | stabilizer | `(e,t,w)` |
|---:|---:|---:|
| 270 | 96 | `(0,0,48)` |
| 2160 | 12 | `(1,0,46)` |
| 6480 | 4 | `(2,0,44)` |
| 2160 | 12 | `(3,0,42)` |
| 2880 | 9 | `(3,0,42)` |
| 240 | 108 | `(3,1,46)` |

The two ordinary triangle orbits of weight 42 remain distinct despite identical `(e,t,w)`, while the distinguished 240-triple orbit has weight 46.

### Four-subset orbits and transfer matrices

There are exactly twenty inner-group orbits on four-subsets. The verifier computes the complete `6 x 20` upward incidence matrix `U` and `20 x 6` downward incidence matrix `D`. If `n_3` and `n_4` are the corresponding orbit-size vectors, then entrywise

\[
\boxed{
\operatorname{diag}(n_3)U
=
\bigl(\operatorname{diag}(n_4)D\bigr)^{\mathsf T}.
}
\]

This is a literal double-counting certificate, not a numerical spectral fit. The combined orbit/transfer hash is

```text
b046eeac796e13eebb71ef72b12aebb4ddf577591c93a55d9f6938dd36e0339e
```

All six triple orbits and all twenty four-subset orbits are stable under the canonical outer permutation. These matrices are the first exact transfer layer needed for an orbit-based full weight enumerator.

---

## Pass 1804 — optimal ambiguity-declaring decoding through weight three

Use the 45-octet matrix `K` as a parity-check matrix for the binary frame code

\[
C=[240,195,4]_2.
\]

For each syndrome, the decoder chooses an error only when the minimum-weight representative is unique; otherwise it declares ambiguity. This is the optimal zero-miscorrection decision rule at each certified minimum weight.

The exact numbers of uniquely decoded errors are

\[
\boxed{
N_0=1,
\quad N_1=240,
\quad N_2=25440,
\quad N_3=1576000.
}
\]

Therefore its exact success contribution through weight three on an independent BSC is

\[
\boxed{
(1-p)^{240}
+240p(1-p)^{239}
+25440p^2(1-p)^{238}
+1576000p^3(1-p)^{237}.
}
\]

Among all

\[
\binom{240}{3}=2,275,280
\]

weight-three errors:

- `1,576,000` have a unique minimum-weight syndrome representative;
- `697,120` lie in ambiguous minimum-weight buckets;
- `2,160` are shadowed by a weight-one syndrome.

The exact weight-three bucket profile is

| multiplicity | number of syndromes |
|---:|---:|
| 1 | 1,576,000 |
| 2 | 268,560 |
| 3 | 38,880 |
| 4 | 4,360 |
| 5 | 2,592 |
| 6 | 2,160 |
| 9 | 240 |

The 240 multiplicity-nine syndromes are precisely the weight-one-shadowed syndromes. Under `PSp(4,3)`, the weight-three syndrome buckets split into exactly

\[
\boxed{110}
\]

orbits; the certificate records orbit sizes, stabilizers, minimum multiplicities, shadow flags, and whether the canonical outer automorphism fixes or pairs each orbit.

This is an exact minimum-weight result through weight three. It is not a proof of unrestricted maximum-likelihood decoding for arbitrary error weights and is not a threshold statement.

---

## Pass 1805 — canonical full-Weyl extension of the coexact 30

For each canonically bipartitioned octet let

- `S` be signed point incidence;
- `U` be consistently oriented edge incidence;
- `d` be the oriented edge boundary.

The exact identities are

\[
dU^{\mathsf T}=-4S^{\mathsf T},
\]

and, for

\[
V=4U+Sd,
\]

\[
\boxed{dV^{\mathsf T}=0,}
\qquad
\boxed{L_1V^{\mathsf T}=4V^{\mathsf T},}
\qquad
\boxed{\operatorname{rank}_{\mathbb Q}V=30.}
\]

Thus `V` realizes the coexact degree-30 carrier from Pass 1538.

Let

\[
s=\operatorname{diag}(1,-1,1,-1)
\]

be the canonical multiplier-minus-one similitude. The induced operator on the coexact 30 satisfies

\[
s^2=I,
\]

with exact data

\[
\boxed{
\operatorname{tr}(s)=2,
\qquad
\dim E_{+}(s)=16,
\qquad
\dim E_{-}(s)=14,
\qquad
\det(s)=1.
}
\]

On the signed 45-octet permutation carrier the same element fixes seven octets and has signed trace five.

This determines the geometric extension selected by the canonical similitude; tensoring by the outer sign gives the alternative trace `-2` extension. The packet deliberately assigns no ATLAS class or named character until a standard-generator fusion certificate identifies the canonical similitude inside `U4(2):2` or `2.U4(2):2`.

---

## External anchors and evidence boundary

The external sources used only for representation-theoretic orientation are:

1. the RWTH Aachen Modular Atlas decomposition matrix `U4(2) (mod 2)`, which lists simple degrees `1,4,4,6,14,20,20,64`;
2. the ATLAS standard-generator 45-point permutation representations of `U4(2)` and `U4(2):2`;
3. the ATLAS standard-generator 240-point permutation representation of `2.U4(2):2`.

Those sources do not contain the W33-specific Bockstein matrix, outer-Frobenius intertwiner, XOR ranks, orbit-transfer matrices, syndrome census, or coexact trace calculation. Those are repository computations.

All promoted module, rank, orbit, decoding, and outer-extension statements are exact finite computations. The bounded HiGHS run is an experiment and is labeled as such. No global resolution verdict, exhaustive weight enumerator, physical threshold, or continuum interpretation is inferred.
