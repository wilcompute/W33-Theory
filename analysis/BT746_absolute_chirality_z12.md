# BT746 — Absolute Chirality, Canonical Involutions, and the Z12 Bundle

BT745 left open whether the full collineation group fuses the two
presentation torsors.  BT746 answers with three exact results — one
falsification and two discoveries.

## T1-T2: the W(E6)-torsor conjecture is FALSE; chirality is absolute

The similitude g = diag(1,1,2,2) (factor 2, non-square mod 3) extends
PSp(4,3) to the full collineation group

```text
PGSp(4,3) = U4(2):2 = W(E6),   order 51840.
```

But the orbit of a presentation pair under PGSp(4,3) is still 25920:
similitudes PRESERVE mask parity (200/200 samples; orbit count exact).
Type-A/Type-B chirality is invariant under EVERY collineation of W(3,3) —
it is an absolute geometric invariant, not a convention.  The natural
reading: for q odd, W(q) is not self-dual (its dual is Q(4,q)); the
chirality of the presentation space is a shadow of that broken duality.

## T3': every presentation pair carries a canonical involution

Since |W(E6)| / orbit = 2, each pair has a Z2 stabilizer in W(E6), and by
BT745 freeness its nontrivial element lies OUTSIDE PSp(4,3): a canonical
anti-symplectic involution attached to every (rectangle, lift) pair —
verified for the seed pair (involution, 8 fixed W33 points, not in PSp).
The presentation space is two copies of W(E6)/Z2 as a W(E6)-set.

## T5: the rectangle stabilizer is CYCLIC Z12

The stabilizer of a centered rectangle in PSp(4,3) has order 12 with
element-order profile {1:1, 2:1, 3:2, 4:2, 6:2, 12:4} — the profile of
**Z12**, the cyclic group.  Consequences:

- The 12 chiral lifts of a rectangle form a single free Z12-orbit: one
  order-12 symplectic symmetry cyclically rotates them.
- BT699's split 24 = 8 x 3 is really **24 = 2 x 12**: chirality times a
  Z12 cyclic rotation.  The D4-mask and Fano-channel layers are the
  2- and 3-parts of one cyclic group: Z12 = Z4 x Z3.
- Selector theory is the theory of sections of a principal **Z12-bundle**
  over the 2160 rectangles; the hinge datum of BT705 trivializes exactly
  one Z12 fiber coherently.
- Substrate reading: 12 = k (the W33 valency) appears as the structure
  group of the selector bundle; 24 = f = 2k as the full fiber.

## Status of the Solomon-idempotent remark

The BT739 aggregate is the difference of the two chirality-orbit sums; the
naive "sign character of W(E6)" interpretation died with the torsor fusion
conjecture, but the alternating structure over the Z12 x Z2 fiber stands —
its 2-part (mask weight) is the alternating sign, its 3-part (channel) is
summed trivially.

## Boundary

Open: the conjugacy class of the canonical pair-involutions in W(E6)
(8 fixed points on 40 — which of the two involution classes outside
U4(2)?); whether the Z12 generator's action on the 12 lifts matches the
Fibonacci sigma^5 clock of BT740 (12 vs 10 — the mismatch is itself
informative); and the Q(4,3)-side mirror of the chirality invariant under
the Klein/Plucker correspondence (P106).
