# Passes 2309–2314 — resolution quotient, quadratic compiler, spread boundaries, hardware contract, and controller fork

## Scope

This packet continues the complete-cover, regular-spread, quadratic-Hom, and hardware tracks after Passes 2300–2308. It also incorporates the parallel field-reduction and controller results without merging mathematically distinct carriers.

## 2309 — the nonlinear signature quotient is feasible

The complete exact-cover census contains 3,547,800 covers in 327 PSp orbits. Their nonlinear 45-coordinate octet signatures form four PSp orbits of sizes

\[
270+135+270+45=720.
\]

The literal 45-octet action was reconstructed and the certified orbit representatives regenerated. The following nine globally realized signatures satisfy the exact capacity equation:

\[
\{8,147,194,324,432,485,512,598,703\},
\qquad
\sum_i t_i=12\mathbf1_{45}.
\]

Therefore the strongest current nonlinear quotient does **not** obstruct a nine-cover resolution. This is not a resolution: the nine signature types may fail to admit pairwise frame-disjoint representatives. Consequently \(\chi(H)=9\) remains open.

## 2310 — twenty-four orbit programs generate fifty maps

The complete quadratic Hom basis contains 50 surjective maps, 26 symmetric and 24 alternating. Deduplicating their signed-orbit tensors gives only 24 seeds. Five seeds project to all four rational targets. Caching seeds once reduces literal orbit-entry storage from

\[
1,213,920\quad\text{to}\quad583,200,
\]

an exact factor \(281/135\). This is compiler/storage sparsity, not spatial locality or minimal tensor rank.

## 2311 — SRG rank is not permutation rank

For the regular-spread orbit the point stabilizer has order

\[
|H|=2q^2(q^4-1),
\]

while the recorded \(q+1\)-relation valency is

\[
k=\frac{q(q-2)(q^2+1)}2.
\]

A single stabilizer orbital requires \(k\mid |H|\). But

\[
\frac{|H|}{k}=\frac{4q(q^2-1)}{q-2},
\]

and reduction modulo \(q-2\) forces \(q-2\mid24\). For odd \(q\), only \(q=3,5\) survive. At the exact computed case \(q=7\), \(875\nmid235200\). Hence the \(q=7\) relation may be strongly regular, but the PGSp action is not rank three.

## 2312 — a non-Desarguesian control has intersection 28

Over \(\mathbb F_9=\mathbb F_3[u]/(u^2+1)\), choose the nonsquare \(n=1+u\). The regular spread uses \(g=-nx\), while the Kantor spread uses \(g=-nx^3\). Both executable line sets contain 82 totally isotropic lines and partition all 820 projective points.

They share exactly

\[
1+9\cdot3=28
\]

lines: the line at infinity plus the affine lines with \(x^3=x\), namely \(x\in\mathbb F_3\). Thus the regular-family intersection values \(1\) and \(q+1=10\) are not universal for symplectic spreads.

## 2313 — theorem-derived RTL semantics

The committed 36-lane mixer masks satisfy

\[
A=A^T,\qquad A\mathbf1=15\mathbf1,\qquad A^2=9I+6J.
\]

Thirty-six frozen probes span the mean-zero subspace and obey \(A^2x=9x\). The single-J phase controller is checked on all 1,152 input transitions. Its register map has kernel

\[
\{(0,0),(2,3)\},
\]

recovering the order-24 image from 48 abstract register states. These are reference semantics, not timing or device measurements.

## 2314 — the exact controller relation fork

Reducing the overlapping arithmetic generators modulo two gives

\[
|\bar R_4|=2,\qquad |\bar U_6|=3,\qquad |\bar R_4\bar U_6|=7,
\]

and

\[
\langle\bar R_4,\bar U_6\rangle=GL(3,2)\cong PSL(2,7).
\]

The quadratic Hom multiplicity controller instead has triangle signature \((2,3,2)\) and closes as \(S_3\). The order-168 group is simple, so there is no quotient to \(S_3\). Engineering consequence: Fano-routing mode and quadratic-demodulation mode require distinct typed state encodings, distinguished by the product-order assertion.

## Evidence firewall

- No electric charge, flux, colour, generation, or neutrino interpretation is restored.
- The signature witness is necessary but not sufficient for a frame resolution.
- Orbit compression is not a physical coupling model.
- The all-odd-q SRG formulas remain unproved beyond computed cases.
- The Kantor example is one explicit mixed pair, not a classification.
- Hardware contracts do not imply synthesis, timing closure, or fabrication.
