# Passes 4664–4671 executed outcomes

All five requested fronts plus three outside-box probes are closed on `master`, except the intentionally open all-q Hermitian 2-saturation theorem in Pass4666. The range was reserved after 4656–4663; that predecessor lane completed while this packet was being integrated, and the maintained manuscript wrappers now place its insert immediately before this one.

## 4664 — the two S3 actions are transverse
The Pass4629 packet S3 and Pass4641/4643 D4 spread-sheet S3 are abstractly isomorphic but are not the same ambient symmetry. The packet order-three subgroup lies inside PSp(4,3); the sheet order-three subgroup is the centralizer C3 outside the distinguished PSp and intersects it trivially. They commute. A common outer reflection inverts both, producing `(C3 x C3):C2` of order 18.

## 4665 — full automorphism group of T
The 45x40 incidence T intrinsically reconstructs point-side W33 by column co-occurrence, then its 40 maximal K4s reconstruct the W33 lines and full W(3,3) incidence geometry. Conversely PGSp(4,3) preserves W33 and the 45 center-quad/sentinel rows. Since the two bipartite sides have different sizes/degrees, they cannot swap. Therefore `Aut(T)=PGSp(4,3)` of order 51840.

## 4666 — Hermitian rank becomes a 2-adic eigenlattice theorem; still OPEN
For Q^-(5,q)=GQ(q,q^2), let `L=im_Z N` and `K=ker_Z N^T`. The identity `NN^T=(q^2+1)I+A_point` and positivity give `K=ker_Z(NN^T)`, the integral negative eigenlattice. Since K is primitive and `L_Q=K_Q^perp`, the saturation is `L_sat=K_Z^perp`. Thus the all-odd-q binary rank theorem is exactly `L tensor Z_2 = K_Z^perp tensor Z_2`, equivalently the finite quotient `K^perp/L` has no 2-primary part, equivalently every nonzero Smith factor of N is odd. Exact q=3,5,7 anchors satisfy the target. No all-q proof was found; the theorem remains OPEN.

## 4667 — selected Smith bit pins H10 head/socle
The selected 135x270 incidence has exactly one Z/2 torsion factor, hence a one-dimensional trivial PSp module. The canonical protected filtration is `0 < <j> < V9=ker(pi) < H10` with factors `1|8|1`. Therefore the unique nonzero maps are `i(1)=j` and `pi:H10->F2`; their composition is zero. The induced rank-one nilpotent `n(x)=pi(x)j` has `n^2=0`, image `<j>`, kernel `V9`, and does not select any direction in the irreducible V8 middle.

## 4668 — F4 choice moduli = D4 triality-intersection planes
Pass4628 and Pass4654 give independent equivariant charts through the same W33-point carrier. Composing them yields `{J,J^2} -> p(J) -> P(p(J))`, an explicit PSp bijection between the 40 compatible F4 structures on U6 and the 40 anisotropic F2 planes fixed pointwise by pairwise triality-conjugate PSp intersections. The stabilizer tower is `216 < 648 < 1296`.

## 4669 — outside box: oriented 80-to-40 moduli cover
The 80 oriented J operators lie over the 40 unoriented pairs `{J,J^2}`. On the triality side the quotient `648/216=C3` cyclically orients each three-point anisotropic plane, while the full outer involution reverses that orientation. Both descriptions therefore lift to the same 80-to-40 orientation double cover, unique after one base orientation is chosen and otherwise differing by global reversal.

## 4670 — outside box: the D4 lane reconstructs T, H10, and CSS
Concurrent Pass4659 reconstructs the 45 cubic tritangents internally from the selected 135_6-270_3 geometry and maps them to protected45. Triality intersections reconstruct the W33-point 40. Transporting the protected cross relation along these two action-level charts reconstructs the same T. Thus the D4-derived lane recovers `SNF(T)=1^15 2^10 0^15`, the H10 Bockstein `(Z/2)^10`, and the `[[40,10,4]]` CSS code.

## 4671 — outside box: exact local S3 stabilizer extension
The concurrent subgroup classification gives `(3^{1+2}:Q8)_216 < (3^{1+2}:SL(2,3))_648 < H_1296`. The 216 group is the triality-conjugate PSp intersection and pointwise plane stabilizer. The quotient `648/216=C3=A3` rotates the three nonzero plane vectors. The 1296 semilinear layer adds the orientation-reversing outer involution, so `1 -> (3^{1+2}:Q8)_216 -> H_1296 -> S3 -> 1`, with the 648 group the preimage of A3.

## Release state
- executable witnesses `analysis/w33_pass4664_*` through `analysis/w33_pass4671_*`;
- frozen certificates `data/PART_W33_PASS4664_*` through `data/PART_W33_PASS4671_*`;
- theorem insert `analysis/PASS4664_4671_s3_automorphism_eigenlattice_triality_insert.tex`;
- public card/page `analysis/PASS4664_4671_s3_automorphism_eigenlattice_triality_index_insert.html` and `docs/s3-automorphism-eigenlattice-triality.html`;
- regression `tests/test_w33_pass4664_4671_s3_automorphism_eigenlattice_triality.py`;
- exact-regeneration workflow `.github/workflows/w33_pass4664_4671_s3_automorphism_eigenlattice_triality.yml`;
- all three maintained manuscript wrappers include the packet after the completed 4656–4663 predecessor.

Evidence discipline remains fail-closed: the all-q Hermitian 2-saturation theorem is not promoted beyond the exact reformulation/anchors; the oriented cover has a global reversal ambiguity; no M24 subgroup, physical chirality/family symmetry, or hardware/dynamics statement is inferred from these finite structures.
