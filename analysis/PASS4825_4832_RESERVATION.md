# Passes 4825–4832 executed outcomes

Passes 4825–4832 were reserved collision-free at commit `07ac7caa63e6c6a273e8a028b2fe0127740c7e53`. All five queued fronts and three outside-box probes were attacked directly. Four passes (4826, 4829, 4831, 4832) are fully frozen at theorem level with independent exact certificates. Four heavier representation/optimization passes (4825, 4827, 4828, 4830) have exact producers and a self-materializing workflow installed, but no generated evidence-bot commit or combined status was visible at close; their numerical outputs are therefore deliberately not promoted here.

## 4825 — characteristic-two Brauer/Loewy closure producer installed; numerical semisimplification not materialized
The existing exact GAP/CTblLib extractor `analysis/PASS4818_U42_MOD2_BRAUER.g` and parser `analysis/w33_pass4818_modular_h1_brauer_loewy_boundary.py` are chained into `analysis/w33_pass4825_brauer_loewy_closure.py`. Once generated, this closes the exact characteristic-two composition-factor census of the 5671-dimensional invariant-flag H1 and combines it with the already-frozen Pass4769 module data:

- `dim H1(F2)=5671`;
- trivial PSp/PGSp socle dimension 4;
- trivial head/coinvariant dimension 1;
- augmentation dimension 5670;
- all four fixed vectors lie inside the augmentation image;
- the apartment deck line is fixed but nonsplit;
- no trivial direct summand exists.

The producer records only Loewy consequences that genuinely follow from those data and a decomposition matrix. A decomposition matrix determines the Brauer semisimplification, not the complete radical/socle ordering of nontrivial simples. No complete nontrivial Loewy series is promoted without an explicit 5671-dimensional MeatAxe module computation.

## 4826 — exact radius-six decoder for the maximal [2025,399,14]_2 code
Pass4819's largest invariant line-parity preimage retaining distance 14 is

`[2025,399,14]_2`,

with outer code `W20+<1>=[27,21,3]_2` and outer dual `W6=[27,6,12]_2`.

The exact physical parity-check rank is

`1626 = 1620 local + 6 global`.

The 1620 local K6-cell checks and their syndrome cosets are exactly those of Pass4821. Each local syndrome has eight representatives and the minimum nonzero zero-local-syndrome word has weight seven. Hence for total error weight at most six only cells with nonzero local syndrome need be searched; at most six cells are affected and the raw search bound remains

`8^6 = 262144`.

The six global W6 syndrome bits uniquely select the correct candidate because two candidates of physical weight at most six with identical complete syndrome would differ by a codeword of weight at most 12, contradicting `d=14`.

Every two distinct nonzero W6 words intersect: nonzero W6 weights are 12 or 16 and the sum of two nonzero W6 words again has weight 12 or 16, so disjoint supports would force sum weight at least 24. Thus the six independent global checks have conflict graph K6 and require six separate global layers. Together with Pass4821's two local layers this gives a certified eight-layer schedule construction. Only the six-layer global requirement is proved minimum; combined global/local depth eight is not claimed globally optimal.

Frozen certificate: `data/PART_W33_PASS4826_CODE399_DECODER.json`.
Producer: `analysis/w33_pass4826_4832_code399_decoder_dualshell.py`.

## 4827 — exact PGSp sign-sector Burnside producer installed; orbit count not materialized
Pass4770 gives an affine 64-dimensional F2 space of admissible S3 sign sectors. Pass4817 proves the selected sign solution is PGSp-fixed, so translation by it identifies the affine set with the linear 64-dimensional sign-cohomology module.

`analysis/w33_pass4827_pgsp_sign_burnside.py` reconstructs the common PSp/PGSp generator matrices on that module, enumerates the finite matrix image rather than the `2^64` vectors, computes the fixed-dimension census, and applies exact Burnside arithmetic

`#orbits = |G_image|^{-1} sum_g 2^{dim Fix(g)}`.

This completely avoids astronomical vector enumeration. The old Pass4817/4823 producer is run first in the same evidence workflow so the 225-dimensional twisted-F3 selected-line data can be carried forward if materialized. At close no generated Pass4827 certificate was visible, so no Burnside orbit count or selected-line uniqueness number is promoted here.

