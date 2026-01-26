Fixture dataset for TOE smoke/E2E tests

Files:
- `action_candidate_features_fixture.csv` — small canonical action candidate features
- `W33_line_phase_map_fixture.csv` — small canonical phase map for the same line_ids
- `node_commutator_line_scores_fixture.csv` — node commutator predictor scores
- `mixed_predictor_oddness_defect_scores_fixture.csv` — mixed predictor scores
- `e_star_oddness_per_line_fixture.csv` — e* oddness per line

Usage:
- Copy the files into the repo layout expected by scripts for quick smoke runs:
  - `data/_workbench/04_measurement/action_candidate_features.csv`
  - `data/_workbench/02_geometry/W33_line_phase_map.csv`
  - predictor files (optional) into `data/_workbench/04_measurement/`

These fixtures are deterministic and intended for CI smoke tests and local debugging.