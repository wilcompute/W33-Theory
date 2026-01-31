We recorded 27 test files that require Sage during local test collection (artifact: `artifacts/skipped_optional_tests.json`).

Files:
- W33_pattern_search.py
- part_cxviii_verify.py
- sage_verify.py
- tmp_w33_lemma2.sage
- w33_81_cycles.sage.py
- w33_81_exploration.py
- w33_clique_complex.py
- w33_comprehensive_verification.sage
- w33_debug_classes.py
- w33_generalized_quadrangle.py
- w33_group_analysis.py
- w33_h1_decomp_direct.py
- w33_h1_decomp_gap.py
- w33_h1_decomp_v2.py
- w33_h1_decomposition.py
- w33_h1_irreducibility.py
- w33_incidence_deep.py
- w33_pysymmetry_analysis.sage
- w33_sage_incidence_and_h1.py
- w33_sage_sp4_3_verification.sage
- w33_sage_verification.sage
- w33_steinberg_check.py
- w33_sylow3_analysis.py
- w33_symplectic_graph.py
- w33_symplectic_verify.py
- w33_v23_analysis.py
- w33_verify_alignment.py

Acceptance criteria:
1. Identify which of the above can be rewritten using pure-Python (NumPy/SciPy/etc.) and which require Sage objects.
2. For convertable files: open small PRs that add pure-Python equivalents and unit tests.
3. For Sage-only files: add documentation explaining why Sage is required and add a smoke test to the `sage-verification` workflow that ensures the script runs in the Sage container.

I can start by taking the smallest scripts (combinatorics / numeric checks) and proposing PRs for review.
