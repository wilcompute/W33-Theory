# Heawood Physics Report

## Executive summary

This report collects the computational and analytic evidence that the Heawood (torus) incidence Laplacian provides an exact finite Clifford packet decomposition and a closed-form spiral ratio governing the mid-shell spectral split.

Key claims and evidence:

- The Heawood Laplacian spectrum is:
  - $0$ (multiplicity 1),
  - $3 - \sqrt{2}$ (multiplicity 6),
  - $3 + \sqrt{2}$ (multiplicity 6),
  - $6$ (multiplicity 1)
- The mid-shell satisfies the polynomial $x^2 - 6x + 7 = 0$, whose roots are $3 \pm \sqrt{2}$.
- The ratio of the high/low mid-shell eigenvalues is

  $$R = \frac{3 + \sqrt{2}}{3 - \sqrt{2}} = \frac{11 + 6\sqrt{2}}{7} \approx 2.7836116248912246$$

  and is exactly represented in `heawood_spiral_closedform.json`.

- Removing the constant and bipartite sign modes and normalizing the mid-shell by $\sqrt{2}$ yields an involution operator on the 12D mid-shell. The projector

  $$P_{mid} = \frac{1}{2} (I + H_{mid})$$

  (constructed in `heawood_projector_clifford.py`) is idempotent in the mid-subspace and has trace $6$ (rank 6) to numerical precision.

- The 48 Fano 7-cycle automorphisms lift to valid Heawood automorphisms; their action on the mid-subspace yields unitary rotations whose phase statistics are reported in `heawood_spiral_closedform.json` (mean-of-means approximately zero, indicating no net global rotation direction across the family).


## Files and scripts

- `heawood_from_fano_7cycles.py` — enumerates and maps Fano collineations to Heawood automorphisms.
- `heawood_fano7_tetra_alignment.py` — compares tetrahedral oscillator to 7-cycle action.
- `heawood_projector_clifford.py` — constructs the centered operator, isolates the mid-shell, normalizes, and builds `P_mid` to verify idempotency and rank.
- `heawood_spiral_closedform.py` — produces `heawood_spiral_closedform.json` including exact closed-form ratio and 7-cycle phase statistics.
- `tetrahedral_harmonic_crack_summary.py` — aggregated numerical summary.


## Reproducibility

Run these commands from the repository root (Windows PowerShell shown):

```powershell
& ".\.venv\Scripts\Activate.ps1"  # activate your venv
python heawood_spiral_closedform.py
python heawood_projector_clifford.py
python heawood_from_fano_7cycles.py
python heawood_fano7_tetra_alignment.py
python tetrahedral_harmonic_crack_summary.py
```

Dependencies: `numpy`, `networkx` (the repo already includes `requirements.txt`).


## Interpretation & physics narrative

- The mid-shell (12 real modes) is precisely the finite realization of a Clifford-like packet `Cl(1,1)` which, when complexified, becomes a canonical 6-dimensional complex gauge packet. This is a natural place to host a gauge fiber or internal symmetry degrees of freedom.

- The algebraic split $F + T = 9I$ (with $F = 2I + J$ the Fano selector and $T = 7I - J$ the toroidal selector) normalizes to the natural vacuum unit via division by 9, connecting discrete finite geometry selectors to continuum gauge normalization.

- The closed-form spectral ratio $R$ is not numerically equal to the golden ratio; instead it is an exact algebraic expression built from the Heawood roots $3 \pm \sqrt{2}$. This suggests a `√2`-dominated structural scaling (silver-family flavor), while the permutation/phase statistics hint at neutral average rotational phase across the 7-cycle family.


## Suggested next analytic pushes

- Use `P_{mid}` to explicitly construct complex basis vectors and test if familiar gauge algebra representations (e.g. `su(3)`, `su(2)`) can be embedded inside the 6D complex packet.
- Explore continuous deformations: form family `H(\alpha) = O + \alpha P_mid` (where `O` is the tetra operator) and track spectral bifurcations.
- Produce figures: eigenvalue histograms, phase rose plots for 7-cycle action, and projector spectral decomposition.


## Closing

This report packages the mathematical facts, the code provenance, and the exact closed-form arithmetic you requested. If you'd like, I can now (a) render this into a PDF via `pandoc`/`wkhtmltopdf`, (b) produce the suggested figures, and (c) attempt explicit gauge embedding tests inside the `P_mid` complex packet.
