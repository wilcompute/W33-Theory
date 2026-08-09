# Passes 4552--4559 executed outcomes

This lane executes the five frontier attacks after Passes 4536--4543, cross-fused with Passes 4544--4551, plus three independent outside-the-box probes.

## 4552 — third exact Q^-(5,q) rank anchor; all-q theorem still open
An independent elliptic-quadric construction of `Q^-(5,5)=GQ(5,25)` gives 756 points and 3276 lines with `rank_2 N=651` and `rank_2(N^T N)=546`. Together with q=3 and q=7, the exact anchors are `(91,70)`, `(651,546)`, `(2451,2150)` and all fit `rank N=q^4+q^2+1`, `rank(N^T N)=(q^2+1)(q^2-q+1)`. The infinite formula remains OPEN. A literature audit corrected a false lead: Bagchi--Brouwer--Wilbrink's 1991 `O(5,q)` paper concerns the dual of the square `Sp(4,q)` generalized quadrangle, not elliptic `Q^-(5,q)=GQ(q,q^2)`, so it is not used as proof.

## 4553 — canonical protected filtration and weight quadratic
The protected chain is intrinsically `0 < <j> < j^perp=V9 < H10`, where `j` is the unique fixed all-ones vector and `pi(x)=B(x,j)`. On `V8=V9/<j>`, `q8([x])=wt(x)/4 mod2` is well defined under complement and polarizes exactly to the protected alternating form. Exhaustion gives 136 singular classes including zero and 120 anisotropic classes, hence plus type `O+(8,2)`. Locating the 1D and 9D layers no longer requires cyclic-submodule search; middle irreducibility is inherited from the independent Pass4477/4496 certificate.

## 4554 — 108-basis exchange/fault-switching ensemble
The 108 local H10 bases form a connected 15-regular graph under one-spoke exchange, with 810 edges, diameter 3, distance distribution `[1,15,48,44]`, and spectrum `15^1,9^8,3^27,0^16,(-3)^56`. The order-162 Borel has two orbits `81+27` with equitable quotient `[[12,3],[9,6]]`. Any specified spoke is avoided by 27 bases; two erased spokes in distinct pencils by 6; two in one pencil by 0; and an erased independent three-pencil triple by exactly one basis.

## 4555 — one C8 selector layer suffices
Pass4551's Boolean degree-four selector `c8(S)=712` already recovers the 1620 apartment columns. From it alone: `H -> HH^T=A_* -> dual W33 -> H10 -> j -> pi -> V9`. No C6 or C7 layer is required once that selector is present. This is one-layer sufficiency, not an absolute information-theoretic minimality theorem.

## 4556 — exact exceptional-six linear no-go
`H10` has composition factors `1,8,1`; the faithful `O^-(6,2)` module `U6` from Passes4522/4544 is simple of dimension six. Therefore `Hom_G(H10,U6)=Hom_G(U6,H10)=0` for `G=PSp(4,3)`. Any real protected-to-Schlaefli bridge must therefore be nonlinear, pass through a larger module, or break equivariance. The existing 27x36 cubic-surface incidence intertwiner acts on different permutation carriers and does not evade this obstruction.

## 4557 — outside box: shell distances recover point pencils
For each even edge vector and the forty odd line-stars, cross-shell Hamming distances occur `12:2, 20:36, 28:2`. The distance-12 stars are exactly the edge endpoints; the distance-28 stars are exactly their two common neighbors. All four form the unique K4 line pencil through the corresponding W33 point. Thus protected Hamming geometry reconstructs vertex-edge incidence and geometric pencils.

## 4558 — outside box: apartments uniformly lift the singular O+(8,2) shell
The 1620 apartments project under `b -> A_*b` to exactly 135 distinct weight-16 protected vectors, each with exactly 12 apartment preimages. They are precisely the 135 nonzero singular classes of `V8`. Within every 12-apartment fiber, adjacency by one-line intersection is exactly `K_{4,4,4}`: degree 8, 48 intersecting pairs, 18 disjoint pairs.

## 4559 — outside box: protected edges are the anisotropic double cover
The 240 weight-20 edge images pair under `x -> x+j` into 120 anisotropic `V8` classes. Geometrically the partner edge is exactly the opposite edge in the unique four-line K4 pencil through the same W33 point. Hence the 240 carrier is a canonical two-sheeted lift of the 120 anisotropic classes; the polar quotient is `SRG(120,63,30,36)`.

## Integration and evidence
- Executable witnesses: `analysis/w33_pass4552_*.py` through `analysis/w33_pass4559_*.py`.
- Frozen certificates: `data/PART_W33_PASS4552_*.json` through `data/PART_W33_PASS4559_*.json`.
- Manuscript insert: `analysis/PASS4552_4559_rank_filtration_basis_shell_insert.tex`, chained after the completed Pass4544--4551 module/zeta packet through the shared frontier.
- Public surfaces: `analysis/PASS4552_4559_rank_filtration_basis_shell_index_insert.html` and `docs/protected-o8plus-shells.html`, registered with the public extension manifest.
- Regression test and focused Actions workflow installed.

Evidence discipline remains explicit: the elliptic `Q^-(5,q)` closed rank formula is not promoted beyond exact q=3,5,7 anchors; the exceptional-six no-go is linear/equivariant only; Hamming distances, 12-fold apartment fibers and the 240->120 cover are finite geometry and not physical distance, degeneracy or particle labels.
