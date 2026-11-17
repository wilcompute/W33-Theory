# The hexagonal torus needs dynamics, refinement and an independent flux choice

The oscillator connection has now been tested as a dynamical regulator. The
minimal seven-site model reproduces topology but substantially distorts both
the continuum dispersion and a three-flux fermion index. Refinement corrects
both in the explicit models below. Flat Wilson lines do not generate a net
chiral index. This is useful progress toward a consistent microscopic model,
but it does not select a physical compactification or Standard Model vacuum.

## Provenance and the actual object

The lattice is the existing norm-seven Eisenstein torus, not a newly chosen
square grid: Z^2/(N B Z^2), B=((-3,-1),(1,-2)), with 7N^2 vertices. Its
N=1 triangulation is the native Csaszar complex and its dual is Szilassi.
The prior map and oscillator results belong to
`analysis/PART_CLXXIII_EISENSTEIN_TORUS_MAP_BRIDGE.py`,
`analysis/w33_dual_szilassi_from_cyclic_csaszar.py`,
`analysis/w33_heawood_szilassi_spectrum.py`, and
`analysis/2026-11-17_csaszar_szilassi_hexagonal_modes.md`.

The overlap-index mechanism is established prior art. The repo already
executes it on a square torus in
`analysis/toe_20261105_overlap_flux_chirality_index.py` and discusses its input
dependence in `analysis/2026-11-05_operator_obstruction_regge_chirality_witting_bridge.md`.
The four-dimensional construction also already exists in
`analysis/toe_20261103_mechanism_four_dimensional_overlap.py`.
The earlier Fano/octonion construction is also recorded in
`analysis/PART_CLXXIV_FANO_CAYLEY_ALBERT_E6_ALGEBRA.py`; it does not select
the spinor regulator or flux used here.
The extension here is the actual norm-seven lattice, its coarse-regulator
failure and refinement checks; no discovery of the index mechanism is claimed.

## Scalar dispersion

The physical triangular basis has unit vectors e1=(1,0), e2=(1/2,sqrt(3)/2).
For lattice spacing h=1/N, use the positive operator

    L_h = (2/(3 h^2)) sum_{d=e1,e2,e1-e2} (2-T_d-T_d^dagger).

Its continuum limit is -Delta. At fixed physical momentum k it has symbol

    |k|^2 - h^2 |k|^4/16 + O(h^4).

The six first reciprocal-shell waves have continuum eigenvalue
16 pi^2/21 = 7.519698591306178. Their degeneracy is exact at every tested N.
A standard stride-two extrapolation cancels the h^2 term. In each direction
its symbol is proportional to
4 sin(t/2)^2 (1+sin(t/2)^2/3), so the improved operator is positive, despite
negative coefficients on some longer links. Its leading error is

    -h^4*(11 kx^6+15 kx^4 ky^2+45 kx^2 ky^4+9 ky^6)/1440.

The sixth-degree polynomial is compatible with sixfold symmetry, but is not
fully rotationally invariant. Fourth-order accuracy is distinct from exact
rotational invariance.

| Sites | Nearest-neighbor relative error | Improved relative error |
| --- | --- | --- |
| 7 | -37.94% | -22.43% |
| 28 | -11.13% | -2.193% |
| 63 | -5.097% | -0.4716% |
| 112 | -2.898% | -0.1537% |
| 448 | -0.7319% | -0.009891% |

The nearest-neighbor seven-site eigenvalue is 14/3, the previous K7 eigenvalue
7 with the geometrically required 2/3 factor. Direct hopping-matrix action
checks the Fourier symbol independently on all six waves at N=1,2,3.
Thus exact topology and even exact polynomial sampling do not by themselves
make a tiny graph a quantitatively accurate continuum regulator.

## Explicit triangular gauge field and fermion operator

Use period columns (7N,0), (4N,N), the Hermite normal form of N B. Sites are
(a,b), 0<=a<7N, 0<=b<N. Links in each of the three lattice directions are
straight parallel transports of A=-F b da, F=2 pi Q/(7N^2), with the required
boundary transition phases. The two positively oriented triangles at every
site have phase pi Q/(7N^2); summing their principal phases measures Q in the
tested regime. Boundary phases around the two period columns are independent
flat holonomies. Every transport is unitary and both triangular plaquette
identities are checked as full matrices.

Supply two Pauli spinor components and choose a Wilson parameter of one:

    D_W(-m) = (1/3) sum_d gamma.d (T_d-T_d^dagger)
              +(1/3) sum_d (2-T_d-T_d^dagger) - m.
    H_W = sigma3 D_W(-m)
    D_ov = 1 + sigma3 sign(H_W)
    index = -Tr sign(H_W)/2.

This is a chosen internal two-dimensional Euclidean spinor regulator. It is
not the cellular de Rham oscillator reinterpreted as a spinor without extra
structure. The lattice sites are those of the same polyhedral torus.

