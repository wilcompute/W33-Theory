# Passes 1158–1162: Corrected Release Record

Date: 2026-07-27  
Status: **superseded in part by Passes 1173–1177**

This file preserves the Pass-1158–1162 namespace while replacing three failed claims with exact results.

## Pass 1158 — exact residual, not arithmetic speculation

The cubic-map kernel has dimension 2195 and contains three copies of the 81-dimensional Steinberg constituent. Pass 1135 already computed the complete character decomposition. After removing the Steinberg packet, the exact residual is

\[
13\cdot1+16\cdot6+5\cdot15+4\cdot15_a+21\cdot20+2\cdot24
+9\cdot30+4\cdot60_a+10\cdot64+1\cdot90,
\]

of dimension 1952. Its commutant dimension is 1109. Numerical factorization of 1952 does not determine a module decomposition.

## Pass 1159 — Hecke invariants only

The verified facts are the Hecke algebra dimension 26, center dimension 9, and mass identity 432. A complete multiplication table requires explicit orbital products; dimension and Wedderburn multiplicities alone are not a structure-constant computation.

## Pass 1160 — corrected character bridge

The full Weyl group has order 51840, while the faithful projective subgroup has order 25920. The exact 25 character degrees in Passes 1124 and 1135 have squared sum 51840. The 40-point rank-three permutation module is

\[
1\oplus24\oplus15.
\]

## Pass 1161 — corrected determinant and Ihara factor

For \(D=A-I\),

\[
\det(I-xD)=(1-11x)(1-x)^{24}(1+5x)^{15}.
\]

For the 12-regular W33 graph, the Ihara--Bass quadratic coefficient is \(k-1=11\):

\[
\det(I-uB)=
(1-u^2)^{200}
(1-12u+11u^2)
(1-2u+11u^2)^{24}
(1+4u+11u^2)^{15}.
\]

## Pass 1162 — corrected synchronization

The synchronization test now locks the exact group orders, character square sum, residual decomposition, residual/kernel/domain commutant dimensions, rank-three point module, and Ihara coefficient.
