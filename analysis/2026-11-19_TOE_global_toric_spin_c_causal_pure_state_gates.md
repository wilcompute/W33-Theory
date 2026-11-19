# TOE: global toric E8 vacuum, adjoint stability, Spin^c family index, causal locality, pure quantum states, optical phase resources

**2026-11-19 | STATUS: rigorously scoped conditional finite calculations, NOT a Theory of Everything.** Based on a review of parallel GitHub commits `7cda851ce` and `1260d6c39` (causal propagation, dimension, holonomies, SJ state, doubling, non-Abelian gauge), plus `017f5cde3` (E8 Z4R and three SU5 adjoints), `0ec1074e4` (complete singlet cubic inventory), `22ac80224` (operational two-copy photon), and actual imported E8 sector file `analysis/toe_20261119_balanced_source_E8_cup_gate.py`. We do **not** claim the established spin^c/causal-set/quantum Gaussian facts are novel. Their intersection with the repo's concrete particle model is the object of investigation.

## 1. Full eight-singlet F/D vacuum, not just the previous five-field subbranch

The prior `017f5cde3` candidate had eight charged E8 Spin10-singlet chiral multiplets and two (R=2) neutral driving multiplets. It constructed a D/F-flat point with five nonzero charged fields, but did not lift the other singlet directions. This report extends the exact source field spectrum rather than quietly assuming the remaining fields disappear.

Label the eight charged singlets in order `A=S12, B=S12conj, C=S13, D=S14, E=S14conj, F=S24, G1=S34_1, G2=S34_2`. Their U1^3 charges, from the parallel E8 sector census, are rows of

```
Q = [(1,-1,0),(-1,1,0),(1,0,-1),(2,1,1),
     (-2,-1,-1),(1,2,1),(1,1,2),(1,1,2)].
```

Its rank is3. The five gauge-invariant monomials

```
I1=AB, I2=DE, I3=AFE, I4=CEG1, I5=CEG2
```

have an integer exponent matrix E of rank5 and satisfy **E Q=0 exactly**. They are algebraically independent local holomorphic coordinates on the generic dense toric quotient; there are (8-3=5) complex gauge-invariant directions before W.

**Construct a fully nonzero gauge-flat point directly from neutral cycles.** The squared magnitudes are the sum of the five exponent vectors,

```
|A,B,C,D,E,F,G1,G2|² = (2,1,2,1,4,1,1,1).
```

Since (Q^T E^T(1,1,1,1,1)^T=0), **all three D terms are exactly zero** with canonical positive Kähler metric and vanishing FI. Every charged field is nonzero.

Add **five**, not two, gauge-neutral chiral driving multiplets `X_i`, all of Z4R charge2. Choose a finite effective cutoff M and gauge-invariant target values `v_i=I_i(phi_0)`; the **chosen** superpotential is

```
W = sum_(i=1..5) X_i [I_i(phi)-v_i] / M^(degree(I_i)-2).
```

All charged singlets have Z4R charge0. This W is gauge-invariant and Z4R-invariant. At phi=phi0, Xi=0, **every F term and D term vanishes**. Its full 13x13 complex symmetric superpotential Hessian has rank **10**. Exactly three gauge-tangent zero directions remain, as checked independently through the monomial Jacobian (J Q_{gauge}=0). Hence this explicit *truncated* eight-charged-plus-five-neutral system has zero local complex physical moduli after quotient by the three complexified Abelian gauge directions. This is stronger than the earlier five-field, two-driving-field subbranch: it tests all eight charged source fields and neutral drivers.

**Anomaly parity connection.** With the minimal 4D SUGRA charge census of `017f5cde3`, the mixed gravitational Z4R coefficient without drivers is −21. Five additional neutral R2 driving multiplets contribute +5, yielding **−16 =0 mod2**, whereas two driving fields leave the coefficient odd. This is a necessary modular condition only; Abelian gauge anomalies and global/compactification inflow must be checked, and the original spectrum might contain more light neutral moduli. Counting five constraints is not proof of a quantum anomaly-free symmetry, nor does the shared parity establish a geometric origin.

**Remaining physical failure gates:** The five chiral neutral driving fields, their target values, M, Kähler metric and effective operator coefficients were freely inserted; cubic invariants with drivers are dimension-five superpotential operators needing UV mediators, and even a local isolated vacuum need not be radiatively natural or globally stable. The full E8 source calculations previously found vanishing strict bulk relative cubic on punctured S3, so a nonzero **physical** mass-generating Yukawa remains to be derived. The local singlet mechanism has no compact G2 metric, no actual SM gauge breaking, no inferred fermion masses, no anomaly inflow proof and no Einstein dynamics. Standard classical F/D quotient source: [Luty & Taylor, 1996](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.53.3399).

## 2. Full SU5 adjoint threshold counterexample is extremely unstable

