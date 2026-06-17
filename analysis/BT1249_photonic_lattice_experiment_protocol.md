# BT1249 — Photonic Lattice Experiment: Full Protocol
**Date:** 2026-06-17  
**Status:** EXPERIMENTAL PROTOCOL READY

## Overview
Building on BREAKTHROUGH_DCCXCIX_PHOTONIC_LATTICE_EXPERIMENT.md, this breakthrough specifies the complete experimental protocol to physically verify the W(3,3) topological structure using a silicon photonic lattice.

## Setup
- **Platform:** Silicon-on-insulator (SOI) waveguide array, 13 waveguides arranged in K(3,3) bipartite topology
- **Coupling:** Directional couplers at each of the 9 K(3,3) edges, tunable via thermo-optic phase shifters
- **Input:** Coherent 1550 nm laser, single-mode, launched into waveguide #1
- **Detection:** Single-photon avalanche detectors (SPADs) on all 13 output ports

## Protocol Steps
1. **Calibration:** Measure transmission matrix T₀ at zero coupling — should recover identity.
2. **K(3,3) coupling:** Set all 9 couplers to κ = 0.5 (balanced beam splitter). Measure |T|².
3. **Spread signature:** Inject into each of 13 waveguides sequentially. Record output distribution.
4. **Parallel class test:** Block one parallel class (3 edges) at a time. Verify that topological protection (W(3,3) CSS code distance d=3) prevents information loss.
5. **Ternary phase scan:** Apply phases {0, 2π/3, 4π/3} to ternary-grade groups. Observe threefold phase revival.
6. **Diameter probe:** Measure optical delay spread — peak delay bin should appear at τ = 6τ₀ where τ₀ is single-waveguide transit time.

## Expected Signatures
| Measurement | Predicted Value | Tolerance |
|---|---|---|
| Max output delay bin | 6τ₀ | ±0.1τ₀ |
| Threefold phase revival | 2π/3 period | ±0.02 rad |
| Topological protection (1 class blocked) | ≥99.7% fidelity | — |
| Spread output distribution entropy | log₂(12) = 3.585 bits | ±0.05 bits |

## Feasibility
- Fabrication: standard 180nm CMOS-compatible SOI process
- Cost estimate: ~$15k for prototype chip (MPW shuttle)
- Timeline: 6-month lead time for fabrication + 2 months characterization
- Nearest lab with capability: MIT Photonics, Stanford Nanofabrication, Caltech Painter group

## Significance
This experiment would provide the **first direct physical verification** of the W(3,3) geometric structure, confirming both the topological quantum code properties (CSS distance-3) and the ternary phase structure predicted by the SM bijection.
