# Passes 2784–2788 — M36 decoder boundary, physical lift sensing, structured CX silicon, reproducible P&R, and repeater remote SUM

The implementation files retain provisional build identifiers 2777, 2778, 2779, 2780, and 2781 because parallel work reserved those numbers while this packet was under construction. The canonical mapping is frozen in `data/PART_BT2784_BT2788_PROVISIONAL_ID_MAP.json`.

## 2784 — deterministic two-copy M36 stabilizer-projection boundary

The exact search enumerates all 5,355 rank-two isotropic subspaces of the four-qubit binary symplectic space and all four syndromes, giving 21,420 `[[4,2]]` stabilizer-projection branches. The original draft used eigenvectors returned by `numpy.linalg.eigh` as a logical basis. Their independent column phases are arbitrary, so the number of branches appearing to close onto an M36 ray changed across numerical-library builds.

The repaired verifier constructs each logical basis vector directly from its rank-one joint Pauli projector and fixes phase by requiring the first nonzero computational component to be positive real. In this frozen canonical logical Pauli decoder gauge, every branch that closes back onto M36 is certified by exact `Q(sqrt(3))` Bernstein-polynomial inequalities to be non-improving throughout its grade-specific magic-witness interval.

This is not an arbitrary-decoder no-go. Arbitrary logical Clifford decoders, larger codes, nonidentical inputs, catalytic resources, adaptive protocols, and non-stabilizer assistance remain open.

## 2785 — physical metaplectic sensor

A phase-stable path ancilla controls `U` and `U^2` on the nine-mode register. Uniform computational-mode randomization and path-X/Y readout estimate `Tr(U)/9` and `Tr(U^2)/9`; the determinant is tracked from the programmed Clifford word and calibrated phase plates. These four quadratures reconstruct `Theta_k=Tr(U^k)^9/det(U^k)`. Across all 34 classes the trace pair gives 33 packets and the W33 projective packet resolves the final collision. The minimum nonzero normalized trace magnitude is `1/9`; a conservative 99%-confidence Hoeffding design uses 29,579 events per quadrature, 118,316 total.

## 2786 — 40 x 12 structured CX compiler

Every one of the 480 CX-centralizer cosets is exactly one W33 Lagrangian line times one of 12 invertible symmetric `2 x 2` forms over F3 with determinant 2. All `40 x 12` pairs occur once, and all 51,840 identities `g CX = r CX c` are verified with `c` in the 108-element centralizer. Storage falls from 829,440 dense dispatch bits to 20,168 structured bits, a 41.13-fold reduction. The generator emits a fail-closed synthesizable decoder.

## 2787 — reproducible placed-netlist closure

The prior hardware run failed before RTL because NumPy eigenvalue floats changed a generated M36 hash and a summary differed only in formatting. M36 serialization now uses exact formulas and fixed-width decimals. Both hardware workflows rebuild exact certificates, run regressions and RTL simulations, synthesize the loadable state machines, reject folded netlists by minimum DFF/cell counts, place and route on iCE40 HX8K, run timing, and upload evidence. No remote hardware result is promoted until observed.

## 2788 — exact purification and nested remote SUM

For isotropic qutrit Bell fidelity `F`, bilateral SUM purification gives

`P_acc=(27F^2-6F+11)/32`,

`F'=(33F^2-2F+1)/(27F^2-6F+11)`.

The fixed points are `1/9`, `1/3`, and `1`, and fidelity improves exactly for `F>1/3`. Swapping obeys `F_swap=F1F2+(1-F1)(1-F2)/8`, with memory decay, classical latency, heralded erasure, purification rejection, and stale frames explicit in the scheduler. Under the labeled scenario assumptions, the optimized 1,280 km packet uses eight segments, two elementary purification rounds, and one post-swap round, giving fidelity about 0.3754 at about 0.242 heralded end-to-end resources per second. This is a modeled design point, not a measured repeater or threshold.

## Evidence

The release has 20 aggregate checks and five focused regressions. Exact finite scans cover all 21,420 stabilizer-projector branches in the stated decoder gauge and all 51,840 group elements. Remote RTL, synthesis, placement, timing, utilization, and fold-guard evidence remain pending until observed.
