# Five-front-plus TOE follow-up: optical compilation, anomaly kernel, calibrated centre, ideal causal process, and prediction gate

**Date:** 2026-11-20 · **Input baseline:** `wilcompute/W33-Theory` master `88127950882918101708ecb9189cd2b3d3498c71`. This follow-up extends the executable six-commutator/holdout, E6 flux, and maximally mixed centrality work. All results here are *mathematical, compiled unitary simulations, or seeded synthetic statistical trials*. **No physical photon experiment, charged singular-G₂ index, anomaly-inflow construction, robust finite-shot linear causal witness, or beyond-Standard-Model prediction has been produced.**

## 1. Optical mode compiler — a reproducible single-photon 18-mode testbed

A logical two-qutrit basis `|a,b>` can be represented by a *single photon* in one of nine mutually exclusive spatial modes `k=3a+b`. A coherent two-path control expands the system to 18 optical modes. For two qutrit Weyl operations `A`, `B`, define `U0=AB`, `U1=BA`. Each is monomial: one phase-weighted nonzero entry in every row and column, so it can be realized abstractly by a mode-routing permutation and phase shifts, without full arbitrary 9×9 interferometer synthesis. With 50:50 branch split and recombination,

`V_phi = (H ⊗ I9) diag(U0, e^{i phi} U1) (H ⊗ I9)`.

This is a precisely defined 18×18 unitary, representable using nine branch-couplers at input and nine at output, plus path-selective phase/wiring networks; **routing is not a claim of zero optical cost**. For each input basis state, the probability of the selected output control port is

`P0(phi)= [1 + Re(e^{-i phi} Tr(U0 rho U1†))]/2`.

Taking `phi=0` and `pi/2` reads the two control quadratures. The code verifies unitarity and probability identities at `~7×10^-16`. It emits a detailed seven-setting netlist: six basis-vector pairs plus `(e1+e3, e2)` holdout. A physically valid nonlinear 81-gate command map `F(u0,u1,u2,u3)=(u0+u1*u3,u1,u2,u3)` leaves all six basis gates fixed but makes this holdout wrong. Every implemented target operation is still a unitary Weyl matrix.

**Noise example:** 160 *accepted* photons per quadrature, seven settings and two quadratures = **2,240 accepted** per protocol. With acceptance probability 0.40, fringe visibility 0.90, detected-bit flip probability 0.015 and phase drift uniformly in ±0.05 radians, 350/350 seeded honest runs were classified correctly and 350/350 malicious-address runs passed the six calibrations but failed the holdout. Mean attempts 5,608.29 per protocol. These are synthetic independently sampled *heralding and detection trials*, not experimental yield or error-rate claims. Separate optical sources, detectors, path stability, SWAP routing losses, and complete causal instruments still need engineering.

## 2. Exceptional matter — exact isolated anomaly-kernel constraint

For `27 -> 16_(+1) + 10_(-2) + 1_(+4)` of `E6 -> Spin(10)×U(1)_psi`, let net **four-dimensional left-handed** representation indices be `(x,y,z)` respectively. Assuming **all three local four-dimensional anomalies must cancel without inflow**, the coefficients are

`A_grav=16x−20y+4z`, `A_U1³=16x−80y+64z`, `A_Spin10²U1=2x−2y` (normalizing `T(16)=2,T(10)=1`).

The integral nullspace of this 3×3 anomaly matrix is **exactly** `Z·(1,1,1)`: the mixed nonabelian anomaly forces `x=y`, then gravity anomaly forces `z=x`; the cubic condition follows. Therefore an isolated chiral spectrum formed solely from these three components and maintaining this gauge group requires *equal net indices*.

For the previous toy four-torus `U(1)_psi` flux `(n12,n34)=(3,1)`, the established continuum index formula `index(D_q)=q² n12 n34` gives `(3,12,48)` and anomaly vector `(0,2160,−18)`. To attain **three anomaly-free complete E6-27 units** with the three spinors fixed, an additional net chiral contribution `(0,−9,−45)` is necessary. No **positive** nonzero flux product with ratio `(1,4,16)` can satisfy the isolated anomaly conditions. This is not a no-go for `E6` as a GUT: an explicit Green–Schwarz mechanism, anomaly inflow, Higgsed U(1), extra representations or a different compactification can change the conditions. Nor does the arithmetic derive three families or a singular-`G2` charged Dirac operator.

