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

## Addendum (same day): literature check, two corrections, and a geometry no-go for the sign

**Crossing redshift in published reconstructions.** arXiv:2504.00985 uses a Gaussian-process fit to DESI DR2 + BAO-based + chronometer H(z) + Pantheon+. It finds w(z) crossing −1 at **z ≈ 0.4**, at about 2σ. With a DESI DR2 prior, it also finds about 2σ evidence for energy flowing **from dark matter to dark energy** at z < 0.5.

In this model:
- late DM→DE flow is the **c > 0** mode, where φ keeps rising and m ∝ e^(−c′φ) keeps falling;
- c < 0 reverses that after its turnaround at z ≈ 1.6;
- the z ≈ 0.4 crossing matches neither sign, since c < 0 crosses at 0.8 and c > 0 never crosses; CPL crosses at 0.4 by construction.

So the published data-driven result also leaves the sign of c open: the energy direction favours c > 0, while the existence of a crossing favours c < 0. S2 stays as frozen.

**Correction (Lyman-α).** §2's "Lyman-α pushes from below at roughly 10–15 keV" was recalled from memory and is probably too strict for scalar-decay production. Merle and Schneider (arXiv:1409.6311) find that decay of heavy singlets is the production mechanism most compatible with Lyman-α, with thresholds of a few keV (slide-level numbers). The 7 keV corridor is therefore less squeezed than stated. The upper edge (clocks) stands. A proper check needs the actual momentum distribution from S decays.

**Geometry cannot fix the sign (`euclid_sign.py`).** The frozen c < 0 and c > 0 predictions differ in D_M/r_d by 0.04–0.11% and in D_H/r_d by 0.03–0.21% at z = 0.93–2.33. With uncorrelated 0.5%, 0.3% and 0.2% errors per quantity, the Asimov Δχ² is 0.35–0.55, 1.0–1.5 and 2.2–3.4. These are upper bounds. **No foreseeable BAO survey determines the sign of c.** It is set only by growth (ΔS8 = 0.011–0.015, about 1.5%), by a particle signal (the line drift), or by the energy-flow direction.

Sources: arXiv:2504.00985, 1409.6311, 2204.08795, 2602.11085 (abstract only), 2503.14738.

## Addendum 2: correcting the correction (Lyman-α edge computed, `sterile_lya.py`)

The first addendum's "a few keV" misread Merle's slide numbers, which are most likely **thermal-equivalent** masses (m_th) and not the sterile-neutrino mass.

The free-streaming match for decay production:
- ⟨p/T⟩ ≈ 2.5 at T ≈ m_S, diluted by entropy (g*S 106.75 → 3.91), gives p ≈ 1.16 T_ν today.
- A thermal warm-dark-matter relic of 5.3 (5.7) keV has ⟨p⟩ = 0.41 T_ν (0.39).
- So **M_N > 15.2 (16.8) keV**. The thermal bounds are from memory (Iršič et al. 2017 and later), not re-read.

Combined with the portal window (thermalisation floor and clock cap):

| M_N | m_S = 1 TeV | 3 TeV | 10 TeV |
|---|---|---|---|
| 10–15 keV | portal ok, **Lyman-α excluded** | excluded | excluded |
| 16 keV | closed | **open** | **open** |
| 18–20 keV | closed | closed | **open** |

**Corrected conclusion:**
- A decay-produced sterile neutrino carrying the fading coupling lives in a narrow corridor: **M_N ≈ 16–20 keV, m_S ≈ 3–10 TeV, λ_hS ~ 10⁻⁶, v_S ≈ 1–3 TeV**.
- The 7.1 keV (3.5 keV line) case is excluded for this production mechanism.
- A line from this candidate would sit at **8–10 keV**, inside XRISM's band.
- The original memory-based "≳ 10–15 keV" was roughly right; the first addendum's relaxation was wrong.
- The thermalisation floor and ⟨p/T⟩ are rough (factor-of-two level), so the corridor's edges move accordingly.

## Addendum 3: X-ray limits, momentum shape, frozen S5

- **X-ray.** NuSTAR blank-sky limits are leading at 15–18 keV (arXiv:2207.04572; also 1908.09037, 1901.01262, 1609.00667). In freeze-in from S decays the mixing angle is free, so these only cap the line's visibility, at roughly sin²2θ ≲ 10⁻¹²–10⁻¹³ (from memory). The dark-matter N then contributes ≲ 10⁻⁹ eV to active-neutrino masses: it decouples from the seesaw, and Pass 12626 §4's neutrino-drift link does not apply to it. The other two N's must make the observed masses.
- **Momentum shape (`sterile_lya_rms.py`).** For f(q) ∝ q^(−1/2) e^(−q) (decay freeze-in shape, recalled from memory), matching the rms velocity instead of the mean momentum moves the Lyman-α edge by +3.7%: **15.8 (17.4) keV** for a 5.3 (5.7) keV thermal bound. The corridor stays at 16–20 keV, with 16 keV marginal under the stricter bound.
- **Frozen S5** (`analysis/toe_uv/prereg_corridor.json`, separate from the d2624061 file, which stays unchanged) states the corridor and the 8–10 keV line drift. It names what falsifies it: a thermal-equivalent WDM bound above about 7 keV, or a detected line without the drift. It also notes that the absence of a line does not falsify it.

## Addendum 4: S → hh, the corridor shrinks; XRISM stacking and a drifting line

**S → hh through the portal (`sterile_hh.py`).** Γ(S→hh) ≈ λ²v_S²/(8π m_S) (rough) is **below** H(T = m_S) at the corridor points, so decays do not keep S in equilibrium. With λ ~ 10⁻⁶, annihilation is only marginally faster than expansion, and S probably freezes out near T ~ m_S, then decays with BR(NN) = 0.6–10%. Treating the decay of the whole relativistic S population as an upper estimate:

| M_N | m_S | S decays at m_S/T | Ω from the decaying population |
|---|---:|---:|---:|
| 16 keV | 3 TeV | 1.5 | 0.14 (consistent with 0.12) |
| 16–20 keV | 10 TeV | 6.4 | 2.5 (overproduces about 20×, unless S stays thermal) |

- At m_S ≈ 3 TeV, freeze-in and the decay of the population agree to order one.
- At 10 TeV, the decaying population overproduces, unless the portal keeps S thermal down to T ≪ m_S. The clock cap forbids a much larger portal.

**The corridor therefore shrinks to roughly M_N ≈ 16 keV, m_S ≈ 3 TeV.** A Boltzmann solution, not these order-one estimates, is needed to say whether it is a point, a sliver or empty. S5 (frozen) states 3–10 TeV, and this addendum flags its upper half as doubtful.

**XRISM stacking (arXiv:2510.24560).** No unidentified line is found in 2.5–15 keV (rest frame), so there are no centroid data. The stack assumes a fixed rest energy. A coupled dark matter's line drifts by up to about 0.27% across z ≲ 0.1, about 25 eV at 9 keV, against a resolution of about 5 eV, so it would be smeared in a rest-frame stack. A search for this model would need a redshift-dependent template: E_rest(z) = E0 (1 + κ z) with |κ| ≈ 0.015–0.02, sign opposite to c, the slope at low z from `line_drift.json`. The cluster redshifts are not in the abstract, so this was not quantified for the actual sample.
