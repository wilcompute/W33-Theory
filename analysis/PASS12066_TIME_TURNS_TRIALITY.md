# Pass 12066: time turns triality

Claude track. Builds on 12064.

## Setting

Two clocks at non-collinear events split one generation as 27 = 1+1+1 + 8_v + 8_s + 8_c (12064).

## Results

1. **Cyclic action on the octets.** The symmetries fixing both events, Stab(p) ∩ Stab(q) (order 48), act on
   {8_v, 8_s, 8_c} as the cyclic group ℤ₃: 16 elements each of id, (012) and (021), and no transposition.
   - The kernel is the two-clock group C₂ × Q₈ = H_p ∩ Stab(q) = Stab(p) ∩ H_q.
   - The ℤ₃ is the clock-choice rotation.
2. **The rotations are ticks.** The tick at each of the four common neighbours r does three things:
   - it fixes p, q and the monomial;
   - it cycles 8_v → 8_s → 8_c, with t_r² going the other way;
   - it moves the clock real form.

   These r are the events simultaneous with both clocks, and their fibres form the D4. Ticks at p, at q and at the
   other two hyperbolic-line events do not fix the pair.

## Reading

A tick at an event simultaneous with both clocks is a triality rotation of the matter octets. It is the same
operation as re-choosing the clocks. Only the cyclic half of triality is realised, so time is oriented.

## Scope

- This is the Weyl-level action on weights.
- Reading the three octets as families is **not** established here.

Producer: `analysis/w33_pass12066_time_turns_triality.py`.
