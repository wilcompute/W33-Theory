# W33 phase-oracle hardware and temporal quantum-memory research pass
**Date:** 2026-10-23  
**Repository:** wilcompute/W33-Theory  
**Scope:** five independent follow-ups after the recursive self-entanglement area-law result. Mathematical proofs, NumPy regressions, optical target circuits and a fail-closed FPGA integration contract. Not a fabricated photon machine.

## Executive result

The W33 adjacency is a **known** binary-rank-16 matrix: `w33_pass88_smith_group.py` explicitly records this rank, and `analysis/w33_20260829_adjacency_sentinel_extension.py` analyzes its codimension-one sentinel subcode. **We do not claim to discover this rank.**

The new application is an exact phase-oracle circuit for the hypothetical two-register W33-controlled sign `(-1)^A[a,b]`. A 16-factor GF(2) bilinear decomposition was constructed and tested against all 1,600 truth-table entries. More strongly, allowing independently programmed one-register diagonal phase tables reduces the optimal nonlocal bilinear rank to **14**, represented naturally by **seven hyperbolic/symplectic pairs**. The computational win is in *logical cross-register parity-product terms*, not in demonstrated optical cost or a physically realized photon-photon interaction.

## Front 1 — Nine-mode quantum eraser and actual null

A single photon with separable factors 3 path modes × 3 temporal modes can be prepared in `|+_3>|0>`, evolved by a controlled time translation `|a,t> -> |a,t+a (mod 3)>`, and analyzed with two `F3†` decoders. The implementation uses an **explicit 9×9 permutation unitary** and density matrices; it does not substitute numerical entanglement claims for a circuit.

For the fully coherent path-time state:
- `P(time-Fourier output 0)=1/3`;
- `P(path-Fourier output 0 AND time output 0)=1/3`;
- `P(path output 0 | time output 0)=1`.

For a deliberately dephased mixture with **identical computational-basis populations**, those three numbers are `1/3`, `1/9`, and `1/3`. Partial off-diagonal coherence `μ` gives a conditional result `(1+2μ)/3`. This is a falsifiable interferometric contrast, but it is not automatically single-photon nonclassicality: require a verified `g²(0)` source characterization, operational path/time observables and calibrated detector counts. Classical vector-wave mode correlations can reproduce some first-order fringe responses.

**Physical blocker:** coherent nine-mode source, delay interferometers, real complex transfer matrix, verified photon statistics and lab measurements are absent.

## Front 2 — A provably minimal *logical* W33 cross-register phase network

Let `A` be the 40×40 W33 adjacency matrix over GF(2), with known rank 16. Choosing W33 address zero as the reference, define

`B[a,b] = A[a,b] XOR A[a,0] XOR A[0,b] XOR A[0,0]`.

Here `A[0,0]=0`, and `B` is alternating: symmetric, zero diagonal and **rank 14**. An exact compiled factorization `B=LRᵀ (mod 2)` with `L,R` of shape 40×14 satisfies

`A[a,b] = A[a,0] XOR A[0,b] XOR XOR_k (L[a,k] AND R[b,k])`.

This implements the desired `(-1)^A` sign as **14 cross-register parity-product controlled phases**, plus **two local single-register phase lookup tables**, with flag compute/uncompute.

**Optimality proof within the declared gate family:** For *any* local phase corrections `u[a]+v[b]+g`, the double-centered matrix remains B. Double-centering is multiplication by fixed binary row/column maps, so `rank(B) ≤ rank(A+u1ᵀ+1vᵀ+gJ)`. The compiler attains rank(B)=14. Thus no 13-term binary bilinear *cross-register parity-product* representation can implement this family up to local diagonal phases. All 40 reference addresses and 32 random local phase compensations were checked.

Because B is alternating, the exact algorithm further produces

`B=Σ_{k=1}^7 (x_k y_kᵀ + y_k x_kᵀ)`.

This is **seven symplectic pairs / fourteen directed cross terms**. W33's rank-16 and its sentinel code are prior repo results; the W33-specific optical oracle, local-gauge reduction and executable seven-pair witness are the engineering deliverables of this pass. The alternating bilinear-form decomposition itself is standard finite-field linear algebra.

**Physical blocker:** Address-dependent reversible lookup, nonlinear or effectively controlled phase interaction, waveguides, optical power, actuator count and calibration all remain unbuilt. In particular, 14 is **not** the MZI count or a deterministic two-photon entangler.

## Front 3 — Non-nearest recursion and when the W33 area law breaks

For the nearest-neighbor 40-ary controlled-phase chain, each contiguous cut crosses one independent W33 interaction, so the exactly proven Schmidt entropy is `H_W33=4.803856189774729` bits (40 Schmidt values).

