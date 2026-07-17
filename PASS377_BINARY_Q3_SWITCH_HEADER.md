# Pass 377: the binary Q3 switch bank has an exact 48-flag clock image

The oscillator/routing scripts contain two different finite layers which were
too easy to blur:

- the route compiler takes the low three **binary** address bits of a W33 label
  and conditionally toggles one of three Q3 coordinates; and
- the horizon code has six separate \(\mathbb F_3\) parity coordinates.

Pass 377 follows the first layer through the actual BT828 header arithmetic. It
does not turn either layer into an analogue oscillator or a physical device.

For a label \(d\in\{0,\ldots,39\}\), a binary axis
\(m\in\{4,2,1\}\), and a depth residue \(n\in\mathbb Z/3\), put

\[
d' = d\mathbin{\operatorname{xor}}m.
\]

The BT828 block and mirror formulas reduce modulo the transversal flag to

\[
H(n,d,d')=
4\bigl(16n+3d+d'\bmod48\bigr)+(d'\bmod4)
\in\{0,\ldots,191\}.
\]

This is a formula for a packet-header address, not a newly invented map.
The GAP witness verifies that all \(3\cdot3\cdot40=360\) directed one-axis
toggle events have the following exact image.

\[
\lvert\operatorname{im}H\rvert=48,
\qquad
48=24+12+12.
\]

The three coordinate axes have pairwise-disjoint supports of sizes
\(24,12,12\). Their combined fibers have the exact profile

\[
24\text{ flags of multiplicity }5,
\qquad
24\text{ flags of multiplicity }10.
\]

So this is deliberately not a one-toggle/one-state correspondence: the header
compiler compresses 360 local switch events into a 48-flag control plane.

## The clock hidden in the header

Increasing the depth residue is not an analogy. On the 48 actual header flags,
GAP proves the concrete permutation

\[
f\longmapsto f+64\pmod{192}.
\]

It has order three, no fixed flag, and decomposes the support as

\[
48=16\cdot3.
\]

The axis-wise cycle profile is

\[
24=8\cdot3,
\qquad
12=4\cdot3,
\qquad
12=4\cdot3.
\]

Thus the exact computational reading of the oscillator layer is now sharper:
a binary Q3 control bank drives a 48-flag header plane carrying a free
\(C_3\) depth clock. The familiar \(16\times3\) shape also appears in the
later LOAD/FLIP/LATCH body schedule, but Pass 377 does **not** claim that the
two 48-element objects are already identified.

## Typed pipeline and boundary

The existing artifacts establish the following typed sequence:

\[
\text{binary Q3 toggle}
\longrightarrow
\text{BT828 header flag}
\longrightarrow
\text{BT1374 Q6 edge address}
\longrightarrow
\text{BT1406/BT1698 pulse and state schedule}.
\]

BT1374 gives a Q6 edge address for every flag, and BT1406/BT1698 give a
tick-level Q6 transition system. What remains unbuilt is an equivariant,
state-level map sending each individual binary Q3 toggle to a particular Q6
edge traversal or a `LOAD/FLIP/LATCH` delta. The binary cube transport group
and tomotope-derived group must therefore remain distinct until such a map is
constructed.

The compact search signature is `360/48/24/12/12/5/10/16x3`.

## Reproduce

```bash
gap -q analysis/w33_pass377_binary_q3_switch_header.g
python3 -m pytest tests/test_pass377_gap_binary_q3_switch_header.py -q
```

The GAP-owned certificate writes
`data/w33_pass377_binary_q3_switch_header.json` and records 13 exact checks.
