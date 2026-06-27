# BT1884-BT1886 summary

Executed BT1884-BT1886.

BT1884 adds a detector-time graph for the `[[66,13,3]]_3` decoder: 56 checks over 3 rounds give 168 detector nodes, 112 time links, and 528 single-error links.  The graph keeps relation-shadow flags so the decoder still does not claim generic weight-2 correction.

BT1885 lowers the BT1882 reuse architecture into switch-fabric primitives: 66 payload paths, 56 check ancillas, 5 switching layers, 4 memory delays, 76 modeled switch/loss units, and 264 edge-touch schedule entries.

BT1886 updates the local splice/build runner so it calls the dual-patch splice script, expects `papers/BT1347_photonic_holonet_journal_with_BT1857_BT1880.tex`, verifies both inserted section labels, rejects enumitem-only `[nosep]`, and attempts a TeX build if a local TeX engine exists.

Boundary: detector graph, primitive lowering, and local runner only; no calibrated likelihood decoder, routed chip, remote PDF build, or physical threshold is claimed.
