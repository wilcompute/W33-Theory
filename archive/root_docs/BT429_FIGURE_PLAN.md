# BT429 — Figure Generation Plan for arXiv / PRL

## Status
This file defines the exact figure set required to turn `BT407_PAPER.tex` into a submission-complete arXiv package.

## Figure package

### 1. `figures/w33_dynkin_diagram.tex`
Purpose: Draw the W(3,3) Dynkin diagram with:
- central node O
- arm A = color / SU(3)
- arm B = weak isospin / SU(2)
- arm C = hypercharge / U(1)
- node distances 1,2,3
- annotation: q=3, lambda=2, mu=4

### 2. `figures/tier_ladder.tex`
Purpose: Tier ladder from n=0 to n=280 with labeled landmarks:
- n=0: Planck
- n=20: cold DM 4.0 TeV
- n=28: top
- n=29: W
- n=31: b
- n=33: tau
- n=36: Lambda_QCD / Omega-
- n=43: electron
- n=63/65/66: neutrinos
- n=129: H0 tier
- n=200: inflation tier

### 3. `figures/observable_scorecard.tex`
Purpose: heatmap / matrix showing sectors and precision classes:
- exact / discrete
- <1%
- 1–5%
- >5%
Rows: couplings, fermions, bosons, hadrons, neutrinos, cosmology, structure.

### 4. `figures/falsifiability_matrix.tex`
Purpose: 8 predictions by experiment and year:
- IPTA 2026: PTA peak 3.07 nHz
- Simons 2027: n_s = 0.9577
- JUNO 2027: normal hierarchy
- KATRIN+JUNO 2027: Sum m_nu = 93.2 meV
- Hyper-K 2027: proton decay ~10^33-10^34 yr
- Lyman-alpha 2028: warm DM 9.6 eV
- CMB-S4 2030: r_ts = 2.38e-3
- FCC-hh 2040: cold DM 4.0 TeV

### 5. `figures/cmb_predictions.tex`
Purpose: Plot or panel with:
- n_s substrate vs Planck
- r_ts substrate vs BICEP/Keck bound and CMB-S4 sensitivity
- visual emphasis that r_ts is within reach

### 6. `figures/charge_quantization_table.tex`
Purpose: Visual table of BT423 charge assignments:
- u_L, d_L, u_R, d_R, nu_L, e_L, e_R, nu_R
- columns: I3, Y, Q
- note: color arm gives 1/q = 1/3 rescaling

### 7. `figures/ckm_pmns_summary.tex`
Purpose: summary panel of:
- CKM: theta_C, delta_CKM, J_CP
- PMNS: theta12, theta13, theta23, Delta m21^2, Delta m31^2

### 8. `figures/hadron_spectrum.tex`
Purpose: hadron mass ladder panel:
- p, n, Delta, Lambda, Sigma, Xi, Omega-
- note exact / near-exact matches

### 9. `figures/cosmology_sector.tex`
Purpose: cosmology panel:
- H0
- Lambda
- n_s
- Omega_DM h^2
- PTA peak
- cold/warm DM masses

### 10. `figures/substrate_hamiltonian.tex`
Purpose: schematic of commuting-projector Hamiltonian:
- H = -J sum_v A_v - J sum_L B_L
- 40 vertex stabilizers + 40 line stabilizers
- finite partition function Z(beta) = [2 cosh(beta J)]^80

## Build workflow
1. Write all figures as standalone TikZ/PGF or simple LaTeX tables.
2. Compile each to PDF.
3. Include in `BT407_PAPER.tex` via `\includegraphics`.
4. Produce arXiv-clean package with only PDF figure outputs plus source .tex if desired.

## Submission-critical note
The paper is now content-complete; figures are the main remaining artifact gap before tarball generation.
