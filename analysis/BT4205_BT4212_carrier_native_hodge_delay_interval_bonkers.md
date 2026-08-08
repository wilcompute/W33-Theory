# Passes 4205-4212: carrier surgery, native dual-rail mapping, compressed Hodge sensing, component delay layout, interval strata, and three outside-box exact probes

## Evidence boundary

This packet contains finite representation bookkeeping, exact graph/Hodge algebra, deterministic finite-support sensing audits, interval/Krawczyk certificates on stated symmetry-fixed subspaces, and engineering contracts grounded in public platform specifications. It does **not** claim a derived Standard Model, viable complete phenomenology, a fabricated 87-transmon processor, a laboratory compressed-Hodge sensor, a DRC-clean/fabricated photonic stack, a globally complete 80-dimensional nonlinear theorem, a measured absorber, a continuum uncertainty principle, or a physical energy-storage device.

## Pass 4205 -- representation surgery instead of add-only repair

The fixed 145-state carrier has standard-charge multiplicities `(Q,u,d,L,e)=(1,15,15,24,1)`. Any anomaly-free standard-charge chiral sector is an integer number `n` of complete generations, of state dimension 15 each. With Weyl matter only,

- `b0_SU3 = 11 - 4 n / 3`, so SU(3) asymptotic freedom permits at most `n=8`;
- `b0_SU2 = 22/3 - 4 n / 3`, so simultaneous SU(3) and SU(2) asymptotic freedom permits at most `n=5`.

Therefore the maximum anomaly-free standard-generation content retaining both nonabelian one-loop signs is five generations: 75 charged states plus 70 gauge singlets, with `b0_SU3=13/3` and `b0_SU2=2/3`. Relative to the original charge labels, 47 state labels can remain unchanged, 28 states must be reassigned among charged species, and 70 become singlets.

An independent exhaustive isotypic-packing audit treats the original `C7 x V1`, `C6 x V15`, and `C2 x V24` sectors as full-PSp commuting blocks. The block configuration counts are 46, 32, and 4; all 5,888 combinations were checked. None gives a nonzero equal-generation standard-charge embedding. Thus a viable standard-charge surgery necessarily breaks the full original PSp action or changes the gauge embedding.

## Pass 4206 -- demonstrated dual-rail transmon topology mapping

The 58 occupation modes become 29 logical dual-rail qubits: 28 payload logical qubits plus one clock logical qubit. A direct mapping to the demonstrated dual-rail transmon architecture uses two data transmons plus one erasure-detection ancilla per logical qubit, for 87 transmons excluding readout. The payload binary tree plus clock-root link needs 28 inter-logical tunable couplers and has logical maximum degree three.

The external operating point is taken from Huang et al., *Nature Physics* 22, 591-597 (2026), DOI `10.1038/s41567-026-03211-9`, together with the corresponding arXiv implementation details. The published final CNOT process fidelity is 98.1% at 13% erasure, with Bell fidelity 98.8% and three-logical-qubit GHZ fidelity 93.9%; the preprint reports millisecond-scale logical coherence, 25 ns single-qubit pi/2 gates, and 150-180 MHz dual-rail gaps. These numbers certify platform relevance, not 28-qubit readiness.

A 28-logical-qubit GHZ tree needs 27 CNOTs in four parallel entangling layers plus an initial one-qubit layer. Naively multiplying independent final-record CNOT fidelities gives only 0.596, while independent no-erasure survival at 13% erasure is only 0.0233. Reaching 90% aggregate over 27 entanglers would require approximately 99.61% per-CNOT fidelity and below 0.389% erasure per CNOT. The topology is native; the demonstrated operating point is not yet a 28-qubit machine specification.

## Pass 4207 -- ten-channel compressed Hodge sensor

The Levi incidence matrix has shape `80 x 160`, rank 79, and cycle dimension 81. The full Hodge sensor uses all 81 orthonormal harmonic rows in addition to the 80 local incidence rows.

This pass constructs a deterministic nested family by projecting seeded Gaussian rows into `H1`, then whitening. It exhaustively audits every simple Levi cycle through 14 edges (386,964 total) and every relevant rank-two theta core (133,920 total). In this fixed nested family, eight and nine cycle channels remain below the design gain 0.05, while ten channels reach minimum cycle gain 0.06776446936 and minimum theta generalized gain 0.06792020380. Thus ten is the first member of this deterministic nested family to clear the target.

Using the Levi girth and the support-14 decomposition into harmonic and incidence-visible components gives a conservative restricted singular lower bound

`0.01383770718`

for the 90-row stacked sensor. This cuts cycle-space readout from 81 channels to 10, an 87.65% harmonic-channel reduction. It is not a proof that ten is globally minimal over all sensor designs.

## Pass 4208 -- component-level static tapped-delay contract

The exact noncrossing schedule contains 919 populated delay-slot units across 160 routes, not the earlier conservative 1,280-unit envelope. At 5 ps slots and assumed group index two, one delay slot is 0.749481145 mm and the maximum eight-slot delay is 5.99584916 mm; aggregate passive delay is 0.688773172255 m.

