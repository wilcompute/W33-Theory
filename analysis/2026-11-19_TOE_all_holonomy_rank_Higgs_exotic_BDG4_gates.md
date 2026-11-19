# TOE physics-first: rank obstruction, isolated Spin10 Higgs completion, BDG4 scalar recovery, and resource gates

**2026-11-19 | Eight executable gates | CONDITIONAL mathematical/4D effective-field-theory results, not a completed Theory of Everything.**

This packet does not assert a valid compact singular G2/M-theory geometry, a particle-physics fit, a quantized anomaly-free spectrum, or a derived 3+1 quantum graviton. Independent code and a JSON certificate reproduce the exact Lie-root, SU5, Hessian and four-layer moment arguments plus targeted numerical checks.

## Review and novelty audit

Read local GitHub master through `75389b70f7b17d08c1d5fdc2654acf3060fb2709`, plus parallel research `d93f49a1` and `b9e08278`, earlier `eaedca990` and `4ea5ae0`, and exact in-repo `analysis/2026-11-18_optimal_W33_3D_symmetry_E6_global_Wilson_modular_memory.md`, `analysis/2026-11-19_twisted_flat_E8_cups_higgs_and_noise.md`, `analysis/2026-11-19_H27_Y7_torsion_gerbes_and_positive_Ricci_no_go.md`. An ordinary Z7 diagonal Wilson line in Spin10/E6 and its vectorlike twisted-cohomology obstruction were ALREADY derived by the November 18 report. Its Z7 calculation is **reproduced, not presented as a discovery**. The 4D Benincasa-Dowker d'Alembertian was developed in 2010 and is likewise prior art. The useful new-to-this-pass elements are (i) a general ALL-inner-holonomies rank obstruction for the *standard* SM embedding, (ii) a fully counted minimal spinor-Higgs branch and a more complete rank-43 cubic Higgs repair checked against the original E8 charge census, (iii) deriving the extra BDG4 moment from the explicit failed prior 3-layer candidate and testing the full quadratic/boost benchmarks, and (iv) systematic independent orbifold and optical hardware gates.

Key external background:
- https://arxiv.org/abs/hep-th/0203052 (G2 quotients, discrete Wilson lines and membrane effects)
- https://doi.org/10.1103/PhysRevD.103.126027 (3-family E8-localization and phenomenological quark/lepton hierarchy, 2021—prior art for a geometry-based hierarchy)
- https://doi.org/10.1007/s41114-019-0023-1 (2019 causal set review and 4D BDG layer coefficients)
- https://doi.org/10.1103/np89-qzjp (January 2026 local d'Alembertian; arbitrary-field nonconvergence caveat for existing nonlocal operators)
- https://doi.org/10.1088/1674-1137/ade6d7 (Spin10 16x16 symmetric 10 + 126 tensor product and physical Yukawa context)
- https://doi.org/10.1140/epjc/s10052-020-8368-x (2020 supersymmetric SO10 rank-breaking and neutrino contexts)

## 1. The Wilson-line rank no-go holds for ANY number of inner flat holonomies, even a nonabelian fundamental group

The original candidate has gauge Spin10 rank5. SM=SU3xSU2xU1 hypercharge has rank4, and its maximal torus T_SM is **the full rank4 diagonal traceless SU5 torus** for the standard SU5 embedding. Identify a Cartan of Spin10 as R5. Every root of the D5 root system is `e_i-e_j` or `e_i+e_j`, with their negatives, for 1<=i<j<=5: 40 total roots.

A D5 root restricts to zero identically on the SU5 traceless diagonal hyperplane iff its coefficient vector is proportional to (1,1,1,1,1), which NONE of the 40 is. The centralizer of T_SM is therefore exactly Spin10's maximal torus T5, with rank5.

For any subgroup H of **ordinary inner flat holonomies** satisfying SM subset C_Spin10(H), every element h in H must commute with every element of T_SM. Therefore H subset C_Spin10(T_SM)=T5, regardless of pi1 being Abelian or nonabelian. Then T5 subset C_Spin10(H), and the unbroken gauge group necessarily has **rank at least five**. Thus neither one Wilson element nor a family of noncommuting flat Spin10 holonomies can yield exactly standard rank4 SM while preserving that embedding. This root-theoretic argument requires no approximation.

