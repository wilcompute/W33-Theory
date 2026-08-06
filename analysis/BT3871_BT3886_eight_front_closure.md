# Passes 3871–3886 — cubic tightening, tomotope correction, modular closure, and Gewirtz residuals

## Frozen status

```text
PASS_5_FRONTS_PLUS_3_BONKERS_WITH_TWO_CORRECTIONS
d1ac79b9df49e25d84c2e08f5c440ac9a0e5bd90b60e89deebe6699f309143b5
```

This packet executes the five open fronts following Passes 3729–3742 and adds three independent constructions. Two results are corrective: the exceptional order-192 tomotope completion is a split centerless outer extension rather than a central double cover, and the cubic-transversal upper witness improves from 178 to 177 without closing the endpoint.

## 3871–3872 — 63-face cap and 177-face transversal

The 5,040 dependency triples on the 240 filled faces retain the exact lower bound

\[
\tau_{\rm cubic}\ge106.
\]

An explicit 63-face cap gives a complementary 177-face transversal and therefore

\[
\boxed{106\le\tau_{\rm cubic}\le177}.
\]

Its triple-hit profile is

\[
1^{876}2^{2217}3^{1947}.
\]

The cap is locally optimal against every exchange removing at most two selected faces. This is not a proof that a 64-cap is impossible. The separate covering-radius boundary remains

\[
389\le R\le435.
\]

## 3873–3874 — corrected exceptional tomotope group

The completion-order square remains

\[
\begin{pmatrix}96&96&192\\192&96&96\\96&192&96\end{pmatrix}.
\]

The three exceptional groups have trivial center, a unique normal elementary abelian subgroup of order 16, and quotient order census

\[
1^1 2^7 3^2 6^2,
\]

identifying the quotient as \(D_{12}\). The ordinary order-96 subgroup is \(2^4:S_3\), while the exceptional group is the split centerless outer extension

\[
\boxed{2^4:D_{12}}.
\]

Thus the previous non-split central-double-cover identification is withdrawn.

## 3875–3877 — complete characteristic-three descent

The previously unresolved 115-dimensional quotient has composition-series dimensions

\[
0<10<24<29<39<64<69<70<84<89<99<100<114<115.
\]

The successive factor dimensions are

\[
10,14,5,10,25,5,1,14,5,10,1,14,1.
\]

Each factor generates the full matrix algebra \(M_d(\mathbb F_3)\), so every factor is absolutely irreducible. The complete composition multiset is

\[
\boxed{1^3\oplus5^3\oplus10^3\oplus14^3\oplus25}.
\]

This is a defining-characteristic theorem over \(\mathbb F_3\), not a characteristic-zero semisimplicity assertion.

## 3878–3879 — asymmetric Gewirtz residual obstruction

The exact Golay/Witt construction produces \(\operatorname{SRG}(56,10,0,2)\). Fixing a second Witt point gives an independent 16-set plus a residual 40-set. The two-point stabilizer has order 960 and residual subdegrees

\[
1,24,3,6,6.
\]

Its unique invariant degree-12 relation union is not W33: adjacent pairs have zero common neighbors, while nonadjacent pairs have four or twelve. Its spectrum is

\[
12^1 4^5 0^{30}(-8)^4.
\]

This closes the natural stabilizer-equivariant residual bridge; fully non-equivariant maps remain open.

## 3880 — durable website migration lock

The authoritative `docs/index.html` remains pinned to Git blob

```text
41a8d733f42da18282fa276f5d2fa82bac7516f6
```

A fail-closed validator permits future replacement only when an explicit authorization record binds the old blob, new blob, byte-exact archive, literal authorization phrase, `approved_by: wilcompute`, and a nonempty reason. This packet does not authorize or perform a migration.

## 3881–3886 — three chained constructions and evidence closure

1. **Free cap-orbit code.** The 63-cap has trivial stabilizer under the order-25,920 face action. Its orbit is a binary constant-weight code with
   \[
   n=240,\quad M=25{,}920,\quad w=63,\quad d_{\min}=62.
   \]

2. **Petersen blow-up.** The invariant degree-12 Gewirtz residual has ten independent twin classes of size four; collapsing them gives the Petersen graph \(\operatorname{SRG}(10,3,0,1)\).

3. **W33 fibre frame.** The cap descends to forty six-face fibres with occupancy histogram
   \[
   0^6 1^{17}2^7 3^9 5^1.
   \]
   The occupancy vector has a free 25,920-element orbit. Its exact W33 spectral energies on the \(12,2,-4\) channels are
   \[
   \frac{3969}{40},\quad\frac{157}{5},\quad\frac{163}{8}.
   \]

## Evidence boundary

No 64-cap nonexistence, exact cubic endpoint, exact radius endpoint, ten-colour closure, fully non-equivariant Gewirtz bridge, remote CI/PDF result, hardware result, laboratory result, Monster embedding, or physical mechanism is asserted.
