# Full 81-address/operator equivariant-compiler obstruction

The 27-dimensional H27 obstruction lifts directly to the actual 81-root virtual-machine chart.

The address side is the regular module of
\[
K_{\rm addr}=H_{27}^{\rm address}\times C_3^{\rm external\ shift},
\qquad |K|=81,
\]
on the frozen labels \(((a,b,c),p)\).

On the execution side, restrict Pauli243 to the internal trinification H27 and the external qutrit shift.  The matter carrier is
\[
(9V_\omega)\otimes\operatorname{Reg}(C_3).
\]

For each of the three external \(C_3\) characters, the regular scheduler supplies only three copies of \(V_\omega\), whereas the operator carrier requires nine.  Hence
\[
\dim\operatorname{Hom}_K=3(3\cdot9)=81,
\]
but
\[
\boxed{\operatorname{rank}T\le 3(3\cdot\min(3,9))=27}
\]
for every \(K\)-equivariant map \(T:\mathbb C^{81}\to\mathbb C^{81}\).

There is also a one-line characteristic-subgroup proof.  The derived subgroup is
\[
[K,K]=Z(H_{27})\times\{0\}\cong C_3,
\]
so it is characteristic.  Its nontrivial generator has spectrum
\[
1^{27},\ \omega^{27},\ (\omega^2)^{27}
\]
on the regular address module, but acts as the scalar \(\omega I_{81}\) on the operator matter module.  Thus an equivariant map can see at most the 27-dimensional matching central eigenspace.

## Consequence

The open frozen-root compiler cannot be an invertible equivariant conjugacy between the landed scheduler and execution actions.  The compiler must be explicitly **symmetry-changing**: either non-equivariant, covariant under a proper common subgroup, or formulated after replacing/enlarging one of the actions.

This is useful rather than destructive.  It tells us not to spend further search effort among the 1920 anchored GQ(2,4) gauges looking for a nonexistent symmetry-preserving 81x81 basis map.

## Boundary

A plain bijection between the 81 root labels still exists.  This theorem does not determine which non-equivariant gauge is physically meaningful and does not, by itself, settle whether non-FI powers of the Qpsi clock normalize the execution algebra.
