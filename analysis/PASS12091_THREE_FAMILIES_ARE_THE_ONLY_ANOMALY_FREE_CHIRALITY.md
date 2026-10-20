# Pass 12091: three families are the only anomaly-free chirality

Claude track. Builds on 12087 and 12090.

## Setup

Take a flag-built Standard-Model grading and add an order-3 torus shift that keeps every SM gauge root. Per complex
plane, the net number of left-handed copies of each field F is
N(F) = (weights of F with phase 1) − (weights of its conjugate with phase 1), divided by dim F.

## Results

Checked on three independent SM gradings, over all 6561 classes:

- There are 242 gauge-compatible non-trivial shifts.
- **The only non-zero anomaly-free patterns are N = (3,3,3,3,3) and (−3,−3,−3,−3,−3)**, for Q, u^c, d^c, L, e^c. Each
  occurs for exactly 10 shifts, all with fixed algebra **e6 + a2**.
- Every other chiral shift is anomalous, e.g. (2,1,5,−3,−3) or (−2,2,1,0,0).
- The family a2 is generally not a W(3,3) event fibre: 0, 0 and 2 of the 20 shifts in the three gradings.

## Reading

With the Standard-Model grading kept, an order-3 twist yields a consistent chiral spectrum only with **exactly three
families**: the SU(3) triplet index of E8 ⊃ E6 × SU(3).

## Prior art

The E6 × SU(3) three-family mechanism is classical. New here is the exclusivity inside the clock/split grading: no
other non-zero anomaly-free family number occurs.

## Scope

Per-plane untwisted counting on the E8 adjoint. Z2 projections and twisted sectors are not included.

## Correction during the pass

An exploratory check said "never an event fibre" for one grading. A third grading has 2 of 20, so the claim is now the
measured counts.

Producer: `analysis/w33_pass12091_three_families_are_the_only_anomaly_free_chirality.py`.
