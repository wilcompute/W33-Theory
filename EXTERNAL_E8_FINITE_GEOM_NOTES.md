# External Notes: E8 + Finite Geometry (Jan 26, 2026)

This note summarizes external sources explored for E8/Witting/finite-geometry
connections and records the current integration attempts in this repo.

## F.G. Marcelis (E8 series)

Key points observed in the E8 series:

- **E8 slices & projections**: E8 roots (240) are visualized via icosahedral
  slices; projections show multiple triacontagons and a 120-point subset
  associated with a 600-cell. These sections emphasize 4D subspace structure
  inside E8 and the 120/120 split of roots.

- **Witting → PG(3,2)**: The Witting polytope is described with coordinates in
  GF(4), and a **trace map GF(4) → GF(2)** is used to map its vertices into
  the 15 points of **PG(3,2)**. The article notes that the 240 vertices map
  with multiplicity to those 15 points.

- **Generalized hexagon**: A generalized hexagon **GH(2,2)** appears in a
  configuration derived from the E8 root system; the **Heawood graph** is used
  to describe 14 points and 21 lines in that configuration.

References (URLs in code block):

```
https://fgmarcelis.wordpress.com/e8-part-1/
https://fgmarcelis.wordpress.com/e8-part-2/
https://fgmarcelis.wordpress.com/e8-part-3/
https://fgmarcelis.wordpress.com/e8-8-diameters-of-witting-polytope-into-pg32/
https://fgmarcelis.wordpress.com/e8-16-a-generalized-hexagon-2-2/
```

## PG(3,2) §5 (Generalized Quadrangle) — Marcelis

Key points from the PG(3,2) §5 page:

- The smallest generalized quadrangle **GQ(2,2)** has **3 points per line**
  and **3 lines per point**.
- The configuration has **6 spreads**, and each line lies in **2 spreads**.
- Each GQ(2,2) line incident structure can be extended to a **GQ(4,2)**
  in GF(4) with 45 points and 27 lines (as described by the page).

Reference:

```
https://fgmarcelis.wordpress.com/pg32/pg32-%C2%A7-5-generalized-quadrangle/
```

## Finitegeometry.org /sc/ (Small Configurations)

The `finitegeometry.org/sc/` site was identified as a key resource. The page
requests timed out from within this environment, so it was not fully crawled.
We will retry or use a mirror if available.

Reference:

```
http://finitegeometry.org/sc/
```

## Formal PG(3,2) Sources (Counts, Spreads)

Two primary references confirm the basic PG(3,2) parameters used here:

- **PG(3,2) has 15 points and 35 lines** (formalized in Coq).
- **Spreads in PG(3,2)** consist of 5 disjoint lines covering all 15 points;
  the spreads/packings enumeration is used in a formalization project.

References:

```
https://drops.dagstuhl.de/opus/volltexte/2021/14669/
https://publis.icube.unistra.fr/1000015210/1/Spreads_and_Packings_in_PG_3_2.pdf
```

## Integration Tests in This Repo

1) **Trace-map test (GF(4) → GF(2))**
   - Script: `tools/witting_trace_map_pg32.py`
   - Result: using 40 base states in GF(4) and coordinatewise trace, we got
     **6 unique projective points**, not the expected 15. This suggests our
     modeled vertex set is incomplete for the Marcelis trace-map construction.
   - Artifact: `artifacts/witting_trace_map_pg32.md`

2) **Trace-map test (full 240 Witting vertices)**
   - Script: `tools/witting_trace_map_pg32_full.py`
   - Result: **15 unique GF(2) points**, each with multiplicity **16**,
     including the (0,0,0,0) vector. This matches the Marcelis statement that
     the 240 vertices map 16-to-1 onto the 15 PG(3,2) points (with 0000 replaced
     by 1111 in projective space).
   - Artifact: `artifacts/witting_trace_map_pg32_full.md`

3) **Ray trace map (40 rays under GF(4) scalars)**
   - Script: `tools/witting_pg32_ray_trace.py`
   - Result: 8 rays map to a single PG point; 32 rays map to 3 points. One
     PG(3,2) point is not hit by ray images. W33 lines map to PG unions of
     sizes 4, 5, 8, or 10.
   - Artifact: `artifacts/witting_pg32_ray_trace.md`

