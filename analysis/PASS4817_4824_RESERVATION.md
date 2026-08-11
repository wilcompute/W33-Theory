# Passes 4817–4824 executed outcomes

Collision-free continuation after occupied/reserved frontier through Pass4816. All five queued fronts and three outside-box probes were attacked directly. Six fronts have fully materialized exact certificates on `master`; the two large representation fronts (4817 and 4818) have exact executable producers and a retriggered evidence workflow, but GitHub has exposed neither an evidence-bot materialization commit nor a combined status. Their numerical representation outputs are therefore **not promoted in this close ledger**. This is an execution/evidence boundary, not a guessed success.

## 4817 — exact finite PGSp module producers installed; global orbit output not materialized
The selected S3-connection moduli from Pass4770/4774 split into two exact finite deformation carriers:

- a 64-dimensional `F2` sign-cohomology quotient of the triangle-filled `GQ(4,2)` point graph;
- a 225-dimensional sign-twisted `F3` quotient `C1 / im(d_tw)`.

The certified producer `analysis/w33_pass4817_4823_pgsp_s3_moduli_certified.py` reconstructs the full PSp generators plus the PGSp outer involution on both quotients. It computes fixed and coinvariant dimensions, checks the selected binary sign sector under the full group, transports the actual selected A3 exponent class, and checks its projective stabilizer. The complete orbit census on all `2^64` sign sectors and all points of `PG(224,3)` is deliberately not brute-forced or inferred.

The workflow was triggered twice, including commit `7d52c5277278236c0e9d8eae169fa58d37aa6a39`. At close, GitHub's combined-status endpoint exposed no statuses and no `Materialize Passes 4817-4824 exact evidence` commit was visible. Therefore no fixed-space numbers or uniqueness claim from this producer are frozen here.

## 4818 — exact GAP/CTblLib Brauer producer installed; semisimplification output not materialized
The exact GAP producer `analysis/PASS4818_U42_MOD2_BRAUER.g` asks CTblLib for the characteristic-two Brauer table and decomposition matrix of `U4(2) ~= PSp(4,3)`. The parser `analysis/w33_pass4818_modular_h1_brauer_loewy_boundary.py` combines that matrix with the frozen ordinary 5671-dimensional H1 character of Pass4745.

Once materialized this computes the exact Brauer semisimplification/composition-factor census. The module-level extension data that do not depend on this job remain exact from Pass4769:

- `dim H1(F2)=5671`;
- trivial PSp/PGSp socle dimension `4`;
- trivial PSp/PGSp head dimension `1`;
- augmentation dimension `5670`;
- all four fixed vectors lie in the augmentation image;
- the apartment deck line is fixed but nonsplit.

A decomposition matrix determines the semisimplification, **not** the complete radical/socle Loewy ordering. No full nontrivial Loewy series is claimed. As with Pass4817, the GAP output file and generated Pass4818 certificate had not materialized through the evidence workflow by close.

## 4819 — complete PGSp-invariant 27-line outer-code algebra
On the 27 quotient lines (`SRG(27,10,1,5)`), the binary even permutation module has the exact nonsplit uniserial chain

`0 < W6 < W20 < E26`

with dimensions

`0,6,20,26`

and irreducible successive factor dimensions

`6,14,6`.

The exact lower and upper extensions are both nonsplit. The six-dimensional code has weight enumerator

`1 + 36 z^12 + 27 z^16`,

and `W20` has minimum distance 4.

The all-one line splits off, so there are exactly eight PGSp-invariant binary outer codes:

- `0`, dimension 0;
- `<1>`, `[27,1,27]`;
- `W6`, `[27,6,12]`;
- `W6+<1>`, `[27,7,11]`;
- `W20`, `[27,20,4]`;
- `W20+<1>`, `[27,21,3]`;
- `E26`, `[27,26,2]`;
- `F2^27`, `[27,27,1]`.

Pulling these eight outer codes back through the canonical Pass4772 27-line parity map gives the complete invariant preimage family

`[2025,378,14]_2`,
`[2025,379,14]_2`,
`[2025,384,14]_2`,
`[2025,385,14]_2`,
`[2025,398,14]_2`,
`[2025,399,14]_2`,
`[2025,404,8]_2`,
`[2025,405,7]_2`.

Hence

`[2025,399,14]_2`

