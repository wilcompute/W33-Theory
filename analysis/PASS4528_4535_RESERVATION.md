# Passes 4528--4535 executed outcomes

This lane executes the five strongest non-sequential next steps stated after Pass 4519 plus three independent outside-the-box probes, while preserving the concurrently reserved Passes 4520--4527 lane.

## 4528 — complete Borel overgroup interval
Exact H-double-coset sizes are `162,486,486,1458,1458,4374,4374,13122`.  Every overgroup containing the canonical order-162 flag/Borel is exactly one of `H`, the order-648 point parabolic, the order-648 line parabolic, or all of `PSp(4,3)`.  Section ranks are respectively `384/384`, `387/388`, `386/387`, and `389/390`.  Thus H is the unique splitting group in its complete overgroup interval and is maximal by inclusion there.  Boundary: this is not a census of unrelated subgroup conjugacy classes.

## 4529 — rank-two obstruction compass
The exact radical cohomology `H^1(PSp(4,3),K/J)=F2^2` is coordinatized by `e_P=fixed_line` and `e_L=sum`; the third nonzero class is `second=e_P+e_L`.  Point and line parabolics kill the distinct axes `<e_P>` and `<e_L>`, while their incident Borel kills the whole two-space.  This is a conceptual coordinate theorem for the computed restriction barcode, not a general Ext theorem.

## 4530 — symbolic Q(5,q) protected law
For `Q(5,q)=GQ(q,q^2)` with `q ≡ 3 (mod 4)`, the general apartment formula gives `HH^T=N^T N` over F2 for the entire family.  With `h(q)=rank_2 H` and `rho(q)=rank_2(N^T N)`, the protected quotient has exact dimension `rho(q)` and the apartment radical dimension is `h(q)-rho(q)`.  Counts are symbolic, including `(q^2+1)(q^3+1)q^6(q+1)/8` apartments.  The q=3 anchor is `(h,rho,radical)=(279,70,209)`.  No closed rank polynomial is guessed from one anchor.

## 4531 — exact nine-clock flag-gauge compiler
The Pass-4504 optimum has 42 source-line/quotient-column incidences.  In the stated single-port bipartite model, maximum degree is 9, so depth is at least 9; a frozen conflict-free 9-round schedule achieves it.  Hence 42 primitive XOR routes compile in exactly 9 clocks in that model, with instantaneous source fanout one.  No FPGA/optical PPA or alternate-hardware optimum is claimed.

## 4532 — Borel/local-cell fusion of the protected 240 edges
The Pass-4513 protected dual-W33 edge action decomposes under the Borel into orbit sizes `3,3,9,9,27,27,81,81 = 2(3+9+27+81)`.  The 13-line `K1 join 4K3` gauge cell contains exactly the four smallest orbits, 24 edges total; 108 edges cross its boundary and 108 are wholly exterior.  The 24 internal edges are 12 center spokes plus 12 triangle edges.

## 4533 — outside box: power-of-three Borel staircase
Line vertices split as `1,3,9,27`; protected edges split as two copies of `3,9,27,81`; edge stabilizers fall as `54,18,6,2`.  This is an exact finite orbit filtration aligned with the order-81 Sylow core.  No physical scale/Bruhat-length interpretation is asserted without an additional theorem.

## 4534 — outside box: nine local spokes saturate the edge-accessible H10 layer
All 240 protected edge images `A_*(e_i+e_j)` span dimension 9, not 10.  Since Pass 4496 proves the unique invariant-submodule lattice `0<1<9<10`, the full edge span is exactly the unique 9D submodule of H10.  Yet the 24 internal cell edges already span rank 9, and even the 12 center spokes do; nine explicitly frozen spokes form a basis.  Thus one local Borel cell is complete for the edge carrier, while the tenth protected direction lies outside the entire 240-edge family.

## 4535 — outside box: spectrally complete eight-state edge quotient
The line graph of the 240 protected edges is 22-regular.  The eight Borel edge orbits form an equitable 8x8 quotient with characteristic polynomial `(x-22)(x-12)^2(x-6)(x+2)^4`.  The full 240-state line graph is annihilated by `(L-22I)(L-12I)(L-6I)(L+2I)`, so the quotient contains every distinct full-graph eigenvalue `{22,12,6,-2}`.  This is exact spectral compression, not a physical Hamiltonian/decoder claim.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4528_*.py` through `analysis/w33_pass4535_*.py`.
- Frozen JSON certificates: `data/PART_W33_PASS4528_*.json` through `data/PART_W33_PASS4535_*.json`.
- Manuscript insert: `analysis/PASS4528_4535_borel_building_compiler_edge_insert.tex`, chained after Pass 4519 and therefore inherited by all three maintained manuscript front doors.
- Public page/card updated and registered; the narrow index materializer can add the new card without touching unrelated website content.
- Regression test and focused Actions workflow installed; the workflow reruns all eight witnesses and semantically compares regenerated JSON against the frozen certificates.

Evidence discipline remains unchanged: preserve the Pass-4503 correction, do not identify the 240-set with E8 from cardinality, do not turn graph locality into spacetime locality, do not infer physical dynamics from an equitable quotient, and do not use literature-search absence as a novelty proof.
