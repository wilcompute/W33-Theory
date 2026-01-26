# W33 Repo Progress Report — Jan 26, 2026

This report summarizes the latest verification steps run in the local W33 repo
and the artifacts generated/updated as part of the “keep going” request.

## What I Ran

- `python3 tools/build_final_summary_table.py`
  - Regenerated the computed prediction tables.
- `python3 tools/build_verification_digest.py`
  - Regenerated the verification digest (baseline audits + Sage/H1 summary).
- `python3 show_results.py`
  - Printed the Sage-incidence/H1 summary from `data/w33_sage_incidence_h1.json`.
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python THEORY_PART_CXIII_SAGE_VERIFICATION.py`
  - Executed the Sage verification script inside the official Sage container.
- `docker run --rm -v "$(pwd)":/work -w /work -e W33_FAST=1 sagemath/sagemath:10.7 bash -lc "scripts/run_all_sage.sh"`
  - Ran the full Sage verification suite using the Docker image (FAST_MODE).
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python tools/srg40_uniqueness.sage`
  - Parsed the Spence SRG(40,12,2,4) adjacency-matrix dataset and enumerated all 28 graphs.
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python tools/e8_linegraph_compare.sage`
  - Compared the W33 line graph to E8 root adjacency graphs (inner product ±1).
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python tools/e8_edge_relation_search.sage`
  - Tested alternative edge‑relation graphs on the 240 W33 edges against E8 root adjacency (inner product 1, 0, −1).
- `python3 tools/qutrit_pauli_w33.py`
  - Rebuilt the 2‑qutrit Pauli commutation geometry summary (fixing a degree variable shadowing bug).
- `python3 tools/e8_witting_compare.py`
  - Compared realified Witting polytope vertices against E8 roots via inner‑product distributions.
- `python3 tools/e8_rootline_partition.py`
  - Found a partition of the 120 E8 root lines into 40 triples of mutually orthogonal lines (exact cover).
- `python3 tools/e8_triple_relation_search.py`
  - Tested all relation-count unions between the 40 orthogonal triples to see if any yields SRG(40,12,2,4).
- `python3 tools/e8_triple_relation_search_full.py`
  - Tested full 6×6 inner‑product relation classes between triples; no SRG(40,12,2,4) found.
- `python3 tools/e8_partition_search.py`
  - Ran randomized searches for alternative 40‑triple partitions that might yield SRG(40,12,2,4).
- `E8_PARTITION_TAG=orthocount_deep E8_PARTITION_TRIES=50 E8_PARTITION_MAX_NODES=400000 python3 tools/e8_partition_search.py`
  - Deeper randomized search (orthogonality‑count relations).
- `E8_PARTITION_TAG=fullip_limited E8_PARTITION_TRIES=5 E8_PARTITION_MAX_NODES=150000 E8_RELATION_MODE=fullip E8_PARTITION_MAX_CLASS_UNIONS=1024 python3 tools/e8_partition_search.py`
  - Full 6×6 inner‑product relation search (limited class unions for runtime).
- `E8_PARTITION_TAG=pattern_filter E8_PARTITION_TRIES=15 E8_PARTITION_MAX_NODES=250000 E8_PARTITION_TARGET_PATTERN='20x(0,3);18x(3,0);2x(1,2)' python3 tools/e8_partition_search.py`
  - Pattern‑constrained partition search.
- `E8_COMPOSITE_MAX_COMB=4 python3 tools/e8_triple_relation_search_composite.py`
  - Composite relation search (triple type patterns + full 6×6 inner‑product classes, combos up to size 4).
- `python3 tools/witting_trace_map_pg32.py`
  - Tested a GF(4)→GF(2) trace map on 40 Witting base states (Marcelis-inspired).
- `python3 tools/witting_trace_map_pg32_full.py`
  - Ran the full 240‑vertex trace map (Marcelis §8) and verified the 16‑to‑1 collapse onto 15 GF(2) points.
- `python3 tools/witting_pg32_fiber_analysis.py`
  - Built W33 from GF(4) hermitian orthogonality and analyzed trace fibers on PG(3,2).
- `python3 tools/witting_pg32_ray_trace.py`
  - Analyzed trace images of the 40 Witting rays under GF(4) scalars and W33 line image unions.
- `python3 tools/witting_pg32_full_fiber_counts.py`
  - Computed multiplicity and unique-vector counts inside each PG(3,2) fiber for the full 240 vertices.
- `python3 tools/witting_pg32_fiber_graphs.py`
  - Built orthogonality graphs on the 8 unique vectors in each PG fiber.
- `python3 tools/witting_pg32_relation_search.py`
  - Searched PG(3,2) trace-image relations between rays for a direct W33 adjacency match.
- `python3 tools/witting_pg32_line_relation.py`
  - Compared W33 lines (4‑cliques) to PG(3,2) lines via trace‑image unions.
- `python3 tools/witting_pg32_plane_relation.py`
  - Checked which W33 line unions contain PG(3,2) planes (7‑point subsets).
- `python3 tools/witting_pg32_ray_line_image.py`
  - Checked whether ray trace images are PG lines and isotropic PG lines.
- `python3 tools/witting_pg32_incidence_relation_search.py`
  - Tested incidence‑based relations (point/line, line/line) for a W33 adjacency match.
- `python3 tools/witting_pg32_plane_cover_map.py`
  - Mapped which PG(3,2) planes are contained in W33 line unions (single‑plane cases).
- `python3 tools/witting_pg32_hit_lines_analysis.py`
  - Analyzed the 16 PG(3,2) lines hit by ray images (coverage + intersection graph).
- `python3 tools/witting_pg32_hit_lines_spread_search.py`
  - Checked for spreads/partial spreads inside the 16 hit lines.
- `python3 tools/witting_pg32_config_invariants.py`
  - Computed invariants (degree and spectrum) for the 14‑point/16‑line configuration.
- `docker run --rm -v "$(pwd)":/work -w /work sagemath/sagemath:10.7 sage -python tools/witting_pg32_config_aut.sage`
  - Computed the automorphism group of the 14‑point/16‑line incidence graph.
- `python3 tools/witting_pg32_line_stabilizer.py`
  - Computed the GL(4,2) stabilizer of the 16 hit lines (geometric automorphisms).
