# Passes 474–478 — execution ledger

This release was renumbered after a parallel Pass 473 landed during execution. All work below was executed and validated locally against the then-current repository frontier.

## Pass 474 — original-coordinate q=5 intertwiner

The faithful 25-dimensional Weyl sheets for collision graph A at central character `t=1` and graph B at `t=2` are exactly similar over `Q(zeta_5)`. Exact Krylov bases produce `X = U_B U_A^{-1}` and verify `B X = X A` and the inverse relation. The canonical lift has 500 nonintegral entries and nonunit determinant norm. Distinct gauge-invariant triangle-gain histograms rule out every permutation plus diagonal fifth-root phase-gauge implementation. This does not exclude every possible integral `GL_25(Z[zeta_5])` lift.

## Pass 475 — concrete GR(9,2) Weyl geometry

For `R = GR(9,2) = Z/9Z[u]/(u^2+1)`, the primitive 81-dimensional Weyl block has spectrum

`80^41 + (-82)^40`,

while the depth-one block has

`728^5 + (-730)^4 + (-1)^72`.

The primitive alternating radical has size 1. The depth-one radical has size 81 and equals `3R × 3R`, the kernel of reduction `R^2 -> F_9^2`. The associated full central-sheet Laplacian determinant valuations are 26244 and 52326.

## Pass 476 — symbolic conductor/Smith valuation budget

For `R = GR(p^n,f)`, set `s=p^f`, `Q=s^n`, `a=s^r`, and `d=Q/a`. The valuation-r character stratum has size `d-d/s`. Its central-sheet Laplacian valuation is `f*n*Q^2` for `r=0`, and

`d^2*f*(n+r) + (Q^2-d^2)*2*f*n`

for `r>0`. Adding the trivial sheet and subtracting `v_p(|H(R)|)=3fn` gives the matrix-tree valuation. Exact controls reproduce 31 for `F_3` and 1916 for `Z/9`. New predictions are 145 for `F_5`, 387 for `F_7`, 2360644 for `GR(9,2)`, 77727 for `Z/27`, and 37390 for `Z/25`. This determines the weighted Smith-exponent budget, not every individual multiplicity.

## Pass 477 — uniform finite-field Lean cardinality

`formal/W33/Pass477UniformProjectiveCardinality.lean` proves over an arbitrary finite field:

- bulk cardinality `q^3`;
- projective-line cardinality `q+1`;
- rim/projective-plane cardinality `q^2+q+1`;
- projective-three-space cardinality `(q+1)(q^2+1)`;
- the bulk decomposition into `q^2` fibers of size `q`;
- the uniform shell-total identity inherited from Pass 465.

The module contains no `sorry` or axioms and is integrated into `formal/W33.lean`. The full uniform incidence proofs of L1–L4 remain open.

## Pass 478 — independent optical acquisition gate

The operator-side generator produces a balanced private blind plan with 48 field and 48 ring samples, randomized sample and phase order, public SHA-256 commitments, and a reveal whose prediction hash remains blank until predictions are frozen. A deterministic test-only run validated the packet.

Physical status: `BLOCKED_PENDING_INDEPENDENT_OPERATOR`.

No measured transfer matrix, sealed optical holdout, prediction file, reveal, or laboratory score is claimed.

## Validation

The complete local package passed 56/56 certificate checks and 5/5 focused regression tests. The two directly browsable computational witnesses, the uniform Lean module, the private operator generator, reservations, and this ledger are committed with this release.
