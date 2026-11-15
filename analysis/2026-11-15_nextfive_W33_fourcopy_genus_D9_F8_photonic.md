# TOE next five and more: covariant four-copy E6 quantum instrument, exact F8 purity counterexample, genus-six polyhedral search, D9 KK vectors, and model-free optical readout

**Date:** 2026-11-15. **Repo:** wilcompute/W33-Theory, master. **Scope:** exact finite geometry and explicitly qualified physical models. Not a Theory of Everything proof. Prior repo commits `984296660`, `20dee36bc`, `332f410e9`, `c23c8b5eb`, `f8ecf3187` were inspected and built upon, not duplicated. Source filenames and tests below are authoritative.

## Executive evidence

1. A **fully W33-symmetry-covariant** CP trace-nonincreasing quantum operation on **four copies** of a 40-mode state is explicitly constructed. It outputs all 27 cubic-line labels and includes the previously inaccessible six-dimensional Schläfli sector. Its finite-dimensional Kraus matrix and a failure complement exist exactly; no efficient optical circuit is claimed. The uniform coherent state has **19.881818%** ideal heralding probability, whereas Haar-random pure inputs average only **0.0119336%**.
2. A genus-six `K12` simplicial map's dual planar-face ansatz `12×3=36` coefficients was optimized from a previous best of **41** to **8** nonadjacent proper boundary-edge self-crossings. The subsequent **90,000** local trials did not improve it; the best candidate still FAILS the necessary simplicity test. All 8 crossings are independently certified using **exact rational arithmetic** on the saved decimal coefficients, not merely floating-point signs.
3. The D9 Einstein–Maxwell `S2×S2` first vector harmonic step is completed **kinematically**, not dynamically: in the finite `l1,l2≤8` mode window, there are **6,560 exact** and **19,360 coexact** one-form harmonics. The six `l=(1,0),(0,1)` Killing coexact modes are mandatory gauge zero-mode combinations after metric/Maxwell mixing, even though their un-mixed Hodge eigenvalues are strictly positive.
4. A five-generator isotropic Pauli subspace **entirely uncovered** by the F8 regulus's 567 measured Paulis yields a rank-two mixed six-qubit state with `Tr(rho²)=1/2` and *zero* covered certainty objective. All three logical Pauli cosets each have exactly **three** covered labels, so **within this two-dimensional stabilizer code** `C(rho)=6 Tr(rho²)-3`. The construction is checked both at the finite-field symplectic-label level and with an actual `64×64` Hermitian Pauli-projector density matrix, including four Bloch-radius tests. This is not a counterexample to a pure-state lower bound.
5. A **full-model-independent contrast-specific** detector-calibration scheme estimates only 16 witness contrasts rather than all 256 entries of the confusion matrix. With 52,642 accepted calibrations per rail and 147,556 for each parity reference, the total conservative sufficient budget is **1,137,384**, versus the previous strict-circulant pooled budget of 6,573,041 and unstructured full-matrix budget of 153,290,096. The fresh synthetic five-setting GHZ witness has conditional **joint 99% lower fidelity 0.9204561**. Correctness does **not** assume cyclic detector response, although the simulated true matrix happens to be circulant.

## Research front 1: the exact four-copy CP map, and its quantitative input-state bottleneck

**Code:** `analysis/toe_20261115_symmetric_fourcopy_W33_E6_heralded.py`.
**Data:** `data/toe_20261115_full_equivariant_fourcopy_quantum_channel.json`.

Previous repo passes built the 45 induced `K_{4,4}` W33 octets, the disjoint-octet graph `C=SRG(45,12,3,3)`, and its 27 maximal five-cliques corresponding to cubic lines. The previous 2026-11-15 quartic construction used **one arbitrarily chosen unordered nonedge point pair per octet**, giving 270 one-hot four-point selectors with `R^T R=10I_{27}`. That basis-choice operation is not itself W33-equivariant on physical input point labels.