4) **Fiber multiplicities & orthogonality cores**
   - Scripts: `tools/witting_pg32_full_fiber_counts.py`,
     `tools/witting_pg32_fiber_graphs.py`
   - Result: each PG fiber has 16 vertices but only 8 unique GF(4) vectors.
     The 8‑vertex orthogonality graphs are not uniform cubes (degree sets vary).
   - Artifacts: `artifacts/witting_pg32_full_fiber_counts.md`,
     `artifacts/witting_pg32_fiber_graphs.md`

5) **Ray line images and incidence relations**
   - Scripts: `tools/witting_pg32_ray_line_image.py`,
     `tools/witting_pg32_incidence_relation_search.py`
   - Result: 32 rays map to PG lines (16 distinct lines); 8 rays map to
     isotropic lines (4 distinct). No union of PG incidence relations matches
     W33 adjacency.
   - Artifacts: `artifacts/witting_pg32_ray_line_image.md`,
     `artifacts/witting_pg32_incidence_relation_search.md`

6) **PG plane cover map**
   - Script: `tools/witting_pg32_plane_cover_map.py`
   - Result: of the 15 PG planes, 8 are covered by exactly 2 W33 lines,
     and 7 are uncovered (among the 16 W33 lines that contain exactly one plane).
   - Artifact: `artifacts/witting_pg32_plane_cover_map.md`

7) **PG line subset induced by ray images**
   - Script: `tools/witting_pg32_hit_lines_analysis.py`
   - Result: 16 PG lines hit, covering 14 of 15 points; point degrees are 3 or 4.
     The line‑intersection graph is not regular (degrees 7 or 9).
   - Artifact: `artifacts/witting_pg32_hit_lines_analysis.md`

8) **Hit‑line spread search**
   - Script: `tools/witting_pg32_hit_lines_spread_search.py`
   - Result: no spread or 14‑point partial spread exists inside the 16 hit lines.
   - Artifact: `artifacts/witting_pg32_hit_lines_spread_search.md`

9) **Configuration invariants + polarity search**
   - Scripts: `tools/witting_pg32_config_invariants.py`,
     `tools/witting_pg32_polarity_search.py`
   - Result: 14‑point/16‑line incidence graph has mixed degrees and non‑SRG spectrum;
     GL(4,2) polarity search can make up to 12 of 16 hit lines isotropic.
   - Artifacts: `artifacts/witting_pg32_config_invariants.md`,
     `artifacts/witting_pg32_polarity_search.md`

10) **Augmented line set**
    - Script: `tools/witting_pg32_augmented_lines_analysis.py`
    - Result: adding the 7 lines through the missing point yields 23 lines total;
      line‑intersection degrees {10,12,14}.
    - Artifact: `artifacts/witting_pg32_augmented_lines_analysis.md`

11) **Configuration automorphisms + GL(4,2) stabilizer**
    - Scripts: `tools/witting_pg32_config_aut.sage`,
      `tools/witting_pg32_line_stabilizer.py`
    - Result: automorphism group order 48; same order realized by GL(4,2)
      stabilizer; no point/line swaps in the full graph automorphism group.
    - Artifacts: `artifacts/witting_pg32_config_aut.md`,
      `artifacts/witting_pg32_line_stabilizer.md`

12) **Alternating/quadratic form searches**
    - Scripts: `tools/witting_pg32_alternating_form_search.py`,
      `tools/witting_pg32_quadratic_rule_search.py`
    - Result: best alternating form hits 12/16 (no exact); quadratic rule
      search finds no exact count-based selection rule.
    - Artifacts: `artifacts/witting_pg32_alternating_form_search.md`,
      `artifacts/witting_pg32_quadratic_rule_search.md`

2) **E8 root-line triple partitions**
   - We found a partition of the 120 E8 root lines into 40 orthogonal triples
     (octahedra), but none of the tested block relations reproduce SRG(40,12,2,4).
   - See `artifacts/e8_rootline_partition.md` and related search artifacts.