**Escapes requiring truly different microscopic input:** a Higgs branch, flux/nonflat connection, an outer/twisted gauge construction, a nonstandard final SM embedding, or a different unification group. This does NOT exclude all finite-holonomy GUT breaking.

## 2. Reproduce Z7 centralizer and expose its charged-family section problem

For `W=diag(zeta_n^a*I3,zeta_n^b*I2)`, SU5 determinant condition `3a+2b=0 modn`. Within Spin10, adjoint `45=24+1+10+10bar` under SU5xU1chi. The SU5 block preserves 12 SM generators; U1chi adds1. Additional invariant generators in the two 10 sectors have weights `2a` (multiplicity3), `a+b` (6), `2b` (1). Consequently

```
dim C_Spin10(W) = 13 + 2[3*(2a=0)+6*(a+b=0)+1*(2b=0)].
```

Exact enumeration for n2..13 finds first dimension13 at n7; one example `(a,b)=(2,4)`. This is **already present** in prior November18 work. Nonzero ordinary b1 is not required to have a Z7 Wilson loop on an appropriate three-cycle with pi1=Z7; but there is no verified compact singular G2 realization here, and the old L(4,1) base does not support order7 characters.

Newly audited *bulk invariant* component count: one Spin10 16 decomposes as `1+10+bar5` of SU5. Under that n7 holonomy, the trivial flat character occurs only for its SU5-singlet component (one of16). Ten antisymmetric-pair components and five conjugate-fundamental components carry nonzero mod7 phases. These are NOT the actual localized defect zero-mode counts; relative cohomology for nontrivial local systems must be recomputed, and the November18 theorem already finds b2>=1 mirror/exotic partners in nontrivial twisted sectors.

## 3. Rank-breaking with a vectorlike Spin10 spinor pair is locally supersymmetric but leaves 5+bar5 massless

Introduce `A=16_H`, `B=bar16_H`, neutral driver `X`, and `W=X(A.B-v²)`. Set equal aligned SU5-singlet components `<N>=<Nbar>=v`, X=0 and all others0. The full Spin10 D terms cancel between conjugate VEVs; F terms vanish exactly; the unbroken group is SU5. The Hessian on 16+16+1=33 chiral components has exact rank2: the X/N/Nbar sector. Its kernel has dimension31; the broken complexified Spin10/SU5 gauge orbit has dimension45−24=21, leaving **ten genuinely physical massless chiral complex components**, a vectorlike SU5 `5+bar5`. Thus this minimal escape does not produce an isolated supersymmetric GUT vacuum and likely leaves phenomenologically unwanted states.

## 4. One real Spin10 10_H repairs those ten exotics with renormalizable cubics

Add a real `H=10_H` and the allowed Spin10 invariant superpotential

```
W=X(A.B-v²)+(lambda/2) A.A.H+(lambdabar/2) B.B.H.
```

The representation product `16*16` has a symmetric 10, and the conjugate pair can couple to the same real10. Give A,B the aligned pure SU5-singlet VEVs, with H=X=0. There are no tadpoles from two such singlets into H: SU5 and U1chi weights prohibit that coupling. Hence F=D=0 still.

Under SU5 decomposition `16=1+10+bar5`, `bar16=1+bar10+5`, `10=5+bar5`, the cubic terms generate independent masses `lambda*v bar5_A 5_H` and `lambdabar*v 5_B bar5_H`. Both five-plet pairs are massive if lambda and lambdabar are nonzero. We explicitly differentiate a 43-component SU5 expansion of the Spin10-allowed superpotential; its 43 F derivatives vanish and its 43x43 symbolic Hessian equals the independently assembled block matrix, **rank22**, hence kernel21. The kernel count equals exactly the 21 complex broken-gauge directions: zero gauge-invariant local chiral moduli remain in this *truncated 4D sector*. Nothing has been measured or fit.

Consistent formal Z4R assignment `R(A)=R(B)=0, R(H)=R(X)=2` allows all three renormalizable superpotential terms. But its **matter-fermion gravitational R-anomaly coefficient shifts by -16-16+10+1=-21 (odd)** under the prior charge convention. This is not a complete discrete anomaly analysis: gaugino/gravitino, extra neutral multiplets, Green–Schwarz counterterms, global quotient and supergravity need recomputation.

