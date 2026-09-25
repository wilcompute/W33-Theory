# Pass 10955 — D4 half-spin sheet exchange is the clock determinant character

Producer: `analysis/w33_pass10955_d4_halfspin_clock_bridge.py`

Certificate: `data/w33_pass10955_d4_halfspin_clock_bridge.json`

Regression: `tests/test_w33_pass10955_d4_halfspin_clock_bridge.py`

## 1. The clock group has a faithful signed 4D realization

Pass 10954 used the four oriented A2 factors as four sign coordinates. For every g in GL(2,3), the frozen tetracode monomial action gives a permutation of those four coordinates together with four signs.

Replacing each ternary scale 1,2 by the real sign +1,-1 gives a 4x4 signed permutation matrix R(g). Exhaustion proves

```text
R(gh)=R(g)R(h)   for all 48^2 ordered pairs,
|R(GL(2,3))|=48.
```

So this is a faithful representation, not a character-level analogy.
## 2. The image preserves the D4 root system

Take the standard D4 root shell

```text
{ +/-e_i +/-e_j : i<j },
```

with 24 roots. Every one of the 48 matrices R(g) preserves this root set exactly.

Inside the full signed permutation group W(B4), the Weyl group W(D4) is the even-sign-flip subgroup. The executable obtains

```text
det_F3(g)=+1  <-> even number of sign flips,
det_F3(g)=-1  <-> odd number of sign flips.
```

Hence the SL(2,3) half lies inside W(D4); the determinant-reversing half lies in the other signed-permutation root-automorphism coset.

This is objectwise compatible with the older Pass 540 determinant/product-parity separator, but the 4D signed representation and its weld to the new clock are new here.
## 3. The sixteen orientation signs are the two D4 half-spin demicubes

Store twice the usual half-spin weights so no fractions are needed:

```text
(+-1,+-1,+-1,+-1).
```

The sixteen sign vectors split into

```text
S+ : even number of minus signs, 8 weights,
S- : odd number of minus signs, 8 weights.
```

The vector minuscule weight set is

```text
V = {+-e_1,...,+-e_4}, |V|=8.
```

For all 48 clock/tetracode elements, det=+1 fixes V, S+, and S- as sets, while det=-1 fixes V and swaps S+ with S-. The outer image is therefore one C2 transposition inside Out(D4)=S3, not a triality 3-cycle.
## 4. The exact order-eight clock alternates the two spinor sheets

For the Pass-10951 clock generator

```text
g = [[0,1],[1,1]]
```

the signed 4D matrix has exact order eight. Its power ladder is

```text
one tick : S+ <-> S-
two ticks: S+ and S- preserved separately
four ticks: R(g)^4 = -I4
eight ticks: identity.
```

On S+ union S-, one tick has two disjoint cycles of length eight, and each cycle alternates sheet at every step. The fourth power negates every vector weight and every half-spin weight. This is the same central -I already seen in Pass 10951, now on the explicit D4 weight carrier.
## 5. One determinant character now controls four exact finite layers

The same GL(2,3)->C2 determinant character is now certified as:

- the extended-Clifford unitary/antiunitary character;
- the Pass-10952 clock CP/non-CP grading;
- the Pass-10954 Fano-hinge orientation-parity grading;
- the D4 half-spin sheet-preserving/sheet-swapping grading.

For the clock powers, even n gives the unitary/CPTP qutrit sector and preserves each half-spin sheet, while odd n gives the non-CP bare-qutrit slot and swaps the two half-spin sheets.

These are two representations of one finite character, not an assertion that complete positivity is literally fermion chirality.

There is also an important distinction from Pass 10954: position-space sheet parity alternates every odd tick, but the missing spectral modes k=2,6 are deck-even. The omitted +i,-i Fourier pair is therefore not “the missing chiral sector.”
## 6. Prior art and evidence boundary

Pass 540 already identified a different 16-sign packet with the two D4 demicubes and showed a determinant-minus-one swap. Pass 10955 does not claim that observation anew. Its new content is the explicit faithful GL(2,3) signed-permutation representation coming from the current tetracode clock, all 48^2 multiplication checks, its exact order-eight power ladder on D4 weights, and the objectwise weld to Passes 10952–10954.

Standard D4 theory has three eight-dimensional minuscule representation classes: vector and two half-spin. The D4 outer S3 permutes those classes. Our subgroup realizes only the transposition fixing the vector class.

## Boundary

“Half-spin” here is the exact D4 root/weight-system notion. This does not identify S+ and S- with observed left/right fermions, the executable Pass-10950 Spin(1,9) Weyl field, or a continuum Pin/Spin bundle. Such a promotion requires a separate representation intertwiner.