Recompute the previous **three `24_F`**, complementary-flavor projector solution at a *chosen* (M_U=2e16) GeV. It has two electroweak Majorana triplets at `7.67789089e6` GeV, one color octet at `5.67838850e4` GeV, all three leptoquark partners near `1e16` GeV, and exact one-loop meeting of inverse gauge couplings. All components of all three fermionic adjoints are included; no scalar Higgs thresholds/2-loop/proton decay calculations are.

These light masses arise from cancellations between SU5 invariant mass matrices with entries on the (M_U) scale. Their operational sensitivity is severe: a common additive perturbation of only `delta M0=10^-6 M_U=2e10 GeV` in the diagonal SU5-invariant mass matrix raises the octet and light triplets to the (10^{10}) GeV scale and destroys the original crossing. Keeping the **octet mass within 10%** would require `delta M0/M_U <=2.839e-13`. The direct one-loop running recomputation gives inverse-coupling spread **4.06545** under the 10^-6 perturbation. This is a **fine-tuning sensitivity test**, not a calculated quantum correction: no symmetry, beta function or UV dynamics has yet predicted such a shift.

Next, demand a protected light flavor subspace compatible with a real SU5-breaking Higgs potential, SM scalar masses, proton decay and two-loop threshold matching before calling the crossing physical.

## 3. Global spin-gauge topology gives a charge-parity/index filter

The parallel causal/spectral report `1260d6c39` found that on a flat 2-torus an antiperiodic spin structure and a pi-gauge Wilson phase can compensate for a charged spinor. **Their compensation is charge-dependent**. For U1 charge q, spin boundary alpha=1/2 and Wilson theta=pi, the total covariant mode twist is `alpha+q*theta/(2pi)=(q+1)/2 modulo1`. It admits zero momentum for **odd q**, not for q=0 or other even charges. A causal model cannot identify spin and U1 holonomies universally across particles with different charges.

There is a deeper established global version: Spin^c structures demand `c1(L)=w2(TM) mod2`. On the compact **Euclidean internal test space** CP2, (w2=H mod2) and signature `sigma=1`. Therefore a determinant line c1(L)=kH is admissible iff k is odd. Atiyah–Singer gives the integer index

```
index D_L=(k²-1)/8 (k odd).
```