- `python3 tools/witting_pg32_alternating_form_search.py`
  - Exhaustive search over alternating forms to match isotropic lines to the 16 hit lines.
- `python3 tools/witting_pg32_quadratic_rule_search.py`
  - Exhaustive search over quadratic-form line selection rules.
- `python3 tools/witting_pg32_line_space_plucker.py`
  - Plücker/Klein-quadric line-space analysis for the 16 hit lines.
- `python3 tools/witting_pg32_line_orbit_structure.py`
  - Orbit decomposition of all 35 PG(3,2) lines under the hit-line stabilizer.
- `python3 tools/witting_pg32_line_orbit_intersections.py`
  - Intersection counts between line orbits (association-scheme style check).
- `python3 tools/witting_pg32_orbit_incidence_table.py`
  - Incidence table between point orbits and line orbits.
- `python3 tools/witting_pg32_line_orbit_point_composition.py`
  - Point-orbit composition of each line orbit.
- `python3 tools/witting_pg32_weight_orbit_analysis.py`
  - Hamming-weight classification of points/lines; identifies the 6‑point tetrahedral subgeometry.
- `python3 tools/witting_pg32_ray_rule_analysis.py`
  - Derives the ray‑level GF(4) rule that separates (1,2,3) vs (2,2,2) line images.
- `python3 tools/witting_pg32_tetrahedral_rays.py`
  - Lists the 8 rays mapping to the 4 tetrahedral (2,2,2) lines.
- `python3 tools/witting_pg32_ray_invariant_product.py`
  - Computes simple GF(4) invariants (product/sum of nonzeros) that separate line patterns.
- `python3 tools/witting_w33_line_tetrahedron_analysis.py`
  - Locates tetrahedral rays inside W33 lines and computes induced subgraph stats.
- `python3 tools/witting_w33_tetra_subgraph.py`
  - Confirms the tetrahedral-ray induced subgraph is K4,4 (bipartite 4‑regular).
- `python3 tools/witting_w33_line_trace_tetra_analysis.py`
  - Classifies W33 lines with tetra rays by PG(3,2) trace-union structure.
- `python3 tools/d4_w33_structure_analysis.py`
  - Checked H12 neighbor subgraph structure and D4 root parallels.
- `python3 tools/h27_jordan_algebra_test.py`
  - Analyzed the 27 non-neighbors (H27) for Jordan-algebra adjacency rules.
- `python3 tools/d4_triality_action.py`
  - Built the triangle co-occurrence graph and triality-style invariants.
- `python3 tools/h12_h27_incidence_patterns.py`
  - Measured how H27 vertices attach to the 4 H12 triangles.
- `python3 tools/triangle_e8_correspondence.py`
  - Compared the triangle graph’s 240 edges to E8 root counts and spectra.
- `python3 tools/d4_d4_e8_decomposition.py`
  - Explored D4×D4 and 240=240 decomposition heuristics.
- `python3 tools/eigenspace_d4_analysis.py`
  - Analyzed λ=2 eigenspace geometry and adjacency separation.
- `python3 tools/edge_root_system_analysis.py`
  - Tested edge-projection vectors as a root-like system.
- `python3 tools/h27_affine_hyperplane_search.py`
  - Searched for triangle labelings making H27 an affine hyperplane in F3^4.
- `python3 tools/h27_latin_cube_search.py`
  - Searched for triangle labelings making H27 a 3×3×3 Latin cube.
- `python3 tools/h27_code_invariants.py`
  - Computed H27 tuple invariants and automorphisms under S3^4 ⋊ S4.
- `python3 tools/h27_triplet_structure.py`
  - Analyzed the 3‑to‑1 collapse into 9 tuple classes and their quotient graph.
- `python3 tools/h27_fiber_translation_structure.py`
  - Searched for Z3 labelings that turn inter‑fiber matchings into translations.
- `python3 tools/h27_affine_plane_equations.py`
  - Extracted the two linear equations defining the 9‑tuple affine plane.
- Updated CI paths + proof test inputs:
  - Added `claude_workspace/run_sage.sh` wrapper so the `sage-verification` workflow can find the script.
  - Fixed `src/PROOF_MINUS_ONE.py` to use repo‑relative data paths.
  - Adjusted `tests/test_proofs_execution.py` to skip missing external proof file.
- `W33_POLARITY_TRIALS=10000 python3 tools/witting_pg32_polarity_search.py`
  - Random GL(4,2) polarity search to maximize isotropic hit lines.
- `python3 tools/witting_pg32_augmented_lines_analysis.py`
  - Added the 7 lines through the missing point and analyzed the augmented configuration.

## Findings (Key Facts)

### 1) W33 incidence + H1 (from existing Sage output)

From `data/w33_sage_incidence_h1.json` (via `show_results.py`):

- Incidence automorphism group order: **51,840**
- Structure: **O(5,3) : C2**
- Non-abelian, non-solvable
- H1 dimension: **81**
- H1 action matrices: **8**

These match the repo’s claims about |Aut(W33)| and the H1 rank.

### 1b) Sage verification run (Docker)

The Docker Sage run completed successfully and wrote:

- `PART_CXIII_verified_results.json`

The script’s internal timestamp reports:

- `2026-01-16T20:23:20.913315`

This timestamp is produced by the script itself (not by Docker), so it reflects
the script’s embedded date logic rather than the wall-clock time of this run.

### 1c) Full Sage suite run (Docker, FAST_MODE)

The full suite completed successfully with `W33_FAST=1` (skipping heavy
clique/chromatic computations in `THEORY_PART_CXIII_SAGE_VERIFICATION.sage`).
Key artifacts updated/created by the suite include:

- `PART_CXIII_sagemath_verification.json`
- `PART_CVII_sage_results.json`
- `PART_CXVIII_explicit_construction.json`
- `PART_CXIX_27_nonneighbors.json`

Notable observations from the suite output (post-fix):

- `THEORY_PART_CXIII_SAGE_VERIFICATION.sage` now constructs the orthogonality
  graph with **240 edges**, and is **isomorphic** to Sage’s built-in
  `SymplecticPolarGraph(4,3)` (parameters SRG(40,12,2,4)).

- `THEORY_PART_LIV_SAGE_VERIFICATION.py` now uses the built-in 40‑vertex W33,
  matches Sp(4,3) order **51,840**, and reproduces eigenvalues
  **{12, 2, −4}** with multiplicities **1, 24, 15**.

