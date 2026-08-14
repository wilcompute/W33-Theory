# Passes 5110–5117 — cut gauge, intrinsic charts, radius-3 decoding, sqrt(17) order ladder, and three outside-box probes

**Status:** EXECUTED 2026-08-14. This packet is now fully materialized and collision-reconciled against Passes 5118–5125. The q=5/all-q distance theorem remains open.

## 5110 — chamber-generator gauge is exactly the Levi cut space
For every W(3,q), the kernel of chamber coefficients acting on apartment coordinates is exactly `Cut(Levi;F2)`. Panel-star relations give the inclusion, connectedness gives cut dimension `|V|-1`, and Pass5066 supplies apartment-code rank `q^4`, forcing equality. Hence each apartment-code word is a Levi edge cochain modulo cuts, and its minimum chamber-generator representative is cut-minimal.

## 5111 — first q=5 low-leader barrier
Cut-minimality in the 6-regular q=5 Levi graph forces selected degree at most three. Combining girth eight with exact chamber-star pair intersections proves every representative of size at most 13 has apartment weight at least 625, so any `<625` counterexample has leader at least 14. **Reconciliation:** Pass5118 subsequently strengthens this to leader at least 17; Pass5111 remains the first cut/girth barrier but is no longer the frontier bound.

## 5112 — code-only reconstruction of roots and opposite-pair charts
From the complete dual weight-3 shell, reconstruct theta checks; from genuine Tanner six-cycles, recover the q-apartment geodesic-root blocks; from a theta triple, recover the unique q+1-root opposite-pair chart. This is a finite-GQ graph theorem and was replayed exactly at q=2,3,4. Therefore local `K_(q+1)` tester/decoder placement is intrinsic to the apartment code and needs no external point/line labels.

## 5113 — q=3 global equivariant decoding radius rises to three
Replace the arbitrary ambiguous local K4 syndrome leader by an S4-equivariant rule: the six unique weight-one syndromes vote; the unique three-way weight-two tie abstains. Apartment transitivity reduces the global weight-three census to all `C(1619,2)=1,309,771` triples containing one fixed apartment. Every triple clears within two sweeps: 1,261,801 clear immediately, 47,520 leave residual weight two, and 450 leave residual weight one; second-sweep failures are zero. The guaranteed finite hard-decision radius is therefore three.

## 5114 — conductor 1→2→4 is an actual nested sqrt(17) lattice tower
With `lambda=(1+sqrt(17))/2`, the natural orders are `O_K`, `Z+2O_K`, and `Z+4O_K`, with discriminants `17,68,272`. Natural inclusion matrices have per-lane indices `2,2,4`; across the fifteen Levi-kernel lanes the global indices are `2^15,2^15,4^15`. This completes the arithmetic order ladder connecting the maximal-order Hecke block, the global theta quadratic carrier, and the q=3 recurrence lattice.

## 5115 — q=5 native root-coset arithmetic defect
The C2 root-coset incidence ranks are exact: q2 `15/15`, q3 generic/native `69/68`, q5 generic/native `405/397`. Thus q=5 has an eight-dimensional defining-characteristic rank drop. The two odd anchors q=3,5 tempted the formula `((q-1)/2)^3`; **Pass5123 later kills it** by finding q7 generic/native ranks `1183/1173`, drop 10 rather than 27. The exact q2/q3/q5 rank theorem survives; the extrapolation does not.

## 5116 — the q=3 code reconstructs its own local U81⋊V4 controller
Primal minima recover the 160 chambers and Levi building; dual minima recover theta; Pass5112 recovers the 1080 charts; choosing one reconstructed chamber yields its 81 apartment support and 108 active 3-charts; Pass5098 identifies that hypergraph with C2 positive-root cosets; Pass5099 identifies its full automorphism group as `U81 semidirect V4`, order 324. With Pass5105, the two index-three subgroups are the extraspecial H27 state torsor and flat F3^3 program torsor, with protected module `H1(F3)|U ~= F3[U]`. Point/line naming remains determined only up to the natural dual swap.

## 5117 — the two apartment presentations are perfect duals
Pass5110 gives the code as Levi edge cochains modulo cuts, while Pass5066 gives oriented/binary apartment generators modulo theta as the Levi cycle space. Since `Cut=Z1^perp`,

`F2^E / Cut ~= Hom_F2(Z1,F2)`.

Thus the apartment code is canonically the full character group of the apartment/theta presentation, with pairing `[g],[A] -> g·boundary(A)`. This is quotient-versus-dual perfect pairing, not a claim that the cycle space is orthogonally self-dual; bicycle/radical intersections may remain nonzero.

## Reconciliation with Passes 5118–5125
Pass5118 strengthens the q=5 leader wall to 17. Pass5119 recasts codeword supports as half-regular subsets of the intrinsic theta graph. Pass5120 adds explicit polynomial state/program coordinates on U81. Pass5123 falsifies the naive q=3,5 native-rank extrapolation. Pass5125 identifies the q=3 torsion defect with the triality-center module. These are complementary continuations rather than replacements for the exact theorems above.

## Evidence boundary
No q=5 or all-q minimum-distance theorem is claimed. Radius four decoding is open. Decoder results are finite hard-decision code statements, not physical noise or fault-tolerance thresholds. The sqrt(17) order tower is an arithmetic/lattice theorem and does not create a historical-object-to-W33 geometric bijection.
