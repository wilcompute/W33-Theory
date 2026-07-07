# BT1859 — Quotient Dashboard Ledger Promotion Rows

These rows promote BT1855-BT1858 into the public theorem ledger supplement and clarify the exact state of the quotient ladder.

| Claim | Tier | Witness / command | Output artifact | Pass condition | Boundary |
|---|---:|---|---|---|---|
| Tetracode code-glue stabilizer intersection | E/C | `analysis/bt1855_code_glue_stabilizer_intersection.py`; `analysis/bt940_full_signed_monomial_chain_lift_attempt.py` | `data/PART_BT1855_CODE_GLUE_STABILIZER_INTERSECTION_summary.json`; `data/bt940_full_signed_monomial_chain_lift_attempt.json` | signed monomial glue stabilizer order 48; S4 block quotient order 24; sign kernel size 2 | Exact in tetracode coordinates; sign-kernel chain lift still open. |
| Transport local survivor to H | E/C | `analysis/bt1856_transport_local_survivor_to_H.py`; `analysis/bt959_selected_minimizer_stabilizer_orbit.py` | `data/PART_BT1856_TRANSPORT_LOCAL_SURVIVOR_TO_H_summary.json`; `data/bt959_selected_minimizer_stabilizer_orbit.json` | S4 quotient transports to H; selected minimizer has orbit 24, stabilizer 1, support-60 intersection singleton | Sign-kernel/local-A2 part not transported without explicit integral A2 representative lift. |
| Selector API refactor | E | `analysis/bt1853_runtime_selector_api.py`; `analysis/bt1857_selector_api_refactor_audit.py` | `data/PART_BT1857_SELECTOR_API_REFACTOR_AUDIT_summary.json` | aperture table, trace schema, and shot protocol consume the same canonical selector constants | Source refactor; does not recompute quotient data. |
| Holonet machine patch materialization | C/E | `analysis/bt1851_holonet_machine_selector_merge_patch.py`; `analysis/bt1858_holonet_machine_patch_materialization_plan.py` | `data/PART_BT1858_HOLONET_MACHINE_PATCH_MATERIALIZATION_PLAN_summary.json` | paper patch has anchor, canonical selector, BT959 witness, and local A2 boundary | Plan/patch witness; not a connector-side full paper rewrite or PDF build. |
| Six-stage quotient dashboard | E/C | `analysis/bt1854_quotient_status_dashboard.py` | `data/PART_BT1854_QUOTIENT_STATUS_DASHBOARD_summary.json` | stages recorded: support minimality, certificate graph, vertex metric, tetracode metric, transported S4, local A2/Weyl/glue; exactly one open stage | Dashboard summary; local A2/Weyl/glue remains the only open quotient level. |

## Current quotient status

Closed or effectively closed:

1. support-minimality: support 60 with six minimizers;
2. intrinsic certificate graph: certificate orbits `[[0,1],[2],[3],[4],[5]]`;
3. vertex metric: minimizer 2;
4. tetracode metric: minimizer 2;
5. transported S4 quotient: orbit 24, stabilizer 1, support-60 singleton.

Open:

6. local A2/Weyl/glue chain lift: sign-kernel/local-Weyl part requires an explicit integral A2 representative lift.