- `THEORY_PART_CXVIII_EXPLICIT_CONSTRUCTION.py` now runs in Docker without WSL.
  It suppresses noisy 12‑vertex subgraph logs by default; set `W33_VERBOSE=1`
  for full trace output.

### 1d) Latest Sage JSON snapshot (2026-01-26)

| Artifact | Key values |
|---|---|
| `PART_CXIII_sagemath_verification.json` | vertices=40, edges=240, SRG=(40,12,2,4), Aut=51840, eigenvalues=(12^1, 2^24, -4^15) |
| `PART_CVII_sage_results.json` | vertices=40, edges=240, triangles=160, Aut=51840, E8 roots=240 |
| `PART_CXIX_27_nonneighbors.json` | H27 edges=108, degree=8, stab=1296, eigenvalues=(8^1, -4^6, -1^8, 2^12) |
| `PART_CXVIII_explicit_construction.json` | success=true (Sage run), timestamp=2026-01-26T04:16:22 |

### 1e) SRG(40,12,2,4) enumeration (Spence dataset)

- Enumerated **28** non‑isomorphic SRG(40,12,2,4) graphs.
- Exactly **one** graph is isomorphic to W33 (index 25 in the dataset).
- Two graphs share `|Aut| = 51840` and `max_clique_count = 40`, but only one
  is isomorphic to W33. This isolates W33 within the 28‑graph family.

See `artifacts/srg40_uniqueness.md` for the full table.

### 1f) E8 adjacency test vs W33 line graph

- W33 line graph has degree **22**, while E8 root adjacency graphs
  (inner product = ±1) have degree **56**.
- The line graph is **not isomorphic** to either E8 adjacency graph.

See `artifacts/e8_linegraph_compare.md`.

### 1g) 2‑qutrit Pauli geometry (F3^4 commutation)

The commutation geometry on projective points of F3^4 matches W33:

- points = 40, edges = 240, SRG parameters (40,12,2,4)
- 40 lines of size 4, 4 lines per point
- triangles = 160

See `artifacts/qutrit_pauli_w33.md`.

### 1h) Alternative edge‑relation search (E8 mapping attempt)

We classified pairs of W33 edges by (shared endpoints, cross‑adjacencies) and
tested **all unions** of these classes for regular graphs on 240 vertices.

Key results:
- No class or class‑union yields a **degree‑56** graph matching E8 root
  adjacency (inner product 1 or −1).
- No class or class‑union matches the **degree‑126** E8 orthogonality graph
  (inner product 0) either.
- The only degree‑22 union is the standard **line‑graph relation** (edges
  sharing a vertex).

See `artifacts/e8_edge_relation_search.md`.

### 1i) Witting vs E8 (realified comparison)

We built the 240 Witting vertices in C^4 (40 rays × 6 phases), realified to R^8,
normalized to norm √2, and compared inner‑product distributions to E8 roots.

Findings:
- Witting inner products include **±1.1547** and **±0.57735**, which are **not**
  present in the E8 root system.
- Per‑vertex neighbor counts at ip=±1 and ip=0 do **not** match E8’s (56 and 126).

Conclusion: the standard realification of Witting vertices is **not** identical
to the E8 root system (at least not under this embedding).

See `artifacts/e8_witting_compare.md`.

### 1j) E8 root-line orthogonal triple partition (octahedra cover)

We grouped the 120 **E8 root lines** (± pairs) into 40 triples of **mutually
orthogonal** lines. Each triple corresponds to an octahedron (6 roots) in the
E8 orthogonality graph, matching the **6-edge structure** of a W33 line.

Results:
- 120 root lines, degree 63 in the orthogonality graph
- 37,800 orthogonal triples (triangles)
- **Exact cover found** in 46 search nodes (fast)

This gives a concrete bridge:  
**W33 lines (40) ↔ orthogonal line triples (A1^3) in E8**, hence  
**W33 edges (240) ↔ E8 roots (240)** via octahedral blocks.

See `artifacts/e8_rootline_partition.md`.

### 1k) Triple‑relation search (40‑block graph)

Using the 40‑triple partition, we defined relations between triples based on
how many orthogonal line‑pairs they contain (0..9) and tested all unions of
these classes.

Result: **no regular SRG** appears (including no SRG(40,12,2,4)).

See `artifacts/e8_triple_relation_search.md`.

### 1l) Full inner‑product relation search (40‑block graph)

Using full 6×6 inner‑product counts between triples (counts of −1, 0, +1),
we searched all unions of relation classes:

- 10 relation classes
- **0 SRG candidates** found (none match SRG(40,12,2,4))

We also observed triple type patterns by E8 root type:
- 20 triples of (type1,type2) = (0,3)
- 18 triples of (3,0)
- 2 triples of (1,2)

See `artifacts/e8_triple_relation_search_full.md`.

### 1m) Randomized partition search (targeting SRG)

We attempted randomized exact‑cover partitions of the 120 root lines into
40 orthogonal triples and tested all orthogonality‑count relations.

Result (baseline): **no SRG(40,12,2,4) found**.

Deeper runs:
- Orthogonality‑count search (50 tries, 400k nodes/try): **no SRG found**.
- Full 6×6 inner‑product search (5 tries, 150k nodes/try, class‑union limit 1024): **no SRG found**.
- Pattern‑constrained search (15 tries, 250k nodes/try, target pattern 20×(0,3), 18×(3,0), 2×(1,2)): **no SRG found**.

See `artifacts/e8_partition_search_orthocount_deep.md`,
`artifacts/e8_partition_search_fullip_limited.md`,
`artifacts/e8_partition_search_pattern_filter.md`.

### 1n) Composite triple‑relation search

We refined relation classes by including triple‑type patterns and full 6×6
inner‑product counts, then searched unions of up to 4 classes:

- 33 composite classes
- 0 SRG candidates (including SRG(40,12,2,4))

See `artifacts/e8_triple_relation_search_composite.md`.

### 1o) Witting trace‑map test (GF(4) → GF(2))

We implemented the coordinatewise trace map **Tr(x)=x+x²** from GF(4)→GF(2)
on the 40 Witting base states:

