# BT1697 - Holonet Typed Packet ABI

The Holonet paper names the packet header early:

```text
(payload, Pauli frame, chart word, apartment hop, mirror slot, clock phase)
```

and then proves each runtime layer separately. BT1697 promotes the missing
object: one typed packet ABI whose projections are the Q6 body, Hesse epilogue,
Witting admission ROM, dual toroidal port, CSS ledger, and D4-quartic magic
rail.

## Master Identity

```text
72 = 48 + 24 = 16*3 + 3*8
```

The first `48` ticks are the tomotope/Q6 body:

```text
16 Q6 edge traversals * 3 pulse phases = 48 body ticks
```

The last `24` ticks are the selected Hesse branch:

```text
3 Hesse return words * 8 ticks = 24 epilogue ticks
```

So a Holonet packet is not just a list of fields. It is a fixed-width
transaction.

## Admission Layer

The Witting desk becomes the admission ROM:

```text
logical table:  1600 = 40*40 = 520 accepted + 1080 retry-shadow
accepted rate:  520/1600 = 13/40
physical table: 640 = 40 tetrads * 4 Alice slots * 4 Bob slots
              = 480 data handshakes + 160 witness apertures
```

The extra `120` physical rows are not extra throughput. They are same-ray
contextual aperture choices: `160 - 40 = 120`.

## The Typed 24 Boundary

The count `24` appears four times, but BT1697 keeps the roles separate:

```text
24 Hesse epilogue ticks
24 Q4 plaquette guard flags
24 CSS guard-tail rows
24 D4-quartic magic apertures = 2 atoms * 4 branches * 3 phases
```

This is the key architecture point. `24` is not one object being renamed. It is a
typed boundary where four projections of the packet meet.

## Front-End and Memory

The dual toroidal physical port is:

```text
192 = 168 + 24 = 21 shared edges * 2 orientations * 4 residues + 24 guards
```

The CSS edge ledger is:

```text
240 = 216 + 24 = 27 Steinberg central cycles * 8 even Q4 states + 24 guards
```

The magic rail is:

```text
24 = 2 D4 quartic atoms * 4 algebraic branches * 3 qutrit phases
192 = 24 * 8 D4 orientations
```

Therefore the same local bus supports front-end parity checking, ternary CSS
memory, and non-Clifford magic injection without collapsing their field
boundaries.

## Global Runtime

The local `48`-block packet ABI globalizes through the mirror bus:

```text
2160 = 45 polar sheets * 48 tomotope blocks
51840 = 24 lifts * 2160 = |Sp(4,3)|
```

This is the architecture theorem: the packet header is the finite operating
system object. Compute, route, admit, check, inject, and commit are typed
projections of the same transaction.

## Verification

```bash
python3 analysis/bt1697_holonet_typed_packet_abi.py
python3 -m pytest --noconftest -q tests/test_bt1697_holonet_typed_packet_abi.py
```
