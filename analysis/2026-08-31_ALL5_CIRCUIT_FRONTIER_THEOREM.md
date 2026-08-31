# All-five circuit frontier theorem: Clifford restrictions, Eisenstein sixes, 540-kernel geometry, Smith filtration, and rank-76 coherent closure

## Setup

Let `C5` be the 216 sentinel five-circuits and `C6` the 540 sentinel six-circuits.  For the maximal-overlap relation `|C5 intersect C6|=3`, let

- `M` be the `(20,8)`-biregular `216 x 540` incidence matrix;
- `M+` and `M-` be its two `PSp(4,3)` orbital colours, each `(10,4)`-biregular;
- `A30,A20` be the commuting five-circuit relation matrices determined by

\[
M_+M_+^T=M_-M_-^T=10I+A_{30},
\qquad
M_+M_-^T+M_-M_+^T=4A_{20}.
\]

The previously certified joint sectors of `A30,A20` have dimensions

\[
1,15,15,20,24,60,81.
\]

This release executes all five previously listed frontier tasks in one exact reconstruction and then resolves an additional directed refinement hidden by the symmetric `A20` fusion.

## 1. All seven sectors under the order-648 point stabilizer

Let `K` be the stabilizer of a W33 point.  Its center is `Z(K)=C3=<z>`.  Exact rational spectral projectors and traces against all 648 elements give the following restriction data.  The three central columns are the dimensions of the `1,omega,omega^2` isotypic pieces; the last column is the exact norm of the restricted character.

| sector dimension | `1` | `omega` | `omega^2` | character norm |
|---:|---:|---:|---:|---:|
| 15 | 3 | 6 | 6 | 3 |
| 15 | 3 | 6 | 6 | 3 |
| 81 | 27 | 27 | 27 | 12 |
| 20 | 8 | 6 | 6 | 3 |
| 60 | 18 | 21 | 21 | 12 |
| 24 | 12 | 6 | 6 | 5 |
| 1 | 1 | 0 | 0 | 1 |

Thus every nontrivial spectral sector now has an exact central-sheet profile.  These norms are intentionally reported rather than guessed into named irreducibles: norm greater than one proves reducibility of the restriction but does not by itself specify a unique irreducible decomposition.

The previously isolated 24-sector row agrees with

\[
24\downarrow_K=1\oplus3\oplus8\oplus6_\omega\oplus6_{\bar\omega}.
\]

## 2. Concrete Eisenstein geometry of the conjugate sixes

On the 12-dimensional rational nontrivial-central carrier inside the 24-sector, define the canonical deck-orientation operator

\[
J=z-z^2.
\]

The exact projector calculation proves

\[
\boxed{J^2=-3I}
\]

on this carrier.  Consequently its scalar extension to `Q(sqrt(-3))=Q(omega)` splits into the two six-dimensional eigenspaces of eigenvalues `+sqrt(-3)` and `-sqrt(-3)`, which are exactly the conjugate `6_omega` and `6_{omega^2}` carriers.

The audit also gives a deterministic witness consisting of six central `C3` deck fibres: one projected vector from each fibre together with its `J`-image forms a 12-vector rational basis.  Equivalently, the same six fibres supply a six-vector basis after passing to the Eisenstein field.  This is a concrete deck-fibre realization of the two sixes, not merely a character-dimension coincidence.

## 3. The 540-side image/kernel geometry

Over characteristic zero,

\[
\operatorname{rank}M=\operatorname{rank}M_+=\operatorname{rank}M_-=216.
\]

Hence all three right kernels in the 540-dimensional six-circuit space have dimension

\[
\boxed{324}.
\]

The stacked colour matrix has exact rank

\[
\operatorname{rank}\begin{bmatrix}M_+\\M_-\end{bmatrix}=372,
\]

so the two colour row spaces meet in

\[
\boxed{216+216-372=60}
\]

dimensions.  Dually, the three right kernels satisfy

\[
\boxed{
\dim(\ker M_+\cap\ker M_-)
=\dim(\ker M\cap\ker M_+)
=\dim(\ker M\cap\ker M_-)
=168.
}
\]

Because `M=M++M-`, these pairwise intersections coincide with the triple intersection:

