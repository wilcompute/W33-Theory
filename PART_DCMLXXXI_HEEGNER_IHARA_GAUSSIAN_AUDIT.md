# Part DCMLXXXI (981) - The Heegner / Ihara / Gaussian Audit

**Date:** 2026-05-18
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED CORRECTIVE AUDIT

---

## Why this part exists

The GitHub `main` note
`NOTES/HEEGNER_IHARA_BREAKTHROUGH_MAY18_2026.md` surfaced a useful pattern:
if one writes the W(3,3) Ihara quadratics with coefficient `12`, the two
non-trivial families land in
\[
Q(\sqrt{-11}),\qquad Q(\sqrt{-2}),
\]
with pole radius \(12^{-1/2}\).

That is not the W(3,3) Ihara-Bass determinant.

For a 12-regular graph, the Bass determinant uses the non-backtracking
branching number
\[
12-1=11.
\]

So this part keeps the insight, but puts it in the correct shell:

- coefficient `12` gives a coherent Heegner shadow;
- coefficient `11` is the actual W(3,3) graph-Ihara theorem;
- the urgent Gaussian division by \(4+11i\) fails.

---

## Correct W(3,3) Ihara determinant

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

Here multiplication of the displayed factors is intended.

The two non-trivial discriminants are
\[
2^2-4\cdot 11=-40,\qquad (-4)^2-4\cdot 11=-28.
\]

Thus the actual Ihara fields are
\[
\boxed{Q(\sqrt{-10})\quad\text{and}\quad Q(\sqrt{-7}).}
\]

The \(s=-4\) sector lands in the Heegner field \(Q(\sqrt{-7})\).  The
\(r=2\) sector lands in \(Q(\sqrt{-10})\), not a class-number-1 Heegner field.

Both non-trivial pole families lie on the graph-RH circle
\[
\boxed{|u|=11^{-1/2}.}
\]

So W(3,3) has strict adjacency spectral slack, since
\[
\max(|2|,|-4|)=4<2\sqrt{11},
\]
but its non-trivial Ihara poles are not inside the Ihara critical circle. They
are exactly on it, as the graph RH requires.

---

## The coefficient-12 shadow

If one instead writes
\[
1-\lambda u+12u^2,
\]
then the discriminants become
\[
2^2-4\cdot 12=-44,\qquad (-4)^2-4\cdot 12=-32.
\]

That produces
\[
Q(\sqrt{-11}),\qquad Q(\sqrt{-2}),
\]
and pole radius \(12^{-1/2}\).

This is the source of the GitHub note's Heegner pattern.  It is a real adjacent
arithmetic shadow, but it is not the Ihara-Bass determinant of the 12-regular
W(3,3) collinearity graph.

---

## Gaussian division result

The requested division is
\[
\frac{160+221i}{4+11i}
=\frac{(160+221i)(4-11i)}{137}
=\frac{3071-876i}{137}.
\]

Neither numerator is divisible by \(137\):
\[
3071\equiv57\pmod{137},\qquad -876\equiv83\pmod{137}.
\]

Therefore
\[
\boxed{\frac{160+221i}{4+11i}\notin Z[i].}
\]

The conjugate divisor \(4-11i\) also fails.  Equivalently,
\[
74441\equiv50\pmod{137},
\]
so no Gaussian prime of norm \(137\) divides \(160+221i\).

What survives is still useful:
\[
137=4^2+11^2,\qquad
4889=20^2+67^2,\qquad
74441=160^2+221^2.
\]

All three are rational primes congruent to \(5\pmod{12}\), so they live on the
same Gaussian/Frobenius sheet.  The exact alpha numerator is
\[
669969=9\cdot74441=480^2+663^2,
\]
so the exact fraction is a Gaussian-sheet norm ratio,
\[
\alpha^{-1}_{\rm exact}
=\frac{N(480+663i)}{N(20+67i)},
\]
not a \(137\)-divisibility tower.

---

## Correct status

\[
\boxed{
\text{The Heegner tower is adjacent to W(3,3), but the live Ihara theorem remains Bass-11.}
}
\]

Coefficient \(12\) is a productive shadow to study.  Coefficient \(11\) is the
graph zeta.

---

## Executable artifact

- Verifier: `verify_dcmlxxxi_heegner_ihara_gaussian_audit.py`
- Tests: `tests/test_dcmlxxxi_heegner_ihara_gaussian_audit.py`
- Data: `data/dcmlxxxi_heegner_ihara_gaussian_audit.json`
- Result: `PART_DCMLXXXI_HEEGNER_IHARA_GAUSSIAN_AUDIT_results.json`
