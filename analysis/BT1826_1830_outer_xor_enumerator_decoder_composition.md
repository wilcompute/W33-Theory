# Passes 1826–1830 — outer-class fusion, exact XOR proof, weight frontier, weight-four decoding, and nonlinear composition

## Executive result

This collision-safe packet executes the five continuations opened after Passes 1801–1805 while preserving the parallel Passes 1816–1825 results. The aggregate frozen certificate has SHA-256

```text
660b1f730a73348f24c241967af6499ca5813b7f2c55b6b5955224ce73cc4d12
```

The exact conclusions are:

1. the canonical multiplier-minus-one similitude is the ATLAS outer involution class `2D`, with centralizer 96 and class size 540; its traces on the four chiral blocks of degrees 15, 24, 30, and 81 are respectively `3,4,2,3`;
2. the complete symmetry-fixed XOR relaxation is exactly satisfiable, with 4,860 variables, rank 2,349, and affine dimension 2,511; the canonical proof witness is frozen, but it violates the nonlinear integer cardinalities and is not a resolution;
3. the exact message-weight layers 0 through 10 and their complements 35 through 45 are enumerated, while Burnside analysis proves that the full subset action has 1,358,719,936 group orbits and 158,938,060 middle-layer orbits, making symmetry-orbit traversal alone non-closing;
4. the exact weight-four syndrome geometry contains 134,810,340 errors, of which 63,416,280 are uniquely minimum-weight decoded, giving the next exact BSC coefficient;
5. the complete 720-signature nonlinear cover quotient from Passes 1821–1825 is composed with the XOR certificate: the XOR system is consistent, but the certified four-packing has no nonlinear five-signature completion. Linear parity satisfiability is therefore strictly weaker than exact-cover realizability for that packing.

The full `2^45` weight enumerator and the existence of an unrelated nine-cover resolution remain open.

## Pass 1826 — standard-class fusion and four-bit chirality

The verifier reconstructs the full projective similitude action of order

\[
|PSp(4,3):2|=51840.
\]

For the canonical multiplier-minus-one involution `s`, it computes

\[
|C_G(s)|=96,\qquad |s^G|=540,
\]

and the fixed-object profile

\[
8\text{ points},\quad6\text{ lines},\quad16\text{ frames},\quad7\text{ octets}.
\]

The ATLAS table for `U4(2):2` has outer involutions `2C`, with centralizer 1440, and `2D`, with centralizer 96. Hence

\[
\boxed{s\in2D.}
\]

Its four chiral blocks have the exact profile

| degree | trace | `+1` | `-1` | determinant |
|---:|---:|---:|---:|---:|
| 15 | 3 | 9 | 6 | +1 |
| 24 | 4 | 14 | 10 | +1 |
| 30 | 2 | 16 | 14 | +1 |
| 81 | 3 | 42 | 39 | -1 |

Thus four-bit chirality is a statement about four independent class functions, while one geometric outer element selects the single `2D` column

\[
\boxed{(3,4,2,3).}
\]

The coexact trace `+2` is the degree-30 coordinate, not a universal scalar handedness bit.

## Pass 1827 — proof-producing XOR solution

The complete symmetry-fixed parity system has

\[
4860\text{ variables},\qquad3114\text{ equations},
\]

and exact `GF(2)` row reduction gives

\[
\boxed{\operatorname{rank}=2349,\qquad\operatorname{nullity}=2511.}
\]

The canonical free-zero solution has Hamming weight 1,594 and raw SHA-256

```text
ba16152cf68eee2221f3316646f0427648e9fe3174e1c33cb0ee1e9a3bfb4e3d
```

with pivot and RREF hashes

```text
33c7517b268352d1fd377a2474ceef35c4a63a43241e0d221d871d0a844c3565
2625f30ef4dfc3881640fff0e9cdcb7a51b4f47f4c33f3d6decdd158367a77d7
```

Its integer frame and edge/color sums include `1,3,5,7,9`, and no octet/color sum equals the required eight. Therefore

\[
\boxed{\text{XOR-SAT does not imply resolution-SAT}.}
\]

This is a complete verdict for the linear parity relaxation only, not a SAT or UNSAT verdict for the nonlinear assignment problem.

## Pass 1828 — exact weight-enumerator frontier

Burnside's lemma for the exact `PSp(4,3)` action on the 45 generators gives

\[
\boxed{1,358,719,936}
\]

subset orbits, including

\[
\boxed{158,938,060}
\]

orbits in each middle layer 22 and 23. Hence direct orbit traversal cannot close the enumerator.

The exact message layers

\[
0\le k\le10
\]

and, by complementation,

\[
35\le k\le45
\]

are fully enumerated. They cover 8,693,628,552 messages; the unresolved middle contains 35,175,678,460,280. Every layer histogram and partial global coefficient is frozen in the certificate. This is a frontier theorem, not a false claim of a complete enumerator.

## Pass 1829 — exact weight-four syndrome geometry

For the binary frame code

\[
[240,195,4]_2,
\]

the verifier enumerates all

\[
\binom{240}{4}=134,810,340
\]

weight-four errors and finds 91,007,752 distinct syndromes. Exactly

\[
\boxed{63,416,280}
\]

errors have unique minimum-weight syndrome representatives.

The lower-weight shadows are

\[
540\text{ by weight }0,\quad0\text{ by weight }1,\quad592,200\text{ by weight }2,\quad0\text{ by weight }3.
\]

The 540 zero-syndrome errors are the canonical weight-four frame codewords. The exact BSC success polynomial through weight four is

\[
\begin{aligned}
P_{\le4}(p)={}&(1-p)^{240}+240p(1-p)^{239}+25440p^2(1-p)^{238}\\
&+1576000p^3(1-p)^{237}+\boxed{63416280p^4(1-p)^{236}}.
\end{aligned}
\]

No decoding threshold or weight-five classification is claimed.

## Pass 1830 — nonlinear signature gate over the XOR affine space

The parallel Passes 1821–1825 release owns the complete exact-cover census and the nonlinear 45-coordinate signature quotient. It proves that the global cover space has 720 realizable signatures in four orbits and that the selected four-packing has no completion by five such signatures.

Pass 1830 composes that theorem with Pass 1827 rather than duplicating it:

\[
\boxed{\text{linear XOR system: consistent, affine dimension }2511,}
\]

but

\[
\boxed{\text{selected four-packing: no realizable nonlinear five-signature completion}.}
\]

The nonlinear gate checks 632 individually fitting signatures, 119,642 admissible pair multisets, 117,548 unique pair sums, and 305,488 admissible triple sums, with no complementary pair/triple split. Thus

\[
\boxed{\text{XOR-SAT is strictly weaker than exact-cover realizability}.}
\]

A resolution solver should apply the 720-signature selection layer before opening the 4,860 frame/color variables. Boundary: this rejects the certified four-packing, not every possible nine-cover resolution.
