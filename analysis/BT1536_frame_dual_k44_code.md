# Pass 1536 — Frame-Dual K4,4 Code Theorem

## Executive result

Let

\[
M\in\{0,1\}^{540\times240}
\]

be the canonical frame/edge incidence matrix: every row is the four-edge collinearity matching between one unordered pair of disjoint totally isotropic lines of \(W(3,3)\). Work over \(\mathbb F_2\).

The frame code and its dual are now determined exactly:

\[
\boxed{C_{\rm frame}=\operatorname{row}_{\mathbb F_2}(M)=[240,195,4]_2,}
\]

\[
\boxed{C_{\rm frame}^{\perp}=\ker_{\mathbb F_2}(M)=[240,45,16]_2.}
\]

The dual is not an anonymous 45-space. The verifier enumerates the intrinsic induced \(K_{4,4}\) subgraphs of the W33 point graph and finds exactly 45. Let

\[
K\in\{0,1\}^{45\times240}
\]

be their edge-incidence matrix. Then

\[
\boxed{MK^{\mathsf T}=0\pmod2,\qquad \operatorname{rank}_2K=45.}
\]

Since \(\operatorname{rank}_2M=195\), this proves

\[
\boxed{\operatorname{row}_{\mathbb F_2}(K)=\ker_{\mathbb F_2}(M).}
\]

An independent mixed-integer parity search proves that the dual minimum distance is 16, exhausts every weight-16 solution, and finds exactly 45 of them. Their supports agree exactly with the 45 rows of \(K\). Therefore:

\[
\boxed{\text{the 45 intrinsic }K_{4,4}\text{ octets are exactly all minimum dual words.}}
\]

They are linearly independent, so the minimum words themselves form a basis of the complete modular frame cokernel.

## Exact LDPC realization

Each octet check has weight 16, and every one of the 240 W33 edges belongs to exactly three octets. Thus \(K\) is a \((3,16)\)-regular parity-check matrix for \(C_{\rm frame}\). Its 240 column signatures are distinct triples, so the frame code has no words of weight one or two. The frame generators have even weight four, hence

\[
\boxed{d(C_{\rm frame})=4.}
\]

The Tanner graph has

\[
45+240=285\text{ vertices},\qquad45\cdot16=240\cdot3=720\text{ edges},
\]

and girth six. This is an exact finite LDPC object. No physical threshold or quantum-code claim is inferred.

## The minimum-word overlap geometry

Two distinct octet words overlap in either zero or one W33 edge. Joining two minimum words when they overlap gives

\[
\boxed{\operatorname{SRG}(45,32,22,24),}
\]

while disjointness gives its complement

\[
\boxed{\operatorname{SRG}(45,12,3,3).}
\]

The integer Gram matrix is

\[
KK^{\mathsf T}=16I+A_{45},
\]

with spectrum

\[
\boxed{48^1\oplus12^{20}\oplus18^{24}.}
\]

Its field-sensitive ranks are

\[
\boxed{\operatorname{rank}_2(KK^{\mathsf T})=14,\qquad
\operatorname{rank}_3(KK^{\mathsf T})=15.}
\]

This is a new concrete source for the recurring modular \(14\) and rational/ternary \(15\) scales. The verified statement is the rank identity; identifying those ranks with any particular irreducible constituent requires a separate equivariant-module certificate.

## Proof architecture

`analysis/w33_pass1536_frame_dual_k44_code.py` performs the following from scratch.

1. Construct the 40 projective points of \(PG(3,3)\) and the W33 collinearity graph from a nondegenerate alternating form.
2. Enumerate the 40 totally isotropic lines, 240 W33 edges, and 540 disjoint-line frames.
3. Build \(M\), verifying row weight 4, column weight 9, and binary rank 195.
4. Enumerate every independent four-set whose common-neighbour set is an independent four-set; quotienting the swapped bipartitions gives exactly 45 induced \(K_{4,4}\) octets.
5. Build \(K\), verifying row weight 16, column weight 3, \(MK^{\mathsf T}=0\), and binary rank 45.
6. Solve the exact parity model \(Mx=2y\), \(x\ne0\), minimizing \(\lVert x\rVert_1\); the optimum is 16.
7. Fix weight 16 and add one no-good cut per solution. The search finds 45 solutions and then proves the residual model infeasible. The solution set equals the row-support set of \(K\).
8. Verify both strongly regular overlap graphs, the Gram spectrum/ranks, and the Tanner parameters.

All 18 verifier checks pass, and two independent runs reproduce the same matrix and support hashes.

## Prior-art boundary

- **BT766 owns** the intrinsic census of 45 W33-induced \(K_{4,4}\) octets and their 45-point strongly regular overlap geometry.
- **Pass 1416 owns** \(\operatorname{rank}_2M=195\) and therefore the 45-dimensional modular cokernel.
- **Pass 1536 is the new bridge:** the entire modular cokernel is exactly the span of those octets, with exact code parameters and an exhaustive minimum-word classification.

The web literature check found broad work on incidence codes and dual minimum weights in finite projective geometry (for example Lavrauw--Storme--Van de Voorde, arXiv:1201.3291), and work on regular induced subgraphs of classical generalized quadrangles (Bamberg--Bishnoi--Royle, arXiv:1708.01095). The search did not surface this specific frame/octet code identification or the \([240,45,16]\) minimum-word theorem. That is a search result, not a universal novelty proof.

## Evidence boundary

This theorem is finite, binary, exact, and reproducible. It does not establish a detector-loss threshold, a decoding threshold, a quantum stabilizer code, or a physical noise model. Those require separate constructions.
