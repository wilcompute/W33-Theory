# Part DCMLXXIX (979) — Ihara Parameter Reconciliation

**Date:** 2026-05-18  
**Series:** W(3,3) Theory of Everything  
**Status:** PARAMETER HYGIENE / PROOF BOUNDARY VERIFIED

---

## Why this part exists

The latest RH/CSS sequence made real progress, but it also exposed a dangerous
notation collision. Three different numbers can all look like ``q'' if the
paper is not careful:

1. **Field parameter:** \(q_{\mathrm{field}}=3\), the ternary field
   \(\mathbb{F}_3\).
2. **PG(2,3) Levi-graph Bass parameter:** the incidence graph is \(4\)-regular,
   so the Ihara determinant uses \(q_{\mathrm{Bass}}=4-1=3\).
3. **W(3,3) collinearity Bass parameter:** the collinearity graph is
   \(12\)-regular, so its Ihara determinant uses \(q_{\mathrm{Bass}}=12-1=11\).

The breakthrough is not another overclaim. It is the exact separation that lets
the graph-Ihara theorem stand cleanly while keeping the classical Riemann
Hypothesis boundary honest.

---

## Correct PG(2,3) Levi graph theorem

The Levi graph of \(\mathrm{PG}(2,3)\) has
\[
|V|=26,\qquad |E|=52,\qquad d=4,\qquad q_{\mathrm{Bass}}=d-1=3.
\]

Its adjacency spectrum is
\[
\{\,4^1,\ (-4)^1,\ (\sqrt3)^{12},\ (-\sqrt3)^{12}\,\}.
\]

The Bass determinant formula is
\[
Z_G(u)^{-1}
=(1-u^2)^{|E|-|V|}\det(I-Au+(d-1)u^2).
\]

For the non-trivial eigenvalue pair \(\lambda=\pm\sqrt3\),
\[
(1-\sqrt3\,u+3u^2)(1+\sqrt3\,u+3u^2)
=1+3u^2+9u^4.
\]

The roots in \(t=u^2\) have \(|t|=1/3\), hence
\[
\boxed{|u|=3^{-1/2}.}
\]

So the finite graph-Ihara RH statement for the PG(2,3) Levi graph is proved:
all non-trivial Ihara poles lie on the critical circle \(|u|=3^{-1/2}\).

---

## What was wrong in the stale formula

The stale quartic
\[
1+5u^2+16u^4
\]
comes from accidentally using \(d=4\) where the Bass determinant requires
\(d-1=3\). That substitution would force \(|u|^2=1/4\), i.e. \(|u|=1/2\), which
is the wrong critical circle for a \(4\)-regular graph.

The correct critical circle is not \(1/2\). It is \(1/\sqrt3\).

---

## W(3,3) collinearity graph is a different graph

The \(W(3,3)\) collinearity graph has
\[
|V|=40,\qquad |E|=240,\qquad d=12,\qquad q_{\mathrm{Bass}}=11.
\]

Its adjacency spectrum is
\[
12^1,\qquad 2^{24},\qquad (-4)^{15}.
\]

Because
\[
\max(|2|,|-4|)=4\le 2\sqrt{11},
\]
the graph is Ramanujan as a \(12\)-regular graph. Its non-trivial Ihara poles
therefore lie on
\[
\boxed{|u|=11^{-1/2},}
\]
not on \(3^{-1/2}\). The field parameter is still \(3\); the graph-Ihara Bass
parameter is \(11\).

---

## Status boundary

What is proved:

- graph RH for the PG(2,3) Levi graph;
- graph RH for the W(3,3) collinearity graph;
- the exact algebra explaining why the stale \(1/2\) radius was a degree/Bass
  parameter slip.

What remains open:

- identifying any finite/projective-limit graph zeta with the classical
  Riemann zeta;
- proving a uniform continuum or adelic limit that transfers graph-Ihara RH to
  classical RH.

So the honest slogan is:

\[
\boxed{\text{Finite graph-Ihara RH is proved; classical RH remains an open bridge.}}
\]

---

## Executable artifact

- Verifier: `verify_dcmlxxix_ihara_parameter_reconciliation.py`
- Test: `tests/test_dcmlxxix_ihara_parameter_reconciliation.py`
- Data: `data/dcmlxxix_ihara_parameter_reconciliation.json`
- Result: `PART_DCMLXXIX_IHARA_PARAMETER_RECONCILIATION_results.json`
