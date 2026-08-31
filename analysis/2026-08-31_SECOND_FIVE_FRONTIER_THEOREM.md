# Second five circuit frontier theorem — 31 August 2026

This note closes the five follow-up questions opened by the first all-five circuit frontier audit.  Every claim below is backed by an executable exact certificate and replayed successfully in GitHub Actions run `33349823610` on commit `1c38a83d2f832648715201534aefb03c997b9fc1`.

## 1. The common colour 60-space is not the symmetric 60-sector

Let

- `M` be the 216 by 540 maximal-overlap incidence,
- `M+` and `M-` its two PSp(4,3) cross-orbital colours,
- `W = row(M+) intersect row(M-)`.

The first audit proved `dim W = 60`.  The symmetric bicolour algebra also has a 60-dimensional joint eigenspace, so equality was a natural possibility.  It is false.

The exact transported-sector audit gives, in sector order

`15, 15, 81, 20, 60, 24, 1`,

pairwise diagonal intersections

`0, 0, 0, 20, 0, 24, 1`,

with no nonzero off-diagonal pairwise intersections.  In particular, the distinguished symmetric 60-sector has intersection zero with the opposite colour row space in both directions.

The Wedderburn calculation below shows that the only repeated simple constituent on the 216-side is a 15-dimensional irrep occurring twice.  Therefore the remaining 15 dimensions of `W`, after the full 1-, 20-, and 24-dimensional constituents are removed, must be one diagonal copy in that doubled 15-isotypic component.  Thus, intrinsically,

`W ~= 1 + 15 + 20 + 24`.

The final 15 is a graph line in the two-dimensional multiplicity space of the 15-irrep; it is not either one of the two symmetric 15-sector summands by itself.

## 2. Exact Wedderburn algebra on the 216 five-circuits

The PSp(4,3) orbital algebra on the 216 five-circuits has dimension 10 and center dimension 7.  Exact multiplication-table and center calculations give complex Wedderburn block sizes

`2,1,1,1,1,1,1`.

Hence

`End_G(C^216) ~= M_2(C) + C^6`.

Equivalently the 216-point permutation representation decomposes over C as

`1 + 2*15 + 20 + 24 + 81 + 30 + 30bar`.

Here the labels denote intrinsic complex dimensions, not an imposed external character-table naming convention.

The two symmetric 15-dimensional sectors, at separator eigenvalues -58 and -22, are the two noncentral rank-one projections inside the unique M2 block.  Their sum is the central projector onto the 30-dimensional doubled 15-isotypic component.

### The symmetric 60-sector is an Eisenstein 30 + 30bar pair

The 60-dimensional symmetric sector at separator eigenvalue 14 is itself central over Q but its center restriction has degree two.  A separating exact central element has minimal polynomial

`x^2 - 578 x + 88813`.

Its discriminant is

`-21168 = -3 * 84^2`,

so the splitting field is exactly

`Q(sqrt(-3))`.

The roots are

`289 +/- 42 sqrt(-3)`.

Therefore the 60-sector is not complex-irreducible: it splits as two Galois-conjugate 30-dimensional irreducibles,

`60_Q -> 30 + 30bar`

over the Eisenstein field.

This is an exact algebraic occurrence of the same quadratic field already forced by the central-C3/qutrit constructions.  No physical identification follows from the common field alone.

## 3. Exact 540-side decomposition and the 324-dimensional kernel

The PSp(4,3) orbital algebra on the 540 six-circuits has dimension 32 and center dimension 9.  Its complex Wedderburn block sizes are

`3,2,2,2,2,2,1,1,1`.

Transporting a separating right-central element through the equivariant embedding `M^T` and subtracting left multiplicities gives the exact right permutation module:

`C^540 ~= 1 + 3*15 + 2*20 + 2*24 + 2*30 + 2*30bar + 60 + 64 + 2*81`.

Since `M` has rank 216, its right kernel has dimension 324.  The exact factorwise subtraction gives

