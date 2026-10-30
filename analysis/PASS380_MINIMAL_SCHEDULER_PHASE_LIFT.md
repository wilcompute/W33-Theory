# Pass 380 — the missing compiler object is a 16-row binding table

Pass 378 showed that a scheduler flag cannot itself carry the free header C3
clock: a flag stays constant through LOAD_FLAG, FLIP_Q6_AXIS, and
LATCH_VERTEX. Pass 380 identifies the smallest honest repair and measures
exactly what it does and does not solve.

## Minimal switch state

For the live BT1407 stress body, there are 16 distinct flag identities and
three phase positions per flag. The label

`(tomotope_flag, phase_trit)`

has 48 states and rotates freely by

`(flag, phase) ↦ (flag, phase + 1 mod 3)`.

It is minimal among labels that retain all 16 flag identities and have a free
three-phase action: each flag orbit requires three distinct states, so at least
`16 × 3 = 48` states are necessary. The existing pair reaches that lower
bound. This is not a new Q6 symmetry; it is the scheduler's pre-existing
phase-fiber refinement.

## The canonical full-bus lift

The phase-refined scheduler has one natural map into the complete 192-flag
bus:

`iota(flag, phase) = flag + 64 × phase (mod 192)`.

GAP proves that it is injective on all 48 pulses and C3-equivariant with the
header depth shift. But its 48-image meets the Pass-377 header plane in only
six flags: exactly two complete header cycles,

~~~
[16, 80, 144]
[48, 112, 176]
~~~

They are the cycles attached to scheduler flags 144 and 112. Thus only two of
the sixteen scheduler orbit classes have a canonical alignment with header
cycles under this lift.

## What remains unbuilt

The two oriented anchors leave 14 scheduler cycles and 14 header cycles
unbound. The count makes the missing object precise:

| condition | equivariant extensions |
|---|---:|
| no anchor fixed | `16! × 3^16 = 900657498850357248000` |
| two oriented anchors fixed | `14! × 3^14 = 416971064282572800` |

So the next implementation is not another count match or another Q6 label. It
is a typed 16-row header-orbit binding table, with one optional phase offset
per row. Until that table is constructed and tested, schedule order, Q6 edge
metadata, and the shared `16 × C3` set type do not form a compiler map.

## Scope

This is a finite logic-switch result. It says how much state a scheduler needs
to retain its phase clock, and identifies the exact missing data needed to
connect it to the header control plane. It does not construct a Q6 geometry
intertwiner, a physical pulse implementation, or a hardware oscillator.

## Reproduction

~~~
gap -q analysis/w33_pass380_minimal_scheduler_phase_lift.g
python3 -m pytest tests/test_pass380_gap_minimal_scheduler_phase_lift.py -q
~~~

- witness: `analysis/w33_pass380_minimal_scheduler_phase_lift.g`
- output: `data/w33_pass380_minimal_scheduler_phase_lift.json`
- regression: `tests/test_pass380_gap_minimal_scheduler_phase_lift.py`

Search signature: `48/6/2/14!3^14/minimal-phase-lift`.
