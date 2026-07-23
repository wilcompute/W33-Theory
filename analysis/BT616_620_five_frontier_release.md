# Passes 616–620: arithmetic factors, H2 representation, Hecke compression, optimal selector, and Poisson minimax release

This release executes the five non-sequential directions following Pass 615. Every result is paired with a deterministic script, immutable JSON certificate, and a focused regression.

## Pass 616 — arithmetic core factorization and Galois closure

The square-free degree-256 characteristic core from Pass 611 factors over `Q` into 17 explicit irreducible factors with degree multiset

`2, 4, 4, 4, 4, 4, 5, 10, 10, 13, 13, 13, 19, 32, 32, 43, 44`.

Every factor has the full symmetric Galois group in its degree:

`S2, S4^5, S5, S10^2, S13^3, S19, S32^2, S43, S44`.

Irreducibility is certified by a prime at which each polynomial remains irreducible. Frobenius cycle types, exact block-system exclusions, Jordan's theorem, and nonsquare discriminants prove the Galois statements. The product coefficient hash reproduces the Pass-611 core hash exactly.

## Pass 617 — the S8-module on H2

The simplicial Lefschetz trace formula was evaluated on all 22 conjugacy classes of `S8`. Murnaghan–Nakayama inversion gives

`H2(Q) = S^(5,1,1,1) + S^(4,2,1,1)`.

The decomposition is multiplicity free, with dimensions 35 and 90. These dimensions coincide with the project's `PG(3,2)` line count and center-quad count, but no objectwise identification or integral lattice splitting is asserted.

## Pass 618 — Hecke compression of the 10,080-sector groupoid

For `H=< (0 1),(6 7)> ≅ C2 x C2`, the double-coset space has 2,892 elements, with size histogram `4^48, 8^672, 16^2172`. The complex Hecke algebra has dimension 2,892 and center dimension 20.

The coset permutation representation contains 20 Specht isotypes. A generic equivariant operator with a 280-dimensional fibre reduces from dimension 2,822,400 to multiplicity-space problems totaling 54,880 dimensions; the largest block has dimension 6,720.

## Pass 619 — optimal eight-rail selector

An exhaustive `S4`-equivariant search enumerates all 30 subgroups, 11 subgroup conjugacy classes, all transitive coordinate orbits, and every stabilizer-invariant base subset. A capped-distance dynamic program proves that no binary equivariant code of length at most seven can encode the twelve oriented tetrahedral edges with minimum distance four.

The optimum is a constant-weight-four `(8,12,4)` code on the eight cube vertices `S4/C3`. It detects every corruption of weight at most three and corrects every single-bit fault, reducing the Pass-614 design from 20 physical channels to eight.

## Pass 620 — adversarial paired-Poisson minimax controller

The controller uses paired Poisson interferometer outputs, so conditional binomial inference cancels common loss. The adversarial family includes common loss, mode-dependent loss, leakage, detector imbalance, trace-three-only drift, and a combined attack.

A finite minimax search selects sentinel probability `0.55` and a 64-photon third-trace audit. The maximum exposure is 464 photons. In the final deterministic simulation it retains nominal worst-class accuracy `0.989`, isolated leakage/imbalance safe-rate floors above `0.93`, and detects trace-three-only drift with probability above `0.75` within five classifications.

## Validation

The five witnesses pass `11 + 9 + 10 + 10 + 12 = 52` internal checks, regenerate byte-identical certificates under `--check`, compile, and pass the focused regression.