Add long-range interactions:
- **Four address digits**, with just the crossing phase edge (1,2), have Schmidt rank 40 and entropy `H_W33` across `01|23`.
- Add two independent crossing edges (0,2) and (1,3) with no other interactions. The cross-cut coefficient matrix is a Kronecker product of two W33 kernels; hence Schmidt rank **1600** and entropy **2 H_W33 = 9.607712379549458 bits** (small rounding differences come from floating-point SVD).
- A three-address `0–1, 0–2` two-spoke model is also evaluated via an exact 40×40 reduced Gram construction.

This is a mathematical counterexample to *universal* depth-independent entanglement: the previously reported area law is specifically a nearest-neighbor geometric cut result, not a restriction on arbitrary recursive nonlocal couplings.

**Physical blocker:** 40-valued tensor factors and distant cross-register phase control are not implemented in the optical apparatus.

## Front 4 — FPGA: fail-closed board pin contract

The existing recursive time-bin metadata RTL was previously simulated over 2,000 cycles and synthesized/placed/routed on an unconstrained iCE40UP5K target. The authoritative **post-route** timing estimate was 68.82 MHz (24 MHz target passed) and 42 logic cells. Earlier 75.45 MHz was a preliminary placement estimate, not the post-route result.

Repository inspection found **no tracked .pcf or .xdc board pin constraint files** for a real target. Instead of inventing a board pinout, the new code parses the actual Yosys netlist and enumerates **25 I/O bit ports** in a manifest with **all pin assignments explicitly unassigned**. It fails closed until an operator supplies a real board identity, documentation fingerprint, voltage-domain statement, every uniquely assigned set_io pin and approval. The 25-port manifest and PCF parser are regression-tested with **synthetic** metadata to test errors (duplicate, missing, unmatched ports). Passing those tests does not validate physical pad legality or electrical safety.

**Physical blocker:** No confirmed board datasheet or board-specific PCF, optical detector drivers, phase actuators, board clock and timing constraints. This track is an integration contract rather than a deployed FPGA.

## Front 5 — Causal-break temporal quantum memory, not retrocausality

A three-qutrit forward-time experiment has an actual accessible reference `R`, system `S`, and memory environment `E`. Start `RS` maximally entangled, `E=|0>`. A first SWAP `S↔E` moves the system's quantum information into E. A genuine causal break completely traces out S and independently prepares `|0>` on S. A second SWAP `S↔E` restores the original system information.

- Keeping E intact retains **RS negativity 1**, demonstrating perfect idealized quantum-reference recovery after the system causal break.
- Resetting E at the break gives **RS negativity 0**, the memoryless control.
- A coherent `|+_3>` probe returns Fourier-plus probability **1** with E retained; a dephased probe with identical computational populations gives **1/3**, whereas resetting E gives **1/3** for both.

This distinguishes **physically accessible quantum environmental memory** from the merely mathematical input/output entanglement of a Choi vector. The full experiment must physically supply R and E, controllable SWAPs, complete system trace-and-reprepare and entanglement tomography; this program is a model of those operations, **not** a full reconstructed process tensor or empirical demonstration of quantum memory. No signal to the past exists in this causal circuit.

## Verification and reproducibility

New scripts:
- `analysis/w33_photonic_five_fronts_GF2_phase_causal_break_20261023.py`: nine-mode circuit, raw rank-16 oracle, long-range recursion, RS/E memory test.
- `analysis/w33_phase_oracle_mod_local_gauge_rank14_20261023.py`: optimum modulo local diagonal phases, all 1,600 pairs, all 40 anchors.
- `analysis/w33_phase_oracle_seven_symplectic_pairs_20261023.py`: seven-pair constructive alternating decomposition.
- `analysis/w33_timebin_UP5K_board_pin_contract_20261023.py`: safe board pin integration gate.

The corresponding tests in `tests/` and frozen JSONs in `data/` are committed alongside this report. An integrated regression suite spanning these new files and previous recursive photon / postselected two-photon modules ran **48/48 passing tests** in approximately 25 seconds on the connected Windows development machine. This does not substitute for the repository-wide suite, optical simulations with measured compact models, or real experimental validations.

**Independent external context:** temporal quantum memory with causal breaks is an established process-tensor technique (e.g. https://www.nature.com/articles/s41534-021-00481-4 and https://doi.org/10.1103/PhysRevX.14.041018). Photonic temporal-mode experiments are established (e.g. https://pmc.ncbi.nlm.nih.gov/articles/PMC12697571/). This pass offers W33-specific exact mappings and protocol models, not claims to have discovered process tensors, finite-field decompositions, or a new physical TOE.
