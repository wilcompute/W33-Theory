# Passes 2946–2952 evidence request

This branch exists only to trigger and retain observable external evidence for the source-complete packet already published on `master`.

The dedicated workflow:

1. runs every Pass 2946 MILP orbit in a separate process;
2. regenerates Passes 2947–2952 exact certificates;
3. runs the focused regressions;
4. generates the OAM router and reversible transcript RTL;
5. exhaustively simulates the M36 microcode, 360 directed OAM routes, 256 transcript states, 6,561 quarter-turn states, and 3,240 joint-rank states;
6. synthesizes and places four datapaths on HX8K;
7. integrates the machine blueprint and website idempotently;
8. compiles the W33 paper, Photonic Holonet, and machine blueprint PDFs.

Do not merge until the job is green and its artifacts have been inspected.
