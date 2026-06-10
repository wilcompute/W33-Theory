# BT745 — The Presentation Space is Two Torsors; Chirality = Mask Parity

BT744 noted 2160 rectangles x 24 lifts = 51840 = |Sp(4,3)|.  BT745 proves
this is a torsor statement, not an accident.

## Results (exact orbit computation, all 51840 pairs)

```text
Q1  the PSp(4,3)-action on presentation pairs is FREE
Q2  exactly 2 orbits, each of size 25920 (two torsors)
Q3  the BT718 canonical sheet lies ENTIRELY in orbit 0 (chiral)
Q4  orbit label = D4 mask parity, for every one of the 24 sheets:
      Type-A masks (weight 3: 1110,1101,1011,0111) -> orbit 0
      Type-B masks (weight 2: 1100,1001,0110,0011) -> orbit 1
    channels are orbit-blind.
```

## Theorem

The space of (centered rectangle, valid lift) presentation pairs is a
disjoint union of two free PSp(4,3)-orbits — two torsors — and the torsor
invariant is the D4 mask weight parity.  Consequences:

1. **Chirality.**  The Type-A/Type-B dichotomy of BT720 is the chirality
   of a free group action.  The parity sign used in the BT739 aggregate
   (+1 weight-3, −1 weight-2) is precisely the torsor character.
2. **Selectors are bundle sections.**  Rectangles form a single orbit
   G/H with |H| = 25920/2160 = 12.  Over each rectangle the chiral fiber
   has exactly 12 pairs (4 Type-A masks x 3 channels), a free H-orbit.
   A selector sheet = a section of the principal H-bundle
   PSp(4,3) -> PSp(4,3)/H.  The BT705 "hinge datum needed" theorem is the
   statement that this bundle has no canonical section — trivializing it
   requires exactly one H-worth of gauge data (24 = 2 x 12: chirality x H).
3. **Torsor coordinates.**  Choosing one base pair identifies the chiral
   torsor with the group itself: every Type-A presentation pair IS a group
   element.  The BT718 sheet is a 2160-element subset of PSp(4,3) mapping
   bijectively to G/H — a transversal of the order-12 subgroup H.

## The session's unified picture (BT739-BT745)

```text
building Delta = Levi graph        chambers = flags     apartments = octagons
St = Solomon-Tits H~1 = chart81 = LeviE4   (BT742, BT744)
selector bridge unique     = Schur's lemma on St          (BT742)
aggregate full rank        = Schur (nonzero => injective) (BT739)
presentation pairs         = two PSp(4,3)-torsors         (BT745)
chirality                  = mask parity = BT739 sign     (BT745)
selector                   = section of order-12 bundle   (BT745)
register moves             = exact braid words sigma^5=Z  (BT740)
global register            = flat local system H^0 = F2^4 (BT741)
mod-2 defect               = mask 1001, H1 = 5 = F_5      (BT743)
```

## Boundary

Open: the isomorphism type of the order-12 rectangle stabilizer H and
whether the BT718 transversal is a coset-geometry object (e.g. related to
the A4/D6/Z12 subgroup lattice); the Type-B torsor's own selector theory;
and the W(E6) = Sp(4,3) x Z2 extension of the chirality story (does the
outer duality swap the two torsors?).
