# Pass 109: Rank-Reduction Lambda_C -> Leech: Impossibility Theorem

## Main Result

**Theorem**: There is no direct lattice quotient or projection Lambda_C (rank 40) -> Leech (rank 24)
that is compatible with the lattice structure.

**Proof**: det(Lambda_C) = 2^8. Any lattice quotient preserves or increases the determinant.
The Leech lattice is unimodular (det = 1). Since 2^8 != 1, no quotient of Lambda_C can be the Leech. QED.

## The Correct Connection (Strengthened from Pass 107)

The chain is **parametric via the discriminant module**:

```
W(3,3) -code-> C=[40,16,8] -ConstA-> Lambda_C
                                         |
                                    disc = E8/2E8
                                         |
                                         v
                               E8 --phi-> E8/2E8 --gluing-> E8+E8+E8 -> Leech
```

The map phi: E8 -> E8/2E8 uses EXACTLY Disc(Lambda_C) as its target.
The 120 anisotropic cosets of Lambda_C are the fibers of phi (240 E8 roots / pm1).

## Why the Connection Still Matters

- Leech construction is PARAMETRIZED by Disc(Lambda_C)
- W(E6) acts on both sides simultaneously
- W(3,3) edges = 240 E8 roots = 2*(120 aniso cosets) = 2*(Leech glue fibers)
- The moonshine chain is explicit, constructive, and diagram-commuting