`ker(M)_C ~= 15 + 20 + 24 + 30 + 30bar + 60 + 64 + 81`.

This decomposition is multiplicity-free over C.  Its character norm is therefore

`<chi_ker,chi_ker> = 8`.

The conjugate 30-pair in the kernel is again defined over the Eisenstein quadratic field.  For the chosen separating right-central element its quadratic factor is

`x^2 - 136 x + 5596`,

with discriminant

`-3888 = -3 * 36^2`

and roots

`68 +/- 18 sqrt(-3)`.

So both the left symmetric 60-sector and the right/kernel conjugate 30-pair are intrinsically controlled by `Q(sqrt(-3))`.

## 4. Complete integral Smith forms of M, M+, and M-

Previous modular certificates proved that every nonunit Smith invariant of the three rectangular incidence matrices is a power of 2.  Exact local Smith elimination over `Z / 2^24 Z` now recovers every 2-adic exponent below the truncation ceiling, so the integral nonzero Smith forms are complete.

For the full incidence,

`SNF_nonzero(M) = 1^156 2^44 4^15 8`.

Thus the finite index of the row lattice in its saturation has 2-adic exponent

`44 + 2*15 + 3 = 77`.

For each colour,

`SNF_nonzero(M+) = SNF_nonzero(M-) = 1^201 2^14 4`,

with 2-adic index exponent 16.

Each 216 by 540 matrix also has the expected 324-dimensional rational right kernel; the displayed Smith lists contain only the 216 nonzero diagonal invariants.

## 5. Exact no-go between the two central-omega sixes

There are now two independently constructed rational 12-dimensional nontrivial central-C3 carriers:

- the `6_omega + 6_omega^2` part of the 24-sector;
- the `6_omega + 6_omega^2` part of dark20.

Both omega sixes are irreducible K-modules: each exact character norm equals 1.  However their exact K-character cross inner product is

`<chi_omega^(20), chi_omega^(24)>_K = 0`.

Therefore they are nonisomorphic irreducible K-modules.

As a constructive check, the K action on the 216 circuit states has 111 orbitals.  Projecting every K-orbital commutant map between the two rational nontrivial carriers gives rank zero; the best projected rank is exactly 0.  Consequently there is no K-equivariant rational intertwiner between them.

This is a useful no-go: dimension six plus the same nontrivial central C3 charge is not enough to identify the two qutrit-like carriers.

## Combined structural picture

The five follow-up questions close into one consistent module picture:

- the 216-side commutant is `M2(C) + C^6`;
- the symmetric 60-sector is an Eisenstein `30 + 30bar`, not the common colour 60-space;
- the common colour 60-space is `1 + 15 + 20 + 24`, with the 15 sitting diagonally in the unique doubled 15-isotypic component;
- the 540-side module adds one new 60-irrep and one new 64-irrep and raises the multiplicities of every shared nontrivial constituent;
- the 324-kernel is the multiplicity-free complement `15+20+24+30+30bar+60+64+81`;
- the integral incidence lattices have complete 2-primary Smith forms;
- and the two central-omega sixes are rigorously distinct K-representation species.

The repeated appearance of `Q(sqrt(-3))` is exact and now occurs at three different levels: the central C3 deck carrier, the left 30+30bar split, and the right/kernel 30+30bar split.  This is strong evidence for a common Eisenstein arithmetic substrate, while the six-sector no-go simultaneously shows that the substrate does not collapse distinct representation species into one.

## Executable certificates

- `analysis/w33_20260831_common_colour_60_sector_test.py`
- `analysis/w33_20260831_c5_wedderburn_kernel.py`
- `analysis/w33_20260831_incidence_2adic_snf.py`
- `analysis/w33_20260831_eisenstein_dark20_intertwiner.py`
- `data/PART_W33_20260831_SECOND_FIVE_FRONTIER_KEY_RESULTS.json`
- `analysis/w33_20260831_second5_frontier_freeze.py`

The heavy exact replay is GitHub Actions run `33349823610`, conclusion `success`.
