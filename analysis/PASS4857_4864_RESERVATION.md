# Passes 4857–4864 — CLOSED

Reserved collision-free at commit `e50fe1fd322c243899514e9ea44db43ac00fb880`. Post-execution searches for canonical Pass4857 and Pass4864 commits found only this packet and its descendants; no competing reservation was found.

All five queued fronts and all three outside-box probes were executed. Pass4859 is deliberately closed as a **partial theorem boundary** rather than an invented exact covering-radius result.

## Frozen evidence

- Pass4857: `data/PART_W33_PASS4857_RATIONAL_ORBITAL_BLOCKS.json`
  - `A_Q(PGSp)=Q^6 x M2(Q)^4 x M3(Q)^3`;
  - with `K=Q(sqrt(-3))`, `A_Q(PSp)=Q^3 x K^2 x M2(Q)^2 x M2(K) x M3(Q)^4`;
  - all noncommutative factors split over their centers. Benard's exceptional-Weyl Schur-index theorem is prior art; the repo result is the exact Pass4850 allocation.
- Pass4858: `data/PART_W33_PASS4858_TERNARY_TEN_MODULE.json`
  - the ten-dimensional quotient `H1_Levi(F3)/<oriented K3,3>` is absolutely irreducible for PSp and PGSp;
  - endomorphism rings are exactly `F3`; all 29524 projective nonzero vectors have PSp cyclic span ten.
- Pass4859: `data/PART_W33_PASS4859_SWITCHING_ENUMERATOR_RADIUS.json`
  - complete `2^35`-word enumerator of the non-cut E6 switching coset, on 40 even weights 120..198;
  - exact covering radius remains open, with rigorous `124 <= rho(K) <= 179`;
  - ordinary cut-space Ising polynomial remains open.
- Pass4860: `data/PART_W33_PASS4860_INTRINSIC_STEINER_SIGNING.json`
  - the 120 Steiner trihedral-pair triangles are exactly the odd triangles of the E6 switching class;
  - the 1200x360 triangle-parity map has rank325, so this parity determines a unique switching class modulo the 35-dimensional cut space;
  - the root-inner-product signing is an independent representative of the same class.
- Pass4861: `data/PART_W33_PASS4861_PORT_MATCHING_SYMMETRY_BREAK.json`
  - a full local bijection between the three sheet cells and the three incident GQ line ports is the minimal datum with trivial local S3 stabilizer;
  - global port matching leaves a diagonal PGSp copy; adding global chirality selects PSp.
- Pass4862: `data/PART_W33_PASS4862_STEINER_TWO_GRAPH_CODE.json`
  - `K=delta^{-1}(<p_Steiner>)` is the one-dimensional Steiner-parity extension of the graph cut space;
  - the 1080 even-Steiner triangles span the full `[360,324,3]_2` dual.
- Passes4863/4864: `data/PART_W33_PASS4863_4864_O5_ADJOINT_HOMOLOGY.json`
  - the 36 norm-two points of the natural five-dimensional O5(3) projective module reproduce the double-six graph;
  - a common-generator Hom calculation has dimension one and unique rank-ten map, giving `Q10 ~= Lambda^2(F3^5)`;
  - transported commutator gives center-zero, perfect `so5(F3) ~= sp4(F3)` with exact Jacobi and PGSp bracket invariance.

## Reproducibility / integration

- Producers: `analysis/w33_pass4857_rational_orbital_blocks.py`, `w33_pass4858_ternary_ten_module.py`, `w33_pass4859_switching_enumerator_radius.py`, `w33_pass4860_intrinsic_steiner_signing.py`, `w33_pass4861_port_matching_symmetry_break.py`, `w33_pass4862_steiner_two_graph_code.py`, `w33_pass4863_4864_o5_adjoint_homology.py`.
- Cross-certificate regression: `tests/test_w33_pass4857_4864_rational_steiner_o5.py`.
- Exact-evidence workflow: `.github/workflows/w33_pass4857_4864_rational_steiner_o5.yml`.
- Synthesis: `analysis/PASS4857_4864_EXECUTED_OUTCOMES.md`.
- Manuscript insert: `analysis/PASS4857_4864_rational_steiner_o5_insert.tex`.
- Shared frontier manifest imports the new insert.
- Standalone public page: `docs/rational-steiner-o5-adjoint.html`.
- Root-index card/materializer sources: `analysis/PASS4857_4864_rational_steiner_o5_index_insert.html` and `tools/integrate_pass4857_4864_public.py`.

Evidence boundary: every promoted algebra/code/incidence/module statement is exact at the stated finite level. The ordinary cut-space weight enumerator and exact covering radius of `[360,36,20]_2` remain genuine open finite computations. No continuum E6/O5 gauge field or automatic hardware realization is inferred.