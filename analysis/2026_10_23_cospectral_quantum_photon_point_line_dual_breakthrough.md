# W33/Q(4,3) duality as a photon phase-oracle circuit resource

**23 October 2026 — verified computational research, no physical photon experiment**

## Executive finding

Two nonisomorphic point collinearity graphs of generalized quadrangles of order (3,3) have **identical complex two-register single-photon mode-state Schmidt spectra**. A real local orthogonal transformation maps one state to the other, so *no unrestricted local-unitary entanglement measure* distinguishes them. Their restricted computational-address controlled-sign phase-oracle implementations have different provably minimal GF(2) nonlocal ranks: W(3,3) has **14 terms/seven hyperbolic pairs**, Q(4,3) has **8 terms/four hyperbolic pairs**, after free local one-body diagonal phase corrections.

The binary adjacency 2-rank separation (W=16, Q=10) is **prior art** (repo Pass 88 and older coding-theory papers), not discovered here. The circuit application uses ordinary finite-field rank and alternating-form elimination. All 1,600 phase entries have exact certificates.

## The architecture link that changes the engineering question

The existing W33 photonic blueprint has 40 four-port **line buses**, not merely 40 abstract point modes. Enumerating the W33 line set and connecting intersecting lines constructs the Q(4,3) point graph by generalized-quadrangle point/line duality. This was verified by a complete 40-vertex graph isomorphism, and the permutation from W33 native bus IDs to independently constructed Q(4,3) vertex labels is frozen in `data/w33_linebus_dual_q43_phase_geometry_20261023.json`.

Thus *the line-bus address space already has the Q graph*, and the cheaper rank-eight phase oracle is a real potential compiler target for the existing 40-bus addressing topology. Intersecting abstract W33 lines are not automatically connected optical waveguides, and nothing here implements the physical controlled phase.

## Distinguish state resources, restricted circuit resources and true hardware resources

For `C=(J-2A)/40`, both geometries have Schmidt probabilities `0.16 x1, 0.04 x15, 0.01 x24` and entropy `4.803856189774729` bits. For the same graph-controlled phases in an n=4 chain, an exact integer contraction of the noncontiguous even-odd cut `(a,c)|(b,d)` gives purity `0.0020128` **for both**: this test does not distinguish the geometries.

For the *computational-basis, locally sign-corrected binary parity-product* phase oracle, double-centering `B_{a,b}=A_{a,b}+A_{a,0}+A_{0,b}` gives W rank14 and Q rank8. These are optimal within **that specified term model**. Arbitrary orthogonal 40-mode mixing, different optical gate libraries, electronic address decoding and signal integrity break any inference that 8 physical gates outperform 14 physical gates.

## Four measured-by-tools electronic controller implementations

All four were synthesized and routed with YoWASP Yosys and nextpnr for the **unconstrained iCE40UP5K SG48 reference**, with the same nominal 24 MHz request and seed 20261023. Each Q variant passed Icarus on all 1600 valid + 2496 invalid address pairs.

| Registered classical controller | Cross terms | Yosys LUT4 | UP5K LCs | I/O |
| --- | ---: | ---: | ---: | ---: |
| W33 point-address rank14 | 14 | 172 | 182 | 34 |
| Q43 independent canonical vertex IDs rank8 | 8 | 115 | 125 | 28 |
| Q43 rank8, runtime translate native W33 bus IDs | 8 | 175 | 185 | 28 |
| Q43 rank8, **compile-time relabel directly in W33 bus IDs** | 8 | 106 | **116** | 28 |

Thus the naive runtime graph-isomorphism address translator costs **69 extra logic cells** versus the direct bus lookup, eliminating the raw Q oracle advantage. The compiler-time translated version needs 116 LCs, 66 fewer than W33's 182 (36.26% fewer in these reference implementations). This is a *real electronic logic and routing comparison* but **not a validated clock speed**: nextpnr reports **No Fmax available; no interior timing paths**, and all I/O pins are unconstrained and automatically assigned. These logic circuits produce classical sign metadata, **not coherent quantum gates**.

The PowerShell builder `hardware/build_w33_q43_dual_linebus_UP5K_20261023.ps1` was actually executed end-to-end and passed, including all three Q Icarus exhaustive simulations and Yosys/nextpnr reference routes. Complete compressed netlists and unpinned place-and-route outputs of the Q canonical, runtime remap and native direct variants are in `data/`; SHA256 and resource counts are in `data/w33_q43_dual_linebus_phase_oracle_hardware_verified_20261023.json`.

## Tests, proof and scope

A selected integrated suite spanning the older W33 photonic models, self-entanglement/time-bin recursion, W33 rank14 and the new cospectral/dual Q variants returned **68 passed**. This is **not** a whole-repository test run. The 4096-address HDL tests were performed independently and are not counted as Python tests.

The standalone mathematical and hardware manuscript is `papers/w33_q43_cospectral_photon_entanglement_20261023.tex`. Its proof establishes exact local real-orthogonal state equivalence and optimal cross rank in the declared restricted phase gate family. It contains the explicitly negative n=4 cut purity result and the W33 bus-Q43 isomorphism. The TeX is a source document, not a compiled or peer-reviewed physical paper.

No results demonstrate a real photon self-entangled with its own past, retrocausality, quantum memory, a manufactured PIC, or a fundamental theory of everything.

## Independent follow-up directions

1. **Physical phase-oracle circuit**: Implement and calibrate a single directly indexed Q43-on-W33-line-bus phase primitive using a foundry PDK; measure actual power, crossings, phase stability and latency versus W33 point-control.
2. **Geometry beyond entropy**: Build an operator-sensitive two-qutrit Pauli contextuality test distinguishing the symplectic W33 point geometry from its line-intersection dual without depending on a choice of arbitrary 40-mode basis.
3. **Multipartite cospectral discrimination**: Derive higher Rényi moments, noncontiguous partition spectra, or multi-time process observables of 4+ address factors; record negative results as rigorously as positive ones.
4. **True temporal quantum memory**: Embed independently addressable path/time qudits and a reference photon into a causal-break protocol; require actual tomography, single-photon source validation, and memoryless controls.
5. **Electronics/electro-optics integration**: Choose a real FPGA board and PDK, provide an approved PCF and actuator interface, then characterize post-register control latency. Do not infer a usable clock frequency from current unconstrained runs.

## Outside-the-box physics questions (hypotheses, not evidence)

- Could the finite-field *point/line duality* appear as a measurable choice of quantum operator algebra, not just an address relabeling? One must introduce actual noncommuting operator preparations and contextuality witnesses.
- Is there a fault-tolerant encoding of the **eight-term line-dual** and **fourteen-term point** phase information with shared error syndrome resources? Compare exact quantum code distances and distinguish classical control circuits from logical quantum gates.
- Can a *recursive path/time address* implement the required phase terms with fewer distinct optical modes using time multiplexing and a real quantum memory? Track the memory survival probability, detector inefficiencies, mode distinguishability and no-cloning restrictions before claiming scaling benefits.

**References:** prior project Pass76/88, W33 optical 40-line bus manifest, binary p-rank literature, and Godsil–Royle finite-field rank/symplectic form context. Prior 40-point construction and binary rank values are established, whereas the directly verified photonic-computer control compilation is the project-specific contribution.
