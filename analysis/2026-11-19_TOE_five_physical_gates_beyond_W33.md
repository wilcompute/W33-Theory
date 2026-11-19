# Five physics-first TOE gates: compact chirality, vacuum UV, covariance, quantum resources, measured couplings

**Date:** 2026-11-19. **Repository:** `wilcompute/W33-Theory` (storage only; this work does **not** use W33). **Status:** reproducible exact constraints, finite-dimensional calculations, and explicitly conditional physics toy models. **Not a solved TOE, not a compactification, not new experimental data.**

## Novelty/collision audit

Compared GitHub's `d67b942e` (new nonproportional E8/PW localizer) and `5bd07266` with the preceding `3edb3b915`, `867f70b96` and earlier H27/SIC/Dirac results. **Parallel-update:** commit `8efe83ec` landed during this pass and independently covers six model-independent consistency tests including SM one-loop RGE, neutrino charge quantization, cosmology and ghost diagnostics. Our SM/MSSM running numbers are an independently reproduced benchmark with a slightly different 2026 PDG input, NOT claimed as novel relative to that work. The latest E8 report is particularly consequential: it derives a local noncompact `Spin(10)` spectrum of **six 16s, three conjugate 16bars, eight 10s and 17 charged singlet field types**, using polynomial flat Cartan profiles on R3. Its signed spinor excess is three, but it finds an obstructed D/F-flat SM-breaking direction, Abelian anomalies, bare Yukawa rank <=2, nonnormalizable gauge modes and no global 11D solution. We do not claim these inherited numerical facts as independent discoveries.

The new increments below directly address the physical completion constraints, including a compact-index cancellation proof on the **actual local f1 profile**, a mirror-mixing invariant Yukawa rank theorem, an asymptotically free *parent* for the vectorlike SIC matter content, an independent 1+1 generally covariant constraint benchmark, a single-photon scaling bound and a measured three-coupling RGE scoreboard.

## 1. Compact chirality: local index -3 cannot survive a smooth closed exact localization

The parallel localizer uses the harmonic real function

    f1(x,y,z) = Re(x+i y)^4/4 - (x²+y²)/2 + z² - x.

Its critical point equations are

    f_x = x³ - 3xy² - x - 1 = 0,
    f_y = y(y² - 3x² - 1) = 0,
    f_z = 2z = 0.

The first branch y=0 has one real solution of x³-x-1=0. The second branch y²=3x²+1 has one real x solution of 8x³+4x+1=0 and **two** y signs. Each of these three critical points is nondegenerate and has negative Hessian determinant, so the *local gradient degree* is **-1** at each and **-3** altogether. This reproduces a concrete signed local concentration property using the actual source polynomial, without trusting any claimed index label.

For a **closed, oriented, smooth 3-manifold** M and globally smooth exact Cartan profile phi=df, the deformed twisted-de-Rham differential d_f=e^(-f) d e^f is conjugate to the ordinary de Rham differential. Thus the even-to-odd Witten index is the Euler characteristic chi(M)=0. Equivalently, Poincare-Hopf requires the total signed indices of zeros of any smooth vector field to equal chi(M)=0. Explicit finite triangulation/cell checks give chi(S3)=5-10+10-5=0 and chi(T3)=1-3+3-1=0.

**Therefore:** this particular local -3 degree *cannot* be extended to a globally smooth vector field on a closed three-manifold without compensating index +3 elsewhere. The charge-by-charge global twisted-de-Rham Euler index also vanishes under the smooth exact hypotheses. The noncompact R3 localizer may still have three normalizable modes; its L2 index is **not** automatically the compact de Rham index. One must explicitly build singularities, boundary conditions, nontrivial local systems/gauge couplings outside these hypotheses, or additional charged loci, then recompute a genuine global chiral index and anomaly inflow.

This neither rules out singular G2 chiral M-theory nor proves that the parallel total Spin10 index equals -3; the local **f1** gradient degree and the total spinor representation index are different quantities and must not be conflated.

