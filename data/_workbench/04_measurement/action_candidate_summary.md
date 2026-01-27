# Action candidate (geometry-only) vs native flux sensors

Features:
- var_q_r: Q12 variance (low is better)
- var_q_class: Q12 variance label
- k12_entropy: entropy of k mod 12 phases
- k12_kl_global: KL divergence from global k mod 12 distribution
- tau_shift_similarity: self-similarity under k12 shift=2 (lower is better)

Candidate score (prior):
- score = -z(var_q_r) - z(k12_entropy) + z(k12_kl_global) - z(tau_shift_similarity)

Fitted score (least squares, standardized features):
- intercept: 3.058705
- weights: var_q=-1.185027, k12_entropy=-1.421878, k12_kl=-1.702543, tau_shift=-1.209396

Evaluation (native mean_abs_delta):
- spearman_prior: 0.1131
- spearman_fit: 0.3615
- top10 overlap prior: 3
- top10 overlap fit: 6

Outputs:
- `data/_workbench/04_measurement/action_candidate_features.csv`
