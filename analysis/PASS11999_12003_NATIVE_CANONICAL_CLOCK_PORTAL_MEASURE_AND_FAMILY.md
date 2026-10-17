# Passes11999–12003: native paths, canonical gravity coordinates, radial decoupling and a different family mass channel

15 October 2026. Reserved by `ffc5239eeb68f6e8a9ed62526016de3551c23172` before computation. This executes the five follow-ups to Passes11994–11998. It supplies explicit constructions where possible and records what those constructions still assume. **It does not solve the TOE, select Einstein dynamics, predict masses, or construct a complete chiral E6 vacuum.**

## What the repo already owned

- Pass11991 constructs the actual primitive four-period native cover; Pass11994 supplies the six-minimum clock order; Pass11995 proves the ten-edge metric chart and permits a supplied Einstein action. These are inputs here, not discoveries of a native continuum or gravity.
- Pass11996 owns the bounded joint singlet/flavour root and its nonzero neutral-scalar portal threshold. Pass11954 owns the matching convention. Passes11298/11303/11313 already identify portal/UV protection obstacles.
- Pass11519, in `analysis/PASS11608_11613_CHIRAL_UNIFICATION.md`, owns the standard Wilson all-volume gap identity and relative-current locality method. Pass11476 already uses homotopy to reconstruct a measure connection. Pass11997's *global* tree gauge is nonlocal. The new construction below uses an independent bounded tree in each native cell and a different regulator; it does not establish locality of the old nearest-edge operator.
- `analysis/w33_20261001_chiral_decuplet_and_condensate_bridge.py` and Pass11613 own the anomaly repair `(27,3)+(1,bar10)` and its minimality. Pass11271 and `spectator_residual_symmetry()` in `analysis/w33_pass11602_11606_geometry_flavor_completion.py` already construct an H27-preserving full-rank spectator mass in the **28** channel. The new result is an explicit **27** channel, not the first decuplet mass or anomaly cancellation. Pass11276 already states the threshold Wess–Zumino matching requirement.
- The Forty Points epilogue and physics scorecard still list masses/mixing/couplings and dynamical gravity as open. Nothing here changes those entries. No paper was edited.

Searches included the actual determinant `1882576080`, the representation products, invariant-space dimensions, the all-momentum polynomial, radial fixed-norm decoupling, the old anomaly inventory and homotopy/current constructions, rather than only pass titles. Novelty remains relative to the searched corpus; the standard external mathematics is credited below.

## 12000: compile the actual periods, then supply a reversible clock

The native primitive edge voltages have a connected zero-voltage subgraph. A literal 26-edge tree gives root-to-site paths for all27 vertices. Four edges carry the four positive unit voltages; closing each by the tree gives primitive loops. Concatenation and reversal compile every integer period.

For the actual ordered covector `u=(3,0,2,1)`, choose

```text
T = [0  1  0  0]
    [0  0  1  0]
    [0  0  0  1]
    [1 -3  0 -2].
```

Its determinant is ±1 and `u^T T=(1,0,0,0)`. Every column is compiled into a closed native edge word (maximum19 hops); the producer checks endpoints and signed deck voltage at every step. These are genuine paths of the selected native cover, rather than a disconnected added cubic lattice.

Place four coin amplitudes at each address and supply

`U(k)=exp(-im beta) exp(-ik1 alpha1) exp(-ik2 alpha2) exp(-ik3 alpha3)`.

The actual four gamma matrices anticommute. Diagonalizing each alpha implements the associated shift by its compiled native period or its reverse. A positive history operator is `C†C`, `C=Sclock-U`. The first-order Hamiltonian squares to `(|k|²+m²)I`, and its exact characteristic polynomial is

`det(omega I-H)=(omega²-|k|²-m²)²`.

Thus a **supplied reversible unitary update** has a Lorentz principal equation without making a negative eigenvalue of a diffusion generator. Continuum refinement is checked. Four of the eight spatial Brillouin corners have zero quasienergy: doubling is present. The coin, update ordering, velocity, clock choice, history law and its identification with physical time remain additional inputs. The clock cone has not been matched dynamically to the acoustic metric of11995.

## 11999: exact canonical variables on the edge-weight chart

Let `G(w)` be the weighted harmonic acoustic metric, recomputing the corrector for each change. Reflect it along `u` by

`K(w)=G(w)-2 G(w)u u^T G(w)/(u^T G(w)u)`

and transform by `T^-1 K T^-T`. Its inverse gives `h_ij`; set `n=N²=-1/K00` and `beta_i=-K0i/K00`. These are ten local coordinates. At unit weights, the envelope derivative `dG/dw_e=C_e^T C_e/27` yields an exact rational10×135 Jacobian. On the already selected ten edges its minor `J` is invertible. Independent finite differences recompute the native harmonic corrector and agree with the derived ADM Jacobian.

The canonical map is `dq=J dw`, `p_w=J^T p_q`; hence `p_w·dw=p_q·dq`. Pull back the six-dimensional DeWitt form

