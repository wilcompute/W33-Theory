# Pass8781–8828 — CSS / Leech / W33 synthesis

This batch was replayed against live `master` after the parallel cyclotomic-lift/coisotropic Pass8721–8776 work landed.

## Five executed fronts

1. **92D logical-half MeatAxe theorem (Pass8781–8788).** The characteristic-two `W(E6)` logical half has composition factors `1^4 + 6^3 + 8^2 + 14 + 40`. Every nonzero vector was tested for the 1/6/8/14 factors; the 40D factor is certified by a 6D kernel of an algebra element with characteristic polynomial `(x+1)^40`, all 63 nonzero kernel seeds generating the full factor.
2. **20,800 bare Leech Lagrangians (Pass8789–8796).** The `G2(4):2` carrier has rank 14 with subdegrees `1,63,72,126,252,252,378,1512,1512,1512,2016,3024,4032,6048`; intersection dimension alone does not close the relations.
3. **Six-qutrit W33 slice space (Pass8797–8804).** The `Sp12(3)/(Sp4(3)xSp8(3))` action has exactly 31 double cosets. Their orbit sizes sum to `2,110,666,092,277,743`, reproducing the full W33-slice census. Intersection shells with a fixed W33 are `d=4:1`, `d=3:262400`, `d=2:6076864200`, `d=1:12684803040000`, `d=0:2097975212111142`.
4. **Point-star logical module (Pass8805–8812).** The forty weight-12 point-stars span dimension 25, have Gram matrix `A_W33 (mod 2)` of rank 16, radical dimension 9, and composition `1|8|1|14|1` with radical `1|8`.
5. **Objectwise Leech→W33→CSS diagram (Pass8813–8820).** The Pass8481 36-object Leech/W33 weld extends to the CSS matching carrier: the twelve Leech three-sheet fibres map to the twelve W33 neighbors of a fixed point, and each neighbor selects the unique matching coordinate on `pq` containing edge `{p,q}`. The twelve coordinates split canonically as `4 x 3` by the four W33 lines through the point.

## Three outside-box results

- **Local split Cayley hexagon (Pass8821–8828).** The unique degree-63 suborbit around a bare Leech six-space, with adjacency given by mutual intersection dimension four, is distance-regular with intersection array `{6,4,4;1,1,3}` and spectrum `6^1 3^21 (-1)^27 (-3)^14`: the point graph of the generalized hexagon `H(2)`.
- **Unique noncommutative orbital block.** The rank-14 Leech orbital algebra is noncommutative but has center dimension 11. Over `C`, semisimplicity forces `C^10 ⊕ M2(C)`: exactly one doubled irreducible sector.
- **E6 tritangents as logical dependencies.** The coefficient kernel of the forty point-stars is exactly `ker(N^T)`, the historical W33 sentinel `[40,15,8]_2` code. Pass4593 already identifies its 45 minimum weight-8 words with the 45 center-quad/E6 tritangent supports. Hence those 45 tritangents are exactly the 45 minimum linear dependencies among the forty canonical logical point-stars.

## Parallel-frontier reconciliation

Pass8721–8776 proves the qutrit cyclotomic descent selects W33 canonically as a **coisotropic subquotient** `K/K^perp`, not as a preferred W33 subspace. This is fully compatible with Pass8797–8804: the bare six-qutrit carrier contains a single enormous orbit of W33 subspaces, split into 31 stabilizer double cosets relative to a reference W33, while the cyclotomic datum bypasses subspace selection entirely.

No physical identification is inferred from the finite combinatorial/module equivalences in this packet.
