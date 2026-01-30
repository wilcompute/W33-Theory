# Z3 Edge Potential: Greedy Decision Tree

We trained a shallow greedy decision tree (depth <= 3) on simple discrete
features (family ids, mu/nu, basis involvement, support size, omega) to predict
the Z3 edge labels.

## Result
- Accuracy: **0.517** (near random 1/3 baseline, only weak signal)

The tree is large and fragmented, with small gains. This indicates the Z3 edge
labels are **not captured by simple local features** like family index or omega.
The structure is global.

Script: `tools/witting_z3_edge_potential_tree.py`