\[
\boxed{\dim(\ker M\cap\ker M_+\cap\ker M_-)=168.}
\]

The right Gram spectrum is therefore

\[
\operatorname{Spec}(M^TM)
=0^{324}+4^{96}+16^{35}+28^{60}+64^{24}+160^1.
\]

The equality between the 60-dimensional common colour row space and the existing 60-dimensional left spectral sector is a strong structural target, but **this release does not identify them without an explicit projector/intertwiner equality**.

## 4. Modular ranks and constrained Smith structure

Exact modular elimination gives:

| `p` | rank `M` | rank `M+` | rank `MM^T` |
|---:|---:|---:|---:|
| 2 | 156 | 201 | 0 |
| 3 | 216 | 216 | 216 |
| 5 | 216 | 216 | 215 |
| 7 | 216 | 216 | 156 |
| 11 | 216 | 216 | 216 |
| 13 | 216 | 216 | 216 |

From the exact Gram spectrum,

\[
v_2\det(MM^T)=601,\qquad
v_5=1,\qquad
v_7=60,
\]

and no other prime divides the Gram determinant.  If a prime divides a nonzero Smith invariant of `M`, every maximal minor is divisible by that prime and therefore the Cauchy--Binet sum `det(MM^T)` is divisible by its square.  Since `M` remains full row rank modulo 5 and 7, the only possible nonunit prime is 2.  The mod-2 rank then fixes the count:

\[
\boxed{\operatorname{SNF}_{\rm nonzero}(M)=1^{156}\oplus(2\text{-power})^{60}.}
\]

The individual 60 positive 2-adic exponents are not resolved here.

Likewise `M+M+^T=10I+A30` has determinant supported only on `2,3,5,11`; `M+` is full row rank modulo `3,5,11` and has mod-2 rank 201.  Thus

\[
\boxed{\operatorname{SNF}_{\rm nonzero}(M_+)=1^{201}\oplus(2\text{-power})^{15},}
\]

and the same statement holds for `M-` by colour symmetry.  Again, the individual positive 2-adic exponents remain open.

## 5. Full two-fibre coherent configuration

The complete Schurian orbital enumeration under `PSp(4,3)` gives

\[
r_{55}=10,\qquad r_{66}=32,\qquad r_{56}=r_{65}=17.
\]

Hence the coherent configuration on the disjoint union of the 216 five-circuits and 540 six-circuits has exact total rank

\[
\boxed{10+32+17+17=76}.
\]

The audit computes the cross-product structure constants into both same-fibre orbital algebras.  In the deterministic `C5 x C5` orbital enumeration,

- `A30` is one single orbital, id `6`;
- `A20` is the fusion of exactly two orbitals, ids `1` and `2`.

Thus the seven-sector commutative algebra is a proper symmetric fusion of the larger 10-orbital five-circuit commutant.

## Directed refinement hidden inside A20

The two constituents of `A20` are transpose-paired directed orbitals, each of valency 10.  Writing

\[
K_c=M_+M_-^T,
\]

its constant values on the pair are exactly `1` and `3`; transpose exchanges them.  Therefore

\[
\boxed{K_c+K_c^T=4A_{20}.}
\]

However,

\[
[K_c,A_{20}]\ne0,
\qquad
[K_c,A_{30}]\ne0.
\]

So the orientation information is not an eighth simultaneous eigenoperator appended to the old seven-sector algebra.  It lives in the genuinely noncommutative 10-orbital `C5` commutant.  The symmetric seven-sector theory is obtained only after erasing this directed distinction.

This is an exact finite-geometry orientation datum.  No identification with physical chirality, helicity, or the separate Holotrade chirality variable is asserted without an explicit equivariant map.

## Reproducibility

- all-five executable: `analysis/w33_20260831_all5_frontier_audit.py`
- directed refinement executable: `analysis/w33_20260831_a20_directed_orbital_refinement.py`
- frozen regression: `analysis/w33_20260831_all5_frontier_freeze.py`
- committed release packet: `data/PART_W33_20260831_ALL5_FRONTIER_KEY_RESULTS.json`
- all-five exact CI: `Frontier Continuation 20260829`, run `33347796426`, success
- directed-refinement exact CI: `Frontier Continuation 20260829`, run `33347955106`, success