## 4828 — arbitrary-rho outage phase-diagram producer installed; phase lines not materialized
`analysis/w33_pass4828_parametric_outage_flow.py` extends each of the six exact Pass4820 failure stabilizer reductions to cold capacity 1 and hot capacity `rho>0`.

For every exact metric-dual optimum the throughput is an affine rational form

`lambda(rho)=A+B rho`.

The producer adaptively discovers the lower envelope of these dual lines. It seeds multiple rational rho values, reconstructs exact rational primal and dual certificates, adds shortest-path separation constraints until closure, computes candidate intersections, and recursively tests every region and breakpoint. The intended output is a complete piecewise-rational phase diagram for each of the six failure types, with exact comparison against the intact breakpoints `63/155`, `111/137`, `239/105`.

At close the self-materializing workflow had not produced the Pass4828 certificate, so no unobserved breakpoint or affine line is promoted here. The exact rho=1 values from Pass4820 remain the current theorem-level failure data.

## 4829 — Levi homology code collapses to a repeated graph-cycle code
The Pass4822 binary homology subcode has the exact objectwise structure

`0^405 + Rep_12(H1(Levi(GQ(4,2));F2))`.

All 405 Petersen-hot coordinates are forced zero. The 135 Levi incidence edges are represented by 135 disjoint 12-coordinate cold repetition blocks, covering all 1620 cold physical coordinates. Puncturing the forced-zero coordinates gives

`[1620,64,96]_2`.

The GQ(4,2) Levi graph has 72 vertices, 135 edges, cycle dimension 64, girth 8 and edge connectivity 3. It has exactly 1080 simple 8-cycles; under twelvefold repetition these are exactly 1080 minimum physical words of weight 96.

The physical dual has dimension 1961 and minimum distance 1. Its sparse basis consists of

- 405 hot singleton checks;
- 1485 weight-two repetition-chain checks;
- 71 independent Levi-star checks;

for total rank 1961. The full dual contains exactly 405 weight-one words and 90,720 weight-two words.

A four-layer syndrome schedule is explicitly constructed: hot singletons together with one alternating repetition-chain half; the other repetition half; the 45 point-star checks; and 26 independent line-star checks. Global optimality of four layers is not asserted.

Maximum-likelihood decoding reduces exactly to a graph problem. For a cold repetition block e let `a_e` be the number of received ones and `c_e=12-2a_e`. Let N be the set of negative-cost Levi edges and `T=boundary(N)`. ML cycle-code decoding is exactly a minimum-weight T-join on the 72-vertex Levi graph with weights `|c_e|`, followed by symmetric difference with N. Since `d=96`, every arbitrary error pattern of weight at most 47 is corrected uniquely.

Frozen certificate: `data/PART_W33_PASS4829_LEVI_HOMOLOGY_CODE.json`.
Corrected producer: `analysis/w33_pass4829_levi_code_corrected.py`.

## 4830 — outside box: exact 64-by-64 common-generator intertwiner test installed; result not materialized
The Pass4770 sign-cohomology module and Pass4822 binary Levi H1 both have dimension 64. This numerical equality is not used as evidence.

`analysis/w33_pass4829_4830_levi_code_sign_module.py` constructs both 64-dimensional representations from the same PSp generators and the same PGSp outer generator, then solves the exact simultaneous equations

`X A_g = B_g X`

over F2 on 4096 unknown matrix entries. The hardened launcher `analysis/w33_pass4829_4830_levi_code_sign_module_hardened.py` accepts a positive isomorphism only from an explicit invertible intertwiner. A negative result is accepted only after exhaustive search of the exact Hom space; if the Hom dimension is too large for an exhaustive negative, the producer raises instead of manufacturing a false nonisomorphism.

No Pass4830 generated certificate was visible at close, so the two 64-dimensional modules remain un-identified.

## 4831 — outside box: 12 deep-hole orbits are not the 12 residue orbitals
Pass4812 has exactly twelve PSp orbits of H10 radius-14 deep holes, but Pass4737's 270-residue action also has rank twelve. The tempting `12=12` identification is false.