- trace values: Tr(0)=0, Tr(1)=0, Tr(ω)=1, Tr(ω²)=1
- resulting projective images: **6** points (not 15)

This suggests the modeled vertex set is incomplete for the published
trace‑map construction (which expects 15 PG(3,2) points).

See `artifacts/witting_trace_map_pg32.md`.

### 1p) Witting trace‑map test (full 240 vertices)

Using the full 240 Witting vertices with the Marcelis coordinate patterns:

- 15 unique GF(2) points
- each point occurs exactly **16 times**
- includes the zero vector (projectively replaced by 1111)

This matches the Marcelis statement about the GF(4)→GF(2) trace map.

See `artifacts/witting_trace_map_pg32_full.md`.

### 1q) Witting→PG(3,2) ray‑trace analysis

We mapped each of the 40 Witting rays via scalar multiples {1, ω, ω²} and
recorded their trace images in PG(3,2), then compared to W33 lines:

- 8 rays map to a single PG point; 32 rays map to 3 PG points
- 1 PG point is uncovered by ray images; the other 14 points are covered
  with multiplicities 7 or 8
- W33 lines (4‑cliques) map to PG unions of size 4, 5, 8, or 10

See `artifacts/witting_pg32_ray_trace.md`.

### 1r) PG(3,2) fiber multiplicities (240 vertices)

Each PG point fiber contains **16** vertices, but only **8** distinct GF(4)
vectors (the other 8 are the ± phase duplicates).

See `artifacts/witting_pg32_full_fiber_counts.md`.

### 1s) Fiber orthogonality graphs (8‑vertex cores)

The 8 unique vectors per PG point do **not** form a uniform 3‑regular cube.
Degree sets vary (e.g., degree 4 for the zero‑vector fiber; degree 2 or mixed
0/2 for others).

See `artifacts/witting_pg32_fiber_graphs.md`.

### 1t) PG(3,2) relation search vs W33

We classified ray pairs by trace‑image set sizes and intersections (6 classes)
and tested all unions for exact W33 adjacency. **No union matches W33**.

See `artifacts/witting_pg32_relation_search.md`.

### 1u) W33 line unions vs PG(3,2) lines

No W33 line maps exactly to a PG(3,2) line under the trace‑image union.
PG lines are covered unevenly (0–17 W33 lines per PG line).
Each W33 line union contains either 0, 1, 7, or 8 PG lines.

See `artifacts/witting_pg32_line_relation.md`.

### 1v) W33 line unions vs PG(3,2) planes

Among 40 W33 lines, **16** line unions contain exactly one PG(3,2) plane
(7‑point Fano plane), and **24** contain none. No ovoid‑like unions detected.

See `artifacts/witting_pg32_plane_relation.md`.

### 1w) Ray images as PG(3,2) lines

The 32 rays with 3‑point trace images **all** map to PG(3,2) lines, but only
**16 distinct PG lines** are hit. Only **8 rays** map to **isotropic** PG lines
(4 distinct isotropic lines).

See `artifacts/witting_pg32_ray_line_image.md`.

### 1x) Incidence‑relation search

We classified ray pairs by PG point/line incidence and line intersection
relations and tested all unions; **no union reproduces W33 adjacency**.

See `artifacts/witting_pg32_incidence_relation_search.md`.

### 1y) W33 line → PG(3,2) plane cover map

Among the 16 W33 line unions that contain exactly one PG plane:
- 8 planes are hit by exactly **2** W33 lines
- 7 planes are hit by **0** W33 lines

See `artifacts/witting_pg32_plane_cover_map.md`.

### 1z) PG(3,2) lines hit by Witting rays

The 16 hit lines cover **14** of the 15 PG points (one point uncovered).
Point incidences split as: 8 points with degree 3, 6 points with degree 4.
The line‑intersection graph is **not regular** (degrees 7 or 9).

See `artifacts/witting_pg32_hit_lines_analysis.md`.

### 1aa) Hit‑line spread search

No full spread (5 disjoint lines covering 15 points) and no partial spread
covering 14 points exist inside the 16 hit lines.

See `artifacts/witting_pg32_hit_lines_spread_search.md`.

### 1ab) Configuration invariants (14 points / 16 lines)

Computed bipartite incidence spectrum and degree sequences for the 14‑point,
16‑line configuration induced by the hit lines. The incidence graph is not
regular and does not match a known SRG by spectrum.

See `artifacts/witting_pg32_config_invariants.md`.

### 1ac) Polarity search (GL(4,2) basis changes)

Random basis changes can raise the number of hit lines that are isotropic.
Best found in 10,000 trials: **12** isotropic hit lines (out of 16).

See `artifacts/witting_pg32_polarity_search.md`.

### 1ad) Augmented line set (add missing‑point lines)

Adding the 7 lines through the missing point gives 23 lines total; point
cover counts become {4: 8, 5: 6, 7: 1}, and line‑intersection degrees are
{10, 12, 14} (still non‑regular).

See `artifacts/witting_pg32_augmented_lines_analysis.md`.

### 1ae) Automorphism group (14 points / 16 lines)

The bipartite incidence graph (with point/line partitions fixed) has:

- `|Aut| = 48`
- point orbits: sizes **6** and **8**
- line orbits: sizes **4** and **12**

Allowing point/line swaps does **not** increase the group:

- full automorphism group order: **48**
- no orbit mixes point and line vertices

This indicates the configuration has a modest symmetry group (not highly
transitive) and splits into two natural point/line orbit types.

See `artifacts/witting_pg32_config_aut.md`.

### 1af) GL(4,2) stabilizer of hit lines

The 16 hit lines are preserved by a GL(4,2) subgroup of order **48**. The
stabilizer fixes the missing point (1111) and has the same orbit sizes as
the incidence‑graph automorphism group:

- point orbits: sizes **6** and **8**
- line orbits: sizes **4** and **12**

So the full automorphism group of the configuration appears to be realized
by projective linear transformations of PG(3,2) (no extra graph symmetries).

See `artifacts/witting_pg32_line_stabilizer.md`.

### 1ag) Alternating-form exhaustive search

We enumerated all **28** nondegenerate alternating bilinear forms on F2^4 and
compared their isotropic line sets to the 16 hit lines:

- best hit count: **12** (unique form)
- no form yields 16/16 isotropic hits

