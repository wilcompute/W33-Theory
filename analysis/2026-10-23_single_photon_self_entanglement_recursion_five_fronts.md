# Self-entanglement, recursion and the five Holonet hardware fronts

Date: 23 October 2026. Repository: wilcompute/W33-Theory. Evidence tiers: exact finite-dimensional mathematics; Python regressions; actual RTL simulation and generic FPGA synthesis/place-route. No photon measurements, PDK signoff, or new physical theory established.

## Central result 1: reused qutrit time bins cycle, they do not grow memory

One photon's path factor has three addresses and the reused temporal factor has three orthogonal bins. The controlled-add operation sends (a,t) to (a,t+a modulo 3). Starting from equal-path-superposition tensor |time0>, rounds one and two produce 1.5849625-bit path/time entanglement and negativity 1; round three restores a product state. The complete cycle repeats every three rounds. This is not backward time travel.

## Central result 2: fresh time registers demand exponentially more modes

Providing genuinely fresh independent time trits gives a GHZ-type one-photon mode state: sum_a |a>path times |a>time1 through |a>timen divided by sqrt(3). The path-versus-all-times entropy remains log2(3) bits at every depth. For n>=2 any path/single-time pair is separable even though the full GHZ state is coherent. Fourier-plus projection of all n time factors succeeds with probability 3^(-n). Conditional path-plus detection is 1 for the coherent state and 1/3 for its equal-population incoherent null. A 3^n-dimensional independent temporal address system and physical source/interferometric controls are required; a three-bin label reused n times is not n independent subsystems.

## Central result 3: input/output Choi entanglement is not an extra photon

For any qutrit unitary channel, including the identity, its normalized Choi vector has maximally mixed input reference and formal entropy log2(3). Recursive compositions U^n do not create a new simultaneous photon or an operational photon-entangled-with-its-past pair. A qutrit dephasing channel composed n times has Choi negativity lambda^n in the specified model. Physical temporal process tests require an accessible reference and causally legitimate operations, not just Choi labels.

## Central result 4: exact W33 graph-phase area law

Take n independently accessible forty-state address factors and the uniform superposition. Apply a conditional minus sign whenever two neighboring address labels are adjacent in the W33 graph. The W33 adjacency spectrum is 12 (once), 2 (24-fold), -4 (15-fold). Across every contiguous cut, local within-half diagonal phases do not affect singular values; the remaining boundary coefficient matrix is (J-2A)/40. Its Schmidt probabilities are 0.16 once, 0.04 fifteen times, and 0.01 twenty-four times. Consequently every cut has rank 40, entropy 4.803856189774729 bits, and purity 0.052, regardless of recursion depth. Explicit depth-2 and depth-3 SVDs and the W33 strongly-regular polynomial were tested. This is an exact mathematical result for a SPECIFIED hypothetical phase-state family. Graph self-similarity alone, without the conditional phase, is a product state and has zero digit entanglement. A physical depth-2 preparation would demand 1600 distinguishable address basis states and pi-phase flips on the 480 ordered W33-adjacent address pairs, not just 40 photonic nodes.

## Five engineering follow-ups

1. PIC: Reused previous four-rail symbolic GDS reference and specified a falsifiable nine-mode (three-path times three-time) photon interferometer. Real PDK, couplers, phase-stabilized delays and DRC/LVS remain unavailable. The larger W33 1600-mode controlled-phase prototype is a research target, not a fabricated circuit.
2. Noise: Reused previous 12-condition correlated-phase model and added coherent-versus-incoherent Fourier quantum-eraser null with loss and detector-efficiency shot counts. For 250000 emitted photons, assumed 0.5 dB loss per step and 78% detector efficiency, at depth 3 the coherent/incoherent expected joint counts are about 5113/1704, and at depth 5 about 451/150, before dark counts. These are synthetic predictions only; they require calibrated source and actual counts.
3. Inter-bus: Checked previous all-780 line-pair four-rail permutations on 160 distinct point-line incidence ports. Even lines intersecting in W33 do not automatically share a physical waveguide. All four optical rails need a physically coherent transfer and synchronized arrival.
4. FPGA: Added a SystemVerilog recursion-guard metadata module, 2000-cycle Icarus randomized scoreboard passing with 676 accepted commands, 665 stalls, 254 fresh-register obligations, 246 reused-delay requests, and 176 invalid path codes. Yosys plus nextpnr iCE40UP5K reference placement used 42 LCs and 25 IO resources; post-route estimated Fmax is 68.82 MHz, PASS at 24 MHz. Earlier 75.45 MHz was a preliminary estimate, not the final routed result. There is no board PCF or physical photon storage.
5. Two photons: Rechecked the separate two-boson eight-rail postselected entangled-state generator. Its ideal code-postselected probability is 0.5 and conditional negativity 0.25; output photon coincidence is destructive and therefore not a reusable entangling gate. A single photon's mode-factor nonseparability cannot automatically replace it.

## Physical falsifiers

A credible experiment needs a heralded/characterized single-photon source with an antibunching measurement, independent path/time mode controls, a Fourier-time decoder, path coherence tomography, calibrated differential phase noise, and an incoherent mixture control. First-order interference alone can have classical vector-wave analogues. For the recursive W33 phase model, full digit-local preparation/measurement and a genuine 40x40 adjacent-digit conditional-phase circuit are prerequisites. An observed departure from a three-cycle revival should first be tested against loss, phase noise, mode mismatch and detector effects.

## Source and prior-art pointers

- BT1556 and BT1569 project notes: source self-entangled Choi interpretation and placeholder symbolic tests.
- BT1700 recursive packet compiler: 40^n address count and 72*40^n abstract ABI ticks; not physical pulse time.
- Single-photon path/mode entanglement prior experiments: https://arxiv.org/abs/1407.0144
- Quantum versus classical nonseparability: https://doi.org/10.1098/rsta.2023.0342
- Genuine entanglement in time/process tensor context: https://doi.org/10.21468/SciPostPhys.10.6.141
- Review of energy-time and time-bin entanglement: https://www.nature.com/articles/s41534-025-01072-3

Reproduce with the three new analysis scripts and three new pytest modules ending _20261023.py, as well as the Icarus testbench and the iCE40UP5K build commands. JSON certificates are under data. Nothing here demonstrates a theory of everything, physical self-interaction with the past, or a completed optical quantum computer.