This pass enumerates **all 12 unordered nonedge pairs within each K4,4 octet** (six in each bipartition). Every such point pair belongs to *exactly one* of the 45 octets. For each of the 270 disjoint-octet pairs there are 12×12=144 decompositions into two nonadjacent pairs, giving 38,880 quartic *pair decompositions*. Distinct unordered four-point subsets number **22,680**: 6,480 have one decomposition, and 16,200 have two. Their two decompositions may point to distinct cubic-line labels. This collision phenomenon must be retained: simply declaring 38,880 orthogonal four-point states is FALSE.

Let `M` be the exact nonnegative integer `27×22680` matrix: `M_{ell,S}` counts decompositions of the four-subset `S` into disjoint-octet pair certificates belonging to cubic line `ell`. The full **integer Gram identity** is

`M M^T = 1440 I_27 +24 A_27 +60(J_27-I_27-A_27)`,

where `A_27` is the classical Schläfli graph adjacency (`10^1,1^20,(-5)^6`). Thus

`spec(MM^T) = {2640^(1),1344^(20),1560^(6)}`, **rank exactly 27**.

The 6D dark sector of every scalar `45×27` linear incidence factorization is now genuinely reached. This full map was checked against **all 40 projective symplectic transvections**, simultaneously acting on 40 input rays and 27 output lines. Unlike the selected-witness construction, the all-pair operator is equivariant.

Now work on `Sym^4(C^40)` (dimension `C(43,4)=123410`). For each four-distinct-point occupation state `|S>` in the **normalized bosonic basis**, set `K|S>= sum_ell M_{ell,S}|ell>/sqrt(2640)` and let K vanish on repeated-label basis states. The verified Gram eigenvalues imply `K K†≤I_27` and therefore `K† K≤I_{Sym4}`. The completely positive success map `rho→K rho K†` is trace-nonincreasing. Add a failure Kraus `F=(I-K†K)^(1/2)` into an orthogonal failure-output space, giving an **exact trace-preserving two-outcome instrument** and an abstract unitary/Stinespring dilation. We have not compiled F or K into a spatially local beam-splitter, photonic interaction, or constant-depth circuit.

For `|+>=(1/sqrt(40))Σ_p|p>` the four-copy input has amplitude `sqrt(24)/40²` on each four-distinct-point bosonic basis state, yielding **P(success)=0.198818181818...**. However the normalized Haar fourth moment is the projector on `Sym4` divided by its dimension; therefore

`E_Haar P(success) = tr(MM†)/(2640*C(43,4)) = 38880/(2640*123410) = 0.000119336137487...`.

For independent random phases at fixed uniform amplitudes, quartet interference terms cancel, giving

`E_phase P(success)=24*38880/(2640*40^4)=0.000138068181818...`.

The coherent-uniform case is about **1,666 times** the Haar average and **1,440 times** the random-phase average. This creates a concrete, not merely conceptual, resource barrier to physical use. No positive **single-copy** effect can reproduce the success probability for every pure input: all 40 computational basis rays give success zero, forcing any hypothetical positive single-copy effect to be zero, while the uniform superposition succeeds. Four coherent copies are sufficient *abstractly*; they have not been shown necessary for every possible alternative 40→27 map.

## Research front 2: genus-six dual 12-plane search and exact failure certificate

**Code:** `analysis/toe_20261115_genus6_plane_optimization.py` and `analysis/toe_20261115_genus6_exact_rational_crossings.py`.
**Data:** `data/toe_20261115_genus6_12plane_optimized_necessary.json`, `data/toe_20261115_genus6_12plane_exact_rational_crossings.json`.

Previous `FACETS_ONE` from `analysis/w33_genus_six_execution.py` is an abstract orientable neighborly genus-six triangulation with `V=12,E=66,F=44`; its dual has `V=44,E=66,F=12`, and each face is an 11-gon. Rather than vary 44 independent spatial vertices, represent the 12 dual face planes by `z=a_i x+b_i y+c_i`, 36 continuous numbers. Each dual vertex is the intersection of the three face planes indexed by a primal triangle; each dual face boundary is the 11-cycle around a primal vertex.

