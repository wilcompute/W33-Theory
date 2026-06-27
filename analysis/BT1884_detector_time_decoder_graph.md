# BT1884 detector-time decoder graph

BT1884 upgrades BT1881 from a small history table to a detector-time graph.

Counts: 56 checks, 3 rounds, 168 detector nodes, 112 time links, and 528 single-error links.

Detector rule: D(c,t)=s_c(t)-s_c(t-1) over GF(3).

Link types: time links connect the same check across adjacent rounds; data links encode the BT1878 single-Pauli syndromes; shadow flags mark known distance-3 relation patterns that should be flagged rather than nearest-single corrected.

Policy: persistent same-syndrome histories prefer data correction; isolated one-round events prefer a time-link explanation; relation shadows request another round or postselection.

Boundary: graph specification only, not a calibrated likelihood model or implemented matching decoder.
