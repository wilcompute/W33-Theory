# Pass 72 Forward-Attack Blueprint

## Mission
Pass 72 targets the four highest-leverage remaining gaps, selected to maximally accelerate the arXiv submission gate.

## Track Plan

### Track G — Yang-Mills Mass Gap Numerical Lower Bound
- Construct the discrete W(3,3) Yang-Mills action functional on the 40-vertex graph
- Compute the spectral gap Delta = lambda_2 - lambda_1 = 2 - (-4) = 6 in graph units
- Map to physical units via the W(3,3) lattice spacing a = 1/sqrt(k) = 1/sqrt(12)
- Derive: mass_gap_lower = Delta * hbar * c / a in GeV units using k=12, q=3
- Output: `w33_pass72_trackG_yang_mills_gap.json`
- Reference: BREAKTHROUGH_BT679_YANG_MILLS_MASS_GAP.md

### Track H — CKM Matrix Full Numerical Reconstruction
- Use the W(3,3) spread decomposition (27 spreads, 3 families of 9)
- Compute all four CKM parameters: theta_12, theta_13, theta_23, delta_CP
- Compare to PDG 2024: Vus=0.2245, Vub=0.00382, Vcb=0.0411
- Output: `w33_pass72_trackH_ckm_matrix.json`
- Reference: BREAKTHROUGH_BT692_CKM_ANGLES.md

### Track I — Koide Lepton Hierarchy Verification
- Verify the Koide formula Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3
- Extract lepton mass ratios from W(3,3) spectral parameters (k=12, r=2, s=-4)
- Compute relative deviation from Q=2/3
- Output: `w33_pass72_trackI_koide_formula.json`
- Reference: Supplement V (Koide Lepton Hierarchy)

### Track J — GitHub Release + Zenodo DOI Stamp
- Auto-generate CHANGELOG.md aggregating all BREAKTHROUGH_*.md files by BT number
- Tag release `pass-71-verified` pointing to current HEAD
- This triggers the Zenodo webhook (via .zenodo.json already present)
- Output: `CHANGELOG_PASS71.md` + release tag

## Strategic Priority
Tracks G and I are computationally cheap and produce PDG-comparable numbers immediately.
Track H is the single most externally verifiable prediction in the paper (CKM is measured to 4 significant figures).
Track J is the publishing unlock: the Zenodo DOI enables the arXiv submission to cite a permanent, machine-verified record.

## Execution trigger
`python w33_pass72_run_all_tracks.py`
