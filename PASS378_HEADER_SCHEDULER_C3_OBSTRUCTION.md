# Pass 378: the two \(16\cdot C_3\) clocks cannot be identified through scheduler flags

Pass 377 built a concrete \(48\)-flag header plane: binary \(Q_3\) toggles
advance under depth by

\[
  f\longmapsto f+64\pmod {192},
\]

so its flags form sixteen free \(C_3\)-orbits.  BT1406 has another \(48\)-slot
object: sixteen Q6 edges, each expanded through the three-phase word

~~~text
LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX.
~~~

It is tempting to identify the two \(16\times3\) structures.  Pass 378 makes
the comparison exact and gives the obstruction.

## Same abstract clock type

The header plane and the BT1406 stress-route phase positions are both free
\(C_3\)-sets with sixteen orbits:

\[
  \operatorname{im}H_{377}\cong16\cdot C_3,
  \qquad
  \operatorname{Pos}_{1406}\cong16\cdot C_3.
\]

An equivariant bijection of these **bare position sets** exists.  It is highly
nonunique: one may permute the sixteen orbits and choose any of three phase
origins on each, so the exact count is

\[
  16!\,3^{16}=900657498850357248000.
\]

This is a set-type coincidence, not a natural map.

## The actual obstruction

The BT1406 scheduler keeps its <code>tomotope_flag</code> constant through a
phase triple:

\[
  \texttt{LOAD\_FLAG}(e,f),
  \texttt{FLIP\_Q6\_AXIS}(e,f),
  \texttt{LATCH\_VERTEX}(e,f).
\]

By contrast, the Pass-377 clock takes every header flag to a **distinct** flag
under its \(C_3\) step.  Therefore an equivariant map from scheduler positions
to header flags cannot factor through the scheduler's actual
<code>tomotope_flag</code> label: phase invariance would force a fixed header
flag, and the header action has none.

The live six-digit stress route makes the mismatch visible.  Its sixteen flags

\[
  [159,83,84,22,13,144,135,134,58,63,112,113,44,37,73,180]
\]

meet the Pass-377 header plane only in \(\{112,144\}\).  Fourteen header
\(C_3\)-cycles contain no stress flag and two contain one; none contains a full
triple.  The stress flag set is not stable under \(f\mapsto f+64\).

So the precise computational conclusion is:

> The header depth clock and pulse-phase clock share the regular
> \(16\cdot C_3\) set type.  The former is a free control-address clock; the
> latter is a three-operation timing index.  No natural edge/flag/state
> intertwiner follows, and the actual scheduler flag projection blocks one.

The compact search signature is <code>48/16x3/16!3^16/2/14+2</code>.

## Reproduce

~~~bash
gap -q analysis/w33_pass378_header_scheduler_c3_obstruction.g
python3 -m pytest tests/test_pass378_gap_header_scheduler_c3_obstruction.py -q
~~~

The focused test also reads the current BT1406 scheduler JSON and pins the
sixteen input flags, so the GAP comparison cannot silently drift if its source
schedule changes.