The public LIGENTEC SiN/TFLN platform is used only as an engineering input. The current public material advertises a 200 mm SiN platform, passive SiN optical loss below 0.5 dB/m in the TFLN specification, 200 nm minimum feature scale on the technology page, low-loss delay-line capability, and 50 um-radius bend loss below 0.005 dB under the quoted platform conditions.

A conservative 50 um-radius serpentine cell uses two half-turns per slot plus two straight sections. Across the whole schedule this gives 919 static delay cells, 1,838 half-turn bends, and 1,838 straight segments. A 40-lane branch at 100 um pitch occupies about 4 mm width; the longest lane has a preliminary longitudinal footprint around 2.54 mm before keepouts.

Under the conservative interpretation of 0.005 dB per quoted 50 um bend, the eight-slot worst path budgets 0.08 dB/use in bends plus 0.003 dB/use propagation, or 0.083 dB/use and 0.415 dB over five uses before taps, couplers, interfaces, and other losses. Static compile-time delay assignment is important: a counterfactual 1x9 dynamic selector would require at least eight 2x2 switches per route, i.e. 1,280 MZI switches over 160 routes.

## Pass 4209 -- edge and nonedge fixed spaces made exhaustive

The point-, edge-, and nonedge-pair stabilizer fixed spaces are now all interval-audited.

The edge-set stabilizer has order 108 and orbit sizes `2+2+18+18`, with quotient adjacency

`[[1,2,9,0],[2,1,0,9],[1,0,5,6],[0,1,6,5]]`.

The nonedge-set stabilizer has order 48 and orbit sizes `2+2+4+16+16`, with quotient adjacency

`[[0,0,4,8,0],[0,0,4,0,8],[2,2,0,4,4],[1,0,1,4,6],[0,1,1,6,4]]`.

Outward-inflated interval range exclusion plus Krawczyk contraction over the inherited global maximum-principle boxes gives exact fixed-space root counts:

- edge selector 24: 5 roots, full Morse indices `0^2 + 23^2 + 24^1`;
- edge selector 15: 3 roots, `0^2 + 15^1`;
- nonedge selector 24: 13 roots, `17^6 + 19^4 + 21^2 + 24^1`;
- nonedge selector 15: 9 roots, `0^4 + 4^2 + 14^2 + 15^1`.

This closes the three maximal stabilizer fixed spaces used so far. It is not yet a global 80-dimensional all-symmetry classification.

## Pass 4210 -- exact critical absorber

Critical coupling applied only to the rank-24 adjacency eigenspace gives the on-resonance scattering operator

`S = I - P2`,

where `P2=(2/3)I+(1/6)A-(1/15)J`. A pure `P2` input is perfectly absorbed in this finite model. A vertex input has absorbed fraction `P2_vv=24/40=3/5`, leaving survival `2/5`; the surviving amplitudes are `2/5` on self, `-1/10` on adjacent vertices, and `1/15` on nonadjacent vertices.

## Pass 4211 -- vertex/spectral support uncertainty

For any nonzero vector supported on `s` W33 vertices and lying in a central spectral subspace of total rank `d`,

`s d >= 40`.

Proof: the central projector onto that spectral subspace has constant diagonal `d/40`; if a vector is simultaneously supported on a vertex subset and lies in the spectral subspace, the compressed projector has eigenvalue one, while its trace is `s d / 40`.

Consequences include support at least 40 in the uniform rank-one sector, at least three in the rank-15 `-4` sector, and at least two in the rank-24 `+2` sector. Delta and uniform vectors saturate the full-rank/rank-one endpoints. This is a finite association-scheme uncertainty theorem, not a continuum position-momentum relation.

## Pass 4212 -- harmonic-cycle storage functional

Define the harmonic projector on Levi edges

`P_H = I - D^T (D D^T)^+ D`

and the quadratic functional

`E_H(x)=1/2 x^T P_H x`.

It is invariant under addition of exact edge gradients `x -> x + D^T phi`; only the 81-dimensional harmonic/cycle component contributes. Edge transitivity gives a single-edge harmonic fraction `81/160` and harmonic energy `81/320`. On the integer circulation lattice, the Levi girth eight implies minimum nonzero support eight and squared norm eight, hence minimum harmonic energy four.

The term “battery” is only an analogy for a gauge-invariant graph-Hodge quadratic form.

## Reproducibility

The packet is frozen in `data/PART_4205_4212_CARRIER_NATIVE_HODGE_DELAY_INTERVAL_BONKERS.json` with semantic SHA-256 `3ac264ad9e91406b0016b01fa987f6e2d5770d5ee3874fb729707b38c475cf37`. The combined execution manifest has semantic SHA-256 `5a93faeedf96f61df842272e827c04ae153f1d37fc8537e4d02ebfb0439abc3f`.

`analysis/w33_pass4205_4212_carrier_native_hodge_delay_interval_bonkers.py` provides a quick deterministic audit and a `--full` path that regenerates the short-cycle/theta sensing census and the edge/nonedge interval root counts.