**Most important ORIGINAL E8 spectrum obstruction:** In the source E8→Spin10xSU4, all four 16 charges are e1,e2,e3,e4=−e1−e2−e3, all nonzero. The possible 10 charges are e_i+e_j, also all nonzero and none equals ±2e_i. With a **neutral driver X and a vectorlike pair q_B=−q_A**, both A²H and B²H imply q_H=−2q_A=+2q_A ⇒ q_A=q_H=0 over the charge lattice Z3. Thus this elegant **43-component** cubic Higgs construction cannot be assembled entirely from the existing source's listed 16 and10 zero modes. A different defect spectrum, new charge-neutral chiral multiplets, charged spurions/higher operators, or a different breaking mechanism must emerge from geometry. Do NOT confuse a possible 4D EFT with a genuine E8 compact vacuum.

This is a particularly useful 'find X, then derive Y' bottleneck: **derive the necessary gauge-breaking source representations and anomaly-compatible flat direction before fitting the fermion Yukawas**.

### 4A. Better bridge: keep the existing source 10_34 and dress BOTH Higgs couplings with its existing singlet condensates

The zero-charge cubic Higgs construction in section 4 is NOT present directly in the original E8 source, but it is not the end of the search. Instead of inventing a charge-neutral 10, take the **existing chiral Spin10 ten `10_34`**, whose SU4/Abelian charge is `(-1,-1,0)`, and introduce ONE additional vectorlike Higgs pair `16_H,bar16_H` with charges `(+1,0,0),(-1,0,0)` and one neutral driver `X_new`. The three existing source singlets and charges are:

```
B=S12_conj: (-1,+1,0),  <B>!=0
C=S13:      (+1,0,-1),  <C>!=0
D=S14:      (+2,+1,+1), <D>!=0
```

Two fully U1^3 gauge-invariant Spin10 couplings are then

```
W_eff,5 = (lambda/M) B 16_H 16_H 10_34
        + (lambdabar/M²) C D bar16_H bar16_H 10_34.
```

Check each charge vector explicitly:
`2(1,0,0)+(-1,-1,0)+(-1,1,0)=0`;
`-2(1,0,0)+(-1,-1,0)+(1,0,-1)+(2,1,1)=0`.
The actual old messenger vacuum supplies `<B>=1,<C>=sqrt(2.08),<D>=1` in its illustrative units, giving nonzero coefficients `lambda_eff=lambda/10` and `lambdabar_eff=lambdabar sqrt(2.08)/100` at M10. These values are **chosen EFT units**, not physical GUT scales.

An exhaustive combinatorial search enumerates nonnegative holomorphic monomials of degree <=6 from all eight existing singlets for each of **3 chiral Spin10 spinor charges x 5 existing ten charges**. All 15 pairings admit some dressing; the global minimal **combined degree is 3 singlet insertions**, achieved by the displayed pair (`B` once; `C D` twice) and at least one alternate. The result is minimal *within this field list/monomial cost*, not a universal UV minimality claim.

At the aligned D-flat Higgs VEV, the charged spurions are nonzero and their new interactions supply the SAME two independent SU5 five-plet mass blocks as section 4, with nonzero masses. An explicit symbolic reduced superpotential verifies the F gradients vanish and all mixed Hessian entries between the three spurion fluctuations and the Higgs mass blocks are zero at this vacuum. Hence the independently tested original **19-field singlet Hessian rank16** and new **43-field Higgs Hessian rank22** form a block-diagonal Hessian on the **62 active chiral components**, total rank **38**, with nullity **24**. The U1^3 singlet condensates break 3 gauge directions and the vectorlike Spin10 Higgs VEV breaks 21, totaling exactly24. **No extra local complex physical Higgs/singlet moduli remain in the specified 62-field effective model**.

This is a more source-compatible **conditional four-dimensional EFT construction** than section4's undressed neutral-Higgs version. It REUSES the existing E8 `10_34`, B,C,D, and their nonzero VEVs. It still requires an additional **vectorlike 16+bar16 pair**, not supplied by the original chiral sector, and a new neutral R2 driver. The source has no mirror 16bar zero mode. The two dressed W operators have superpotential degree **4 and5**, so they are not renormalizable by themselves; actual heavy-messenger or local defect/M2 mechanisms producing them are missing. The original Abelian anomalies and protective discrete-R anomaly, Kähler corrections, supersymmetric G2 compactification, true light Higgs, CKM/PMNS and proton-decay gates remain open. **Do not confuse exact charge/F/D algebra with an actual compactification or a physical Yukawa calculation.**

