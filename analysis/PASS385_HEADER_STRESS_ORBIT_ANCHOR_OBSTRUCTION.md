# Pass 385 — the header quotient and stress path have an orbit-anchor obstruction

Passes 377–380 put two sixteen-element carriers next to one another:

- the sixteen free-\(C_3\) cycles of the binary-\(Q_3\) header plane; and
- the sixteen directed \(Q_6\) edges used by the live BT1407 stress body.

Pass 381 correctly treated their crosswalk as reviewed ABI data. Pass 385 asks
whether the two carriers nevertheless possess a natural equivariant
identification that would derive that crosswalk. GAP reads the live BT1371 and
BT1407 tables, reconstructs the Pass-377 quotient, and answers **no for the
inherited actions and the two canonical Pass-380 anchors**.

This is stronger than counting sixteen objects on each side, but deliberately
narrower than a hardware or dynamics claim.

## The header quotient

The Pass-377 header map has

\[
360\ \text{toggle events}\longrightarrow48\ \text{flags}
\longrightarrow16\ C_3\text{-cycles}.
\]

Those cycles compress the 24 directed edges of \(Q_3\). Eight classes contain
one directed edge and have event-fiber size 5; eight contain two directed edges
and have event-fiber size 10. Thus the intrinsic class-size and fiber profiles
are

\[
1^8,2^8,
\qquad
5^8,10^8.
\]

The full directed-edge action of

\[
\operatorname{Aut}(Q_3)\cong C_2^3\rtimes S_3
\]

has order 48. Its setwise preserver of the sixteen compression fibers has
order 16, and its induced faithful action on the quotient is

\[
C_2\times D_8.
\]

It has two transitive orbits of length 8, exactly the singleton and doubleton
classes, with point stabilizer order 2. The named-axis profile `[8,4,4]` is
therefore not the natural orbit partition: the quotient action fuses the two
four-cycle blocks and exposes an intrinsic `[8,8]` partition.

## The live stress carrier is rigid

The sixteen phase-zero rows of the BT1407 body use the flags

```text
159 83 84 22 13 144 135 134 58 63 112 113 44 37 73 180
```

and form an embedded sixteen-edge path on seventeen distinct \(Q_6\)
vertices. Abstractly that path has the reversal group \(C_2\). The live edge
kind, BT1371 orbit color, and direction metadata destroy the reversal, so the
metadata-preserving path automorphism group is trivial.

The BT1371 order-96 subgroup has two regular 96-edge orbits on all 192 edges
of \(Q_6\). The stress path meets those orbits in `[8,8]`, but its setwise
stabilizer in that group is trivial. The stronger calculation in the full

\[
\operatorname{Aut}(Q_6)\cong C_2^6\rtimes S_6,
\qquad |\operatorname{Aut}(Q_6)|=46080,
\]

also gives a trivial setwise stabilizer. The stress edge-kind profile is six
packet edges plus ten connector edges, and its six-direction profile is
`[2,4,3,2,2,3]`.

So the second `[8,8]` is inherited from a coloring of a rigid live path. It is
not an eight-plus-eight orbit decomposition of a nontrivial stress-path
symmetry.

## The two canonical anchors cross the partitions

The decisive obstruction is visible in two exact rows:

| Scheduler flag | Header \(C_3\)-cycle | Header orbit | BT1371 orbit |
|---:|---:|---:|---:|
| 144 | `[16,80,144]` | 0 | 0 |
| 112 | `[48,112,176]` | 0 | 1 |

Both anchored header cycles lie in the same singleton-class orbit of
\(C_2\times D_8\), while their live scheduler edges have opposite BT1371
colors. Swapping the names of the two scheduler colors does not remove that
contradiction. Therefore no bijection respecting both inherited `[8,8]`
partitions can retain both canonical oriented anchors.

Without anchors, the number of abstract partition-respecting cycle bijections
is

\[
2(8!)^2=3,251,404,800.
\]

Allowing an independent \(C_3\) phase offset on every target cycle gives

\[
2(8!)^2 3^{16}=139,962,315,283,660,800.
\]

Those numbers count a choice space; they do not define an automorphism group
of the complete scheduler.

## Precise boundary

The current finite carriers do not supply a nontrivial intrinsic equivariant
header/scheduler binding. Pass 381's sixteen-row crosswalk is therefore
**necessary ABI input**: a total binding must break or ignore at least one of
the two inherited partitions, or change one of the canonical orientations.

This result does not say that a \(Q_6\) implementation is impossible, that a
physical oscillator cannot realize the schedule, or that no data-enriched
compiler can produce a useful crosswalk. It says only that the present group
actions, orbit colors, and two anchors do not canonically derive one.

## Reproduce

```bash
gap -q analysis/w33_pass385_header_stress_orbit_anchor_obstruction.g
python3 -m pytest tests/test_pass385_gap_header_stress_orbit_anchor_obstruction.py -q
```

The GAP-owned witness writes
`data/w33_pass385_header_stress_orbit_anchor_obstruction.json` and checks 31
independent structural assertions.

Search signature:
`48/16/8/8/16/96/1/46080/1/2/orbit-anchor`.
