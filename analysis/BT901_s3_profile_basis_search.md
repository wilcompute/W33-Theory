# BT901 — \(S_3\) Profile-basis Search

BT895 found the representation home:

\[
\mathbb C[27]=6\cdot\mathbf1\oplus3\cdot\mathbf{1'}\oplus9\cdot\mathbf2.
\]

BT901 makes the profile layer explicit as

\[
V_{\rm profile}=\mathbb C^9\otimes \mathrm{Std}(S_3).
\]

That is the clean commutant model: physical profile matrices act on the multiplicity factor \(\mathbb C^9\) and tensor with the identity on the \(S_3\) standard doublet.

## Result

The Cabibbo primitive from BT897 embeds as a two-plane rotation in the multiplicity space:

\[
\cos\theta=\frac{13}{\sqrt{178}},\qquad
\sin\theta=\frac{3}{\sqrt{178}}.
\]

The verifier lifts the up/down profile Gram matrices to

\[
A\otimes I_2,\qquad B\otimes I_2
\]

on the full \(18=9\cdot2\) standard-doublet sector. Both commute with the \(S_3\) rotation and reflection generators, while the up/down profile Gram matrices fail to commute with each other.

So the profile layer has the needed freedom without breaking flavor equivariance:

\[
\boxed{\text{CKM/PMNS rotations act on the }\mathbb C^9\text{ multiplicity space and commute with }S_3.}
\]

## Important boundary

The \(q^2=9\) layer is not nine extra generations. It is the multiplicity space of the nine copies of the \(S_3\) standard doublet.

## Witness

```text
analysis/bt901_s3_profile_basis_search.py
data/PART_BT901_S3_PROFILE_BASIS_SEARCH_results.json
```
