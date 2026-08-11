# Passes 4865–4872 — executed outcomes

## Scope and audit discipline

This packet continues directly from the closed Passes 4857–4864 frontier. The repository is currently receiving more than one hundred commits in less than a day, so the one-week audit was reconstructed as substantive mathematical/code fronts and commit ranges, while reservation/freeze/publication-only commits were treated as bookkeeping rather than independent mathematical claims. The three named root manuscripts are integration wrappers; their `_body.tex` files plus certified inserts carry the actual long-form manuscript content.

The packet preserves the existing evidence firewall: finite counts are not promoted to isomorphisms without maps, external literature is prior-art/cross-check evidence rather than proof, and negative/intertwiner-obstruction results are retained rather than hidden.

## Pass 4865 — ternary Levi radical filtration theorem

Producer: `analysis/w33_pass4865_4866_ternary_filtration_steiner_clique.py`

Frozen certificate: `data/PART_W33_PASS4865_TERNARY_LEVI_RADICAL_FILTRATION.json`

For the 64-dimensional ternary cycle space of the GQ(4,2) Levi graph and the 54-dimensional oriented-K3,3-generated submodule:

- the canonical edge dot product has rank 35 and radical dimension 29;
- the full 29-dimensional radical lies inside the 54-dimensional K3,3-generated module;
- the radical has the exact invariant diamond `14 < {19,24} < 29`;
- its simple factors are `14,5,10`, while the 54-dimensional module has factors `14,5,10,25`;
- `54/29` is irreducible 25-dimensional;
- both `0 -> 29 -> 54 -> 25 -> 0` and `0 -> 54 -> 64 -> 10 -> 0` are nonsplit for PSp and PGSp;
- after quotienting the radical, the nondegenerate 35-space decomposes canonically as `25 orthogonal-sum 10`, and the 10-space is explicitly intertwined with the previously certified adjoint quotient.

ATLAS's characteristic-three U4(2)=PSp(4,3) degree list `{5,10,14,25,81}` is used only as an independent representation-label cross-check.

## Pass 4866 — Steiner clique homology / characteristic obstruction theorem

Same producer as Pass 4865.

Frozen certificate: `data/PART_W33_PASS4866_STEINER_CLIQUE_HOMOLOGY_OBSTRUCTION.json`

For the double-six graph `SRG(36,20,10,12)`:

- its clique complex has `f=(36,360,1200,1080,216)`;
- the maximal cliques are exactly 216 K5's and 120 maximal K3's;
- those 120 maximal triangles are exactly the Steiner trihedral-pair triangles, giving a graph-only characterization: Steiner iff the triangle has no common neighbor;
- every other triangle has exactly four common neighbors and lies in exactly two K5's;
- boundary ranks are `(35,325,755,216)` over both F2 and F3;
- Betti numbers are `(1,0,120,109,0)` over both fields;
- the 1080 non-Steiner triangle boundaries have rank 324 over F2 but 325 over F3, so the one-dimensional even-triangle defect is characteristic-two-only;
- over F3, H2 is canonically the 120-dimensional permutation module on Steiner/maximal triangles;
- exact common-generator calculations give `Hom_PSp(H2,Q10)=0` and `Hom_PSp(Q10,H2)=0`.

Therefore no linear PSp-equivariant Steiner-H2 / adjoint-10 bridge exists. A deeper bridge would have to be nonlinear, characteristic-changing, or use additional structure.

## Pass 4867 — ordinary cut Ising polynomial and complete binary code enumerator

Producer: `analysis/w33_pass4867_cut_ising_full_enumerator.py`

Frozen certificate: `data/PART_W33_PASS4867_CUT_ISING_FULL_CODE_ENUMERATOR.json`

The marked-double-six K6 chart reduces a cut, after fixing the marked vertex side, to 15 duad bits plus 20 triad bits. The 15 duad bits are a labeled graph on six vertices. Quotienting by S6 leaves exactly 156 unlabeled six-vertex graph classes; exhausting the `2^20` triad states for each representative and restoring orbit multiplicities replaces `2^35` direct cut-word enumeration by `156 * 2^20` exact evaluations.

Results:

- ordinary cut space size `2^35`;
- 82 occupied weight levels;
- minimum nonzero cut weight 20;
- maximum cut weight 216;
- exactly 120 maximum cuts;
- combining with the frozen Pass4859 nontrivial switching-coset enumerator closes the complete `2^36`-word weight enumerator of `K=[360,36,20]_2`;
- MacWilliams gives `A0..A7 = 1,0,0,1080,10530,127656,2329680,37193040`, independently recovering the 1080 weight-three even-triangle dual checks.

