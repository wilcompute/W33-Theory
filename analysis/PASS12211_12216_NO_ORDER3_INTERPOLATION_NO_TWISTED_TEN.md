# Passes 12211–12216: no order-3 interpolation, no twisted 10, the string material consolidated

Claude track. Producer: `analysis/w33_pass12211_to_12216_no_order3_interpolation_no_twisted_ten.py`. Drivers:

- `analysis/search_drivers_12211/` (`z3ss.py`, `twisted10.py`, `twisted10_draws.py`)
- `analysis/search_drivers_12213/` (`triplets.py`)

## 12211: no order-3 Scherk–Schwarz on T6/Z3

An interpolation needs every SUSY-breaking element θ^b θ'^a to act freely. I checked every order-3 rotation v' and every
spinor lift: there are 72 free choices, and in all of them the θ-invariant gravitino gets the phase ±1, never a cube root.

- **Phase +1:** SUSY is preserved.
- **Phase −1:** θ'³ is (−1)^F times a lattice translation, a non-free fermion parity. That is the ordinary non-SUSY
  orbifold, not an interpolation.

Control: without the freeness requirement, cube-root phases occur 114 times.

**T6/Z3 admits no Scherk–Schwarz interpolation of any order.** Order 2 is ruled out by 12177 (27 fixed points); order 3
is ruled out here.

## 12212: no twisted 10 on the mass shell

This is a lattice computation, a necessary condition checked before any projection phase.

- **SU(5)** is the invariant A4.
- **The cosets** are all 27 fixed-point shifts and their Witten partners.
- **The search** is for vectors of norm 4/3 whose SU(5) projection has norm 6/5 (10-type weights).

There are **0 such vectors in 1616 configurations**: the 163 saved models, plus 300 and 1153 fresh draws on the second and
third torus. Control: 100 untwisted 10-type roots in every configuration.

## 12213: placement

The parity theorem already excludes N_even = 2 together with a symmetric direction (all 10 such parents lack one). The
only empirical case left is N_even = 3. It occurs in one parent, SM_2751, which is the only one with an untwisted
family-triplet quark multiplet. (SM_923 has a family doublet and N_even = 2.)

## 12214: cross-track note

See `analysis/CROSS_TRACK_NOTE_12214_NATIVE_NARAIN_AND_INTERPOLATION.md`. The question is put to the owning track: does
any dynamics break the native C3×C3?

## 12215: paper

Section 7's string material from 12174–12212 is consolidated into one subsection, "The string's fermion parity, and why
interpolation fails". It has Theorem 7.5 (the real form decides the string) and Theorem 7.6 (no interpolation keeps
three generations), plus paragraphs on temperature, the missing 10_H and the native Narain point, and a scope boundary.