## 3. Noise-aware centrality — finite nonzero-error confidence certificate

For **independently warranted unitary** `K=(BA)†(AB)` in dimension `d=9`, a maximally mixed target gives `c=Tr(K)/d` and exact deviation `||K−(Tr K/d)I||²_F=d(1−|c|²)`. The previous zero-error binomial criterion has poor practical sensitivity if detectors flip bits.

With a *trusted*, known phase `zeta`, run two independent phase-matched experiments: (i) a reference known to have unit coherence (`c_ref=1` after phase matching), and (ii) the test. Assume both share the same unknown but stable, **positive** measurement gain `g`, with `0<g≤1` and no additive readout bias, so that `p_ref=(1+g)/2` and `p_test=[1+g Re(zeta* c)]/2`. Obtain exact Clopper–Pearson intervals for both Bernoulli counts using confidence budgets `delta/2` each. The lower test-success bound and the **upper** reference-success bound then imply, when positive,

`Re(zeta* c) ≥ (2 p_test_low−1)/(2 p_reference_up−1)`.

Set this to zero if the numerator is nonpositive, and clip at one. Because `|c|≥Re(zeta*c)`, this yields a conservative bound `d[1−max(0,c_lower)²]` on noncentral Frobenius squared. The joint coverage is at least `1−delta` by the union bound (the intervals used here are conservative two-sided CP intervals). The method does not presume zero detector errors or perfect visibility, but **does presume identical stable gain** between reference and test, an independent unitary guarantee, IID accepted events, and no unbounded preparation/readout artifacts.

**Synthetic example:** `g=0.96` corresponds to a 2% matched-basis readout error in an otherwise ideal visibility model. With 250,000 accepted shots in *each* arm, 99% target confidence, and 250 seeded repetitions, the median upper noncentrality squared of an ideal central test is **0.05926**, and **148/250** reference-calibrated runs certify `||K−scalar||_F≤0.25`; a noncentral example with `Re(zeta*c)=0.96` has median upper squared ≈**0.77122** and no successful certifications. Finite confidence bounds do not guarantee that every finite run certifies even an exactly central device.

**General CPTP ambiguity:** Two branches can individually implement the **same identity CPTP channel** on the target while leaving different environmental which-path states. Their overlap may be 0, 0.4, or 1, and that overlap directly changes the observed control coherence. Target *channel marginals alone* therefore cannot recover the coherent-order interference; an environment/reference model is required. The scalar-**unitary** identity does not extend to arbitrary CPTP channels, even when the two target marginals match exactly. This is a precise obstruction to an overbroad claim of channel centrality certification.

## 4. Causal-order certification — ideal-process **structural proof**, not a lab witness

For a qubit target initially `|0>` and a coherent control `|+>`, construct the **standard ideal quantum-switch routing process vector** in axes `(A_in,A_out,B_in,B_out,F_target,F_control)`, six qubits, Hilbert dimension **64**. Unnormalized maximally entangled links connect the party output ports in either order; the two alternatives carry orthogonal future control labels. The resulting process matrix `W=|w><w|` is positive, rank one, trace **4** (the product of the output Hilbert dimensions). The independent code checks normalization against **32 pairs of random unitary** local CPTP maps and **32 pairs of random three-Kraus general CPTP maps**, as well as representative local preparations and measurements.

A replacement channel preparing `|1>` at laboratory A changes B's probability of recording measurement outcome `1` from **0 to 1/2**, and conversely a replacement channel at B changes A's `1` probability by the same amount. This is two-way signaling **of the overall process**, not simultaneous signaling along each individual branch. The incoherent dephased mixture of the two definite orders shows *the same* marginal bidirectional signals, so marginal signaling alone does **not** distinguish indefinite from classical random order.

