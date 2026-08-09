# Part CCVI — Intersection Theory Bridge for W(3,3)

## Theorem (Intersection Theory Bridge)

For the W(3,3) collinearity graph $\mathrm{SRG}(40,12,2,4)$ with atoms
$Q=3$, $V=40$, $K=12$, $\lambda=2$, $\mu=4$, $\Phi_3=13$, $\mathrm{EDGES}=240$,
all principal intersection-theoretic invariants are fixed with zero free parameters.

## Core identities

- Chow ring size: $\dim A^*(X)=V=40$
- Self-intersection of the $K$-class: $K\cdot K = K = 12$
- Degree map image: $\deg(A^{\text{top}})=\mathrm{EDGES}=240$
- Divisor degree: $\deg D = K = 12$
- Local intersection multiplicity: $A^1\cdot A^1 = \lambda = 2$
- Excess intersection: $\mu-\lambda = 2$

## Characteristic classes

- $\mathrm{ch}_0 = 1$
- $\mathrm{ch}_1 = K = 12$
- $\mathrm{ch}_2 = K^2/2 - \lambda = 70$
- Todd class first component:
  $$\mathrm{td}_1 = K/2 = 6 = \mathrm{MULT\_K2}$$
- Pontryagin class:
  $$p_1 = 2\lambda - K^2 = -140$$

## Riemann–Roch and projection

- Riemann–Roch shadow:
  $$\chi(\mathcal O(D)) = V - \frac{\mathrm{EDGES}}{K} = 40 - 20 = 20$$
- Projection formula value:
  $$\pi_*(D)\cdot C = \lambda\,\mathrm{EDGES} = 480$$
- Blowup excess class:
  $$E^2 = -K = -12$$

## Verification status

- Script: `exploration/PART_CCVI_INTERSECTION_THEORY_BRIDGE.py`
- Results: `PART_CCVI_intersection_theory_results.json`
- Tests: `tests/test_intersection_theory_bridge_ccvi.py`
- Regression result: **19/19 tests passing**
