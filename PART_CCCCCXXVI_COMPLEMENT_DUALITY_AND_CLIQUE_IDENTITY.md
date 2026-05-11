# PART_CCCCCXXVI_COMPLEMENT_DUALITY_AND_CLIQUE_IDENTITY.md

## Complement Duality

The complement of \(W(3,3)\) has parameters
\[
\overline{W}(3,3)=\mathrm{SRG}(40,27,18,18).
\]
Its nontrivial eigenvalues are
\[
+3 \text{ and } -3.
\]
Thus the complement has exact symmetric spectrum \(\pm q\) with \(q=3\).

This gives a duality statement:
- the original graph has eigenvalues \(2\) and \(-4\), asymmetrically placed around 0,
- the complement collapses to the perfectly balanced pair \(\pm 3\).

## Clique Polynomial Identity

The clique polynomial of \(W(3,3)\) is
\[
C(x)=1+40x+240x^2+160x^3+40x^4.
\]
Three evaluations are especially rigid:
\[
C(0)=1,
\]
\[
C(1)=1+40+240+160+40=481=480+1=vk+1,
\]
\[
C(-1)=1-40+240-160+40=81=3^4=q^{q+1}.
\]

The alternating value \(C(-1)=81\) is especially striking, since it is exactly \(q^{q+1}\) for the unique master value \(q=3\).

## Interpretation
The complement encodes an exact \(\pm q\) mirror symmetry, while the clique polynomial evaluates at \(-1\) to a pure power of \(q\). Together these form a new algebraic-spectral lock for the \(W(3,3)\) structure.
