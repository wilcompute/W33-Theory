# Holonet v5 hardware package

This directory contains four architecture-level artifacts with deliberately
different evidence levels:

- `holonet_v5_hybrid_phase.va`: a hand-written, foundry-neutral Verilog-A interface model. CI checks its static parameter/interface contract; it does not run a Verilog-A or PDK simulator.
- `holonet_v5_frame_reducer.sv`: SystemVerilog for a 17-channel AXI-style frame reducer with completed-frame count and overflow snapshots.
- `tb_holonet_v5_frame_reducer.sv`: a two-frame RTL smoke test that holds a completed summary under backpressure and checks zero-based frame numbering.
- `analysis/w33_levi_next5_v5_gds.py`: a deterministic GDSII record/placement-sketch generator. Run `python analysis/w33_levi_next5_v5_gds.py hardware/holonet_v5_hybrid.gds`; CI generates it twice, parses its record envelope, and requires byte-for-byte equality.

The GDS contains reference rails and PZT/EO/monitor placement rectangles. It
contains no routed couplers, functional MZIs, optical ports, PDK layer map,
parasitic extraction, or DRC closure and is not a tape-out candidate. The
85.607097 mW figure is an architectural allocation, and the reported corner
fidelities are fixed-seed phase-error simulations rather than measured yield.
The mathematical mesh compiler emits 376 phase commands, while the sketch has
120 abstract interferometer slots; this package does not yet provide the
command-to-electrode netlist needed to claim they are one implemented manifest.
