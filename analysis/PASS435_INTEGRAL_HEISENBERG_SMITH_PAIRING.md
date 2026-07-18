# Pass 435 — Integral Heisenberg Smith pairing theorem

## Theorem

Let \(q=p^f\) be an odd prime power, let \(H_q\) be the three-dimensional Heisenberg group over \(\mathbb F_q\), and let \(L_q\) be the Laplacian of the native bulk Cayley graph with connection set

\[
S=\{(u,v,0):(u,v)\neq(0,0)\}.
\]

Write

\[
m_+=\frac{q(q^2-1)}2,
\qquad
m_-=\frac{q(q-1)^2}2.
\]

For every odd prime \(\ell\neq p\),

\[
\boxed{
K(L_q)_{(\ell)}\cong
(\mathbb Z/\ell^{\nu_\ell(q-1)})^{m_+}
\oplus
(\mathbb Z/\ell^{\nu_\ell(q+1)})^{m_-}
}
\]

with factors of exponent zero omitted. For \(\ell=2\),

\[
\boxed{
K(L_q)_{(2)}\cong
(\mathbb Z/2^{\nu_2(q-1)})^{q(q-1)}
\oplus
(\mathbb Z/2^{\nu_2(q^2-1)})^{m_-}.
}
\]

Thus Pass 434's five-field law holds for every odd prime power.

## Central Fourier reduction

Fourier transform in the center is unimodular at every prime \(\ell\neq p\), because its determinant is a power of \(q\). The central-trivial block contributes only \(q^2\), hence contributes no \(\ell\)-torsion.

For a nontrivial central character \(t\), identify functions on \(\mathbb F_q^2\) with a free module of rank \(q^2\). The symplectic Fourier matrix is

\[
(F_t f)(x)=\sum_{y\in\mathbb F_q^2}\psi_t(\omega(y,x))f(y),
\qquad F_t^2=q^2I.
\]

The corresponding Laplacian block is

\[
B_t=q^2I-F_t.
\]

Its rational eigenvalues are \(q(q-1)\) and \(q(q+1)\). The multiplicities per nontrivial central character are

\[
r_+=\frac{q(q+1)}2,
\qquad
r_-=\frac{q(q-1)}2.
\]

Multiplying by the \(q-1\) nontrivial central characters gives \(m_+\) and \(m_-\).

## Odd primes \(\ell\neq p\)

When \(\ell\) is odd, \(2\) is a unit. Therefore the projectors

\[
P_\pm=\frac12\left(I\pm q^{-1}F_t\right)
\]

are integral over the unramified extension containing the character values. Hence the two eigenspaces split integrally. The elementary divisors are exactly those of \(q(q-1)\) on the \(+q\) sector and \(q(q+1)\) on the \(-q\) sector. Since \(q\) is an \(\ell\)-unit, this gives the stated odd-prime formula. Faithful flatness of the unramified extension descends the elementary divisors to \(\mathbb Z_\ell\).

## The exceptional prime \(2\)

Set

\[
N=qI-F_t.
\]

Then

\[
N^2=2qN
\]

and

\[
B_t=q(q-1)I+N.
\]

The missing datum is the integral rank of \(N\) modulo two.

### Transpose lemma

Let \(H=(\psi_t(ab))_{a,b\in\mathbb F_q}\) be the one-dimensional Fourier matrix. It is symmetric and invertible over the unramified 2-adic character ring. Under the matrix identification \(f(a,b)\leftrightarrow X\), the symplectic Fourier transform is equivalent modulo two to

\[
X\longmapsto A X^T A^{-1}
\]

for a symmetric invertible matrix \(A\). Its fixed-point equation becomes, after writing \(X=AY\),

\[
Y=Y^T.
\]

Therefore the fixed space has dimension

\[
\frac{q(q+1)}2,
\]

and

\[
\operatorname{rank}_{\mathbb F_2}(N)=
q^2-\frac{q(q+1)}2=rac{q(q-1)}2=r_-.
\]

Consequently the image and coimage lattices of \(N\) are primitive. There is a rank factorization

\[
N=UV,
\qquad
VU=2qI_{r_-},
\]

with both \(U\) and \(V\) primitive. Since \(2q\equiv0\pmod2\) and \(V\) remains surjective modulo two, compatible integral bases put \(N\) into the form

\[
N\sim
\begin{pmatrix}
2qI_{r_-}&I_{r_-}&0\\
0&0&0\\
0&0&0
\end{pmatrix},
\]

where the final block has size

\[
q^2-2r_-=q.
\]

Thus \(B_t\) is a direct sum of \(r_-\) paired blocks

\[
\begin{pmatrix}
q(q+1)&1\\
0&q(q-1)
\end{pmatrix}
\]

and \(q\) residual scalar blocks \(q(q-1)\).

Each paired block has a unit entry, so its Smith form is

\[
\operatorname{diag}\left(1,q^2(q^2-1)\right).
\]

At the prime two, \(q^2\) is a unit. Hence every paired block contributes one factor of valuation \(\nu_2(q^2-1)\), while every residual block contributes one factor of valuation \(\nu_2(q-1)\). Multiplying by \(q-1\) nontrivial central characters yields

\[
q(q-1)
\]

residual factors and

\[
(q-1)r_-=\frac{q(q-1)^2}{2}
\]

paired factors, proving the theorem.

## Consequence

Pass 435 completes the entire prime-to-characteristic part of the critical group for every odd prime power. Pass 425 supplies the characteristic-primary part through projective monomial types and affine-chart gluing. Their combination is executed in Pass 437.

## Claim boundary

The theorem concerns the native Heisenberg bulk graph. It does not claim that arbitrary Cayley sections, residue-ring analogues, or switched graphs share the same integral lattice. Pass 438 shows explicitly that \(\mathbb Z/p^2\mathbb Z\) has additional conductor strata and a different Smith profile.
