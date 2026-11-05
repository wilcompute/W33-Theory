# Pass 12623: DESI's pull on n_s is 1.7σ under ΛCDM and 0.1σ when w crosses −1

Claude track. Continues Pass 12621 §3, which gave point shifts only. Script: `analysis/toe_uv/ns_fisher.py`, run in WSL with the patched CLASS. Producer: `analysis/w33_pass12623_ns_fisher.py`. Test: `tests/test_w33_pass12623.py`.

**Method.** I take the lowest-training neutral holdout fits on Dovekie from Pass 12597. For each, σ(n_s) comes from the inverse Fisher matrix of the training residuals, marginalised over all other free parameters. The fits are trained either with BAO (SN held out) or without BAO (BAO held out). The likelihood is plik-lite + τ prior + ACT DR6 lensing + fσ8 + the other probe. It does **not** include ACT DR6 primary spectra, which are not available here.

| model | n_s with BAO | n_s without BAO | shift | shift / σ(no BAO) | (with BAO − 0.965)/σ |
|---|---:|---:|---:|---:|---:|
| ΛCDM (control) | 0.9708 ± 0.0032 | 0.9642 ± 0.0038 | +0.0066 | **1.73** | 1.79 |
| exponential (thawing) | 0.9709 ± 0.0034 | 0.9655 ± 0.0039 | +0.0055 | 1.39 | 1.75 |
| CPL | 0.9664 ± 0.0036 | 0.9660 ± 0.0039 | +0.0004 | **0.11** | 0.40 |
| fading coupling | 0.9656 ± 0.0037 | 0.9652 ± 0.0043 | +0.0005 | **0.11** | 0.17 |

**Reading.**
- **[N]** Without BAO, all four models agree on n_s ≈ 0.965 to within 0.0018.
- Adding BAO pulls ΛCDM and the thawing exponential up by 1.4 to 1.7σ.
- It leaves CPL and fading unmoved: their shift is 0.1σ.
- So with BAO in, Higgs, Starobinsky or SMASH-type n_s ≈ 0.965 sits 1.8σ low under ΛCDM. Under the two models that can cross w = −1 it sits within 0.4σ.

**Not the zero it might look like.** The vanishing shift for CPL and fading comes from the same pipeline that measures a 1.7σ shift for ΛCDM, which is the non-vacuous control. The mechanism is that the BAO–CMB tension is absorbed by w(z) instead of by n_s, as described in arXiv:2512.05108.

**Limits.**
- Fisher widths at best fits, not MCMC.
- The two training sets share the CMB, so the ratio is an indicator, not a proper difference test.
- plik-lite understates the published ACT-driven tension (n_s = 0.9743 ± 0.0034 for P+ACT+DESI).
- Dovekie only.
- Novelty is not claimed. arXiv:2507.12459 reports n_s only under ΛCDM. It says evolving dark energy accommodates CMB and BAO together and refers to SPT-3G D1 (arXiv:2506.20707), Table VII, for extended-model fits. I have not read that table. The n_s value under w₀wₐ is probably already there, so treat this pass as an in-house replication with a fading-coupling column added.