This confirms the random polarity search was already optimal (12/16).

See `artifacts/witting_pg32_alternating_form_search.md`.

### 1ah) Quadratic-form rule search (line selection)

We tested all **2048** quadratic forms Q on F2^4 and all subsets of line
selection rules based on the count of Q-values on a line’s 3 points.

Result:
- **no exact rule** reproduces the 16 hit lines
- best overlap includes all 16 hit lines but selects **25** total lines
  (Jaccard = 0.64), for Q with all cross terms = 1 and linear terms = 0

See `artifacts/witting_pg32_quadratic_rule_search.md`.

### 1ai) Line-space (Plücker) analysis

We embedded the 35 PG(3,2) lines into the Klein quadric in PG(5,2) via
6-bit Plücker coordinates and searched for linear/quadratic equations that
cut out exactly the 16 hit lines.

Results:
- **No linear hyperplane** selects exactly the 16 hit lines (best overlap 12/16).
- **No quadratic form** on Plücker coordinates selects exactly the 16 hit lines.
- Best quadratic overlap contains all 16 hit lines but selects **20** total lines
  (Jaccard = 0.80).

See `artifacts/witting_pg32_line_space_plucker.md`.

### 1aj) Line-orbit structure under the stabilizer

The 48-element stabilizer splits the **35** PG(3,2) lines into orbits of sizes
**12, 12, 4, 4, 3**. The 16 hit lines are exactly the union of a **12‑orbit**
and a **4‑orbit**; the remaining **12, 4, 3** orbits are entirely non‑hit.

Point orbits under the same stabilizer are sizes **8, 6, 1**, with the missing
point **1111** forming the fixed 1‑orbit.

See `artifacts/witting_pg32_line_orbit_structure.md`.

### 1ak) Orbit intersection counts

Intersection counts between orbit types are **uniform** (min=max) for every
pair, giving a small association scheme on the 35 lines. For example:

- Each line in the 12‑hit‑orbit meets **5** lines in its own orbit and **8**
  lines in the other 12‑orbit.
- The 4‑hit‑orbit is disjoint from the other 4‑orbit (0 intersections), but
  meets each 12‑orbit in **6** lines.
- The 3‑orbit meets every line in any 4‑orbit (4 intersections each) and has
  2 internal intersections.

This rigid intersection pattern suggests the 16 hit lines form a union of
stabilizer orbits in a small association scheme, rather than a hyperplane or
quadratic section of the Klein quadric.

See `artifacts/witting_pg32_line_orbit_intersections.md`.

### 1al) Orbit incidence table (points ↔ lines)

Incidence counts are uniform within each point orbit, giving a clean orbit
incidence table:

- Points in the **8‑orbit** lie on 3 lines from each 12‑orbit and 1 line from
  one 4‑orbit (the other 4‑orbit/3‑orbit contribute 0).
- Points in the **6‑orbit** lie on 2 lines from each 12‑orbit, 2 lines from the
  other 4‑orbit, and 1 line from the 3‑orbit.
- The **fixed point (1111)** lies on 4 lines from the non‑hit 4‑orbit and 3
  lines from the 3‑orbit (and none of the 12‑orbits).

This strongly constrains how the 16 hit lines (12+4 orbits) distribute across
the 14 covered points.

See `artifacts/witting_pg32_orbit_incidence_table.md`.

### 1am) Line‑orbit point composition

Each line orbit has a fixed point‑orbit composition:

- Both 12‑orbits (hit + non‑hit) consist of lines with **2 points from the 8‑orbit**
  and **1 point from the 6‑orbit**.
- The 4‑hit‑orbit consists of lines entirely inside the **6‑orbit** (composition
  **0,3,0**).
- The 4‑non‑hit‑orbit consists of lines through the fixed point and two 8‑orbit
  points (composition **2,0,1**).
- The 3‑orbit consists of lines through the fixed point and two 6‑orbit points
  (composition **0,2,1**).

This clean orbit‑type description gives a combinatorial characterization of the
16 hit lines: **all 12 lines of one (2,1,0) orbit plus all 4 lines of the (0,3,0)
orbit**.

See `artifacts/witting_pg32_line_orbit_point_composition.md`.

### 1an) Weight‑class characterization + tetrahedral core

Using Hamming weights of PG(3,2) points (in the trace‑map basis), we get a
clean description of the 16 hit lines:

- Point weights: **4 points of weight‑1**, **6 points of weight‑2**, **4 points
  of weight‑3**, and the fixed point **1111** (weight‑4).
- **All 12 lines** with weight pattern **(1,2,3)** are hit.
- **All 4 lines** with weight pattern **(2,2,2)** are hit.
- No other weight patterns appear among hit lines.

The 6 weight‑2 points form a 6‑point / 4‑line subgeometry:

- exactly **4** lines, each with 3 points
- each point lies on **2** of these lines
- every pair of lines intersects in exactly one point

This is precisely the edge–vertex incidence of a **tetrahedron (K4)**: the
6 points correspond to the 6 edges, and the 4 lines correspond to the 4
vertex‑stars (each star = 3 edges through a vertex).

So the user’s “tetrahedron” intuition is real, but only for the **4‑line**
(2,2,2) substructure; the other **12 hit lines** are exactly the (1,2,3) weight
pattern lines.

See `artifacts/witting_pg32_weight_orbit_analysis.md`.

### 1ao) Ray‑level GF(4) rule for line patterns

The trace‑map line pattern is determined **directly** by the multiset of
GF(4) entries in the ray (after projective normalization):

- **Point images**:
  - `(3,1,0,0)` (three zeros, one 1) → single point of weight **1**
  - `(1,3,0,0)` (one zero, three 1s) → single point of weight **3**
- **Line images** (size‑3):
  - `(1,1,1,1)` (one 0 and **one of each** 1, ω, ω²) → line pattern **(2,2,2)**
    — these are exactly the 4 tetrahedral lines.
  - `(1,2,1,0)`, `(1,2,0,1)`, `(1,1,2,0)`, `(1,1,0,2)` (one 0 and a **repeated**
    nonzero) → line pattern **(1,2,3)** (the other 12 hit lines).

So the 16 hit lines are separated by a clean GF(4) combinatorial rule:
**“all‑distinct nonzeros” ⇒ tetrahedral (2,2,2); repeated nonzero ⇒ (1,2,3).**

