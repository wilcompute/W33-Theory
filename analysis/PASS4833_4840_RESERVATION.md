# Passes 4833–4840 — CLOSED

Reserved collision-free after canonical Passes 4825–4832 at commit `298a76e948c78cf4435320745a011c84c9c63a24`. All five queued fronts and all three outside-box probes were executed. The complete synthesis is `analysis/PASS4833_4840_EXECUTED_OUTCOMES.md`; theorem integration is `analysis/PASS4833_4840_code_interaction_cycles_insert.tex`.

## Closure index

- **4833 / 4838:** exact invariant filtration `C_Levi <= C_378 <= C_399`, dimensions `64 < 378 < 399`; cold puncture injective. Certificate `data/PART_W33_PASS4833_4838_LEVI_SUBCODE_CODE399.json`.
- **4834:** corrected exact sparse syndrome schedule depth `3` for `[2025,399,14]_2` in the stated canonical sparse-local-basis/disjoint-support model; layers `945,675,6`, rank `1626`, radius six preserved. Certificate `data/PART_W33_PASS4834_CODE399_OPTIMAL_SCHEDULE.json`.
- **4835 / 4839:** specified low dual-shell design has quotient automorphism group `S3^135:S135`, so those shells alone cannot reconstruct PGSp/GQ/Petersen global geometry. Certificate `data/PART_W33_PASS4835_4839_INTRINSIC_DUALSHELL_AUT_FALSIFIER.json`.
- **4836:** the `1080` binary Levi minimum words form one PSp orbit and one PGSp orbit, stabilizers `24` and `48`, and are exactly the `1080` four-cycles of `SRG(27,10,1,5)`. Certificate `data/PART_W33_PASS4836_LEVI_MINIMUM_ORBITS.json`.
- **4837:** all four prior evidence gates are closed. Pass4825 exact mod-2 Brauer composition census gives `71*1 + 70*4a + 70*4b + 154*6 + 70*14 + 56*20a + 56*20b + 14*64`, forcing Loewy length at least `3`; Pass4827 exact sign-sector Burnside counts are `711679993497112` PSp and `355840805040988` PGSp with a unique fully symmetric affine sign sector; Pass4828 has exact arbitrary-rho phase diagrams for all six failure types; Pass4830 gives a unique nonzero rank-64 PGSp intertwiner between sign-H1 and binary Levi-H1. Aggregate certificate `data/PART_W33_PASS4837_HEAVY_EVIDENCE_CLOSURE.json`.
- **4840:** exact connected `1080_3 - 360_9` incidence between binary Levi minima and the canonical ternary induced-K3,3 witnesses; incidence ranks `324,359,360,360` over `F2,F3,F5,F7`. Certificate `data/PART_W33_PASS4840_LEVI_CYCLE_K33_INCIDENCE.json`.

## Integration

- Frozen cross-certificate regression: `tests/test_w33_pass4833_4840_code_interaction_cycles.py`.
- Shared manuscript frontier already imports `analysis/PASS4833_4840_code_interaction_cycles_insert.tex`, so `w33_paper.tex`, `photonic_holonet.tex`, and `holonet_machine_blueprint.tex` inherit the packet.
- Public theorem card: `analysis/PASS4833_4840_code_interaction_cycles_index_insert.html`.
- Standalone page: `docs/code399-levi-cohomology-cycles.html`.
- Public registry updated through `data/w33_public_frontier_extension_pass4461_4464.json`.
- `docs/index.html` was not directly rewritten.
- Temporary draft evidence PR #296 was closed unmerged after the repository-wide Actions queue remained saturated; theorem-level numerical results were independently reconstructed and frozen instead.

Evidence discipline: all promoted statements are exact finite graph/group/module/code/homology/fractional-flow/decoder results or explicit falsifiers. The complete nontrivial Loewy ordering of the 5671-dimensional module and the separate 225-dimensional twisted-F3 projective-moduli problem remain open. No particle/gauge-field/measured-hardware/fault-tolerance-threshold inference is made.