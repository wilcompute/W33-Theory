# Part CDXV — Z[ω]/(1-ω)^3 as the W33 Vertex Ring

## The Main Identification

Let π = 1-ω be the Eisenstein prime above 3 in Z[ω],
with N(π) = 3. Then:

    |Z[ω]/π^k| = N(π)^k = 3^k

    k=1: |Z[ω]/π| = 3   (residue field F_3)
    k=2: |Z[ω]/π^2| = 9
    k=3: |Z[ω]/π^3| = 27 = V(W33)  ← !!

**Theorem CDXV.1 (W33 Vertex Ring):** The 27 vertices of W33 are
in bijection with the elements of the quotient ring Z[ω]/(1-ω)^3.

## Ring Structure

Z[ω]/(π^3) is a local ring with:
- Residue field: Z[ω]/(π) ≅ F_3
- Maximal ideal: (π)/(π^3) of order 9
- Unit group: order 27 - 9 = 18 (elements not in maximal ideal)
- Additive group: (Z/3Z)^3

## The Three-Layer Filtration

The ideal filtration gives a three-step tower:

    Z[ω]/(π^3)  ―――  27 elements  (full ring)
         ↓
    (π)/(π^3)   ―――   9 elements  (maximal ideal)
         ↓
    (π^2)/(π^3) ―――   3 elements  (socle)
         ↓
         0

Each successive quotient is isomorphic to F_3 (3 elements):

    Z[ω]/(π) ≅ F_3        ← graded piece 0 (1st generation)
    (π)/(π^2) ≅ F_3       ← graded piece 1 (2nd generation)
    (π^2)/(π^3) ≅ F_3     ← graded piece 2 (3rd generation)

**Corollary:** The three graded pieces of the π-adic filtration of
the W33 vertex ring correspond to the three fermion generations.

## The Socle and the Ghost Rungs

The ghost rungs {72, 192\*, 240} correspond to elements that
lie in the maximal ideal but not at the top level:
- Ghost rung 72 ↔ elements in (π)/(π^2): 2nd-generation obstruction
- Ghost rung 240 ↔ elements needing all three layers: full-depth
- The filtration depth = number of ghost rungs = 3
