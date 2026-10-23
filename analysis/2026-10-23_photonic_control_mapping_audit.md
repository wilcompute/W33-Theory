# Photonic systems audit — 2026-10-23

## Decision

The original suggestion to map **376 angles directly to electrodes** is too early and overstates hardware degrees of freedom. The actual v5 Givens basis uses 120 three-angle SU(2) matrices and 16 diagonal phases; a propagating diagonal gauge eliminates 120 redundant angles, producing an exactly equivalent **256-coordinate abstract U(16) control network**. The special upstream target is real orthogonal, making the reduced phase values 0 or pi while retaining 120 nonzero mixing angles. None of these counts certifies a physical number of electrodes: the phase-to-actuator factorization, layout, and electrical IO remain unspecified.

The better immediate deliverable for photonic-IC engineering is an **executable, traceable optical/electrical schematic contract with gauge-correct control semantics and a phase-identifiability test**, followed by a real PDK-backed reduced test cell. This release implements the abstract-contract portion, not the PDK-backed test cell.

## Primary source audit

- `papers/forty_points/main.pdf`: 202 pages, examined by full-page text extraction and topical section/page review. Printed page 131 explicitly states the integrated device has **not been built**; it separates prior-art measured SUM gates from project-specific specification and mathematical verification. Printed pages 131–134 list remaining physical and dynamical gaps. This paper has no electrode layout or optical-waveguide PDK bill of materials.
- `papers/forty_points/main.tex`, `sec03_selfentangle.tex`, `sec04_time.tex`, `sec05_e8.tex`, `sec09_physics.tex`, `sec10_machine.tex`: programmatic full-text terminology audit; these sections are mathematical and architecture-level context, not mask layout.
- `photonic_holonet_body.tex` and `holonet_machine_blueprint_body.tex`: searched for device, phase, timing, waveguide, measurement and actuator scope. Substantial machine architecture work precedes this pass.
- The last-seven-days Git history through the observed 23 October master contained **374 commits**, indexed by SHA/date/subject/changed paths. This is a complete commit-index scan, **not a claim that every diff was manually read**. We inspected the photonic-specific changes, especially 21–22 October passive surrogates and optical loss limitations.

## Prior engineering work that changes the direction

- v2 (`analysis/w33_levi_next5_v2_photonic.py`) already produced a 16-mode Halmos dilation and 120 two-mode mathematical rotations. A new decomposition should reuse, not overwrite, that foundation.
- v3 (`analysis/w33_levi_next5_v3_tolerance.py`) addressed synthetic phase/drift/extinction/jitter, not measured loss or wafer corners.
- v4 (`analysis/w33_levi_next5_v4_foundry.py`) studied a foundry-targeted 16-mode mesh and numerical calibration; these are modeled assumptions.
- v5 (`analysis/w33_levi_next5_v5_hybrid.py`) exposed the 376-angle representation, 16-bit quantization and hybrid PZT/EO architecture. The associated `hardware/README_v5.md` explicitly says the GDS contains **no routed couplers or functional MZIs, optical ports, PDK layer mapping, DRC closure, parasitic extraction, or terminal 376-to-device manifest**.
- October 21 commits (including `ccbcd72cab` and `d945dbe22f`) prove signed shift surrogates can be passive-unitary but the raw weighted Frobenius companions are **nonunitary in standard optical amplitudes**. Conflating them would be a serious design error.
- October 17 TOE95 calibration explicitly notes 40 four-mode control settings, trusted basis probes, drift assumptions and the prohibitive worst-case zero-error calibration shot count; a power-only measurement is not interchangeable with phase tomography.

## New exact and falsifiable results

1. The identity `G(theta,phi,alpha) = D(alpha)R(theta,phi)` plus the commuting rule `P R^H(theta,phi) = R^H(theta,phi+delta_i-delta_j) P` defines an exact all-gate reduction.
2. Full 16-mode synthesis using 120 two-mode blocks and a rightmost 16-phase diagonal reproduces the original v5 synthesized matrix within numerical floating precision. **The rightmost diagonal acts at the physical input** under a column-vector convention, regardless of the upstream variable name `output_phases`.
3. Every gate is assigned two logical optical inputs, two logical outputs, two logical control IDs and two virtual driver IDs; each of 16 input-phase cells has one virtual driver ID. All 256 are unique and the connected 16-rail path is checked.
4. A two-balanced-coupler identity provides an independent algebraic surrogate `R^H = D(gamma) H D(theta) H D(-gamma)` with `gamma=(phi+pi/2)/2`. This is **not** a fabricated two-electrode MZI.
5. The basis-input intensity map is invariant under the 16-dimensional rightmost input phase bank. One perturbed input phase changes the **complex** transfer matrix without changing any of the 16x16 basis-input output powers. Stable coherent reference and a measured sensitivity Jacobian are therefore part of the instrument specification.

Reproduction: `py analysis/w33_photonic_control_netlist_20261023.py` and `py -m pytest -q tests/test_w33_photonic_control_netlist_20261023.py`.

## Engineering requirements and measurement gates

- Netlist: implement a real optical/electrical PDK component hierarchy, including named port orientation, waveguide bends/crossings, MZI splitting conventions and buffer/tap insertion. The old abstract GDS placement **cannot** be identified directly with the serialized Reck sequence without proof.
- Actuation: measure phase-voltage behavior and thermal/EO cross-talk; derive electrode/control sensitivity and rank. The 256 mathematical control coordinates are **not** 256 certified pads or DAC outputs.
- Metrology: classical coherent transfer matrix, controlled phase perturbations, stable LO reference, complete SPAM assumptions, loss/dispersion bounds; then separate heralded single-photon and correlation protocols.
- Foundry: choose an authorized PDK, verify connectivity and DRC, do electrical LVS and optical extraction, produce actual packages and electrical interfaces.
- Portfolio: first target a tractable 2-mode or 4-mode demonstrator while retaining the 16-mode mathematical manifest for scaling.

## Outside comparison

- AIM Photonics low-loss PDK documents supported materials, layers and tools: https://www.aimphotonics.com/low-loss-pdk
- GDSFactory PDK methodology distinguishes component libraries, layers, and verification decks: https://gdsfactory.github.io/gdsfactory/notebooks/08_pdk/
- Zheng et al. (2024), *Global calibration of large-scale photonic integrated circuits*, https://arxiv.org/abs/2407.02207, describes simultaneous phase/current learning and splitter characterization.
- Elmas et al. (July 2026), *Local Variance-Based Calibration of Programmable Photonic Interferometer Meshes*, https://arxiv.org/abs/2607.14759, describes experimental intensity-variance calibration in an 8x8 processor.
- These literature experiments are **not** results from W33.

## Release evidence boundary

This packet advances a logical schematic/measurement protocol and a new living LaTeX atlas, not a manufactured photonic integrated circuit. It does not prove physical quantum universality, implemented fault tolerance, photon self-entanglement, or a theory of everything. The original v5 target residual (~5.44e-9) is inherited; the new gauge equivalence is tested more tightly. Exact physical actuator count remains open.