See `artifacts/witting_pg32_ray_rule_analysis.md`.

### 1ap) Explicit tetrahedral ray map

The 4 tetrahedral lines (pattern (2,2,2)) arise from **8 rays**, two per line.
All 8 rays have entries `{0,1,ω,ω²}` with **all three nonzero values present**.

Each tetrahedral line is hit by exactly **two** rays (the ω/ω² swap):

- `((0,0,1,1),(0,1,0,1),(0,1,1,0))` ← rays 24, 32
- `((0,0,1,1),(1,0,0,1),(1,0,1,0))` ← rays 25, 33
- `((0,1,0,1),(1,0,0,1),(1,1,0,0))` ← rays 26, 34
- `((0,1,1,0),(1,0,1,0),(1,1,0,0))` ← rays 27, 35

See `artifacts/witting_pg32_tetrahedral_rays.md`.

### 1aq) Simple GF(4) invariants (product/sum)

Two very clean invariants on the normalized ray entries separate the line types:

- **Product of nonzero entries**:
  - (2,2,2) tetrahedral rays → product **= 1** (all 8 rays)
  - (1,2,3) line rays → product **= ω or ω²** (12 each)
- **Sum of nonzero entries**:
  - (2,2,2) tetrahedral rays → sum **= 0**
  - (1,2,3) line rays → sum **= 1, 2, or 3** (8 each)

This gives a compact intrinsic rule: **product = 1 (or sum = 0)** picks out the
tetrahedral ray class, while product ≠ 1 captures the (1,2,3) class.

See `artifacts/witting_pg32_ray_invariant_product.md`.

### 1ar) Tetrahedral rays inside W33

Using the Hermitian orthogonality graph to reconstruct all **40** W33 lines:

- Each W33 line contains **0 or 2** tetrahedral rays (never 1,3,4).
- Exactly **16** W33 lines contain **2** tetrahedral rays; **24** contain none.
- Each tetrahedral ray lies on **4** W33 lines (as expected for GQ(3,3)).
- The induced graph on the 8 tetrahedral rays has **16 edges** (degree 4 for each),
  forming a regular 8‑vertex subgraph.

So the tetrahedral class is not just a PG(3,2) artifact: it aligns with a clean
2‑per‑line structure inside W33 itself.

See `artifacts/witting_w33_line_tetrahedron_analysis.md`.

### 1as) Tetrahedral-ray subgraph = K4,4

The induced subgraph on the 8 tetrahedral rays is **bipartite** with a
4‑4 split and **16 edges**, hence isomorphic to **K4,4**.

This gives a very crisp internal structure: the tetrahedral class forms a
complete bipartite subgraph inside W33.

See `artifacts/witting_w33_tetra_subgraph.md`.

### 1au) W33 lines with tetra rays vs trace unions

For the **16** W33 lines that contain **two tetra rays**:

- **4 lines** contain tetra rays that map to the **same** tetra PG line.
  - These have trace‑union size **5**.
- **12 lines** contain tetra rays from **two distinct** tetra PG lines.
  - These have trace‑union size **10**.

By contrast, W33 lines with **0 tetra rays** have union sizes **4, 8, or 10**.

This splits the tetra‑bearing lines into a small “same‑tetra” class (size 4)
and a larger “cross‑tetra” class (size 12), adding a precise trace‑map
signature to the K4,4 substructure.

See `artifacts/witting_w33_line_trace_tetra_analysis.md`.

### 1at) CI fixes (pytest + Sage workflow)

To address GitHub notification failures:

- Added a missing `claude_workspace/run_sage.sh` wrapper so the Sage workflow
  can resolve its script path.
- Fixed `src/PROOF_MINUS_ONE.py` to load data from the repo’s `data/` folder
  instead of a hard-coded local Windows path.
- Updated `tests/test_proofs_execution.py` to skip the external proof script
  if it is not present in this repo.

These changes should stop the Sage workflow from failing on “file not found”
and prevent pytest from failing due to missing local-only data paths.

### 1av) H12 = 4 disjoint triangles (D4 signal)

The H12 neighbor subgraph splits into **four disjoint triangles** (12 vertices,
degree 2 inside H12). The tool checked 5 representative vertices and found the
same 4‑triangle decomposition each time.

This reinforces the D4‑style 4‑fold structure and matches the **24**
eigenvalue‑2 multiplicity (D4 root count).

See `artifacts/d4_w33_structure_analysis.md`.

### 1aw) H27 adjacency fully determined by W33 common neighbors

For the 27 non‑neighbors (H27) of a base vertex:

- H27 is **8‑regular** with **108 edges**.
- Two H27 vertices are adjacent **iff** they share exactly **2** common W33
  neighbors (non‑adjacent pairs share **4**).

This gives a clean combinatorial rule for H27 adjacency.

See `artifacts/h27_jordan_algebra_test.md`.

### 1aw‑b) H27 attaches one-per-triangle to H12

For any base vertex v0, H12 splits into 4 disjoint triangles. Every H27 vertex
is adjacent to **exactly one** vertex in **each** triangle:

- Pattern per H27 vertex: **(1,1,1,1)** (ordered or unordered)
- H27 degree into H12: **4**, uniformly
- This distribution is **identical for all 40 base vertices**

So the H12–H27 incidence is a perfectly balanced 12×27 bipartite structure,
with each H27 vertex picking one vertex from each triangle. This is a strong
triality‑style constraint.

See `artifacts/h12_h27_incidence_patterns.md`.

### 1aw‑c) H27 collapses to 9 tuple types (3‑fold cover)

The triangle‑choice encoding does **not** yield 27 distinct tuples in F3^4.
Instead, it yields exactly **9** distinct tuples, each realized by **3** H27
vertices (regardless of triangle labelings). So H27 is a 3‑fold cover of a
9‑point base.

These 9 tuples form an **affine F3^2 plane** (rank‑2 span), with:

- 12 affine lines inside the 9‑point set
- 1 affine 2‑plane (the set itself)

The 3‑fold fibers are **independent sets** (no edges), and every pair of
distinct fibers has **exactly 3 edges** (a perfect matching across the 3×3).
The quotient graph on the 9 fibers is complete (K9), but with 3‑edge matchings
between each pair.