For free momenta p,q, the kinetic zeros are Gamma, the three M points and two
K points. Exhaustiveness follows from sin(q)=sin(p-q): either p=2q modulo
2pi, giving sin(q)(2cos(q)+1)=0, or p=pi, giving sin(q)=0. Their derivative
orientations are +1,-1,-1,-1,+1,+1; Wilson values are 0,8/3,8/3,8/3,3,3.
Consequently the free single-species mass interval is 0<m<8/3. Finite magnetic
fields can shift actual kernel crossings; the free interval alone is not an
admissibility proof at finite spacing.

## Results: a chiral index can survive, but seven sites can erase it

For Q=-3,-1,0,1,3 and m=0.5,1,2, the script diagonalizes all 60 combinations
at N=1,2,3,4. The sign convention is index=-Q in the resolved physical branch.

| Sites | Index at Q=3, m=0.5 | m=1 | m=2 |
| --- | --- | --- | --- |
| 7 | 0 | 0 | -2 |
| 28 | -3 | -3 | -3 |
| 63 | -3 | -3 | -3 |
| 112 | -3 | -3 | -3 |

At N=2,3,4 every tested Q and mass gives index=-Q. At N=3,m=1 the Q=3
overlap matrix has exactly three zero modes, each with chirality -1 to
floating-point accuracy. Flux reversal reverses the index. At N=4,Q=1,
moving m through 1,2.8,3.5 gives indices -1,+2,0, consistent with the different
free doubler branches. A regulator branch must therefore be specified.

At Q=0, trivial holonomy gives two zero modes with opposite chiralities;
three tested nontrivial holonomies remove both. All have index zero. More
generally, each free momentum block of H_W is a traceless Hermitian 2x2
matrix, hence has paired eigenvalues whenever gapped. Flat holonomies only
shift momenta; they cannot produce a nonzero index in this free model.

## Robustness and physical limits

At 28 sites, Q=3,m=1 has Wilson-kernel gap 0.6465757373451908. Random site
gauge conjugation preserves it to floating-point accuracy. Independent link
phase noise bounded by 0.02 radians preserves index -3, total flux three and
gives gap 0.6445860083551516. Conjugating the noisy field gives the same gap.
The bound

    ||delta H_W|| <= 8 sin(eta/2)

follows from three directions and the kinetic plus Wilson norm bounds.
For eta=0.02 this is less than 0.08, far below the measured gap. Thus the
entire bounded perturbation ball stays in the same index sector, conditional
on the measured baseline gap. The calculation uses dense floating-point
eigensolvers, not a formal interval spectral certificate. Explicit overlap
matrices check the Ginsparg-Wilson identity and zero-mode chirality.

No mechanism here selects Q=3. In fact the supplied pure plaquette action on
the uniform background is 14N^2*(1-cos(pi Q/(7N^2))), minimized at Q=0 among
distinct principal-flux sectors. Other interactions or constraints would be
needed to prefer nonzero flux. A three-dimensional kernel does not supply
Standard Model representations, anomaly cancellation, Yukawa couplings or
an interacting chiral measure. A flat gauge holonomy also does not remove
the neutral scalar instability of the existing gravity compactification.
Adding magnetic matter and its backreaction would change that model.

## A further dynamical bridge: Landau levels and a vortex-condensate quartic

The charged scalar uses precisely the same transports. The continuum
magnetic field magnitude is |B|=4 pi |Q|/(7 sqrt(3)); the first two Landau
levels should be |B| and 3|B|, each |Q|-fold degenerate. Both bands approach
these limits. At 448 sites the lowest-band relative errors are -0.2022% for
Q=1 and -0.6048% for Q=3; the next-band errors are -0.3368% and -1.0065%.
The finite-band splittings are retained in the certificate.

