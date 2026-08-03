# Passes 2772–2776 — M36 no-go, physical lift sensing, structured CX silicon, reproducible P&R, and repeater remote SUM

## 2772 — complete two-copy M36 stabilizer-projection no-go

The exact search enumerates all 5,355 rank-two isotropic subspaces of the four-qubit binary symplectic space and all four syndromes, giving 21,420 `[[4,2]]` stabilizer-projection branches. Inputs are two identical depolarized M36 resources; arbitrary logical Clifford decoding is absorbed by the Clifford-invariant 36-ray orbit. Among branches closing back onto M36, exact `Q(sqrt(3))` polynomial certificates find no fidelity-improving branch anywhere in the grade-specific magic-witness interval: shallow 35/35 non-improving, deep 237/237 with 25 fidelity-identical, middle 11/11. This excludes only the stated two-copy stabilizer family, not larger, adaptive, catalytic, nonidentical-input, or non-stabilizer-assisted protocols.

## 2773 — physical two-shot metaplectic sensor

A phase-stable path ancilla controls `U` and `U^2` on the nine-mode register. Uniform computational-mode randomization and path-X/Y readout estimate `Tr(U)/9` and `Tr(U^2)/9`; the determinant is tracked from the programmed Clifford word and calibrated phase plates. These four quadratures reconstruct `Theta_k=Tr(U^k)^9/det(U^k)`. Across all 34 classes the trace pair gives 33 packets and the W33 projective packet resolves the final collision. The minimum nonzero normalized trace magnitude is `1/9`; a conservative 99%-confidence Hoeffding design uses 29,579 events per quadrature, 118,316 total.

## 2774 — 40 x 12 structured CX compiler

Every one of the 480 CX-centralizer cosets is exactly one W33 Lagrangian line times one of 12 invertible symmetric `2 x 2` forms over F3 with determinant 2. All `40 x 12` pairs occur once, and all 51,840 identities `g CX = r CX c` are verified with `c` in the 108-element centralizer. Storage falls from 829,440 dense dispatch bits to 20,168 structured bits, a 41.13-fold reduction. The generator emits a fail-closed synthesizable decoder.

## 2775 — reproducible placed-netlist closure

The prior hardware run failed before RTL because NumPy eigenvalue floats changed a generated M36 hash and a summary differed only in formatting. M36 serialization now uses exact formulas and fixed-width decimals; the old workflow uses a stable-artifact drift guard. The new workflow rebuilds all certificates, runs regressions, checks RTL syntax, synthesizes the structured decoder and controllers, places/routes them on iCE40 HX8K, runs timing, and uploads evidence. No remote hardware result is promoted until observed.

## 2776 — exact purification and nested remote SUM

For isotropic qutrit Bell fidelity `F`, bilateral SUM purification gives

`P_acc=(27F^2-6F+11)/32`,

`F'=(33F^2-2F+1)/(27F^2-6F+11)`.

The fixed points are `1/9`, `1/3`, and `1`, and fidelity improves exactly for `F>1/3`. Swapping obeys `F_swap=F1F2+(1-F1)(1-F2)/8`, with memory decay, classical latency, heralded erasure, purification rejection, and stale frames explicit in the scheduler. Under the labeled scenario assumptions, the optimized 1,280 km packet uses eight segments, two elementary purification rounds, and one post-swap round, giving fidelity about 0.3754 at about 0.242 heralded end-to-end resources per second. This is a modeled design point, not a measured repeater or threshold.

## Evidence

Local release: 19/19 aggregate checks and 5/5 focused regressions. Exact finite scans cover all 21,420 M36 branches and all 51,840 group elements. Remote RTL, synthesis, placement, timing, and utilization remain independent pending evidence until observed.
