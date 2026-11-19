# TOE dependency-first research: the missing keystones, not more unexplained coincidences

**2026-11-19 | 7 executable gates + dependency graph | CONDITIONAL research, NOT a Theory of Everything.** Main repo: wilcompute/W33-Theory; initially tested against master `eaedca990e1d9d822a6c894455e3841864bbcd69`, including parallel `d5edaa9a`, `4ea5ae0`, `cb1a667`, `ff5090ff`, and the `eaedca990` anomaly/causal pass. Concurrent master `b9e08278` landed during our tests; its entire commit diff was reviewed. It independently reconstructs causal antichain topology, studies positive-transfer gauge actions, causal-history decoherence and charge-family ambiguity. This pass's E8 Higgs/Green–Schwarz center lattice, quadratic-field causal-operator falsifier, M2 geometric target, same-parity SU5 mass split gate, one-photon mode resource test and explicit dependency DAG are distinct.

## What we ACTUALLY have versus what is still assumed

| Subject | Rigorous or reproducible pieces | Still unbuilt or inserted |
|---|---|---|
| Chiral matter | Finite balanced E8 sector 3x16 + 5x10 + 8 singlets, relative cohomology and index; 19-field exact renormalizable F/D-flat messenger vacuum | Globally compact singular G2 metric and source index, exact N=1 supergravity field content |
| Anomalies | Original 3 U1 cubic/Spin10/gravity coefficients; exact two-direction polynomial factorization | Axion kinetic/Stueckelberg and quantized Wess-Zumino terms, actual inflow, anomaly-free UV action, global quotient and R symmetry |
| Flavor | Three gauge-allowed diagonal operators with nonzero formal singlet spurions | Nonzero physical Yukawa overlap (strict punctured S3 ordinary bulk cup=0), observed masses/mixings from geometry, one light Higgs |
| GUT | Conditional one-loop three-adjoint threshold matching and SM parity projection of 5D SU5 X zero modes | Radiative protection, full 5D field/brane boundary problem, proton decay, 2-loop thresholds |
| Gravity | Causal order, finite Regge and multiple linearized constraint/response checks | Derived 3+1 Lorentzian microaction, healthy local wave operator, first-class nonlinear Einstein constraints, physical quantum vacuum |
| Photon | Correct single-photon multimode gates and loss/phase/SSR models | Scalable BQP with polynomial physical resources; a new measured prediction, not just QM reformulation |

## Gate 1: the E8 axions can reuse charges already in the Higgs vacuum

Import the **actual** source's eight charged Spin10 singlets `A,B,C,D,E,F,G1,G2`, and exact Greens–Schwarz anomaly shifts `s1=(2,1,1)`, `s2=(0,1,-5)` from the previous pass. The eight-row charge matrix has Smith invariant factors **(1,1,4)**. The two axion shift vectors are **integer combinations** of pre-existing singlet Higgs charges:

```
s1 = charge(D)
s2 = -2*charge(A) + 4*charge(C) - charge(D).
```

Adding the two shift vectors to the Higgs charge lattice leaves the Smith factors **(1,1,4)** unchanged. Thus the *charge-lattice obstruction* to sourcing two anomaly-shift directions by Higgs phases is absent. Nothing in this calculation constructs the axionic Wess–Zumino/Green–Schwarz couplings: the phase fields are gauged/eaten, and anomaly cancellation additionally needs correctly quantized 4D topological couplings, local counterterms, global group identification and possibly genuine higher-dimensional inflow.

**Better interpretation of the repeated four:** Every Higgs/axion charge satisfies `q1+q2+q3=0 mod4`. In the original spectrum the **three 16s** have `sum q =1 mod4`, the **five 10s** have `sum q =2 mod4`, and the eight singlets have `sum q=0 mod4`. The residual diagonal U1 transformation `exp(i pi/2*(q1+q2+q3))` therefore acts as `i` on Spin10 16, `-1` on 10 and `1` on singlets. That is precisely the Spin10 center charge pattern. In the full **(Spin10 x SU4)/Z4** subgroup of E8, the naive Abelian Higgs Z4 may be identified with the existing Spin10 center rather than defining an independent discrete selection rule. **It does not derive the separate Z4^R** needed to forbid singlet cubics; treating them as the same because both have order4 would be false.

**First physical gate:** derive one compactification action containing BOTH axionic directions and all anomaly-canceling couplings while preserving the R selection and fermionic source spectrum. If that is impossible, do not fit Yukawas or claim a viable E8 model.

## Gate 2: physical flavor has one measurable geometric target

The renormalizable messenger F/D vacuum produced three nonzero *spurions*, but their ratio is only ~1.44. An illustrative charged mass ratio of `10^5` therefore requires an additional overlap/Higgs projection ratio of `R=69337.5245` if this is the entire texture. For equal prefactors in instanton-mediated Yukawas, `Y_i \propto exp(-S_i)`, this requires a difference

```
Delta S = log(R) = 11.1467415.
```

