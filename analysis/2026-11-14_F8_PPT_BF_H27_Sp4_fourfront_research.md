# Five independently tested TOE fronts — exact F8 PPT obstruction, AdS masses, H27 clocks, 4D address locality and optical GHZ readout

**Date:** 2026-11-14. **Evidence:** finite exact arithmetic, explicitly conditioned 9D Einstein–Maxwell reduction, 27-element group enumeration, finite symplectic group orbit and numerical optical-statistics simulations. **Not** a completed theory of everything.

A concurrent assistant reserved Pass 12672 to study the F8 code-space lower bound. This report instead independently tests a *specific failed proof strategy* and three orthogonal physical-interface constructions. All local dirty edits and prior staged work were preserved, using only uniquely named files.

## Front 1 — F8: an exact positive, symmetric PPT two-copy state with certainty objective zero

Producer: \`analysis/toe_20261114_F8_two_copy_PPT_zero_countercertificate.py\`; exact certificate: \`data/toe_20261114_F8_two_copy_PPT_zero_countercertificate.json\`.

The 9 F8-regulus mutually unbiased stabilizer bases in C^64 cover 567 distinct nonidentity Pauli labels, each from a maximal commuting class of 63. Define \`C\` as their union and \`K=sum_{P in C} P tensor P\`. For pure one-copy state \`psi\`, \`c8(psi)=<psi tensor psi|K|psi tensor psi>\`.

Use a Bell basis indexed by \`w=(u,z) in F2^12\` and the swap parity \`q(w)=u dot z\`. The exact eigenvalues of K on the symmetric Bell sector are \`567\` once, \`55\` on 567 covered nonzero labels and \`-9\` on 1512 even-parity uncovered labels. The antisymmetric sector has dimension 2016.

**Construct the two-copy density matrix as a Bell-diagonal probability distribution**

- identity Bell label weight \`p0=0\`;
- each of the 567 covered even labels weight \`pC=1/4032\`;
- each of the 1512 other even labels weight \`pU=55/96768\`;
- each odd/swap-antisymmetric label weight \`0\`.

Then \`567*pC+1512*pU=1\`, so the state is manifestly positive and supported on the symmetric subspace. Its K expectation vanishes **exactly**:

\`567*p0 + 567*55*pC -1512*9*pU=0\`.

This state is also **PPT** across the 64x64 copy split. Since the partial transpose of a symmetric Bell projector is diagonal in a Bell basis, its spectrum follows from a symplectic Walsh transform of the weights, with **exact rational multiplicities**:

\`(1/64)^1, 0^567, (31/96768)^1512, (1/4032)^2016\`.

Every eigenvalue is nonnegative and the trace is 1. The script independently reconstructs the nine F8 commuting groups and all 4096 PT eigenvalues, performs a full 4096-entry exact integer Walsh transform, and checks the spectrum and objective using \`fractions.Fraction\`.

**Rigorously established:** the standard symmetric **two-copy** PPT relaxation admits an objective of zero and therefore its optimum is **at most zero**. Thus it cannot certify *any positive* pure-state certainty lower bound. Its actual PPT optimum **might be negative**; no claim of equality to zero is made. This does not contradict stronger nontrivial PPT/SDP bounds that impose additional constraints (the repository's earlier quoted ~2.0818 lower bound is not refuted). Pass 12671's exact cyclotomic upper witness remains valid; the global minimum is still unproved.

The deeper message: positivity of the pure-state certainty polynomial is not captured by even symmetrically supported PPT two-copy density matrices alone. Higher-copy, exchangeability, rank-one constraints, or nontrivial quartic SOS localizers are necessary if using this relaxation family.

## Front 2 — Radion BF test plus minimally coupled probe Kaluza–Klein tower

Producer: \`analysis/toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py\`, \`compactification_radion_BF\`.

Use the **specified** 9D Einstein–Maxwell theory \`S=∫sqrt(-g)(R-F^2/4)\`, whose on-shell background was established in the previous pass: \`AdS5 x S2 x S2\`, both spheres radius 1, magnetic field \`F=f(vol1+vol2)\` with \`f^2=14/5\`, and \`L_AdS^2=10\`.

Write two logarithmic radii \`beta1=u+v\` and \`beta2=u-v\`. The Einstein-frame gravitational kinetic terms in d=5 are

\`-sum_i n_i (d beta_i)^2 - (sum_i n_i d beta_i)^2/(d-2)\`, \`n1=n2=2\`.

Therefore the canonical convention \`-1/2 G_ab du_a du_b\` yields **\`G=diag(56/3,8)\`**. The homogeneous potential Hessian already derived is \`H=diag(112/3,144/5)\`; hence \`G^-1 H=diag(2,18/5)\`, **not** simply the raw Hessian. In AdS units,

\`m_volume^2 L^2=20\`, \`m_relative^2 L^2=36\`.

Both satisfy the AdS5 BF bound \`m²L² >= -4\`.

For a **minimally coupled, free probe scalar** on the same unwarped product geometry, the S2xS2 Laplacian has harmonics

\`m^2_KK = l1(l1+1)+l2(l2+1)\`, degeneracy \`(2l1+1)(2l2+1)\`.

All entries with \`0<=l1,l2<=3\` are exhaustively checked; the first nonzero probe level has \`m²L²=20\`. Under common radius rescaling of this Lambda=0 family, \`L_AdS² / r_sphere² =10\` stays fixed, so this background does not admit a parametric large-radius separation between 5D AdS curvature and KK physics by tuning the common flux scale.

**Unresolved:** the *full coupled* Einstein–Maxwell fluctuation matrix, tensor/vector/scalar harmonics with metric/flux mixing, gauge constraints, all KK levels, nonlinear stability, quantum flux quantization and a genuine E6 ExFT embedding. This is a certified zero-mode BF + free probe tower, **not** a claim that the full 9D vacuum has been proved KK stable. Relevant existing product-sphere stability literature: Brown & Dahlen, https://arxiv.org/abs/1310.6360 (the q=2 cases are studied there); https://inspirehep.net/literature/1262000 .

## Front 3 — A native noncommutative H27 four-pulse clock

Use the order-27 Heisenberg group with multiplication

\`(a,b,c)*(u,v,w)=(a+u,b+v,c+w+a*v) (mod 3)\`.

The standard steps \`X=(1,0,0)\`, \`Y=(0,1,0)\` generate a connected four-regular Cayley graph with inverses. Exactly four noncommuting elementary pulses produce

\`X Y X^-1 Y^-1=(0,0,1)=Z\`, \`Z^3=1\`.

The left-regular action permutes all 27 group-address states in exactly **nine disjoint three-cycles**. The central clock operator has eigenvalues \`1,omega,omega²\` each with multiplicity nine, and a full return occurs after **three central steps = twelve elementary pulses**. All 81 choices of the 2D step components were checked, with commutator center \`det[[a,b],[c,d]] mod3\`.

**Interpretation:** a mathematically exact *quantized clock/holonomy* associated with the regular H27 addresses, making the center operational. It **does not** furnish a clock in seconds, derive a local relativistic Hamiltonian, produce the thermodynamic arrow, or identify gravity. The Weyl/Heisenberg commutator is established algebra; the contribution here is this specific finite address-and-pulse protocol and its falsifiable finite-spectrum bookkeeping.

## Front 4 — Symplectic-covariant locality no-go and a framed 4D address limit

Use the 81 affine addresses \`V=F3^4\` underlying W(3,3)'s symplectic phase space. Generate transvections

\`T_v(x)=x+Omega(x,v)v\`, \`Omega(x,y)=x0*y2+x1*y3-x2*y0-x3*y1 (mod3)\`.

Exact preservation of \`Omega\` was checked on basis vectors for every nonzero \`v\`, and orbit enumeration confirms that the transvections act **transitively on all 80 nonzero address displacements**. This is a classical property of the full symplectic group, consistent with the standard theorem that symplectic transvections generate Sp(V), see https://math.mit.edu/~dav/sympgen.pdf .

Therefore any undirected **translation-invariant Cayley graph** on these 81 affine addresses whose displacement set is invariant under **all** Sp4(3) must be either empty or the 80-regular complete graph. It cannot be sparse/local while preserving those exact symmetries.

Choosing a **symplectic frame** deliberately reduces symmetry. The 8 coordinate generators \`±e0,...,±e3\` give the sparse 4D torus \`C3^4\`, with exact adjacency spectrum

\`8^1,5^8,2^24,(-1)^32,(-4)^16\`.

For growing odd prime p, the same **framed** address lattice \`C_p^4\` has normalized-Laplacian heat trace

\`H_p(t)=[p^-1 sum_{k=0}^{p-1} exp(-(t/4)(1-cos(2pi k/p)))]^4\`.

For \`1<<t<<p²\`, it exhibits **\`d_s~4\`**. Explicit p=3,11,31,101 and diffusion times 10,20,100 are recorded. The continuum regime requires both enlarging the finite field and breaking full symplectic symmetry by selecting four preferred axes; at p=3 the graph's long-time dimension collapses to zero.

**New physical issue isolated:** a local emergent spacetime needs a microscopic mechanism that selects a sparse frame, or alternatively must relax full affine translation and symplectic invariance. This model yields neither a spontaneous frame selector, a Lorentzian metric nor Einstein field equations. Do not mistake a deliberately chosen Cartesian frame for a symmetry-free derivation of 3+1D physics.

## Front 5 — A falsifiable, five-setting 16-rail GHZ witness

The one-photon four-virtual-qubit encoding uses 16 orthogonal rail/time/frequency modes; it is not four spatially separated photons.

Let \`M(theta)=cos(theta) X + sin(theta) Y\` on each logical virtual qubit. Four equatorial parity measurements at \`theta_j=j*pi/4\` reconstruct the target coherence **for arbitrary 16x16 density matrices**, with no GHZ-subspace assumption:

\`A=(1/4) sum_{j=0}^3 (-1)^j <M(theta_j)^tensor4> = 2 Re(rho_{0000,1111})\`.

One Z-basis rail measurement supplies \`p0+p15\`, giving **exact**

\`F_GHZ = (p0+p15+A)/2\`.

This is a standard efficient GHZ-fidelity witness design, not an original general theorem; prior art on n+1 equatorial measurement settings and fidelity >1/2 genuinely multipartite entanglement is discussed in https://www.nature.com/articles/s41534-024-00867-0 .

The implementation numerically checked the exact Fourier identity on 40 independently generated positive trace-one 16x16 matrices to <1e-12. A **crucial negative control** \`(|0011>+|1100>)/sqrt2\` has \`<X^tensor4>=1\` but **target GHZ fidelity zero**; the Fourier-filtered coherence yields \`A=0\`, preventing a naive false interpretation.

Specified hypothetical noise model: depolarization weight 0.03, independently jittered two-endpoint relative phase with per-endpoint sigma=0.10 rad, slow drift standard deviation 0.07 rad, systematic offset 0.08 rad, photon transmission per traversed layer 0.98. The predicted conditional fidelity is approximately **0.96434**.

A seeded synthetic accepted-count test allocates **4096 accepted shots to each of the five settings**, uses a five-setting union-bound Hoeffding analysis for 99% coverage under independent accepted observations and reports a positive one-sided fidelity bound above 1/2. The optical upper-bound count assumes four preparation layers; each equatorial analyzer requires four more logical Hadamard layers (8 disjoint balanced two-rail couplers per layer). **Expected** loss-only raw counts: Z setting 4441, each equatorial setting 4815, total **23701**. These counts are expectations under the model, not a high-confidence raw-event guarantee or measured performance.

A fidelity above 1/2 rules out biseparable states **of the four selected internal virtual qubits** under trusted settings. It is **not** a spacelike Bell-nonlocality test, a device-independent certificate, a scalable quantum computer, or an observed chip result. Dark counts, mode-dependent crosstalk, detector tomography, switching transients and correlations are intentionally outside this idealized falsifier, and would require new uncertainty budgets before a hardware claim.

## Prior-art and exact-status separation

- Existing repo passes established the F8 exact upper witness but **not** its global minimum. This report excludes an overly weak PPT two-copy attack and does **not** claim to replace the stronger PPT lower-bound analysis from another track.
- The on-shell D9 Einstein–Maxwell background is prior local work. Here the novel *project-specific* step is exact canonical mass conversion, BF values and probe KK spectrum, not the origin of Freund–Rubin physics.
- H27 multiplication and symplectic transitivity are standard mathematics, not original theory. The earlier repo report `analysis/2026-10-08_twenty_apartment_torus_F20_H27_physical_packet.md` already established a mod-3 alternating cup pairing and H27 central-flux link on a selected W33 torus-like complex, including a full 729-pair holonomy census. This pass adds only the explicit four-pulse left-regular clock dynamics and its 27-state orbit/shortest-path verification, not a new H27-versus-torus identification. The finite symplectic affine-locality obstruction is a separate symmetry-conditional theorem.
- GHZ n+1 settings are known; here we implement explicit **single-photon rail** resources, a physically meaningful false-positive control and conditional finite-sample budget.
- New exact conditions are model-specific; no derivation of physical Standard Model masses/couplings, fundamental c, or quantum gravity.

## Commands and artifacts

- \`py -3 analysis/toe_20261114_F8_two_copy_PPT_zero_countercertificate.py\`
- \`py -3 analysis/toe_20261114_AdS5_H27_Sp4_optical_fourfronts.py\`
- \`py -3 -m pytest tests/test_toe_20261114_five_front_stronger_certificates.py -q\`

JSON certificates are in \`data/toe_20261114_F8_two_copy_PPT_zero_countercertificate.json\` and \`data/toe_20261114_AdS5_H27_Sp4_optical_fourfronts.json\`. The independent test suite executes all producers without any remote internet dependency.

**Bottom line:** A **zero-valued symmetric PPT countercertificate** closes a tempting but unproductive F8 proof route; the D9 radion modes pass physical normalization and BF tests; H27 supplies an exact finite central clock; a full symplectic invariance requirement obstructs sparse nearest-neighbor address locality; and a five-setting optical witness distinguishes genuine internal GHZ coherence from a false positive. None alone establishes a TOE.
