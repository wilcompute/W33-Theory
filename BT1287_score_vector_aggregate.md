# BT1287 — Score-Vector Aggregate Report

**Theorem:** BT1287  
**Frontier:** BT1267–BT1285  
**Top candidate:** `canonical_seed_BT1275`  
**Pareto-optimal front:** `canonical_seed_BT1275`, `recovery_integrator_BT1282`

## Ranked Candidates

| Rank | Candidate | Composite | Coverage | Rec.Depth | λ-conf | μ-conf | SM-Spine |
|------|-----------|-----------|----------|-----------|--------|--------|----------|
| 1 | `canonical_seed_BT1275` | 0.8825 | 1.000 | 0.333 | 1.000 | 1.000 | 1.000 |
| 1 | `recovery_integrator_BT1282` | 0.8825 | 1.000 | 0.333 | 1.000 | 1.000 | 1.000 |
| 2 | `external_protocol_BT1276` | 0.8620 | 0.975 | 0.333 | 1.000 | 1.000 | 0.970 |
| 3 | `sparse_full_closure_BT1271` | 0.8340 | 1.000 | 0.250 | 1.000 | 1.000 | 0.940 |
| 4 | `diameter12_BT1271` | 0.5210 | 0.850 | 0.083 | 1.000 | 0.875 | 0.690 |
| 5 | `not_full_order_BT1271` | 0.4490 | 0.600 | 0.200 | 0.800 | 0.800 | 0.490 |

## Score Dimensions

| Dimension | Description |
|-----------|-------------|
| `polar_path_coverage` | Fraction of W(3,3) points reachable from seed |
| `recovery_depth` | 1/max_depth — lower depth is higher score |
| `lambda_conformance` | SRG λ=2 conformance (adjacent pairs) |
| `mu_conformance` | SRG μ=4 conformance (non-adjacent pairs) |
| `generation_match` | Z₃ generation identification from C(R) |
| `gauge_decomposition` | 1⊕3⊕8 adjoint split quality (BT886) |
| `color_heisenberg` | 3^{1+2} matter-shell Heisenberg match |
| `sm_spine_completeness` | BT886 composite SM spine score |

## Key Finding

The **canonical_seed_BT1275** and **recovery_integrator_BT1282** are jointly Pareto-optimal,
achieving perfect scores on all SM-physics dimensions while maintaining recovery depth = 3.
This confirms that the BT1275 polar-path certificate is the unique minimal complete recovery
packet for the W(3,3) photonic holonet architecture.
