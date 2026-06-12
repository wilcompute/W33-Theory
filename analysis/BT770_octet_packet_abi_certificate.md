# BT770 — Octet Nonedge Packet ABI Certificate

Status: all checks pass.

The exporter is `analysis/bt770_octet_nonedge_packet_abi.py`.

Core facts verified:

- packet count: 45
- points per packet: 8
- stored W33 nonedges per packet: 12
- crossing W33 edges per packet: 16
- stored nonedge total: 540
- unique stored nonedges: 540
- unique crossing edges: 240

Cover laws:

- every W33 point appears in 9 packets
- every W33 edge appears as a crossing edge in 3 packets
- every W33 nonedge appears as a stored nonedge in 1 packet

Graph checks:

- packet intersection graph is SRG(45,32,22,24)
- packet disjointness complement is SRG(45,12,3,3)

Boundary: this is a deterministic export layer for the 45 intrinsic K4,4 octets. It does not assert any unavailable external label table.
