# BT1673 — Block-Encoding Normalization Audit

## Correction

BT1669 minimized raw coefficient mass in powers of the unnormalized Laplacians
\(L_c\) and \(L_m\).  A block-encoded implementation normally supplies

\[
H_c=L_c/\Lambda_c,
\qquad
H_m=L_m/\Lambda_m.
\]

Therefore

\[
\sum_i c_iL^i
=
\sum_i c_i\Lambda^iH^i.
\]

So the physical LCU coefficient mass is not

\[
\sum_i |c_i|,
\]

but rather

\[
\sum_i |c_i|\Lambda^i.
\]

For the current graphs,

\[
\Lambda_c=6,
\qquad
\Lambda_m=30.
\]

## Result

The raw BT1669 algebraic optimum was

\[
(d_c,d_m)=(9,8),
\qquad
\|c\|_{1,\rm raw}=2.0822330410596202\times10^{-10}.
\]

But after block-encoding normalization its LCU mass becomes

\[
\boxed{289713.4069956163.}
\]

The tested block-encoded optimum is instead

\[
\boxed{(d_c,d_m)=(4,2)}
\]

with

\[
\|c\|_{1,\rm raw}=0.2610280546327058,
\]

and

\[
\boxed{\|c\|_{1,\rm block}=334.6461794019932.}
\]

The minimal-depth point

\[
(d_c,d_m)=(3,2)
\]

has

\[
\|c\|_{1,\rm block}=344.2142857142845.
\]

Thus the block-encoded optimum is only one clock degree deeper than the minimal
compiler, and it is nowhere near the raw high-degree endpoint.

## Interpretation

This is a major hardware correction.  The raw high-degree coefficient collapse in
BT1669 is largely a normalization artifact when monomial LCUs are compiled through
\(H=L/\Lambda\).

## Boundary

This audit applies to monomial LCU block-encodings.  Chebyshev, QSVT, or other
orthogonal polynomial compilers need their own normalization analysis.

## Files

- `analysis/bt1673_block_encoding_normalization_audit.py`
- `data/PART_BT1673_BLOCK_ENCODING_NORMALIZATION_AUDIT_results.json`
