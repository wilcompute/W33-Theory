# Step 3 — 432-Orbit Stabilizers: Executed Classification

**Date:** 2026-07-27  
**Status:** COMPLETE — the earlier order-60 plan is retracted.

## Group correction

The three 432-orbits are orbits of the full Weyl group
`W(E6)=U4(2):2`, whose order is 51840. The order-25920 group is the projective
index-two subgroup `U4(2)≅PSp(4,3)`. Therefore the stabilizer order is

`51840/432=120`, not 60.

## Exact computation

`analysis/w33_pass1134_we6_432_stabilizers.py` reconstructs the 240 E8 roots,
closes the six E6 reflection generators to all 51840 group elements, enumerates the
2240 A2 triples, and identifies the three size-432 orbits. For each representative
it computes the full stabilizer and its intrinsic invariants.

Every stabilizer has

- order 120;
- element orders `{1:1,2:25,3:20,4:30,5:24,6:20}`;
- center order 1;
- derived subgroup order 60;
- abelianization order 2.

This fingerprint is `S5=SmallGroup(120,34)`. It excludes `A5×C2`, which has a
central involution and elements of order 10, and excludes `SL(2,5)`, which is
perfect with center order 2.

## Conjugacy theorem

Explicit conjugating elements were found for every pair of stabilizers. Hence the
three subgroups are pairwise conjugate inside `W(E6)`, and the three 432-orbits are
isomorphic transitive G-sets:

`Omega_i ≅ W(E6)/S5`, for `i=1,2,3`.

Combining this with Pass 1126, each copy contains exactly one `81_minus` Steinberg
constituent.

## Certificate

- verifier: `analysis/w33_pass1134_we6_432_stabilizers.py`
- result: `data/w33_pass1134_we6_432_stabilizers.json`
- status: PASS
