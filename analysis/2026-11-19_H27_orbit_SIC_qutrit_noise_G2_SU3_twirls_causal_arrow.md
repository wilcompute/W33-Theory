# Six independent TOE / Holonet controls: exact H27 orbit selection, memory noise threshold, SU(3) Weyl detector twirl, real G2 degeneracies, causal arrow

**Date:** 2026-11-19. **Baseline:** `366aefd1189eed06ed9f5c34b6420d7d457fa475`, with parallel `f287b72a`, `0fc4aca`, `3700bb0f`. **Scope:** rigorous finite-dimensional mathematics and specified quantum/instrument toy models; **NOT** an experimentally confirmed Theory of Everything. Executable certificate at `analysis/toe_20261119_five_physics_gates_v3.py`, tests at `tests/test_toe_20261119_five_physics_gates_v3.py`, outputs at `data/toe_20261119_five_physics_gates_v3.json`.

## External source check, with a correction to an earlier experimental plan

Read the complete extended arXiv HTML of Beyer et al., *Observation of Genuine Multi-Time Quantum Memory* (2026-11-12), https://arxiv.org/html/2611.17268 , especially their Eqs. (1)-(2), Supplement VI (S36)-(S38), Appendices A-C, and the experiment. Their three-time witness uses **dynamical maps from a common initial time**, with **no intermediate interventions needed for the witness measurement** (though interventions are useful for reconstructing full processes). This corrects the imprecise implication in some earlier project next steps that interventions are mandatory to *measure this witness*. Our common 12-dimensional qutrit+environment dilation remains a prescribed time-dependent toy, not the paper's continuously driven superconducting-qubit demonstration.

For qutrit Weyl unitary 1-designs: https://www.nature.com/articles/s41534-024-00892-z and https://sirui-lu.com/QICLean/docs/QICLean/Channel/WeylTwirl.html . For the Albert realization as 3x3 Hermitian octonionic matrices: https://books.physics.oregonstate.edu/GELG/aa.html and https://doc.sagemath.org/html/en/reference/algebras/sage/algebras/jordan_algebra.html . Earlier repo file `analysis/2026-11-19_SIC_SU3_Plucker_Hesse_baryon_selector.md` already gave SU(3) baryons and SIC/Hesse selection; the new exact orbit-rank classification here has a narrower, explicit claim.

## 1. Noise robustness of the native qutrit three-time-only quantum memory hierarchy

Use the previous 3-level construction:

- `E1(rho)=(1-gamma)rho+gamma |0><0|Tr rho`;
- `E2=D_B` computational-basis complete dephasing;
- `E3=D_C` Fourier-MUB complete dephasing.

Now **postprocess E2 and E3** by the identical depolarizing channel `Lambda_e(rho)=(1-e)rho+e Tr(rho) I3/3`. Any basis projector output becomes `rho_j=(1-e)|j><j|+e I3/3`, with commuting eigenvalues `a=1-2e/3`, `b=e/3`. The *root* Uhlmann fidelity for two distinct basis outputs is `f=2 sqrt(a b)+b`; there are three pairs for each of the two late channels. The published dimension-three MUB witness therefore equals

`W3(e,gamma)=6[2 sqrt((1-2e/3)(e/3))+e/3]-2gamma`.

At `gamma=.36`, the negative witness disappears at `e=0.010263207615968259`. For `e=.01`, `W3=-0.009492939934717337`; for `e=.02`, `W3=0.2932420048477151`. At `gamma=.05,.36,.75,1`, threshold e values are in the JSON certificate. Above threshold the witness becomes **inconclusive**, not evidence of classical memory.

**All three two-time classical-memory explanations persist with depolarization**, explicitly, not by intuition:

1. `(E1,E2')`: `K0=sqrt(1-gamma)I`, `Kj=sqrt(gamma)|0><j|`, then branch-conditional computational dephase or reprepare `|j>`, followed by `Lambda_e`.
2. `(E1,E3')`: the same E1 channel resolved in the Fourier basis `|c_j>` and corresponding feedback, followed by `Lambda_e`.
3. `(E2',E3')`: `E2'` is random Weyl unitary with probabilities `q_ab=(1-e)/3 * 1_{a=0} + e/9` for `X^a Z^b`; the classical branch stores `(a,b)`, undoes the unitary, then implements `E3'`.

All 9x9 Choi comparisons and branch CPTP checks are below `1e-12` for five representative `(gamma,e)` pairs. The source's existing three-time construction remains physically coherent under late-time CPTP postprocessing; **the new result is an analytical noise threshold and explicitly preserved pairwise hierarchy**, not an invented quantum-memory theorem or a fabricated optical device.

## 2. Extension to dimension d and a new scaling obstruction

The same construction works for every `d` with two mutually unbiased bases. For `E1(rho)=(1-gamma)rho+gamma |0><0|Tr rho`, one has `S1=gamma(d-1)`. After late depolarization, two distinct basis outputs have root fidelity

`f_d(e)=2sqrt((1-e+e/d)(e/d))+(d-2)e/d`.