As an *independent laboratory toy profile*, if three equal-width Gaussian wavefunctions are centered at `x1=x2=0`, `x3=d`, their triple overlap relative to coincident centers is `exp(-d^2/(3 sigma^2))`; obtaining the same ratio needs `d/sigma=5.7827523`.

These are **inverse-designed targets**, not predictions of a compact singular G2 geometry. Acharya–Witten showed chirality requires G2 singularities; G2 Yukawas may arise through localized/M2-instanton physics, where metric/action data matter. Relevant literature: https://arxiv.org/abs/hep-th/0109152 ; https://doi.org/10.1016/S0550-3213(02)00612-0 ; https://arxiv.org/abs/hep-th/0409191 .

**Craftier next experiment:** keep the already chirally productive punctured-S3 source topology, and first test *localized defect or membrane corrections* with actual intersection/action integrals, instead of switching to a punctured T3 simply to obtain an ordinary cup product—T3 introduces three unwanted adjoint multiplets. If one compact defect geometry has nonzero Yukawas while keeping the original three chiral source index and no exotics, we simultaneously unblock family masses and anomaly inflow. Do not assert a nonzero defect overlap until physically computed.

## Gate 3: flavor-independent orbifold parities cannot distinguish the SU3 octet and SU2 triplet

Under `P=diag(+++--)` the su3 and su2 adjoint generators **both** have gauge parity +. Any pair of *shared* flavor involutions `F0,Fpi` therefore has the **same (+,+) flavor zero-mode subspace** for octets and triplets, even if F0,Fpi do not commute. This is an exact parity-design no-go, narrower than all 5D models.

A constructive 4D boundary-EFT escape: start from two adjoint fermions with two weak triplets and two octets, and introduce at the SM-preserving, SU5-broken boundary a gauge-invariant **octet-selective Majorana mass** for one octet, without that mass for the two triplets. A simple diagonal example keeps the two triplets at `10^7 GeV`, one octet at `10^5 GeV`, and the second octet near `10^13 GeV`. No cancellation of two ~10^16 GeV bulk masses is required for the octet splitting **in this effective algebra**. The boundary operator and all three mass scales are freely chosen; its full 5D KK boundary-value problem, brane anomalies, gauge coupling matching, proton decay and scalar sector are NOT solved.

**First physical gate:** derive the representation-selective boundary operator from a protective symmetry, then solve the complete 5D mass eigenvalue problem before attempting precision unification.

## Gate 4: falsify the signed causal operator with one quadratic scalar

Previous `eaedca990` derived unique signed interval-layer weights `(1,-5,4)` (up to scale) that cancel leading and subleading divergences of the **constant** field response in a 3+1 Minkowski time-1 cone. The constant weighted expectation approaches **3**.

But define `s(t,x,y,z)=t^2-x^2-y^2-z^2`. With metric `(-,+,+,+)`, **Box(s)=-8**. Its weighted finite-layer expectation is

```
K_rho[s]=pi rho int_0^1 du e^(-rho*pi*u²/24)
         [1-5z+2z²] g(u) * u,
z=rho*pi*u²/24;
g(u)=sqrt(1-u)-u ln((1+sqrt(1-u))/sqrt(u)).
```

The leading term cancels from `sum weights=0`, while the remainder is O(log rho / sqrt rho) and approaches **zero**. At rho=10^6 the direct quadrature yields **-0.099304263**, already close to zero, not -8. Subtracting a constant multiple of the center field cannot repair this probe because s(origin)=0.

This is an **explicit falsifier of interpreting this unrescaled finite signed expectation as the d'Alembertian.** It does NOT prove that no rescaling, more layers or other causal operators could work. In fact, independently published 2026 PRD work demonstrates convergence of a different local causal-set d'Alembertian, so the correct next step is to compare against its constant/linear/quadratic and boosted-frame benchmarks: https://doi.org/10.1103/np89-qzjp ; https://doi.org/10.1007/s41114-019-0023-1 .

**First gravity gate:** derive a microscopic causal-exchange kinetic operator that survives **Box(1)=0**, **Box(t)=0**, **Box(t²-r²)=-8** *before* claiming Einstein dynamics. Then test stability, constraint closure and nonlinear emergent metric.

## Gate 5: a sole photon is not an exponentially compact universal computer

For one photon in d orthogonal accessible modes, the physical one-particle Hilbert space has dimension d. Independent n-qubit information requires dimension 2^n, hence `d>=2^n`. This includes independent time bins/OAM modes: labeling them all as “one photon” does not make their orthogonal states free.

| d orthogonal modes | Maximum n-qubit register dimension |
|---:|---:|
| 40 | 5 |
| 240 | 7 |
| 1024 | 10 |
| 4096 | 12 |
| 65536 | 16 |

