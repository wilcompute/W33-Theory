# Robust affine quantum-walk obstruction and minimum W33 harmonic polarization completion

**Date:** 2026-11-08.  
**Executable source:** analysis/w33_20261108_stability_hodge_completion.py  
**Regression suite:** tests/test_w33_20261108_stability_hodge_completion.py  
**Workflow:** .github/workflows/w33_20261108_stability_hodge_completion.yml  
**Certificate:** generated data/w33_20261108_stability_hodge_completion.json in the independent CI artifact.

**Scientific status:** Two conditional mathematical theorems, independent numerical checks, and a concrete finite optical/representation test. This is not a derivation of a photon, alpha, physical spacetime, Lorentz covariance or an experimentally confirmed TOE.

## Provenance and latest parallel work

The previous PASS20261108_AFFINE_COVARIANCE_NO_GO proves that an exactly affine-GL2-invariant unitary on Sym2(Fq), odd prime-power q>=5, cannot be complex Hadamard: at d=(0,1,0) its amplitude is bounded by 2/q². Our November 8 chirality report and corrections identify the faithful congruence group as GL2(q)/{±I}, **not** PGL2(q) for q>3.

Parallel commit eea5a46a20 adds a determinant-isometry-preserving Gaussian Hadamard clock K(S,T)=q^(-3/2) psi(det(S-T)), respecting a subgroup of index (q-1)/2 in full GL2 congruence. At q=5 the subgroup is index two. That construction is exactly unitary and flat but its principal-log Hamiltonian is nonlocal. We **reuse rather than reassert** that prior result here.

The existing PASS20261108_S4_HARMONIC_QDUAL gives the 46D cohomology's translation-character ranks and the 18D span of the two S4-fixed harmonic modes; this pass derives an **adjacency-spectral characterization** and conditional polarization-capacity obstruction.

## Theorem 1: a quantitative amount of symmetry breaking is compulsory

Let V=Sym2(Fq), |V|=q³, q any odd prime power, with G=V rtimes GL2(q) acting by translations and matrix congruences. Let R_g be the  q³-dimensional permutation representation, and define the finite group twirl of a unitary U:

\[
\mathcal T_G(U)=|G|^{-1}\sum_{g\in G}R_gUR_g^\dagger.
\]

**Key extension of the earlier no-go:** T_G(U) is a contraction (operator norm at most one), not necessarily a unitary; nevertheless the five dual-orbit Fourier-character bound still applies. At the fixed difference d=(0,1,0),

\[
|\mathcal T_G(U)_{0d}|\le2/q^2.
\]

If U is exactly flat, |U_{0d}|=q^(-3/2). The reverse triangle inequality for one entry and the elementary bound |B_{ij}|<=||B||op give the robust inequality

\[
\boxed{\|U-\mathcal T_G(U)\|_\mathrm{op}
\ge\delta_q=q^{-3/2}-2q^{-2}>0\quad(q\ge5).}
\]

Because ||U-T(U)|| <= sup_g||U-R_gUR_g†||op = sup_g||[U,R_g]||op, the same δ_q lower-bounds the **maximum group commutator**. This remains true with nonlocal hopping, arbitrary complex phases, arbitrary evolution time or an internally chosen Hamiltonian, so long as the unitary acts on the same q³-dimensional permutation representation and exact flatness is required.

**Hamiltonian version:** For U=e^(-itH), with H bounded and self-adjoint, Duhamel's identity implies ||[U,R_g]||op <= |t| ||[H,R_g]||op. Therefore a flat walk at t≠0 must satisfy

\[
\boxed{\sup_g\|[H,R_g]\|_\mathrm{op}\ge\delta_q/|t|}.
\]

If the selected amplitude only approaches flatness within ε, replace δ_q by max(0,δ_q−ε). This is an exact, normalization-aware conditional constraint; the dimension of the Hamiltonian commutator is inverse time in the chosen units.

Six exact prime-character coefficient checks give the following amplitude and probability bounds:

