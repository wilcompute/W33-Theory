# Passes 3025–3033 claim ledger

| Claim | Type | Evidence | Boundary |
|---|---|---|---|
| 48,826 exact D4 fault hypotheses; 1,436 post-base collision classes | exact finite | `bt3025_3031_common.py` | discrete permutation faults only |
| noisy escalation policy values | exact DP for explicit model | `bt3025_noisy_d4_bayes.py` | base class exact; channels synthetic |
| verified 28-row upper bound | exact finite | `bt3026_27_triangle_sat.py`, inherited PR #231 schedule | does not prove 27 impossible |
| 164,220-clause central-r² obstruction | exact reduction | CNF generator | UNSAT must be proof-checked |
| optimum fixed schedule equals 28 | **pending** | dedicated SAT/proof workflow | not claimable from source alone |
| cyclic block edit-distance obstruction | exact combinatorics | `bt3027_edit_sync_pilot_order.py` | isolated cyclic block |
| pilot-order score 1/2; combined score 3/5 | exact finite construction | same generator | length 12, not asymptotic |
| adaptive posterior core | source-complete RTL | `rtl/w33_pass3028_*` | simulation/synthesis pending |
| 1,436 → 457 initial causal states | exact finite | `bt3029_predictive_causal_states.py` | canonical noiseless action policy, STOP-only leaf |
| 1.078290855-bit predictive reduction | exact under frozen prior | same certificate | logical entropy, not measured heat |
| five-channel D4 Fourier predictor | exact representation theory | `bt3030_d4_fourier_belief_engine.py` | class-invariant convolution only |
| conjugacy sensor retains 99.6683% risk reduction | exact for explicit channel/prior | `bt3031_measurement_basis_portfolio.py` | synthetic moderate profile |
| laboratory D4 likelihoods or edit rates | **not measured** | none | requires one coherent optical stack |
| FPGA area, timing and power | **pending** | focused evidence workflow | do not infer from RTL source |
| three PDFs compile with the overhaul | **pending** | focused evidence workflow | do not merge before observed green evidence |
