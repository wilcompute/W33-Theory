# What Passes 12620–12628 establish (Claude track, 2026-11-05/06)

A short reading guide to one line of work: is there evidence for evolving dark energy, which model, and what could carry it in particle physics? **Not a theory of everything.** Each claim cites its pass, and all numbers come from committed JSON certificates.

## Data (cosmology)

1. **Evolving dark energy beats ΛCDM out of sample on two supernova compilations** (Passes 12620, 12622, 12626; prior-truncated posterior predictive):

   | elpd gain over ΛCDM | fading c < 0 | CPL | exponential |
   |---|---:|---:|---:|
   | Dovekie | +5.7 | +5.5 | +3.5 |
   | DES-SN5YR | +7.2 | +9.5 | +6.0 |

   The ordering among models is not stable across compilations, so there is no evidence for the fading coupling over evolving dark energy in general. The DESI-era preference itself is published; the out-of-sample check is what this adds.
2. **DESI's upward pull on n_s depends on the dark-energy model** (Pass 12623): 1.7σ under ΛCDM, 0.1σ under CPL or fading. So whether Higgs or Starobinsky inflation is "under pressure" depends on late-time modelling. Replication of a mechanism in arXiv:2512.05108; it agrees with SPT-3G D1's ΛCDM shift.
3. **DES Y3 shear at fixed background** penalises CPL by 4.6 against 0.2–1.6 for fading (Pass 12625 addendum). That makes shear the candidate probe to split them. A joint refit is pending (Pass 12627).
4. **BAO cannot separate fading from CPL, or fix the sign of the coupling, at any foreseeable precision** (Passes 12625, 12628). Δχ² ≤ 4 at DESI DR3 depth, and ≤ 3.4 between the two signs even at 0.2% per bin.

## The sign of the coupling c is one switch for several observables (Pass 12628)

| | c < 0 | c > 0 |
|---|---|---|
| field history | turns around at z ≈ 1.6 | monotone |
| effective w (uncoupled-CDM reading) | crosses −1 at z ≈ 0.8 | never phantom |
| DM mass today | growing | fading |
| DM→DE energy flow at z < 0.5 | reversed | yes (favoured by arXiv:2504.00985) |
| decay-line rest-energy drift at z = 0.5 | −0.7 to −0.9% | +0.75 to +0.94% |
| S8 | 0.833–0.837 | 0.822 |
| current data | full data prefer it by 2.0 | shear prefers it by 1.35 |

The sign is undetermined today. A direct two-dimensional integral is running (Pass 12627).

## Particle physics: what can carry the coupling (Passes 12625, 12626, 12628)

- **Not a PQ axion.** Coupling through Λ_QCD or the Higgs vev fails Cassini by 100–1000× and atomic clocks by about 10⁴×. Coupling through f_a leaks through the Higgs portal and needs λ < 7×10⁻²³, while the Higgs-stability threshold needs about 0.1.
- **Not a radion on an SM brane** (Passes 12593–12602, earlier).
- **A sterile neutrino** whose mass comes from a singlet vev of about 1 TeV can carry it. After Lyman-α (computed edge 15.8–17.4 keV) and the S → hh and late-decay estimate, the corridor is about **M ≈ 16 keV, m_S ≈ 3 TeV, portal about 10⁻⁶**. That is order-of-magnitude only and needs a Boltzmann solution. Its line would sit at about 8 keV and drift with source redshift.
- **Chat's gauged Z9 N_e^c fails as freeze-in dark matter** (g_X < 10⁻¹² is forced). See `HANDOFF_CLAUDE_TO_CHAT_20261106.md`.

## Axion/unification side (Passes 12621, 12624)

- Unification does not select three trinification copies: 2 to 5 all unify at M_U ≈ 3.5×10¹⁶ GeV.
- On the orbifold with small brane terms, the axion is heavy (≳ TeV to be BBN-safe) and not the dark matter.
- PQ quarks soften but do not cure Higgs instability.

## Frozen, falsifiable statements (in `analysis/toe_uv/`)

- `class_prereg_dovekie.json` (sha 186786a8): cosmological predictions.
- `dr3_prereg.json` (6d76b63b): DESI DR3 BAO.
- `growth_prereg.json` (bd407618): S8 and fσ8.
- `prereg_statements.json` (d2624061), S1–S4:
  - S1: shear prefers fading over CPL;
  - S2: phantom crossing if and only if c < 0;
  - S3: line-drift signs;
  - S4: DR3 BAO will not split the models.
- `prereg_corridor.json` (b5aa8d4b), S5: the sterile-neutrino corridor. Its 3–10 TeV range is flagged in Pass 12628 addendum 4.

## Corrections made along the way (all recorded in the passes)

- The point-estimate cross-validation lead for fading was retracted (Pass 12620).
- The c′ band from an inflation prior was an over-read (Pass 12624 addendum).
- "Within 2.3 elpd" became a spread of 3.5 (Pass 12626).
- The Lyman-α edge was relaxed wrongly and then recomputed (Pass 12628 addenda 1–2).
- SPT was not, after all, prior art for the n_s number (Pass 12623 addendum).

## Open, in order of leverage

1. The joint CPL + shear refit and the shear-held test (S1 against DES Y3).
2. P(c > 0) from the grid.
3. A Boltzmann solution for the sterile-neutrino corridor.
4. A redshift-dependent template for X-ray line searches.
5. The next shear release (DES Y6 or KiDS-Legacy) and DESI DR3.