The recent paper [Akamatsu et al., Vacuum structure of a scalar field on a
torus with uniform magnetic flux](https://arxiv.org/abs/2604.22248), published
in PTEP in 2026, studies scalar condensation near a critical area, with a
fixed magnetic background. Its numerical vacuum classification uses a
square torus. This suggested testing the quartic functional on our
hexagonal torus instead. The older repo already owns normalized magnetized
wavefunction overlaps, e.g.
`analysis/w33_20261010_toe46_magnetized_overlap_flux336.py`; we do not claim a
new mechanism for flux-induced families or Yukawas.

For lowest-band eigenvectors U and a unit coefficient vector c, minimize

    beta_N(c) = (7N^2) sum_sites |(U c)_site|^4.

This is the interaction ratio <|psi|^4>/<|psi|^2>^2. At Q=3 sixteen
deterministic random starts give the same candidate value at each tested
refinement, within 6e-13. This is a local multistart search, not a proof of
global optimality, and it neglects the tiny finite-band splitting.

| Sites | Q=1 beta | Q=3 candidate beta |
| --- | --- | --- |
| 63 | 1.159584974471 | 1.159702851141 |
| 112 | 1.159592113082 | 1.159626099903 |
| 252 | 1.159594657957 | 1.159600950824 |
| 448 | 1.159595075788 | 1.159597022924 |

Both approach the established triangular Abrikosov ratio

    beta_triangle = sum_{a,b in Z} exp[-(2 pi/sqrt(3))(a^2+ab+b^2)]
                  = 1.159595266964...

The finite regulator need not obey the continuum bound; the Q=1 numbers
approach from below. In the continuum lowest-mode approximation, a supplied
Higgs potential -mu^2 |phi|^2+lambda |phi|^4 has critical area
A_c=2 pi |Q|/mu^2. If <|psi|^2>=1, the condensate's reduced energy density is
(|B|-mu^2) rho^2+lambda beta rho^4. Minimizing it gives
rho^2=(mu^2-|B|)/(2 lambda beta) above threshold. This supplies an actual
interaction-based reason for investigating a hexagonal condensate, beyond
the polyhedron's face shape. The flux, potential and fixed-field approximation
are still imposed; the neutral gravity triad is not thereby identified with
this charged order parameter.

There is also an exact explanation for the different convergence rates.
Using normalized oscillator variables, the script verifies

    sum_d (d.Pi)^4 |0> = (9/4) B^2 |0>
    sum_d (d.Pi)^6 |0> = B^3 [(45/8)|0>+(9 sqrt(5)/2)|6>].

The triangular stencil's h^2 correction shifts the lowest Landau energy
without mixing higher levels. Its first mixing is with level six at h^4:

    E0 = B-h^2 B^2/8+h^4 B^3/96+O(h^6)
    |psi0> = |0>-h^4 B^2 sqrt(5)/1440 |6>+O(h^6).

These are formal smooth-field expansions for B>0. Sixfold symmetry removes
the level-two and level-four mixing channels. This explains why the
quartic ratios can converge more rapidly than the energies; it is not a
proof of the full nonlinear vacuum's convergence or stability.

Triangular vortex-lattice energetics are established physics, see
[Tzaneteas and Sigal](https://arxiv.org/abs/1112.1897). A preprint posted
12 November 2026 by [Di Fratta and Slastikov](https://arxiv.org/abs/2611.17543)
reports a broader coefficient-identification result for rotating condensates.
That theorem and its stated premises are separate from our finite torus
calculation; our numerical agreement is not a verification of their proof.

Including a dynamical gauge field supplies a further decisive boundary. For
the minimal Abelian-Higgs energy measured above its homogeneous vacuum,
the terms B^2/(2g^2), |D phi|^2 and lambda(|phi|^2-v^2)^2 are nonnegative.
The Q=0 homogeneous Higgs vacuum attains zero. A nonzero-flux sector cannot
attain zero, so this model alone does not energetically select three flux
quanta, even after allowing gauge backreaction.

At lambda=g^2/2 the standard Bogomolny square completion, checked symbolically
in the script, gives E_relative>=2 pi |Q| v^2. Integrating the BPS equation
B=g^2(v^2-|phi|^2) gives the necessary area bound
A>=2 pi |Q|/(g^2 v^2). Since mu^2=g^2 v^2 at this tuning, this is precisely
the critical-area expression above. The connection to the established
[Bradlow bound](https://users.math.msu.edu/users/parker/993Spring11/Bradlow_Vortices.pdf)
is therefore explicit in matching conventions. It is not a new bound.
At BPS coupling vortex positions are moduli; the fixed-field quartic search
must not be presented as lifting those moduli in the fully coupled theory.

## Reproduction and external research

Run `python analysis/toe_20261117_hexagonal_regulator.py`. The adjacent data
certificate records all spectra, measured fluxes, dispersion errors and
robustness controls. Runs were executed on the authorized local device via
Remote Desktop Commander while the external literature was checked.

The standard methods and limits are consistent with
[Thampi et al., Isotropic discrete Laplacian operators](https://arxiv.org/abs/1202.3299),
[Chow, Discretization errors on non-hypercubical lattices](https://arxiv.org/abs/hep-lat/9810051),
[Neuberger, Exactly massless quarks on the lattice](https://arxiv.org/abs/hep-lat/9707022),
and [Kurokawa and Fujiwara, uniform-field Wilson-Dirac spectrum](https://doi.org/10.1103/PhysRevD.67.025015).
[Aoki et al., The index of lattice Dirac operators and K-theory, published
2026](https://arxiv.org/abs/2407.17708) proves a continuum/lattice index
correspondence at sufficiently fine spacing for its stated Wilson setup.
It motivates the refinement test; it is not a proof of our specific oblique
triangular stencil or its finite-spacing thresholds. Our table is an explicit
finite-matrix calculation.
