# Passes 1500–1504: Five Exact Continuation Frontiers

**Status:** exact local workers complete; compact certificate frozen; fail-closed remote replication supplied.  
**Compact certificate SHA-256:** `757b01bacbfc157484851ec76cc3322204116c3aeb9cdf81851a2dbee1a56b3e`

## Pass 1500 — Exact modular Gabriel Ext¹ quivers

For the 83-dimensional selector orbital algebra, the bad-characteristic simple modules and every ordered Ext¹ space were computed directly from derivations modulo inner derivations.

At \(p=2\), there are 13 simple vertices, the Ext¹ arrow-dimension sum is 15, and the regular Loewy data are

\[
J^r:\ 45,16,0,
\qquad
A/J\leftarrow J/J^2\leftarrow J^2:\ 38,29,16.
\]

At \(p=3\), there are five simple vertices and

\[
\dim\operatorname{Ext}^1(S_i,S_j)=
\begin{pmatrix}
2&0&1&0&1\\
0&3&0&1&1\\
1&0&0&0&0\\
0&1&0&0&0\\
1&1&0&0&1
\end{pmatrix},
\]

with radical powers \((72,49,27,14,4,0)\). Higher Yoneda relations are not inferred from Ext¹.

## Pass 1501 — Tensor-factor selector Fourier transform

The fourteen Mackey isotypic sectors are refined deterministically to

\[
\mathbb Q^{m_\chi}\otimes V_\chi,
\]

with \((m_\chi,\dim V_\chi)\)

\[
(1,1),(1,2),(1,2),(1,4),(1,4),(1,8),(1,8),
(2,1),(2,2),(3,4),(3,4),(3,8),(4,8),(5,1).
\]

All 83 orbital operators act as \(M_\chi\otimes I_{V_\chi}\). The exact basis and inverse hashes are

- \(U\): `58b5c1cdc2aefd67a4efde0221f4a708b8e1267b5eb4bad8e1a586bf02ff84b7`
- \(U^{-1}\): `bb75dd295832c7a76fd0a72268ac328fbd437676670bef6ecc64cb1fb12fc160`

The pivot rule is canonical relative to the frozen orbital coordinates and matrix units, not under arbitrary input gauge changes.

## Pass 1502 — Complete apartment-bridge census

All \(8\times3\times4=96\) mask/residual/sign gauges were exhausted:

\[
\text{sheet ranks}:70^4,76^1,81^{19},
\qquad
\text{bridge ranks}:70^{16},76^4,81^{76}.
\]

Every rank-81 sheet is exactly the full Levi cycle/Steinberg rowspace. Among the 76 rank-complete bridges, 57 retain all fourteen Mackey sources at full dimension and 19 lose exactly one dimension in the terminal five-dimensional source sector.

## Pass 1503 — Explicit maximal overorder containing the orbital order

Using the stable lattices \(Oe_b\) in one minimal left ideal of every split Wedderburn block gives

\[
M_O=\bigoplus_b\operatorname{End}_{\mathbb Z}(Oe_b),
\qquad O\subset M_O.
\]

The exact index is

\[
[M_O:O]=2^{36}3^{113},
\]

and

\[
\operatorname{disc}(M_O)=1,
\qquad
\operatorname{disc}(O)=[M_O:O]^2.
\]

This is a different conjugate maximal order from the previously frozen matrix-unit order; containment is verified objectwise.

## Pass 1504 — Full apartment linking algebra

The 76 rank-complete bridges span a 75-dimensional off-diagonal space. Their unique relation is exact over \(\mathbb Z\), supported on twelve side-0/edge-1 bridges in the four weight-three masks across all residuals.

Collectively the bridges cover all 120 selector coordinates and detect all 81 cycle coordinates. Their pairing corners generate

\[
M_{120},\qquad M_{81},
\]

and the closed bimodule has dimension \(120\cdot81=9720\). Therefore the linking envelope has dimension

\[
120^2+81^2+2(120\cdot81)=201^2=40401,
\]

so it is the full \(M_{201}\) and gives a strict gauge-fixed Morita context. This does not promote the construction to a natural full-\(G\)-equivariant Morita equivalence.

## Verification boundary

The five canonical worker hashes are frozen in `data/w33_pass1500_1504_five_frontiers.json`. Local exact executions produced those hashes. The workflow independently regenerates each worker and rejects any mismatch. Queued or unobserved remote jobs are not represented as successful evidence.
