# Pass 12628: the sign of the fading coupling decides phantom crossing, line drift and shear together; a sterile-neutrino coupled dark matter fits only near 10 keV; Chat's gauged Z9 sector cannot host it

Claude track. Producer: `analysis/w33_pass12628_sign_of_c_links.py`. Test: `tests/test_w33_pass12628.py`. Scripts in `analysis/toe_uv/`: `weff_turnaround.py`, `sterile_window.py`, `prereg_statements.py` (frozen, sha256 d2624061). The MCMC chain, the joint CPL+DES refit and the shear-held posterior predictive are still running, for Pass 12627.

**Not a theory of everything.**

## 1. Sign of c ⇔ phantom crossing (`weff_turnaround.py`)

The effective w(z) is what an observer assuming uncoupled CDM would infer, computed at the full-data fits:

| fit | w_eff(0) | w_eff(1) | w_eff(2) | crosses −1 | field turnaround |
|---|---:|---:|---:|---|---|
| fading c < 0, Dovekie / DES-SN5YR | −0.89 / −0.86 | −1.02 | −1.09 / −1.12 | **z ≈ 0.80 / 0.84** | z ≈ 1.6 / 1.7 |
| fading c > 0 | −0.92 / −0.88 | −0.93 / −0.91 | −0.85 / −0.82 | **never** | none |
| CPL (control) | −0.81 / −0.76 | −1.15 / −1.16 | −1.27 / −1.29 | z ≈ 0.39 / 0.43 | — |

- **c < 0:** the dark matter drives φ up early. The potential (slope opposite) pulls it back after z ≈ 1.6, so the dark-matter mass m ∝ e^(−c′φ) grows at late times, which an uncoupled-CDM analysis reads as phantom. This is the mechanism of arXiv:2601.05235 ("evolving DM mass mimics phantom"), cited, not claimed.
- **c > 0:** the field rolls one way and never goes phantom.

So one parameter, the sign of c, decides several things at once:

| | c < 0 | c > 0 |
|---|---|---|
| phantom crossing | yes, z ≈ 0.8 | no |
| decay-line drift at z = 0.5 (Pass 12626) | −0.7 to −0.9% | +0.75 to +0.94% |
| DES Y3 shear at fixed background (Pass 12625) | +1.6 | +0.2 |
| full-data χ² (Dovekie) | preferred by 2.0 | — |
| BAO (Pass 12625) | blind | blind |

Current data split almost evenly between the signs (net about 0.7).

## 2. Minimal sterile-neutrino coupled dark matter (`sterile_window.py`)

Setup: a real singlet S with (y/2) S N N, so M_N = y v_S/√2, and freeze-in from S → NN with S thermal (formula from Hall et al. 2010, recalled from memory). Ωh² = 0.12 fixes y. The Higgs portal must lie between a rough thermalisation floor and the clock cap of Pass 12626:

| M_N | m_S | y | v_S | λ_hS window |
|---:|---:|---:|---:|---|
| 7.1 keV | 100 GeV – 3 TeV | 0.7–3.6×10⁻⁸ | 0.3–1.5 TeV | [1–7×10⁻⁷, 3×10⁻⁷ – 8×10⁻⁶]: **open** |
| 15 keV | 3 TeV only | 2.5×10⁻⁸ | 0.86 TeV | [6.5×10⁻⁷, 8.8×10⁻⁷]: marginal |
| 30 keV | any | — | 2.4–13 TeV | **closed** |

- **The corridor is near 10 keV.** Lyman-α bounds on decay-produced sterile neutrinos (roughly M ≳ 10–15 keV, recalled from memory) push from below, and the clock cap pushes from above. The thermalisation criterion is good to a factor of a few, so the edges move by that much.
- XRISM's stacked-cluster limit (arXiv:2510.24560) does not confirm the 3.5 keV line. It is still about 5× above the XMM signal, so a 7 keV line remains allowed but unestablished.

## 3. Chat's flavour-gauged Z9 sector cannot be this dark matter

In Chat's sector (6e0f24d33), N_e^c gets its Majorana mass from S (X = −18), which is the same structure, but N_e^c also carries X = +9:
- Keeping the Z′ from thermalising N_e^c before freeze-in requires g_X < 10⁻¹².
- That makes the Z′ light (10 eV to keV) and electron-coupled at 10⁻¹¹, far above stellar-cooling limits (roughly 10⁻¹⁴ to 10⁻¹⁵, recalled from memory).

So the gauged N_e^c fails as a freeze-in coupled dark matter. It could survive only as a thermal relic diluted afterwards, which I have not checked. The thermalisation criterion is rough.

## 4. Frozen statements (`prereg_statements.json`, sha256 d2624061)

- **S1:** fading predicts cosmic shear better than CPL in the next shear release (DES Y3 at fixed background: 2.99).
- **S2:** w_eff crosses −1 if and only if c < 0, near z ≈ 0.8.
- **S3:** the line-drift amplitudes and signs above.
- **S4:** DR3 BAO alone will not separate fading from CPL by more than 4, or fix the sign of c.

Each statement names the data that score it and what falsifies it. They were written before the Pass 12627 refit results.

## Prior art and sources

The line-drift test was not found in two searches (standard and extended), so no novelty is claimed. Related work: arXiv:2601.05235, 2608.05032 (evolving DM mass and phantom); 2510.24560 (XRISM); 1602.04816 (sterile-neutrino white paper).