The table is `k=1 -> 0, k=3 -> 1, k=5 -> 3, k=7 -> 6`. The exact index **3** for inserted flux k=5 illustrates a topological route to integer chirality, **not a physical derivation of three Standard Model families**. No dynamics selects CP2 or k=5; CP2 is not itself a Lorentzian 3+1 spacetime, and constructing an appropriate singular 7D G2 compactification with the required gauge/zero-mode data is open. Source: [Spin^c structures and Dirac index](https://academic.oup.com/qjmath/article/72/1-2/603/6225869); [CP2 index tutorial](https://georgedouzas.github.io/posts/fundamentals-of-mathematics-for-physicists/part-i-13-spinors-dirac-operator.html).

## 4. A causal-link locality no-go for naive bounded-degree information hardware

Given a Poisson sprinkling density rho into fixed Minkowski regions, the conditional probability that origin and an event x form a direct causal link is `exp(-rho V(origin,x))`. Therefore the expected number of future links equals `rho int_region d^d x exp(-rho V(origin,x))`. This is the established causal-set nonlocal light-cone link structure, not a proposed new physical law.

For a **1+1 null-coordinate diamond** `0<u<1,0<v<1`, with diamond-volume `uv/2`,

```
E[L2]=gamma_E+ln(rho/2)+E1(rho/2) ~ ln(rho).
```

For a **3+1 future light cone truncated at t=1** and fixed origin, proper-time-square `s=t²-r²`, Alexandrov interval volume `V4=pi s²/24`,

```
E[L4]=pi*rho int_0^1 ds exp(-rho*pi*s²/24) *
   [sqrt(1-s)-s ln((1+sqrt(1-s))/sqrt(s))]
   ~ pi sqrt(6) sqrt(rho).
```

The integration and asymptotic scaling are independently verified at densities 40..40960. The computed high-density quotient `E[L4]/sqrt(rho)=7.48880`, converging toward `pi sqrt(6)=7.69530`. **Direct links are not a fixed valence local graph**, despite microscopic finite interval cardinality. A naive per-event processor that only exchanges information with, say, 4 or 8 nearest Hasse neighbors is NOT the generic Lorentz-invariant sprinkling network. A physically motivated nonlocal kernel or mesoscopic suppression prescription must be supplied and tested for Lorentz covariance and recoverable locality. This does not itself establish an energy lower bound or disprove all information-substrate TOEs.

Prior research: [Surya, causal sets review](https://doi.org/10.1007/s41114-019-0023-1); [recent causal-set nonlocality discussion](https://link.springer.com/article/10.1007/s10714-024-03281-1).

## 5. Even positivity AND Gaussian purity do not uniquely fix the quantum vacuum

The new parallel `1260d6c39` correctly identified nonuniqueness of positive states sharing the same retarded causal commutator using a mixed shift `W_SJ+eps I`. A stronger test shows that **requiring a PURE Gaussian state still does not select a unique vacuum**.

For one CCR pair with real antisymmetric `Delta=[[0,1],[-1,0]]`, define for every real squeeze parameter r:

```
W_r = (1/2) [[exp(2r), i],[-i,exp(-2r)]]
V_r=Re W_r=diag(exp(2r),exp(-2r))/2.
```

Then `W_r-W_r^T=iDelta`, `W_r >=0`, `det V_r=1/4` (saturates pure Gaussian uncertainty), and `det W_r=0`. Thus **all r are distinct positive, PURE Gaussian states with exactly the same commutator**. r=0 is the Sorkin–Johnston positive spectral part of the chosen `iDelta` under the *chosen* counting Euclidean inner product, but r=.2,.7,1.2 are also valid pure states. They have different position and momentum variances. A further state selection, symmetry, metric, stationarity or physical boundary principle is necessary; the causal commutator and purity alone do not derive Born probabilities, vacuum or the interacting quantum state.

This is standard Gaussian symplectic-state theory; the new-to-repository step is strengthening the precise causal-vacuum failure case from positive mixed states to a one-parameter family of pure Gaussian states. References: [Quantization, dequantization, and distinguished states](https://doi.org/10.1088/1751-8121/ad7427); [pure Gaussian covariance condition](https://doi.org/10.1103/PRXQUANTUM.2.030204).

## 6. Photonic falsifier with phase-reference noise and explicit loss accounting

The prior two-copy activation `22ac80224` uses **two physical photons** and an ideal pre-setting herald, yielding the local one-photon-per-lab Bell state at ideal probability1/2. Extend it to a realistic failure channel: if the two independently prepared single-photon copies acquire a fluctuating *relative* phase with Gaussian standard deviation sigma, then the conditional Bell coherence is `V=E[cos(delta phi)]=exp(-sigma²/2)`.

In a two-qubit dephased dual-rail sector, the Horodecki CHSH maximum is exactly `Smax=2 sqrt(1+V²)`. Add independent isotropic/white two-qubit noise with Bell fraction w: `Smax=2w sqrt(1+V²)`; violation requires `w>1/sqrt(1+V²)`. The implementation constructs the 4x4 density matrix, correlator T_ij=Tr rho (sigma_i tensor sigma_j) and verifies the singular-value criterion independently at sigma=0,.2,.6,1,2. For **w=.82** the ideal phase-locked condition violates CHSH; sufficiently large phase diffusion does not. Ideal transmission eta=.8 per source photon reduces pre-setting success probability to `eta²/2=.32` before any herald/detector inefficiency.

Consequently, the extra phase-stability/coherence resource is not optional even if an additional photon resolves local number superselection. Everything computed agrees with standard quantum mechanics. A TOE would need a **different quantitative prediction** and a loophole-free experimental protocol. Source: [Horodecki CHSH criterion / dephased Bell pair](https://marcinplodzien.github.io/quantum-many-body-simulation/ch08_quantum_information_protocols/19_bell_states_and_chsh.html).

## Reproduction and scientific classification

```powershell
python analysis/toe_20261119_global_toric_spectral_causality_followup.py
python -m unittest discover -s tests -p test_toe_20261119_global_toric_spectral_causality_followup.py -v
```

Output `data/toe_20261119_global_toric_spectral_causality_followup.json` records exact construction matrices, check ranks, model assumptions, distributional expectations and numerical values.

**Exact finite theorems:** toric charge/invariant rank and local Hessian null count, pure Gaussian state nonuniqueness, charge-dependent flat holonomy, Spin^c index formula, phase-dephased dual-rail CHSH criterion.

**Conditional numerical EFT/sprinkling:** mass-threshold sensitivity, finite-density expected links, GUT one-loop matching, assumed noise model. None establishes dimension selection, UV unitary dynamics, true physical vacuum, three actual observed generations, anomalously protected symmetry, or a Theory of Everything.

## Best five independent next tasks

1. **Dynamical E8 origin:** derive the FIVE neutral R2 driving fields, effective operators, target values and full discrete-gauge/anomaly inflow from one compact action; show the physically calculated Yukawa overlaps are nonzero and correct full-rank SM masses.
2. **SU5 naturalness and proton safety:** obtain an exact symmetry protecting the three-adjoint complementary light subspaces against radiative mixing; include two-loop beta/mass RG, all scalar/Higgs thresholds and proton partial lifetimes.
3. **Global chirality without fake generations:** construct a physically valid singular seven-dimensional internal compactification whose characteristic flux and spin data are *dynamically determined*, yield three family indices with no adjoint exotics, and cancel all global anomalies.
4. **Causal gravity with true locality:** derive a Lorentz-covariant, non-doubled and finite-energy exchange kernel for its growing lightcone degree; show 4D selection and nonlinear first-class Einstein dynamics, not only a correct causal order or linearized Bianchi identity.
5. **Quantum vacuum and photonic operational predictions:** derive a unique physically acceptable Hadamard quantum state/positive S-matrix, Born rule and a photonic CHSH/process-tensor prediction including reference phase and loss that standard QM does not also predict.
