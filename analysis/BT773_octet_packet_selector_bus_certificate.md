# BT773 — 2160 Octet Packet Selector Bus Certificate

Status: verifier added.

Verifier: `analysis/bt773_octet_packet_selector_bus.py`.

Core identity:

\[
2160=45\cdot48=540\cdot4=240\cdot9.
\]

Interpretation:

- 45 intrinsic K4,4 octet packets
- 48 selector slots per packet
- 540 W33 nonedges
- 4 opposite-half selector centers per stored nonedge
- 240 centered local K3,3 charts
- 9 W33 nonedges per chart

The verifier constructs each selector slot as:

\[
(\text{packet},\text{stored nonedge},\text{opposite selector center})
\]

and maps it to the centered chart determined by the two W33 lines from the
selector center to the endpoints of the stored nonedge.

Verified checks:

- total slots: 2160
- 45 packets each have 48 slots
- 540 W33 nonedges each have 4 slots
- 240 centered local K3,3 charts each have 9 slots
- 40 selector centers each occur in 54 slots
- packet selector slots equal chart/nonedge incidences exactly

Boundary: this fuses the 45 packet ABI to the 2160 chart/nonedge selector bus.
It is a W33-intrinsic incidence bijection, not a root-torsor table.
