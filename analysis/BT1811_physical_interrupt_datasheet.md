# BT1811 — Physical Interrupt Datasheet

## Purpose

BT1811 turns BT1807--BT1810 into a builder-facing interrupt-sheet. It is not a claim about wall-clock hardware performance. It is the exact finite routing contract that an optical/electronic/VM implementation must preserve.

## Primitive

Substrate:

\[
W(3,3)=SRG(40,12,2,4).
\]

Per defect center \(p\):

\[
\Gamma(p)=12,
\qquad
\mathrm{Safe}(p)=27,
\qquad
\mathrm{Phase}(p)=9.
\]

The defect star splits into four star-lines:

\[
\Gamma(p)=L_1\sqcup L_2\sqcup L_3\sqcup L_4,
\qquad |L_i|=3.
\]

The nine interrupt-vector rows form:

\[
TD(4,3)\cong AG(2,3).
\]

## Interrupt vector row

Each vector row contains:

| Field | Exact meaning |
|---|---|
| `center` | active defect center \(p\) |
| `phase` | one of 9 Hesse/Wigner phase points |
| `safe_triad` | 3 safe payload/address points, partitioning the 27-point safe zone |
| `cheap_quad` | 4 cheap relocation targets, one on each star-line |
| `slot` | one of 3 deterministic cover slots for the chosen directed edge |

The local row count is:

\[
9\text{ phase rows}\times4\text{ cheap exits}=36\text{ exits per center}.
\]

Each of the 12 neighbors appears in exactly three exits:

\[
36=12\cdot3.
\]

## Global scheduler contract

Across all centers:

\[
40\cdot9\cdot4=1440=3\cdot480=6\cdot240.
\]

Therefore:

- every directed W33 edge is exposed by exactly 3 interrupt vectors;
- every undirected W33 edge is exposed by exactly 6 directed interrupt vectors;
- the deterministic scheduler has 3 equal slots of 480 rows each.

## Page-loader contract

Every relocation changes the 27-point safe zone by exactly nine points:

\[
|\mathrm{Safe}(p)\cap\mathrm{Safe}(q)|=18,
\qquad
27-18=9.
\]

The phase-level shape distinguishes edge moves from nonedge moves.

### Edge move

For \(p\sim q\):

\[
\boxed{6\text{ phase triples survive whole} + 3\text{ phase triples rebuild whole}.}
\]

Histogram:

\[
\{0:3,\;3:6\}.
\]

### Nonedge move

For \(p\not\sim q\):

\[
\boxed{9\text{ phase triples each keep two points and rebuild one}.}
\]

Histogram:

\[
\{2:9\}.
\]

Both moves have the same nine-point page bill, but edge moves preserve phase blocks and already win on Pass-64 ray price. So the compiled rule is:

\[
\boxed{\text{relocate along a W33 edge whenever possible}.}
\]

## Hardware/VM pins

| Quantity | Value |
|---|---:|
| Centers | 40 |
| Neighbors per center | 12 |
| Safe points per center | 27 |
| Phase rows per center | 9 |
| Cheap exits per phase row | 4 |
| Cheap exits per center | 36 |
| Directed fabric edges | 480 |
| Scheduler rows | 1440 |
| Directed edge exposure | 3 |
| Relocation page bill | 9 points |
| Edge phase rebuild | 3 whole phase triples |
| Nonedge phase rebuild | 1 point in each phase triple |

## Honest scope

This datasheet is an exact finite-incidence interface. It says what a correct implementation must preserve. It does not assert photon loss, switching time, wall-clock throughput, thermal budget, or experimental contextual-fraction measurement.