`W(E,F)=tr(h^-1 E h^-1 F)-tr(h^-1 E)tr(h^-1 F)`.

The ten-dimensional velocity Hessian has inertia **(5 positive,1 conformal negative,4 zero)**. The four null directions are explicitly the first four columns of `J^-1`; the certificate stores all rational entries. The conformal negative direction is the familiar constrained ADM direction, not evidence for an unconstrained stable ten-field theory.

At nonzero Fourier momentum, the four linearized continuum Hamiltonian/momentum constraints have rank4 and zero mutual Poisson brackets. Their transverse-traceless kinetic form is positive definite on exactly two directions. If the full action is supplied as

`S[w]=∫ N sqrt(h) (Kij K^ij-K²+R3(h)-2Lambda) dt d³x`,

its full nonlinear constraint algebra is inherited through the local invertible field redefinition. This is a canonical implementation, **not a new derivation of GR**. If the other125 edge directions enter only through the ten metric coordinates they are redundant; the conditional phase-space count is `270-2(125+8)=4`. Generic kinetic terms for all135 weights invalidate this count. Neither the spatial curvature term, Newton constant, cosmological constant nor continuum derivatives have been selected microscopically. The finite pointwise bracket failure in11976 remains.

## 12001: remove radial mixing instead of tuning its coefficient

The actual11996 neutral-scalar threshold uses a19×19 scalar Hessian and the fitted triangular Barr mass. A linear unitary internal symmetry cannot forbid `H†H h†h`, since `h†h` is invariant in every such representation.

Add the positive radial stiffness

`DeltaV=MR²(|h|²-n0)²/(8n0)`.

At the existing root it leaves the gradient unchanged and adds `MR² r r^T` to the Hessian, where `r` is the unit radial vector in the six real coordinates of the first triplet. The baseline portal coefficient remains0.1. A scan to `MR/vf=10000` suppresses the threshold by more than10^5, but its final magnitude is approximately `4.45×10^-10`: **it still fails the illustrative10^-10 target**.

In the strict constraint EFT `|h|²=n0`, project onto the radial tangent space. The portal becomes constant on that manifold and has no Higgs–angular mixing. Pure flavour scalar vertices change only the lower Barr row, so their determinant trace vanishes. For a pure Higgs vertex `YH`, with arbitrary Hermitian loop spectral matrix `F`,

`tr(M^-1 YH F M† YH)=tr(F11 m^T m)`

is real. Therefore the **specified one-loop neutral-scalar channel** vanishes exactly in the constraint model; numerical threshold evaluation and CP-conjugate controls verify this limit.

This is a change of field manifold, not a protective internal charge assignment. The extreme radial hierarchy corresponds to nonperturbative elementary quartic coupling unless supported by extra UV dynamics. A composite/nonlinear-sigma completion must be matched for allowed angular, higher-dimensional, gauge, tadpole, gluino and two-loop operators. Technical naturalness and full strong CP remain open.

## 12002: a local native-path regulator with an all-volume gap

Use the same zero-voltage tree separately inside every27-site native cell, and the four compiled period loops. For each site, its period transport goes to the cell root, around the root loop and back at the destination. Each hop is an original native edge; the maximum composite path length is **23**, independent of volume.

With arbitrary Abelian native link phases, bounded cell transport conjugates the path Wilson operator exactly to

`D_native ≅ DW4(U_rootloops) tensor I27 + kappa I tensor Ltree`,

where `kappa=4×27²=2916`. This exact factorization is checked on108 vertices and on a second volume with new random link phases. It is a designed regulator: tree, cycles and large optical coupling are supplied, many original edges are unused, and H27/canonical covariance has not been established.

The tree Poincare bound `lambda2>=1/729` gives `kappa lambda2>=4`. In the acoustic sector the **prior11519** Wilson identity is

`Q4(k)^2=[1+2 sum_(mu<nu) r_mu r_nu]I`, `r_mu=1-cos(k_mu)`.

Consequently its free gap is at least1 at **all** momenta and periodic volumes, and its norm is at most7. Each optical sector has Hermitian part at least `kappa lambda-1>=3`, even with arbitrary unitary gauge links.

For native phase sup-norm epsilon the perturbation bound is `(8R+2 kappa dmax)epsilon`. Choosing its product at most1/4 preserves a3/4 gap. The certificate distinguishes the charge-one radius from the radius for maximum integer charge6. Finite native range, volume-independent norm and gap give exponentially decaying sign-projector polynomial tails; the constants may be very conservative.

For each optical mode use the homotopy

`D_lambda(t)=(kappa lambda-1)I+t DW_mass0(U)`.

Its gap remains at least3. The initial projector is the **onsite gamma5 projector**, commuting with every gauge transformation. Kato transport therefore gives a smooth equivariant heavy frame from an explicitly onsite spin basis; direct polar-projector transport checks its endpoint and gauge covariance. This avoids a volume-spanning gauge tree. The gapped finite-range homotopy supplies a quasilocal generator, and finite homotopy time retains quasilocality.