The H10 orbit-size multiset is

`1080^1, 2160^2, 3240^1, 4320^2, 6480^2, 12960^4`,

with stabilizer orders

`24^1, 12^2, 8^1, 6^2, 4^2, 2^4`.

The residue ordered-pair orbitals have subdegrees

`1,12,16,48,16,6,24,96,12,12,24,3`,

hence homogeneous orbit sizes

`270^1, 810^1, 1620^1, 3240^3, 4320^2, 6480^2, 12960^1, 25920^1`,

and ordered-pair stabilizer orders

`96^1, 32^1, 16^1, 8^3, 6^2, 4^2, 2^1, 1^1`.

The multisets differ, so no componentwise PSp-homogeneous G-set bijection can identify the two twelve-part decompositions. More indirect incidence maps are not ruled out.

Frozen certificate: `data/PART_W33_PASS4831_DEEPHOLE_RESIDUE_12X12_FALSIFIER.json`.
Producer: `analysis/w33_pass4831_deephole_residue_12x12_falsifier.py`.

## 4832 — outside box: the [2025,399,14] dual shells reconstruct the router cells intrinsically
Ignoring all imported router labels, the 2025 generator columns of the `[2025,399,14]_2` code form exactly 540 equivalence classes:

- 405 classes of size 4;
- 135 classes of size 3.

These recover the cold K2,2 blocks and Petersen-hot triples respectively. Equal-column pairs give the complete weight-two dual shell:

`405*C(4,2) + 135*C(3,2) = 2835`

words, spanning dimension 1485.

Quotienting the dual by that complete weight-two span gives length 540 and dimension 141. Its minimum weight is four. The minimum shell consists of exactly 135 relations, each with class-size profile `(4,4,4,3)`, and these 135 relations partition all 540 quotient coordinates. They are precisely the 135 physical K6 cells via the local relation

`A+B+C+H=0`

on three cold size-four classes and one hot size-three class.

The six extra outer W6 dual directions cannot create another weight-four quotient relation. At each GQ point a W6 word meets either zero or two of the three incident quotient lines; adding a local cell relation sends k to `4-k`, so the minimum local quotient contribution remains zero or two on each sheet. Since W6 nonzero weights are 12 or 16, these directions have minimum quotient weights 180 or 240.

Frozen certificate: `data/PART_W33_PASS4832_CODE399_DUAL_SHELL_GEOMETRY.json`.
Producer: `analysis/w33_pass4826_4832_code399_decoder_dualshell.py`.

## Integration and evidence state
- Reservation commit: `07ac7caa63e6c6a273e8a028b2fe0127740c7e53`.
- Exact producer workflow: `.github/workflows/w33_pass4825_4832_loewy_decoder_moduli_outage_levi.yml`; latest hardened trigger state includes corrected Pass4829 and fail-closed Pass4830.
- Frozen regression: `tests/test_w33_pass4825_4832_loewy_decoder_moduli_outage_levi.py`.
- Shared theorem insert: `analysis/PASS4825_4832_loewy_decoder_moduli_outage_levi_insert.tex`.
- `analysis/W33_CURRENT_FRONTIER_MANIFEST.tex` imports the new theorem block after Pass4817–4824, so all maintained manuscripts inherit it through the shared frontier.
- Public card: `analysis/PASS4825_4832_loewy_decoder_moduli_outage_levi_index_insert.html`.
- Standalone page: `docs/code399-levi-cycle-decoder.html`.
- Public registry updated through `data/w33_public_frontier_extension_pass4461_4464.json`.
- `docs/index.html` was not directly rewritten.

At close, no `Materialize Passes 4825-4832 exact evidence` bot commit was visible and GitHub's combined-status surface exposed no usable status for the hardened trigger. Therefore Passes4825/4827/4828/4830 remain exact executable research fronts but their unobserved numerical outputs are not claimed.

Evidence discipline: all promoted numerical statements above are exact finite graph/group/code/homology/decoder results or explicit falsifiers frozen in the repo. No identification is made from equal dimensions/counts/orders alone, and no physical particle/gauge-field/measured-hardware/fault-tolerance-threshold inference is made.