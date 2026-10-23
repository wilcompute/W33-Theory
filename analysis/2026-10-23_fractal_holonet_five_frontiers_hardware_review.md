# Fractal Holonet engineering pass — five tracks, physical boundaries, and reproducible certificates

**Date:** 23 October 2026  
**Repository:** `wilcompute/W33-Theory`, master  
**Evidence level:** mathematical identities, Python simulation, SystemVerilog RTL simulation, and generic GDSII geometry. **No foundry PDK, quantum-optical experiment, timing-closed FPGA, or fabricated chip.**

This pass extends the 40 four-port W33 line-bus architecture implemented in `analysis/w33_fractal_linebus_switch_matrix_20261023.py` and `analysis/w33_linebus_xor2_photonic_compiler_20261023.py`. Existing geometric facts (40 W33 lines and earlier matching schedules) are not claimed as novel.

## 1. XOR versus Walsh PIC trade study and GDS reference

`analysis/w33_pic_xor_walsh_pareto_20261023.py` simulates both exact four-state bus implementations:

[
P_m = (H_2\otimes H_2)D_m(H_2\otimes H_2)
]
and the earlier two-stage four-MZI implementation (U_m=i^{\mathrm{popcount}(m)}P_m), with its scalar frame corrected.

A **generic**, process-neutral GDSII file and SVG preview are generated in `hardware/generated/w33_40bus_switch_ref_20261023.gds` and `hardware/generated/w33_40bus_switch_ref_20261023.svg`. They contain 40 XOR macro references, a Walsh comparator macro, 0.5 μm nominal reference rails at 20 μm spacing, symbolic MZI and passive-coupler footprints, and **explicit layer-99 markers for unrouted stage-2 nonadjacent mode couplings**. A GDSII read/write round trip succeeded. The GDS is 7,100 bytes. Optical netlist connectivity is **incomplete**; no PDK, DRC, LVS or photonic functionality has been signed off.

The seeded, independently generated Monte Carlo study imposes 0.06 rad Gaussian control errors, 1,600 synthetic evaluations per architecture:

| Metric | Four-MZI XOR | Fixed Walsh + binary phases |
|---|---:|---:|
| Mean normalized unitary overlap | 0.998210 | 0.997363 |
| 5th-percentile overlap | 0.995763 | 0.993010 |
| Mean worst-port wrong-output probability | 0.002910 | 0.002637 |

These are not comparable production yield metrics; the assumed error mechanisms differ. Three illustrative loss scenarios reverse which architecture is preferred. **Neither design wins without a process-specific component loss, power, area and thermal calibration budget.**

## 2. Two-arm coherent-photon interference

`analysis/w33_fractal_timing_optimal_interference_20261023.py` exhaustively checks all **3,240** unordered pairs of two-hop W33 routes between nonadjacent endpoints under the three-slot global switch schedule. It finds **192 pairs** with equal modeled arrival times and a nontrivial modulo-four optical phase difference.

A particularly useful early witness is:

- Arm A: **4 → 5 → 19**
- Arm B: **4 → 11 → 19**
- Both arrive at discrete tick 4 from tick 0.
- Both require **two WAIT slots**, which are not a physically demonstrated delay or quantum memory.
- Ideal switch phase-frame ratio: **i**.

A separate no-wait obstruction holds in this exact model: if both two-hop routes are executed in the same two consecutive global slots, the mandatory switch masks are identical by slot, hence their ideal scalar (i)-phase products are identical. **Nontrivial phase contrast is impossible for such an entirely wait-free two-hop interferometer.**

For a laboratory implementation, time alignment is only one necessary condition. Must also characterize continuous optical carrier phase, photon wavepacket overlap, delay-line loss, dispersion, switch settling, source indistinguishability and measurement SPAM. No photon data were acquired.

## 3. Verified RTL phase-frame controller

The existing `hardware/w33_linebus_phase_frame.sv` implements the recurrence

[
e_{t+1}=\bigl[(\mathrm{clear} ? 0 : e_t)+\mathrm{popcount}(m_t)\bigr]\bmod4
]

with ready/valid output and (-e\bmod4) correction metadata. On this pass Icarus Verilog 12 was installed on the authorized development machine and **used to compile and actually simulate** both:

- `hardware/tb_w33_linebus_phase_frame.sv`: directed test **PASS**. A stale asserted clear signal in the original stimulus was identified and fixed.
- `hardware/tb_w33_linebus_phase_frame_random_20261023.sv`: 1,500-cycle pseudorandom scoreboard **PASS**, with **493 accepted commands and 507 stall observations**.

