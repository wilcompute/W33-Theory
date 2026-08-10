# Passes 4579--4586 executed outcomes

This lane executes the five strongest protected-geometry next moves after Passes 4552--4559 plus three independent outside-the-box constructions, while preserving the concurrently active Passes 4571--4578 lane.

## 4579 — W33 lifts reconstruct the full 255-state O+(8,2) geometry
The 135 apartment-derived singular classes and 120 opposite-edge anisotropic classes are disjoint and exhaust every nonzero class of `V8=V9/<j>`. The lift-native quadratic `q([x])=wt(x)/4 mod2` reconstructs the polar form. Exact degrees are singular->singular 70, singular->anisotropic 56, anisotropic->singular 63, anisotropic->anisotropic 63. The 10,795 projective binary lines split as 1,575 all-singular, 3,780 one-singular/two-anisotropic, and 5,440 all-anisotropic triples.

## 4580 — the elliptic rank law is reduced to one exact code theorem
For the binary point-line code `C=im(N)` of `Q^-(5,q)=GQ(q,q^2)`, the candidate formulas are equivalent to `dim C=q^4+q^2+1`, `C^perp=ker(N^T)<=C`, and `dim C^perp=q(q^2-q+1)`. These imply `rank(N^T N)=dim(C/C^perp)=(q^2+1)(q^2-q+1)`. Exact q=3,5,7 anchors satisfy the full dual-containing identity. A targeted literature audit found related defining-characteristic polar-space rank theorems but no direct cross-characteristic binary point-line theorem for this elliptic family; the infinite formula remains OPEN.

## 4581 — every K4,4,4 apartment fiber is an equivariant 3x4 resolution
The three independent four-sets of a 12-apartment fiber are three distinct partitions of the same 16-line support into four disjoint apartments. The singular stabilizer has order 192 and line orbits 16,8,8,8, with the common support the unique 16-orbit. Its fiber action has image order 96 and kernel 2; the three parts are permuted as S3 with C2^4 kernel. A one-part setwise stabilizer restricts as D8 on its four apartments.

## 4582 — exact optimal erasure-robust H10 readout
Among the 280 natural protected carriers (40 line-stars + 240 edge vectors), 11 channels are necessary and sufficient to survive any one arbitrary channel loss, and 14 are necessary and sufficient to survive any two. The one-loss lower bound is dimensional. For two losses, a binary `[n,10,d>=3]` readout code is required; the Hamming bound excludes n=12,13 and an explicit 14-channel witness survives every pair deletion. The parity anchor is therefore distributed rather than tied to one center star.

## 4583 — first exact nonlinear protected-to-exceptional-six bridge
For protected `V8`, the alternating square has dimension 28. Contraction with the protected alternating form gives `K27=ker(B:Lambda^2 V8->F2)`. It contains a 15D invariant core and exact exhaustion gives `K27/K15 = U6 direct-sum U6`, with exactly three invariant simple six-submodules. Each U6 has faithful PSp image order 25920 and nonzero orbits 27+36. Thus an unordered distinct orthogonal pair `(v,w)` maps equivariantly by `v wedge w` to the exceptional O^-(6,2) six-space after choosing one invariant factor. Across all 16,065 orthogonal pairs, zero has 945 preimages and every nonzero U6 vector has exactly 240. This is bilinear/pair-valued and is consistent with Pass4556 and Pass4576: those no-go theorems concern unary linear or unary Boolean degree<=2 maps, whereas Pass4583 changes the domain to protected pairs.

## 4584 — outside box: a new cross-shell [120,9,56] code
The 135x120 singular-anisotropic orthogonality matrix has row weight 56, column weight 63 and binary rank 9. Mod 2, `R R^T=0` and `R^T R=J_120`. Its row code is self-orthogonal `[120,9,56]` with complete enumerator `1 + 255 z^56 + 255 z^64 + z^120`; it contains the all-ones word and has an 8D fixed-word quotient.

## 4585 — outside box: the singular shell has a canonical 135 -> 45 quotient
The 12-apartment fiber over each singular class uses a 16-line support, but only 45 distinct supports occur. Each support carries exactly three singular classes; they are pairwise orthogonal and sum to zero, hence form a totally singular projective line. The 45 supports form one PSp orbit with stabilizer 576. Its action on the three singular points is C3 with kernel 192, exactly the singular-point stabilizer order from Pass4581.

## 4586 — outside box: a rank-15 45x40 transport crosses W33 point/line non-self-duality
Each original W33 point supplies an all-anisotropic projective line from the three opposite-edge classes in its four-line K4 pencil. Incidence between the 45 singular support-lines and these 40 anisotropic lines is defined by complete 3x3 polar orthogonality. The resulting matrix `T` has row weight 8, column weight 9 and binary rank 15. Its integer Gram identities are `T T^T=8I_45+2A_45` with `A_45=SRG(45,32,22,24)` and `T^T T=8I_40+2A_point+J_40`, where `A_point` is exactly the POINT-side W33 graph. The executable explicitly checks `A_point != A_*`, the protected LINE-side graph. Existing 45-object repo carriers with the same SRG parameters are not identified with this new 45-set absent an explicit action intertwiner.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4579_*.py` and `analysis/w33_pass4580_*.py` through `analysis/w33_pass4586_*.py`.
- Frozen certificates: `data/PART_W33_PASS4579_*.json` through `data/PART_W33_PASS4586_*.json`.
- Manuscript source: `analysis/PASS4579_4586_o8plus_rank_decoder_exceptional_insert.tex`.
- Public sources: `analysis/PASS4579_4586_o8plus_exceptional_bridge_index_insert.html` and `docs/protected-o8plus-exceptional-bridge.html`, registered in the public extension manifest.
- Regression test and focused Actions workflow installed.
- Manuscript attachment is now concurrency-safe in all three maintained wrappers: `W33_CURRENT_FRONTIER_MANIFEST` -> `PASS4579_4586_o8plus_rank_decoder_exceptional_insert` -> `PASS4587_4588_d4_triality_insert`. This leaves the concurrent Passes4571--4578 lane free to attach inside the shared frontier while preserving the numerical order of this packet relative to Pass4587+.

Evidence discipline remains explicit: the elliptic all-q binary-rank theorem is not promoted beyond q=3,5,7; the exceptional bridge is bilinear on pairs and requires a U6-factor choice; the 45-object parameter match is not an E6 identification; finite erasure/Hamming/fiber structures are not physical thresholds, degeneracies, or spacetime locality.
