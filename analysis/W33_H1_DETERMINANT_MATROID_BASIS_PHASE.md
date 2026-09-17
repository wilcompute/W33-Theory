# Determinant magic is a mod-3 matroid basis invariant

## Status

**Exact finite theorem.** This note strengthens the current
`w33_h1_det_two_weight2_witness.py` result. It does **not** promote the
candidate determinant phase to a physical VOA gate; that OPE/addressability
boundary remains open.

## The identity

Let

\[
V=[v_1\;\cdots\;v_m]\in\mathbb F_3^{4\times m},
\qquad
S=VV^T=\sum_i v_i v_i^T,
\qquad
X=SJ,
\]

with \(J\) the standard symplectic form. Cauchy--Binet gives

\[
\det(VV^T)=
\sum_{\substack{I\subseteq[m]\\|I|=4}}\det(V_I)^2.
\]

Over \(\mathbb F_3\), a nonzero determinant is \(\pm1\), hence its square is
\(1\). Therefore

\[
\boxed{
\det X=
\#\{I:|I|=4,\;V_I\text{ is a basis}\}\pmod 3.
}
\]

The set on the right is the set of bases of the represented column matroid
\(M(V)\). Since \(T_M(1,1)\) counts matroid bases,

\[
\boxed{\det X=T_{M(V)}(1,1)\pmod3.}
\]

Thus the candidate synchronized-sector phase becomes

\[
\boxed{\omega^{r\det X}=\omega^{\,rT_M(1,1)}}
\]

with the exponent reduced mod \(3\).

This also gives a deletion--contraction recursion for the phase exponent: for
an ordinary matroid element \(e\),

\[
b(M)=b(M\setminus e)+b(M/e)\pmod3.
\]

## Minimal four-direction theorem

With fewer than four Pauli directions, \(S\) has rank at most three and
\(\det X=0\).

With exactly four projective directions,

\[
\boxed{
\det X\ne0
\iff
\{v_1,v_2,v_3,v_4\}\text{ spans }\mathbb F_3^4,
}
\]

and whenever they span,

\[
\boxed{\det X=1.}
\]

So the latest \((e_1,e_2,e_3)+(e_4,0,0)\) witness is not exceptional:
**every projective basis is a determinant-magic witness at the finite
equivariant level.**

## Exhaustive \(PG(3,3)\) census

The verifier exhausts all four- and five-subsets of the 40 projective points.

Four-subsets:

\[
\binom{40}{4}=91\,390,
\]

split as

\[
\boxed{63\,180\text{ bases}+28\,210\text{ dependent quadruples}.}
\]

The basis count has the closed form

\[
63\,180=\frac{|GL(4,3)|}{2^4\,4!}.
\]

Five-subsets:

\[
\binom{40}{5}=658\,008.
\]

Their numbers of rank-four bases are distributed as

\[
\boxed{
0^{51\,480},\quad
3^{252\,720},\quad
4^{252\,720},\quad
5^{101\,088}.
}
\]

Therefore the determinant distribution is

\[
\boxed{
0^{304\,200},\quad
1^{252\,720},\quad
2^{101\,088}.
}
\]

Every subset satisfies

\[
\det((VV^T)J)=\#\mathrm{bases}(M(V))\pmod3.
\]

## Why this is useful

The quartic determinant is now a coordinate-free combinatorial observable of
the Pauli support. The matrix formula, the projective geometry, and matroid
deletion--contraction are three descriptions of the same finite quantity.
This supplies a recursive compiler for the **candidate** phase exponent and a
clear falsification target for any proposed VOA realization.

It also separates this result from the repository's earlier Cauchy--Binet
apartment-volume theorems (Passes 5444/5449): those sum real/integer cycle
lattice volumes, whereas this theorem is the rank-four column-matroid basis
count in \(\mathbb F_3^4\).

## External mathematical anchors

- Cauchy--Binet is the determinant identity used in the proof.
- The standard Tutte evaluation \(T_M(1,1)=\#\{\text{bases of }M\}\) is
  documented, for example, by the Encyclopedia of Mathematics:
  https://encyclopediaofmath.org/wiki/Tutte_polynomial
- A coding/matroid treatment explicitly using the same \(T_M(1,1)\) basis
  evaluation is:
  https://www.mdpi.com/2227-7390/11/12/2774

## Evidence boundary

This proves the finite identity and the exhaustive \(PG(3,3)\) censuses.
It **does not** prove that the actual \(A_8^3\) two-operator OPE coefficient
is \(\omega^{r\det X}\), nor that a physical controller can independently
address it. Those remain the next dynamical/VOA questions.
