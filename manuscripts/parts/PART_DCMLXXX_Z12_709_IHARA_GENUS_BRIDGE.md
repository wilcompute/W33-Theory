# Part DCMLXXX (980) — The \(Z[\zeta_{12}]\) 709 / Ihara / Genus Bridge

**Date:** 2026-05-18
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED WITH CORRECTIONS

---

## Why this part exists

The \(Z[\zeta_{12}]\) search surfaced a striking element:
\[
z = 1 + 2\zeta_{12} + 6\zeta_{12}^2 + 4\zeta_{12}^3.
\]

It appeared to unify \(137\), \(13\), and \(709^2\).  The real result is even
cleaner, but it requires a correction:

- the exact algebraic norm is \(709\), not \(709^2\);
- the existing exploratory script reports \(709^2\) because it multiplies
  squared complex magnitudes over all four embeddings;
- the Eisenstein shadow has exact norm \(13\);
- the identity-embedding squared magnitude rounds to \(137\), but is not
  exactly \(137\).

This part records the exact arithmetic and then checks whether \(709\) enters
the \(W(3,3)\) Ihara determinant.

---

## Exact cyclotomic facts

Let \(K=\mathbb{Q}(\zeta_{12})\).  For
\[
z=(1,2,6,4)
\]
in the basis \(1,\zeta_{12},\zeta_{12}^2,\zeta_{12}^3\), the algebraic norm is
\[
\boxed{N_{K/\mathbb{Q}}(z)=709.}
\]

The exploratory script's reported full norm is therefore
\[
709^2 = 502681,
\]
the square of the algebraic norm.

The prime \(709\) is itself special:
\[
709\equiv1\pmod{12},\qquad 709-1=708=12\cdot59,
\]
so it splits completely in \(\mathbb{Q}(\zeta_{12})\).

The Diophantine curio is also verified:
\[
\boxed{709^3=193^3+461^3+631^3,}
\]
and \(709\) is the first prime with this positive three-prime-cube property in
the checked range.

---

## Shadow norms: exact vs rounded

The identity embedding gives
\[
|z(\zeta_{12})|^2 = 71 + 38\sqrt3 \approx 136.817\ldots,
\]
so it rounds to \(137\), but it is not an exact Gaussian norm \(137\).

The Eisenstein shadow is exact.  Evaluating at \(\omega=\zeta_3\),
\[
z(\omega)=-1-4\omega,
\]
and therefore
\[
N_{\mathbb{Z}[\omega]/\mathbb{Z}}(-1-4\omega)
=(-1)^2-(-1)(-4)+(-4)^2
=13.
\]

The true relative norms land at \(709\):
\[
N_{K/\mathbb{Q}(i)}(z)=15+22i,\qquad 15^2+22^2=709,
\]
and
\[
N_{K/\mathbb{Q}(\omega)}(z)=25+28\omega,\qquad
25^2-25\cdot28+28^2=709.
\]

So the clean reading is:
\[
\boxed{\text{\(13\) is an exact Eisenstein shadow; \(709\) is the exact cyclotomic norm; \(137\) is a near identity-embedding shadow.}}
\]

---

## W(3,3) Ihara alignment

For the \(W(3,3)\) collinearity graph,
\[
\boxed{
Z_G(u)^{-1}
=(1-u^2)^{200}
(1-12u+11u^2)
(1-2u+11u^2)^{24}
(1+4u+11u^2)^{15},
}
\]
where multiplication of the displayed factors is intended.

The primitive Ihara factor support is
\[
\{2,3,5,7,11\}.
\]
Intersecting with the proposed spectral-prime packet
\[
\{7,13,137,709\}
\]
gives only \(\{7\}\).  Thus \(709\) is not a primitive Ihara pole factor.

However, the expanded determinant has three exact structural zero coefficients:
\[
[u^1], [u^2], [u^{479}]\,Z_G(u)^{-1}=0.
\]

After removing those exact structural zeros, the full degree-\(480\)
determinant has exactly one nonstructural coefficient that vanishes modulo
\(709\):
\[
[u^{338}]\,Z_G(u)^{-1}\equiv0\pmod{709},
\]
and no other nonstructural coefficient does.

This is the right status:

\[
\boxed{\text{\(709\) is a secondary nonstructural coefficient resonance, not a primitive graph-Ihara factor.}}
\]

---

## Spectral genus correction

The genus polynomial is
\[
H(n)=\frac{(n-3)(n-4)}{12}.
\]

For \(n=3+4s\) and \(s=\frac12+it\),
\[
H(3+4s)
=\frac{(2+4it)(1+4it)}{12}
=\frac{1-8t^2}{6}+it.
\]

So the identity
\[
\operatorname{Im}H(3+4(\tfrac12+it))=t
\]
is exact.

But the same affine map sends the critical line to
\[
\operatorname{Re}(n)=3+4\cdot\frac12=5.
\]
The axis of the \(H(n)\) parabola is
\[
\operatorname{Re}(n)=\frac72,
\]
which under \(n=3+4s\) corresponds to
\[
\operatorname{Re}(s)=\frac18.
\]

So the correct statement is:

\[
\boxed{\text{the \(n=3+4s\) map preserves the imaginary coordinate on RH, but it does not send RH to the genus axis.}}
\]

The exact modular evaluation remains:
\[
H\!\left(-\frac1{12}\right)
=\frac{1813}{1728}
=\frac{7^2\cdot37}{12^3}.
\]

---

## Executable artifact

- Verifier: `verify_dcmlxxx_z12_709_ihara_genus_bridge.py`
- Tests: `tests/test_dcmlxxx_z12_709_ihara_genus_bridge.py`
- Data: `data/dcmlxxx_z12_709_ihara_genus_bridge.json`
- Result: `PART_DCMLXXX_Z12_709_IHARA_GENUS_BRIDGE_results.json`
