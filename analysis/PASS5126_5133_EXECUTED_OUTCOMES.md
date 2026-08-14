# Passes 5126–5133 — q=5 leader 18, decoder radius 5, all-q controller, odd-q bicycle theorem, and three outside-box closures

**Status:** EXECUTED 2026-08-14; frozen certificates committed, remote replay workflow added separately. Evidence firewall remains active: q=5/all-q apartment-code distance is still open.

## 5126 — q=5 strict counterexamples now require chamber leader at least 18
For a 17-edge cut-minimal leader, exact bipartite max-degree-three girth-eight feasibility rejects all 51 ordered degree-sequence pairs whose adjacent-edge-pair count exceeds 25. The cap 25 is sharp. Exact q=5 Delsarte optimization at that cap gives pair-distance distribution `(25,66,45,0)`, maximum pair overlap 5000, and Bonferroni apartment-weight lower bound 625. With Pass5118, every word of weight below 625 therefore has minimum chamber leader at least 18. Equality at 625 is not classified.

## 5127 — q=5 minimum-shell heavy charts are quantized
At weight 625 the point-chart and line-chart coarea sums are each 1250. A nonzero K6 cut has size 5, 8, or 9. Writing `A_type` for active charts of one type and `h8,h9` for the two heavy sizes gives

`5 A_type + 3 h8 + 4 h9 = 1250`.

Thus `3h8+4h9` is divisible by five. The smallest nonzero defect is uniquely `(h8,h9)=(2,1)`, so an exotic minimum word must contain at least three heavy charts in one type and has total active-chart count at most 498, versus 500 for a chamber star.

## 5128 — q=3 equivariant decoder has global radius four
The apartment chart-sharing graph is 20-regular. Fixing one apartment gives exactly 1, 20, 490, and 13269 connected error sets of sizes 1 through 4. Exhaustive connected-component decoding introduces no false apartment and clears every connected four-set within two sweeps. Since distinct chart-sharing components occur in no common chart, every arbitrary weight-four pattern clears within at most three sweeps.

## 5129 — the intrinsic controller is an all-q C2 unipotent theorem
For W(3,q), choosing a reconstructed chamber gives a q^4-apartment carrier on which the type-C2 maximal unipotent group U(q) acts regularly. The 4q^3 active opposite-pair charts are exactly right cosets of the four positive-root subgroups. Objectwise executable anchors at q=2,3,4,5, including GF(4), match the full hypergraph exactly. Combined with Pass5112, this controller is determined by the apartment code up to code automorphism and the point-line orientation swap.

## 5130 — the odd-q binary Levi bicycle formula is now a theorem
The known binary incidence-rank theorem for the odd-q symplectic generalized quadrangle gives

`rank_F2 N = 1 + q(q+1)^2/2`,

hence `null_F2 N=q(q^2+1)/2`. For odd q the Levi degree q+1 is even, so the Levi bicycle calculation from Pass5124 gives

`dim Bike_2(Levi)=2 null_F2(N)-1=q^3+q-1`.

The repo independently rebuilds q=3,5,7,11 anchors: 29, 129, 349, 1341. The theorem is for odd prime powers; even q is separate.

## 5131 — BONKERS 1: q=3 decoder radius rises again, to five
There are exactly 381480 connected weight-five error components through a fixed apartment. Exhaustive decoding again introduces no false coordinates. Connected sets of sizes 1–5 require at most 1,1,2,2,3 sweeps respectively. Component separation therefore certifies every arbitrary q=3 weight-five error pattern within three sweeps. Weight six is not certified.

## 5132 — BONKERS 2: minimum theta support is the root-direction Cayley graph
Under the U(q)-torsor identification of a chamber-star support, the induced theta graph is exactly

`Cay(U(q), union_i (H_i \ {1}))`,

where H_i are the four positive-root subgroups. It is 4(q−1)-regular with `2 q^4(q−1)` edges, and its 4q^3 active q-cliques are precisely the root-subgroup cosets. Full edge-set equality is verified at q=2,3,4,5. This explains the Pass5119 half-regular saturation geometrically.

## 5133 — BONKERS 3: state/program transport is a reversible all-field polynomial compiler
For every finite-field anchor q=2,3,4,5, including GF(4),

`(b; a,c,d) -> (a; b, c+ab, d+2ac+a^2b)`

is a bijection on the regular U(q) carrier with inverse

`c=C-ab, d=D-2aC+a^2b`.

The corresponding root-subgroup matrix factorizations are exact. Characteristic two is handled automatically by `2ac=0`.

## Evidence boundary
The q=5 minimum-distance theorem remains open for leaders at least 18, even though the weight-625 exotic shell is now strongly constrained. Radius six is not proved. The odd-q bicycle theorem uses the established cross-characteristic incidence-rank theorem; it is not an empirical extrapolation. Controller, Cayley, and compiler statements are finite code/building/group algebra, not hardware-performance claims.
