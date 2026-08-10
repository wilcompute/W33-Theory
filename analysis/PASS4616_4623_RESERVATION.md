# Passes 4616--4623 executed outcomes

This is the canonical protected-geometry continuation immediately after the published paired-axis/Golay packet 4592--4615. The mathematics was first developed in collided temporary namespaces; `analysis/PASS4592_4599_NAMESPACE_COLLISION.md` records the history. The current public/manuscript/data surfaces use only Passes 4616--4623.

## 4616 — explicit protected 45 = center-quad/E6-tritangent 45
The 45 protected 16-line singular supports of Pass4585 are explicitly PSp(4,3)-equivariantly identical to the older 45 antipodal center-quad quotient points. A representative protected support stabilizer has order 576 and fixes exactly one old quotient point; the orbit map `g U0 -> g Q0` is well-defined, bijective on 45 objects and generator-equivariant. Under this same bijection the protected `SRG(45,32,22,24)` is exactly the old center-quad transport/complement graph. The earlier parameter-only comparison is therefore closed by an explicit intertwiner.

## 4617 — the 45x40 transport is the complete minimum shell of the sentinel code
Under the Pass4616 row bijection, the Pass4586 transport matrix `T` is exactly the old center-quad 8-point support-incidence matrix. Over F2, `rank T=15`, the W33 point-line incidence has `rank N=25`, and `T N=0`. Hence `ker(T)=im(N)` and `row(T)=ker(N^T)` by dimension. The latter is the sentinel `[40,15,8]` code. All 45 rows of `T` have weight 8, and the exact sentinel enumerator has exactly 45 weight-8 words, so the rows are the complete minimum shell. The full enumerator is `1 +45 z^8 +720 z^12 +6930 z^16 +17376 z^20 +6930 z^24 +720 z^28 +45 z^32 +z^40`.

## 4618 — PSp gives an S3 multiplicity line; the W33 outer involution fixes one U6
For `Q12=K27/K15`, Pass4583's three PSp-invariant six-submodules are exhaustive. The full PSp commutant has F2-dimension 4 (16 elements), with exactly 6 units; those units realize all 6 permutations of the three six-spaces, i.e. `GL(2,2)=S3` on the multiplicity projective line. Thus no factor is canonical under PSp. The actual W33 outer similitude has cycle type `1+2` on the three: it fixes exactly one and swaps the other two. The fixed factor has inner image order 25920 and outer image order 51840. This is an internal multiplicity-space statement, not an identification with geometric D4 triality.

## 4619 — all 270 D4 half-spinor generators now have concrete W33-derived lifts
The maximal totally singular four-spaces have PSp orbit sizes `[27,36,36,36,135]`. For the transitive 135 family, a representative order-192 stabilizer fixes exactly three maximal/unextendable size-8 W33 partial spreads; these are exactly its three 8-line orbits in the line decomposition `[8,8,8,16]`, and each has full stabilizer 192. Thus this half-spinor object has a concrete three-valued lift. In the other half-spinor family, the degree-27 orbit is explicitly the 27 center-quad/E6 quotient-line G-set (order-960 stabilizer fixes a unique such line), while each of the three degree-36 orbits is explicitly the W33 spread G-set (order-720 stabilizer fixes a unique spread). The independent partial-spread census reconfirms 1755 size-8 partial spreads, of which 135 are maximal/unextendable.

## 4620 — the all-odd-q elliptic rank conjecture is exactly a Hermitian binary generator-code problem; still OPEN
Duality identifies `Q^-(5,q)=GQ(q,q^2)` with the dual of the Hermitian surface `H(3,q^2)=GQ(q^2,q)`. The proposed binary incidence rank is therefore exactly the statement `dim_F2 C_1(H(3,q^2))=q^4+q^2+1=theta_2(q^2)=|PG(2,q^2)|`, equivalently `C^perp subset C` with `dim C^perp=q(q^2-q+1)`. For odd q the relevant line-graph SRG coefficients are all even, so its adjacency squares to zero mod2 automatically. Exact q=3,5,7 anchors remain `(rank N, rank N^T N)=(91,70),(651,546),(2451,2150)`. A targeted literature audit found related Hermitian generator-code work but not the required cross-characteristic binary dimension theorem. The all-q formula remains OPEN.

