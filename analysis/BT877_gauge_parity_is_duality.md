# BT877 — Gauge Parity Is Duality: A₄ → S₄ Across the W/Q Duality

**Status: PROVEN (machine-verified, `analysis/bt877_gauge_parity_is_duality.py`, data `data/bt877_gauge_parity_is_duality.json`)**

Closing the BT876 open. The gauge module 1⊕3⊕8 came from C(R) = Stab(p₀)
acting as **A₄** (even permutations only) on the 4 lines through p₀. BT877
asks where the missing odd permutations are — and finds them in the duality.

## The theorems

- **T1:** building PGSp(4,3) = W(E₆) (order 51840) by adjoining the
  non-symplectic similitude M = diag(1,1,2,2) (which scales the symplectic
  form by 2 — the anti-symplectic generator) closes the full group.
- **T2:** Stab_PSp(p₀) acts on the 4 gauge lines as **A₄** (order 12, zero
  odd permutations), but Stab_PGSp(p₀) acts as the **full S₄** (order 24,
  with 12 odd permutations). The **odd permutations of the 4 gauge lines are
  exactly the anti-symplectic (W/Q duality) coset** — an outer element fixing
  p₀ realizes an odd 4-line transposition.
- **T3:** so the gauge sector's parity — the restriction to A₄ inside PSp —
  is the W/Q duality Z₂ of BT772. Parity lives only in the full W(E₆); the
  inner symplectic group sees only the even (orientation-preserving) gauge
  rotations.

## Reading

This is a parity-violation statement in substrate terms. The gauge group
acts on its 4-line structure (the SU(2)/U(1) sector, the 1+3 part of the
1+3+8 decomposition) through only the **even** permutations A₄ when restricted
to the symplectic (inner) group — the odd permutations require the
anti-symplectic duality. So:

- the **even** gauge rotations are inner (symplectic, the physical
  point-of-view-preserving transformations);
- the **odd** gauge rotations are the duality/chirality coset (BT772: chirality
  = axis type via the W↔Q point-line duality; BT869: the polar-pair
  involution);

and the gauge sector's handedness is tied to the same Z₂ that runs through the
chirality ledger (BT857/862/869). The Standard Model's weak sector acts
chirally (parity is violated); here the gauge 4-line action is restricted to
A₄ in the inner group, with full S₄ recovered only by adjoining the duality —
a substrate shadow of "parity is not an inner symmetry."

## Open

- Tie the specific odd transposition (1,0,2,3) to the weak-isospin doublet
  pairing of the 4 lines (which 2 lines pair under parity).
- The interplay of this gauge-parity Z₂ with the matter chirality Z₂ (BT869
  polar-pair involution) and the generation Z₃ (BT874) — the full
  C₂ × C₂ × C₃-ish discrete flavor/parity structure.
