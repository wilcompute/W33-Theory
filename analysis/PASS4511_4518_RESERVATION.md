# Passes 4511--4518 executed outcome

This eight-front continuation was reserved after reconciling the parallel 4503--4510 block. All eight fronts were executed with exact certificates or explicit fail-closed frontiers.

- **4511 — CLOSED.** The 84,240 weight-4 dual words span rank 1,580, exactly the even-weight subcode of the 1,581-dimensional dual. Together with any odd triangular-prism weight-3 word they generate all of `C^perp`. One regular PSp orbit of 25,920 weight-4 relations already spans the complete even dual sector and supplies all 366 dimensions missing from the prism span.
- **4512 — EXACT REDUCTION; NUMERICAL ENUMERATOR OPEN.** For coefficient subset `S`, `wt=162m-12*C(m,2)-42e+12p3-8c4`. Burnside leaves 10,789,604 exact PGSp+complement codeword orbits. The complete coefficient table has not yet been accumulated and must remain labelled open.
- **4513 — CLOSED.** The protected prism 240-orbit is explicitly the dual-W33 edge action: `protected(prism)=A_*(e_i+e_j)` for a unique adjacent pair. Every edge has exactly nine prism preimages.
- **4514 — CLOSED THROUGH LENGTH 8.** Primitive signed Ihara coefficients C6, C7, C8 have exact parity-support decompositions with 10, 26, and 142 nonzero PSp support orbits. The degree-2 Walsh layer of C6 is 252 on adjacent pairs and 48 on disjoint pairs, hence reconstructs `A_*` exactly.
- **4515 — PARTIAL EXACT FRONTIER.** For `Q(5,3)=GQ(3,9)`, `wt=1458m-12*C(m,2)-150e+36p3-8c4`; supports 2--12 cannot beat a line word, so any counterexample to `d=1458` lies at gauge-fixed support 13--140. Equality remains open. The dual minimum distance is exactly 3 with 544,320 triangular-prism words. Pass 4506 retains ownership of the separate 70-dimensional apartment/protected quotient.
- **4516 — CLOSED, outside-box.** The nine prism preimages over one edge carry an affine `C3^2:C4` action of order 36 from the order-108 edge stabilizer, with kernel `C3`.
- **4517 — CLOSED, outside-box.** One weight-4 relation with trivial PSp stabilizer has a 25,920-element orbit spanning the full 1,580-dimensional even dual code.
- **4518 — CLOSED, outside-box.** The quadratic Walsh layer of primitive C6 is `48*(J-I)+204*A_*`, so length-six graph-zeta data reconstructs dual-W33 adjacency independently.

Evidence files:
- `analysis/w33_pass4511_4514_dual_even_prism_ihara.py`
- `analysis/w33_pass4512_apartment_weight_enumerator_reduction.py`
- `analysis/w33_pass4515_q53_apartment_code_frontier.py`
- `data/PART_W33_PASS4511_4518_DUAL_EVEN_PRISM_IHARA.json`
- `data/PART_W33_PASS4512_APARTMENT_WEIGHT_ENUMERATOR_REDUCTION.json`
- `data/PART_W33_PASS4515_Q53_APARTMENT_CODE_FRONTIER.json`
- `analysis/PASS4511_4518_dual_enumerator_ihara_q53_insert.tex`
- `docs/apartment-dual-enumerator-ihara-q53.html`
- `.github/workflows/w33_pass4511_4518_dual_enumerator_ihara_q53.yml`

Evidence discipline is unchanged: no cardinality-only identifications, no physical interpretation from finite code/group facts, no claim that the full W33 numerical enumerator or the Q(5,3) distance equality is closed.
