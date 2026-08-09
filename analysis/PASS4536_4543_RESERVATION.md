# Passes 4536--4543 executed outcomes

This lane executes the five strongest next steps after Passes 4528--4535, cross-fused with the completed concurrent Passes 4520--4527 lane, plus three independent outside-the-box attacks.

## 4536 — the missing tenth protected direction is coefficient parity
The protected edge vectors `A_*(e_i+e_j)` are images of the connected line graph's even coefficient hyperplane.  The entire kernel of `A_*` is even, so
`pi(A_* b)=sum b mod 2` is well defined on `H10=im(A_*)`.  Its kernel is exactly the 9D edge layer `V9`.  Any single line-star supplies the missing direction.  Exhausting all 1024 protected vectors gives
`pi=0: 1 + 135 z^16 + 240 z^20 + 135 z^24 + z^40` and
`pi=1: 40 z^12 + 432 z^20 + 40 z^28`.
The 240 even weight-20 vectors are exactly the edge shell; the 40 odd minimum weight-12 vectors are exactly the line-stars.

## 4537 — exact q=7 rank anchor, but the all-q formula remains open
An independent elliptic-quadric builder gives `Q^-(5,7)=GQ(7,49)` with 2752 points and 17200 lines, `rank_2 N=2451`, `dim ker N^T=301`, and `rank_2(N^T N)=2150`.  Together with q=3, both anchors match
`rho(q)=(q^2+1)(q^2-q+1)=|L|/(q+1)` and `dim ker N^T=q(q^2-q+1)`.  For every odd q the line-graph SRG parameters are even, so `A_*^2=0` over F2 exactly.  The compact closed-rank formula is recorded as a conjecture, not promoted to an infinite theorem.

## 4538 — global maximum splitting order is 162
Pass 4503 already makes all five maximal subgroup types nonsplit.  Standard subgroup structure of those maximals reduces every remaining proper subgroup class above order 162 to seven large types of orders `360,324,288,216,216,192,192`.  Exact representatives have inconsistent section systems `386/387,386/387,386/387,385/386,386/387,385/386,380/381`.  Hence every subgroup of order greater than 162 is nonsplit, while the canonical order-162 chamber/Borel splits.  Boundary: completeness of the order reduction uses standard finite-group subgroup classification; the executable independently verifies representatives and section ranks.

## 4539 — exact ten-sample local decoder
One local line-star plus the nine Pass-4534 center spokes form a basis of all H10.  Ambient coordinates `[0,1,2,3,4,5,7,8,10,11]` give an invertible 10x10 restriction; its frozen inverse reconstructs all 40 ambient protected bits and was exhausted over all 1024 protected states.  Decoder row fan-ins are `[4,5,3,3,4,4,4,4,8,6]`, 45 total XOR inputs.  The first decoded bit is `pi`; the remaining nine are local-spoke coordinates.  The eight-state Borel quotient remains a spectral/orbit compression, not a full identity-preserving decoder.

## 4540 — primitive-six zeta data reconstructs the protected 9+1 filtration
For W33 the primitive-C6 degree-two Walsh matrix is `M6=48(J-I)+204 A_*`, so it recovers `A_*` exactly and therefore the complete chain
`M6 -> A_* -> H10=im(A_*) -> V9=A_*(even) -> H10/V9=F2 parity`.
Cross-fusion with Passes 4524/4526 also explains the prism exception: a 3-rung fan equals its `(t-2)`-rung complement modulo the line-graph kernel for odd t.  Only t=3 makes that complement one rung, giving W33's nine-sheet edge collapse; Q(5,3), t=9, has seven complementary rungs and 544320 injective prism images.

## 4541 — outside box: parity is pairing with the unique fixed vector
The all-ones protected vector satisfies `1=A_*(e0+e1+e2+e3)`, and the protected alternating form gives
`pi(A_*b)=B(A_*b,1)=b^T 1`.  Pass 4496 proves the fixed space is 1D and its perpendicular is 9D, so the established uniserial chain is exactly
`0 < <1> < 1^perp=V9 < H10`.  The missing bit is the symplectic coordinate dual to the unique PSp-fixed protected vector.

## 4542 — outside box: the odd minimum shell reconstructs W33
The forty odd minimum vectors `s_i=A_*e_i` all have weight 12.  Across their 780 pairs, `wt(s_i+s_j)=20` for exactly 240 pairs and 16 for exactly 540.  Joining the weight-20 pairs reconstructs exactly `SRG(40,12,2,4)`, the dual-W33 line graph.  The 240 distinct adjacent differences are exactly the protected edge shell.  Thus parity-refined H10 weight geometry is self-describing.

## 4543 — outside box: exactly 108 local full H10 bases
The 13-line Borel cell is `K1 join 4K3`.  Choose nine of the twelve neighbors, equivalently omit a triple.  Omitted triangle / edge-plus-isolated / independent triples occur `4/108/108` times and leave ranks `7/8/9` respectively.  Therefore precisely the 108 independent omitted triples give local V9 bases; adjoining the center line-star produces exactly 108 full ten-line H10 bases.  Any ten-line subset avoiding the center has rank at most nine, so the parity center is essential.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4536_*.py` through `analysis/w33_pass4543_*.py`.
- Frozen certificates: `data/PART_W33_PASS4536_*.json` through `data/PART_W33_PASS4543_*.json`.
- Manuscript insert: `analysis/PASS4536_4543_parity_rank_decoder_reconstruction_insert.tex`, chained after Passes 4528--4535.  A duplicate historical inclusion of 4528--4535 through Pass 4519 was removed while preserving the direct sequential frontier chain.
- Public card/page: `analysis/PASS4536_4543_parity_decoder_index_insert.html` and `docs/protected-parity-decoder.html`, registered with the safe public extension materializer.
- Regression test and focused Actions workflow installed; the workflow re-executes all eight witnesses and compares regenerated JSON semantically against the frozen certificates.

Evidence discipline remains explicit: the q=7 anchor is exact but the all-q rank formula is still conjectural; the global order bound uses standard subgroup-classification input; coefficient parity is not a physical charge; local graph/matroid completeness is not spacetime locality or a hardware threshold; and zeta/Walsh reconstruction is not dynamics without an additional physical theorem.
