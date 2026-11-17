# The hexagonal torus behind the polyhedra oscillator

The user's pointer is correct: Szilassi has seven hexagonal faces; its dual
Csaszar has fourteen triangular faces. Both describe a genus-one cellulation.
The equilateral intrinsic version is a triangular lattice torus with a
honeycomb dual. This does not assert that the actual embedded polyhedron has
regular hexagons or the same Euclidean metric.

## Prior work and scope

This is an extension of existing results, not a new identification of these
polyhedra. See `analysis/PART_CLXXIII_EISENSTEIN_TORUS_MAP_BRIDGE.py` for the
norm-seven Eisenstein quotient, `analysis/w33_dual_szilassi_from_cyclic_csaszar.py`
for the exact native faces, `analysis/w33_heawood_szilassi_spectrum.py` and
`analysis/w33_heawood_square_recovers_csaszar.py` for the dual graph spectrum,
and `analysis/2026-11-15_csaszar_szilassi_genus_fano_and_sevenfronts.md` for the
earlier audit. The original oscillator discussion is in
`manuscripts/parts/PART_CCCCCXL_TOPOLOGICAL_HARMONIC_OSCILLATOR.md`.
The present executable supplies explicit lattice lifts, harmonic edge
cochains, and nonlinear sampling checks against the continuum triad used in
`analysis/toe_20261117_11D_hexagonal_triad.py`.
The rediscovery guard also points to
`analysis/PART_CLXXIV_FANO_CAYLEY_ALBERT_E6_ALGEBRA.py` and
`analysis/PART_CLXXIX_TORUS_FIREWALL_FACTORIZATION.py`: their Fano/octonion
construction and shared edge-count arithmetic are earlier work. The present
calculation does not establish an additional exceptional-algebra identification.

## Explicit map and oscillator

Use triangular basis Gram matrix Q=((1,1/2),(1/2,1)) and period columns
B=((-3,-1),(1,-2)). Then det(B)=7 and B^T Q B=7Q. The vertex map
(x,y) -> x+3y mod 7 sends the six nearest lattice steps to all six nonzero
residues. The triangular graph is therefore K7. Its native triangles are
{j,j+1,j+3} and {j,j+2,j+3}, modulo seven. The 60-degree lattice rotation
descends to multiplication by three modulo seven.

With unit cellular weights, oriented boundary maps give L0=d1 d1^T,
L1=d1^T d1+d2 d2^T, and L2=d2^T d2. Their spectra are:

| Operator | Eigenvalues (multiplicities) |
| --- | --- |
| Csaszar vertex L0 | 0 (1), 7 (6) |
| Edge L1 | 0 (2), 7 (6), 6 (1), 3-sqrt(2) (6), 3+sqrt(2) (6) |
| Szilassi vertex L2 | 0 (1), 6 (1), 3-sqrt(2) (6), 3+sqrt(2) (6) |

The two edge zero modes are explicit lifted dx,dy cochains: closed and
coclosed with two independent winding periods. These are the torus's genuine
topological harmonic modes. The alternating heat trace is identically zero,
as expected from Euler characteristic zero. This extends a vertex graph
oscillator to the full cellular complex. It does not identify its eigenvalues
with physical particle masses. The existing W33 vertex heat trace
1+24 exp(-10 beta)+15 exp(-16 beta) belongs to a different graph.

The native honeycomb off-diagonal Fourier symbol is
D(k)=1+zeta^k+zeta^(-2k), zeta=exp(2 pi i/7). Its squared norm is nine at k=0
and two otherwise: the signed differences of {0,1,-2} exhaust the six
nonzero residues. This explains the previously recorded Heawood bands
directly in the torus's cyclic labels.

## Nonlinear sampling: a necessary distinction

For C=cos(x)+cos(y)+cos(x+y), Fourier convolution gives these exact averages.
Refinement N samples the torus at 7N^2 points; modes in N B^T Z^2 alias to
zero. The continuum average retains only the zero wavevector.

| Sampling | <C^2> | <C^3> | <C^4> | <C^5> | <C^6> |
| --- | --- | --- | --- | --- | --- |
| 7 sites | 3/2 | 15/4 | 93/8 | 555/16 | 3333/32 |
| 28 sites | 3/2 | 3/2 | 45/8 | 45/4 | 1065/32 |
| 63 sites | 3/2 | 3/2 | 45/8 | 45/4 | 255/8 |
| Continuum | 3/2 | 3/2 | 45/8 | 45/4 | 255/8 |

Thus the minimal Csaszar regulator preserves the quadratic average but adds
cubic resonances. Copying its cubic coupling into the continuum AdS action
would be wrong by a factor 5/2 for this observable. The 28-site refinement
removes aliasing through degree five; 63 sites suffice through degree six
for this particular wave shell. This is not a universal quadrature claim for
arbitrary fields. It also does not fix finite-lattice derivative dispersion.

## Verification and external context

Run `python analysis/toe_20261117_csaszar_szilassi_hexagonal_modes.py`.
All face, period, orientation, Hodge characteristic-polynomial and moment
assertions pass with exact rational arithmetic. The adjacent JSON contains
the regenerated values and lifted harmonic cochains.

Primary external references distinguish toroidal complexes from their spatial
realizations: [Grunbaum and Szilassi, Geometric Realizations of Special Toroidal
Complexes](https://faculty.washington.edu/moishe/branko/BG277%20Toroidal%20complexes.pdf),
and [Ceballos and Doolittle, Generalized Heawood Graphs and Triangulations of
Tori](https://arxiv.org/abs/2307.11859). These support the geometric setting;
the sampling table is calculated by the supplied script.

The resulting bridge is concrete but limited: the oscillator, polyhedra and
hexagonal triad share a torus lattice construction. A physical continuum
limit, interactions, chirality and gravitational dynamics are additional
requirements, not consequences of the shared cellulation.
