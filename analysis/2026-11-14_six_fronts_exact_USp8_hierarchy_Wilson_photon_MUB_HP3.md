# 2026-11-14 — Exact \(E_6\leftrightarrow USp(8)\) Pauli intertwiner, tensor hierarchy, Wilson selection falsifier, photonic clock, MUB, quaternionic geometry

## Executive result and audit provenance

This pass began at live **W33-Theory master f2e6fa929**, already **46 commits ahead of our previous verified 89d6878ec**. It reviewed the 46 commit subjects and important changed source/report files, especially Pass12656 (Pauli cubic), Pass12657–12663 (finite-field reguli, nonstabilizer witnesses, exact SOS and parity), the generalized M/IIB gauge section files, and the monopole tail work. This is **not** an assertion that every changed source line was read in entirety. The local Windows worktree already contained many unrelated modified/untracked files; they are to be left untouched.

**Main new deliverables:** (1) a completely EXACT integral-Gaussian 28x27 intertwiner and order-6 8x8 Albert-clock lift, (2) first tensor-hierarchy identities on both E6 sections, (3) exhaustive 630-pair compact Wilson selection no-go for this ensemble, (4) loss-aware 35-mode optical reference protocol and single-photon erasure no-go, (5) independent GF2 symmetry and positive-witness checks of the size-8/9 five-qubit Pauli MUB files, and (6) an exact quaternionic-Hopf differential-rank result that constrains the physical reading of 27 charges.

The *known theory* is E6(6) exceptional field theory and USp(8) representation theory, not independently discovered physical spacetime. New is an explicit exact dictionary to our signed 45-term cubic and the specific repo clock, plus machine-checkable falsifiers and more disciplined physics separation.

## 1. EXACT Gaussian-integer USp(8) map and reduced four-coupler clock

**Producer:** analysis/toe_20261114_exact_gaussian_us8_pauli_clock.py

Previous numerical 28x27 highest-weight intertwiner agreed with all 36 compact generators to ~1e-14 but required floating-point eigendecompositions and stored 12-decimal arrays. The new approach starts instead from the independently constructed three-qubit Pauli representation in Pass12656.

Take three-qubit Hermitian Paulis P(v), v in F2^6, with YII antiunitary J=P(YII)K, J²=-I. The elliptic 27-point quadric consists of the nonzero Paulis commuting with J (under the antiunitary action). Its 45 commuting triples have signed cubic
  N_P(x)=Tr[(sum_v x_v P(v))³]/48.
Build the 27-vertex Schläfli incidence graph for BOTH this set and the repository signed canonical cubic; an actual VF2 graph isomorphism supplies all 27 index labels. Solve the 45 coefficient sign equations over GF2. Exactly **eight sign flips** produce termwise equality to the original signed repo polynomial. A dictionary of all 27 labels and all flips is in the JSON certificate.

For each normalized repo basis operator P_i, the antisymmetric 8x8 matrix Z_i=P_i P(YII) defines a vector in Lambda²_0(C8); flatten its 28 upper-triangle entries into a Gaussian integer column B_i. The entire B=2T matrix has exactly **108 nonzero entries**, all 0, ±1 or ±i, and verifies **B†B=4 I27** and exact singlet orthogonality in Z[i].

The other 36 nonquadric Paulis give anti-Hermitian compact-USp8 matrices iP_a. Induce them on wedge² and project exactly through B. The resulting 36 source matrices are pairwise orthogonal with squared Frobenius norm **48**, and *every one* of the repository's 36 compact root-packet generators is **exactly** an integer-rational combination, verified by cross-multiplication of integer Gram products. This closes the full algebra intertwiner in the actual canonical basis WITHOUT floating-point linear algebra.

For the original cubic-preserving order-three Albert clock U27, let K'=U27-U27^T. Express K' in this exact 36D basis. Its unique compact USp8 lift has rational Gaussian numerator H and denominator D=96 with the exact identities
  H†H=D²I8, H^T J H=D²J, H³=-D³ I8,
  Lambda²(H) B=D² B U27.
