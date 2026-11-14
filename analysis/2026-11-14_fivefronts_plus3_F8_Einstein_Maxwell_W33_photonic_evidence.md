# Five independently executed TOE frontiers + three orthogonal falsifiers — November 14, 2026

**Provenance and execution status.** This note records a research pass executed using the connected authorized Windows machine while it was online. The eight-front Python producer `analysis/toe_20261114_five_fronts_plus_three_field_eom_spectral.py` was written **locally** and returned a `PASS` result for each of its eight checks. An independent 15-test regression file was also written locally, but its final result could **not** be retrieved when Desktop Commander disconnected. Those local files and a JSON certificate are **not included in this GitHub commit** and must not be described as synchronized or passing independent CI. This note preserves the independently derivable mathematical results, not unverified hardware physics.

Parent prior work: Pass 12671 exact F8 upper witness, prior E6 torus flux runaway analysis, and the independent exact-rational witness commit `3c373c924`. A different assistant has concurrently reserved Pass 12672 for a code-space lower-bound search; this note does not claim that work.

## 1. Exact two-copy spectral barrier to the nine-F8-MUB global lower bound

The nine mutually unbiased stabilizer bases in dimension 64 consist of nine pairwise disjoint maximal commuting Pauli subgroups, each with 63 nonidentity elements. Using GF(8) multiplication modulo `x^3+x+1`, trace `Tr:F8 -> F2` and trace-dual masks, the 9x63=**567** covered operators were reconstructed independently.

For any unit vector `psi`, the certainty objective can be written exactly as

`c8(psi) = sum_{P in C} <psi|P|psi>^2 = <psi tensor psi| K |psi tensor psi>`, where `K=sum_{P in C}P tensor P`.

All doubled Hermitian Pauli operators commute. In the standard Bell basis indexed by 12-bit phase-space labels `w`, the contribution from each complete size-64 stabilizer subgroup is `63` if `w` lies in that Lagrangian subspace, and `-1` otherwise. Because the nine nonzero subgroups are disjoint, the exact spectrum is:

- Full two-copy Hilbert space, dimension `64^2=4096`: `567^1, 55^567, (-9)^3528`.
- Symmetric subspace, dimension `64*65/2=2080`: `567^1, 55^567, (-9)^1512`.
- Antisymmetric subspace, dimension `64*63/2=2016`: `(-9)^2016`.

The covered labels have even swap parity; hence the nontrivial positive eigenvalue sector is entirely symmetric. An independent random-state numerical check matched the nine-basis chirped-Fourier fourth-moment formula to the direct covered-Pauli expectation-square sum to about `6e-15` in an exploratory sample.

**Falsification:** The naive symmetric two-copy Rayleigh–Ritz lower bound is `-9`, which is useless for certifying the conjectured global infimum near `2.4985086467`. The mixed one-copy relaxation also admits the maximally mixed state, with zero objective. Therefore purity, product structure, PPT and/or stronger moment constraints cannot be omitted from any successful global lower-bound proof. In particular, this spectral computation does **not** improve the existing exact PPT lower bound of approximately `2.0818`, nor does it supersede Pass 12671's exact algebraic upper witness `(47-32 cos(2pi/9))/9`.

## 2. Exact **on-shell** nine-dimensional Einstein–Maxwell background, not just a radion extremum

Specify a different gravitational theory, with action `S9 = integral sqrt(-g) [R-F_MN F^MN/4]`. On the direct-product metric `AdS5 x S2 x S2` take both round sphere radii equal to one and `F = f(vol_a+vol_b)` with **`f^2=14/5`**.

Then `F_MN F^MN=4 f^2=56/5`. The trace-reversed Einstein equation in these conventions is

`R_MN = F_MP F_N^P / 2 - g_MN F^2 / [4(D-2)]`, `D=9`.

It is satisfied componentwise with

- `R_mu,nu = -2/5 g_mu,nu` on AdS5, i.e. `L_AdS^2=10`;
- `R_ab = g_ab` on **both** unit-radius round two-spheres;
- `R9 = 2`, consistent with the trace equation.

The field strength is closed and co-closed because it is a constant sum of the product-sphere volume forms: `dF=d(*F)=0`. The 5D Einstein-frame homogeneous potential in coordinates `x=e^(u+v), y=e^(u-v)` is

`V(u,v)=(14/5)e^(-20u/3)cosh(4v)-4e^(-14u/3)cosh(2v)`.

At `u=v=0`, `V=-6/5`, the gradient vanishes, the Hessian is **`diag(112/3,144/5)`**, and the external Ricci equation agrees with `R_mu,nu=V/(5-2)g_mu,nu=-2/5g_mu,nu`.