The single acoustic block is a standard coarse four-dimensional Wilson/overlap operator. **Conditional reduction:** if a supplied anomaly-free Abelian charge inventory and *all* required Lüscher admissibility, locality and global-sector conditions hold, the known Abelian measure construction plus the explicit heavy trivializations pull back through bounded paths/cell transport. The acoustic Lüscher current is **not implemented numerically here**; a non-Abelian Standard Model measure, correct family inventory and a dynamically selected4D continuum remain open. This neither retracts nor proves locality for11991/11997's original nearest-edge kernel.

## 12003: an explicit27-channel spectator mass, with its costs

For the ten cubic monomials of three variables, the exact multiplication map

`Sym²(Sym³3) → Sym⁶3`

has dimensions55→28 and rank28. Its27-dimensional kernel is the SU3 irrep `(2,2)`. Its mass tensors fixed by the standard family Heisenberg generators `X,Z` form a **three-dimensional** space. An explicit integer symmetric tensor `N` in this space has

`det(N)=1882576080`.

After multinomial normalization `M=diag(mult)^-1/2 N diag(mult)^-1/2`, the spectator mass is full rank10. Exact checks verify both H27 generators, all kernel equations, and that the eight SU3 Lie variations have rank8: every continuous family generator is broken. H27 is retained; the full finite stabilizer is not identified.

The renormalizable operator is `y chi_bar10^T Phi27 chi_bar10/2`, with `Phi27` an E6 singlet, center-trivial and legal for `(E6×SU3)/Z3`. The **previously established** `(27,3)+(1,bar10)` continuous SU3 anomaly cancellation is unaltered by this scalar. Integrating out the spectator requires threshold Wess–Zumino matching; it does not erase its anomaly.

Compared with the old elementary28-channel mass, this replaces a complex28 (`T=63`,56 real components) by a complex27 (`T=27`,54 real components). In the stated nonsupersymmetric inventory the family one-loop coefficient changes from the old28 case `-57/2` to `-33/2`, still not asymptotically free. The old no-mass-scalar coefficient is `-15/2`. No UV fixed point or mass scale is established.

A **separate optional N=1 extension** introduces an independent dual27 and singletX, with `W=X(PhiBar.Phi-v²)+y chi chi Phi/2`. The supplied pair `Phi=M`, `PhiBar=M*`, `X=chi=0`, `v²=||M||²` gives F=D=0 and a global zero-energy supersymmetric branch. Its mass sector alone retains45 complex flat moduli, excluding the original massless matter directions. This optional extension changes the particle inventory and running; it is not a selected isolated E6 flavour vacuum.

Only SU3 is gauged in this repair. Gauging the extra atlas U1 requires further mixed, cubic and gravitational anomaly cancellation. Neither observed Yukawas nor full E6-to-SM breaking, vacuum alignment, global/discrete anomalies or threshold matching have been completed.

## External checks and reproducibility

- Arnowitt–Deser–Misner, [The Dynamics of General Relativity](https://arxiv.org/abs/gr-qc/0405109): continuum canonical gravity is an input.
- Arrighi–Nesme–Forets, [The Dirac equation as a quantum walk](https://arxiv.org/abs/1307.3524): coined Dirac continuum limits are prior art.
- Hernandez–Jansen–Lüscher, [Locality properties of Neuberger's lattice Dirac operator](https://arxiv.org/abs/hep-lat/9808010): gapped overlap locality is prior art.
- Lüscher, [Abelian chiral gauge theories on the lattice with exact gauge invariance](https://arxiv.org/abs/hep-lat/9811032): conditional acoustic measure theorem, not a newly proved general chiral theory.
- [Radiative corrections to the strong CP problem in Nelson–Barr models](https://arxiv.org/abs/2105.09122): threshold/protection motivation; this packet treats only the explicitly stated channel.
- [Cartan monopoles](https://doi.org/10.1103/PhysRevD.110.045026), representation appendix: decuplet anomaly conventions, not an original anomaly formula here.

Five producers and their same-stem JSON certificates are `w33_pass11999_native_adm_weights`, `w33_pass12000_native_unitary_clock`, `w33_pass12001_radial_portal_decoupling`, `w33_pass12002_native_path_overlap`, `w33_pass12003_h27_decuplet_mass27`. Run12000 before11999/12002. The dedicated workflow regenerates all five between frozen and regenerated regression checks. Tests are in `tests/test_w33_pass11999_12003_native_completion.py`; they include actual-map finite differences, a second gauge volume and arbitrary-link heavy-frame controls.

The parallel TOE93/94 reports were read for intake: the new exact central multiplier and fixed-map CSS face obstruction retain their stated scopes; optical/QKD simulations remain conditional. They are independent of the five proofs above and are not used to infer physical gravity, flavour or quantum security.
