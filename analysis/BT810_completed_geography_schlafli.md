# BT810 — The Completed Geography and the Schläfli Dictionary

Every maximal subgroup of PSp(4,3) now has a name in W(3,3) language and
a classical name on the cubic surface.  The last unknown (index 45) is
settled by GAP + Python verification.

## The index-45 theorem

The 130 lines of PG(3,3) split as 40 isotropic + 90 hyperbolic; the
symplectic polarity L -> L^perp is fixed-point-free on the hyperbolic
lines, giving exactly 45 polar pairs {L, L^perp}, and

```text
Stab{L, L^perp} = (SL(2,3) x SL(2,3)) : C2,  order 1152, index 45.
```

Mechanism: the pair splits F3^4 = L (+) L^perp into two orthogonal
symplectic planes, each carrying Sp(2,3) = SL(2,3) = **2T, the binary
tetrahedral group — the vertex group of the 24-cell** — and the
polarity swaps the two factors.

## The completed geography

```text
index 27:  2^4 : A5            F4^2 register : icosahedron       (BT809)
index 36:  S6 = PSigmaL(2,9)   regular spread stabilizer, 36 spreads
index 40:  parabolic           W33 point stabilizer (building)
index 40:  parabolic           W33 line stabilizer (building)
index 45:  (2T x 2T) : 2       hyperbolic polar pairs            (BT810)
```

## The cubic-surface dictionary

PSp(4,3) = W(E6)', and the maximal indices are exactly the Schläfli
inventory of the 27 lines on a cubic surface:

```text
27 lines on the cubic        <->  icosahedral F4^2 registers
36 double-sixes              <->  regular spreads of W(3,3)
40 + 40 Steiner trihedra     <->  points / lines of W(3,3)
45 tritangent planes         <->  hyperbolic polar pairs
```

The double-six / spread match is particularly clean: both count 36,
both have stabilizer S6, and a double-six's two sextets mirror the
spread's hemisphere split (BT809 T3).

## The platonic ladder inside Sp(4,3)

```text
2T (24-cell vertex group)  = Sp(2,3), two per polar-pair stabilizer
order-48 cube group        = skew-pair chart stabilizer (BT773, 540 Q3s)
2I (600-cell vertex group) = SL(2,5), icosahedral core of spread chain
```

The binary polyhedral groups are not decoration: they are the local
cores of the substrate's maximal subgroup geography — 24-cell at the
hyperbolic splittings, cube at the chart atlas, 600-cell at the spread
fibrations.

## Boundary

Open: the explicit double-six <-> spread bijection (which 6+6 of what?);
the 2T x 2T action on the 9+9 points off the polar pair
(40 = 4 + 4 + 16... compute the point orbits of the index-45 maximal);
and the binary octahedral question: is the order-48 chart group 2O or
O_h as an abstract group (both order 48 — settle by element orders)?
