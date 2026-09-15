# Pass 2026-09-15 — the E8 twisted register is the Pass-1021 root quotient

## Result

Two constructions that were previously only known to land on isomorphic copies of \(W(3,3)\) are in fact the **same quotient map on the \(E_8\) roots**.

Let \(c\) be the canonical Coxeter element used in Pass 1021 and let

\[
g=c^{10},\qquad |g|=3.
\]

Pass 1021 proved that the 240 roots of \(E_8\) split into forty six-root fibres under

\[
\langle c^5\rangle=\langle -1,g\rangle\cong C_6,
\]

and that this 40-set is the \(W(3,3)\) point action of \(PSp(4,3)\).

Holotrade commit `68df33f` independently identified the \(g\)-twisted ground-state register of the lattice VOA with the Heisenberg representation of \(E_8/(1-g)E_8\), with the twisted commutator geometry \(W(3,3)\).

The new certificate `analysis/w33_e8_twisted_fibration_weld.py` proves that these are not two parallel realizations. They coincide root-by-root.

## Exact quotient

Using the same simple roots and Coxeter convention as Pass 1021,

\[
\det(1-g)=81
\]

and

\[
\operatorname{SNF}(1-g)
=
\operatorname{diag}(1,1,1,1,3,3,3,3).
\]

Therefore

\[
E_8/(1-g)E_8\cong \mathbb F_3^4.
\]

The 240 roots occupy **all 80 nonzero vectors** of this quotient, with exactly three roots per vector. For every root \(r\), its quotient fibre is exactly

\[
\{r,gr,g^2r\}.
\]

This is forced algebraically by \(gr-r\in(1-g)E_8\), and the certificate verifies that the 80 resulting root cosets are distinct and exhaust every nonzero quotient vector.

Projectivizing the four-dimensional ternary quotient identifies \(v\sim -v\). Hence the 80 nonzero vectors become 40 projective points, and the root fibre over one projective point is

\[
\{\pm r,\pm gr,\pm g^2r\}.
\]

But \(g=c^{10}=(c^5)^2\) and \(-1=c^{15}=(c^5)^3\), so this is exactly the Pass-1021 orbit under \(\langle c^5\rangle\cong C_6\). Thus the old root fibration and the new twisted-register quotient are literally identical.

## Twisted commutator form

For the order-three twist, using the commutator-exponent convention already certified in Holotrade `68df33f` from Bakalov--Kac, arXiv:math/0402315, Eq. (4.43),

\[
\Omega(a,b)
=
\sum_{k=1}^{2} k\,\langle g^k a,b\rangle
\pmod 3 .
\]

The exact calculation finds:

- \(\Omega\) is alternating modulo 3;
- its rank on \(E_8/3E_8\) is 4;
- \((1-g)E_8\bmod 3\) is exactly its radical;
- therefore the induced form on \(E_8/(1-g)E_8\cong\mathbb F_3^4\) is nondegenerate symplectic;
- projective orthogonality has parameters
  \[
  \operatorname{srg}(40,12,2,4).
  \]

Thus the 40 quotient points carry the symplectic polar space \(W(3,3)\) intrinsically.

## Pauli dictionary sharpened

The finite dictionary is now exact:

\[
240\ E_8\text{ roots}
\longrightarrow
80\ \text{nonidentity two-qutrit Pauli labels}
\longrightarrow
40\ W(3,3)\text{ projective Pauli points},
\]

with fibre sizes \(3\) and \(6\), respectively.

The first quotient is by the order-three Coxeter twist orbit. The second is projectivization \(v\sim -v\), i.e. identifying the two nonzero elements of each one-dimensional \(\mathbb F_3\)-subspace.

This is stronger than a count match or an abstract graph isomorphism: it identifies the exact map used by the \(E_8\) root shell with the exact phase-space quotient carried by the twisted ground-state Heisenberg register.

## Prior ownership and literature boundary

This pass does **not** reclaim:

- Pass 1021's \(240=40\times 6\) Coxeter/Eisenstein fibration and \(PSp(4,3)\) point action;
- Holotrade `68df33f`'s twisted-register construction and identification of its commutator geometry with \(W(3,3)\);
- the classical theory of twisted lattice-VOA modules and their Heisenberg commutators.

The new corpus contribution is the exact equality of the two previously separate quotient maps.

Bakalov and Kac classify twisted modules for lattice vertex algebras and give the relevant group commutator formula in Eq. (4.43) of arXiv:math/0402315. Their result supplies the classical twisted-module framework; the finite root-fibre weld above is the new computation here.

## Reproduction

Run:

```text
python analysis/w33_e8_twisted_fibration_weld.py
```

The script writes `data/w33_e8_twisted_fibration_weld.json`. The certificate has 16 exact checks and returns `PASS`.

## Scope

This is an exact finite lattice / symplectic-geometry / twisted-register theorem. It strengthens the internal mathematical architecture of the TOE program. It does not by itself establish a physical theory, a continuum limit, or experimental predictions.
