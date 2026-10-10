# Passes 2967–2973 observable evidence request

This branch exists only to retain observed toolchain evidence for the source-complete packet on `master`.

The dedicated workflow must establish:

1. the exact/modelled Python generator reports `PASS 7 / 7`;
2. all focused regressions pass;
3. the nine-gate M36 microcode and D12 curvature-clock RTL testbenches pass under Icarus;
4. both RTL datapaths synthesize and place on HX8K, with logs retained;
5. blueprint and site integration are idempotent;
6. the W33 paper, Photonic Holonet, and machine-blueprint PDFs compile;
7. artifact hashes and observed logs are committed back to this branch.

Do not infer laboratory calibration, optical locality, autonomous-clock behavior, or physical reset energy from a green digital workflow.