A 240-mode, 600 passive beamsplitter/phase-gate numerical simulation preserves the norm exactly to floating precision with only **240 complex classical amplitudes**. Standard passive one-photon gates are polynomial-time classically simulable in physical mode count; they do not imply a scalable computational advantage with polynomial physical resources. Actual literature [Universal Quantum Computation by a Single Photon](https://archive.ymsc.tsinghua.edu.cn/pacm_download/343/12580-lzw25.pdf) explicitly encodes n qubits in 2^n OAM modes; [Interfering trajectories](https://pmc.ncbi.nlm.nih.gov/articles/PMC6456595/) similarly uses 2^M time bins. Active non-Gaussian resources, many photons, measurements and nonlinearities must be included in resource accounting.

**Strategic choice:** either reframe this architecture as physically valuable high-dimensional optical processing, or specify and simulate a scaling-changing active/nonlinear resource before claiming polynomial-overhead BQP.

## Gate 6: pre-registered experimental statistics BEFORE speculation

A useful model-independent engineering benchmark: suppose a *future theory* makes a prespecified binary probability prediction `p1=0.51` where calibrated standard QM predicts `p0=0.50`. These values are **illustrative**, not predictions of E8, causal gravity, or the photon hypothesis. With 55,000 accepted independent trials, a symmetric two-sided type-I error budget 0.001, and the corresponding binomial critical threshold, the exact one-sided power for the upward `p1` alternative exceeds 90%. With two photons, transmission 0.8 each and two independent nondemolition herald efficiencies 0.7 each, the ideal accepted fraction is only **0.1568**, requiring an expectation of ~350,765 emitted two-photon pairs before final detection or drifts.

Even this experiment is **scientifically pointless for discriminating a TOE** until that TOE derives `p1 != p0`; more statistics cannot distinguish two theories that predict exactly the same observational probabilities. Lock down detector and postselection loopholes first.

## Gate 7: dependency DAG and the best “find X, then derive Y” priority

A reproducible 16-node DAG with 18 edges, no cycles, explicitly marks which repo results are conditional and which physical goals are unbuilt. The computed downstream-descendant counts for its two highest-leverage independent roots are:

- `UV_causal_action`: **7** reachable downstream nodes in the stipulated project graph.
- `compact_G2_geometry`: **6** reachable downstream nodes.

These are **subjective project-planning leverage scores**, not predictions or uniqueness theorems. The point is that *both trunks can be attacked independently*. More W33 graph identities or more digit coincidences are not prerequisites for any physics gate.

**Particle causal chain:** compact source geometry → (physical localized chiral index + quantized axion/inflow + defect Yukawa overlap) → anomaly-free SM low-energy theory → actual charged fermion masses & Higgs → experimental particle constraints.

**Gravity causal chain:** microscopic exchange action → unique Lorentzian/time generator, positive kinetic operator and metric → nonlinear first-class Einstein constraints → physical selected quantum state → operationally distinct process-tensor prediction → falsifying experiment.

**Two most valuable immediate falsifiers:**
1. A **quantized two-axion/defect Yukawa compactification** that retains exactly three chiral 16s without mirror/adjoint exotics. If that does not exist, no amount of fitting masses salvages the source model.
2. A **causal kinetic operator** that passes test fields (constant/linear/quadratic), boosted frames, spectral positivity and first-class constraint closure. If it fails `Box(s)=-8`, do not call it gravity.

The two trunks might ultimately require a common deeper principle, but no current theorem says solving one automatically produces the other. The missing pieces together mean we have several mutually interesting **conditional models**, not yet one unified predictive dynamics.

## Reproduce

```powershell
python analysis/toe_20261119_dependency_first_GS_causal_photon_modes.py
python -m unittest discover -s tests -p test_toe_20261119_dependency_first_GS_causal_photon_modes.py -v
```

Machine-readable certificate: `data/toe_20261119_TOE_dependency_first_gate_bridge.json`.

## Top 5 independent next experiments

1. **Two true axion couplings**: derive compact quantized WZ/GS coefficients and gauge kinetic/Stueckelberg terms for the two charge-lattice shift vectors; verify gauge/global anomalies and the independent protective R symmetry together.
2. **Defect Yukawa from the existing chirality source**: derive a nonzero actual overlap/M2 amplitude with `Delta S ≈11.15` for a test hierarchy while retaining net3 families and zero unwanted adjoint modes, then compute full CKM/PMNS/SM Higgs mixing.
3. **SU5 brane-mass spectral model**: solve full boundary-value eigenmodes for two bulk 24s with one octet-selective boundary mass and proper brane/gauge anomaly inflow, then 2-loop threshold and proton decay.
4. **Derived kinetic operator first**: benchmark exact scalar `Box` on 1, t, t²-r² (plus boosted fields) against modern convergent causal-set operators; only then construct a nonlinear tensor/gravity constraint system and its physical quantum state.
5. **Photonic computational and experimental falsifier**: count all orthogonal modes/ancillas/photons and model a nonlinear resource if claiming BQP; require an independent physically derived non-QM numerical deviation before any Bell/event-ready sample-size trial.
