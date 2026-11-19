# TOE follow-through: a 19-dimensional W33 logical module, optimal qutrit checks, and four physical falsifiers

**Date:** 2026-11-19 (America/New_York 2026-11-18 late evening).
**Scope:** exact finite-field and group computations, explicitly constrained analytic field-theory and spin-geometric results, and conditional photonic/noise models. **This does not solve the Theory of Everything.**

## Repository provenance and collision check

Started from GitHub/local master `22a122ec8`, preserved all preexisting dirty tracked files and independent untracked files. Reopened the exact source files rather than inferring their contents from summaries:

- `analysis/toe_20261119_w33_40_qutrit_css.py`: preexisting [[40,19,4]]_3 CSS pairing, dX=4, dZ=6.
- `analysis/PASS4948_MODULAR_BOSE_MESNER_CORRECTION.md`: **prior** W33 modular adjacency radical and 10/19/10 Loewy sequence.
- `analysis/PASS7701_7740_LEECH_H27_POLARIZATION_CODE_WELD.md` and `analysis/w33_pass7733_7740_leech_quadratic_code_weld.py`: **prior** common [40,11,13]_3 and [40,10,18]_3 row spaces and 234-polarity independence.
- `analysis/toe_20261105_mub_qutrit_memory_witness.py`: **prior** complete four-MUB qutrit Bell witness, optical compiler, and IID calibrated-loss shot estimates. We do NOT claim discovery of the MUB witness.
- `analysis/toe_20261118_H27_explicit_E8_248_embedding_charge_sectors.py` and `analysis/2026-11-18_native_E8_C9_Clifford_link_Higgs_G2_qutrit.md`: **prior** E8 branching, (E6 x SU3)/Z3 common center, and forbidden (27,1) rep.
- `analysis/2026-11-19_H27_Y7_torsion_gerbes_and_positive_Ricci_no_go.md`, `analysis/2026-11-18_H27_S5T2_G2_sextic_SIC_E8_center_sequential_qutrit.md`: **prior** Y7 topology, integral cup relation and flat Dirac gap.
- Parallel local `867f70b`: **prior** cubic renormalizable ten-pair anomaly-free classical SIC model, distinguished below from the earlier nine-pair EFT.
- **Concurrent commit `3edb3b9` was published during this audit, before this packet:** `analysis/toe_20261119_w33_code_gate_and_decoder.py` and `analysis/toe_20261119_four_structural_frontier_tests.py` independently establish the Nf>=N² one-loop SIC constraint, torus-only nonflat Dirac gap, qutrit SWAP causal-break test, finite graph differential calculus, a **stronger** diagonal T9 transversal no-go, logical T9 magic injection, and a bias-aware **tX=1,tZ=2** decoder. Their 12 tests pass. All such overlapping results below are consistency checks or refinements, **not novel discoveries attributed to this packet**.

**Further concurrent update:** commit `5bd07266` independently established the enlarged **PGL(4,3)** code automorphism group (order 12,130,560), the same *optimal 323-support* CSS basis, a bias-aware decoder, one-loop/flux audits, four-MUB shot design and Cartesian cycle-grid refinement. The mathematical 323 lower bound and PGL action are **already published there**, not discoveries exclusive to this packet. We independently reverified them and extend the published picture with the **inherited nondegenerate 19-dimensional orthogonal form, a faithfulness proof for the full PGL4 action using PSL simplicity, a separate balanced minimal-weight basis of maximum data degree 9, a fully explicit collision-free 18-layer 323-gate incidence schedule**, and transfer of the stronger parallel bias decoder to this balanced basis. The integral c1=3m eta and cover-flux degree9m calculation and a strict *unconditional local-MUB* efficiency/loophole test are further incremental results. Uniform T9 failure, a weaker one-site decoder, the product flux gap and externally imposed grid refinement overlap with the parallel papers and are not claimed as first discoveries.

