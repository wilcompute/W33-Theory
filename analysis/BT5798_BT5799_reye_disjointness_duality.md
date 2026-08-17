# Passes 5798–5799 — the outer twist is a full Reye incidence dualization

Passes 5792–5797 identified the q=5 centerless Latin carrier with the affine left/right matrix group

\[
G_{576}=M_2(\mathbb F_2)_+:\bigl(GL_2(2)\times GL_2(2)\bigr)
\]

and showed that matrix transpose realizes the point/heavy outer factor swap.  The same coordinates now give a stronger object-level theorem.

## Pass 5798 — heavy/line disjointness is a second Reye configuration

Write a Reye line as the graph of a linear map

\[
L_M=\{(w,Mw):0\ne w\in W\},
\qquad M\in\operatorname{Hom}(W,V),
\]

and a heavy block as

\[
H_{\phi,\psi}=\{(w,x):\phi(x)+\psi(w)=1\}.
\]

Restricting the heavy equation to `L_M` gives

\[
\phi(Mw)+\psi(w)=(\phi M+\psi)(w).
\]

Over `W=F_2^2`, a nonzero linear functional takes value one on exactly two of the three nonzero vectors, while the zero functional never does.  Therefore

\[
\boxed{
|L_M\cap H_{\phi,\psi}|=
\begin{cases}
0,&\psi=\phi M,\\
2,&\psi\ne\phi M.
\end{cases}}
\]

The complete `16*12=192` intersection census is

\[
\boxed{0^{48}\oplus2^{144}}.
\]

Define a new incidence matrix `D` by disjointness:

\[
D_{M,(\phi,\psi)}=1
\iff L_M\cap H_{\phi,\psi}=\varnothing.
\]

For each `M` there are three nonzero `\phi`, hence exactly three incident heavy blocks.  For fixed `(\phi,\psi)`, the equation `\phi M=\psi` has four solutions `M`, hence each heavy block is incident with four lines.  Thus

\[
\boxed{D\text{ is a }12_4,16_3\text{ configuration}.}
\]

More strongly, it is exactly a second Reye copy.  Under the point/heavy factor swap

\[
F(w,x)=(w^T,x^T)
\]

and line transpose

\[
M\mapsto M^T,
\]

the original incidence

\[
x=Mw
\]

becomes

\[
x^T=w^TM^T,
\]

which is precisely the disjointness criterion `\psi=\phi M^T`.  In matrix form,

\[
\boxed{
D[M,h]=R[F^{-1}(h),M^T].
}
\]

So transpose carries the original point–line Reye configuration to a heavy–line Reye configuration on the same 16-line family.  The Pass5674 outer involution is therefore a complete incidence dualization, not merely a permutation-character equivalence.

## Pass 5799 — the disjointness Reye matrix is the signed W9 cross-transform

Let

\[
C_R=4R-J_{12\times16},
\qquad
C_H=2H-J_{12}
\]

be integer centerings of the point–line and point–heavy incidence matrices.  Their row Gram matrices both encode the common projector of Pass 5776.

The new cross matrix is

\[
\boxed{
B=\frac14 C_R^TC_H.
}
\]

Every entry of `B` is `1` or `-3`, and the exact identity is

\[
\boxed{
B=J_{16\times12}-4D.
}
\]

Thus the second Reye incidence is not an auxiliary object: it is literally the signed cross-transform between the line and heavy realizations of the common 9-space.

The verifier proves

\[
\boxed{\operatorname{rank}B=9},
\]

\[
\boxed{BB^T=C_R^TC_R},
\qquad
\boxed{B^TB=4C_H^TC_H},
\]

and

\[
(C_R^TC_R)^2=64(C_R^TC_R),
\qquad
(C_H^TC_H)^2=16(C_H^TC_H).
\]

Hence

\[
\boxed{U=\frac18B}
\]

is a rank-nine partial isometry satisfying

\[
\boxed{
UU^T=E_{W_9,L},
\qquad
U^TU=E_{W_9,H}.
}
\]

This is the canonical linear operator that the earlier character-overlap results were missing: it identifies the heavy and line copies of the common irreducible `W_9` exactly.

## Boundary

Everything here is finite incidence geometry and rational linear algebra.  It strengthens the internal q=5 Reye/Latin duality but does not identify the construction with a quantum system, spacetime, gauge dynamics, or particle phenomenology.