| q | Flat amplitude q^-3/2 | Affine upper 2/q² | Required norm defect δ_q | Probability ceiling 4/q^4 |
|---|---:|---:|---:|---:|
| 3 | 0.192450 | 0.222222 | 0 (none) | 0.049383 |
| 5 | 0.089443 | 0.080000 | 0.009443 | 0.006400 |
| 7 | 0.053995 | 0.040816 | 0.013179 | 0.001666 |
| 11 | 0.027410 | 0.016529 | 0.010881 | 0.000273 |
| 13 | 0.021335 | 0.011834 | 0.009500 | 0.000140 |
| 17 | 0.014267 | 0.006920 | 0.007346 | 0.000048 |

### Explicit q=5 comparison with the parallel Lorentz-isometry clock

Take the parallel agent's flat Gaussian convolution kernel K(d)=5^-3/2 exp(2πi det(d)/5). We computed its exact translation/Fourier eigenvalues and their full GL2-orbit means; the group twirl remains translation invariant, so it suffices to average Fourier phases over the five dual-orbit classes.

The actual **matrix operator-norm** distance from this isometry-preserving unitary to its full affine group twirl is

\[
\boxed{\|K-\mathcal T_G(K)\|_\mathrm{op}=\sin(2\pi/5)\approx0.9510565163.}
\]

Its selected original amplitude is 1/sqrt(125)≈0.0894427191, while the twirled amplitude is only ≈0.0276393202. The general lower bound for *any* exactly flat q=5 unitary is ≈0.0094427191. These are model calculations; neither equals a physical measured symmetry-breaking parameter.

The 2/q² upper bound on the selected entry is **sharp** among fully affine-invariant unitaries. At q=5, put Fourier phases +1 on all five congruence momentum classes except the rank-two positive-determinant class, where the phase is -1. The resulting Fourier multiplier has modulus one, defines a real unitary involution, and attains amplitude exactly 2/25=0.08 at the chosen entry. **It is not flat**, as required by the no-go. Sharpness of this *single-entry bound* does not establish optimality of the global δ_q among all flat unitaries.

**Experimental distinction:** At q=5 the selected probability of any fully affine-symmetric unitary is <=4/625=0.0064, whereas an exactly flat device has 1/125=0.008. This 0.0016 difference is a finite-symmetry calibration check and can be tested with known quantum-optical equipment. It does **not** distinguish standard quantum theory from the proposed TOE.

## Theorem 2: graph adjacency determines the harmonic momentum capacities exactly

Use the existing 27-vertex null Cayley graph over F3³ with the four projective null directions d_j. Every vertex has degree 8 and its adjacency A is

\[
A=\sum_{j=1}^4(T_{d_j}+T_{-d_j}).
\]

For each Fourier momentum k define n0(k)=#{j:k·d_j=0}. Since each null direction contributes 2 if perpendicular and -1 otherwise,

\[
\lambda_A(k)=3 n_0(k)-4.
\]

The edge-chain Fourier fiber C1(k) has dimension four. The 36 edge-disjoint triangle cells contribute n0(k) independent Fourier face boundaries; the vertex-gradient image has dimension one at k≠0 and zero at k=0. Consequently

\[
h(k)=\dim H^1(k)=4-n_0(k)-\mathbf1_{k\ne0}
=\frac{5-\lambda_A(k)}3+\mathbf1_{k=0}.
\]

The simultaneous exact adjacency and H1 rank census is:

| Adjacency eigenvalue | Number of k | Harmonic rank h(k) | Total H1 dimension |
|---|---:|---:|---:|
| 8 | 1 | 0 | 0 |
| 2 | 12 | 1 | 12 |
| -1 | 8 | 2 | 16 |
| -4 | 6 | 3 | 18 |
| **Total** | 27 | — | **46** |

The global index identity follows directly: trace(A)=0, so sum_k h(k)=(5/3)*27+1=**46**. This is a true algebraic link between the graph spectrum and topological harmonic cohomology, not a numerical parameter fit.

### An exact minimum auxiliary completion

