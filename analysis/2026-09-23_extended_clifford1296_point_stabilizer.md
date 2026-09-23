# 2026-09-23 — The full W33 point stabilizer is the 1296 extended qutrit Clifford

## Result

The previously open \(648\to1296\) central-lift boundary is now closed on the
correct side of the \(W(3,3)\) geometry.

Starting from the native \(\mathbb F_3^4\) symplectic model, adjoining the
explicit multiplier-\(2\) similitude

\[
D=\operatorname{diag}(2,1,2,1)
\]

to \(PSp(4,3)\) gives the full projective similitude group:

\[
|PSp(4,3)|=25920,
\qquad
|PGSp(4,3)|=51840.
\]

The stabilizer of the selected W33 point has orders

\[
648
\quad\text{inside }PSp(4,3),
\]

and

\[
1296
\quad\text{inside }PGSp(4,3).
\]

The \(648\)-group is the already certified physical one-qutrit Clifford
stabilizer. The new verifier reconstructs its extraspecial normal Heisenberg
group

\[
H_{27}\cong 3_+^{1+2}
\]

and then finds an explicit \(GL(2,3)\) complement of order \(48\) in the full
point stabilizer.

Every one of the \(1296\) elements has a unique normal form

\[
n\ell,
\qquad
n\in H_{27},
\quad
\ell\in GL(2,3).
\]

Therefore

\[
\boxed{
G_{\rm ext}
\cong
3_+^{1+2}:GL(2,3),
\qquad
|G_{\rm ext}|=1296.
}
\]

Its even subgroup is

\[
\boxed{
G_{\rm Cliff}
\cong
3_+^{1+2}:SL(2,3),
\qquad
|G_{\rm Cliff}|=648.
}
\]

## The phase \(C_3\) changes status under anti-linear completion

Let

\[
Z(H_{27})=\langle z\rangle\cong C_3.
\]

In the \(648\)-element Clifford group, this \(C_3\) is central. In the full
\(1296\)-element extension it is still normal, but determinant-\(-1\) elements
act by

\[
\boxed{z\mapsto z^2=z^{-1}.}
\]

Hence

\[
\boxed{Z(G_{\rm ext})=1.}
\]

So the earlier phrase “extended with \(C_3\) center” must be read only as a
counting shorthand. The anti-linear completion does **not** retain that
\(C_3\) as the center of the full group.

This is exactly what the Heisenberg commutator predicts: a general
\(g\in GL(2,3)\) rescales the two-dimensional symplectic form by
\(\det g\), and the central Heisenberg commutator scales by the same factor.

## Exact quotient

Quotienting by the normal phase \(C_3\) gives

\[
\boxed{
G_{\rm ext}/C_3
\cong
AGL(2,3),
\qquad |AGL(2,3)|=432.
}
\]

The verifier does not infer this from order. It constructs the induced
nine-point phase-space action and compares all \(432\) permutations against
the explicit affine group; the sets are identical.

Similarly,

\[
\boxed{
G_{\rm Cliff}/C_3
\cong
ASL(2,3),
\qquad |ASL(2,3)|=216.
}
\]

Thus the full tower is now executable:

\[
\begin{array}{ccccc}
3_+^{1+2}:SL(2,3) &\triangleleft&
3_+^{1+2}:GL(2,3)\\
648 && 1296\\[2mm]
\downarrow /C_3 && \downarrow /C_3\\[2mm]
ASL(2,3) &\triangleleft& AGL(2,3)\\
216 && 432.
\end{array}
\]

## Spinor-parity lift

The determinant/spinor character from the previous theorem lifts through the
Heisenberg phase extension:

\[
\boxed{
\chi(n,g)=\det(g)
=\theta_{\rm spin}(\rho(g)).
}
\]

Its two fibers have sizes

\[
648+648=1296,
\]

and

\[
\boxed{\ker\chi=G_{\rm Cliff}.}
\]

So the same finite \(C_2\) bit separates unitary and anti-linear operations at
all three levels:

\[
216\subset432,
\qquad
648\subset1296,
\qquad
A_4\subset S_4.
\]

## Side selection matters

The repo already proved that \(PSp(4,3)\) has two nonconjugate order-\(648\)
stabilizer classes:

- point/Hessian side: extraspecial \(3_+^{1+2}\);
- line/dual side: elementary-abelian \(3^3\).

The present theorem uses the **point/Hessian side** selected by the physical
qutrit Clifford certificate. It does not identify the nonconjugate line-side
\(1296\) carrier with the extended qutrit Clifford.

## Evidence boundary

This closes a finite group-theoretic compiler boundary. The \(C_2\) character
is still not physical CPT, continuum spacetime parity, a Lorentz \(Pin/Spin\)
bundle, or a derivation of particle chirality.

Executable evidence:

- analysis/w33_extended_clifford1296_point_stabilizer.py
- data/w33_extended_clifford1296_point_stabilizer.json
- tests/test_w33_extended_clifford1296_point_stabilizer.py