Reproduce:

```powershell
python analysis/toe_20261119_E8_source_dressed_GUT_Higgs_bridge.py
python -m unittest discover -s tests -p test_toe_20261119_E8_source_dressed_GUT_Higgs_bridge.py -v
```

JSON: `data/toe_20261119_E8_source_spurion_dressed_Spin10_Higgs_bridge.json`.

## 5. Repair the causal scalar kinetic operator: the FOUR-layer 4D Benincasa-Dowker kernel

The preceding `eaedca990` construction used weights `(1,-5,4)` for counts of intervals with k=0,1,2 internal points. It made one signed expectation finite, but later `75389b70` demonstrated that on `s=t²-r²`, with Box(s)=-8, the unrescaled combination approaches0. It is NOT a wave operator.

Instead, reconstruct the **known** four-layer scalar retarded d'Alembertian. In a 3+1 Minkowski future cone `0<t<1`, density rho, interval volume `V=pi*s²/24`, require the normalized first four layer weights to satisfy THREE exact moments:

```
M = [[1,1/2,3/8,5/16],
     [1,1,1,1],
     [1/2,3/4,15/16,35/32]]
M*w = 0.
```

The integer primitive null generator is uniquely `w=(1,-9,16,-8)` (up to scale). Its Poisson-weighted continuum polynomial is `e^-z (1-9z+8z²-(4/3)z³)`. The 4D known scalar operator is

```
B_rho f(0)=4 sqrt(rho)/sqrt(6) * (K_rho[f]-f(0)).
```

The exact digamma moment `sum_k w_k Gamma(k+3/2)psi(k+3/2)/k! = -sqrt(pi)/3` gives `B_rho(t²-r²)→-8`. The constant expectation tends1 before subtracting f(0), hence the local counterterm. Independent radial/temporal integrals and density quadratures yield the following at rho=10^6:

