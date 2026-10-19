# Pass 12080: time reversals inside E8

Claude track. Builds on 12059, 12069 and 12079.

## Construction

Putting C in bipartite form gives an involution w ∈ W(E8) with wCw⁻¹ = C⁻¹. It inverts ω = C¹⁰ and preserves the
fibres. The coset w·Sp(4,3) contains all the antilinear elements of interest.

## Results

1. **Two square classes.** The elements of the coset that act as involutions on the forty events are exactly:
   - **72 with no fixed event, e² = −1**: the Kramers observers;
   - **1080 with 8 fixed events, e² = +1**: the bosonic CPs.

   So J² = ∓1 is literally e² = ∓1 in W(E8).
2. **ω and the clocks.** ω keeps each clock at its event and **3-cycles the three clocks there**: the clock choice at an
   event is a choice of cube root of unity.
3. **CP-compatible clocks.** Kramers reversals preserve no clock. **Each bosonic CP preserves exactly one clock at each
   of its 8 fixed events.**
4. **Link to the Hamming code.** For all 1080 CPs, the CP-compatible clocks on L leave su(2)⁸ on exactly the CP's own
   fixed set L ∪ L′.

## Reading

Observers' time reversals and flavour CP are the two square classes of the antilinear Weyl elements of E8. A flavour CP
picks one clock at each event it fixes.

Producer: `analysis/w33_pass12080_cp_compatible_clocks.py`.
