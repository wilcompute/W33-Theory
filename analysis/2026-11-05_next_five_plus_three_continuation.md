# November 5, 2026 — Five TOE frontiers plus three independent falsifiers

**Scope:** five executable mathematical/quantum-model continuations and three
independent structural controls, not a completed Theory of Everything, an
experimental result, or a derivation of measured Standard Model parameters.

**Baseline:** W33-Theory master dcb8bd37ad44ea9db38461a8bed06264c9524cfe
and the 215-page `papers/forty_points/main.pdf`. Work executed in a separate
worktree; preserve unrelated uncommitted changes in the main checkout.

**Reproduce with:**

```powershell
python analysis/toe_20261105_s3_nonabelian_matter_gauge.py
python analysis/toe_20261105_4d_ward_locality_cfl.py
python analysis/toe_20261105_photon_memory_chirality.py
python analysis/toe_20261105_three_orthogonal_physics_falsifiers.py
python -m pytest -q --noconftest tests/test_toe_20261105_next5_plus3.py
```

## 1. Non-Abelian dynamical action with matter — an exact 27-sector surprise

Use the non-Abelian finite group \(D_3\cong S_3\), two loop holonomies
\(g_1,g_2\in S_3\) at a common vertex, and two distinguishable matter
doublets in the real 2-dimensional irreducible representation \(\rho\).
Raw Hilbert dimension: \(|S_3|^2\,2^2=144\).

The local gauge transformation \(h\) conjugates both holonomies and
acts by \(\rho(h)\otimes\rho(h)\) on the matter. The group average
\(P_G=(1/6)\sum_h U_h\) is idempotent and has exact rank

\[
\mathrm{rank}P_G =
\frac{144+3\cdot 0+2\cdot9}{6} = 27.
\]

The traces follow directly from centralizer sizes and matter
characters: identity 144, each transposition 0, each 3-cycle 9.

A fully specified gauge-invariant finite Hamiltonian has
\(H=J E+K M+g C\), with:
- \(E\): two loop electric kinetic shifts by the **class sum** of the
  three transpositions;
- \(M\): the class function of the plaquette loop commutator
  \(g_1g_2g_1^{-1}g_2^{-1}\) via the 2D representation character;
- \(C\): two matter-loop covariant real-symmetric colour couplings.

The executable code directly verifies \([H,U_h]=0\), \([H,P_G]=0\),
Hermiticity, \(P_G^2=P_G\), the rank-27 projection, and noncommuting
electric/magnetic and electric/matter terms. The electric/magnetic
commutator Frobenius norm is 10.9544511501. Four parameter points
have explicitly diagonalized 27-by-27 physical Hamiltonians.
For \((J,K,g)=(0.5,1,0.3)\), the ground gap is 0.3050001581.

**Nonidentification:** The gauge-invariant sector has the same dimension
as the paper's 27-event affine histories, as the Hilbert space of
three qutrits, and as the three-site \(Z_3\) quantum clock model below.
Dimension alone supplies no canonical isomorphism, intertwining
operators, physical Lorentz symmetry, chiral fermions or continuum.

This is a **finite S3 pure-loop gauge theory coupled to localized
dynamic matter colour**, not an SU(2)/SU(3) Standard Model lattice
with propagating quarks. Finite-group gauge projector, magnetic flux
and electric dynamics are established prior art.

## 2. Locality and 3+1-dimensional continuum falsifier

Use the symmetric rank-2 perturbation \(h_{\mu\nu}\) in four Euclidean
coordinate directions. The finite-difference symbol is
\(k_\mu=2\sin(\pi m_\mu/n)/a\), \(a=1/n\).

Define the linearized Einstein operator

\[
2G_{\mu\nu}(h) =
 k^2h_{\mu\nu}-k_\mu(hk)_\nu-k_\nu(hk)_\mu+
 k_\mu k_\nu\mathrm{tr}h
 -\delta_{\mu\nu}(k^2\mathrm{tr}h-kh k).
\]

For nonzero momentum it has rank 6 on 10 symmetric components,
and exactly four gauge directions
\(h_{\mu\nu}=k_\mu\xi_\nu+k_\nu\xi_\mu\).
The code verifies both \(k^\mu G_{\mu\nu}=0\) and \(G(k\xi+\xi k)=0\)
for five lattice refinements. It also tests that an explicit mass
regulator breaks this gauge null identity.

