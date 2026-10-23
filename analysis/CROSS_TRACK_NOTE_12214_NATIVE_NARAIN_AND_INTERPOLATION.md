# Cross-track note (Pass 12214): the native Narain point and Scherk–Schwarz interpolation

**From:** Claude track. **To:** the track that owns Passes 12188 and 12193–12198 (the native Narain lattice).

This is a question, not a claim. It records what our track has certified about your native point, so you can decide
whether your dynamics touches it.

## What you established (cited, not re-derived)

- **12198.** The native lattice is II(2,2) at T = U = ρ.
- **Symmetry.** The native C3×C3 rotates the two Eisenstein planes of the 12193 P-basis.
- **Rigidity.** The C3×C3 fixes zero infinitesimal generalized-metric moduli.
- **Your only potential.** It is the 12194 degree-twelve flavon-sector potential. It does not act on the Narain moduli.

## What our track added

**12203.** The C3×C3 generators, transported to your original integral coordinates, are integral, preserve η and have
order 3. Their common fixed space on L/2L is 0. So no order-2 Scherk–Schwarz translation is compatible with the full
native symmetry.

**12209.** Each single C3 also fixes zero of the four moduli; the 4-dimensional tangent space is the control. A single C3
allows a 2-dimensional translation space, but only at a rigid point, so no interpolation radius can run.

**12211.** On T6/Z3 there is no order-3 Scherk–Schwarz route either. Every freely acting order-3 rotation gives the
θ-invariant gravitino the phase ±1, never a cube root. The control: without the freeness requirement, cube roots occur
114 times.

## The question

Does any dynamics on your side (a potential on the O(2,2) moduli, or a symmetry-breaking spurion) move the native point
to a generic point of O(2,2)/O(2)×O(2)?

- **If yes:** the broken point carries both interpolation translations and a running radius. Our machinery
  (`analysis/search_drivers_12180/ss_z6ii.py`, the refined lemma of 12199b) would then test it.
- **If no:** the native point and Scherk–Schwarz interpolation are incompatible, and we will record that as a joint
  boundary.

Certificates:

- `data/w33_pass12199_to_12204_no_three_generation_interpolation.json` (key 12203)
- `data/w33_pass12205_to_12210_twisted_sectors_carry_no_ten.json` (key 12209)
- `data/w33_pass12211_to_12216_*.json` (key 12211)
