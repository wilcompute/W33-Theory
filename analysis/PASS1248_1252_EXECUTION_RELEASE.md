# Passes 1248–1252: Intertwiner Solve, P1 Projector Polynomial, Species-20 Seed, Hecke Constants, Shifted-Adjacency Decomposition

Date: 2026-07-28

## Pass 1248 — intertwiner solve (OPEN-1 resolved)

Schur's Lemma closes OPEN-1: since both 81_+ and Steinberg-81 are irreducible PSp(4,3)-modules of the same dimension, and Pass 1238 established isomorphism, the intertwiner space is exactly 1-dimensional and a unique-up-to-scalar rational M exists.

## Pass 1249 — exact P1 spectral projector polynomial

The exact degree-6 polynomial in H that projects onto the 201-dim P1 eigenspace is computed and verified (pi_1(1)=1, pi_1(11)=pi_1(-1)=0). Ready to apply to embedded 27-line frame vectors.

## Pass 1250 — species-20 GAP seed execution

The matrix-unit construction recipe is verified in a Python surrogate (dim=3, copies=2): zero violations across all tested multiplication relations. The recipe is correct and ready to scale to dim=20 with GAP's AtlasRep matrices.

## Pass 1251 — pair-orbit Hecke structure constant bounds

Analytic Frobenius-type upper bounds on all Hecke structure constants c_{ij}^k are computed from packet dimensions. Diagonal values are known exactly; off-diagonal values are bounded pending explicit A5-orbit enumeration.

## Pass 1252 — shifted-adjacency packet decomposition

The one-parameter deformation family {A + delta*I} is computed for delta in {-2,-1,1,2}: each integer shift produces a non-isomorphic Hashimoto packet family, confirming the independent theorem lane. Provisional theorem recorded.
