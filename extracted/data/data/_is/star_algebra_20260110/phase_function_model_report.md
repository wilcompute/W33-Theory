# Tomotope → Projective Clock: phase-function model (2026-01-10)

## What was computed
From the CSV artifacts in this chat, we rebuilt the 15 matched tomotope triangles as 15 W(3,3) rainbow lines (quartets of projective classes).

Each projective class is of the form `sec{s}_m{m}` with sector s∈{0,1,2,3} and m∈Z3.

## Two rigid invariants (empirical, exact on the 15 lines)

1) Rainbow constraint: every quartet contains exactly one class from each sector.

2) Phase-sum constraint: for every quartet L,
   Σ m(L) ≡ 1 (mod 3).
   (Verified on all 15 lines.)

This implies the completion rule:
If a triple omits sector s*, then the missing phase is forced by

   m_{s*} ≡ 1 − Σ_{s≠s*} m_s  (mod 3).

## Why the “sec0_m2 always completes missing sector-0” happens
Among the 6 triples that omit sector 0, the known phase sum over sectors 1,2,3 is constant:

   Σ(m1,m2,m3) ≡ 2 (mod 3),

so the forced completion is

   m0 ≡ 1−2 ≡ 2.

Hence all 6 missing-sector-0 completions land on sec0_m2.

## Phase-function representation (minimal algebraic model)
Identify sectors with bits u∈GF(2)^2 via:

   sec0=(0,0), sec1=(1,0), sec2=(0,1), sec3=(1,1).

Any assignment of m-values to the four sectors corresponds uniquely to a polynomial

   f(u1,u2) = a0 + a1 u1 + a2 u2 + a3 u1 u2   (coeffs in Z3),

since (u1,u2) takes exactly 4 values.

For each realized rainbow line, we solved for the unique coefficient vector (a0,a1,a2,a3)∈Z3^4
whose evaluations produce its m-tuple (m0,m1,m2,m3).

### The rainbow-line hyperplane in coefficient space
The phase-sum constraint Σ m ≡ 1 becomes the single affine constraint on coefficients:

   a0 − a1 − a2 + a3 ≡ 1 (mod 3).

So all rainbow lines live on an affine hyperplane of size 3^3=27 inside Z3^4.

### Tomotope selection rule (new, concrete statement)
The tomotope contributes 15 of those 27 possible phase-functions.
The remaining 12 hyperplane elements are not realized by tomotope triangles.

Files written:
- phase_function_hyperplane_all27.csv (all 27, with realized flag)
- phase_function_hyperplane_missing12.csv (the missing 12)
- tomotope_15_rainbow_lines_phase_function_model.csv (triangle → quartet → m_tuple → coeffs)

## “Star” around sec0_m2
Counting line membership in the 15-line set:

- sec0_m2 appears in 9/15 lines (distinguished),
- sec0_m0 and sec0_m1 appear in 3/15 lines each,
- all non-sector-0 classes appear in 5/15 lines each.

This makes sec0_m2 a natural basepoint/identity candidate for building a local algebra from the tomotope-induced subconfiguration.

File:
- lines_containing_sec0_m2_star.csv
