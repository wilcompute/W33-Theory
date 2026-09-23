# 2026-09-23 — Determinant / spinor-norm weld for the Hesse null cone

## Breakthrough

The explicit adjoint lift from the preceding pass exposed an apparent mismatch:

\[
\det g=-1
\]

for the anti-linear qutrit phase-space reflection, but

\[
\det \rho(g)=+1
\]

in the three-dimensional hull orthogonal module.

That is not a contradiction. The missing index-two invariant of \(SO(Q)\) is
the **spinor norm**.

For the hull Gram matrix

\[
Q=
\begin{pmatrix}
0&1&1\\
1&0&1\\
1&1&0
\end{pmatrix}
\]

define

\[
q(v)=\frac12 v^TQv
\]

over \(\mathbb F_3\), where \(1/2=2\). For a nonsingular vector \(v\),
the orthogonal reflection \(r_v\) has spinor square-class \(q(v)\).
The verifier enumerates all nine projective reflections and all 24 elements of
\(SO(Q)\). Every special-orthogonal element is expressed as a product of two
reflections; every such decomposition gives the same square-class.

The exact weld is

\[
\boxed{
\theta_{\rm spin}(\rho(g))
=
\det(g)
\pmod{(\mathbb F_3^\times)^2}
}
\]

for all 48 \(g\in GL(2,3)\).

Therefore

\[
\boxed{
\rho(SL(2,3))
=
\Omega(Q)
\cong PSL(2,3)
\cong A_4
}
\]

and

\[
\boxed{
\rho(GL(2,3))
=
SO(Q)
\cong PGL(2,3)
\cong S_4.
}
\]

The unitary/Hessian \(A_4\) layer is the spinor-norm kernel, while the
anti-linear completion occupies the nontrivial spinor-norm coset.

## Anti-linear reflection

For

\[
\kappa=
\begin{pmatrix}
2&0\\
0&1
\end{pmatrix},
\qquad \det\kappa=2=-1,
\]

the adjoint lift is

\[
\rho(\kappa)=
\begin{pmatrix}
2&0&1\\
0&2&1\\
0&0&1
\end{pmatrix},
\qquad
\det\rho(\kappa)=1.
\]

Yet it has nontrivial spinor norm. One explicit factorization is

\[
\rho(\kappa)
=
r_{(1,1,0)}\,r_{(1,2,0)}
\]

with

\[
q(1,1,0)=1,\qquad q(1,2,0)=2,
\]

hence

\[
\theta_{\rm spin}(\rho(\kappa))=2.
\]

So the corrected finite dictionary is

\[
\boxed{
\text{qutrit determinant character}
\longleftrightarrow
\text{hull spinor-norm character}.
}
\]

This is stronger and cleaner than calling the odd Hesse action an
“orientation reversal.”

## External check

Standard finite-orthogonal-group theory defines \(\Omega_d(q)\), for odd
\(q\), as the kernel of the spinor norm restricted to \(SO_d(q)\).
The project calculation independently reconstructs that kernel and finds the
expected 12-element \(A_4\) subgroup.

## Evidence boundary

The word *spinor* here refers to the standard spinor-norm square-class
invariant of a finite orthogonal group. It does **not** by itself produce
physical fermionic spin, a continuum \(Spin/Pin\) bundle, Lorentz symmetry,
CPT, or spacetime parity.

Executable evidence:

- analysis/w33_hesse_nullcone_spinor_norm.py
- data/w33_hesse_nullcone_spinor_norm.json
- tests/test_w33_hesse_nullcone_spinor_norm.py
