# BT1701-BT1703 - Holonet Runtime Safety Packet

BT1698-BT1700 made the Holonet packet executable. BT1701-BT1703 make it
inspectable, schedulable, and fault-classified.

## BT1701 - trace visualizer

The packet trace is now emitted as generated HTML/SVG:

```text
docs/bt1701_holonet_packet_trace_visualizer.html
```

It shows the 72 ticks, the five physical windows, the 48/24 body/guard split,
and the recursive compiler law on one page.

## BT1702 - scheduler collision audit

The scheduler key is:

```text
extended_slot = packet_address*2160 + polar_sheet*48 + body_slot
phase = body_slot mod 3
```

This proves collision freedom on the extended recursive key. If the packet
address is dropped, recursive packets intentionally reuse the same finite
2160-slot bus. That reuse is safe only as time-division:

```text
(packet_time_slice, local_mirror_slot, phase)
```

So the result is strong but bounded: recursive packets can interleave without
same-key collisions, but the finite 2160 physical bus is not magically infinite
parallel hardware.

## BT1703 - symbolic fault propagation

The lowered packet now has a symbolic fault table:

```text
LOSS       -> retry frame or local reprogram retry
DARK_CLICK -> local dark-reference termination
PARITY     -> CSS syndrome handoff
```

All 72 loss hooks, 8 dark-reference clicks, and 24 parity guard-weld faults are
classified. This is not a calibrated noise theorem; it is the ABI-level routing
table required before calibrated physics can be attached.
