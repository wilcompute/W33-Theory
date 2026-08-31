# Seven-sector spectral algebra of the bicoloured 216 x 540 circuit incidence

## Exact setup

Let `C5` be the 216 sentinel five-circuits and `C6` the 540 sentinel six-circuits.  The maximal-overlap relation

\[
|C_5\cap C_6|=3
\]

is a `(20,8)`-biregular `216 x 540` incidence relation and splits into two `PSp(4,3)` orbitals of size 2160.  Write their biadjacency matrices as `M+` and `M-`.  Each colour is `(10,4)`-biregular.

The CI-verified exact audit proves

\[
M_+M_+^T=M_-M_-^T=10I+A_{30},
\]

\[
M_+M_-^T+M_-M_+^T=4A_{20},
\]

where `A30` and `A20` are respectively 30- and 20-regular simple graphs on the 216 five-circuits. Their edge sets are disjoint, and

\[
[A_{30},A_{20}]=0.
\]

Consequently, for the uncoloured maximal-overlap incidence matrix `M=M++M-`,

\[
MM^T=20I+2A_{30}+4A_{20}.
\]

## Exact spectra

The relation graph spectra are

\[
\operatorname{Spec}(A_{30})=
30^1,12^{15},6^{39},0^{60},(-4)^{81},(-6)^{20},
\]

and

\[
\operatorname{Spec}(A_{20})=
20^1,8^{24},2^{80},(-2)^{81},(-4)^{15},(-10)^{15}.
\]

Because the two matrices commute, their simultaneous eigenspaces can be resolved exactly.  A separating operator

\[
A_{30}+7A_{20}
\]

has seven distinct certified eigenvalues

\[
-58,-22,-18,8,14,62,170,
\]

and forces precisely seven joint sectors:

| `A30` | `A20` | dimension | `MM^T` eigenvalue |
|---:|---:|---:|---:|
| -4 | -2 | 81 | 4 |
| 0 | 2 | 60 | 28 |
| 6 | 8 | 24 | 64 |
| -6 | 2 | 20 | 16 |
| 12 | -10 | 15 | 4 |
| 6 | -4 | 15 | 16 |
| 30 | 20 | 1 | 160 |

Thus the exact joint-sector dimensions are

\[
\boxed{1,15,15,20,24,60,81}.
\]

The uncoloured Gram spectrum is

\[
\boxed{
\operatorname{Spec}(MM^T)=
160^1+64^{24}+28^{60}+16^{35}+4^{96}.
}
\]

In particular `M` has full row rank 216 over characteristic zero.  The associated 756-vertex bipartite adjacency matrix has zero multiplicity 324 and nonzero eigenvalues

\[
\pm4\sqrt{10},\quad
\pm8,\quad
\pm2\sqrt7,\quad
\pm4,\quad
\pm2
\]

with multiplicities `1,24,60,35,96` on each sign respectively.

## Proof mode

The executable does not infer this theorem from floating-point diagonalisation. It certifies annihilating polynomials with exact integer matrix arithmetic and recovers multiplicities from exact traces.  The seven-eigenvalue separating operator eliminates all other Cartesian pairings of the individually certified spectra.

## Interpretation boundary

The seven simultaneous eigenspaces are exact `PSp(4,3)`-invariant spectral sectors of this commutative incidence algebra.  Their dimensions are suggestive of known representation dimensions, especially `15,20,24,60,81`, but irreducibility or identification with named complex `PSp(4,3)` representations is **not** asserted without a separate character-theoretic audit.

## Reproducibility

- executable: `analysis/w33_20260830_c5_c6_bicolour_spectral_algebra.py`
- certificate: `data/PART_W33_20260830_C5_C6_BICOLOUR_SPECTRAL_ALGEBRA.json`
- exact CI: `Frontier Continuation 20260829`, run `33345071604`, success
