# Part DCMLXXXII (982) - Ihara/Z12 Cross-Branch Resonance Audit

**Date:** 2026-05-18
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED CORRECTIVE AUDIT

---

## Why this part exists

The remote GitHub `main` notes from May 17-18 contained real arithmetic
signals, but they mixed three layers:

- the live W(3,3) Ihara-Bass determinant;
- a coefficient-12 arithmetic shadow;
- the Z[zeta_12] norm-709 packet.

This part reconciles those layers without merging remote `main` wholesale.  It
uses the remote notes as audited source material and promotes only exact,
locally reproducible statements.

---

## Live graph zeta: Bass-11

For the W(3,3) collinearity graph,
\[
|V|=40,\qquad |E|=240,\qquad d=12,\qquad q_{\rm Bass}=d-1=11.
\]

The exact reciprocal Ihara determinant is
\[
\boxed{
Z_{W33}(u)^{-1}
=(1-u^2)^{200}
(1-12u+11u^2)
(1-2u+11u^2)^{24}
(1+4u+11u^2)^{15}.
}
\]

Multiplication of the displayed factors is intended.

The two non-trivial discriminants are
\[
2^2-4\cdot 11=-40,\qquad (-4)^2-4\cdot 11=-28.
\]

Thus the live graph-zeta fields are
\[
\boxed{Q(\sqrt{-10})\quad\text{and}\quad Q(\sqrt{-7}).}
\]

The \(Q(\sqrt{-7})\) sector is Heegner; the \(Q(\sqrt{-10})\) sector is not.
Both non-trivial pole families lie on the graph-RH circle
\[
\boxed{|u|=11^{-1/2}.}
\]

---

## Coefficient-12 shadow

If the quadratic coefficient is changed from \(11\) to \(12\), the two
discriminants become
\[
2^2-4\cdot 12=-44,\qquad (-4)^2-4\cdot 12=-32.
\]

This produces
\[
\boxed{Q(\sqrt{-11})\quad\text{and}\quad Q(\sqrt{-2})}
\]
with radius \(12^{-1/2}\).

That branch is real arithmetic structure, but it is not the W(3,3)
Ihara-Bass determinant.  The exact Bass decrement is:
\[
-44\longrightarrow -40,\qquad -32\longrightarrow -28.
\]

Only the live \(s=-4\) sector lands in a Heegner field after the decrement:
\[
Q(\sqrt{-7}).
\]

---

## Z12 norm and the 709 resonance

For
\[
z=1+2\zeta_{12}+6\zeta_{12}^2+4\zeta_{12}^3,
\]
the exact algebraic norm is
\[
\boxed{N_{\mathbb{Q}(\zeta_{12})/\mathbb{Q}}(z)=709.}
\]

The associated exact and shadow readings are:

- \(709\) is the exact Z[zeta_12] algebraic norm;
- \(709^2\) is the squared-magnitude artifact from multiplying squared complex
  magnitudes;
- \(13\) is the exact Eisenstein shadow norm;
- \(137\) is only a rounded identity-sheet shadow for this Z12 element.

The W(3,3) primitive Ihara factor support is
\[
\{2,3,5,7,11\}.
\]
Intersecting it with \(\{7,13,137,709\}\) gives only \(\{7\}\), so \(709\) is
not a primitive graph-zeta factor.

The exact expanded-determinant comparison is sharper:

- Bass-11 has exact structural zero coefficients at degrees \(1,2,479\) and
  one nonstructural mod-\(709\) resonance at degree \(338\);
- coefficient-12 has exact structural zero coefficients at degrees \(1,479\)
  and one nonstructural mod-\(709\) resonance at degree \(424\).

Thus the 709 signal is branch-sensitive:
\[
\boxed{338\text{ is the live Bass-11 resonance; }424\text{ is the coefficient-12 shadow resonance.}}
\]

---

## Alpha and Heegner boundary

The exact alpha packet still has a live Gaussian reading:
\[
\alpha^{-1}=137=11^2+4^2.
\]

The prime \(137\) splits in both \(Q(\sqrt{-7})\) and \(Q(\sqrt{-11})\).  The
important boundary is that \(Q(\sqrt{-7})\) is the live Bass-11 Heegner sector,
while \(Q(\sqrt{-11})\) belongs to the coefficient-12 shadow branch.  The Z12
element's rounded \(137\) shadow should not be promoted into an exact
three-norm unification with \(13\) and \(709\).

---

## RH status

The finite W(3,3) graph-Ihara RH statement is proved.  The classical Riemann
Hypothesis is not proved here.

The remaining theorem target is unchanged:
\[
\boxed{zeta_W=zeta\text{ remains an open adelic/projective-limit identification bridge.}}
\]

---

## Executable artifact

- Verifier: `verify_dcmlxxxii_ihara_z12_cross_branch_resonance_audit.py`
- Tests: `tests/test_dcmlxxxii_ihara_z12_cross_branch_resonance_audit.py`
- Data: `data/dcmlxxxii_ihara_z12_cross_branch_resonance_audit.json`
- Result: `PART_DCMLXXXII_IHARA_Z12_CROSS_BRANCH_RESONANCE_AUDIT_results.json`
