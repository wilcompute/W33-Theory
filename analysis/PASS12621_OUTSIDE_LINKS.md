# Pass 12621: three cross-sector links from the axion-unification candidates

Claude track. Continues `PASS12616_12620_FIVE_ITEMS.md`. Producer: `analysis/w33_pass12621_outside_links.py`. Test: `tests/test_w33_pass12621.py`.

**Not a theory of everything.** Three cheap tests that connect the particle candidates with cosmology.

## 1. The trinification axion against DMRadio-m³

`trin_window.py`. Trinification with three vectorlike (3,3̄,1) (Pass 12616) has E/N = 8/3, the DFSZ coupling, and f ≳ 7×10¹² GeV from σ stability. As a pre-inflation axion with misalignment:

| m_a (μeV) | f_a (GeV) | θ for all of DM | DMRadio-m³ DFSZ reach | H_I bound (GeV) |
|---:|---:|---:|---|---:|
| 0.8 | 7×10¹² | 0.30 | yes | ≲ 2×10⁷ |
| 0.3 | 1.9×10¹³ | 0.17 | yes | ≲ 3×10⁷ |
| 0.12 | 4.8×10¹³ | 0.10 | yes, edge | ≲ 5×10⁷ |
| 0.05 | 1.1×10¹⁴ | 0.06 | no | ≲ 7×10⁷ |

DMRadio-m³ targets DFSZ above about 120 neV in a 5-year scan, as the search tool summarised arXiv:2204.13781; I did not read the paper. So it would test this variant for θ ≈ 0.1 to 0.3. The isocurvature bound H_I ≲ 10⁻⁵ θ f is an order-of-magnitude recollection. It implies low-scale inflation and no observable primordial gravitational waves.

## 2. The PQ quarks do not stabilise the Higgs on their own

`pq_higgs_selfstab.py`. Extra coloured states make b₃ less negative, so y_t falls faster and λ is pushed up. Only the difference from the SM is computed at one loop, and it is added to a baseline crossing zero at 2.7×10¹⁰ GeV (Pass 12612), an approximation to the NNLO curve. **Control:** no new states gives zero shift.

| Model | y_t(M_P) | min λ |
|---|---:|---:|
| SM | 0.414 | −0.0154 |
| Model A, M_X = 2.7×10¹⁰ | 0.393 | −0.0115 |
| trinification ×3 | 0.386 | −0.0117 |
| Model A, M_X = 10⁹ | 0.382 | −0.0090 |

The minimum is 25 to 40 percent shallower, but λ stays negative. **The σ threshold mechanism remains necessary**, and with it the axion-mass ceiling of Pass 12612.

## 3. Evolving dark energy removes DESI's upward pull on n_s

`ns_by_model.py`, from existing fits with no new runs. McDonough and Ferreira, arXiv:2512.05108 (abstract read), show that adding DESI BAO pushes n_s up through the BAO–CMB tension, which puts Higgs and Starobinsky inflation (n_s ≈ 0.965) under about 2σ pressure with Planck + ACT + DESI (0.9743 ± 0.0034, per the papers the search tool returned).

In my fits (plik-lite, τ prior, not ACT):

| n_s | ΛCDM | exponential | CPL | fading |
|---|---:|---:|---:|---:|
| full fit, Dovekie | 0.9702 | | 0.9671 | 0.9657 |
| full fit, DES-SN5YR | 0.9700 | | 0.9671 | 0.9654 |
| trained without BAO | 0.9642 | 0.9655 | 0.9660 | 0.9652 |
| **shift from adding BAO** | **+0.0066** | **+0.0055** | **+0.0004** | **+0.0005** |

**[N]** The pull vanishes for the two models whose effective w can cross −1 (CPL, fading), but not for the thawing exponential. These are also two of the three models that win out of sample (Pass 12620). So whether Higgs, Starobinsky or SMASH-type inflation is under pressure depends on how the late universe is modelled. Model A with Higgs-portal inflation would fit n_s ≈ 0.966 under those models.

Limits: plik-lite, not ACT, where the shift is largest; the τ coupling stressed in arXiv:2512.05108 is not separately examined; point fits, not posteriors. The underlying mechanism is theirs; the per-model split is what this pass adds, and I have not searched DESI's own w₀wₐ papers for it, so **no novelty is claimed**.

## Sources

arXiv:2204.13781, 2512.05108, 2510.18656, 2607.04504, 2606.24131, 1307.3536.
