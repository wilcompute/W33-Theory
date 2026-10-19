# Pass 12069: flavour CP is a bosonic time reversal, not an observer

Claude track. Joins 12004/12044 to 12059–12060.

## Question

The flavour chain's generalised CP elements are CP∘g, with CP: Ω → −Ω̄ (that is, diag(I, −I)) and g drawn from:

- the theta-group family T^{2b} × T^{2b'} (12004);
- the S-type family S × S, S × T^{2b} and T^{2b} × S (12044).

What are they on the forty events after reduction mod 3?

## Results

1. **All are bosonic.** Every element reduces to an anti-symplectic J with J² = +1, never J² = −1. So no flavour CP is
   a Kramers reversal, an observer or a mirror frame.
2. **They are pairs of opposite contexts.** There are 1080 anti-symplectic involutions, 540 up to sign, and they are
   exactly the 540 pairs of opposite contexts (L₊, L₋), which are their ±1 eigenspaces.
3. **CP reverses time on 8 events.** Each one fixes exactly the 8 events of L₊ ∪ L₋ and inverts their ticks:
   J t_p J⁻¹ = t_p⁻¹. Elsewhere it maps t_p to t_{Jp}⁻¹.
4. **The corpus elements are all distinct.** The 16 distinct named elements give 16 distinct context pairs. CP itself
   gives (span(e₁,e₂), span(e₃,e₄)).

## Reading

The geometry has two kinds of time reversal:

- fermionic: Kramers, J² = −1, 36 of them, the observers;
- bosonic: J² = +1, 540 of them, the context pairs.

Flavour CP is bosonic. It reverses time exactly on the eight events of its two contexts.

## Scope and prior art

- This is the mod-3 reduction of the named elements.
- Generalised CP in Sp(4,ℤ): Ding–Feruglio–Liu, arXiv:2010.07952.

Producer: `analysis/w33_pass12069_flavour_cp_is_a_bosonic_time_reversal.py`.
