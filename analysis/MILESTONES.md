# Release milestones — criteria, not momentum

*Releases fire when gates close, not when a round feels productive. Gates may
be overtaken by results; when that happens, replace the gate and say so.*

## v1.0-selection-layer-closed — shipped

The selection layer closed in the negative (chirality no-go, torsor theorem,
attributions corrected); self-verifying claims ledger; failure taxonomy.

## v1.1-cover-law-and-audit — shipped

The cover law proved for all odd q; sections classified (= characters);
nesting tower law; PDS certified; third stream's Pass 399 audited GOOD;
executable batch intake; both papers compile.

## v1.2-integral-tower-and-attribution — shipped

Polhill attribution corrected; the prime-to-characteristic Smith theorem proved;
characteristic and prime-to-characteristic layers welded through q=27; the
finite-field/residue-ring atlas and synthetic torsion detector released.

## v1.3-conductor-geometry-and-formal-kernel — shipped

Passes 440–444 close all five mathematical/software gates opened after v1.2.

1. **Finite-chain-ring conductor tower — CLOSED by Pass 440.** For every odd
   unramified finite chain ring of length n and residue order q, exact central
   character conductor j gives the full rational spectrum and every
   prime-to-characteristic Smith layer. Length one recovers the field theorem;
   length two recovers the Z/p² atlas; length three is explicitly certified.
2. **Independent formal kernel — CLOSED at the algebraic kernel by Pass 441.**
   Lean/mathlib proves the explicit unimodular 2×2 Smith reduction and the
   conductor/multiplicity polynomial identities without `sorry` or custom
   axioms. The representation-theoretic central Fourier decomposition remains a
   named formalization boundary rather than being silently assumed complete.
3. **Blind optical preregistration — CLOSED as a synthetic dry run by Pass 442.**
   Labels are hash-committed before prediction; the 16×16 transfer matrix,
   affine-fit classifier, abstention threshold, and primary endpoint are frozen.
   The sealed 192-sample holdout is classified 192/192 with all commitments
   verified. A measured-hardware run remains an experimental gate, not a
   mathematical one.
4. **Section-sensitive torsion — CLOSED at q=3 by Pass 443.** The 81
   inverse-closed sections split into exactly two Aut(H₃)-orbits, detected by a
   two-component curl. The 9 flat sections and 72 curved sections have different
   characteristic polynomials, spanning-tree prime supports, and critical
   groups; no hidden cospectral/Smith-distinct third class exists at q=3.
5. **Hjelmslev conductor geometry — CLOSED at length two by Pass 444.** Explicit
   AHG(2,Z/9) and AHG(2,Z/25) incidence objects verify the neighbor map
   point-by-point. The Gram law `BB^T=q²I+(q-1)N+J` identifies q³ residue-plane
   modes with conductor one and q² within-neighborhood modes with primitive
   conductor.

The permanent Passes 440–444 workflow regenerates all five certificates, runs
focused regressions, and compiles the Lean package in a separate pinned job.

## v1.4 — OPEN. Gates

1. Determine the characteristic-primary Smith layers for finite chain-ring
   Heisenberg graphs at nilpotent length n≥2.
2. Formalize the central Fourier decomposition and primitive rank factorization
   in Lean, upgrading the Pass 441 algebraic kernel into an end-to-end proof.
3. Replace the synthetic Pass 442 transfer kernel by a measured optical transfer
   matrix and execute the preregistered blind hardware holdout unchanged.
4. ~~Lift the section-curl/orbit/Smith classification from q=3 to q=5.~~
   **RESOLVED-NEGATIVE by Passes 446-447**: exact affine Burnside gives
   20,592 Aut-orbits (validated at q=3 -> 2); the action is nearly free
   (counting floor 20,345), so orbit classification is vacuous at q>=5 -- AND
   the spectral census (400 samples -> 396 distinct spectra) shows invariant
   VALUES are near-injective too. The q=3 flat/curved dichotomy is a
   small-numbers accident in both senses. Replacement gate: explain the
   sampled field atlas -- every quadratically-paired irrational eigenvalue
   across 396 sampled q=5 spectra lies in Q(sqrt5), the SAME field as the q=3
   curved class. Why sqrt5, uniformly, at two rungs?
5. Extend the Hjelmslev conductor dictionary to length n≥3 and compare its
   filtration with affine-building and Bruhat–Tits residue layers.

## Deferred beyond v1.4

- m=6 Coxeter–Todd rung of the QR tower (GAP; handoff `data/m6_handoff_k12.json`).
- exp-3/exp-9 versus ordinary/twisted Frobenius–Schur correspondence.
  (The PDS half closed in Pass 445: (27,10,1,5) is a PDS in the exponent-9
  extraspecial group too — a q=3-only phenomenon, no exp-25 analogue at q=5
  within H:SL(2,5). The character-theoretic half remains open.)
- measured-device calibration and physical error bars for every photonic claim.