The published dimension-d theorem yields the **new explicit family formula**

`W_d(e,gamma)=(d-1)[d f_d(e)-gamma]`.

All three pairwise models can be constructed by the same basis-sensitive replacement instrument and a random Weyl-unitary instrument; the complete dephasing map is uniform random clock phases, and depolarization is uniform random Weyl conjugation. This gives a constructive family, not merely a witness inequality. At fixed `gamma=.36`, critical depolarization by dimension is:

| d | 2 | 3 | 4 | 5 | 6 | 9 | 12 |
|---|---:|---:|---:|---:|---:|---:|---:|
| epsilon critical | .016333 | .010263 | .007483 | .005887 | .004853 | .003178 | .002362 |

At small gamma, `epsilon_crit ~ gamma^2/(4d)` for fixed d, gamma->0. This is a *noise detectability* limitation, not a failure of quantum memory with higher-dimensional systems.

## 3. An exact H27 translation-coordinate obstruction in SU(3) SIC baryons

Revisit the previous engineered gauge-invariant local `SU(3)` SIC vacuum, with nine fundamental triplets and 84 baryon invariants `B_ijk=det(Q_i,Q_j,Q_k)`; previous 19 coordinate baryons had full local Jacobian rank 19, fixing all deformations modulo eight complex gauge directions.

Take a standard Hesse qutrit SIC, `Q_{a,b}=X^b Z^a(1,-1,0)`, `a,b∈F3`. As *species labels*, the translation subgroup `T=F3^2` acts on unordered baryon triples. The 84 triples split into exactly **four length-3 orbits** and **eight length-9 orbits**. A coordinate-selected set of baryons that is translation-closed must be a union of these 12 orbits.

Compute the entire 84x27 differential matrix **exactly** over `Q(sqrt(-3))` using SymPy `DomainMatrix`; its rank is 19. Enumerate all `2^12=4096` translation-closed coordinate sets. For sets no larger than 27, the exact rank census is:

| # baryon coordinates | Full rank 19? | Rank distribution |
|---:|:---:|:---|
| 18 | No | rank 15: 48 sets; rank 16: 12 |
| 21 | No | rank 15: 24; rank 17: 96 |
| 24 | No | rank 17: 96; rank 18: 72 |
| 27 | Yes | rank 15: 8; rank 17: 16; rank 18: 72; **rank 19: 72** |

Other sets of size <18 also cannot reach 19 (rank bound plus explicit census). Thus **27 is the minimum number of coordinate baryons in a translation-closed subset with local full rank** for this specific SIC labeling. The machine-readable JSON lists a winning subset and its exact source-orbit IDs.

**Critical qualifications:** (a) this is a **coordinate subset** restriction, NOT an obstruction to a translation-invariant 19-dimensional *linear span of baryon combinations*; (b) the constants `b_ijk=B_ijk(Q*)` must transform compatibly with the proposed H27 symmetry, not automatically; (c) 27 independent linear multipliers for 19 local baryon ranks introduce eight *additional* massless multiplier directions unless symmetry-legal quadratic/cross interactions lift them; (d) nothing here derives these matter fields from an E8 representation or checks quantum-corrected vacuum selection. This precisely identifies why naïvely making the earlier 19-target construction symmetry closed is not enough.

## 4. Exact detector-bias cancellation by three or nine qutrit Weyl settings

Earlier repo calibration scans showed that a color-biased detector `eta` yields apparent loop character `m(K)=3Tr(eta K)/Tr eta`, not invariant under a gauge-frame conjugation `K->UKU†`; an identity-loop reference still gives three and therefore cannot calibrate this bias.

There is a constructive fix if **physically controlled, phase-stable conjugations** of the loop/readout can be implemented. For `W_ab=X^a Z^b` in the three-dimensional Weyl group,

`(1/9)sum_ab W_ab† eta W_ab = Tr(eta)/3 I`, so

`(1/9)sum_ab [3 Tr(eta W_ab K W_ab†)/Tr eta] = Tr K`.

That is **exact for every 3x3 K and any fixed Hermitian detector response eta**, including nondiagonal responses. For a *diagonal* detector, just three settings `X^a`, `a=0,1,2`, suffice to cancel the bias by cyclic mode permutations. For arbitrary non-diagonal eta, the three-shift average does NOT generally cancel bias; the complete nine-Weyl average does. In 48 randomized `SU(3)` commutator-loop checks across diagonal/rotated detectors, nine-setting maximum complex-character residual is `4.97e-16`. One diagonal-detector example has uncorrected character error `.300`, yet 3-shift and 9-Weyl error vanish; a rotated-detector example has uncorrected error `.647`, 3-shift residual `.443`, nine-Weyl residual negligible.

With the earlier ideal balanced Bernoulli optical model, common visibility `v=.8`, target complex-trace absolute accuracy `epsilon=.2`, and confidence `1-delta=.99`, a union-of-Hoeffding bound requires **8,426 accepted detections per phase**, now distributed among the twirl settings. This bound assumes independent trials and controlled phase/visibility **identical across all Weyl settings**. In a physical multiport, coherent conjugation errors, time-varying detector effects, unequal setting illumination and superselection rules can defeat the cancellation. It is a proof about readout calibration, not a deployed photon experiment, dynamical SU3 gauge simulation, or TOE-specific prediction.