Boundary: the covering radius is **not** closed by this pass. The prior exact bound remains `124 <= rho(K) <= 179`.

## Pass 4869 — marked double-six K6 / F2^6 symplectic residue theorem

Producer: `analysis/w33_pass4869_marked_double_six_k6_symplectic_residue.py`

Frozen certificate: `data/PART_W33_PASS4869_MARKED_DOUBLE_SIX_K6_SYMPLECTIC_RESIDUE.json`

Mark one double-six. Its twelve lines form six canonical opposite columns. The remaining 35 double-sixes become:

- 15 duads C(6,2), the non-neighbor orbit;
- 20 triads C(6,3), the neighbor orbit.

Adjacency is unified by the nondegenerate alternating form on F2^6

`B(x,y)=x.y + wt(x)wt(y) mod 2`, with matrix `I6+J6` and rank six.

The full marked-residue automorphism group has order 1440 and is explicitly `S6 x C2`: S6 permutes the six columns and C2 fixes duads while complementing triads. The old 15-coordinate K6-duad carrier is therefore incidence-derived once a double-six is marked.

Boundary: the marking is extra data and the 35-vertex shell is not the whole 63-point W(5,2) three-qubit symplectic polar space.

## Pass 4871 — intrinsic Levi adjoint bracket theorem

Producer: `analysis/w33_pass4871_intrinsic_levi_adjoint_bracket.py`

Frozen certificate: `data/PART_W33_PASS4871_INTRINSIC_LEVI_ADJOINT_BRACKET.json`

Using only the Levi-incidence-derived 10-dimensional action matrices, solve for equivariant alternating products `Lambda^2 Q10 -> Q10`:

- PSp Hom dimension = 1;
- PGSp Hom dimension = 1;
- the two Hom lines agree up to nonzero F3 scalar;
- the unique nonzero map has rank 10;
- Jacobi holds on every basis triple;
- center dimension = 0;
- derived dimension = 10.

Thus the finite Lie bracket `Q10 ~= sp4(F3)` is intrinsic to the Levi incidence action, up to nonzero scalar. The earlier O5/Lambda^2 model is now an independent cross-certificate rather than a required definition.

## Pass 4872 — qutrit-native port-matching information/compiler theorem

Producer: `analysis/w33_pass4872_port_matching_information_compiler.py`

Frozen certificate: `data/PART_W33_PASS4872_PORT_MATCHING_INFORMATION_COMPILER.json`

Each local minimal S3-breaking sheet-to-port matching is exactly

`i -> (-1)^b i + r (mod 3)`, with `r in F3`, `b in F2`.

Hence:

- local native state = one trit + one bit;
- full 45-point table = 45 trits + 45 bits;
- state count = `6^45`;
- information = `45 log2(6) = 116.32331253245202` bits;
- globally packed fixed binary minimum = 117 bits;
- independent local three-bit encoding = 135 bits, an 18-bit overhead;
- adding global chirality raises the globally packed optimum to 118 bits;
- irreversible-reset Landauer lower bound = `45 k_B T ln 6`, plus `k_B T ln 2` for chirality.

Boundary: reversible routing does not pay the Landauer erasure cost unless information is actually erased, and no claim is made that a particular FPGA/photonic implementation attains the Shannon bound.

## Manuscript / release integration

The exact packet is integrated into all three root manuscripts through the shared frontier mechanism:

- the previous live frontier manifest is preserved byte-for-byte as `analysis/W33_CURRENT_FRONTIER_MANIFEST_THROUGH_4864.tex`;
- the live `analysis/W33_CURRENT_FRONTIER_MANIFEST.tex` now imports the preserved frontier and `analysis/PASS4865_4872_ternary_clique_cut_symplectic_insert.tex`;
- `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` already consume that shared frontier;
- the new insert has an idempotence guard so repeated inclusion is harmless;
- `w33_paper.tex` was restored byte-for-byte to its pre-edit blob after the shared-manifest integration, avoiding wrapper drift.

Frozen-certificate regression is committed at `tests/test_pass4865_4872_frozen_certificates.py`. A clean local checkout could not be performed in this runtime because the container had no DNS resolution for GitHub, and the GitHub combined-status endpoint currently reports no completed status contexts for the regression commit. Therefore this release does **not** claim that a newly triggered remote CI run has already been observed passing.

## Open reserved fronts

- Pass4868: exact covering radius of K remains open.
- Pass4870: quadratic refinement / Arf-type or other nonlinear characteristic-changing Steiner-to-adjoint bridge remains open.

These are intentionally left open rather than converted into count-based claims.
