# Five active frontier closure — 31 August 2026

This note reconciles the five active W33/Holotrade fronts against the current master branches. It separates exact finite statements, dedicated CI evidence, and still-open engineering boundaries.

## 1. Compact W33 recovery RTL

Holotrade's source/geometry certificate proves the exact transformation from the legacy labelled-pair search to the adjacency-indexed compact chooser: the candidate set is the 480 directed W33 edges; the line equations and point-line masks match the canonical substrate; `(F+delta,F+s1,-p,-q)` and `(delta,s1,-p,-q)` have identical candidate order for common `F`; and the sequential state block is identical after normalization.

The earlier whole-module Yosys miter did **not** produce a counterexample. Its dedicated step was cancelled at the 20-minute workflow limit. To avoid turning a timeout into a false no-go, Holotrade now also carries a factored bit-vector proof (`52c5883`, `69b1acd`, `b958920`): the small Yosys SAT miter proving score arithmetic and tie-break equivalence completed successfully, as did the exact source/geometry transformation. At the time this note was written, compact LUT4 synthesis in that factored workflow was still executing, so no new LUT4 count is claimed here. The monolithic whole-module miter remains a stronger optional backstop, not a completed proof.

## 2. Symmetry-breaking zero-mode threshold

The tested equivariant-coupling chain is exact:

| symmetry | exact maximum rank | minimum zero modes |
|---|---:|---:|
| `PSp(4,3)` | 25 | 35 |
| `S5` | 30 | 25 |
| `A5` | 34 | 17 |
| `S4` | 36 | 13 |
| `A4` | 40 | 5 |

Thus the first full rectangular rank in the displayed chain is `A4`. This is finite representation theory: it says which couplings symmetry permits, not which perturbations are local or dynamically generated.

## 3. Nonsplit central C3 cover and the rank-20 dark map

The 216 circuit states form a nonsplit three-sheeted central `C3` cover of 72 fibres. The exact rank-20 circuit-to-dark-sector map decomposes canonically into an 8-dimensional deck-fixed/fibre-sum image and a 12-dimensional sheet-resolving fibre-difference image. The full map therefore does not descend to the 72-state quotient: 12 of the 20 dark directions require the sheet coordinate. This is an exact finite representation-theoretic statement, not an identification of the 216 states with calibrated physical Clifford gates.

## 4. Five length-14 Koopman chains

Holotrade's repaired depth-14 replay finds six maximum-depth leaves, all certified optimal near-ovoids with the standard three missed / three doubled punctured-pencil defect geometry. Their first images are all distinct, but exactly one pair coalesces later. Independently,

`|Im T^13| = 2891`, `|Im T^14| = 2886`, and `|Im T^15| = 2886`,

so the terminal image-rank drop is exactly five. Hence there are exactly five zero-eigenvalue Jordan blocks of maximal size 14. The delayed two-to-one merge explains the six-leaf/five-chain discrepancy at state level. The dedicated depth-14 workflow completed successfully.

## 5. q=3/2 OAM radial recentering

The earlier p=0 firewall showed the algebraic benefit and optical cost of `q=3/2`: `Delta ell = +/-3` is invisible modulo three, but a p=0-only receiver captures only 0.5460971605 on average versus 0.8181230869 for `q=1/2` in the declared same-waist phase-only model.

The new full-LG audit (`8fdd4de`, `8e523ff`, `ba768d7`) resolves that apparent loss into the complete target-|ell| radial basis. The exact recurrence is

`P0 = Gamma((m+n)/2+1)^2 / (Gamma(m+1) Gamma(n+1))`,

`P[p+1]/P[p] = (p+(n-m)/2)^2 / ((p+1)(p+n+1))`.

Consequently the ideal full coherent radial superposition is unitary under inverse phase recentering: the p=0 deficit is radial-mode redistribution rather than intrinsic absorption in this model. The engineering cost is the long tail. For the hardest `q=3/2` channel, `ell=0 -> |ell|=3`, one needs radial modes through `p=222` for 99% capture, `p=2247` for 99.9%, and `p=22497` for 99.99%. Averaged over the six centered-qutrit/helicity transitions, truncation at `p<=24` captures 0.9691316725 for `q=3/2` and 0.9965225260 for `q=1/2`. The dedicated multimode workflow completed successfully.

This is still an ideal same-waist analytic model. Finite aperture, propagation/Gouy phase, q-plate retardance profile, aberration, radial sorter/corrector loss, detector coupling, and measured insertion loss remain outside the certificate.

## Boundary

No finite group, code, Koopman, or ideal-mode calculation in this packet is promoted to a claim about a physical Theory of Everything without an explicit physical map and calibrated evidence.