This establishes simulation agreement, not synthesis, place-and-route, timing closure, output electrical pad delays, optical actuator timing, or any FPGA deployment. The simulator is not the photon channel. A metadata frame is not automatically a physical optical phase correction.

## 4. Timed multi-commodity demand and fault capacity

`analysis/w33_fractal_multiuser_linebus_capacity_20261023.py` reserves unique undirected physical-neighbor pair IDs per global slot for deterministic classical demands, delaying launch to avoid occupied links. A link-bus failure excludes all of its affected neighbor pairs. Every WAIT is flagged as an **unimplemented quantum-memory obligation**.

Using 90 requests, a deterministic seed and a finite launch-slip horizon, the greedy planner delivered all 90 demands in all four tested cases:

| Scenario | Delivered | Mean postponed launch, slots |
|---|---:|---:|
| Baseline | 90/90 | 0.1778 |
| Failed line bus 0 | 90/90 | 0.1889 |
| Final phase frame constrained to 0 | 90/90 | 0.4111 |
| Failure and zero-frame constraint | 90/90 | 0.4667 |

The planner is **not an optimal multi-commodity flow proof** and does not model photon storage, coherent queuing, bandwidth, real switch-settling, sources, detector dead time or higher-level packaging. As demand increases, link occupancy and latency must be evaluated together.

## 5. Three-mode qutrit Fourier processing tile

`analysis/w33_fractal_qutrit_F3_tile_drift_20261023.py` reconstructs the ideal four-mode target (operatorname{diag}(F_3,1)) using **three complex two-mode Givens blocks** and four terminal phases. The ideal Frobenius reconstruction error is approximately **4.19 × 10⁻¹⁶**. The auxiliary fourth mode is isolated in the ideal circuit.

A seeded 180-trial-per-setting coherent-error surrogate gives:

| Gaussian phase sigma | Mean unconditional (F_3) overlap | Mean worst-basis auxiliary leakage |
|---|---:|---:|
| 0.00 rad | 1.000000 | 0 |
| 0.01 rad | 0.999872 | 0.00000332 |
| 0.05 rad | 0.997271 | 0.0000801 |
| 0.10 rad | 0.987076 | 0.000388 |

This model introduces deliberately weak unwanted coupling between mode 2 and the auxiliary mode. The statistics are hypothetical, not actual photonic-gate fidelity. An arbitrary nonidentity four-port XOR permutation is not a deterministic operation on the naive three-mode qutrit subspace, because its 3×3 compressed block has singular values (1,1,0). Thus the qutrit processor **must remain a separately characterized subsystem**.

## Reproduce

```powershell
$env:W33_GDSTK_PATH = 'C:\Temp\w33_gdstk_isolated'
py analysis/w33_pic_xor_walsh_pareto_20261023.py
py analysis/w33_fractal_timing_optimal_interference_20261023.py
py analysis/w33_fractal_multiuser_linebus_capacity_20261023.py
py analysis/w33_fractal_qutrit_F3_tile_drift_20261023.py
py -m pytest -q tests/test_w33_pic_xor_walsh_pareto_20261023.py tests/test_w33_fractal_five_frontier_extension_20261023.py
& 'C:\iverilog\bin\iverilog.exe' -g2012 -s tb_w33_linebus_phase_frame_random -o 'C:\Temp\w33_frame_random.vvp' hardware/w33_linebus_phase_frame.sv hardware/tb_w33_linebus_phase_frame_random_20261023.sv
& 'C:\iverilog\bin\vvp.exe' 'C:\Temp\w33_frame_random.vvp'
```

The `gdstk` dependency was installed in **an isolated temporary target directory** on the connected machine, not assumed as a repository-level PDK. GDS file and SVG are **reference geometry only**. For a true PIC, choose a licensed foundry PDK, instantiate process-characterized couplers, route the interstage crossed paths, assign electro-optic actuation and detectors, simulate the full S-parameters, perform DRC/LVS, and measure physical transfer matrices.

**Selected external context:** gdsfactory's PDK methodology (<https://gdsfactory.com/plus/v2/gdsfactory/notebooks/08_pdk/>) and an experimental electro-optically programmable four-mode PIC in *Physical Review Research* 5, 033206 (2023), DOI:10.1103/PhysRevResearch.5.033206. Those published device measurements are not measurements of the Holonet.
