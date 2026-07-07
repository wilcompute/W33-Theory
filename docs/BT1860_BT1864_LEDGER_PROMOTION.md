# BT1860-BT1864 — Ledger Promotion Rows

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Integral A2 representative lift candidate | C/E | `analysis/bt1860_integral_a2_representative_lift.py` | `data/PART_BT1860_INTEGRAL_A2_REPRESENTATIVE_LIFT_summary.json` | four-plane long Weyl element preserves the A2 Gram form and reduces to identity mod 2 | Candidate in tetracode metric coordinates; not a canonical chain-complex lift. |
| Sign-kernel action on winner 2 | E/C | `analysis/bt1861_sign_kernel_action_on_winner2.py` | `data/PART_BT1861_SIGN_KERNEL_ACTION_ON_WINNER2_summary.json` | winner-2 support mask fixed at H level | Integral E8 sign/phase action remains open. |
| Refined quotient dashboard | E/C | `analysis/bt1862_quotient_dashboard_refinement.py` | `data/PART_BT1862_QUOTIENT_DASHBOARD_REFINEMENT_summary.json` | glue stabilizer closed, S4 transport closed, sign-kernel support fixed, integral chain lift open | Dashboard summary; final lift still open. |
| Selector API routed into compression/trace layer | E | `analysis/bt1847_shot_protocol_compression.py`; `analysis/bt1863_trace_runner_selector_api_overlay.py` | `data/PART_BT1863_TRACE_RUNNER_SELECTOR_API_OVERLAY_summary.json` | shot compression imports BT1853; trace runner has BT1853 overlay | BT1848 direct replacement skipped in connector pass. |
| Tetracode glue stabilizer paper insert | C/E | `paper/BT1864_tetracode_glue_stabilizer_upgrade_insert.tex` | TeX insert | states 48 = 2 x 24 split, S4 transported, sign-kernel lift open | Insert, not full rebuilt paper/PDF. |

## Current last open problem

Construct a canonical integral A2 representative chain lift for the sign-kernel/local-Weyl action. Everything else in the selector quotient ladder is now closed or support-mask closed.
