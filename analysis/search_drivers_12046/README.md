# Search drivers for Pass 12046 (Claude track)

These scripts produced the records quoted in `analysis/w33_pass12046_geometric_row_closure.py`. Run each from this
folder with `py -3`. The `*.json` files are the run records.

| script | what it does | status |
|---|---|---|
| `torsion.py` | Pins Re w (or all of w) at torsion values, using broad starts. | Converged too rarely; stopped. |
| `curve.py` | Continuation in Re w. | Fails at folds; replaced by `arc.py`. |
| `arc.py` | Pseudo-arclength continuation of the five CP-even targets. Branch A record: J spans [9e-6, J_max], Re w stays in [-0.078, -0.049]. | Used. |
| `recover.py` | Recovers branch coordinates (D, G) from the 12045 catalogue keys. | Used. |
| `scaleC.py` | Follows a branch in the matching scale with the SM running of Codex 12011, under both lepton rules. | Used. |