The new seeded stochastic local search evaluated 9,000 proposed moves from six restarts, reducing a prior random best count of 41 to **8** proper crossings between **nonadjacent edges of a single face**. A further 90,000 moves with perturbative warm restarts did not improve the score. The saved coefficients have minimum absolute triple-plane normal determinant >0.6 (so the selected 44 vertices are well-defined) and maximum vertex distance ≈29.6 in the chosen affine coordinate chart.

Crucially, another independent validator parses the saved 36 *decimal strings as exact rational numbers*, reconstructs each vertex with 2×2 Cramer's rule, computes every polygon orientation sign using exact fractions, and obtains per-face crossing vector

`[1,0,1,1,1,0,0,2,0,2,0,0]`, summing to **8**.

There are **zero** tested zero-orientation degeneracies for nonadjacent boundary-edge pairs. Thus the saved candidate is **definitively not** a polyhedral embedding, despite the improved search score. An actual realization would additionally require all 12 faces simple and all nonincident edges/face interiors mutually nonintersecting.

For current external context see Bokowski and Kevin H., *Symmetry* 17 (2025) 622, §8.3 (https://www.mdpi.com/2073-8994/17/4/622): numerical search for all 59 such abstract duals was unsuccessful; this is not a theorem for the nontriangular dual. Schewe's theorem (https://arxiv.org/abs/0801.2582) prohibits the **primal triangular** K12 polyhedral embeddings; it is not by itself a dual no-go.

## Research front 3: exact one-form KK Hodge decomposition prior to metric–Maxwell mixing

**Code:** `analysis/toe_20261115_D9_product_oneform_KK_decomposition.py`.
**Data:** `data/toe_20261115_D9_S2S2_Hodge_vector_KK_pre_mix.json`.

On round `S²(r1)×S²(r2)`, a scalar product harmonic of angular degrees `l1,l2` has multiplicity `g=(2l1+1)(2l2+1)` and Laplace eigenvalue

`lambda L² = 20[l1(l1+1)+t l2(l2+1)]/(1+t)`, `t=r1²/r2²`.

Hodge theory gives **one exact 1-form polarization** for every nonconstant scalar harmonic. The number of **coexact** polarizations is:
- zero at `(0,0)`;
- one if exactly one `l_i>0`;
- three if **both** `l_i>0`, given by the two coexact sphere-specific `*d_iY` modes plus a divergence-canceling combination `lambda_2 d_1Y - lambda_1 d_2Y`.

Enumerating the full `0≤l1,l2≤8` finite window gives **6,561 scalar harmonics**, **6,560 exact 1-form modes**, **19,360 coexact 1-form modes**, and **25,920 total 1-form modes**. These counts are verified against closed forms with `S=(L+1)²=81`: exact `S²−1`, coexact `3(S−1)²+2(S−1)`.

Within the coexact spectrum, the `(l1,l2)=(1,0)` and `(0,1)` modes comprise **six Killing directions** (three rotations of each sphere). They have **positive raw Hodge eigenvalues** `2/r_i²` even though gauge-compensated SO(3)×SO(3) symmetry of the magnetic background mandates six **physical five-dimensional massless vectors** after graviphoton–Maxwell mixing. Therefore, any purported full KK spectrum that simply assigns raw Hodge eigenvalues to the six would-be gauge bosons is false. This is a useful exact spectral and gauge bookkeeping constraint; the actual coupled mixed KK mass matrices, gauge-fixing and stability analysis remain to be derived.

Reference: Brown–Dahlen, general Einstein–Maxwell product fluctuations (https://arxiv.org/abs/1310.6360).

## Research front 4: F8 purity dependence and the field-trace dual-basis trap

**Code:** `analysis/toe_20261115_F8_mixed_purity_stabilizer_falsifier.py`.
**Data:** `data/toe_20261115_F8_mixed_uncovered_stabilizer.json`.

Use the repo's F8 multiplication and field trace to label the **567 nonidentity covered Pauli operators** as `Q(x,z)=x1 z1 + x2 z2=0` over `F8`. A constructive randomized search returned five binary-symplectically commuting generators with integer labels

`[2778,2315,599,2616,1322]`.

Their 32-element additive span contains **only the identity plus 31 uncovered operators**. The 2-dimensional simultaneous stabilizer eigenspace has normalized maximally mixed projector `rho_0` with `Tr rho_0²=1/2`, and **all covered Pauli expectations exactly zero** in the symbolic subgroup calculation. This is independently verified by an actual `64×64` projector and direct Pauli traces; numerical matrix-check residuals are within the asserted floating tolerance.

**Important basis correction:** the 3 binary bits representing a field element in a polynomial F8 basis are **not generally self-dual under the field trace**. Z masks must be transformed by the binary Gram matrix `W_ij=Tr(e_i e_j)` before constructing six-qubit Hermitian X/Z matrices; otherwise the purported generators fail to commute and the projector fails idempotence. The code explicitly uses `zMask_j=Tr(e_j zField)`. This is a concrete implementation pitfall for proposed F8 QASM/circuit protocols. See Gottesman's QECCbook, finite-field Pauli dual basis: https://www.cs.umd.edu/~dgottesm/QECCbook-2024.pdf .

The 128-element symplectic centralizer of the rank-five subgroup decomposes into four 32-element cosets; beyond the stabilizer subgroup, the **three logical Pauli cosets each contain exactly 3 covered labels**. Hence within this encoded qubit, with Bloch vector `r=(rx,ry,rz)`,

`C(rho)=3(rx²+ry²+rz²)=6Tr(rho²)-3`, for `1/2≤Tr rho²≤1`.

The program verifies this for `|r|=0,0.25,0.6,1` using the actual six-qubit density matrices and all 567 covered Pauli moments. This is an **exact subgroup identity, supported by numerical matrix realization checks**, not a full-C64 pure-state minimum. The exact algebraic **upper** witness remains `(47−32cos(2π/9))/9≈2.4985086467`. The exact PPT lower `2.0818` is restricted to the 16D common code, and the Pass12673 global degree-six SOS `0.7603` is numerical, not an exact rational global certificate.

**Parallel update checked before publication:** newly arrived master commit `212d80effc` (Pass12674, `analysis/PASS12674_F8_CODESPACE_DEG8_CERTIFIED_TO_9_DIGITS_STABILISER_TYPES.md`) proves a far stronger **integer-exact degree-eight SOS bound `64F≥2.498508646` on a specific 8D T stabilizer code space**. It closes that code's pure-state uncertainty bracket to `6.9×10⁻¹⁰`, with the existing exact algebraic upper witness. It does NOT establish the same bound over all 64 complex dimensions. The type-A/type-B 16D code-space reduction remains numerically observed, not proven. We did not regenerate the new exact SOS certificate in this pass; we inspected its repo artifact and scope. Do not apply a pure-state lower bound to arbitrary mixed experimental preparations.

## Research front 5: direct-observable calibration with model-free column handling

**Code:** `analysis/toe_20261115_direct_witness_contrast_calibration.py`.
**Data:** `data/toe_20261115_direct_witness_contrast_calibration.json`.

Given a *fixed nominal* 16×16 detector confusion matrix `C0`, define the ideal two-endpoint rail contrast `v=e0+e15` and its inverse-weight estimator `w=C0^{-T}v`. The **true detector C** may deviate arbitrarily from C0 and need not be circulant. For any unknown actual rail population vector `p`,

`|(w^T C-v^T)p| ≤ max_j |w^T C[:,j]-v_j|`.

Prepare each known rail basis state `j` independently and estimate the **one scalar** `mu_j=w^TC[:,j]` by sampling the weights of its detected outputs. If each output weight belongs to an interval of range R, the 16 two-sided simultaneous Hoeffding inequalities give

`Pr(max_j |muhat_j-mu_j|>r) ≤32 exp(-2 n_C r²/R²)`.

Thus the *observed*, calibration-conditional maximum bias bound is simply

`B_Z=max_j|muhat_j-v_j|+r`.

No full matrix tomography or rail-translation symmetry is required. Independently estimate the two parity-flip rates with `n_P` accepted Bernoulli references each; the corresponding `α_P` bound is `4 exp(-2 n_P δ²)`. Correct the five-setting GHZ witness means and combine simultaneous failure budgets `(α_C,α_P,α_W)=(.0025,.0025,.005)`, which sum to .01.

For nominal signal data `n_Z=12000`, `n_E=8000` in each of four equatorial settings, tolerances `r=.01,δ=.005` and `R≈1.05511`, the sufficient accepted calibration counts are:

- **52,642 per true rail, 842,272 across 16 rails**;
- **147,556 per parity-flip reference, 295,112 for both**;
- **1,137,384 accepted calibration measurements total**.

In a frozen seeded synthetic experiment, the observed `Fhat=0.9632748417`; the 5-setting statistical confidence halfwidth is `0.03216538`; the calibration halfwidth is `0.01065339`. Thus the **joint 99% lower bound is 0.92045607** under the explicitly stated conditions of known input preparations, stationarity, independent trials and a trusted parity calibration. It is NOT real experimental data. A negative-control 16×16 matrix with **only one rail's readout distribution shifted** produces a >0.5 contrast anomaly; the direct-observable calibration is sensitive to this defect without assuming cyclic pooling.

**Crucial distinction:** this certifies the desired single observable rather than the entire unknown detector channel. The shot count is sufficient under Hoeffding and not optimized; imperfections in reference preparations, calibration drift and correlated loss require additional robust inference. The inverse weights require a fixed nominal calibration model to be defined, but validity of the observed contrast bound does **not** require that nominal model to be correct.

## Reproduction / scope gates

```powershell
py -3 analysis/toe_20261115_symmetric_fourcopy_W33_E6_heralded.py
py -3 analysis/toe_20261115_genus6_plane_optimization.py
py -3 analysis/toe_20261115_genus6_exact_rational_crossings.py
py -3 analysis/toe_20261115_D9_product_oneform_KK_decomposition.py
py -3 analysis/toe_20261115_F8_mixed_purity_stabilizer_falsifier.py
py -3 analysis/toe_20261115_direct_witness_contrast_calibration.py
py -3 -m pytest tests/test_toe_20261115_nextfive_quantum_geometry_uncertainty.py -q
```

The genus optimizer is seeded and saves a reproducible best configuration; running it with prior output present performs a **90,000-trial warm-start extension**, not an exact global solver. To replay the saved optimized candidate without stochastic search, invoke the exact crossing validator and relevant pytest test. The 14 new scripts/results/tests/report artifacts are isolated under unique paths; no existing repo source or dirty parallel worktree files are overwritten.

## Five independent future research bets

1. **Quantum hardware:** synthesize the explicit four-copy Kraus operator by a physically realistic low-loss multiphoton circuit or prove a relevant gate-count / postselection lower bound; investigate whether a two-copy alternative can access the six dark Schläfli directions with a different operator alphabet.
2. **Genus-six topology:** add global face-face nonintersection and exact cyclic-orientation sign SAT constraints to the 36-parameter plane model. A computer-assisted no-go proof must address all 59 abstract duals, not only FACETS_ONE.
3. **D9 dynamics:** gauge-fix and diagonalize the coupled metric–Maxwell vector/scalar blocks, reproducing the six protected Killing massless modes before trusting massive KK eigenvalues, then include ghosts and AdS BF bounds.
4. **F8 pure-state certainty:** develop a rigorous global `C64` lower certificate, not a code-space or solver-only bound; test purity-aware experimental witness corrections using the exact rank-two mixed-state family.
5. **Photonic calibration:** build an online contrast-drift monitor and independent rail-preparation verification; optimize allocation of the 16 rail samples and two parity references directly for a desired fidelity threshold rather than generic full-channel accuracy.
