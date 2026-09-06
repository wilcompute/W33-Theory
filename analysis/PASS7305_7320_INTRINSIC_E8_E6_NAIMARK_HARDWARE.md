# Passes 7305–7320 — intrinsic E8/E6 reconstruction, exact Naimark transport, and proof-carrying finite hardware

## Boundary first

This packet proves finite incidence, code, root-system, frame, group, and RTL
statements.  It does not derive a continuum theory, a particle assignment, a
mass or coupling, a photonic layout, a quantum state-preparation circuit, or a
laboratory device.  Place-and-route frequencies below are deterministic proxy
results with unconstrained IO, not board measurements.

Two embedding choices must remain separate.  The current W33 code embedding is
transitive on all 120 anisotropic classes of `E8/2E8`; the 36 projective E6
roots occur in the nonconjugate ordered-pair branching embedding.  The explicit
36-root map below chooses an A2 anchor and one H36 isomorphism gauge.  It is an
exact cross-carrier map, not a canonical invariant 36-subset of the 120-orbit.

The classical 27-line, 36-double-six, and exceptional-Lie-algebra background is
consistent with Manivel's configuration models
([paper](https://arxiv.org/abs/math/0507118)) and the classical count of 36
double-sixes recorded by Dolgachev–Kapranov
([paper](https://arxiv.org/abs/alg-geom/9304005)).  Those references provide
context; every identity promoted here is replayed exactly inside the repository.

## 7305–7306 — the E8/D4 spread code decodes the 36 double-sixes intrinsically

Passes 7182/7184 constructed

\[
C_{\rm spread}=[45,21,5]_2
\]

from the 27 ten-D4 spreads in the selected E8 atlas.  Exhausting all
\(2^{21}\) codewords gives 21,168 words of weight 15.  Their intersection
profiles against the intrinsic 27-word minimum shell split into six classes;
exactly 36 have profile

\[
\{0^{12},3^{15}\}.
\]

Those 36 words are exactly the tritangent-disjointness columns of the 36
double-sixes.  Support intersection six reconstructs

\[
H_{36}=\operatorname{SRG}(36,20,10,12),
\]

with 360 adjacent and 270 nonadjacent pairs.  Thus the code and its minimum
shell recover the double-six carrier without importing double-six labels into
the selection rule.

## 7307–7309 — the two visible carriers resolve the whole 36-space

Let \(B\) be the `40 x 36` W33-line/spread incidence and \(N\) the aligned
`45 x 36` tritangent/double-six disjointness incidence.  With \(A\) the
complementary `SRG(36,15,6,6)`, define

\[
C_4=4B-J,
\qquad
D_3=3N-J.
\]

Exact integer linear algebra gives

\[
C_4^TC_4=288E_{15},
\qquad
D_3^TD_3=162E_{20},
\qquad
C_4D_3^T=0,
\]

and

\[
E_{15}+E_{20}+E_1=I_{36}.
\]

Appending the one common scalar mode to the centered rank-20 shadow produces
an `ETF(36,21)` of norm squared `21/2`, off-diagonal values `±3/2`, and
normalized coherence `1/7`.  The full real analysis operator satisfies

\[
T^TT=18I_{36}.
\]

Its multiplier-free integer lowering

\[
K=\begin{bmatrix}3C_4\\4D_3\\6J_{2\times36}\end{bmatrix}
\]

has coefficients `{-4,-3,6,8,9}` and

\[
K^TK=2592I_{36}.
\]

This is an exact finite isometry and shift-add transform.  Standard Naimark
complement theory explains the frame terminology; it does not supply a built
optical mesh.

## 7317–7320 — the new E8/E6 breakthrough

Let

- \(T\) be the `27 x 45` cubic-line/tritangent incidence,
- \(R\) be the `27 x 36` cubic-line/double-six incidence,
- \(N\) be the `45 x 36` tritangent/double-six disjointness matrix.

The raw identity \(T^TR=2(J-N)\) was already owned by Pass 4659.  The new
composition starts by recovering \(R\) from the two intrinsic shells of
\(C_{\rm spread}\):

\[
R_{\ell D}=1
\quad\Longleftrightarrow\quad
\operatorname{supp}(T_\ell)\cap\operatorname{supp}(N_D)=\varnothing.
\]

This reconstructed matrix has row degree 16, column degree 12, and rank 21.
After centering,

\[
T_0=T-\frac19J,
\qquad
R_0=R-\frac49J,
\qquad
N_0=N-\frac13J,
\]

GAP proves

\[
T_0^TR_0=-2N_0,
\quad
T_0T_0^T=6E_{20}^{(27)},
\quad
R_0R_0^T=12E_{20}^{(27)},
\quad
N_0^TN_0=18E_{20}^{(36)}.
\]

Therefore the new rank-20 Naimark shadow is exactly the two-stage partial
isometry

\[
\boxed{
-\frac{N_0}{\sqrt{18}}
=
\left(\frac{T_0}{\sqrt6}\right)^T
\left(\frac{R_0}{\sqrt{12}}\right)
}.
\]

In object language, the 36 double-sixes/projective E6 roots pass through the
common 27-line E6 minuscule carrier into the 45 tritangent/selected-E8-D4-pair
carrier.  This is stronger than a shared dimension: the maps and normalization
are explicit and exact.

The same shell-reconstructed \(R\) identifies 120 of the 1,200 H36 triangles
by empty triple line intersection.  Their triangle-edge matrix has binary rank
325 and a 35-dimensional homogeneous kernel, exactly the cut-space dimension.
Solving the parity system reconstructs the unique switching class whose signed
Gram matrix has

\[
\operatorname{rank}=6,
\qquad
G^2=12G,
\qquad
\operatorname{spec}(G)=12^6\oplus0^{30}.
\]

So the intrinsic E8/D4 spread-code shells reconstruct not only the unsigned
double-six graph but the signed projective E6 root geometry.

### Direct chosen-anchor map to actual E8 roots

In the current 240-root E8 model, choose fiber zero and the two A2 roots

\[
(2,2,0,0,0,0,0,0),
\qquad
(-1,-1,-1,1,-1,1,-1,-1).
\]

The 72 roots orthogonal to this A2 form 36 antipodal root lines.  One frozen
H36 isomorphism maps the intrinsic shell objectwise onto those lines.  Its
mapping SHA-256 is

`d288a0c2e6dc19ce7410cb44934373128af5a26b83f511a49c77818605f9a069`.

The mapped doubled-coordinate roots are all A2-orthogonal and have normalized
Gram profile

\[
(-1)^{120},\quad0^{270},\quad(+1)^{240},
\]

rank six, and spectrum \(12^6\oplus0^{30}\).  The result is exact but depends
on the displayed A2 anchor, a sign convention, and one of 51,840 H36 gauges.

### A useful negative: K is not the E8 Z12 phase carrier

Every column of the integer transform \(K\) is identical modulo 12.  Its row
residue census is

\[
9^{40},\qquad8^{45},\qquad6^2.
\]

Hence `K mod 12` cannot be the nontrivial E8 Z12 grading.  Removing the common
residue and dividing by 12 gives \(Z\) with

\[
Z^TZ=18I_{36}+42J_{36}.
\]

Taking 35 column differences gives

\[
D^TD=18(I_{35}+J_{35}),
\]

a scaled A35 difference lattice.  The negative result blocks a tempting
over-identification while leaving a concrete lattice checksum.

## 7310–7312 — a proof-carrying q=7 finite Pauli validator

The packet freezes one 33-point `GF(7)^4` projective witness and verifies all
528 unordered symplectic products.  Independent rescaling changes the six
nonzero residue-bin populations, so the RTL exports only the projectively
meaningful zero/nonzero predicate.

Yosys SAT proves the Mersenne-fold implementation equivalent to both the signed
integer formula and a naive `% 7` implementation for all \(2^{24}\) raw input
assignments (20,319 variables, 59,982 clauses).  This is exactly the semantics
of the documented `sat -verify -prove-asserts` flow
([Yosys documentation](https://yosyshq.readthedocs.io/projects/yosys/en/v0.60/cmd/index_formal.html)).

Measured `synth_ice40` results are:

| implementation | LUT4 | carry | FF | BRAM | latency |
|---|---:|---:|---:|---:|---:|
| naive pair core | 528 | 262 | 0 | 0 | combinational |
| Mersenne pair core | 129 | 40 | 0 | 0 | combinational |
| full parallel | 58,462 | 21,120 | 0 | 0 | combinational endpoint |
| register serial | 1,637 | 63 | 814 | 0 | 562 cycles |
| BRAM serial | 196 | 63 | 48 | 1 | 1,618 cycles |

The standard projective symplectic/Clifford stabilizer is trivial.  A unique
order-two PCSp symmetry lies outside PSp, fixes one label, and pairs the other
32; it is not a standard Clifford compression.

## 7313–7316 — typed stabilizers and the q=9 trace firewall

Native GAP separates the linear Sp stabilizer, projective PSp image, and
projective conformal PCSp stabilizer:

| q | Sp stabilizer | PSp stabilizer | PCSp stabilizer |
|---:|---:|---:|---:|
| 3 | 18 | 9 | 18 |
| 5 | 24 | 12 | 12 |
| 7 | 2 | 1 | 2 |
| 9 | 4 | 2 | 2 |

For the frozen q=5 18-set, the linear group is `SL(2,3)`, its projective image
is `A4`, and the orbit has size 390,000.  This does not classify every maximum
q=5 set.

At q=9, the physical Weyl–Heisenberg commutator uses the absolute trace from
`GF(9)` to `GF(3)`, not the nonzero field value alone.  Field reduction turns
the 51 GF(9)-projective points into 204 physical F3-projective classes.  Their
commuting graph consists of 51 internal K4 blocks with a 4K2 perfect-matching
crossbar between every pair of blocks; it is 53-regular with 5,406 edges.  The
old “51 pairwise noncommuting physical Pauli classes” reading is therefore
false, while the finite W(3,9) partial-ovoid statement remains valid.

Lean separately checks the generic algebraic rule: rescaling both arguments of
a bilinear similitude changes its multiplier by \(c^2\), so an
antisymplectic map becomes symplectic exactly when \(c^2=-1\).  The finite
enumerations remain GAP-owned.

## Reproduction

```bash
python3 analysis/w33_pass7305_7306_cspread_intrinsic_double_six.py
python3 analysis/w33_pass7307_7309_double_six_naimark_isometry.py
gap -q analysis/w33_pass7310_7312_q7_pauli_validator.g
gap -q analysis/w33_pass7313_7316_pauli_trace_and_stabilizer_scope.g
gap -q analysis/w33_pass7317_7320_e8_d4_double_six_fusion.g
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest -q \
  tests/test_w33_pass7305_7306_cspread_intrinsic_double_six.py \
  tests/test_w33_pass7307_7309_double_six_naimark_isometry.py \
  tests/test_w33_pass7310_7312_q7_pauli_validator.py \
  tests/test_w33_pass7313_7316_pauli_trace_stabilizer_scope.py \
  tests/test_w33_pass7317_7320_e8_d4_double_six_fusion.py
```

