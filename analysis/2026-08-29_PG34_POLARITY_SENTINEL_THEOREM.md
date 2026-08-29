# PG(3,4) polarity closure: the 45 Hermitian supports are exactly the W33 sentinel minima

Date: 2026-08-29

**Status: PASS.** The executable certificate is
`analysis/w33_20260829_pg34_polarity_sentinel.py`; the machine-readable output is
`data/PART_W33_20260829_PG34_POLARITY_SENTINEL.json`.

This packet continues the independently reconstructed 40x45 Hermitian
cross-incidence matrix `B` from the 85-state W33/GQ(4,2) module. It produces
one classical closure and one project-specific identification.

## 1. The loopless 85-state operator is one diagonal away from PG(3,4)

The existing 85-state module writes the loopless Hermitian-polarity adjacency as

\[
P=\begin{pmatrix}
A_{W33}&B\\
B^T&A_{GQ(4,2)}
\end{pmatrix},
\]

with 40 nonisotropic and 45 isotropic points. Hermitian polarity fixes exactly
the 45 isotropic points. Therefore the point-to-polar-plane incidence matrix is

\[
H=P+\operatorname{diag}(0^{40},1^{45}).
\]

The certificate rebuilds this matrix from W(3,3) alone and verifies entry by
entry

\[
\boxed{H^2=16I_{85}+5J_{85}}.
\]

Equivalently, every polar plane contains 21 points and two distinct polar
planes meet in 5 points. Thus `H` is the symmetric

\[
\boxed{2-(85,21,5)}
\]

point-plane design of `PG(3,4)`, expressed in the repository's native
40+45 Hermitian coordinates.

Because `H 1 = 21 1` and `tr(H)=45`, its exact spectrum is

\[
\boxed{21^1,\quad 4^{45},\quad (-4)^{39}}.
\]

Immediate exact consequences are

\[
\det H=-21\,4^{84},
\qquad
H^{-1}=\frac1{16}H-\frac5{336}J.
\]

This is a useful simplification of the earlier loopless spectrum: the quadratic
irrational pairs there are produced solely by deleting the 45 polarity loops.
The full polarity incidence has only three integral eigenvalues.

## 2. Binary reduction: the 45 cross-neighborhoods generate the sentinel

Reduce the same cross-incidence `B` modulo two and regard its 45 columns as
40-bit words. Each column has weight eight. Exact row reduction gives

\[
\operatorname{rank}_{2}B=15.
\]

Enumerating all \(2^{15}\) words in their span gives

\[
\boxed{
1+45z^8+720z^{12}+6930z^{16}+17376z^{20}
 +6930z^{24}+720z^{28}+45z^{32}+z^{40}
}.
\]

This is exactly the already-certified weight enumerator of the historical
W33 sentinel code

\[
\mathcal S=[40,15,8]_2.
\]

More strongly, the certificate compares sets, not just enumerators:

\[
\boxed{\{\text{45 columns of }B\}
      =\{\text{all weight-8 words of }\mathcal S\}.}
\]

Hence the 45 minimum sentinel words have four simultaneous exact
interpretations:

1. the 45 columns of the Hermitian 40x45 cross-incidence;
2. the nonisotropic neighborhoods of the 45 isotropic points of `PG(3,4)`;
3. the 45 eight-point supports from the antipodal trade-lattice minima;
4. all minimum-weight words of the W33 `[40,15,8]_2` sentinel code.

The code is self-orthogonal and doubly even directly from this generator set.

## 3. The 85-code / 40-code diagram

Over `F_2` the full 85x85 point-plane matrix has rank

\[
\operatorname{rank}_2 H=17,
\]

recovering the classical `[85,17,21]_2` code of the `2-(85,21,5)` design.

Puncturing the full plane code to the 40 nonabsolute coordinates has rank 16.
But if one takes only the 45 rows indexed by **absolute** Hermitian points and
then restricts those rows to the 40 nonabsolute coordinates, the result has
rank 15 and is exactly `S`.

So the sentinel has a clean geometric construction inside the 85-point space:

\[
\boxed{
\mathcal S
=
\left.
\langle \text{polar planes of the 45 absolute points}\rangle_{\mathbf F_2}
\right|_{\text{40 nonabsolute points}}.
}
\]

This is stronger than a common group-order or dimension match: it supplies
explicit generators in the coordinates already used by the W33 trade lattice,
the GQ(4,2) carrier and the 85-state coupling.

## 4. Attribution and novelty boundary

The following facts are classical/published and are **not** claimed as new here:

- `PG(3,4)` has the symmetric `2-(85,21,5)` point-plane design;
- the associated binary plane code is `[85,17,21]_2`;
- the `S_4(3)`/`PSp(4,3)` degree-40 action has an invariant doubly-even
  `[40,15,8]_2` code.

The new project-level statement is the exact identification through the
independently reconstructed `B`: its 45 columns are precisely all 45
minimum-weight sentinel words, and adding the 45 absolute loops to the existing
85-state operator reconstructs the classical polarity design with
`H^2=16I+5J`.

Literature cross-checks used while drawing this boundary:

- B. G. Rodrigues, *Self-orthogonal designs and codes from the symplectic
  groups S4(3) and S4(4)*, Discrete Mathematics 308 (2008), 1941-1950;
- the standard `PG(3,4)` point/hyperplane design `2-(85,21,5)`;
- the repository's earlier `analysis/2026-07-10_levi_next5_v2.md`, which
  independently certifies the sentinel enumerator.

## 5. Why this matters for the current frontier

The same 40x45 matrix now has four exact roles without changing coordinates:

- over `Q`, it couples the common `1+24` sectors and exposes the 15+20 chiral
  kernels;
- over `Z`, its 45 columns are the eight-support incidence of the trade/GQ
  carrier;
- over `F_2`, those columns are exactly the 45 minimum sentinel codewords;
- after restoring the absolute loops, it is one off-diagonal block of the
  full `PG(3,4)` polarity design satisfying `H^2=16I+5J`.

That makes the 85-point Hermitian module a genuine **coefficient-change
junction** between representation theory, integral trade geometry and binary
error detection. No physical particle, Hamiltonian or measured coupling is
inferred from that statement; it is an exact finite-geometric/code theorem.
