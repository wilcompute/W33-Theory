# Pass 361 — logical Hadamard is exact, and maximal in the simple lift class

## Result

Pass 360 constructs an exact logical Hadamard on the quadratic-residue CSS code

\[
[[137,1,21]].
\]

Pass 361 proves the corresponding boundary.  Modulo Pauli phases, among every
operation made from

1. the same one-qubit Clifford on all 137 qubits, and
2. an arbitrary coordinate permutation,

the only Pauli-label actions that can normalize this CSS stabilizer are

\[
I\quad\text{and}\quad H:X\leftrightarrow Z.
\]

Thus Pass 360's logical image \(\langle\overline H\rangle\cong C_2\) is maximal
inside this uniform local-Clifford-plus-permutation class.  In particular, a
uniform logical phase gate is not hiding in the same construction.

A stronger diagonal check also closes the obvious nonuniform escape: no
nonempty subset of physical phase gates \(S\) (or \(S^\dagger\), which has the
same binary Pauli-label action) normalizes the fixed CSS splitting, even after a
coordinate symmetry that preserves or exchanges the QR/NQR halves.

## The orthogonal decomposition that makes the proof work

Write

\[
A=Q^\perp,
\qquad
B=N^\perp
\]

for the two rank-68 check spaces in \(\mathbb F_2^{137}\), and let \(E\) be the
even-weight hyperplane.  GAP proves

\[
\dim A=\dim B=68,
\qquad
A\perp B,
\qquad
A\cap B=0,
\qquad
A\oplus B=E.
\]

The restrictions of the binary dot product to both \(A\) and \(B\) are
nondegenerate: both self-Gram matrices have rank 68.  The all-ones vector is
orthogonal to \(E\) and has odd norm, so the entire ambient space decomposes as

\[
\boxed{
\mathbb F_2^{137}
=A\perp B\perp\langle\mathbf1\rangle
}
\qquad(68+68+1).
\]

The odd-like codes themselves are recovered without another generator:

\[
Q=B\oplus\langle\mathbf1\rangle,
\qquad
N=A\oplus\langle\mathbf1\rangle.
\]

This is the linear-algebraic core behind both the CSS code and its logical
duality.

## Why only identity and Hadamard survive uniformly

Modulo phases, the one-qubit Clifford group acts on the three nonzero binary
Pauli labels

\[
X=(1,0),\qquad Z=(0,1),\qquad Y=(1,1)
\]

through

\[
GL(2,2)\cong S_3,
\]

which has six matrices.  Suppose a uniform label map sends one of \(X,Z\) to
\(Y\).  For a nonzero check support \(v\), any coordinate permutation sends
\(v\) to another nonzero support \(u\).  A \(Y\)-labelled image has both
\(X\)- and \(Z\)-support equal to \(u\).  Membership in the CSS stabilizer
would therefore require

\[
u\in A\cap B=0,
\]

a contradiction.  Four of the six matrices contain a \(Y\) column.  The only
two that do not are the identity and the \(X/Z\) swap.  Pass 360 constructs
both possibilities: residue-affine permutations realize identity, while a
nonresidue permutation composed with transversal \(H\) realizes the swap.

Since every coordinate permutation fixes \(\mathbf1\), these induce exactly
the identity and \(\overline H\) on the all-ones logical Pauli pair.

## The 4,692-constraint phase-mask no-go

Let \(m\in\mathbb F_2^{137}\) mark a subset of qubits on which an odd power of
\(S\) is applied, and put \(D_m=\operatorname{diag}(m)\).  On binary Pauli
labels,

\[
X(v)\longmapsto X(v)Z(D_mv).
\]

For every \(X\)-check to remain a stabilizer, one must have

\[
D_mA\subseteq B.
\]

Because \(B^\perp=N\), this is equivalent to

\[
\sum_i m_i a_i n_i=0
\quad
\text{for all }a\in A, n\in N.
\]

Using bases of dimensions 68 and 69 gives \(68\cdot69=4{,}692\) binary linear
constraints on the 137 mask bits.  GAP finds

\[
\operatorname{rank}=137,
\qquad
\operatorname{nullity}=0.
\]

The reverse system \(D_mB\subseteq A\) independently has the same 4,692 rows,
rank 137, and nullity zero.  Therefore neither the phase map nor its
Hadamard-conjugate has a nonzero subset mask.  Coordinate symmetries only
permute mask entries, so combining one with a pair-preserving or pair-swapping
permutation does not evade the obstruction.

## What this closes—and what it does not

The positive and negative results now fit together:

\[
\text{exact QR/NQR duality}
\Longrightarrow
\overline H,
\qquad
\text{orthogonal }68+68+1\text{ split}
\Longrightarrow
\text{no simple }\overline S.
\]

This is useful engineering information: the affine fold-transversal layer
supplies a protected logical basis exchange, but a full logical Clifford gate
set requires a genuinely new resource.

The theorem does **not** rule out:

- general nonuniform Clifford circuits;
- entangling gates between physical qubits;
- ancillas, measurement, feed-forward, or teleportation;
- gauge fixing or code deformation; or
- a different CSS presentation of an equivalent code.

It rules out only the precisely named simple lift class, and it does so by rank
certificates rather than search exhaustion.

## Reproduce

```bash
gap -q analysis/w33_pass361_alpha_code_clifford_maximality.g
python3 -m pytest -q tests/test_pass358_359_gap_github_integrity_alpha_code.py -k pass361
```

Expected GAP summary:

```text
Pass361 status=PASS checks=23 output=data/w33_pass361_alpha_code_clifford_maximality.json
```
