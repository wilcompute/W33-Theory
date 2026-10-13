# TOE64 — Exact signed-square flux decomposition and frustration gain

**Date:** 2026-10-13. **Scientific owner:** finite W33 U(1)^3 spinless-fermion leading high-temperature term. **Not:** dynamical gauge vacuum, all-temperature theorem, device tolerance, CP violation or a solved TOE.

## Why TOE63 is not the endpoint

TOE62 gave a sufficient 14.0585413% independent positive-link disorder tolerance; TOE63 improved it to 14.5687762% with an unsigned 3-by-3 positive-definiteness bound. Both lose structural information because one cross winding is `cos(phi_2-phi_3)`, not `cos(phi_2+phi_3)`. The mixed winding triangle carries a *signed/frustrated* incidence geometry, and signs affect the relevant spectral gap.

Using native TOE59/TOE62 loop census, let the **positive weighted six Fourier amplitudes** be `a=(a1,a2,a3)` and `(d,e,f)` for `cos(phi1+phi2),cos(phi1+phi3),cos(phi2-phi3)`. Under `phi=pi+delta`, define `u_i=1-cos(delta_i)` and `t_i=sin(delta_i)/sqrt(2)`. The exact elementary identity `u_i=t_i^2+u_i^2/2` yields **without approximation**:

```
S_w(pi+delta)-S_w(pi)
= t^T H t
  + (1/2)*sum_i H_ii*u_i^2
  + d*u1*u2 + e*u1*u3 + f*u2*u3,

H = diag(a)
    - d*(e1+e2)(e1+e2)^T
    - e*(e1+e3)(e1+e3)^T
    - f*(e2-e3)(e2-e3)^T.
```

This is an exact global sum of squares plus nonnegative quartic terms, not a local Taylor/Hessian approximation. The sign on `e2-e3` is indispensable.

Let `L=(1-epsilon)^8`, `U=(1+epsilon)^8`. Every positive octagon product is in `[L,U]`, and the native counts are `a>=L*(79,77,77)`, `(d,e,f)<=U*(1,1,3)`. Therefore, in positive-semidefinite (Loewner) order:

```
H >= L*[D-r*M_signed], r=U/L,
D=diag(79,77,77),
M_signed=[[2,1,1],[1,4,-3],[1,-3,4]].
```

Diagonalizing the antisymmetric 2–3 direction gives `77-7r`; the remaining symmetric 2x2 block has determinant `6083-233r` and positive diagonal up to the relevant boundary. Consequently, `D-r*M_signed` is positive semidefinite for `r<=11` and strictly positive definite for `r<11`.

```
epsilon_* = (11^(1/8)-1)/(11^(1/8)+1)
          = 0.14875640159021247...
```

At equality, `H` may have a null direction but every `H_ii>0` (at worst proportional to 57,33,33), so the `(1/2) sum H_ii u_i^2` remainder is strictly positive for every nonzero `delta mod 2pi`. Hence **the unique global minimizer survives even at equality**.

Thus, the theorem certifies arbitrary native edge-amplitude perturbations **through 14.8756402%**, improving TOE62 by approximately 0.8171 percentage points, with no high-beta or continuum claim. The exact sum-of-squares representation reveals how the relative sign of one mixed winding suppresses the worst-case frustrated direction.

## What is and is not sharp

For the larger **artificial independent Fourier-amplitude interval box**, the threshold is optimal for *local* stability: choosing every single-axis coefficient at its allowed minimum and every mixed coefficient at its allowed maximum makes the antisymmetric Hessian negative as soon as `r>11`; an explicit box-allowed counterexample is recorded at epsilon=0.155. Such simultaneous Fourier extremes need **not** be realizable by any single collection of W33 edge-product hoppings. Therefore no optimal physical disorder threshold, phase transition, or loss of W33 minimum above this epsilon is asserted.

The certificate and the 750 randomized coefficient identity checks are implemented in `analysis/w33_20261013_toe64_signed_square_flux_robustness.py` and `tests/test_w33_20261013_toe64_signed_square_flux_robustness.py`. All exact input integers come from the committed native winding census, not parameter fitting.