## 4621 — outside box: the sentinel minimum shell reconstructs both sides of the 45x40 incidence
Retain only the 45 weight-8 sentinel words. Pairwise support intersections are `0:270, 2:720`; joining two minimum words when their intersection has size 2 reconstructs exactly the center-quad/E6 transport `SRG(45,32,22,24)`. On the 40 coordinate positions, pairwise co-occurrence counts are `1:540, 3:240`; joining coordinates with co-occurrence 3 reconstructs exactly the point-side W33 `SRG(40,12,2,4)`, explicitly different from the protected line-side graph `A_*`. Thus the complete sentinel minimum shell is a self-describing incidence object.

## 4622 — outside box: the 135 maximal partial spreads have a second canonical 3-to-1 quotient
The 135 maximal/unextendable size-8 W33 partial spreads are transitive. Pass4619 gives an order-192 subgroup `H` fixing exactly three of them, each with full stabilizer `H`. Therefore the 135 objects package into 45 conjugacy packets of three common stabilizers. Orbit-stabilizer gives `|N_G(H)|=576`, hence `N_G(H)/H=C3`, acting regularly on the three spreads in each packet. This produces another exact `135 -> 45` cover with C3 deck action. It is not identified with the center-quad 45-set without a separate explicit intertwiner.

## 4623 — outside box: outer W33 symmetry makes the exceptional 6|6 extension nonsplit
Although `Q12=K27/K15` restricts to PSp as `U6 direct-sum U6`, the outer involution fixes only one of the exhaustive three PSp-invariant six-spaces and swaps the other two. Any PGSp-stable complement to the fixed six-space would be a second outer-stable PSp-invariant six-space, which does not exist. Therefore `0 -> U6_fixed -> Q12 -> Q12/U6_fixed -> 0` splits over PSp but is nonsplit over PGSp, and no PGSp-equivariant projection `Q12 -> U6_fixed` exists. The Pass4583 orthogonal-pair wedge map is canonically outer-equivariant into the 12D extension, but selecting one U6 quotient requires dropping to inner equivariance or breaking the outer symmetry.

## Integration and evidence
- Canonical executable wrappers: `analysis/w33_pass4616_4617_e6_sentinel_transport_closure.py`, `w33_pass4618_outer_canonical_u6_factor.py`, `w33_pass4619_concrete_d4_triality_w33_lifts.py`, `w33_pass4620_qminus_hermitian_binary_rank_reformulation.py`, `w33_pass4621_sentinel_minimum_shell_self_reconstruction.py`, `w33_pass4622_partial_spread_stabilizer_packets.py`, `w33_pass4623_outer_nonsplit_u6_extension.py`.
- Canonical frozen certificates: `data/PART_W33_PASS4616_*.json` through `data/PART_W33_PASS4623_*.json`.
- Theorem insert: `analysis/PASS4616_4623_e6_sentinel_triality_rank_insert.tex`.
- Public card/page: `analysis/PASS4616_4623_e6_sentinel_triality_rank_index_insert.html`, `docs/protected-e6-sentinel-triality.html`, registered in the public extension manifest.
- Regression: `tests/test_w33_pass4616_4623_e6_sentinel_triality_rank.py`.
- Focused exact-regeneration workflow: `.github/workflows/w33_pass4616_4623_e6_sentinel_triality_rank.yml`.
- All three maintained manuscript wrappers insert this packet immediately after `PASS4592_4615_paired_axes_golay_enumerator_scheme_insert`, preserving numerical order.
- Namespace guard: paired-axis/Golay owns 4592--4615; this packet owns 4616--4623. The collided transient reservations/certificates were retired. Earlier `w33_pass4592_...` implementation files remain helper modules only and are explicitly noncanonical.

Evidence discipline remains explicit: the Hermitian all-q binary-rank theorem is not promoted beyond exact q=3,5,7; the E6/D4/O6-minus names denote explicit finite G-sets and modules; finite coding/triality structure is not a physical particle, spacetime, or dynamics identification.
