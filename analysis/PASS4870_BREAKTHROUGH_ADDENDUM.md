# Pass 4870 breakthrough addendum — Steiner three-cover of W33 and quadratic adjoint bridge

Pass4866 established that the 120-dimensional ternary H2 permutation module on the Steiner/maximal triangles has no nonzero PSp-equivariant linear map to or from the 10-dimensional adjoint quotient Q10.

Pass4870 classifies the PSp(4,3) action on unordered pairs of the 120 Steiner triangles. There are exactly four pair orbits:

| pairs | degree | triangle intersection | cross edges | role |
|---:|---:|---:|---:|---|
| 120 | 2 | 0 | 0 | forty K3 fiber components |
| 1620 | 27 | 1 | 6 | nonadjacent-fiber refinement |
| 2160 | 36 | 0 | 6 | complete K3,3 lift of W33 adjacency |
| 3240 | 54 | 0 | 4 | nonadjacent-fiber refinement |

The 120-pair relation is exactly 40 disjoint K3's, giving an intrinsic partition of the Steiner triangles into forty three-element fibers. The 2160-pair relation is complete between adjacent fibers: every quotient edge lifts to all nine pairs in a K3,3. Collapsing the fibers gives an SRG(40,12,2,4), and an exact graph-isomorphism check identifies it with the standard symplectic W(3,3) collinearity graph. The induced PSp action on the quotient has order 25,920.

Because 2 is invertible in F3, equivariant homogeneous quadratic maps H2 -> Q10 are equivalent to `Hom_PSp(Sym^2 H2,Q10)`. Sym^2 of the 120-point permutation module decomposes into the diagonal orbit module plus the four unordered-pair orbit modules. Stabilizer fixed-space dimensions in Q10 are:

- diagonal orbit, stabilizer 216: fixed dimension 0;
- 120-pair orbit, stabilizer 216: fixed dimension 0;
- 1620-pair orbit, stabilizer 16: fixed dimension 0;
- **2160-pair W33-adjacency lift, stabilizer 12: fixed dimension 2**;
- 3240-pair orbit, stabilizer 8: fixed dimension 0.

Therefore

`dim Hom_PSp(Sym^2 H2,Q10) = 2`.

Both dimensions occur exclusively on the pair relation that projects to W33 adjacency. Thus the linear obstruction is sharp: the first PSp-equivariant Steiner-to-adjoint bridge occurs quadratically, and W33 itself is the mediator.

Producer: `analysis/w33_pass4870_steiner_w33_quadratic_bridge.py`

Frozen certificate: `data/PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json`

Manuscript insert: `analysis/PASS4870_steiner_w33_quadratic_bridge_insert.tex`

Public page: `docs/pass4870-steiner-w33-quadratic.html`

Boundary: the two-dimensional quadratic Hom space does not select a preferred nonzero map, continuum normalization, or physical coupling without additional structure.
