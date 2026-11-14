# Pass 12666: the 4D N = 8 central charge in the 28 antisymmetric three-qubit Paulis; the Planck-criticality top mass against the 2025 ATLAS pole mass

Claude track. Follows Pass 12665. **Not a theory of everything.**

## 1. 4D: central charges from pairs of three-qubit states (`w33_4d_central_charge_pauli.py`)

The 28 three-qubit Paulis with an odd number of Y's are antisymmetric 8×8 matrices, and they span them (rank 28). So the 4D N = 8 central charge, a complex antisymmetric Z_AB (28 complex = 56 real numbers, the 56 of E7(7) at the origin of moduli space), is Z = Σ_a z_a P_a with z ∈ C²⁸.

Cartan–Cremmer–Julia quartic invariant: I4(Z) = Tr(ZZ̄ZZ̄) − ¼(Tr ZZ̄)² + 4(Pf Z + Pf Z̄).

| check | result |
|---|---|
| normal form, skew-eigenvalues (ρ, 0, 0, 0) | I4/ρ⁴ = 1.000000 (the 1/8-BPS attractor, Ferrara–Kallosh hep-th/0603247) |
| two states φ, ψ: Z = φψᵀ − ψφᵀ | rank 2, skew spectrum (r, 0, 0, 0), r = ‖φ∧ψ‖, Pf Z = 0, **I4 = r⁴** (6 of 6, to 10⁻¹⁵) |
| Pauli coefficients | z_a = −(φᵀP_aψ)/4, to 10⁻¹⁵ |
| 5D → 4D: quaternionic line {ψ, Jψ} (Pass 12665) | rank 2, r = 1, **I4 = 1** |
| generic z | rank 8, I4 of both signs |
| SU(8) invariance of I4 | 5×10⁻¹² (a U(8) matrix breaks it through det U in the Pfaffian, which an earlier version of the check missed) |

**Reading.** The 1/8-BPS attractor central charges in 4D are the two-planes of C⁸ (Gr(2,8) = SU(8)/S(U(2)×U(6)), the known residual SU(2) × SU(6)). In 5D they are the quaternionic lines (HP³, residual USp(2) × USp(6)). The 5D attractors embed in the 4D ones with I4 = N^{4/3} = 1.

**Weight.** "Rank-2 antisymmetric = φ∧ψ" is linear algebra, and rank 2 being the BPS form is standard supergravity. The only additions here are the Pauli labelling (28 antisymmetric Paulis, complementing the 27 + 36 split of Pass 12656) and the explicit embedding. This is much thinner than Pass 12665, and no 4D attractor flow over E7(7)/SU(8) was computed.

## 2. Planck-scale criticality and the top mass (`toe_uv/top_pole_2025.py`)

Pass 12537 found that λ(M_Pl) = 0 (Buttazzo et al. eq. 61, three-loop running) needs **M_t = 171.04 ± 0.37 GeV**. Web check, November 2026:
- The PDG 2026 review still cites the ATLAS+CMS Run 1 combination, 172.52 ± 0.33 GeV (a Monte Carlo-scheme mass); no newer joint combination was found.
- **New:** ATLAS published a top-quark **pole** mass from tt̄ + 1 jet (JHEP 12 (2025) 023, arXiv:2507.02632, read in the PDF): **170.7 ± 0.3 (stat) ± 1.4 (syst) ± 0.3 (scale) ± 0.2 (PDF+α_s) GeV**.

| measurement | value | pull against 171.04 ± 0.37 |
|---|---|---|
| Run 1 combination (MC mass) | 172.52 ± 0.33 | +3.0σ |
| preliminary pole combination (Nov 2025 talk; Pass 12537) | 172.25 ± 0.95 | +1.2σ |
| **ATLAS pole mass, JHEP 2025** | **170.7 ± 1.48** | **−0.2σ** |

The vacuum-stability fit uses the pole mass, so the ATLAS number is the like-for-like comparison, and it agrees.
- **But it cannot discriminate:** at ±1.5 GeV it is equally compatible with 172.5 (1.2σ).
- So this is consistency, not support. The test remains a pole mass at the 0.3 GeV level (a lepton-collider threshold scan) or a final LHC pole combination.
- The pass does not change the status of the repo's "top mass" kill-list item.

## Sources

- [ATLAS, top-quark pole mass in tt̄+1-jet (JHEP 12 (2025) 023)](https://www.osti.gov/pages/servlets/purl/3020240)
- [PDG 2026 top-quark review](http://pdg.lbl.gov/2026/reviews/rpp2026-rev-top-quark.pdf)
- [ATLAS+CMS Run 1 combination, arXiv:2402.08713](https://arxiv.org/html/2402.08713v1)
- [Ferrara–Kallosh, On N=8 attractors, hep-th/0603247](https://arxiv.org/abs/hep-th/0603247)