External background consulted: Acharya/Witten G2 chiral matter (https://www.sciencedirect.com/science/article/abs/pii/S0550321302006120), N=1 SQCD and Seiberg windows (https://doi.org/10.1007/978-3-032-09219-9_18), higher-order quantum/process tomography (https://journals.aps.org/prxquantum/abstract/10.1103/92c4-g7qs), and qutrit magic distillation (https://journals.aps.org/pra/abstract/10.1103/61q5-f754). The new results below are derived in the accompanying code; citations provide context rather than claiming external physical verification.

## 1. Quantum coding: identify the W33 Loewy middle layer as the logical carrier

Let V=F3^40, J the all-ones matrix and A the W33 point-adjacency. Put N=A+I, C11=row_F3(N), C10=row_F3(J-N). Previously proved: dim C11=11, dim C10=10, C10 is self-orthogonal and C11=<1> direct-sum C10. The 40-qutrit CSS code is H_X=N, H_Z=N-J, hence

    L_X=ker(H_Z)/row(H_X)=C10^perp / (<1> + C10),
    L_Z=ker(H_X)/row(H_Z)=C11^perp / C10.

Because <1,1>=40=1 mod3, every class of L_X has a unique sum-zero representative. Therefore BOTH logical carriers identify with the same 19-dimensional space

    L=(W intersect C10^perp)/C10, W=1^perp.

The coordinate dot product on W intersect C10^perp has radical **exactly C10**: its orthogonal complement in V is C10+<1>, and <1> intersects W trivially. Thus the induced bilinear form on L is nondegenerate.

Certificate: an explicit F3 complement has dimension19, Gram rank19 and determinant1 mod3. Five symplectic transvections acting on the 40 projective F3^4 points generate **all 25,920 projective symplectic point permutations**. Exact closure and kernel testing proves their induced action on L is **faithful** and preserves this symmetric form. Hence the W33 code carries a concrete faithful representation

    PSp(4,3) -> O(L,dot), dim_F3 L=19.

This is a direct gate/operator bridge: each point permutation preserves both CSS stabilizer spaces and therefore maps the encoded 19-qutrit space to itself. It does NOT imply easy local routing, hardware fault tolerance, or E8 physical dynamics. The 10/19/10 modular sequence and classical weight enumerators were already known; identifying the 19-space as both logical sectors plus its faithful orthogonal action is this packet's contribution.

**Extended symmetry certificate (building on parallel `5bd07266`):** The 40-point CSS *row spaces* are preserved by the entire PGL(4,3), not only the graph-preserving PSp(4,3); the PGL result and transvection Jordan ranks were first reported in 5bd07266. We verify all 13 elementary generator matrices on the exact quotient \(\mathcal L\), show that every induced 19-by-19 matrix preserves the above dot-product Gram form, and reproduce the elementary transvection nilpotent ranks (10,3,0) and Jordan multiplicities (2,4,3). **Faithfulness of the entire 12,130,560-element PGL action follows without enumerating its elements:** PSL4(3) is simple and index two; one elementary PSL transvection acts nontrivially, so the representation kernel intersects PSL trivially. Any remaining kernel has order at most two and is normal in the centerless PGL, hence trivial. Therefore \(\mathrm{PGL}_4(3)\hookrightarrow O(19,3)\). This adds an explicit orthogonal interpretation and a faithful-kernel proof to the parallel PGL logical-action construction.

## 2. Quantum engineering: a PROVEN minimal-weight check basis

Full finite enumeration gives the **preexisting** classical weight distributions:
- C11=[40,11,13]_3: exactly80 nonzero weight-13 codewords, the 40 projective closed-neighborhood rows with their negatives.
- C10=[40,10,18]_3: exactly1560 nonzero weight-18 words (780 projective).

We select 11 independent weight-13 X stabilizers and 10 independent weight-18 Z stabilizers, with zero CSS symplectic product, and give ALL 21 explicit vectors in the JSON certificate.

The original straightforward independent check presentation costs

    11*13 + 10*27 = 413 ancilla-data two-qutrit interactions.

Our exact basis costs

    11*13 + 10*18 = 323 interactions, a 90/413 = 21.79% reduction.

This is the **global lower bound for any independent CSS stabilizer basis** because each of 11 independent X checks must have weight>=13 and each of 10 independent Z checks weight>=18. Since the bound is attained, 323 is mathematically optimal for this metric.

The balanced basis has maximum data-node incidence9, while max ancilla-check incidence18. The bipartite Tanner edge chromatic number is thus18. We actually construct and certify a deterministic **18-layer collision-free incidence schedule**, padding to a 40x40 18-regular bipartite multigraph, repeatedly extracting 18 perfect matchings and deleting dummy edges. Each of the 323 real (check,data,coefficient) interactions appears EXACTLY ONCE in the JSON schedule; every layer uses any check or data qutrit at most once.

**Critical scope correction:** Edge coloring is a valid two-qudit-resource schedule, but concurrent noncommuting X/Z ancilla extraction may introduce ordering-dependent cross-ancilla errors. We have **not proved** an 18-layer coherent joint syndrome-extraction circuit; safe sequential X then Z measurement has an independent collision-free scheduling upper bound of 13+18=31 layers. Ancilla fault propagation, readout, hardware connectivity and repeated rounds remain to be addressed. A 27-round naive *Z-only* basis is no longer necessary even under conservative sequential types.

## 3. Exact minimum-weight decoder, and two logical-gate obstructions

Build independent syndrome lookups for X and Z errors of weight at most1. Each has 81 keys including zero, corresponding to all80 nontrivial one-sector Pauli faults; combined they correct all320 nonidentity single-site qutrit Pauli faults.

Exhaustively enumerate all

    binom(40,2) * 8^2 = 49,920

two-site depolarizing Pauli configurations. Of these, precisely

    6,240 = (1/8)*49,920

are exactly recovered by the two independent weight-one decoders: one site carries a pure X error and the other a pure Z error (either order). All other two-site patterns involve at least two errors of a common sector and cannot be decoded by these deliberately simple lookup rules. The report stores exact per-site error parameters.

**Important contemporary correction:** The parallel 3edb3b9 decoder is strictly stronger: it corrects one X-component error and **two** Z-component errors. Rather than claiming that algorithm as new, we imported its exact decoder and verified **81 X plus 3,201 Z syndrome entries** on our optimized 11×13 and 10×18 check bases, giving 259,281 jointly correctable component patterns. The 6,240/49,920 figure above describes only our simpler baseline, **not** the full capacity of the parallel decoder. This merger retains its higher correction radius at the newly proven minimum measurement interaction count 323.

For independent per-site depolarizing error probability p, a rigorous guaranteed recovery-probability bound is

    P_success >= (1-p)^40 + 40p(1-p)^39
                + (1/8)*binom(40,2)p^2(1-p)^38.

The inequality is **not** an exact full logical-error law beyond two faults; degeneracy and higher-weight coincidences may add correctable events. The code's minimum distance4 certifies correction of every arbitrary **single physical-site** Pauli error, not generic two-site errors.

Two tempting gates are invalid:

- Uniform transversal qutrit ninth-root cubic T9=diag(zeta9^(j^3)) does not preserve the CSS code. On a weight-13 X stabilizer h, the encoded-zero superposition gives relative phases 1 versus zeta9^13=zeta9^4, not equal. This exhibits a specific codeword-level failure.
- Uniform tensor Fourier swaps the pure X and Z stabilizer groups, whose ranks differ 11 and10, and therefore cannot preserve the same stabilizer code.

The faithful PSp(4,3) point permutations **are** logical code automorphisms. Universal logical quantum computing requires a different non-Clifford resource (magic injection, code switching, or a redesigned transversal construction).

## 4. UV SIC model: anomalies, perturbative running, global E8 center

Two preexisting classical SUSY SIC choices:
- Nine SU3 fundamental+antifundamental pairs, 19 holomorphic baryon constraints plus27 bilinears, 46 singlets, **nonrenormalizable** quartic-singlet baryon EFT; Hessian rank92/100.
- Parallel `867f70b` ten flavor pairs, one cubic renormalizable superpotential with45 mesonic+1 baryonic constraints, Hessian rank98/106.

Both cancel the perturbative SU3^3 cubic gauge anomaly by their vectorlike matter. A one-loop N=1 SU3 beta count gives

    b0=3*3-Nf:
      Nf=9  -> b0=0
      Nf=10 -> b0=-1.

**Neither** is asymptotically free by this one-loop test; b0=0 is not proof of conformality, since Yukawa couplings and higher loops matter. For the actual E8 branching under the global compact subgroup H=(E6 x SU3)/Z3, the quotient kernel generator acts on an (R_E,R_F) representation as omega^(e-f), with e,f its E6/SU3 center charges mod3. A representation descends iff e=f mod3.

Thus (27,3),(27bar,3bar),(78,1),(1,8) are allowed, whereas **(1,3),(1,3bar) and (27,1) are forbidden** as representations of the unbroken quotient. The (27,1) obstruction was already in the repo; this packet applies the same rule explicitly to the bare E6-neutral SIC fundamental. This is stronger than a missing field in the E8 adjoint branching: (1,3) fails as an honest representation of H itself. The toy nine/ten-flavor SIC VEV cannot simply be assigned to elementary (1,3) fields without changing gauge/global structure. The actual E8 (27,3) contains E6 charge and requires a different F/D-flat analysis.

**Open physical target:** an E8-compatible source for tuned SIC parameters and an anomaly-consistent chiral spectrum, with quantum corrections and dynamical scale control.

## 5. Nonflat flux is still insufficient on the specified smooth H27 7-manifold

Recall Y7=(S5(R) x T2)/H27 and its integral ring relation a cup b=3 eta, with eta primitive in H²(Y;Z). A degree-m line bundle from the **quotient base torus** has c1=3m eta; its pullback to the original S5 x T2 cover has torus Chern number9m.

A unitary connection pulled back from that base is constant in S5 directions on the cover. The spin Dirac square splits exactly:

    D7,m² = D_S5(R)² tensor 1 + 1 tensor D_T2,9m².

The nonzero flux sector has |9m| topologically protected **2D torus** zero modes on the cover (with sign as its 2D chiral index), but

    |lambda(D7,m)| >= 5/(2R)

for **every** m. Therefore **no ordinary 7D charged massless Dirac mode is generated by ANY such base-pulled torus-only magnetic flux**. This is genuinely stronger than the earlier flat Wilson twist obstruction.

The primitive class eta does **not** descend from the base (only its triple does), so an eta-flux field with sphere-dependent equivariant connection can escape this *factorized* theorem. Other escapes: non-Abelian sphere curvature, flux-coupled supercovariant operators, singular ADE geometry and localized Callias domains. No explicit successful physical example is claimed in this packet.

## 6. Three-time photonic memory: strict unconditional loss loophole

The repo already constructs a physical local four-qutrit-MUB witness, with projector

    M_match=(I9+3 Phi3)/4.

For every separable state its ideal matched outcome probability is <=1/2. If inefficiency simply erases ideal clicks, an unconditional "both detectors clicked and outcomes match" event is a SUB-EVENT of the ideal match event, so its separable upper bound remains **1/2**, even for adversarial outcome-dependent thinning. The older calibrated expression eta²/2 is only a valid separable null after assuming setting-independent detector efficiencies and fair sampling.

For an isotropic qutrit Bell survival s and independent identical detector efficiencies eta,

    q_click_and_match=eta²(1+2s)/3.

Thus the conservative uncancelled-loss witness requires

    eta > sqrt(3/[2(1+2s)]).

At s=.35 this means eta>.9393. At eta=.85 no amount of additional shots beats the unconditional separable null (q<.5) under this witness; a conditional click-postselected analysis must explicitly declare its fair-sampling assumptions.

**Why this is not a contradiction with parallel 3edb3b9:** that report uses an *entangling global Bell projection* and one joint event-ready efficiency eta, whose separability bound is 1/3; this report uses *local four-MUB measurements* with two independently detected qutrits (coincidence eta squared) and a separability bound 1/2. They are different physical POVMs and different efficiencies. Our stricter local measurement threshold adds an engineering tradeoff rather than superseding the parallel global Bell witness.

For q>.5, false-positive <=alpha and power >=1-beta can be guaranteed conservatively using Hoeffding with

    n >= (sqrt(log(1/alpha))+sqrt(log(1/beta)))² / [2(q-1/2)²].

This is a sufficient IID shot bound, not a tight likelihood-ratio optimum or device-independent claim. It exposes precisely which engineering assumptions matter before promoting a numerical causal-memory signal to a physical observation.

## 7. Why 40 W33 points do not by themselves generate 3+1D gravity

The 40-point W33 graph Laplacian has spectrum 0^1,10^24,16^15. There is no intrinsic accumulation of nonzero eigenvalues toward0 in a fixed finite graph.

A controlled mathematical *counterexample to a too-strong no-go* is the artificial Cartesian-product refinement W33 square (C_n)^3 with a=2pi/n. Its product Laplacian eigenvalues are

    lambda=mu_W33 + 4a^-2 sum_{i=1}^3 sin²(pi*k_i/n).

At fixed low momenta the torus-grid branch converges to the 3D spatial Laplacian; the 39 other W33 internal modes remain gapped at mass-squared10 or16. This demonstrates that a **refinement with W33 as an internal finite fiber** can recover ordinary low-energy propagation.

Crucially the 3D grid was **supplied by hand**, not generated by W33 recursion. This construction supplies no dynamical metric, local Lorentz symmetry beyond its ordinary continuum regulator, Hamiltonian/diffeomorphism constraint algebra, gravitational coupling or Einstein equations. It cleanly separates "a finite internal fiber compatible with an imposed continuum" from "spacetime emerges unassisted from W33."

## Reproducible files and checks

Run from repo root:

    python analysis/toe_20261119_w33_logical_decoder_certificate.py
    python analysis/toe_20261119_physics_followthrough.py
    python -m unittest discover -s tests -p test_toe_20261119_five_frontier_followthrough.py -v

New machine-readable certificates:
- `data/toe_20261119_w33_logical_decoder_certificate.json`: all 21 stabilizers, exact projective group audit, 18 explicit collision-free gate layers, full code weight counts, syndrome-decoder counts and transversal no-gos.
- `data/toe_20261119_physics_followthrough.json`: one-loop coefficients, global center charges, magnetic flux indices, loss-efficiency bounds and graph refinement spectra.

Every claim is a mathematical consequence of specified models and assumptions; **none is a verified physical TOE prediction**.

## Top five independent next tasks

1. **Actual E8-compatible SUSY SIC vacuum:** replace the forbidden (1,3) with legitimate H=(E6xSU3)/Z3 representation sections; solve coupled E6/SU3 F and D equations, anomaly matching, RG and quantum stability.
2. **Physical chiral seven-dimensional operator:** choose a sphere-dependent non-Abelian or singular ADE connection; construct and solve its charged Dirac spectrum/index, including APS/inflow boundary terms, without confusing 2D torus index and 7D chirality.
3. **Photonic loophole-resistant implementation:** design a heralded 4-MUB qutrit Bell-memory experiment, include basis-dependent dark counts and detection-efficiency mismatch, and determine exact finite-shot power beyond IID theory.
4. **Gravitational emergence falsifier:** propose a non-hand-imposed W33 refinement and an explicit Lorentzian dynamical action; test signature, local constraint closure and Einstein limit independently of numerical graph analogies.
5. **Fault-tolerant 40-qutrit architecture:** simulate the full X/Z syndrome circuit ordering, ancillary propagation and erasure, benchmark a practical decoder under noisy repeated measurements, and test nonuniform T9 injection or gauge-permutation logical gates.