Thus the defining 8D clock has order SIX (cube equals the central -I), while its 27D exterior-square action has order THREE. These are **integer matrix equations**, not finite-precision numerical residuals.

**Extra operational insight:** Every entry in H is divisible by 48; the defining gate is H/96 = (H/48)/2. The reduced numerator entries are 0, ±1±i; the 8-mode unitary separates into **four independent balanced two-port couplers** on mode pairs (0,4),(1,5),(2,6),(3,7). This gives a physical synthesis advantage for the *defining* 8-mode reference clock. The induced 27D gate still occupies 27 modes; it is **not** an eight-path implementation of a 27-mode arbitrary state.

## 2. E6 first tensor hierarchy verified directly on five- and six-coordinate sections

**Producer:** analysis/toe_20261114_e6_tensor_hierarchy.py

With T_ijk the integer ±1 symmetric tensor on 270 ordered signed 45-triple entries, set
  (A bullet B)_r=T_pqr A^p B^q,
  (hat∂ H)^m=T_mnr ∂_n H_r,
  Y^mn_pq= T_mnr T_pqr.
For the generalised Lie derivative L_A B with the repo's weight-1/3 convention, exact sparse quadratic polynomial arithmetic verifies:
  L_A B + L_B A=hat∂(A bullet B),
  [L_A,L_B] V=L_[A,B]_E V,
  L_(hat∂H) V=0.
For the E bracket [A,B]_E=(L_A B - L_B A)/2, the explicit nonvanishing Jacobiator
  J_E=[[A,B]_E,C]_E+cyclic
obeys the precise potential identity
  6 J_E=hat∂ ( [A,B]_E bullet C
                 +[B,C]_E bullet A
                 +[C,A]_E bullet B ).
This was measured and tested as exact integer polynomial coefficient equality on 16 independent quadratic triples for each 5D and 6D representative. ALL Jacobiators were nonzero as parameters yet acted trivially as gauge transformations.

This implements the **beginning** of the well-known ExFT tensor hierarchy, which introduces a covariant 2-form B to repair non-Lie E-bracket curvature. It does **not** solve the complete 2-form field equations, external generalized metric, Bianchi hierarchy, supergravity dynamics, or discrete finite-difference closure. The latter is explicitly obstructed in the parallel repo's newest lattice notes.

Primary literature: Hohm–Samtleben, ExFT I, https://arxiv.org/abs/1312.0614 ; PoS(CORFU2014)133, https://pos.sissa.it/231/133/pdf (equations 2.7–2.15); Aldazabal–Graña–Marqués–Rosabal, https://doi.org/10.1007/JHEP04(2014)049 .

## 3. Wilson action census: a controlled NEGATIVE dimension-selection result

**Producer:** analysis/toe_20261114_e6_Wilson_section_census.py

For all **630** unordered pairs of 36 compact signed quarter-turn generators U_i=I+K_i+K_i² and U_j, compute each integer orthogonal plaquette W=U_i U_j U_i^-1 U_j^-1. Enumerate all 216 maximal coordinate five-sections and 72 six-sections independently.

Results:
- **270** plaquettes are flat, **360** non-flat.
- ALL 360 non-flat plaquettes stabilize at least one coordinate five-section AND one coordinate six-section.
- **ZERO** non-flat plaquettes preserve exclusively a five-section, exclusively a six-section, or neither family.
- Among non-flat plaquettes, the minimum integer Wilson action 27-Tr W is **18**.

Therefore the single-plaquette action on this 36x36 packet-gate ensemble CANNOT select M-vs-IIB dimensional type. This is an ensemble-specific no-go, NOT a no-go for arbitrary E6 holonomies or general dynamical sections. Section counts in a fixed coordinate gauge are not absolute gauge invariants unless the section itself is transported under gauge transformations. A promising next construction needs plaquette products/common preserved sections, flux terms, matter coupling, boundaries, or a justified dynamical functional.

## 4. Loss-aware 35-mode two-irrep central clock and optical erasure firewall

**Producer:** analysis/toe_20261114_35mode_loss_photonic_witness.py

