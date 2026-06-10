# BT748 — Half-Fibers are Centralizer Torsors; the BT718 Sheet is Not Root-Natural

Executes the two BT747 boundary questions.

## Q1: the torsor structure of the root-triple fibers

The centralizer C = C_W(E6)(t) of a pair-involution has order 96
(48 inner + 48 outer), equal to the fiber size — but the fiber is NOT a
C-torsor: the C-orbit of a fiber pair has size 48 and stays inside one
chirality class.  The correct statement is sharper:

```text
the INNER centralizer C ∩ PSp(4,3)  (order 48)
acts freely and transitively on EACH chirality half-fiber.
```

(The full-C stabilizer of a fiber pair is exactly <t> itself.)  Hence every
presentation pair acquires complete equivariant coordinates

```text
pair  <->  (root triple tau, chirality eps, centralizer element c)
51840  =       540        x      2       x       48.
```

The presentation space is the associated bundle of the 3A1 class with
half-fibers torsors under the order-48 inner centralizer.  Identifying
that order-48 group and its relation to the Z12 rectangle clock (BT746) is
the next structural question.

## Q2: the BT718 sheet fails root-uniformity

If the canonical sheet were natural for the root fibration it would meet
each of the 540 fibers 2160/540 = 4 times.  Measured distribution of hits:

```text
hits:   0   1   2   3   4   5   6   7   8   9  10  11
fibers: 75  44  64  56  64  60  72  52  23  18  10   2
```

Wildly non-uniform — 75 root triples are never selected, 2 are selected 11
times.  The BT718 edge-order convention sheet, although rank-complete
(BT714), is NOT equivariantly natural with respect to the canonical root
coordinates.  Together with BT741's fragmented gluing (56 components) this
is the second independent signal that a better canonical selector should
exist: one defined directly in (tau, eps, c) coordinates, e.g. fixing a
canonical centralizer element per root triple.  Such a selector would be
root-uniform by construction and likely repair the gluing fragmentation.

## Boundary

Open: isomorphism type of the order-48 inner centralizer (vs Z12 of BT746:
48 = 4 x 12?); construction of the root-natural selector (pick c = identity
in torsor coordinates after a base choice — what does it look like as a
sheet? is it rank-81? is its gluing flat?); and the chirality-flip map
(outer centralizer elements swap nothing — what canonical object exchanges
the two half-fibers?).