The ideal **coherent** `W` is rank one. In any positive semidefinite decomposition `W=W_AprecB + W_BprecA`, both positive summands must have range contained in the one-dimensional span of `W`. Hence each nonzero summand would itself have to represent the *same* pure process, but the observed bidirectional signaling makes that pure process incompatible with either fixed-order class. **Therefore the ideal coherent switch is causally nonseparable within the standard process-matrix axioms.** This is a structural proof for the specifically constructed ideal process, not an independently measured operational causal witness. As a control, dephasing the control yields a rank-two causally separable order mixture; after trace normalization, process-state purities are `1` versus `1/2` and their trace distance is `1/2`.

To reach an experimentally valid claim one must reconstruct the process (or an appropriate subset) from trusted intervention instruments, enforce process-matrix normalization/non-signaling constraints, and evaluate a **linear causal witness with a rigorous causally-separable bound**, including finite-count confidence and SPAM assumptions. The established literature provides such witnesses (Araújo *et al.*, NJP **17** 102001 (2015); *Higher-Order Process Matrix Tomography of a Passively-Stable Quantum Switch*, PRX Quantum **5**, 010325 (2024)). Central W33 Pauli commutator fringes alone are still insufficient.

## 5. What can W33 predict that standard quantum theory does not?

A strictly associative projective representation of `F_3^4` with multiplier `phi(u,v)=z(u)·x(v)` enforces the cocycle identity; the code verifies it for 30,000 independent sampled triples with **zero violations**. Consequently, simply discovering the W33 Pauli commutator, a six-setting symplectic reconstruction, or a quantum-switch order phase is not an anomalous prediction: all follow ordinary standard quantum mechanics.

The packet defines a **prospective discrimination protocol** for a hypothetical extra associator phase `theta=2π/9` chosen *externally*, with ideal fringe visibility `v=0.9`. The standard-null and toy-alternative binary probabilities are `0.95` and `0.84472`. A conservative IID Hoeffding midpoint calculation gives **957 accepted measurements per hypothesis** for <1% combined classification error under that chosen toy alternative. **The alternative phase has not been derived from a physical microscopic action or from the TOE**; it is a sensitivity illustration only, not a parameter-free prediction, a detected deviation, or evidence against quantum theory. Physical mechanism, Lorentz/gauge consistency, scale and experimental channel remain open.

## Reproducibility and provenance

The full script does not rely on the preceding repo scripts; it uses standard Python 3, NumPy, SciPy, fixed random seeds, and independently evaluates all five fronts. The frozen JSON contains the seven optical netlists, explicit anomalous and compensating indices, finite-shot results, and the ideal 64-dimensional process checks. All `unittest` cases verify specific outputs and failure conditions.

```bash
python analysis/toe_20261120_fivefront_plus_bridge.py
python -m unittest discover -s tests -p test_toe_20261120_fivefront_plus_bridge.py -v
```

**Supporting established literature:**
- Causal witnesses for the switch: https://doi.org/10.1088/1367-2630/17/10/102001
- Process-matrix tomography: https://doi.org/10.1103/PRXQuantum.5.010325
- Trusted quantum input causal certification: https://doi.org/10.1103/PhysRevLett.129.090402
- Higher-order quantum operations (2026 review): https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs
- E6 branching: https://doi.org/10.1140/epjc/s10052-025-15043-7
- Standard overlap index prior art: https://doi.org/10.1103/PhysRevD.67.025015

## Five independent next gates

1. **Instrumented optical test:** build the emitted 18-mode layout in a real photonic device; measure all 14 quadratures, attempted-versus-accepted events, path coherence and nine-mode permutation fidelity with a frozen holdout.
2. **Physical chiral sector:** specify a singular-`G2`/ADE charged Dirac operator, calculate a true index and its inflow, and ensure complete 4D matter anomaly cancellation with a dynamical vacuum; no hand-picked family count.
3. **CPTP-safe operator certification:** characterize the *coherent dilation* rather than just the target-channel marginals, and report robust calibration confidence when reference/test gains drift.
4. **Linear causal witness:** decompose the ideal process into physically trusted instruments and compute an explicit noise-robust causally separable SDP bound plus finite-count error bars.
5. **Unfitted physics observable:** define a microscopic Lorentz/gauge-consistent action and derive one numerical scattering/coupling/mass/gravity prediction **before** comparison with independent measurements. If this cannot be done, report the lack of discriminatory physics rather than a numerical coincidence.
