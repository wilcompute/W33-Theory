# Pass 4870 corrected breakthrough addendum — Steiner three-cover of the W33 line action and quadratic adjoint bridge

Pass4866 established that the 120-dimensional ternary H2 permutation module on the Steiner/maximal triangles has no nonzero PSp-equivariant linear map to or from the 10-dimensional adjoint quotient Q10.

Pass4870 correctly classified the PSp(4,3) action on unordered pairs of the 120 Steiner triangles. There are exactly four pair orbits:

| pairs | degree | triangle intersection | cross edges | role |
|---:|---:|---:|---:|---|
| 120 | 2 | 0 | 0 | forty K3 fiber components |
| 1620 | 27 | 1 | 6 | nonadjacent-fiber refinement |
| 2160 | 36 | 0 | 6 | complete K3,3 lift of Q(4,3) adjacency |
| 3240 | 54 | 0 | 4 | nonadjacent-fiber refinement |

## Correction from Passes 4953–4955

The original Pass4870 addendum made one false identification after obtaining the correct SRG parameters. Collapsing the forty K3 fibers does give an `SRG(40,12,2,4)`, but it is **not** the standard symplectic W(3,3) point graph. Pass4954 reconstructs both degree-40 generalized-quadrangle actions and proves:

- the standard W(3,3) point graph and the Steiner quotient are nonisomorphic;
- the Steiner quotient is exactly the intersection graph of the forty W(3,3) lines;
- equivalently, it is the point graph of the odd-q dual generalized quadrangle `Q(4,3)`;
- the W33 point graph has independent-triad common-neighbor census `1^2880 4^360`;
- the Q(4,3)/Steiner quotient has census `0^1080 2^2160` and has no spread.

Pass4955 then determines the dual roles directly from the maximum-cut/Steiner cross-incidence: the 120 maximum cuts collapse 3:1 onto the forty **W33 points**, while the 120 Steiner triangles collapse 3:1 onto the forty **W33 lines**. Their quotient non-splitting matrix is literal W33 point-line incidence.

The induced PSp action on the Steiner quotient still has order 25,920. This is the second, nonisomorphic degree-40 action, not a second copy of the point action.

## Quadratic bridge — survives unchanged except for the quotient label

Because 2 is invertible in F3, equivariant homogeneous quadratic maps H2 -> Q10 are equivalent to `Hom_PSp(Sym^2 H2,Q10)`. Sym^2 of the 120-point permutation module decomposes into the diagonal orbit module plus the four unordered-pair orbit modules. Stabilizer fixed-space dimensions in Q10 are:

- diagonal orbit, stabilizer 216: fixed dimension 0;
- 120-pair orbit, stabilizer 216: fixed dimension 0;
- 1620-pair orbit, stabilizer 16: fixed dimension 0;
- **2160-pair Q(4,3)-adjacency lift, stabilizer 12: fixed dimension 2**;
- 3240-pair orbit, stabilizer 8: fixed dimension 0.

Therefore

`dim Hom_PSp(Sym^2 H2,Q10) = 2`.

Both dimensions occur exclusively on the 2160-pair relation. Thus the linear obstruction remains sharp: the first PSp-equivariant Steiner-to-adjoint bridge occurs quadratically, but its orbital mediator is the recovered **Q(4,3) line-action quotient**, not the W33 point graph.

Pass4941 then combines any basis `q1,q2` of this quadratic plane with the intrinsic adjoint bracket to form the outer-even projective quartic `F(x)=[q1(x),q2(x)]`, which has full Q10 image.

Legacy producer: `analysis/w33_pass4870_steiner_w33_quadratic_bridge.py`

Corrected frozen certificate: `data/PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json`

Authoritative correction producers:

- `analysis/w33_pass4954_steiner_quotient_is_q43_dual.py`
- `analysis/w33_pass4955_maxcut_points_steiner_lines_incidence.py`
- `analysis/w33_pass4956_point_line_24d_intertwiner.py`

Manuscript insert: `analysis/PASS4870_steiner_w33_quadratic_bridge_insert.tex`

Public page: `docs/pass4870-steiner-w33-quadratic.html`

Boundary: the two-dimensional quadratic Hom space does not select a preferred nonzero map, continuum normalization, or physical coupling without additional structure. The old standard-W33 graph identification is superseded and must not be used downstream.