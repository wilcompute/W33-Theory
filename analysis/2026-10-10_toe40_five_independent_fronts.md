# TOE40 — Five independent TOE research fronts (10 October 2026)

**Status:** executed finite mathematics and selected negative controls; **not a Theory of Everything**. All code is replayable against W33-Theory `master`. We separate facts from hypotheses.

## 1. Modular vacuum / CP
Producer: `analysis/w33_20261010_toe40_four_controls.py`, JSON `data/w33_20261010_toe40_four_controls.json`.
The product theta-null for tau1=0.173+1.07i and tau2=0.286+1.29i has purity 1. Integral shear Omega12->Omega12+1 acts as qutrit CZ and yields fixed-frame purity 0.8955915583. The three-shear average 0.9303943722 is shear-invariant and CP-even, but differs by 0.1321209141 under the modular Fourier S generator. Thus even this partial orbit repair is **not a full Siegel modular invariant**. No CP-breaking stabilizing physical potential is claimed. Compare Pass11869-11878 and TOE38 framing firewall.

## 2. W33 Maxwell gauge Hamiltonian
Producer: `analysis/w33_20261010_toe40_native_maxwell_hamiltonian.py`, JSON `data/w33_20261010_toe40_native_maxwell_hamiltonian.json`.
Uses Round38's **actual** W33 three-deck Levi gradient B(k) and 1,385 locally closed plaquette rows P(k); it does not synthesize an unrelated cubic lattice. The quadratic positive Hamiltonian
`H(A,E)=0.5*||E||² + 0.5*||P(k)A||²`
has gauge equivalence `A ~ A+B(k)phi` and constrained Gauss law `B(k)^dagger E=0`. Verified `P(k)B(k)=0`, so potential energy is gauge invariant and `B^dagger P^dagger P A=0` conserves Gauss constraint along canonical flow.
For k=(0.01,0,0), the lowest transverse curl eigenvalues are 0.0001904736055, 0.0002051906807 and then 99.592296; for k=(0.02,0,0), 0.0007618634008, 0.0008207329778 then 99.592387. Two lowest eigenvalue ratios are 3.999837 and 3.999855, consistent with omega ~ |k|. No relativistic isotropy, lattice-to-continuum limit, physical electromagnetic gauge coupling, or quantization shown.

## 3. Chirality / finite Dirac index
The direct 40-by-40 point-line incidence matrix M of W(3,3) satisfies `MM^T=4I+A`, with exact spectral multiplicities `16^1, 6^24, 0^15`. Its untwisted balanced 80-dimensional bipartite Dirac operator anti-commutes with chirality and has 15 positive and 15 negative zero modes. **Index = 0**. Graph-theoretic kernel count does not supply one chiral Standard Model family. Nontrivial background and growing-local regulator remain necessary; see Nielsen-Ninomiya and Ginsparg-Wilson.

## 4. Exact cubic non-Clifford quantum operation (surrogate)
On three qutrits use `U|a,b,c>=omega^(abc)|a,b,c>`. This is unitary. The mixed third finite derivative of `abc` is 1 modulo 3, unlike quadratic phase gates, proving a non-Clifford phase. Conjugating first-qutrit X induces the b-c CZ phase; U is in the third level of the Clifford hierarchy. Under the **specified global depolarization model** `rho=(1-p)|psi><psi|+p I/27`, at p=0.01 ideal-output fidelity is 0.99037037. This is **not** implementation of the E6 27-variable signed 45-triad norm; translation of its cubic tensor into a valid optical Hamiltonian remains open.

## 5. Locked experimental falsifiers
Frozen historical W33 `alpha^-1=137+40/1111=137.03600360036...` versus CODATA 2022 `137.035999177(21)` gives **210.64 sigma** discrepancy if forced to be an **exact uncorrected** value, with no theoretical uncertainty. It is an archived numerical formula, not a physical prediction; other W33 formulas already exist and the source manuscript excludes alpha numerology from TOE evidence. NIST: https://physics.nist.gov/cuu/pdf/all.pdf .
Pass11876 shape ratios rounded at a given mass scale: up=0.569, down=2.77, charged-lepton=0.081, total extreme ratio 34.198; no common sector-universal shape constant can fit. The best possible minimax multiplicative error is sqrt(2.77/0.081)=5.8479, independently of fitting. This reproduces and sharpens the prior no-go, not a novel experimental mass prediction.

## Dependencies and boundary
- Primary W33 data and code are already in this repository (TOE38, TOE39, Pass11869-11878); this file has no ownership claim over their prior discoveries.
- A *complete* theory requires a physical action/vacuum, universal causality or Lorentz limit, anomaly-free chiral matter, experimentally derived couplings and laboratory validation.
- Independent scholarly anchors: Carducci et al., JHEP (2026), https://link.springer.com/article/10.1007/JHEP09%282026%29268 ; Lüscher, Phys. Lett. B 428 (1998) 342-345, https://doi.org/10.1016/S0370-2693(98)00423-7 .

## Best five independent next research actions
1. Construct a **full Sp(4,Z)-invariant** candidate potential from Igusa/Burkhardt ratios, prove positive Hessian and non-CP-symmetric vacuum up to modular isomorphism, then evaluate sector-marked theta tensors.
2. Determine full small-k Maxwell acoustic tensor and anisotropy across directions; prove asymptotic twofold dispersion, quantize constrained canonical brackets and couple to a *local* charge operator.
3. Implement a gauge-covariant Ginsparg-Wilson/overlap operator on a growing W33-derived local lattice and compute index/anomaly, not just nullity.
4. Give the 45-triad E6 cubic an explicit Hermitian generator or ancilla dilation with stated physical resources, test actual non-Clifford injection and leakage against the CCZ control.
5. Freeze a single renormalized dimensionless observable and uncertainty budget from a chosen action *before* looking at data, and retain exact negative controls as regression gates.
