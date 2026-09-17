# The 1,620 W33 apartments are determinant-one Pauli bases

## Theorem

Let \(p_1,p_2,p_3,p_4\) be the four point vertices of an induced W33
quadrangle/apartment, cyclically ordered as

\[
p_1-p_2-p_3-p_4-p_1.
\]

Write \(V=[p_1\ p_2\ p_3\ p_4]\) in projective representatives over
\(\mathbb F_3\), and let \(J\) be the standard symplectic form. Then

\[
\boxed{\det V\neq0}
\]

and

\[
\boxed{\det((VV^T)J)=1.}
\]

There are exactly

\[
\boxed{1620}
\]

such induced quadrangles, and each lifts uniquely to one alternating point-line
8-cycle in the W33 Levi graph.

Therefore the current determinant/Tutte candidate phase is uniform on the
entire apartment set:

\[
\boxed{\omega^{r\det((VV^T)J)}=\omega^r}
\]

for synchronized central character \(r=1,2\).

## Direct proof

Adjacent apartment points are collinear in W33 and hence symplectically
orthogonal:

\[
\langle p_i,p_{i+1}\rangle=0.
\]

Because the quadrangle is induced, its two opposite pairs are noncollinear, so

\[
a=\langle p_1,p_3\rangle\neq0,
\qquad
b=\langle p_2,p_4\rangle\neq0.
\]

In the cyclic basis, the alternating Gram matrix \(V^TJV\) has only those two
opposite pairings. Hence

\[
\det(V^TJV)=(ab)^2.
\]

Every nonzero element of \(\mathbb F_3\) has square \(1\), so

\[
\det(V^TJV)=1.
\]

Thus \(V\) is invertible. Since \(\det J=1\),

\[
\det((VV^T)J)=\det(V)^2\det J=1.
\]

This is the apartment-specialized form of the more general matroid identity

\[
\det((VV^T)J)=T_{M(V)}(1,1)\pmod3.
\]

## Exhaustive verifier

`analysis/w33_h1_det_apartment_phase_bridge.py` reconstructs:

- all 40 projective points of \(PG(3,3)\);
- the W33 point graph with degree 12 and 240 edges;
- all 40 totally isotropic GQ lines;
- all 1,620 **induced** point \(C_4\) apartments;
- the unique four GQ lines attached to each apartment;
- all 1,620 corresponding Levi 8-cycle lifts.

Every apartment passes both the direct symplectic-Gram test and the
matroid/determinant test.

## Semantic firewall

Pass 4474 already established that W33 has two different relevant simple
four-cycle populations:

\[
1740=1620+120,
\]

where 1,620 are induced quadrangle/apartments and 120 lie inside the forty
geometric \(K_4\) lines. This theorem concerns **only the 1,620 induced
apartments**. It does not rename the 120 line-internal cycles.

## Why this bridge matters

The newest determinant work began in the ten-dimensional \(H_1\cong
\mathfrak{sp}_4(\mathbb F_3)\) controller and, at first, only supplied a
four-direction witness. The matroid theorem makes that witness coordinate-free;
the present theorem then identifies a canonical W33 family on which the
invariant is forced to be nonzero: the full building-apartment family.

So three previously separate objects now agree on one exact finite carrier:

\[
\boxed{
\text{W33 induced quadrangle}
\;\longleftrightarrow\;
\text{Levi 8-cycle apartment}
\;\longleftrightarrow\;
\text{rank-4 Pauli matroid basis with det}=1.
}
\]

That is a finite theorem, not yet a dynamical one.

## Evidence boundary

This does **not** prove that the \(A_8^3\) VOA OPE realizes the phase
\(\omega^{r\det X}\), nor that a Holonet controller can address one apartment
phase independently. It supplies the exact geometric support on which such a
coupling would have to act if the determinant proposal is physical.
