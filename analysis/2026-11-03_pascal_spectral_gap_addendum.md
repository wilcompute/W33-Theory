# 2026-11-03 — Spectral-gap cross-check of exact Pascal transport RG

**Companion to** `analysis/2026-11-03_pascal_w33_transport_scale_audit.md`; the original seven-file certificate is committed at `b2fca22dea122e0ad7059eaf55e37e152e4fb3f1`.

The exact three-terminal electrical reduction yielded `c_(n+1)=c_n(9c_n+7)/(15c_n^2+31c_n+15)`, with resistance multiplier `r=15/7`. If the six-cell self-similar graph admits standard compatible harmonic diffusion, the candidate diffusion-time multiplier is `6r=90/7` per spatial magnification by 3. This calculation tests that forecast against an observable **not used in the circuit proof**: the smallest positive eigenvalue of the unweighted Laplacian.

## Independent numerical data

| Pascal depth n | vertices | first positive Laplacian eigenvalue |
|---:|---:|---:|
| 1 | 6 | 1.697224362268005 |
| 2 | 36 | 0.139531657582319 |
| 3 | 216 | 0.010805280371610 |
| 4 | 1,296 | 0.000836815231248 |
| 5 | 7,776 | 0.000064944893209 |

Consecutive eigenvalue ratios (depth n to n+1): **12.16372, 12.91328, 12.91238, 12.88500**. Exact conditional time multiplier: **90/7 ≈ 12.85714**.

Negative control: perform the **same** eigenvalue computation on the full undeleted triangular lattice, with edge resistance and local hopping rate held fixed. Its first three ratios are **6.29133, 7.94976, 8.63560**, which are approaching ordinary two-dimensional diffusive factor 9 rather than 90/7.

The spectral calculation uses `scipy.sparse.linalg.eigsh`. To avoid accidentally dropping the uniform zero eigenvalue during the Lanczos iterations, it adds the rank-one projector onto the constants, moving the zero eigenvalue to one while leaving all orthogonal modes unchanged. At depth one the complete dense spectrum is used. The scalar spectral gaps are certified numerically; possible degeneracies are **not** certified by the Lanczos output.

## Conditional continuum exponents

Under the standard harmonic and random-walk scaling assumptions for a six-copy self-similar network,

```text
spatial scale    3
mass scale       6
resistance scale 15/7              (exact graph-electrical result)
time scale       6*(15/7)=90/7     (conditional diffusion limit)
walk exponent    ln(90/7)/ln(3)    ≈ 2.3246595251
spectral dim.    2*ln(6)/ln(90/7) ≈ 1.4031558049
```

The finite-size spectral ratios support but do not constitute a theorem of spectral convergence. None of these quantities determines an absolute length, a 4D Lorentzian continuum, or Newton's gravitational constant. No dimensional identification has been inserted into this experiment.

## Reproduce

```powershell
python analysis/2026_11_03_pascal_spectral_gap_scaling.py
```

Output: `data/2026_11_03_pascal_spectral_gap_scaling.json`.

## Prior art

Level-3 Sierpiński gasket resistance factor 15/7 is not new, see https://doi.org/10.1109/ICICES.2013.6508276 and https://doi.org/10.1016/0016-0032(89)90047-1 . This is a project-specific independent spectrum-versus-circuit consistency test for the chosen triangular nearest-neighbor Lucas graph.
