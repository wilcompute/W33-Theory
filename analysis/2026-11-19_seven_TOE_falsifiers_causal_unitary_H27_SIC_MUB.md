# Seven TOE falsification tracks: causal monotonicity, unitary dilation, and H27 SIC/MUB mass splitting

**2026-11-19.** Mathematical and numerical certificate, not a physical Theory of Everything. This is a source-aware continuation of `dba7c8d10` and `1c9771ef6`. Prior work already established U(1) causal diamond gauge interference, spectral determinant blindness, a 2D overlap flux index, H27 sextic SIC rays, a four-gate sequential qutrit GHZ emitter, the heavy-flavor rank-one CP obstruction, and conditional causal-operator smoothing. We do not relabel those established results as new.

## External research checks

- [Causal fermion systems in curved spacetime, October 2026](https://doi.org/10.1007/s11005-026-02168-3) constructs a physically distinct causal-action framework using the one-particle density operator of a quasi-free Hadamard state, and studies its Einstein–Dirac continuum behavior. We have NOT implemented that construction here. This is a nontrivial benchmark for our *microscopic action*, which remains missing.
- [A Guide to Higher-Order Quantum Operations, November 2026](https://doi.org/10.1103/92c4-g7qs) clarifies process-tensor instrument causality and classical versus quantum memory. Our output GHZ witness is NOT such a full process tensor certification.
- [Observation of Genuine Multi-Time Quantum Memory, November 2026](https://arxiv.org/abs/2611.17268) finds genuinely three-time-only memory, experimentally and theoretically; the repository's old GHZ marginal coincidence does not by itself reproduce that achievement.
- [Reflection positivity in free fermionic theories, November 2026](https://doi.org/10.1007/s11005-026-02191-4) reinforces the positivity gate for chiral and nonlocal constructions.
- [Qutrit toric code and parafermions, 2025](https://doi.org/10.1038/s41467-025-61391-z) is directly relevant hardware prior art, not evidence that our specific qutrit Holonet exists.

## Front 1: Causal history selection — exact monotonicity obstruction

Fix an ordered set of n events and any nonnegative strictly upper triangular adjacency A, with m>0 and alpha>0. Since A^n=0,

`G=(mI-alpha A)^(-1)=m^(-1) sum_{k=0}^{n-1} (alpha A/m)^k`.

Each entry of G is a positive polynomial in the forward edge weights. Adding an edge with positive weight strictly raises G at that edge's endpoints, and cannot lower any other nonnegative matrix entry. Therefore

`R(A)=Tr(G G^dagger)=sum_{ij} |G_ij|^2`

is strictly increased when a positive edge is added, for real nonnegative links. Bare det D=m^n is still constant. This is exact for ANY finite acyclic graph with positive link weights and no complex interference.

**Numerical exhaustive proof control:** n=5 has 10 possible ordered edges and 2^10=1024 edge configurations. Comparing every configuration to every one-edge extension gives 5,120 strictly positive response differences, no exceptions. R ranges from 2.9585798816568 to 6.6493169118958 at m=1.3, alpha=0.6.

**Physical interpretation:** A positive reweighting by R could systematically favor denser directed networks; the inverse weighting systematically penalizes edges. Neither is a derived manifoldlike selector. With complex gauge phases, cancellations invalidate this simple monotonicity, but selecting a gauge phase or sign by hand would recreate the original theory-selection problem. These adjacency sets are arbitrary forward DAGs, not necessarily transitively closed causal posets.

## Front 2: Physically consistent fermions

Construct an independently written 2D Wilson kernel on LxL torus at L=4,6 with integer flux q=-1,0,+1. The Hermitian gamma5 Wilson kernel has spectral-sign overlap index -q in all six cases. This verifies only a **known lattice index identity**, not a four-dimensional chiral theory. The topology, flux, gamma structure, Wilson mass, and spacetime dimension are externally supplied; no reflection-positivity or interacting anomaly test is claimed. New physical target: a causally meaningful Hilbert construction before proceeding to gravitational predictions.

## Front 3: SU(2) Wilson gauge-frame covariance

48 independent SU(2) plaquette holonomies are generated from arbitrary unitary link matrices. Each is transformed by four random local SU(2) frames. Wilson matrices transform by conjugation at the basepoint; maximum Frobenius covariance residual is 1.27e-15. No Yang–Mills action, flux source or observed gauge coupling is derived.

## Front 4: Genuine quantum-memory caution

Rebuild pure qutrit GHZ rho=|000+111+222><...|/3 and its dephased classical mixture. All three pairwise output marginals agree to below 2e-16, whereas Re Tr[(X⊗X⊗X)rho]=1 and the dephased mixture gives 0. This is a standard tripartite-coherence witness, NOT an operational exclusion of all classical-memory *processes*. Arbitrary intervention slots and causal constraints remain absent.

## Front 5: Flavor CP rank

For a diagonal three-family mass basis, a single heavy mixing vector a induces Hermitian H=diag(m)-aa†/M, so Im(H12 H23 H31)=0 identically. Add a second nonparallel complex vector b and this cycle can be nonzero. The explicit controlled example gives 0 versus 1.2110726643598489e-4. The source-repo already discussed rank-one CP obstructions; this is independent reproduction, not a prediction. Couplings, up-sector masses, and defect overlaps remain chosen.

## Front 6 (new architecture gate): no forward-only finite unitary on a fixed event basis

**Theorem:** A finite upper triangular unitary matrix is diagonal. Proof by first-column orthogonality and induction. In particular, a strict nontrivial forward-order state-transition matrix cannot itself be a unitary evolution operator on the same fixed event basis.

**Constructive escape:** Any contraction T admits a Julia/Halmos unitary dilation on a doubled Hilbert space:
```
U = [[T, sqrt(I-TT†)],
     [sqrt(I-T†T), -T†]]
```
For T=[[0,0.35],[0,0]], numerical unitary defect 1.37e-17. A further 128 random triangular nontrivial controls were correctly rejected as nonunitary.

**Important distinction:** This is not a no-go theorem for microscopic causal quantum theory! Time-layered channels, sequential unitary dynamics, ancilla/environment dilations, and continuous-time unitary evolution may all realize causality. Instead it prohibits confusing strict triangular one-step propagation with a closed-system Hamiltonian on the event-address space.

## Front 7 (strongest new algebraic connection): H27 SIC/MUB Hessian dichotomy

The previously certified H27-invariant toy superpotential is
```
W = x³+y³+z³ - (x⁶+y⁶+z⁶)/2
F_i = 3 x_i² (1-x_i³).
```
Its 64 stationary configurations have support census (1,9,27,27) for supports 0,1,2,3.

The previously recognized **support-two** branch has 27 F-flat vectors, collapsing to nine projective rays that are a qutrit SIC: all off-diagonal squared overlaps 1/4 and normalized nine-state POVM completeness. **New physical test:** the exact Hessian is diag(6x_i-15x_i⁴). At support-two vacua, one entry vanishes, so complex Hessian rank is 2. With global SUSY, canonical Kähler potential and an F-flat vacuum, tree-level scalar mass-squared is Hessian†Hessian and equals (0,81,81). The vanishing F_i has a double zero at that coordinate; its local scalar potential starts `9|delta|^4 + O(|delta|^7)`. Consequently the zero is *quadratically massless but quartically stabilized*, **not** an exact continuous modulus.

The **support-three** branch has 27 vectors / nine projective rays
```
psi_ab=(1, omega^a, omega^b)/sqrt(3), a,b in F3.
```
Partition them by `a+b mod 3`. Each partition has three mutually orthogonal states, and every pair from different partitions has squared overlap exactly 1/3. They are **three mutually unbiased qutrit bases**. At every support-three point all three Hessian singular values are 9 (mass-squared=81), hence no quadratic zero modes.

This is the **SIC–MUB quadratic mass dichotomy in the very same F-flat toy**: geometric SIC support-two vacua are quadratically gapless; mass-gapped support-three vacua organize as MUBs rather than SICs.

Certificates: SIC Gram maximum residual 6.7e-16; completeness 5.4e-16; MUB basis residual 5.3e-16; cross-basis overlap residual 2.3e-16.

**Scope:** These are exact algebraic facts about the particular separable H27 invariant toy under canonical global-SUSY assumptions. A gauged SU(3)/E6/E8 completion, D-flatness, Kähler corrections, messenger dynamics, physical mass scales, vacuum selection and phenomenology could change them. No observed particle masses or TOE claim follows.

## Reproduction

```
python analysis/toe_20261119_six_independent_physics_falsifiers_v1.py
python analysis/toe_20261119_H27_sextic_SIC_MUB_hessian_dichotomy.py
python -m unittest discover -s tests -p test_toe_20261119_six_falsifiers_and_SIC_MUB_v1.py -v
```

Outputs: `data/toe_20261119_six_independent_physics_falsifiers_v1.json` and `data/toe_20261119_H27_sextic_SIC_MUB_hessian_dichotomy.json`.

## Five independent next research targets

1. Replace the synthetic 2D overlap kernel with a physically admissible 3+1 spinor process passing reflection positivity or a direct Lorentzian positivity/unitarity equivalent, plus local/global anomaly checks.
2. Derive normalized causal-history weights that favor manifoldlike 4D histories in a nonparameterized continuum limit, surviving the exact positive-edge monotonicity adversary.
3. Build a process tensor with arbitrary intermediate instruments for the emitted qutrit source and solve a classical-memory exclusion SDP, comparing with the November 2026 genuine three-time memory literature.
4. Embed a flavor/center-covariant gauge dynamics into an actual E8/E6 representation with anomaly-free chiral matter, derive couplings and zero-mode overlaps rather than assigning them.
5. UV-complete the sextic H27 SIC flavon so its quadratic zero mode is lifted without losing the nine-state SIC and without violating F/D-flatness, global gauge invariance or phenomenology.

## Further outside-the-box corollary: a BPS wall between SIC and MUB branches

All 64 F-flat stationary points have **zero scalar F-term vacuum energy**, irrespective of support. Their superpotential critical values depend only on the number s of nonzero coordinates, **W=s/2**. Thus the gapped support-three MUB branch is NOT energetically preferred over the gapless support-two SIC branch merely because its Hessian is nondegenerate. The branches are exactly degenerate as supersymmetric F-vacua in this toy.

However, hold two coordinates fixed at unity and let the previously zero coordinate interpolate along the real interval 0<=x<=1. The standard global-SUSY BPS equation is

`dx/dz=3x²(1-x³)`.

This admits a monotone trajectory from x(-infinity)=0 (support-two SIC) to x(+infinity)=1 (support-three MUB). The critical-value separation is `Delta W=1/2`; its exact dimensionless BPS wall tension is **T=2|Delta W|=1**. The wall's SIC-side tail is algebraic, `x(z)~-1/(3z)`, while the MUB-side approach is exponential, `1-x(z)~exp(-9z)`. The asymmetry traces directly to the SIC branch's massless quadratic fluctuation.

The independent symbolic/numerical certificate is `analysis/toe_20261119_H27_SIC_MUB_BPS_domain_wall.py`, `data/toe_20261119_H27_SIC_MUB_BPS_wall_certificate.json`. This wall is a **global-SUSY toy**: it does not establish a physical soliton in the gauged, gravitational or E8-completed theory, and it does not select either branch as our universe.