For a **supplied** periodic 4D local scalar lattice, the mesoscopic
spectral dimension at \(t=0.02\) approaches 4; at \(n=32\) it is
4.02401452495. For a separate Lorentzian 3-spatial/1-time lattice
wave discretization, the stability condition is
\(\nu=c\Delta t/\Delta x\le1/\sqrt3\): \(\nu=.55\) is stable at the
Brillouin-zone corner, while \(\nu=.60\) is unstable.

**Guard:** This is a linearized Euclidean gauge identity together with
a separate Lorentzian finite-difference CFL test. It does not derive
general relativity, the nonlinear constraint algebra, a physical
Lorentzian metric, or the 4D local lattice from W33. The conformal-factor
indefiniteness remains.

## 3. Adapted ququart Helstrom optical circuit

Source of the forty authoritative Witting rays:
`tools/bt1408_witting_contextual_communication_bridge.py`.
Source of the exact four-port compiler and perturbation model:
`analysis/toe_20261104_fourrail_givens_drift_detector_validation.py`.

For ququart mixed states
\(\rho_i=(1-\epsilon)I_4/4+\epsilon P_i\),
diagonalize \(\rho_i-\rho_j\) and physically represent its Helstrom
projector measurement by one \(U(4)\) transformation followed by
four output-port detection. The compiler produces at most six
nearest-neighbour 2-mode Givens interferometers. The ideal port
probability total-variation distance equals the trace distance
to machine tolerance.

At \(\epsilon=.2,\eta=.85\), with independent loss and random
no-click assignments:

| pair | native Witting 40-effect success | Helstrom four-port success | Givens |
|---|---:|---:|---:|
| orthogonal | 0.534000 | 0.585000 | 5 |
| squared overlap 1/3 | 0.528333 | 0.569402 | 6 |

Three static mesh perturbation regimes (32 calibrations each) are
computed. Their minima are **sample minima, not worst-case guarantees**.
A mixed state requires proper source randomization, not one pure
single-photon unitary. No chip was fabricated.

## 4. Memory with loss and an adversarial failure mode

Reuse the explicit 27-dimensional \(R,S,E\) qutrit SWAP and
trusted entanglement-breaking reset model in
`analysis/toe_20261104_reset_immune_quantum_memory_falsifier.py`.
Quantum environmental storage restores Bell fidelity 1;
classically dephased storage gives 1/3; memoryless model gives 1/9.

For a depolarized quantum memory with survival \(p\),
\(F(p)=(1+8p)/9\),
\(\mathcal N(p)=\max(0,(4p-1)/3)\).
The all-trials success probability with independently characterized
herald efficiency \(\eta\) is \(\eta F+(1-\eta)/9\).
The *calibrated separable null with the same efficiency* is
\(\eta/3+(1-\eta)/9\), not blindly 1/3.

At \(p=.35,\eta=.85,n=3000\): null 0.30, alternative
0.375555556, Bell-count rejection threshold 960,
exact false alarm 0.00916773 and model power above 0.9999999999.
These numbers assume fixed rates, a trusted reference, trusted reset,
independent herald and no quantum bypass.

A separable state with true Bell fraction 1/3 can be displayed
at **conditional** fraction above 0.8 if the detector efficiency
depends on Bell-outcome success (\(\eta_+=.95,\eta_-=.10\)).
This is biased measurement selection, not recovered entanglement.
The calibration/null assumptions are integral to the claim.

## 5. Anomaly and chirality vacuum nonuniqueness

One family of left-handed SM fermions **with a right-handed neutrino**
admits charges \(X=a(6Y)+b(3(B-L))\).
The code checks each of the 48 bounded nonzero pairs
\(a,b\in[-3,3]\) for:
\(SU(3)^2X\), \(SU(2)^2X\), gravitational-X, \(X^3\),
\(Y^2X\), \(YX^2\) anomaly cancellation and all four
ordinary Yukawa monomials. Every check passes.

These 48 sample points contain equivalent rescalings and should
**not** be counted as 48 physically distinct viable models.
The larger two-parameter anomaly-free family shows that these
requirements **do not select** a unique \(U(1)\), flavour masses,
mixing matrix or CP sign.

