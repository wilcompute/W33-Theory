# BT1823-BT1827 Execution Summary

## BT1823

`analysis/w33_packet_vm_kernel.py` now imports `bt1818_compiled_packet_kernel_controller` and uses `CompiledInterruptController`, a subclass of the Pass-64 interrupt controller. Relocations retain the cheapest edge target but now record compiled phase-row selection by counter modulo 3.

## BT1824

`analysis/bt1824_executable_packet_replay.py` runs the seeded controller and compiled controller over the same 1600-input TritCPU router workload and writes `data/PART_BT1824_EXECUTABLE_PACKET_REPLAY_results.json` when executed.

## BT1825

`analysis/bt1825_aperture_shot_table_exporter.py` exports the full 1440-row aperture readout table with center, phase, striation, aperture point, safe triad, target contextual fraction, and blank observed columns.

## BT1826

`docs/BT1826_holonet_theorem_ledger_mainline_patch.md` records the ledger rows that extend the BT1807-BT1816 block with BT1823-BT1825.

## BT1827

`holonet_machine.tex` now contains a `Compiled defect runtime stack` result connecting the TD(4,3) escape surface to the three-slot scheduler, fixed-edge run law, nine-point cache law, and aperture readout skeleton.

## Honest boundary

The kernel source is patched, and the executable replay/exporter scripts are present. Full CI and full host replay were not run inside this connector pass.
