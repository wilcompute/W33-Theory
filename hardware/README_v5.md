# Holonet v5 hardware package

This directory contains three mutually checked hardware artifacts:

- `holonet_v5_hybrid_phase.va`: Verilog-A PZT coarse-trim plus Pockels fine-control phase element.
- `holonet_v5_frame_reducer.sv`: synthesizable AXI-style 17-channel time-tag frame reducer.
- `tb_holonet_v5_frame_reducer.sv`: deterministic RTL smoke test.
- `analysis/w33_levi_next5_v5_gds.py`: deterministic valid GDSII reference-floorplan generator. Run `python analysis/w33_levi_next5_v5_gds.py hardware/holonet_v5_hybrid.gds`; CI generates it twice and requires byte-for-byte equality.

The GDS is a reference floorplan, not a tape-out-ready PDK implementation. Waveguide, PZT, electrode, and monitor layers must be remapped and DRC-closed against a selected foundry process.
