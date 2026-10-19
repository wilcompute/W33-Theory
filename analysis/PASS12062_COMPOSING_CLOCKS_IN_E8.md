# Pass 12062: composing clocks in E8

Claude track. Builds on 12052–12056.

## Method

Inner involutions compose as θ_h θ_h' = θ_{h+h'}. In the root model this is the XOR of their parity vectors on the
240 roots. All 120 × 120 pairs of clocks were classified.

## Results

| Clocks c at p and c' at q | Product θθ' |
|---|---|
| same event | The three clocks and 1 form a **Klein four-group**: c₁c₂ = c₃. The clock choices multiply like the quaternion units i, j, k modulo sign. |
| collinear (context {p, q, r, s}) | **Always split.** The 9 products are exactly the 9 split involutions of the **3 factorisations that separate r from s**. |
| non-collinear (hyperbolic line {p, q, r, s}) | **6 products are the clocks at r and s** (three each), and **3 are the splits of ⟨p,q⟩ ⊕ ⟨p,q⟩^⊥**. |

## Reading

- Two compatible times never compose to a time: they compose to a two-factor (split) structure.
- Incompatible times compose to the times of the remaining events of their hyperbolic line, or to the factorisation
  they span.
- The single-event Klein group matches the Q₈ of 12058 taken modulo ±1.

## Prior art

The rule θ_hθ_h' = θ_{h+h'} is classical. A corpus grep for clock-involution products and Klein four-groups found
nothing.

Producer: `analysis/w33_pass12062_composing_clocks_in_e8.py`.
