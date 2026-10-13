# TOE63 — Strictly stronger global continuous-flux robustness certificate

**Date:** 2026-10-13. **Scope:** native finite W33 flat U(1)^3 spinless free-fermion hopping problem. This is not a claim of a physical Theory of Everything.

## Source dependency and checked novelty

TOE62's committed recovery source `analysis/w33_20261013_toe62_global_flat_flux_proof.py` regenerates exactly 238 nonzero-winding octagons from `data/w33_20261013_toe59_eight_cycle_census.json`. Its six Fourier counts are single axes (79,77,77) and mixed axes (1,1,3). The local original TOE62 seven-producer script `analysis/w33_20261013_toe62_weighted_flux_robustness.py` used a diagonal cosine estimate and certified a 14.0585% sufficient positive-link-amplitude tolerance. This note strengthens that *sufficient analytic bound* without changing the Hamiltonian.

## Spectral bound

Write `delta=phi-(pi,pi,pi)` and `u_i=sqrt(1-cos(delta_i)) >= 0`. For all real x,y,

```
1-cos(x+y) <= (sqrt(1-cos x)+sqrt(1-cos y))^2,
1-cos(x-y) <= (sqrt(1-cos x)+sqrt(1-cos y))^2.
```

Indeed, `sqrt(2)|sin((x+-y)/2)| <= sqrt(2)(|sin(x/2)|+|sin(y/2)|)`. Positivity of every hopping magnitude makes all weighted loop contributions positive. Every winding length-eight loop acquires a weight between `L=(1-e)^8` and `U=(1+e)^8`. Thus, for arbitrary **independent** link magnitudes in `[1-e,1+e]`,

```
S_w(phi)-S_w(pi,pi,pi) >= u^T [ L*D - U*M ] u,
D=diag(79,77,77),
M=[[2,1,1],[1,4,3],[1,3,4]].
```

Here the mixed loop counts (1,1,3) define `M=sum c_ij(e_i+e_j)(e_i+e_j)^T`; the sign of the `delta_2-delta_3` term is immaterial to the rigorous upper bound.

Let `r=U/L=((1+e)/(1-e))^8`. In the antisymmetric (2,3) channel, `D-rM` has eigenvalue `77-r`. On the symmetric two-dimensional channel the matrix is

```
[[79-2r, -sqrt(2)r],[-sqrt(2)r, 77-7r]]
```

with determinant `6083-707r+12r^2`. The first loss of positive definiteness occurs exactly at

```
r_* = (707-sqrt(207865))/24 = 10.461577396829...
e_* = (r_*^(1/8)-1)/(r_*^(1/8)+1) = 0.145687762158...
```

For `0 <= e < e_*`, the matrix is strictly positive definite. Hence the leading finite-model beta^7 free-energy holonomy term uniquely minimizes at three-pi, modulo 2pi, throughout the full continuous flat U(1)^3 torus, for **every** allowed selection of independent positive edge hopping magnitudes. The prior bound was `e<0.140585412966...`: the sufficient certified range expands by about **0.510 percentage points**.

This matrix criterion is only sufficient and not asserted to be optimal. No all-beta free-energy comparison follows, no dynamical gauge field is integrated, no CP-odd physical order parameter is computed, and no device manufacturing tolerance is inferred.

## Reproducibility

Run `python analysis/w33_20261013_toe63_spectral_flux_disorder.py`, which rebuilds counts from the native census, evaluates the algebraic threshold and positivity gaps, and writes `data/w33_20261013_toe63_spectral_flux_disorder.json`. Execute `python -m pytest -q tests/test_w33_20261013_toe63_spectral_flux_disorder.py`. Tests include 600 random choices of six independent positive Fourier amplitudes across the entire octagon-product intervals (a superset of amplitudes realizable by native edge disorder). The algebraic proof, not these samples, establishes the theorem.
