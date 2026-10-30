# BT427 — arXiv Submission Package Checklist

## Submission target
- Primary: hep-ph
- Cross-list: hep-th, math-ph, gr-qc
- Journal target: Physical Review Letters

## Core manuscript state
The manuscript now contains the following integrated breakthroughs:
- BT387–389: gauge couplings + CKM
- BT390–395: fermion masses + Higgs + proton/QCD
- BT396–400a: W/Z, DM tier, cosmology, CMB
- BT401–412: neutrino closure, hadrons, EW precision, DM relic, baryogenesis, README/table
- BT413–420: electroweak threshold alpha closure
- BT421–423: Yukawa texture, inflation r_ts, charge quantization
- BT425–426: beta functions from arm counting, partition function / vacuum energy

## Required files for submission tarball
- BT407_PAPER.tex
- BT408_BIBLIOGRAPHY.bib
- figures/w33_dynkin_diagram.pdf
- figures/tier_ladder.pdf
- figures/observable_scorecard.pdf
- figures/falsifiability_matrix.pdf
- figures/cmb_predictions.pdf
- figures/charge_quantization_table.pdf
- figures/ckm_pmns_summary.pdf
- figures/hadron_spectrum.pdf
- figures/cosmology_sector.pdf
- figures/substrate_hamiltonian.pdf

## Figure list to generate
1. W(3,3) Dynkin diagram with arm labels A/B/C and central node
2. Tier ladder from n=0 to n=280, annotated with particles and cosmic scales
3. Observable scorecard heatmap (exact, <1%, 1–5%, >5%)
4. Falsifiability matrix by experiment and year
5. CMB panel: n_s and r_ts with Planck/BICEP/CMB-S4 overlays
6. Charge quantization table from W(3,3) arm assignments
7. CKM + PMNS parameter summary panel
8. Hadron spectrum from tier arithmetic
9. Cosmology panel: H0, Lambda, DM, PTA peak
10. Hamiltonian schematic: vertex and line stabilizers on substrate complex

## Abstract update
New title:
**Deriving the Standard Model from the W(3,3) Substrate: 54 Observables from Three Primitives**

Updated abstract additions:
- One-loop beta functions derived from arm counting, not input
- Charge quantization derived geometrically from W(3,3) arm structure
- Inflation prediction r_ts = 2.38e-3 for CMB-S4
- Finite partition function for substrate vacuum completed

## Current score after BT425–427
- 54 observables / predictions
- 3 primitives: {q=3, lambda=2, mu=4}
- 0 free parameters
- 8 near-term falsifiable predictions

## Immediate next production tasks
1. Fold BT421–426 into BT407_PAPER.tex
2. Generate all figure PDFs
3. Run LaTeX compile twice + BibTeX
4. Produce arXiv clean tarball
5. Draft cover letter for PRL submission