is the **largest member of this complete PGSp-invariant line-parity preimage family that retains distance 14**.

For the repetition embedding of the same outer codes the exact physical minimum weights are

`2025,720,720,384,297,192,105`

for `<1>, W6, W6+1, W20, W20+1, E26, F2^27`, respectively.

Executable: `analysis/w33_pass4819_4822_outer_code_levi_classification.py`.
Frozen certificate: `data/PART_W33_PASS4819_OUTER_CODE_ALGEBRA.json`.

## 4820 — all six symmetry-broken outage flows are exact
Pass4773 supplied certified lower/upper brackets for six symmetry-breaking failures. Pass4820 closes all six fractional all-pairs problems exactly.

For each failure, the exact failure stabilizer in PSp reduces surviving edges and ordered commodities to finite orbits. A metric-dual cutting-plane calculation adds shortest-path constraints until closure; a matching path-based symmetry-averaged primal is then reconstructed. Every frozen rational certificate verifies:

- exact unit commodity sums;
- exact edge-orbit capacity inequalities with at least one tight orbit;
- exact dual normalization;
- exact rational shortest-path separation with no violated path inequality;
- reciprocal primal congestion/dual throughput equality.

At unit surviving-edge capacities and unit demand for every ordered distinct surviving pair:

- one hot Petersen fiber outage:
  `lambda = 67/5952`;
- two adjacent hot-fiber outages:
  `lambda = 665/59746`;
- two nonadjacent hot-fiber outages:
  `lambda = 133/11946`;
- one ten-vertex fiber removed:
  `lambda = 189/16538`;
- two adjacent ten-vertex fibers removed:
  `lambda = 1767/153094`;
- two nonadjacent ten-vertex fibers removed:
  `lambda = 351/30670`.

The symmetry reductions are also frozen. For example one hot-fiber outage has stabilizer order 960, 9 surviving edge orbits and 123 ordered-pair orbits; the two-hot cases have stabilizer orders 192/120 and 470/714 ordered-pair orbits for adjacent/nonadjacent failures.

Executable: `analysis/w33_pass4820_exact_outage_multicommodity.py`.
Frozen certificate: `data/PART_W33_PASS4820_EXACT_OUTAGE_MULTICOMMODITY.json`.

## 4821 — sparse parity checks, optimal two-layer syndrome schedule, and exact radius-six decoder
The `[2025,378,14]_2` router code has an explicit rank-1647 parity-check system:

- 1485 local weight-two repetition rows;
- 135 local weight-four coupling rows;
- 27 global weight-fifteen GQ-line rows.

The local physical cell is the literal Pass4776 K6. Its local `[15,3,7]_2` code has three four-edge cold repetition blocks carrying logical values `a,b,c`; the three hot matching edges all carry `a+b+c`.

Under the model that simultaneous parity checks must have disjoint physical-bit supports, all 1647 checks admit an exact two-layer schedule:

- layer A: 945 checks;
- layer B: 702 checks.

Depth one is impossible because some physical coordinates participate in two checks. Therefore schedule depth two is optimal in this stated model.

The local 12-check matrix has 4096 syndromes and exactly eight error representatives per syndrome. The zero-syndrome coset has weight census

`0^1, 7^3, 8^3, 15^1`.

Thus a total error of weight at most six cannot hide in a zero-local-syndrome cell. A bounded-distance decoder therefore:

1. measures all local/global checks in the two layers;
2. ignores zero-local-syndrome cells;
3. enumerates the eight local-coset representatives only on affected cells, pruning total weight above six;
4. uses the 27 global syndrome bits to select the unique remaining candidate.

At most six cells can be affected at radius six, giving a raw search bound

`8^6 = 262144`.

Distance 14 proves uniqueness through arbitrary physical error weight six.

Executable: `analysis/w33_pass4821_global_router_decoder_schedule.py`.
Frozen certificate: `data/PART_W33_PASS4821_GLOBAL_ROUTER_DECODER_SCHEDULE.json`.

## 4822 — outside box: router line checks are Levi cuts, and Levi homology gives [2025,64,96]
The binary Levi graph of `GQ(4,2)` has

- 72 vertices;
- 135 edges;
- binary boundary rank 71;
- `dim H1(F2)=64`;
- girth 8.