This upgrades the preceding potential-only toy minimum to a **full field-equation solution for a specified nine-dimensional Einstein–Maxwell theory**. It remains unrelated to a derived E6 ExFT gauging/section solution; the mass spectrum of inhomogeneous KK modes, flux quantization with a specified charge/coupling, stability of all other fields, and any physical identification with our universe remain open. Product-sphere Freund–Rubin-type backgrounds can exhibit nonhomogeneous instabilities (see https://inspirehep.net/literature/556247).

## 3. Microscopic finite-speed quantum clock: exact reversible QCA control

For a two-state local coin `C=exp(-i theta sigma_x)` and conditional nearest-neighbor shift `S(k)=diag(e^(ik),e^(-ik))`, the exactly unitary Floquet step `U(k)=S(k)C` has

`cos omega(k)=cos(theta) cos(k)`;

`|d omega/dk|=|cos(theta)sin(k)|/sqrt(1-cos(theta)^2cos(k)^2)<=|cos(theta)|<=1`.

The local 101-site example checked 11 finite-cone ticks with norm conservation and inverse evolution. Low `k,theta` produce a Dirac-type dispersion `omega~sqrt(k^2+theta^2)`. This is established quantum-walk mathematics, **not novel fundamental dynamics**, and does not derive the repository's 120 Clifford ticks. Relevant prior literature: https://arxiv.org/abs/hep-th/9304070 ; https://doi.org/10.1103/PhysRevA.95.062344 .

## 4. Exact intrinsic W33 uniform edge-refinement *one-dimensional* continuum limit

W33's collinearity graph has `V=40, E=240`, degree 12. Replace each edge with a length-`L` path. Then `V_L=40+240(L-1)`, `E_L=240L`. For symmetric normalized adjacency `P=D^(-1/2) A D^(-1/2)`,

`Tr(P^2)/V_L = (120L-200)/(240L-200) -> 1/2`.

The density of vertices within any fixed radius `r` of the original 40 branching vertices is bounded above by `[40+480r]/V_L -> 0`. Consequently the uniformly rooted local limit is the two-regular infinite path. Its odd normalized-adjacency moments vanish; even moments equal `binomial(2k,k)/4^k`. The fixed-time heat trace limit is

`H(t)=e^(-t) I_0(t)`,

with spectral dimension `d_s(t)=2t(1-I_1(t)/I_0(t)) -> 1` at large diffusion time (with **L->infinity first**). Thus this natural *intrinsic* refinement fails to produce four-dimensional diffusion. This is not a theorem against all possible W33-inspired towers or a Lorentzian/spacetime claim.

## 5. Concrete photonic internal-rail computation and resource falsifier

In the single-photon one-particle subspace, `M=16` orthogonal rails implement an algebraic four-qubit tensor-factor encoding. A logical Hadamard uses eight disjoint balanced two-rail couplers; a logical CNOT uses four mode-pair swaps; a logical controlled-Z uses four conditional mode phases. One Hadamard and three controlled permutations exactly prepare the **internal-mode** GHZ vector `(|0000>+|1111>)/sqrt(2)`.

In general, representing arbitrary `n` logical qubits in a single photon requires `M>=2^n` orthogonal modes and the elementary logical Hadamard requires `2^(n-1)` pair couplings, so this encoding **does not scale with polynomial optical resources**. Internal factor entanglement is not spatially separated Bell nonlocality.

For a hypothetical four-layer optical network with independent per-layer photon survival `eta=0.98`, survival is `eta^4=0.92236816`. Independent Gaussian relative-mode phase noise with individual standard deviation `sigma=0.1` yields internal GHZ X⊗4 visibility `exp(-sigma^2)`. Under independent accepted ±1 measurements, Hoeffding's inequality gives **2952 accepted samples** for absolute precision `0.05` with error probability at most `0.05`; allowing only the specified loss requires **3201 raw trials**. **Important readout resource:** Measuring X⊗4 by four logical Hadamards before rail detection requires another 4×8=32 balanced two-rail couplers organized into four additional layers. If every preparation and analyzer layer incurs the same eta=0.98 loss (eight total traversed layers), the survival becomes eta^8=0.8507630225817855 and the same accepted-shot target requires **3470 raw trials**, not 3201. The 3201 figure applies only when analyzer loss is excluded. Neither gate fidelity nor loss is an experimental observation here. Context: https://www.nature.com/articles/s41467-019-08951-2 and https://www.nature.com/articles/s42005-024-01610-z .

## Three more outside-the-box tests

**6. Spectral blindness to flux orientation.** A 3-site U(1) flux ring with `E_k(Phi)=2cos((2pi k+Phi)/3)` has *the same unordered energy spectrum* at `Phi` and `-Phi`, but oriented currents `-dE_k/dPhi` reverse. So energy spectra alone cannot certify a physically selected chirality. The `Phi=+/-2pi/3` test is an explicit example, not an E6 chirality selector.

**7. Flux-sector topology mismatch.** `b_k(T4)=(1,4,6,4,1)`, `b_k(S2xS2)=(1,0,2,0,1)`. In particular, `H^3(T4)` has rank four whereas `H^3(S2xS2)=0`; `H^2` ranks are six versus two. Euler characteristics differ (0 versus 4). An ordinary topology-preserving deformation cannot equate the original flat T4 three-form scenario with the new S2xS2 Maxwell magnetic two-form background.

**8. Exchange count does not determine dimensional c.** The same dimensionless local unitary lattice clock can be assigned `(a,delta_t)=(1,1),(2,1),(1,3),(3,7)`, producing maximum lattice hop speeds `1,2,1/3,3/7` in external physical units. An independent length/time matching law is needed before proposing a physical speed of light.

## Research-integrity conclusions

**Certified within the stated models:** the exact F8 Bell spectral barrier; the D9 Einstein–Maxwell background equations; the exact local weak limit and limiting diffusion dimension; the algebraic scaling and topology comparisons; the finite specified quantum- and photonic-operation models.

**NOT certified:** a global F8 lower bound, an E6 exceptional-field-theory vacuum, all-moduli or KK stability, emergent 3+1D Lorentzian geometry, spacelike Bell violation by an internally factorized single photon, scalable single-photon BQP, or a derived measured SI value of c.

**Artifact / synchronization note:** The authorized local Desktop Commander machine disconnected after writing the implementation, tests and preliminary certificate. Accordingly, this GitHub file is the synchronized evidence artifact; it does **not** attest that those separate local files were committed, that their pytest process finished, or that the local worktree was synchronized after this cloud commit.