Background: Higgs bundles/Morse theory in G2 model engineering [Braun et al., JHEP 03 (2019) 199](https://link.springer.com/article/10.1007/JHEP03%282019%29199); [Acharya-Witten](https://arxiv.org/abs/hep-th/0109152). The explicit polynomial calculations and compactness gate are this pass.

### Mirror mixing cannot cure the bare star Yukawa rank

The parallel source proves that every allowed bare 16-16-10 cubic in this profile uses a single designated sheet-3 spinor. Its six-by-six symmetric flavor Yukawa matrix necessarily has the form

    Y = u v^T + v u^T,   rank(Y)<=2,

where u picks out the privileged spinor. Let M be any full-rank 3x6 Higgs-independent mirror mass matrix pairing the three 16bars to three linear combinations of six 16s. The remaining three chiral light modes form a full-rank 6x3 matrix N spanning ker M. Their bare tree-level Yukawa is

    Y_light = N^T Y N,    rank(Y_light)<=rank(Y)<=2.

This holds for **arbitrary mirror mixing**, not only aligned or diagonal mixing. A scan of 64 random complex full-rank mass matrices found rank 2 in all cases; the rank upper bound is algebraic, not statistical. At least one light 16 consequently retains **zero mass from this bare linear Higgs texture**. Higher-dimensional operators, Higgs-dependent mirror mixing, other electroweak Higgs sectors or radiative corrections may evade the bound and must be computed.

### Abelian anomaly gate (source inputs)

The parallel localizer gives mixed anomaly vectors `Tr Q=(102,141,49)` and `Tr Spin10² Q=(12,15,7)`. Their integer cross product has primitive generator `u=(14,-7,-9)`. Although this line cancels those two mixed anomalies, the parallel source calculates `Tr(u.Q)^3=49032 !=0`. Thus **none** of these three Abelian combinations survives as an anomaly-free U1 without additional charged matter, a global inflow/Green-Schwarz sector or other changes. This is a conditional conclusion about the source spectrum, **not** an independent recomputation of the cubic charge census.

## 2. Asymptotically free SIC UV parent exists at the matter-content level

The previously constructed elementary SU3 nine-SIC triplet model with nine vectorlike flavor pairs has N=1 SQCD one-loop b0=3Nc-Nf=0; the ten-pair cubic version has b0=-1. This does not imply there can be no asymptotically free parent.

Take **SU(4) with ten vectorlike fundamental-antifundamental pairs** and gauge-singlet fields only. Its one-loop coefficient is `b0=3*4-10=+2` and cubic gauge anomaly cancels. Give one vectorlike pair equal VEV along color e4, Q_9=V e4, P_9=V e4^dag; this is D-flat and Higgses SU4->SU3. The **nine** other flavors then transform as SU3 triplets/antitriplets, with b0=9-9=0 below the heavy threshold, before their own alignment. Placing the nine Hesse SIC columns in the first three color components, with P_i=Q_i^dag and a smaller VEV r, retains exact D-flatness for the entire SU4 background; a 4x4 baryon composed of three linearly independent SIC flavors and the heavy Higgsing flavor is nonzero.

This removes the *one-loop UV asymptotic-freedom objection to the parent matter sector*. **It does not solve** the fundamental problem: constructing a natural SU4-invariant holomorphic F-flat superpotential with the desired two scales, stable quantum vacuum, all heavy-field thresholds, anomaly constraints for any additional representations, and unbroken SM gauge/color structure. SU4's quartic fundamental baryon is nonrenormalizable as a bare superpotential term; mediator completions have to be engineered and checked.

Background: ordinary N=1 SQCD beta functions, e.g. [SQCD classical moduli and gauge dynamics](https://qft.org/supersymmetry-duality/four-dimensional-n1-gauge-dynamics/sqcd-fields-symmetries-classical-moduli/).

## 3. Classical Lorentzian covariance: a physically meaningful constraint-algebra benchmark

Instead of inferring GR from a finite graph, start from a *parametrized relativistic string*, a genuine first-class 1+1 reparametrization-invariant classical system with canonical fields X^a(s), P_a(s). Its Hamiltonian and momentum constraints are

    H[N] = 1/2 int ds N(s) [eta^ab P_a P_b + eta_ab Xprime^a Xprime^b],
    D[xi] = int ds xi(s) P_a Xprime^a.

Direct functional differentiation and periodic integration by parts yield

    {H[N], H[M]} = D[N M' - M N'],
    {H[N], D[xi]} = H[N xi' - xi N'],
    {D[xi], D[eta]} = D[xi eta' - eta xi'].

These are the continuum **hypersurface-deformation-form** brackets in a fixed flat target string (equivalently centerless classical Virasoro constraints). They provide a nontrivial, well-defined baseline for a proposed finite state update law. Our script evaluates the HH bracket on 32, 64, 128 and 256 periodic sites for two embedding components. Centered differences exhibit an O(h²) Leibniz/closure defect; FFT differentiation closes the sampled low-band bracket to machine precision but fails for deliberately aliased high modes.

This **does not derive** general relativity: the target metric is nondynamical and the full GR structure function `q^{ij}(x)` is field-dependent. There is also a finite-algebra no-go: any ordinary derivation of complex vertex functions with pointwise multiplication on a finite set is zero. A realistic theory must specify continuum/refinement or another differential bimodule and an anomaly-free field-dependent constraint algebra. See [Non-degenerate metrics and hypersurface deformation algebra (2024)](https://link.springer.com/article/10.1007/s10714-024-03313-w).

## 4. One-photon computation and quantum memory: resource scalability gate

A single photon in an explicitly counted set of **M orthogonal optical modes** has a one-excitation Hilbert space of complex dimension M. An exact embedding of an arbitrary n-qubit register requires at least `M>=2^n` orthogonal modes. This is a dimension theorem, independent of how the modes are labeled (path, time bins, OAM or frequency).

| n logical qubits | minimum modes | duration for sequential nonoverlapping 1ns bins |
| ---: | ---: | ---: |
| 4 | 16 | 16 ns |
| 10 | 1,024 | 1.024 microseconds |
| 20 | 1,048,576 | ~1.05 milliseconds |
| 30 | 1,073,741,824 | ~1.07 seconds |
| 40 | 1,099,511,627,776 | ~18.3 minutes |
| 60 | 1,152,921,504,606,846,976 | ~36.5 years |

The **duration estimates are not universal**: they assume one sequential time-bin alphabet with >=1ns spacing. Spatial/OAM/frequency modes distribute overhead differently, but Hilbert-space dimension still limits an arbitrary lossless one-photon register. A 40-mode one-photon system can encode at most **five** arbitrary logical qubits as a 32-dimensional subspace, not 40. This does not rule out one-photon qutrit demonstrations, hybrid systems, repeat-use processors, unusual continuous-variable algorithms, or the single-photon-universe hypothesis as metaphysics; it prevents falsely claiming polynomial-resource scalable BQP from one-photon mode relabeling alone.

A quantum-memory SWAP model needs environment Schmidt rank >=3 to preserve an arbitrary qutrit entangled with a reference. Under depolarization p, the entangled fraction is `F=1-8p/9`, so an event-ready all-trial witness against an entanglement-breaking classical-only memory at retrieval/detection efficiency eta requires `eta > 1/(3F)` (for p=.20, about .405). The script also independently rechecks the **known unencoded** one-qutrit ninth-root T9 injection and all three Clifford feed-forward corrections for 48 random outcome/state cases. None is an encoded fault-tolerant gate or experimentally demonstrated photonic process tensor. A real TOE should explain such physical quantum capacities from a causal dynamics rather than merely implement them.

## 5. Measured gauge-coupling running, not numerology

Use explicit Z-scale MS-bar reference inputs `alpha_EM^-1=127.930` (PDG electroweak review 2025), `sin²(theta_W)=.23122` and `alpha_s(MZ)=.1177` (PDG 2026 electroweak review; uncertainties are ignored in this one-loop illustration), `MZ=91.1876 GeV`. With GUT normalization `alpha_1=(5/3) alpha_Y`:

    alpha_1^-1(MZ) = (3/5) * alpha_EM^-1 * cos²(theta_W);
    alpha_2^-1(MZ) = alpha_EM^-1 * sin²(theta_W);
    alpha_3^-1(MZ) = alpha_s^-1(MZ).
    alpha_i^-1(mu) = alpha_i^-1(MZ) - b_i/(2 pi) ln(mu/MZ).

The SM one-loop coefficients are `b=(41/10,-19/6,-7)`. The pairwise meeting scales are about **1.03e13**, **2.39e14**, and **9.30e16 GeV** for (12),(13),(23), so the Standard Model alone does *not* unify the three gauge couplings at one loop. At the alpha1=alpha2 crossing, `alpha_3^-1-alpha_1^-1=-5.5588`.

The illustrative MSSM one-loop coefficient set is `b=(33/5,1,-3)`. Turning it on abruptly at 1 TeV (with SM running below) reduces the same inverse-coupling mismatch to about **-0.5796**, but does not make a prediction or prove MSSM spectra. Complete E8/SM unification would have to supply the actual threshold spectrum, coupling matching, two-loop running, and measured values. No gauge coupling constant, Higgs mass, gravity, or 11D dynamics was derived here.

Official benchmark: [PDG 2026 electroweak review](https://ccwww.kek.jp/pdg/2026/reviews/rpp2026-rev-standard-model.pdf) (Table 10.2, page 23; eq. 10.41), and [PDG 2025 electroweak review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf). These measured numbers are **inputs**, not novel predictions.

## Reproducible work

```powershell
python analysis/toe_20261119_five_physical_gates_beyond_W33.py
python -m unittest discover -s tests -p test_toe_20261119_five_physical_gates.py -v
```

JSON certificate: `data/toe_20261119_five_physical_gates_beyond_W33.json`. Independent checks cover analytic critical-point classification, signed local index, two odd-manifold Euler characteristics, 64 random mirror decouplings, anomaly vector kernel, parent gauge beta/D-flatness, canonical bracket discretization, mode capacity, non-Clifford injection and SM/MSSM coupling running.

**Claim-status firewall:** Exactly known mathematical identities are distinguished from source-dependent E8 counts, numerically sampled checks, imported experimental parameters and open physical constructions. More finite-group matches would not cure any of the five gates.

## Top five independent frontier tasks

1. **Global compact chiral index:** explicitly resolve the +3 compensating index needed to extend the local f1 profile, then construct a singular/flux background that still yields exactly three physical net chiral families, a compact seven-dimensional metric and anomaly inflow.
2. **Physical vacuum and spectrum:** realize a natural, F/D-flat, asymptotically free parent yielding three chiral families and a full-rank three-family Yukawa matrix *after* mirror decoupling, with no arbitrary target VEVs.
3. **Actual spacetime theory:** construct dynamical 3+1 gravitational variables, first-class field-dependent hypersurface constraints, a unitary quantum theory and a controlled Lorentzian continuum/refinement limit.
4. **Operational photonic dynamics:** specify causal-process tomography, active three-time interventions, event-ready photon-loss accounting and a scalable architecture whose Hilbert-space resource count is explicit.
5. **Predictive unified couplings:** compute a physical particle/threshold spectrum and run the gauge/Yukawa couplings to observed low-energy values, with preregistered numerical error tolerances and at least one nontrivial new prediction.

This pass finds several **physical necessities and obstructions**, not a Theory of Everything.
