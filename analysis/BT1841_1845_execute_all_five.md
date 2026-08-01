# Passes 1841–1845 — second signature orbit, higher packing suborbits, second no-lift, elementary-abelian witness geometry, and the outer quotient

## Executive result

All five requested fronts were executed against the complete 720-signature model and the certified 327 cover-orbit census.

1. **A second exact nine-signature orbit exists.** Besides the known orbit of size 2,880 with stabilizer order 9 and class composition `6T128+3T96`, an orbit-blocked exact binary MILP found a free orbit of size 25,920 with class composition `3T128+2T120+2T104+2T96`. Thus there are at least two inner solution orbits and at least 28,800 distinct signature-level resolutions.
2. **The certified chiral four-packing family has a free higher-packing action.** Its six pair-subpackings, four triple-subpackings, and one four-packing each generate separate full-size `PSp(4,3)` orbits. This yields 155,520 pairs, 103,680 triples, and 25,920 quadruples in that family. Every one of those inner subpacking orbits is exchanged with a distinct outer mirror orbit.
3. **The new free signature orbit does not lift.** Its nine candidate-cover classes have sizes
   `11664, 2808, 864, 864, 11664, 288, 288, 2808, 11664`.
   The deterministic nine-partite exact search returns `UNSAT` after 289 nodes and 288 dead ends, with trace `ee79a871c5609103`.
4. **The order-nine stabilizer is `C3 × C3`, not cyclic `C9`.** It has three 3-point orbits: two `T128` triangles and one `T96` triangle. On the six `T128` signatures, inner product 74 is exactly `2K3`, while inner product 70 is exactly `K3,3`; all remaining 21 pairs have inner product 78.
5. **The canonical outer involution fixes both certified inner signature orbits.** The stabilized group over the 2,880-orbit is `C3 × S3` of order 18, with element-order histogram `1^1 2^3 3^8 6^6`. The free inner orbit acquires a `C2` setwise stabilizer in `PGSp`.

## Pass 1841 — exact second-orbit frontier

The known solution orbit was blocked by all 2,880 of its supports. HiGHS then found a second exact binary solution after 3,786 branch nodes. Its setwise stabilizer is trivial, so its inner orbit has the full group size 25,920. Its pairwise Gram histogram is distinct from the first orbit, and the canonical support hashes differ.

Multiplicity probes with a repeated representative were exact `INFEASIBLE` for `T128`, `T120`, and `T104`. The repeated-`T96` probe and a proof of no third binary orbit both exceeded their exact time limits. Therefore Pass 1841 is a rigorous frontier, not a complete orbit census.

## Pass 1842 — pair/triple/quadruple suborbits in the certified chiral family

The previously certified four-packing has trivial setwise stabilizer in `PSp(4,3)`. Consequently its six unordered pairs, four unordered triples, and the full quadruple are not identified by inner symmetry. Direct orbit construction gives:

- six pair orbits of size 25,920;
- four triple orbits of size 25,920;
- one quadruple orbit of size 25,920.

The canonical outer similitude sends every one of these 11 inner orbits to a distinct mirror orbit. This completely resolves the higher-packing orbit structure **inside this certified chiral family**, but not globally over all disjoint cover triples and maximal four-packings.

## Pass 1843 — proof-producing no-lift for the free signature orbit

The complete 327-orbit cover census was expanded under the 25,920 frame actions and filtered against the nine target signatures. The deterministic MRV backtracking search exhausts the resulting nine-partite instance in 289 nodes. The exact candidate binary has SHA-256

`e78d18aec34eafcdf483d94b1e5568ab16daf1950ab355c30c4657166b1bf470`.

Together with Pass 1835, two distinct inner signature-resolution orbits—2,880 plus 25,920 solutions—are now proved not to lift. This is not global nine-cover `UNSAT`, because the signature-resolution orbit census remains incomplete.

## Pass 1844 — intrinsic `C3 × C3` and Gram geometry

All eight nonidentity setwise stabilizer elements have order three. The action has exactly three point-orbits of size three. The first two are the two `T128` triangles and the third is the `T96` triangle. The Gram labels then become forced:

- the two internal triangle edge sets carry inner product 74 (`2K3`, six edges);
- all cross-edges between the `T128` triangles carry inner product 70 (`K3,3`, nine edges);
- the `T96` triangle and every `T96`–`T128` edge carry inner product 78 (21 edges total).

This explains both the order-nine stabilizer and the `70/74/78` histogram without spectral extrapolation.

## Pass 1845 — outer-equivariant quotient

For each certified inner signature orbit, the canonical outer image lies back in the same inner orbit. Hence neither orbit fuses with a distinct inner orbit in `PGSp`.

For the first orbit, adjoining an outer-coset stabilizer element to `C3 × C3` gives a group of order 18 with center order three and order histogram `1^1 2^3 3^8 6^6`, identifying it as `C3 × S3`. For the free inner orbit, the extended setwise stabilizer has order two.

## Verification and evidence boundary

The frozen verifier checks all five certificate self-hashes, reconstructs the 720 signatures, rebuilds the 25,920-element signature action, recomputes both orbit sizes, reconstructs the certified packing suborbits, verifies the `C3 × C3` Gram geometry, and reruns the second exact no-lift worker. The focused regression invokes the frozen verifier; CI invokes the full worker.

Open boundaries:

- complete the binary orbit census and settle repeated `T96` signatures;
- classify all disjoint cover triples and maximal four-packings, not only the certified chiral family;
- continue proof-producing lifts for every newly found signature orbit;
- derive the `C3 × S3` extension directly from the anchor `K4,4,4` model;
- classify the canonical outer action on the eventual complete signature-resolution orbit set.
