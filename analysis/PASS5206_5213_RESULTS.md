# Pass5206–5213 executed outcomes

**Status:** executed on 2026-08-14. This packet carries the five requested live frontier attacks plus three outside-the-box probes. It is collision-free with the separately reserved Pass5214–5221 continuation.

## Pass5206 — leader 36 full-cut attack

The first non-singleton consequences of the full cut-coset theorem were aggregated exactly by selected-degree class. At q=5 they imply

`x^T N y <= 16 n1 + 34 n2 + 45 n3`

on either bipartition side. Over the eleven open Pass5205 layers N1=54..64 this yields N2 upper bounds 381..405, while the dangerous Delsarte distributions use only N2=164..175. Thus this entire degree-class aggregation is redundant. Leader 36 is not closed; the next cut attack must preserve correlated larger-shore host incidences rather than collapse them to degree counts.

## Pass5207 — remaining P-heavy equality reduced to footprint wt <=24

Every q=5 weight-625 word has nonzero P-component parity footprint because the P components partition apartment coordinates and 625 is odd. Every nonzero P-component restriction costs at least 25 apartments, and a P-heavy word has at least one component whose weight is strictly greater than 25. Therefore, if t is footprint weight,

`625 >= 26 + 25(t-1)`, hence `t<=24`.

So any exotic P-heavy equality word produces a nonzero footprint-code word of weight at most 24. Point footprints already have weight 25. Therefore proving footprint distance 25 would, together with Pass5191, classify the complete q=5 weight-625 shell as chamber stars.

## Pass5208 — odd-q dual-grid spanning reduced to one rank theorem

For odd prime powers Pass5130 gives

`dim C(W)^perp = q(q^2+1)/2`.

Since every dual grid lies in the incidence dual, the conjecture that dual grids span the full dual is equivalent to

`rank_2(F)=q(q^2+1)/2`.

Exact anchors q=3,5,7,11 give 15,65,175,671. q=5 is a theorem by Pass5188. No all-odd proof is promoted. Even characteristic is a genuine firewall: known even-q results show minimum dual-grid words need not span the whole dual for q>=4.

## Pass5209 — q=5 footprint hull and mod-4 law

The footprint code C_F has dimension 65 and Gram relation `FF^T=J` over F2. Its hull `C_F cap C_F^perp` has dimension 64. Every hull word has weight 0 mod4 and every word in the other coset has weight 1 mod4. The 156 point rows have weight 25; sums of two point rows have weight 40 when the points are collinear and 48 otherwise.

Thus a hypothetical nonzero word below 25 is restricted to:

- hull: 4,8,12,16,20,24;
- odd coset: 1,5,9,13,17,21.

The target `[325,65,25]_2` remains open, but the search space is structurally much narrower.

## Pass5210 — root-controller / dual-grid Borel intertwiner

The four U(q) controller coordinates are the four positive C2 roots, with split-torus characters `r,s,rs,r^2s`; this is exactly the Pass5192 action `(a,b,c,d)->(ra,sb,rsc,r^2sd)`. W-points and hyperbolic polar-pair dual grids are canonical PSp4(q)-sets, hence their incidence matrix satisfies

`P_pts(g) F = F P_grid(g)`.

So the controller Borel group acts by automorphisms of the footprint code and the P-component block graph. Parallel Pass5217 subsequently strengthens this at q=5 to an explicit objectwise atom projection `(a,b,c,d)->(a,c)`.

## Pass5211 — outside-box: the P-block graph is NO_5^+(q)

For odd q, the quotient `Lambda^2(F_q^4)/<omega>` is the 5D orthogonal module for the exceptional identification `PSp4(q) ~= POmega5(q)`. A polar hyperbolic-line pair `{H,H^perp}` maps to one plus-type nonisotropic projective point. Under this bijection the Pass5203 block graph is the classical rank-3 graph `NO_5^+(q)`.

At q=5 this is exactly `SRG(325,144,68,60)` with eigenvalues 144,14,-6.

## Pass5212 — outside-box: a 13-dual-grid Hoffman resolution

An explicit deterministic set of 13 q=5 dual grids partitions all 156 W-points. The selected grids are pairwise disjoint, hence form a coclique in `NO_5^+(5)`. Hoffman's bound gives alpha<=13, so it is maximum. Every distinguished W-point footprint 25-clique meets this 13-coclique exactly once.

This is simultaneously a maximum SRG coclique and a dual-grid resolution of the W-point set.

## Pass5213 — outside-box: exact dual footprint code

For `C_F=im(F^T)`, the dual is `ker(F)`. Pass5202 gives dimension 260. For a t-block dual word, even point degrees imply an induced block-graph edge count `E>=3t`, hence t>=7. Weight 7 would force a K7 of selected blocks with every covered W-point appearing exactly twice. Fixing one block by transitivity reduces this to a deterministic local search over its 144 neighbours; the complete backtrack takes 265 recursion nodes and finds no solution.

An explicit weight-8 support exists. Its eight dual grids cover 48 W-points exactly twice and induce `K8` minus a perfect matching. Therefore

`C_F^perp = [325,260,8]_2`.

## Current boundaries

- q=5 strict counterexamples still require chamber leader >=36; leader 36 is open.
- footprint primal distance 25 remains open; if proved, Pass5207 + Pass5191 close the complete weight-625 equality shell.
- all-odd dual-grid spanning remains a rank conjecture, although q=3,5,7,11 agree.
- all promoted statements are finite geometry/code/group statements, not physical performance claims.