As a separate boundary-chirality firewall, a 20-cell SSH chain with
\(t_1=.6,t_2=1\) has a pair of \(\sim2.34\times10^{-5}\) boundary
modes and exact sublattice chiral anticommutation. The trivial
\(t_1=1.4,t_2=1\) model is gapped. The finite system has **paired**
opposite-boundary modes, not a single unpaired 4D Weyl fermion.

## Three independent experiments beyond the five

### 6. Exact isospectral nonidentification

Two six-vertex connected nonisomorphic graphs have the same integer
Laplacian characteristic polynomial:

\[
p(x)=x(x-3)^2(x-2)(x^2-6x+4).
\]

Their degree multisets differ: \([1,2,2,3,3,3]\) versus
\([2,2,2,2,2,4]\), yet their global heat traces are identical
for all time. At \(t=1\), the sorted local heat-kernel diagonal
vectors differ by Euclidean norm \(\sim0.21259746\).

This is a counterexample to *uniquely* reconstructing physical
geometry from a global spectral clock. It is classical inverse
spectral graph theory; no novelty of cospectral graphs is claimed.

### 7. Contemporary Z3 parafermion continuum control

An October 29, 2026 Physical Review D paper
(Siew, Chandrasekharan, Bhattacharya, DOI 10.1103/xtsm-rw6d)
demonstrates a qubit-regularized SU(3) plaquette-chain continuum
related to the \(Z_3\) parafermion CFT. We independently diagonalized
periodic 3-state Potts chains with \(L=3,\ldots,7\).
At the self-dual coupling \(g=1\), \(L\Delta_L\) changes from about
2.28094 to 2.20995, consistent with critical \(1/L\) closing.
At \(g=1.8\), the absolute gap stays near 2.9.

The three-site model has dimension \(3^3=27\), but neither the size
nor \(Z_3\) arithmetic identifies this continuum critical dynamics
with the paper's W33 histories or the S3 invariant sector above.
Any such bridge must preserve *local Hamiltonian algebra and scaling*,
not numerical cardinalities.

### 8. An arrow-of-time versus Shannon entropy counterexample

A four-state cyclic Markov chain with \(p_+=.7,p_-=.2,p_0=.1\)
has uniform stationary distribution and Shannon entropy \(\log4\),
but a nonequilibrium current \(0.125\) and entropy-production rate
\((p_+-p_-)\log(p_+/p_-)=0.6263814842\).
The reverse-bias chain has the same state-count, entropy and positive
entropy-production rate but **opposite current**. A symmetric chain
\(p_+=p_-=.45\) has the same uniform stationary entropy but
zero entropy production.

Thus finite exchange counts or stationary information capacity
alone do not derive a temporal arrow. Direction requires specified
transition dynamics and a thermodynamic or boundary condition.

## References and novelty boundaries

- Non-Abelian lattice gauge simulation and gauge protection:
  https://www.nature.com/articles/s42005-025-02230-x
- Qudit gauge simulation including matter and plaquette:
  https://www.nature.com/articles/s41567-025-02797-w
- Qubit-regularized SU3 continuum via parafermion clock:
  https://doi.org/10.1103/xtsm-rw6d
- Lattice chiral anomaly and doubled fermion physics:
  https://doi.org/10.1103/PhysRevLett.134.021601
- Kaplan on anomaly cancellation and chiral boundaries:
  https://doi.org/10.1103/PhysRevLett.132.141603
- Discrete gravity with local Lorentz symmetry:
  https://doi.org/10.1103/PhysRevD.106.064001

None of these external structures or the elementary analytic formulas is
claimed as a new mathematical theorem. The repository-specific contribution
is the direct gauge/projector implementation, model-to-model
falsifiers, quantified errors and controls, and explicit absence of
canonical physical identifications.

## Artifacts

1. `analysis/toe_20261105_s3_nonabelian_matter_gauge.py`
2. `analysis/toe_20261105_4d_ward_locality_cfl.py`
3. `analysis/toe_20261105_photon_memory_chirality.py`
4. `analysis/toe_20261105_three_orthogonal_physics_falsifiers.py`
5. `tests/test_toe_20261105_next5_plus3.py`
6. Four corresponding `data/toe_20261105_*.json` certificates.

All models are deliberately finite or numerical. Their claims are
reproducible within model assumptions. No measured constant,
full gravitational action or empirical Standard Model explanation
has been derived.