The qutrit Weyl 1-design theorem itself is established prior art; our increment is its exact application to the explicit **mode-biased non-Abelian trace** problem from the preceding repo experiments.

## 5. Albert algebra / real G2: three seven-dimensional copies force multiplet degeneracies

The exceptional Albert Jordan algebra has a canonical real presentation `H3(O)` with three real diagonal entries and three offdiagonal octonions. Restrict the compact `G2=Aut(O)` action. Since each real octonion is `1 ⊕ 7` as a G2 module, **the 27-real-dimensional Albert carrier decomposes exactly**

`H3(O)|_G2 = 6*1 ⊕ 3*7`.

Independently construct the standard positive Fano 3-form. On seven imaginary octonions, its infinitesimal skew stabilizer has 21 unknown skew generators, exactly seven independent constraints, hence 14 generators. The exact commutant of those 14 on the irreducible real 7-space has dimension one (full 686x49 rational linear system rank 48): **only scalar multiples of identity** commute with compact G2.

Consequently, the most general *real symmetric* G2-equivariant mass quadratic form on this specific 27 carrier is an arbitrary symmetric 6x6 singlet block plus a symmetric 3x3 multiplicity block tensored with `I7`—exactly `21+6=27` real parameters; every charged seven-multiplet mass eigenvalue remains **sevenfold degenerate**. A tested random symmetric mass commutes with the 14 G2 generators and has three non-singlet eigenvalues each repeated seven times. This provides a concrete constraint on any proposed 3-family interpretation in a real G2/Albert toy. It is NOT a global chiral Dirac spectrum or physical 4D particle mass mechanism; compact G2 representation symmetry must be broken or enlarged for more general patterns. The representation-theoretic branching is standard mathematics, not claimed new to the literature.

## 6. Causal orientation: an odd cubic degree witness detects 23/24 dual pairs, but not all

Independently enumerate the 63 nonisomorphic five-event partial orders by transitive closures of all 1024 naturally ordered edge subsets and exact canonicalization over all 120 permutations. The 63 classes contain 15 self-dual classes and 24 pairs of non-self-dual causal orders. The previous undirected Hasse spectra and inverse Frobenius response are exactly insensitive to `P->P^op`.

For each event i, let `p_i` count strict predecessors and `f_i` count strict successors. Define the intrinsic orientation-odd scalar

`A3(P) = sum_i (p_i^3-f_i^3)`.

It satisfies `A3(P^op)=-A3(P)` and detects **23 of the 24** non-self-dual pairs. Exactly one non-self-dual pair has `A3=0` on both partners. The certificate contains both 25-bit canonical adjacency keys for this blind pair; one Hasse-edge presentation is `(2->1,3->2,4->0,4->2)` (labels are not canonical physical clocks).

For directed Hasse adjacency H and `G=(mI-alpha H)^-1`, the old scalar response `||G||_F²` is even under reversal, whereas the **antisymmetric response tensor** `G-G^T` changes sign when the causal order is reversed. Reading the sign requires oriented source/detector labels, not an unmarked scalar spectrum. Neither statistic constitutes a physically generated arrow, a time-directed quantum gravitational measure, a Lorentz-invariant continuum action or proof of emergent 4D Einstein dynamics.

## Five independent next research gates

1. **Symmetry-respecting SIC UV:** Search for *linear-combination* H27 baryon multiplets with a 19-dimensional invariant source, not just coordinate-orbit closure. Derive symmetry-compatible holomorphic masses for surplus multipliers and enforce the E8 matter branching and anomalies before claiming a physical vacuum.
2. **Reliable photonic multi-time certification:** Make the qutrit witness robust against realistic state-preparation and process-tomography uncertainties. The hard numerical target is to retain a statistically significant negative witness at output depolarization materially below 1.03%, with pairwise-classical certificates and explicit heralding/loss model.
3. **True gauge-twirl hardware:** Compile the 3- or 9-setting coherent Weyl conjugations into a realistic photonic multiport, quantify pulse infidelity, temporal drift and setting-dependent visibility; test that the color-twirl residual is smaller than statistical error.
4. **Physical G2/E6 charged fermions:** Select an actual compact/singular 7D manifold and bundle, derive the 7D Dirac index and real-form kinetic action, and determine whether an anomaly-free 4D three-family spectrum exists with realistic nondegenerate Yukawas. Do not count three real sevens as three chiral Standard Model families.
5. **Causal spinor/arrow dynamics:** Couple an operational oriented propagator to spinorial matter and examine 4D causal sprinklings and order-dependent amplitudes. Show how a T-symmetric fundamental law can still accommodate an operational arrow without inserting sign-sensitive boundary data by hand.

**Outcome:** Six new exact/numeric finite-model controls and 23 focused regression tests; no claimed quantum gravity, E8 completion, real particle-mass prediction or experimental physics beyond established quantum theory.
