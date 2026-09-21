# Complete physical Clifford-648 ↔ W33 stabilizer dictionary

The previous bridge fixed the \(SL(2,3)\) quotient action. This pass fixes every one of the 648 group elements.

For the physical qutrit normal form \(Z^aX^bz^c\), choose the Pass-1054 Hessian generators so that
\[
X_{\rm phys}\mapsto x,\qquad Z_{\rm phys}\mapsto y,\qquad z_{\rm phys}\mapsto z_{\rm Hess}^{-1}.
\]
Then the exact Heisenberg-coordinate map is
\[
\boxed{(a,b,c)\mapsto(b,a,-ab-c)\pmod3}.
\]
It is checked on all \(27^2\) products.

Pass 1054 supplies a deterministic split complement \(L\cong SL(2,3)\). For every one of its 24 quotient matrices we select the unique element of this chosen complement, fixing the Clifford lift gauge. Thus each of the \(27\times24=648\) physical normal forms is mapped to:

- a specific permutation of the 40 W33 points;
- a specific affine permutation of the 27 Heisenberg states;
- its order and 40-point cycle partition.

The verifier exhausts all \(648^2=419{,}904\) products and freezes a SHA-256 digest of the complete multiplication-index table.

This is the complete finite group dictionary in one split-complement gauge. It is not a claim that the 27-dimensional permutation representation and the 3-dimensional Schrödinger representation are related by a literal square-matrix conjugation.
