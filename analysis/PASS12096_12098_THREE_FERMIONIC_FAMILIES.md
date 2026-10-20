# Passes 12096–12098: three chiral fermionic families from the clock gradings

Claude track. Builds on 12089–12091.

## 12096: the SO(10) level (realisable)

The SO(10) grading is the E6 clock vacuum of an event plus a split. That is dimension 3, so one order-2 shift plus two
order-2 Wilson lines suffice. Across all 27 such gradings, with every order-3 shift keeping so(10):

- the net number of chiral 16s per plane is **0 or ±3 only**, never 1, 2 or 4;
- ±3 occurs exactly when the fixed algebra is e6 + a2;
- the 10s stay vector-like;
- **the split σ is odd on every spinor root**, so the three chiral 16s are fermions.

## 12097: the Standard-Model level

Across three SM gradings, pair each of the 20 three-family shifts with each of the 5 clean fermion parities.

- **40 of the 100 pairs put all three families in fermionic (σ-odd) sectors, with no chiral bosons.**
- The other 60 split the families: fermionic (2,2,0,0,2) and bosonic (1,1,3,3,1).

## 12098: families as an event

Across 33 SM gradings:

- every grading has exactly 20 three-family shifts;
- in 12 gradings, exactly one ±t pair has the family a2 equal to an event fibre; in the other 21 gradings, none does;
- whenever the family a2 is the fibre of an event x, the E6 is **E6(x)** (24 of 24).

In those vacua the three families are the Eisenstein-unit triplet A2(x) of a single event, and the unified group is
that event's E6: the corpus's 81 = 27 × 3.

A first count filtered on fixed dimension 86 alone. That included anomalous shifts and was wrong.

## Scope

Untwisted, per-plane counting. Twisted sectors and modular invariance are not computed.

Producer: `analysis/w33_pass12096_12098_three_fermionic_families.py`.