See `artifacts/h27_triplet_structure.md` and `artifacts/h27_code_invariants.md`.

### 1aw‑c2) Affine plane equations for the 9 tuple types

The 9 distinct tuples satisfy two independent **linear** equations over F3:

- `2x0 + 2x1 + x2 = 0`
- `x0 + 2x1 + x3 = 0`

So the 9 tuple types are exactly an **affine 2‑plane** in F3^4.

See `artifacts/h27_affine_plane_equations.md`.

### 1aw‑c3) Z3‑translation labeling across fibers (exists but not difference‑invariant)

We can label each 3‑vertex fiber by Z3 so that **every** inter‑fiber matching
is a **translation** (i → i + c). Such a labeling exists, but the translation
constant **c** is **not** a function of the affine difference between fibers.

This means the fiber matchings are translation‑structured, but not globally
coordinatized by the F3^2 base plane.

See `artifacts/h27_fiber_translation_structure.md`.

### 1aw‑d) Affine/Latin cube tests (negative under 27‑tuple assumption)

We tested whether a 27‑tuple encoding could be:

- An affine hyperplane in F3^4 (a·x = c), or
- A 3×3×3 Latin cube (one coordinate determined by the other three)

Across all **40** base vertices and **1296** labelings each, **no** solution
exists. This is consistent with the 3‑fold collapse above: the triangle‑choice
pattern inherently yields only **9** distinct tuples.

See `artifacts/h27_affine_hyperplane_search.md` and
`artifacts/h27_latin_cube_search.md`.

### 1ax) Triangle co‑occurrence graph has 240 edges

The triangle co‑occurrence graph (160 triangle vertices) has **240** edges and
degree **3**, with spectrum **3^40, (‑1)^120**. This is the sharpest 240=240
match to E8 roots found so far.

This graph is a **disjoint union of 40 K4 components** (each base vertex gives
one K4 on its four H12 triangles), which explains the spectrum and degree.

The line graph on these 240 edges has degree 4 and a 120‑dimensional nullspace,
which mirrors the 120 root‑line count but is not isomorphic to the E8 root
adjacency graph.

See `artifacts/triangle_e8_correspondence.md`.

### 1ay) λ=2 eigenspace cleanly separates adjacency

Projecting vertices into the λ=2 eigenspace (dimension **24**) yields **exact**
separation:

- Adjacent pairs have inner product **0.1**
- Non‑adjacent pairs have inner product **‑0.0667**

So adjacency is determined purely by λ=2 inner products.

See `artifacts/eigenspace_d4_analysis.md`.

### 1ay‑b) Closed‑form projection formula (explains the separation)

For SRG(40,12,2,4) with eigenvalues {12, 2, −4}, the projector onto λ=2 is:

`P₂ = (2/3) I + (1/6) A − (1/15) J`

So for distinct vertices:

- Adjacent: `P₂(i,j) = 1/10`
- Non‑adjacent: `P₂(i,j) = −1/15`

This exactly matches the observed 0.1 / −0.0667 values and shows the
separation is an intrinsic SRG identity (not an artifact of a particular
numerical basis).

### 1az) Edge projections are root‑like but not E8

The 240 edge‑projection vectors in the λ=2 eigenspace:

- Have identical norm (≈1.1832)
- Have **6** inner‑product values (not the E8 4‑value pattern)
- Fail integrality/closure checks and have **no** antipodal pairs

So the edge system is “root‑like” but **not** an E8 root system.

See `artifacts/edge_root_system_analysis.md`.

### 2) Computed prediction tables (internal consistency)

The summary tables are now computed directly from the formulas in
`FINAL_THEORY_SUMMARY.md`, ensuring the errors are reproducible. The largest
percent errors are the “order-of-magnitude” predictions:

- `rho_Lambda / M_Pl^4`: ~619% (as percentage error)
- `M_Pl / v`: ~200% (as percentage error)

Several entries that were previously tagged “sub-percent” compute to the
1–4% range when derived strictly from the listed formulas/values:

- `m_e`, `m_mu`, `m_d`, and `Delta m^2_21 / Delta m^2_31` land at ~1–4%.

See `artifacts/final_summary_table.md` for the full computed tables.

### 3) Baseline audit (expression search)

The baseline audits indicate many low-complexity expressions can approximate
target values within a few percent, which is important context for multiple-
comparisons risk:

- `data/w33_baseline_audit_results.json` (full grammar)
- `data/w33_baseline_suite_results.json` (strict/medium grammars)

The digest summarizes hit counts at 0.1%, 0.5%, 1%, 5%, 10% tolerances. See
`artifacts/verification_digest.md` for the exact counts.

## Generated/Updated Artifacts

