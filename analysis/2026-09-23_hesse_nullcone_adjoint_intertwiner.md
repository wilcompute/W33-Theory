# 2026-09-23 — Explicit adjoint lift of the Hesse / hull null cone

## Result

The preceding anti-linear Clifford–Hessian theorem proved that two actions have
the same permutation image \(S_4\):

1. \(\mathrm{GL}(2,3)\) on the four affine/Hesse direction classes of
   \(\mathbb F_3^2\), and
2. \(SO(Q)\) on the four isotropic projective rays of the new 3-dimensional
   affine-hull quotient.

The new verifier lifts that equality from permutations to an explicit linear
intertwiner.

Write a traceless \(2\times2\) matrix as

\[
X(a,b,c)=
\begin{pmatrix}
a&b\\ c&-a
\end{pmatrix}.
\]

Then

\[
q_{\mathfrak{sl}_2}(a,b,c)
=-\det X
=a^2+bc
\]

has polar Gram matrix

\[
B=
\begin{pmatrix}
2&0&0\\
0&0&1\\
0&1&0
\end{pmatrix}.
\]

For the certified hull form

\[
Q=
\begin{pmatrix}
0&1&1\\
1&0&1\\
1&1&0
\end{pmatrix},
\]

the explicit matrix

\[
P=
\begin{pmatrix}
1&1&0\\
1&0&2\\
2&0&0
\end{pmatrix}
\]

satisfies

\[
\boxed{P^TQP=2B}.
\]

Thus the hull quadratic space is explicitly the determinant quadratic space on
\(\mathfrak{sl}_2(\mathbb F_3)\), up to the harmless nonzero scalar \(2\).

## Exact group lift

For \(g\in GL(2,3)\), define

\[
\boxed{
\rho(g)=P\,\operatorname{Ad}(g^{-T})\,P^{-1}.
}
\]

The inverse transpose is forced by the existing repository convention that the
four Hesse directions are represented as normal covectors.

Exhaustive verification over all \(48\) matrices of \(GL(2,3)\) proves

\[
\rho(g)^TQ\rho(g)=Q,
\qquad
\det\rho(g)=1.
\]

Moreover,

\[
\boxed{
\ker\rho=\{\pm I_2\},
\qquad
\operatorname{im}\rho=SO(Q),
\qquad
|\operatorname{im}\rho|=24.
}
\]

Hence the already-observed projective \(S_4\) is no longer only a coincidence of
permutation sets:

\[
GL(2,3)/\{\pm I\}
\cong
SO(Q)
\cong
PGL(2,3)
\cong
S_4
\]

for this concrete finite module. Restricting to \(SL(2,3)\) gives a
12-element image whose four-ray action is exactly \(A_4\).

## The four rays are the nilpotent cone, point-for-point

The projective nilpotent cone of \(\mathfrak{sl}_2(\mathbb F_3)\) has the
Veronese parametrization

\[
\nu(u,v)=(-uv,u^2,-v^2).
\]

Applying \(P\) reproduces the parent Hesse/null dictionary **without any
relabeling**:

\[
\begin{array}{ccl}
(1,0)&\mapsto&(1,0,0),\\
(0,1)&\mapsto&(0,1,0),\\
(1,1)&\mapsto&(0,0,1),\\
(1,2)&\mapsto&(1,1,1).
\end{array}
\]

This is the strongest part of the bridge: the four Hesse directions are not
merely another four-element \(S_4\)-set. They are the four projective
nilpotent directions of the explicit \(\mathfrak{sl}_2(\mathbb F_3)\)
determinant form that is linearly equivalent to the certified hull form.

## Anti-linear reflection: one important correction of language

For the determinant-minus-one phase-space reflection

\[
\kappa=\operatorname{diag}(-1,1)
=
\begin{pmatrix}2&0\\0&1\end{pmatrix}
\quad(\mathbb F_3),
\]

the lift is

\[
\rho(\kappa)=
\begin{pmatrix}
2&0&1\\
0&2&1\\
0&0&1
\end{pmatrix}.
\]

It induces exactly the parent odd transposition on the four null rays,

\[
(0,1,3,2),
\]

but

\[
\boxed{\det\rho(\kappa)=+1.}
\]

So there are **two different parity notions** in play:

- determinant \(-1\) in the 2D qutrit phase-space action;
- odd permutation parity on the four Hesse/null directions.

After the adjoint lift, the latter lives inside \(SO(Q)\). Therefore an odd
four-ray permutation is *not* a determinant-\(-1\) transformation of the
3D quadratic module. This sharpens the previous “orientation reversal”
language and prevents a false Lorentz/parity inference.

## Literature anchor

Artebani–Dolgachev, *The Hesse pencil of plane cubic curves*, Proposition 4.1,
identifies the Hessian group \(G_{216}\) with
\(\mathbb F_3^2\!:\!SL(2,3)\), as the determinant-one index-two subgroup of
the affine group of order \(432\), and records the \(A_4\) action on the four
singular members. The new contribution here is not that classical group
identification; it is the explicit basis-level weld to the repository's
independently derived affine-hull quadratic quotient.

## Parallel E8 real-form boundary

A parallel commit that landed during this pass independently identifies the exact
anti-linear involution of the 248-dimensional compiler as a real structure with
fixed form \(E_{8(8)}\), via Killing inertia \((128,120)\). That is a
characteristic-zero Lie-algebra result. The present \(\mathbb F_3\) adjoint/null-cone
intertwiner is logically separate: no map from this three-dimensional finite
quadratic module to the real \(E_{8(8)}\) geometry is asserted.

## Evidence boundary

This is a theorem of finite quadratic geometry over \(\mathbb F_3\). It gives
an exact adjoint lift and a concrete nilpotent-cone dictionary. It does **not**
identify the finite quadratic space with Lorentzian spacetime, prove a
continuum spin structure, derive \(Spin(3,1)\), CPT, measured CP violation, or
a spacetime metric.

Executable evidence:

- analysis/w33_hesse_nullcone_adjoint_intertwiner.py
- data/w33_hesse_nullcone_adjoint_intertwiner.json
- tests/test_w33_hesse_nullcone_adjoint_intertwiner.py
