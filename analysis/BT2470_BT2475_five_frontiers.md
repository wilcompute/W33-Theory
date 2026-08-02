# Passes 2470–2475: five exact frontier results

## Release status

`PASS_FIVE_EXACT_FRONTIER_RESULTS_WITH_GLOBAL_U6_BITMAP_COMPLETION_BOUNDARY`

Aggregate semantic SHA-256:

`edb352760cf624957c1f2903c8d8e8edef056ffe8b7c073ccd9d30c1d27919fa`

## Pass 2470 — exact multishard U6 union engine

The union reducer was executed on 2, 4, and 8 overlapping fixed-triple shards, using the frozen 240 syndrome columns from Pass 1848. The largest run processed

- 17,525,360 shard records;
- 16,762,010 distinct fixed-chart representatives after overlap removal;
- 13,757,867 syndrome groups;
- 2,402,982 collision groups;
- 5,407,125 collision-marked representatives;
- 11,354,885 singleton representatives within this executed union.

The overlap histogram agrees exactly with

\[
N_d=\binom nd\binom{238-n}{4-d},
\]

and the total union agrees with

\[
\binom{238}{4}-\binom{238-n}{4}.
\]

This proves the idempotent shard-union semantics and exercises them on 17.5 million records. It does **not** execute the full 4,096-shard chart union, so the global \(U_6\) singleton coefficient remains open.

An exploratory local run accidentally supplied frame/octet labels instead of syndrome columns. Its 64-group collapse exposed the input mismatch, and it was rejected before publication. The frozen release requires `data/w33_pass1848_syndrome_columns.txt`.

## Pass 2471 — radius-four asymmetric signature obstruction

The selected nine-signature tuple has no two-signature trade preserving the total signature sum. Exhaustive search finds exactly three three-signature trades and eleven four-signature trades. All fourteen alternatives were lifted to their complete exact-cover fibers.

Across 43 reconstructed signature fibers, 903 pair relations and 13,333,289,472 cover-pair candidates were checked. Every one of the fourteen alternative tuples contains an empty frame-disjoint pair relation. Hence no exact nine-cover resolution exists anywhere in the complete signature-trade ball of radius four around the selected tuple.

This is a strictly asymmetric result and is consistent with the independent theorem that no nine-colouring can be full-group-equivariant. It does not rule out tuples at trade distance at least five.

## Pass 2472 — rank-nine scheme decoded

The unique finest binary-generated commutative fusion of the rank-22 `PGSp(4,3)` shell algebra is an exact symmetric association scheme of rank nine. Its valencies are

\[
1,256,24,128,48,48,8,3,24,
\]

and its primitive multiplicities are

\[
1,15,15,20,162,135,108,24,60.
\]

The first eigenmatrix is integral; the second eigenmatrix and all Krein parameters are rational. All Krein parameters are nonnegative. Exhaustive support tests find no P-polynomial or Q-polynomial ordering.

The imprimitivity geometry is explicit:

- relation 6 is `45 K_{4,4,4}`;
- relation 7 is `135 K_4`, giving the three four-point parts inside every `K_{4,4,4}`;
- their union is `45 K_12`.

## Pass 2473 — natural tomotope quotient refuted

On the canonical selected 192 curved events, the natural elementary relation “same distinguished center, replace one leaf” has

- 336 edges;
- degree split \(2^{96}5^{96}\);
- eight connected components of 24 vertices;
- 42 edges per component;
- twelve tie-2 and twelve tie-3 events per component.

Every nonempty union of the four archived rank involutions is regular. All 15 rank-colour unions were enumerated, and none has the degree/component profile above. Therefore the natural center-preserving elementary-event quotient is not the archived tomotope-like rank adjacency system.

This does not forbid an arbitrary quotient that forgets the event center or elementary-change relation.

## Pass 2474 — the normalizer reinstates the Hom obstruction

The normalizer of a Sylow-five subgroup in `Sp(4,3)=2.U4(2)` has order 40 and is the nonsplit group

\[
5{:}8,
\]

not \(C_2\times(5{:}4)\). Its element-order census is

\[
1^1 2^1 4^{10}5^4 8^{20}10^4.
\]

Every lift of a projective order-four normalizer generator has order eight and fourth power equal to the center. On the 144-dimensional \(C_5\)-equivariant Hom space, the center acts as \(-I\), so

\[
T^4=-I.
\]

Consequently the Hom space is 36 copies of the relevant faithful four-dimensional `5:8` module. It has no normalizer-invariant vector:

\[
\operatorname{Hom}_{5{:}8}(E_8,90)=0.
\]

The four 36-dimensional primitive-eighth-root eigenspaces arise only after complex diagonalization. Forgetting the central sign produces a projective 36-dimensional block, not an honest map between the original carriers.

## Parallel-track reconciliation

The later Pass 2505 concern that the 327-orbit cover frontier might be incomplete is superseded by Passes 1821–1825.  Pass 1821 compiled an Algorithm-X enumeration through frame zero that visited every branch, produced exactly 394,200 fixed-frame covers, and used frame transitivity plus orbit reduction to prove the complete global count 3,547,800 in 327 orbits.  Therefore the 43 fibers reconstructed in Pass 2471 are complete, not frontier-relative.  The Pass 2496/2503 K8-link criterion remains a useful alternative global test, but no successful K8 computation was reported.

Pass 2502 independently identifies the chiral C5 restriction as the pentagon augmentation ideal and the achiral restriction as the regular representation.  This is consistent with Pass 2474: the 144-dimensional C5-Hom exists because only nontrivial C5 characters contribute, while the lifted 5:8 normalizer restores the central-sign obstruction.

## Boundaries

The exact open problems after this packet are:

1. execute the complete 4,096-shard bitmap union, including lower-shadow overlap;
2. search signature multisets at distance at least five, or bypass signatures entirely;
3. determine whether the rank-nine scheme has a useful physical interpretation beyond its exact finite geometry;
4. classify more destructive tomotope coarsenings only if a principled forgotten datum is named;
5. locate a canonical nonlinear or symmetry-breaking coupling, because the full normalizer supplies no linear invariant.