| Field | Exact flat Box at origin | Calculated B_rho |
|---|---:|---:|
| 1 | 0 | -0.004582 |
| t | 0 | -0.006072 |
| t² | -2 | -2.009199 |
| x²+y²+z² | 6 | 6.009532 |
| t²-r² | -8 | -8.018882 |
| x² | 2 | 2.003177 |
| boosted (t')² with beta0.6 | -2 | -2.012587 |
| boosted (x')² with beta0.6 | 2 | 1.999790 |

This *reconstructs the published 2010 BD result*, independently checks its four-layer moment system and explicitly repairs the previous 3-layer failure. It does **NOT** establish arbitrary-field convergence, finite Poisson sprinkling variance/low-density concentration, healthy spin-2 gravitons, first-class constraint closure, interacting quantum states, or Einstein gravity. The 2026 local-operator paper specifically cautions against inferring universal convergence from traditional nonlocal scalar operators.

**Next gravity keystone:** derive a causal Lorentzian microaction selecting the operator, its normalization and physical quantum state, and only then derive a consistent tensor/Einstein constraint algebra. Known scalar d'Alembertian is a benchmark, not a new physical fundamental law.

## 6. More precise five-dimensional GUT boundary condition test

For a scalar proxy of a 5D boundary mode with Neumann at y=0, Robin `f'(L)+h f(L)=0` at y=L, the exact dimensionless quantization rule is `x tan x=mu`, `x=kL`, `mu=hL`. It has a zero mode for mu0 and raises the lowest positive mode continuously toward `pi/(2L)` as mu→infinity. With cutoff 1/L=10^13GeV and mu100, the first mode rises to roughly1.56×10^13GeV. A representation-selective boundary term can therefore lift one octet without a cancellation of opposite ~GUT-scale bulk masses in this simple spectral proxy. But the actual 5D fermion/Majorana boundary problem has different first-order boundary conditions, and one octet plus two triplet zero modes requires a genuine symmetry-permitted SM-brane operator. This toy spectrum is a necessary mathematical diagnostic, NOT a solved GUT, 2-loop unification or proton-decay result.

## 7. The one-photon architecture still pays for its qubit register

In a single-photon, one-of-d orthogonal mode basis, n logical qubits require d>=2^n. Even implementing one logical Pauli-X acting on the highest bit as a permutation of physical modes requires 2^(n−1) disjoint independent mode swaps in the explicit unary optical encoding; a general U(d) has d² real parameters. Verified swap counts for n=4,7,10,12 are **8,64,512,2048**. These are encoding-specific hardware requirements, NOT a bound on every possible multiplexed hardware controller or adaptive multi-photon architecture.

**Experimental selection-bias gate:** A calibrated null p0=.50 can be transformed into an observed successful-event frequency pobs=.51 if success trials have relative acceptance odds 51/49≈1.040816 times failure trials. Thus a mere **4.08% success-dependent selection bias can imitate a hypothetical 1% absolute deviation**, even if 55,000 accepted trials give overwhelming nominal statistics. This is a quantitative calibration demand, NOT a derived nonstandard TOE prediction.

## 8. What finding the first missing piece buys us

The cleanest high-leverage *particle* keystone is no longer a phenomenological numerical fit. It is a **globally valid source for one vectorlike Spin10 Higgs pair and the two specific B / CD spurion-dressed superpotential terms**, compatible with the already present E8 singlet and 10_34 fields, together with quantified anomalies and nonzero actual localized amplitudes. The integrated 62-active-component EFT passes local F/D and mass counting, while the required vectorlike Higgs zero modes, microscopic higher-dimensional interactions and anomaly/R global closure are missing. Deriving their origin could enable a single global background to test rank breaking, source chirality and Yukawas rather than gluing unrelated models.

The independent *gravity* keystone is a genuinely derived dynamical action: the known four-layer BDG scalar kinetic operator passes selected flat tests, but the choice of action, tensor constraints and quantum vacuum remain arbitrary inputs. Reproducing a known differential operator is necessary but insufficient.

The *computational/experimental* keystone is a physically resource-efficient non-Gaussian mechanism that gives a genuine prediction different from standard QM. Numerical codes and mode counts do not manufacture an experimental distinction.

### Reproduction

```powershell
python analysis/toe_20261119_all_holonomy_rank_BDG4_higgs_exotics.py
python -m unittest discover -s tests -p test_toe_20261119_all_holonomy_rank_BDG4_higgs_exotics.py -v
```

JSON certificate: `data/toe_20261119_rank_Higgs_BDG4_boundary_photon_gates.json`. Tested against parallel `tests/test_toe_20261119_two_GS_axions_causal_layer_and_Bell_gates.py`, `tests/test_toe_20261119_dependency_first_GS_causal_photon_modes.py`, and `tests/test_toe_20261119_twisted_flat_E8_higgs_and_noise.py`. Independent JSON content, finite root enumeration, symbolic F/Hessian and numerical quadratures all included; full repository CI not run.

## Top five independent next experiments

1. **Compact particle origin:** derive the missing vectorlike 16_H + bar16_H and neutral driver from a globally consistent singular G2/E8 defect source, while reusing the original 10_34, B,C,D via the derived one- and two-spurion operators. Derive their microscopic coefficients and check all Abelian/Spin10/gravitational/discrete-R anomalies plus twisted family indices.
2. **Physical flavor amplitudes:** compute one actual defect/M2 localized Yukawa coefficient—nonzero under the source's flat/local coefficient system—and check that full-rank CKM/PMNS/Higgs projections can follow without input mass fits.
3. **Orbifold fermion completeness:** replace Robin scalar proxy with honest five-dimensional Dirac/Majorana boundary equations, symmetry-protected octet mass, complete KK/regulator matching, and proton lifetime.
4. **Gravity-action derivation:** use the BDG4 four-layer field tests as a BASELINE, then test arbitrary smooth fields, stochastic variance, reflection positivity, spin2 poles and the nonlinear first-class Einstein constraint algebra in 3+1.
5. **Photonic decisive resource:** derive a hardware-polynomial active/nonlinear resource and a nonstandard quantitative probability or process-tensor prediction; preregister event-ready measurements robust against >=4% relative acceptance bias and other loss/drift channels.

**Conclusion:** The nearest tractable particle crack is exact source-field provenance for a rank-reducing, moduli-free Higgs sector; the nearest tractable gravity crack is a selected first-class causal action, not an elegant finite signed count. None is yet a fundamental TOE.
