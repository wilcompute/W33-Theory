> **REFUTED AND REPLACED (Pass 1375, 2026-07-31).** Both premises of this file
> are wrong. `|Sp(4,3)| = 51840`, not 25920 -- 25920 is `|PSp(4,3)| = |U4(2)|`,
> and `Sp(4,3) = 2.U4(2)` is its double cover. And the group acting on the 2240
> A2 root triples is neither of those: it is `W(E6) = U4(2):2`, also of order
> 51840 but NOT isomorphic to `Sp(4,3)` (25 irreducibles and two degree-81s, vs
> 34 and one). So the stabiliser order is `51840/432 = 120`.
>
> The computation this file planned has now been run, and it answers the
> question it set out to ask: the stabiliser **is `S5 = SmallGroup[120,34]`**,
> and all three 432-orbits are **conjugate** in `W(E6)`. The 60 asserted here is
> not meaningless -- it is `|S5 n PSp(4,3)| = |A5|` -- but it was reached by
> dividing the order of a group that is not acting, so it names that A5 only by
> coincidence.
>
> This file also mislocates the object: its script searches for 432-orbits among
> the 780 point-PAIRS of `W(3,3)`, where the orbits are `240 + 540` and no orbit
> of size 432 exists at all. The 432s live on the 2240 A2 root triples in E8.
>
> Certificate: `data/w33_pass1375_432_stabiliser.txt`.
> Script: `analysis/w33_pass1375_432_stabiliser_identification.g`.

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
