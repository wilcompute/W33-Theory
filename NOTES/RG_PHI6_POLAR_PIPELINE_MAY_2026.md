# RG Phi6-Polar Pipeline Integration — May 2026

**Status:** selected QCD-local RG branch wired as executable adapter  
**Primary file:** `scripts/w33_rg_phi6_polar_pipeline.py`  
**Tests:** `tests/test_rg_phi6_polar_pipeline.py`

---

## Result

Parts CXXXIX--CXLIII reduced the QCD RG/GUT mismatch to a selected finite branch:

\[
k_{3,\rm bare}=\frac{24}{13},
\qquad
\tau_{\rm GUT}=\log\sqrt{\frac{\mu}{\Phi_6}}.
\]

The selected branch is QCD-local because

\[
\beta_0=\Phi_6(3)=7
\]

lives in the negative Hashimoto field

\[
x=-2\pm i\sqrt{\Phi_6}=-2\pm i\sqrt7.
\]

The pipeline implements

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{24/13}
\left(1+\frac{\alpha_{\rm unified}}{2\pi}\log\sqrt{\frac{\mu}{\Phi_6}}\right).
\]

With

\[
\alpha_{\rm unified}=\frac{1}{25},
\qquad
M_{\rm GUT}=\frac{13}{7}\cdot10^{16}\,\mathrm{GeV},
\]

the live two-loop RK4 RG integrator gives

\[
\alpha_s(M_Z)=0.11800503473579949.
\]

Compared with PDG input

\[
\alpha_s(M_Z)=0.1180\pm0.0009,
\]

the residual is

\[
5.03\times10^{-6},
\]

or

\[
0.0056\sigma.
\]

---

## Why this is important

The old baseline `k3=1` was useful as a diagnostic, but it is not the selected W(3,3) QCD branch.  The new adapter keeps the old RG module intact while adding the selected branch as a clean executable surface.

Run:

```bash
python scripts/w33_rg_phi6_polar_pipeline.py
```

Expected headline output:

```text
model                = W33-Phi6-polar
k3_bare              = 1.846153846
tau_GUT              = -0.279807894
delta_GUT            = -0.001781312
k3_eff               = 1.849448291
alpha_s(M_GUT)       = 0.021628072
alpha_s(M_Z)         = 0.118005035
sigma                = 0.0056
```

---

## Regression coverage

`tests/test_rg_phi6_polar_pipeline.py` verifies:

1. \(k_{3,\rm bare}=24/13\),
2. \(\tau_{\rm GUT}=\log\sqrt{\mu/\Phi_6}\),
3. the threshold is negative and sub-percent,
4. \(k_{3,\rm eff}=1.849448291286928\),
5. \(\alpha_s(M_{\rm GUT})\) is finite and physical,
6. the full two-loop run gives \(\alpha_s(M_Z)\) within \(10^{-5}\) of 0.1180,
7. the report carries the selected branch metadata.

Local status:

```text
7 passed in 0.40s
```

---

## Next move

The V42 mass/Yukawa pipeline should switch from the provisional baseline to this selected branch wherever it needs the QCD coupling chain.

The clean integration target is:

```python
from scripts.w33_rg_phi6_polar_pipeline import w33_phi6_polar_alpha_s_mz
```

and then consume `result["alpha_s_mz"]`, `result["alpha_s_gut"]`, and `result["k3_effective"]`.
