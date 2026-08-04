# Passes 3262–3265 — Exact-cover signature \(S_3\) Fourier and five-bit affine-lift theorem

## Status

**Exact finite theorem.** The verifier is self-contained, uses integer/binary arithmetic only, and passes all six frozen checks.

## Input from the complete cover census

The complete nonlinear exact-cover signature classification supplies 45 anchor octets. Relative to the unique anchor, the three independent four-cells of the induced \(K_{4,4,4}\) carry one of four unordered patterns:

\[
(2,2,2),\qquad(0,3,3),\qquad(1,2,3),\qquad(0,2,4).
\]

Permuting the three cells gives orbit sizes

\[
1,\qquad3,\qquad6,\qquad6.
\]

Thus the local signature alphabet is the sixteen-state \(S_3\)-set

\[
\Omega\cong 1\;\sqcup\;S_3/C_2\;\sqcup\;S_3\;\sqcup\;S_3,
\qquad |\Omega|=16,
\]

and the global census count is

\[
45\cdot16=720.
\]

This imports only the already-frozen cell patterns and anchor count. Everything below is recomputed independently.

## Pass 3262 — exact \(S_3\) Fourier decomposition

The permutation character of \(\Omega\), on the identity, transposition and three-cycle classes, is

\[
\boxed{\chi_\Omega=(16,2,1).}
\]

Indeed, the identity fixes all sixteen states, a transposition fixes the constant state and one state in the three-point orbit, and a three-cycle fixes only the constant state.

Taking inner products with the rational irreducible characters of \(S_3\) gives

\[
\boxed{
\mathbb Q[\Omega]
\cong
4\,\mathbf 1
\oplus
2\,\mathrm{sgn}
\oplus
5\,V_{\mathrm{std}}.
}
\]

The local signature algebra therefore contains four invariant scalar channels, two sign channels and five standard Fourier doublets. This refines the newest port result that the sign bit alone is only the Abelian shadow of the full non-Abelian \(S_3\) connection.

## Pass 3263 — the rank-45 coherent algebra

Burnside/Schur gives

\[
\dim_{\mathbb Q}\operatorname{End}_{S_3}(\mathbb Q[\Omega])
=4^2+2^2+5^2
=\boxed{45}.
\]

The verifier also constructs the orbitals directly. The diagonal action of \(S_3\) on \(\Omega\times\Omega\) has exactly

\[
\boxed{45}
\]

orbits, with size histogram

\[
\boxed{1^1\,3^3\,6^{41}}.
\]

Hence the exact rank-degree identity is

\[
\boxed{
720
=45\cdot16
=\dim\operatorname{End}_{S_3}(\mathbb Q[\Omega])\,|\Omega|.
}
\]

The corresponding rational commutant has Wedderburn form

\[
\boxed{
M_4(\mathbb Q)\oplus M_2(\mathbb Q)\oplus M_5(\mathbb Q).
}
\]

**Boundary.** The equality between the 45 anchor octets and the 45 local orbitals does not by itself produce a canonical bijection. It is an exact equality of two independently constructed ranks, not an asserted object-level identification.

## Pass 3264 — four-bit affine no-go

Set-theoretically, sixteen states require only four bits. The natural next question is stronger:

> Can the exact cell-permutation \(S_3\)-action be implemented by affine transformations of \(\mathbb F_2^4\)?

The answer is no.

The local signature action has a unique fixed state, \((2,2,2)\). Any affine realization with a fixed point is translation-conjugate to a linear realization. The verifier therefore enumerates all

\[
|GL(4,2)|=20160
\]

invertible binary matrices and all

\[
\boxed{2800}
\]

embedded \(S_3\) subgroups. Their orbit profiles on \(\mathbb F_2^4\) are exactly

\[
(1,1,2,3,3,6)^{1680},
\]

\[
(1,1,1,1,3,3,3,3)^{560},
\]

and

\[
(1,3,3,3,6)^{560}.
\]

The required profile

\[
\boxed{(1,3,6,6)}
\]

never occurs. Therefore:

\[
\boxed{
\text{No four-bit affine }\mathbb F_2\text{ register realizes the exact signature }S_3\text{-action.}
}
\]

A four-bit controller is still possible with nonlinear lookup/permutation logic. The no-go concerns affine binary gates only.

## Pass 3265 — explicit minimal five-bit lift

The obstruction is sharp. Take

\[
\mathbb F_2^5
=\mathbb F_2^3_{\mathrm{perm}}
\oplus
\mathbb F_2^2_{\mathrm{std}},
\]

where \(S_3\) permutes the first three coordinates and acts as

\[
GL(2,2)\cong S_3
\]

on the final two coordinates. For generators \(r=(012)\) and \(s=(12)\), one exact row-matrix realization is

\[
R=
\begin{pmatrix}
0&0&1&0&0\\
1&0&0&0&0\\
0&1&0&0&0\\
0&0&0&0&1\\
0&0&0&1&1
\end{pmatrix},
\qquad
S=
\begin{pmatrix}
1&0&0&0&0\\
0&0&1&0&0\\
0&1&0&0&0\\
0&0&0&1&1\\
0&0&0&0&1
\end{pmatrix}.
\]

They satisfy

\[
R^3=S^2=I,
\qquad
SRS=R^{-1}.
\]

Let \(u_0=01,u_1=10,u_2=11\) be the three nonzero vectors of \(\mathbb F_2^2\), and let \(e_i\) be the coordinate vectors of \(\mathbb F_2^3\). An explicit equivariant encoding is:

\[
(2,2,2)\longmapsto(000,00),
\]

\[
\operatorname{pos}_x(0)=i,
\quad x\in S_3(0,3,3)
\quad\Longrightarrow\quad
x\longmapsto(e_i,00),
\]

\[
\operatorname{pos}_x(1)=i,
\quad\operatorname{pos}_x(2)=j,
\quad x\in S_3(1,2,3)
\quad\Longrightarrow\quad
x\longmapsto(e_j,u_i),
\]

and

\[
\operatorname{pos}_x(0)=i,
\quad\operatorname{pos}_x(4)=k,
\quad x\in S_3(0,2,4)
\quad\Longrightarrow\quad
x\longmapsto(111+e_k,u_i).
\]

The selected sixteen vectors have orbit profile \(1+3+6+6\), and the verifier checks equivariance for all \(6\cdot16=96\) group-state pairs.

Since four dimensions are ruled out and five dimensions are explicit,

\[
\boxed{
\text{the minimal affine binary signature register has dimension }5.
}
\]

Thus the exact hardware law is

\[
\boxed{
4\text{ information bits}+1\text{ symmetry bit}=5\text{ affine-equivariant bits}.
}
\]

## Engineering consequence

The 16 exact-cover signature states and the 16 OA ports have the same cardinality, but the signature action cannot be identified with a four-bit affine port register without an explicit nonlinear intertwiner. A controller has two honest options:

1. retain four state bits and implement the \(S_3\) action by a small nonlinear LUT/permutation network; or
2. add one bit and use the explicit five-bit linear representation above.

No claim is made that the signature alphabet is already the OA\((16,3,4,2)\) port alphabet. The theorem instead supplies a falsifier: any proposed direct four-bit affine identification is impossible.

## Reproduction

```bash
python analysis/bt3262_3265_signature_s3_affine_lift.py \
  --json data/PART_BT3262_BT3265_SIGNATURE_S3_AFFINE_LIFT_results.json
python -m pytest -q tests/test_bt3262_3265_signature_s3_affine_lift.py
```

Expected terminal line:

```text
PASS 6/6 exact signature-S3 affine-lift checks
```
