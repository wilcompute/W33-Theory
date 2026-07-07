# BT1865-BT1869 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Integral representative equivalence classes | E/C | `analysis/bt1865_integral_representative_equivalence_classes.py` | `data/PART_BT1865_INTEGRAL_REPRESENTATIVE_EQUIVALENCE_CLASSES_summary.json` | `O(A2)` order 12, `W(A2)` order 6, `-I` preserves Gram and lies outside plain Weyl subgroup | Classifies lattice representatives; not a physical E8 chain lift. |
| Phase-action invariant | E/C | `analysis/bt1866_phase_action_invariant.py` | `data/PART_BT1866_PHASE_ACTION_INVARIANT_summary.json` | identity bit 0, central-inversion bit 1, support mask blind to both | Bookkeeping invariant; does not decide physical equivalence. |
| Canonical lift criterion | C/E | `analysis/bt1867_canonical_lift_criterion.py` | `data/PART_BT1867_CANONICAL_LIFT_CRITERION_summary.json` | neutral representative `I`; nontrivial representative `-I`; both height 1 | Canonical as lattice bookkeeping only. |
| Refined dashboard replacement | E/C | `analysis/bt1854_quotient_status_dashboard.py`; `analysis/bt1862_quotient_dashboard_refinement.py` | `data/PART_BT1854_QUOTIENT_STATUS_DASHBOARD_results.json`; `data/PART_BT1862_QUOTIENT_DASHBOARD_REFINEMENT_summary.json` | nine stages recorded; only open stage is integral A2 representative chain lift | Dashboard summary only. |
| Merged selector/glue subsection | C/E | `paper/BT1869_selector_glue_merged_subsection.tex` | `data/PART_BT1869_SELECTOR_GLUE_MERGED_SUBSECTION_summary.json` | combines canonical selector, `48 = 2 x 24` glue split, phase-coset bit, and final boundary | Insert-ready subsection; not a rebuilt PDF. |

## Current final boundary

Everything visible on the mod-2 support shadow is closed. The only remaining open layer is choosing/proving a canonical integral A2 representative chain-complex lift for the central-inversion phase action inside a concrete E8 representative model.