- `artifacts/final_summary_table.md`
- `artifacts/final_summary_table.json`
- `artifacts/verification_digest.md`
- `artifacts/verification_digest.json`
- `SYNTHESIS_ROADMAP_JAN26_2026.md`
- `artifacts/srg40_uniqueness.md`
- `artifacts/srg40_uniqueness.json`
- `artifacts/e8_linegraph_compare.md`
- `artifacts/e8_linegraph_compare.json`
- `artifacts/e8_edge_relation_search.md`
- `artifacts/e8_edge_relation_search.json`
- `artifacts/e8_witting_compare.md`
- `artifacts/e8_witting_compare.json`
- `artifacts/e8_rootline_partition.md`
- `artifacts/e8_rootline_partition.json`
- `artifacts/e8_triple_relation_search.md`
- `artifacts/e8_triple_relation_search.json`
- `artifacts/e8_triple_relation_search_full.md`
- `artifacts/e8_triple_relation_search_full.json`
- `artifacts/e8_partition_search_orthocount_deep.md`
- `artifacts/e8_partition_search_orthocount_deep.json`
- `artifacts/e8_partition_search_fullip_limited.md`
- `artifacts/e8_partition_search_fullip_limited.json`
- `artifacts/e8_partition_search_pattern_filter.md`
- `artifacts/e8_partition_search_pattern_filter.json`
- `artifacts/e8_triple_relation_search_composite.md`
- `artifacts/e8_triple_relation_search_composite.json`
- `artifacts/witting_trace_map_pg32.md`
- `artifacts/witting_trace_map_pg32.json`
- `artifacts/witting_trace_map_pg32_full.md`
- `artifacts/witting_trace_map_pg32_full.json`
- `artifacts/witting_pg32_fiber_analysis.md`
- `artifacts/witting_pg32_fiber_analysis.json`
- `artifacts/witting_pg32_ray_trace.md`
- `artifacts/witting_pg32_ray_trace.json`
- `artifacts/witting_pg32_full_fiber_counts.md`
- `artifacts/witting_pg32_full_fiber_counts.json`
- `artifacts/witting_pg32_fiber_graphs.md`
- `artifacts/witting_pg32_fiber_graphs.json`
- `artifacts/witting_pg32_relation_search.md`
- `artifacts/witting_pg32_relation_search.json`
- `artifacts/witting_pg32_line_relation.md`
- `artifacts/witting_pg32_line_relation.json`
- `artifacts/witting_pg32_plane_relation.md`
- `artifacts/witting_pg32_plane_relation.json`
- `artifacts/witting_pg32_ray_line_image.md`
- `artifacts/witting_pg32_ray_line_image.json`
- `artifacts/witting_pg32_incidence_relation_search.md`
- `artifacts/witting_pg32_incidence_relation_search.json`
- `artifacts/witting_pg32_plane_cover_map.md`
- `artifacts/witting_pg32_plane_cover_map.json`
- `artifacts/witting_pg32_hit_lines_analysis.md`
- `artifacts/witting_pg32_hit_lines_analysis.json`
- `artifacts/witting_pg32_hit_lines_spread_search.md`
- `artifacts/witting_pg32_hit_lines_spread_search.json`
- `artifacts/witting_pg32_config_invariants.md`
- `artifacts/witting_pg32_config_invariants.json`
- `artifacts/witting_pg32_config_aut.md`
- `artifacts/witting_pg32_config_aut.json`
- `artifacts/witting_pg32_line_stabilizer.md`
- `artifacts/witting_pg32_line_stabilizer.json`
- `artifacts/witting_pg32_alternating_form_search.md`
- `artifacts/witting_pg32_alternating_form_search.json`
- `artifacts/witting_pg32_quadratic_rule_search.md`
- `artifacts/witting_pg32_quadratic_rule_search.json`
- `artifacts/witting_pg32_line_space_plucker.md`
- `artifacts/witting_pg32_line_space_plucker.json`
- `artifacts/witting_pg32_line_orbit_structure.md`
- `artifacts/witting_pg32_line_orbit_structure.json`
- `artifacts/witting_pg32_line_orbit_intersections.md`
- `artifacts/witting_pg32_line_orbit_intersections.json`
- `artifacts/witting_pg32_orbit_incidence_table.md`
- `artifacts/witting_pg32_orbit_incidence_table.json`
- `artifacts/witting_pg32_line_orbit_point_composition.md`
- `artifacts/witting_pg32_line_orbit_point_composition.json`
- `artifacts/witting_pg32_weight_orbit_analysis.md`
- `artifacts/witting_pg32_weight_orbit_analysis.json`
- `artifacts/witting_pg32_ray_rule_analysis.md`
- `artifacts/witting_pg32_ray_rule_analysis.json`
- `artifacts/witting_pg32_tetrahedral_rays.md`
- `artifacts/witting_pg32_tetrahedral_rays.json`
- `artifacts/witting_pg32_ray_invariant_product.md`
- `artifacts/witting_pg32_ray_invariant_product.json`
- `artifacts/witting_w33_line_tetrahedron_analysis.md`
- `artifacts/witting_w33_line_tetrahedron_analysis.json`
- `artifacts/witting_w33_tetra_subgraph.md`
- `artifacts/witting_w33_tetra_subgraph.json`
- `artifacts/witting_w33_line_trace_tetra_analysis.md`
- `artifacts/witting_w33_line_trace_tetra_analysis.json`
- `artifacts/d4_w33_structure_analysis.md`
- `artifacts/d4_w33_structure_analysis.json`
- `artifacts/h27_jordan_algebra_test.md`
- `artifacts/h27_jordan_algebra_test.json`
- `artifacts/d4_triality_action.md`
- `artifacts/d4_triality_action.json`
- `artifacts/triangle_e8_correspondence.md`
- `artifacts/triangle_e8_correspondence.json`
- `artifacts/d4_d4_e8_decomposition.md`
- `artifacts/d4_d4_e8_decomposition.json`
- `artifacts/eigenspace_d4_analysis.md`
- `artifacts/eigenspace_d4_analysis.json`
- `artifacts/edge_root_system_analysis.md`
- `artifacts/edge_root_system_analysis.json`
- `artifacts/h27_affine_hyperplane_search.md`
- `artifacts/h27_affine_hyperplane_search.json`
- `artifacts/h27_latin_cube_search.md`
- `artifacts/h27_latin_cube_search.json`
- `artifacts/h27_code_invariants.md`
- `artifacts/h27_code_invariants.json`
- `artifacts/h27_triplet_structure.md`
- `artifacts/h27_triplet_structure.json`
- `artifacts/h27_fiber_translation_structure.md`
- `artifacts/h27_fiber_translation_structure.json`
- `artifacts/h27_affine_plane_equations.md`
- `artifacts/h27_affine_plane_equations.json`
- `artifacts/h12_h27_incidence_patterns.md`
- `artifacts/h12_h27_incidence_patterns.json`
- `artifacts/witting_pg32_polarity_search.md`
- `artifacts/witting_pg32_polarity_search.json`
- `artifacts/witting_pg32_augmented_lines_analysis.md`
- `artifacts/witting_pg32_augmented_lines_analysis.json`
- `EXTERNAL_E8_FINITE_GEOM_NOTES.md`
- `artifacts/qutrit_pauli_w33.md`
- `artifacts/qutrit_pauli_w33.json`

## Limitations

- CXVIII output can be large; use `W33_VERBOSE=1` only when you want full
  candidate-subgraph traces.

## Suggested Next Steps

If you want fresh Sage verification outputs:

- `python3 sage_verify.py`

Or via Docker:

- `docker run --rm -v "$(pwd)":/work -w /work -e W33_FAST=1 sagemath/sagemath:10.7 bash -lc "scripts/run_all_sage.sh"`

---

This report is meant to be checked into the repo as a snapshot of the current
verification status and computed-table consistency.
