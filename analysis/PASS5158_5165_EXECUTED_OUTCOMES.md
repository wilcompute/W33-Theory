# Passes 5158–5165 — executed outcomes

**Status:** science producers and manuscript integration are committed on 2026-08-14. The broad GitHub Actions replay is tracked separately and must not be described as green unless its current job is rechecked. The q=5 path/DP arithmetic, the q=5 W=40 girth rejections, the q=2,3,4,5 four-chamber census, and the q=3 decoder radius-five/centered-six probe were also independently replayed during development.

## 5158 — q=5 leader 21 closes from selected four-edge paths

Pass5148 left exactly `m=21,N1=33`, with pair bound `-439`, `N112>=48`, and a deficit of 42 triple-intersection incidences. The selected-Levi degree equations force at least six selected four-edge paths. Each such path injects two distinct `(1,2,3)` chamber triples, and Pass5140 gives five common apartments for each at q=5. Hence `N123>=12`, total triple mass is at least `25*48+5*12=1260`, and the cubic lower bound is

`-439 + (6/7)*1260 = 641 > 625`.

Therefore every q=5 word below 625 has minimum chamber leader at least 22.

## 5159 — all-q four-chamber star intersection law

Four distinct chamber edges can appear in one apartment `C8` in exactly seven dihedral six-distance patterns. The consecutive four-edge pattern

`(1,1,1,2,2,3)`

has exactly `q` common apartments. The six signatures

`(1,1,2,2,3,4)`, `(1,1,2,3,3,4)`, `(1,1,3,3,4,4)`, `(1,2,2,3,3,3)`, `(1,2,2,3,3,4)`, `(2,2,2,2,4,4)`

each determine one apartment; every other six-distance signature gives zero. Complete rooted q=2,3,4,5 censuses show no signature splitting. At q=5 the rooted histogram is `1^19375,5^500`.

This is the exact fourth-order chamber-star coefficient needed for future degree-four parity attacks.

## 5160 — hub pruning preserves radius five and repairs the entire centered weight-six obstruction family

The modified decoder keeps the original local syndrome ROM and global max-vote set, but among tied max-vote candidates corrects only those of minimum induced degree in the apartment chart-sharing graph.

All connected representatives through a base apartment at weights one through five were replayed: `1,20,490,13269,381480`. There were zero false corrections and every case cleared within three sweeps.

The complete centered `2+2+2` weight-six false-center family contains 32 representatives through a fixed center; all 32 clear monotonically. On the original failure `{1,2,3,6,27,54}`, the max-vote tie remains `{0,1,2,3,6,27,54}`, but false center 0 has tie-degree 6 while every true error has degree 2, so the hub-pruned correction is exactly the six true errors.

This repairs the complete minimal centered obstruction family but is **not** yet a global radius-six theorem; non-centered connected weight-six types remain to be classified.

## 5161 — q=5 leader 22 closes by local degree-type path DP

Deleting an edge and using the leader-21 cap gives `N1<=35`. Exact Delsarte plus the `(1,1,2)` cubic term closes the lower sectors. A degree-class stub-balancing relaxation gives selected-four-edge-path lower bounds `P4>=56,68` in the sharp `N1=34,35` sectors. The full sector weight lower bounds are

`N1=31:1168`, `32:950`, `33:668`, `34:972`, `35:900`.

Hence strict sub-625 counterexamples require leader at least 23.

## 5162 — all-q second shell of the chamber dependency code

For every finite q>=2 the chamber dependency code `Cut(Levi(W(3,q)))` has second nonzero weight

`2q`.

The weight-`2q` words are exactly cuts of adjacent point-line Levi vertex pairs, one per chamber, giving `(q+1)^2(q^2+1)` words. Girth eight handles shores of size at most seven; the exact Levi Laplacian gap `q+1-sqrt(2q)` excludes all larger smaller shores.

This is the dependency/cut code, not the apartment-code distance theorem.

## 5163 — q=5 leader 23 closes

Deletion gives `N1<=38`. The local degree-type relaxation forces

`P4>=44,54,64,76,94`

for `N1=34,35,36,37,38`. Combining pair, `(1,1,2)`, and `(1,2,3)` contributions yields corresponding weight lower bounds

`1151,1040,854,781,760`.

The `N1=33` branch is already at 992, so every leader-23 word exceeds 625. Strict sub-625 counterexamples therefore require leader at least 24.

## 5164 — q=5 leader 24 closes after two exact girth rejections

Deletion and degree arithmetic reduce to `N1<=40`. Every sector through 39 is already above 625. At `N1=40`, the local relaxation has degree-count profiles

`(1,7,11)->P4>=100`, `(4,4,12)->P4>=96`, `(7,1,13)->P4>=96`.

Both `P4=96` equality profiles are impossible in a simple bipartite girth-eight selected Levi graph. For `(4,4,12)`, equality forces a degree-three `C12` plus four antipodal two-edge chords; the antipodal chord classes would need an independent set of size four in quotient `C6`, but `alpha(C6)=3`. For `(7,1,13)`, equality forces the degree-three induced split `(3,2,2,2,2,2,2)|(3,3,3,2,2,2)`, and exact backtracking rejects every C4/C6-free realization.

Thus actual `P4>=97`, giving the final `N1=40` weight bound `629`. The live q=5 strict-counterexample barrier is therefore

`leader >= 25`.

## 5165 — root-Cayley metric in characteristic three

For every finite field `F_q`, `q=3^f`, the normalized three-move curves are

`u=0`, `u=-1`, or `v in {0,1,-u,u,u-1,u^2}`.

Outside `u in {0,-1,1}` the six v-values are distinct; at `u=1` they collapse to three. The exact shell formula is

`1`, `4(q-1)`, `8(q-1)^2`, `10(q-2)(q-1)^2`, `(q-1)^2(q-3)(q-5)`.

At q=3 this gives the exact profile `1,8,32,40`. Together with Pass5143, symbolic root-Cayley shell formulas now cover every odd characteristic. Characteristic two remains the uniform open family.

## Requested-front audit and evidence boundary

The q=5 exotic weight-625 shell was attacked but not eliminated. For a local K6 cut of weights 5,8,9 the selected line graph has respectively 5,2,0 four-cliques, so

`Q4_type = 1250 - 6 h8 - 9 h9`.

The minimal exotic profile `(h8,h9)=(2,1)` therefore has `Q4_type=1229`, a fourth-local-moment defect of 21 in addition to its triangle defect of 28. No global invariant forcing the star fourth moment has been proved, so the profile remains open.

The full all-q nonlinear theta gap was not duplicated because Pass5150–5157 was already collision-reserved for centered/theta spectral work. At this packet’s release point no nonlinear-gap theorem from that reserved packet had landed; the exact open target remains `sum_i ||P_i f||^2 <= 3||f||^2` on the mean-zero nonlinear sector.

The q=5/all-q apartment-code distance theorem remains open for leaders at least 25. The decoder’s global radius six remains open. Controller/metric statements are finite algebraic geometry, not hardware-performance claims.