The 27 global line-parity checks used by the router code are **literally the pullbacks of the 27 line-vertex star vectors in the binary Levi cut space** under the three-coordinate collapse. They are not cycle/homology checks.

Independently, repeat a binary Levi cycle on all three sheet coordinates and apply the local physical `[15,3,7]_2` generator map. This gives an injective 64-dimensional physical subcode with exact weight law

`wt_phys = 12 * wt_Levi_cycle`.

Since the Levi graph has girth 8, this produces the canonical exact binary homology subcode

`[2025,64,96]_2`.

Pass4807's ternary Levi homology also has dimension 64, but no cross-characteristic identification is inferred.

Executable: `analysis/w33_pass4819_4822_outer_code_levi_classification.py`.
Frozen certificate: `data/PART_W33_PASS4822_LEVI_BINARY_ROUTER_HOMOLOGY.json`.

## 4823 — outside box: selected-connection projective invariant producer installed
The same certified producer as Pass4817 transports the actual selected S3 A3-exponent class into the 225-dimensional twisted F3 quotient and computes its PSp/PGSp projective stabilizer and fixed-space dimensions. Because PSp(4,3) is perfect, a PSp-stable one-dimensional projective F3 line must be fixed vectorwise. The code therefore tests the proposed sharp signature:

`selected connection = unique PSp-fixed line in twisted H1(F3)`.

No result is promoted at close because the evidence workflow has not materialized the corresponding certificate. This preserves the Pass4746 lesson: the triangle-transposition rule alone is massively nonunique, so a stronger invariant must be explicitly computed rather than named.

## 4824 — outside box: exact module obstruction between flag H1 and binary Levi H1
The 64-dimensional binary Levi homology carries an exact PSp action reconstructed through the 27 quotient-line action. Exact linear algebra gives

`dim (H1_Levi)^PSp = 0`,

and

`dim (H1_Levi)_PSp = 0`.

Therefore

`Hom_PSp(1,H1_Levi)=0`

and

`Hom_PSp(H1_Levi,1)=0`.

Since Pass4769 gives a four-dimensional trivial PSp socle in the 5671-dimensional flag H1, no nonzero PSp-equivariant linear map can send any of those four trivial lines into binary Levi homology; conversely Levi homology has no trivial quotient onto which a transfer can land. The tempting same-characteristic bridge fails at the module-intertwiner level.

Executable: `analysis/w33_pass4824_flag_h1_levi_transfer_obstruction.py`.
Frozen certificate: `data/PART_W33_PASS4824_FLAG_H1_LEVI_TRANSFER_OBSTRUCTION.json`.

## Integration and evidence
- Reservation commit: `50a506e715edf46aee69211dc144a6aeabc3b662`.
- Executable producers are present for all eight passes.
- GAP extractor: `analysis/PASS4818_U42_MOD2_BRAUER.g`.
- Cross-certificate regression: `tests/test_w33_pass4817_4824_pgsp_loewy_code_flow_decoder.py`.
- Evidence workflow: `.github/workflows/w33_pass4817_4824_pgsp_loewy_code_flow_decoder.yml`; retriggered after frozen-certificate integration at commit `7d52c5277278236c0e9d8eae169fa58d37aa6a39`.
- Shared theorem insert: `analysis/PASS4817_4824_pgsp_loewy_code_flow_decoder_insert.tex`.
- The shared frontier manifest `analysis/W33_CURRENT_FRONTIER_MANIFEST.tex` imports the new theorem block after Pass4809–4816, so all three maintained manuscripts inherit it without direct wrapper rewrites.
- Public card: `analysis/PASS4817_4824_pgsp_loewy_code_flow_decoder_index_insert.html`.
- Standalone page: `docs/pgsp-moduli-outer-code-outage-decoder.html`.
- Public frontier registry updated through the registered-card route.
- `docs/index.html` was not directly rewritten.

At close, `get_commit_combined_status` for the workflow retrigger still returned an empty status list and no evidence-bot materialization commit was visible. Therefore Pass4817/4818/4823 representation outputs are explicitly left unpromoted rather than assumed successful.

Evidence discipline: all promoted numerical statements are exact finite graph/code/module/homology/decoder results or exact fractional multicommodity-flow theorems under stated conventions. No identification is made from equal dimensions or counts alone. No physical gauge field, particle/generation assignment, measured-hardware performance or physical fault-tolerance threshold is inferred.