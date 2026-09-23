# 2026-09-23 — Full Hesse affine spinor-parity character

The determinant/spinor-norm identity now extends over the entire Hesse affine
group.

Write an affine symmetry as

\[
x\longmapsto gx+t,
\qquad
t\in\mathbb F_3^2,\quad g\in GL(2,3).
\]

Define

\[
\boxed{
\chi(t,g)
=
\det(g)
=
\theta_{\rm spin}(\rho(g))
\in\mathbb F_3^\times/(\mathbb F_3^\times)^2
\cong C_2.
}
\]

Exhaustion of all

\[
432^2=186624
\]

ordered products verifies that \(\chi\) is a homomorphism.

Its two fibers have equal size:

\[
\boxed{216+216=432.}
\]

More precisely,

\[
\boxed{
\ker\chi
=
\mathbb F_3^2:SL(2,3)
=
ASL(2,3),
\qquad |\ker\chi|=216.
}
\]

That is exactly the projective one-qutrit Clifford/Hessian group already
certified in the repository. The other 216 elements are the
determinant-minus-one/anti-linear affine coset.

The nine translations are invisible to the character, so the compiler bit is
purely linear:

\[
\chi(t,g)=\chi(0,g).
\]

Under the preceding adjoint lift, all 432 affine elements collapse in fibers
of size

\[
9\cdot2=18
\]

onto the 24-element orthogonal image \(SO(Q)\): nine translations times the
central pair \(\{\pm I_2\}\).

Thus the full finite dictionary is now

\[
\boxed{
AGL(2,3)
\xrightarrow{\ \chi\ }
C_2,
\qquad
\ker\chi=ASL(2,3),
}
\]

with

\[
\chi
=
\det_{\mathbb F_3^2}
=
\text{spinor norm on }SO(Q).
\]

For the anti-linear generator

\[
\kappa=\operatorname{diag}(-1,1),
\]

\[
\chi(\kappa)=-1.
\]

This gives the factor-two Hessian extension a canonical group-theoretic parity
bit.

## Important 1296 boundary

The repo also has:

- a nonsplit central \(C_3\) lift of \(ASL(2,3)\), order \(648\);
- an extended-with-center count \(1296\);
- several other exact \(1296\)-stabilizer/carrier constructions.

Those are **not** identified here by cardinality. A concrete central-extension
intertwiner is still required before promoting the affine spinor bit to one
particular 1296 permutation group.

## Evidence boundary

This is a finite compiler/group character. “Spinor parity” means the pullback
of the finite orthogonal spinor norm. It is not physical spatial parity,
fermion parity, CPT, or a continuum \(Pin/Spin\) structure.

Evidence:

- analysis/w33_hesse_affine_spinor_parity.py
- data/w33_hesse_affine_spinor_parity.json
- tests/test_w33_hesse_affine_spinor_parity.py
