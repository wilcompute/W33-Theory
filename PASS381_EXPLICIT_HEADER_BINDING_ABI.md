# Pass 381 — the header/scheduler crosswalk is now executable ABI data

Pass 380 established that the phase-refined scheduler and the Pass-377 header
plane have the common abstract type \(16\cdot C_3\), but that only two of their
sixteen cycles align through the canonical full-bus lift.  It did **not** make
the remaining fourteen correspondences natural.

Pass 381 does the next honest computing step: it makes those correspondences
explicit, reviewed compiler input and verifies the resulting finite control
trace in GAP.

## The input object

`analysis/w33_pass381_header_orbit_binding_abi.json` has sixteen rows.  A row
contains

```text
(edge_step, tomotope_flag, header_cycle_rep, phase_offset).
```

For phase \(p\in\mathbb Z/3\), its compiler rule is

\[
  (f,p)\longmapsto
  r+64(p+o)\pmod {192},
\]

where \(r\) is the selected header-cycle representative and \(o\) is the
stored phase offset.  Thus every scheduler phase step compiles to the header
depth step `flag -> flag + 64 (mod 192)`.

Two rows preserve the genuine Pass-380 anchors:

| scheduler flag | header cycle | offset | phase-zero output |
|---:|---|---:|---:|
| 144 | `[16,80,144]` | 2 | 144 |
| 112 | `[48,112,176]` | 1 | 112 |

The other fourteen rows are deliberately labelled
`reviewed_external_binding`.  They are configuration, not consequences of
Q6 geometry, raw scheduler flags, numeric ordering, or an automorphism-group
argument.

## Exact verified behavior

GAP reads the table and the live 48-pulse BT1407 body.  It verifies:

\[
  16\text{ rows}\quad\Longrightarrow\quad48\text{ distinct compiled flags}
  =\operatorname{im}H_{377}.
\]

The compiled trace is bijective, has a checked inverse position for every
pulse, and respects every three-operation scheduler word:

```text
LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX
```

\[
  c(e,p+1)=c(e,p)+64\pmod{192}.
\]

So the table creates an executable crosswalk, including a complete audit trace
of all 48 live scheduler pulses.  It does **not** repair Pass 379: the current
BT1371 address table still does not turn the header clock into a Q6 geometric
operation.  Nor does it prove that a different table is forced by the current
finite objects.

The compact search signature is `16/48/2+14/external-binding-abi`.

## Reproduce

```bash
gap -q analysis/w33_pass381_explicit_header_binding_abi.g
python3 -m pytest tests/test_pass381_gap_explicit_header_binding_abi.py -q
```

Artifacts:

- input: `analysis/w33_pass381_header_orbit_binding_abi.json`
- GAP verifier: `analysis/w33_pass381_explicit_header_binding_abi.g`
- output: `data/w33_pass381_explicit_header_binding_abi.json`
- regression: `tests/test_pass381_gap_explicit_header_binding_abi.py`