A rank-two harmonic polarization bundle at **every nonzero translation momentum** is impossible inside H1 alone: the twelve λ=2 momenta each have h(k)=1. If one insists on such a rank-two bundle inside H1 plus a new auxiliary momentum representation, at least **one extra dimension at each of those 12 momenta** is necessary. Thus the minimum selective auxiliary space has dimension 12, yielding 46+12=58 total; a 2-by-26=52 dimensional selected bundle would leave six unselected dimensions (from the six rank-three momenta).

Importantly, **the minimum auxiliary representation is mathematically explicit**: take the adjacency eigenspace for eigenvalue 2. Its orthogonal idempotent projector is the cubic graph polynomial

\[
\boxed{P_2=\frac{(8I-A)(A+I)(A+4I)}{108},\qquad P_2^2=P_2,\quad\operatorname{rank}P_2=12.}
\]

The exact translation-invariant projector kernel has these values for its 27 displacement types:

| Kernel entry | Number of displacements |
|---|---:|
| 4/9, diagonal | 1 |
| +1/9, null neighbors | 8 |
| -1/9, other non-null neighbors | 12 |
| 0 | 6 |

Its support spans the diagonal and 20 nonzero displacements. Algebraically P2 is expressible using up to three adjacency multiplications, a useful finite-network design recipe. It does not mean a single physical nearest-neighbor gate can implement this measurement without ancillary operations or coherent control.

If a *uniform on-site scalar auxiliary species* is added to all 27 vertices, that contributes 27 additional degrees instead of the selective 12. A selective twelve-character complement is translation- and S4-covariant but generally nonlocal in the site basis. Its exact spectral projector P2 shows this nonlocality explicitly.

**Critical physical boundary:** H1 cohomology labels static harmonic 1-cochains; it is not automatically the space of radiative Maxwell photons. The full edge-cochain space also contains exact and coexact components, which may provide dynamical polarizations without introducing twelve new physical particles. The conditional obstruction applies only to models that demand *both* polarizations be present entirely in the H1 harmonic space at *all* nonzero Fourier momenta. It does not rule out electromagnetism or prove the need for twelve fundamental fields.

## Verification and prior art

The exact rank and graph projector claims were checked independently by constructing the full 27×27 null adjacency, evaluating the polynomial P2, testing idempotence and trace, and acting on all 27 Fourier basis vectors. The stability bound is proved at the operator level, while its p=5 group twirl is checked with the explicit Gaussian chirp and five-orbit Fourier means.

The previously established full-affine no-go, Lorentz-type Gaussian escape, S4 character decomposition and earlier Hodge construction are prior repository owners, not independent new external confirmations. A wider literature review finds that complex Hadamard matrices and uniform quantum mixing in association schemes are established mathematical topics: Godsil–Mullin–Roy (2017), doi:10.37236/4745; Godsil–Zhan (2017), doi:10.37236/6855. Finite Hodge decomposition is a standard construction, e.g. Desbrun et al., *Discrete Differential Forms for Computational Modeling*, https://geometry.caltech.edu/pubs/DKT05.pdf. The new repository-specific inequalities and certificates are not claimed to have independent publication priority.

## Five independent next falsifiers

1. **Matter and photons:** allow dynamical coexact 1-form modes and construct a translation-covariant, gauge-invariant rank-two polarization bundle. Test locality, positive kinetic energy, and charge normalization.
2. **Near-affine clocks:** optimize exactly flat q=5 quantum circuits over subgroups of GL2 and quantify minimum *global* symmetry-breaking distance, which can exceed our sharp one-entry obstruction.
3. **Hamiltonian locality:** search for strictly null-local logarithms of the index-two Lorentz-isometric Gaussian clock or rigorously prove they do not exist within a specified bounded-degree polynomial class.
4. **E6 flavor:** test whether any symmetry-allowed scalar from the actual native E6 tensor supplies three independent kernel-lifting channels, rather than arbitrary SVD-fitted repairs.
5. **Optical phase benchmark:** compile q=5 symmetry-breaking witnesses and the q=3 27-port interferometer into a full-routing, loss-calibrated, phase-sensitive protocol with independent controls.
