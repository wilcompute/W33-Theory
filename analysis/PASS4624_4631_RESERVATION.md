# Passes 4624--4631 executed outcomes

This is the canonical continuation after Passes 4616--4623. All eight requested fronts were executed and integrated. The all-q Hermitian binary theorem remains explicitly OPEN; all other claims below are exact finite certificates.

## 4624 — packet 45 = protected support 45 = center-quad/E6 45
For a packet of three maximal size-8 partial spreads sharing the same order-192 stabilizer H, their union contains 24 W33 lines. Its 16-line complement is exactly one Pass4585 protected support. The full orbit of that complement is all 45 protected supports; its PSp stabilizer has order 576 and contains H with index three. Thus complement-of-union is an explicit PSp-equivariant bijection from the 45 stabilizer packets to the protected-support carrier, and composing with Pass4616 gives the center-quad/E6-tritangent 45.

## 4625 — intrinsic 45x40 classification
For the center-quad/sentinel support matrix T, the exact integer Smith form is `1^15 2^10 0^15`. Hence rank_Q(T)=25, every odd-characteristic rank is 25, and rank_F2(T)=15. Row intersections recover SRG(45,32,22,24); column co-occurrence recovers point-side W33; the exactly 40 weight-4 minimum words of ker_F2(T) are W33 lines and their intersection graph recovers line-side W33. Thus one unlabeled 45x40 incidence object contains all three finite carriers. The full side-preserving automorphism group is not separately claimed here without an independent exact automorphism computation.

## 4626 — explicit outer U6 descent cocycle
Choose a PSp splitting Q12=U+W with U the unique outer-stable six-space. Every inner generator is block diagonal. The outer involution is block upper triangular and its W->U off-diagonal block has rank six. Direct intertwiner equations give dim_F2 Hom_PSp(W,U)=1. Therefore the two PSp-equivariant complements form an F2 torsor and the outer involution exchanges them: the obstruction is the nonzero affine C2 descent cocycle, zero on PSp and nonzero on the outer generator. This is a descent-class computation inside the PSp-split problem, not a complete global Ext^1_PGSp computation.

## 4627 — rational rank theorem; binary problem = 2-saturation, still OPEN
For Q^-(5,q)=GQ(q,q^2), NN^T=(q^2+1)I+A_point. The point graph negative eigenvalue -(q^2+1) has multiplicity q(q^2-q+1), so ker_Q(N^T) is exactly that eigenspace and rank_Q(N)=q^4+q^2+1 for every q. For odd q, the proposed binary equality is therefore equivalent to rank_F2(N)=rank_Q(N), equivalently every nonzero Smith invariant factor is odd / the incidence image lattice is 2-saturated. Exact q=3,5,7 anchors satisfy this. A targeted primary-literature audit found defining-characteristic and weight-structure results but no directly applicable all-q cross-characteristic 2-saturation theorem, so the binary statement remains OPEN.

## 4628 — the compatible F4-choice space is point-side W33
On the outer-stable U6, compatible F4 structures are unoriented pairs {J,J^2} with J^2+J+I=0. The actual PGSp action has 80 oriented J and 40 unoriented structures. A representative has centralizer order 648 and normalizer order 1296. Carrying the same group elements on W33 points and lines shows that normalizer fixes exactly one W33 point and no W33 line. Hence the 40 compatible F4 structures form exactly the point-side W33 G-set. This identifies the noncanonical choice used in Pass4592 before the hexacode/Golay/MOG pipeline; the frozen Golay coordinate embedding itself is not PGSp-equivariant.

## 4629 — outside box: full outer S3 fiber
For each 45-object support, the PSp support stabilizer has order 576 and quotient C3 over H_192. Under PGSp the support stabilizer has order 1152 and induces all six permutations of the three maximal partial spreads, with kernel exactly H. Thus `1 -> H_192 -> Htilde_1152 -> S3 -> 1`; the PSp image is A3=C3 and the outer coset supplies transpositions.

## 4630 — outside box: H10 = binary homology = CSS logic = Smith 2-torsion
Because TT^T=0 mod2, `F2^45 --T^T--> F2^40 --T--> F2^45` is a complex with middle homology `ker T / im T^T = Cperp/C = H10`, dimension 10. The reduction modulo two of the integral kernel of T equals row_F2(T). Therefore the Bockstein `[x] -> [Tx/2]` identifies H10 with the `(Z/2)^10` torsion represented by the ten Smith factors 2. Using T as both redundant X and Z check matrices gives the exact `[[40,10,4]]` CSS code.

## 4631 — outside box: E6 incidence on F4-choice moduli
Combining Passes 4625 and 4628, T is an exact incidence between 45 center-quad/E6 objects and the 40 compatible F4 structures on U6. Each row contains 8 structures and each structure lies on 9 rows. Pair co-occurrence is 3 for exactly the 240 W33-adjacent pairs and 1 for the other 540. The 40 minimum weight-4 words in ker(T) are minimal even tetrads of F4 structures and are exactly the W33 lines.

## Integration and evidence
- Executables: `analysis/w33_pass4624_packet45_support_e6_intertwiner.py` through `analysis/w33_pass4631_f4_moduli_e6_incidence.py`.
- Frozen certificates: `data/PART_W33_PASS4624_*.json` through `data/PART_W33_PASS4631_*.json`.
- Theorem insert: `analysis/PASS4624_4631_packet_incidence_cocycle_f4_insert.tex`.
- Public card/page: `analysis/PASS4624_4631_packet_incidence_cocycle_f4_index_insert.html` and `docs/packet-incidence-f4-h10.html`, registered in the public frontier extension manifest.
- Regression: `tests/test_w33_pass4624_4631_packet_incidence_cocycle_f4.py`.
- Exact-regeneration workflow: `.github/workflows/w33_pass4624_4631_packet_incidence_cocycle_f4.yml`.
- `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` insert this packet immediately after Passes 4616--4623 and before the currently integrated 4640--4647 packet; a concurrent 4632--4639 lane can still insert numerically between them without collision.

Evidence boundary: finite incidence, integral-lattice, code, and group-action theorems only. The all-odd-q binary Hermitian rank formula remains open. The F4/Golay result identifies the choice G-set, not a PGSp subgroup of M24, and none of the E6/D4/S3/Bockstein/CSS structures is promoted to a physical particle, field, spacetime, or anomaly without an independent dynamics theorem.