Take eight defining and 27 antisymmetric-traceless modes in a coherent balanced interferometer. After three pulses the relative central phase is pi, and after six pulses both branches return. Model per-pulse branch intensity transmission eta8=.98 and eta27=.95, iid relative Gaussian jitter sigma=.10 rad, detector efficiency .82, dark-click probability 1e-5 (ALL illustrative, not measured).

For n applications the unconditional return probability under relative sign epsilon is
  p_ret=(eta8^n+eta27^n+2 epsilon sqrt(eta8^n eta27^n) exp(-sigma²/2))/4,
and survival is p_survive=(eta8^n+eta27^n)/2. Keep unconditional, conditional, and detected-click quantities distinct.

For three pulses:
- central-sign hypothesis predicted unconditional return p ≈ 0.00272868; conditional on surviving p ≈ 0.00303429; raw detector return click ≈ 0.00224750.
- calibrated null no-sign hypothesis raw click ≈ 0.73517760.
- Under fixed iid calibrated Bernoulli hypotheses, the classical Bhattacharyya bound gives **23 shots** for a nominal equal-prior misclassification upper bound 1e-6. It is NOT a realistic experimental sample-complexity claim including unknown nuisance phases, correlated drift, or mode crosstalk.

A strong general NO-GO applies to loss of the SOLE photon: in M single-photon paths, Kraus operators sqrt(1-eta)|vac><j| have pair-products spanning End(C^M), hence Knill-Laflamme cannot hold on any logical code subspace of dimension >1. An explicit three-dimensional repetition-code counterexample is included. Correcting arbitrary photon loss requires a physically redundant quantum encoding with independent carriers or equivalent resources. An arbitrary externally imposed pi phase can mimic the proposed relative-sign optical signal, so cross-checked gate synthesis and phase references are mandatory.

## 5. Independent GF2 symmetry, positive and negative Pauli MUB certificate validation

**Producer:** analysis/toe_20261114_independent_fivequbit_rankcode_audit.py

A new stand-alone bitset GF2 implementation enumerates **32,768** symmetric 5x5 matrices; finds exactly **13,888** nonsingular; derives independent O(5,2) matrix orthogonality (order **720**); and verifies 5,760 normalized admissible second matrices partition exactly into **eight disjoint 720-element congruence orbits**, represented by codes [692,693,694,695,700,701,702,703]. Independently invert S and perform S->S+I to obtain two S3 symmetry classes [[0,1],[2,3,4,5,6,7]].

Crucially, it independently verifies ALL **ten** positive nine-set witnesses from forward and reversed exact-cover files by pairwise nonsingular differences and by checking maximality against every one of the 13,888 candidate invertible extenders. That is a rigorous exact positive certificate for size 9.

The previous full negative size-eight run reports 433,517,130 DFS nodes across eight orbits; a reversed traversal reports 107,943,913 across two S3 classes. Both report no timeouts and no witnesses. The new script inspects those claims, but DOES NOT independently rerun their enormous search trees, and reversed traversal uses the same underlying algorithm family. The minimum-nine result is therefore a strong **computationally reported** conclusion, with a separate independent UNSAT implementation or independently checkable proof log still desirable. Kantor's maximal symplectic partial spread constructions are established prior art: https://pages.uoregon.edu/kantor/PAPERS/maxPartial.pdf .

## 6. Novel independent geometry: exact horizontal metric of pure-state E6 charges

**Producer:** analysis/toe_20261114_CP7_HP3_charge_differential.py

Pass12656 proved that for every pure three-qubit state |psi>, the 27 commuting-quaternionic charges z_i=<psi|P_i|psi> obey
  Σ_i z_i²=3,  N(z)=1.
The concrete geometric explanation is quaternionic Hopf/twistor structure. Let J be the Pauli-Y antiunitary with J²=-1. Then psi and Jpsi are orthogonal, and Pi=|psi><psi|+|Jpsi><Jpsi| is a rank-2 quaternionic-line projector. X=Σ z_i P_i=4Pi-I8; Tr(X²)=24, Tr(X³)=48.

