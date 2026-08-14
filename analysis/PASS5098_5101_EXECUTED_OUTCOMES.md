# Passes 5098–5101 — root-coset supplement to the derivative packet

**Status:** EXECUTED 2026-08-14. These passes contain only results not already owned by the concurrently landed Pass5090–5097 packet.

## 5098 — exact active-chart / positive-root-coset hypergraph isomorphism
The existing derivative packet identified four q^3 root sheets around a chamber. This pass upgrades that count to an explicit incidence theorem.

For q=2 and q=3, reconstruct the W(3,q) apartments through a fixed chamber and the active opposite-pair charts of its chamber-star word. Separately construct the standard maximal unipotent subgroup U<Sp(4,q) from the four positive-root subgroups. The two finite hypergraphs are explicitly isomorphic:

- vertices: q^4 chamber-star apartments <-> q^4 elements of U;
- hyperedges: 4q^3 active charts <-> right cosets of the four positive-root subgroups;
- each hyperedge has q vertices.

The isomorphism matches the hyperedges themselves, not only the associated point graphs. Exact anchors are 16 points/32 two-point charts at q=2 and 81 points/108 three-point charts at q=3.

## 5099 — q=3 derivative-graph automorphism group is U81 semidirect V4
For q=3, exhaustive graph automorphism enumeration gives order 324. The left-regular U action contributes a normal subgroup of order 81. The stabilizer of the identity has four elements with order census `1^1 2^3`, hence is V4, and it normalizes the left-regular subgroup.

Therefore

`Aut(G_der) ~= U_81 semidirect V4`.

The four positive-root coset parallel classes are intrinsic and the V4 stabilizer fixes each one setwise. The order agrees exactly with the full projective W33 chamber stabilizer:

`324 = |PGSp(4,3)|/160 = 51840/160`.

Thus the derivative graph has no accidental symmetry enlargement beyond the full projective chamber stabilizer.

## 5100 — general split-Lie positive-root derivative law
Let a split finite Chevalley group have N positive roots. Its maximal unipotent subgroup has q^N elements, the defining-characteristic Steinberg degree. Each positive-root subgroup has order q, so it has q^(N-1) cosets in U. Summing over the N positive roots gives

`N q^(N-1) = d(q^N)/dq`.

For C2, N=4, yielding 4q^3. This makes the user's derivative observation part of a general root-coset counting law rather than an isolated W33 arithmetic coincidence.

**Boundary:** the root-coset law is general; identifying those cosets with active apartment-code tester charts is a separate rank-two theorem, explicitly certified in Pass5098 at q=2,3 and geometrically by the W(3,q) root-sheet construction.

## 5101 — exact C2 odd-characteristic commutator curvature
Use the standard positive-root nilpotents

`X0=E01-E32`, `X1=E13`, `X2=E03+E12`, `X3=E02`.

Their only nonzero Lie brackets are

`[X0,X1]=X2`,

`[X0,X2]=2 X3`.

All other unordered pairs commute. Hence in odd characteristic the six pairs of root directions generate subgroup orders

`q^2,q^2,q^2,q^2,q^3,q^4`:

- four commuting pairs remain q^2;
- <X0,X2> creates X3 and has q^3 elements;
- <X0,X1> creates X2 and then X3, generating the full q^4 unipotent cell.

In characteristic two the coefficient 2 vanishes and the second commutator layer collapses, explaining the previously observed q=2 exceptional profile.

## Synthesis
The formal derivative `4q^3=(q^4)'` is not merely a matching count: at q=2,3 the entire first-order incidence geometry is the positive-root-coset geometry of the C2 maximal unipotent group. At q=3 its full automorphism group is exactly `U_81 semidirect V4`, the full projective chamber stabilizer. Higher directional composition departs from ordinary Cartesian calculus precisely through the C2 Chevalley commutators.

The global apartment-code distance problem is still separate: this packet explains the chamber equality geometry and its symmetry, but does not prove that every nontrivial cohomology class must activate at least 4q^3 charts.
