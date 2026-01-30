# Z3 Edge Potential: Affine/Quadratic Fit Attempt

We attempted to fit the Z3 edge labels (mod 3) as **affine** or **quadratic**
functions of the family parameters (mu, nu) for each family pair separately.

Model features:
- Affine: `[mu_i, nu_i, mu_j, nu_j, 1]`
- Quadratic: all degree <= 2 monomials in (mu_i, nu_i, mu_j, nu_j)

## Result
For **every** family pair (including B–F and F–F blocks), **no exact fit exists**
for either affine or quadratic models.

This rules out any low-degree closed form in (mu, nu) even when restricting to
fixed family pairs, and suggests the Z3 edge potential is governed by a more
global constraint than per-family algebraic rules.

Script: `tools/witting_z3_edge_potential_fit.py`
Output: `docs/witting_z3_edge_potential_fit.txt`