**New metric calculation:** For a horizontal normalized tangent δpsi perpendicular to span_C{psi,Jpsi}, the derivative satisfies
  Σ_i (δz_i)² = 8 ||δpsi||².
Proof: dX=4 dPi, Tr((dPi)²)=4||δpsi||², Tr((dX)²)=8 Σ_i(δz_i)². The 2-dimensional real tangent fibre δpsi ∝ Jpsi has δz=0. Thus the real differential CP7 (dimension14) -> HP3 (dimension12) has rank12, a CP1 vertical kernel, and twelve equal squared nonzero singular values **8**.

At |000> this is verified EXACTLY: 27x14 integral Jacobian, Gram diagonal with 12 eights and 2 zeros (vertical indices 6,7). At 20 independent generic random pure states the cubic/norm/metric residuals are <=1.6e-14.

Intersections with the coordinate sections are **NOT** an automatic dimension selector:
- At the special |000> stabilizer basepoint, 216 five-sections split rank4 (120) and rank5 (96); 72 six-sections split rank5 (48) and rank6 (24).
- At a generic state ALL 216 five-section projections have rank5, and ALL 72 six-section projections have rank6.

So the 27 charge coordinates on pure three-qubit states form a constrained 12-real-dimensional submanifold, not 27 independent physical coordinates. This is a useful non-overclaim firewall: the representation embeds quaternionic projective geometry, but it doesn't derive an 11-dimensional spacetime, a 10-dimensional spacetime, or any observed gravitational field equations.

## Validation and evidence hierarchy

Six deterministic producers and six JSON certificates under analysis/ and data/, plus tests/test_toe_20261114_six_fronts_exact.py. The integration suite reruns all six scripts, proving exact integer identities rather than trusting their JSON. Older parallel commits and their data remain untouched.

- **Exact:** E6 cubic relabel/sign identity; USp8 Gaussian integer intertwiners; finite 8D/27D group orders; 630 Wilson trace/section census; tensor-hierarchy finite polynomial identities; finite GF2 orbit/witness checks; CP7 basepoint differential; analytical loss no-go.
- **Numerical:** generic pure-state tangent checks (20), illustrative optical probabilities/shot bound (double precision).
- **Reported but NOT independently reproduced:** 433M+108M complete negative-size-eight exact-cover search nodes.
- **Unverified physical speculation:** selected spacetime dimension; true quantum-gravity dynamics; actual laser/photonic synthesis and hardware noise; constants derived from graph alone.

## Top five independent research experiments

1. **Finite exact hierarchy with meaningful dynamics:** give the 2-form B an explicit external lattice action or higher bracket and demonstrate a corrected discrete curvature/Bianchi identity on a finite torus, with negative stencil controls.
2. **Genuinely discriminating section vacuum search:** use multiple independent Wilson plaquettes whose COMMON invariant section families differ, include a nontrivial calibrated field functional, and test whether a fixed-gauge preference survives gauge transport.
3. **Implement the reduced four-coupler eight-mode gate:** use the exact 8x8 half-Gaussian entries to compile a measured interferometer; separately synthesize the 27D action and set a phase-noise tolerance based on calibrated drift, not iid toy noise.
4. **Obtain a machine-checkable MUB size-eight no-go:** independent exact-cover implementation (different branching/data structure or SAT with proof logging) and a reduced verifiable UNSAT certificate, not another read-only audit of the existing two runs.
5. **Push quaternionic charge geometry toward a genuine falsifier:** compute the quartic defining ideal of the HP3 orbit in R27, examine how ExFT 5/6 tangent sections intersect its normal bundle, and identify any prediction not tautological in compact USp8 representation theory.

**Assessment:** The strongest incremental theorem is the complete exact Gaussian-integer full-36 compact-intertwiner plus a four-coupler 8D lift of the original Albert clock. The strongest limiting findings are the 630-case section nonselection and the rank12 pure-state charge manifold. The broad theory of everything remains an unproved physical hypothesis; the mathematical structures and their reproduction files are concrete.
