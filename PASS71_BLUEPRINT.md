# Pass 71 Forward-Attack Blueprint

## Mission
Pass 71 targets the three hardest open verification gaps in the W33 programme:
1. **Explicit HX/HZ parity-check matrix construction** for the claimed `[[360,9,≥9]]` code
2. **Closed-form Ihara zeta pole** confirmation at `u = 1/√7` for the W(3,3) graph, matching the GRH claim in Supplement G
3. **Numerical PMNS mixing-angle extraction** from the raw W(3,3) adjacency eigenvectors — producing concrete θ₁₂, θ₁₃, θ₂₃ and δ_CP predictions for comparison against PDG 2024 values

## Track Plan

### Track D — [[360,9,d]] CSS Parity-Check Matrices
- Build `H_X` and `H_Z` as sparse binary matrices from the W(3,3) symplectic structure
- Verify `H_X · H_Z^T = 0` over F₂
- Compute minimum distance lower bound via BFS on the Tanner graph
- Output: `w33_pass71_trackD_css_matrices.npz` + witness JSON

### Track E — Ihara Zeta Pole Confirmation
- Construct the full 40×40 Hashimoto directed-line-graph matrix `B`
- Factor the characteristic polynomial of `B` numerically
- Locate poles of `Z_W(u)⁻¹` and confirm the nearest pole to origin satisfies `|u| = 1/√(k-1) = 1/√11`
- Output: `w33_pass71_trackE_ihara_zeta_poles.json`

### Track F — PMNS Angle Extraction
- Assemble the explicit 40×40 adjacency matrix `A` from the symplectic form over F₃⁴
- Diagonalise; project the 15-dimensional eigenspace of eigenvalue −4 onto a 3×3 PMNS-candidate unitary
- Report θ₁₂, θ₁₃, θ₂₃ and compare to PDG 2024: θ₁₂≈33.4°, θ₁₃≈8.6°, θ₂₃≈48.4°
- Output: `w33_pass71_trackF_pmns_angles.json`

## Why These Three Are Outside-the-Box
- **Track D** turns a spectral claim into a concrete hardware-checkable QEC blueprint for any ion-trap / superconducting quantum computer team
- **Track E** is the first step toward a machine-verifiable Graph-RH certificate, directly relevant to the Riemann Hypothesis Clay Prize connection
- **Track F** produces a table-ready falsifier: if any angle deviates from PDG by more than the current experimental uncertainty (≈0.5°), the programme is falsified at that step

## Execution trigger
Run `python w33_pass71_run_all_tracks.py` once those three scripts are pushed in the next session.
