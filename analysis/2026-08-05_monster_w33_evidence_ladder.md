# Passes 3584–3590 — Monster/W33 evidence ladder

## Result

The repo’s Monster material contains a genuine structural opening, but it must be separated from a large arithmetic shadow.

The exact W33 group is

\[
PSp(4,3)\cong U_4(2),\qquad |PSp(4,3)|=25920,
\]

and its full graph/Weyl extension has order

\[
|W(E_6)|=51840=2\cdot25920.
\]

The Monster order is divisible by both numbers. More importantly, the finite-group literature documents Monster subgroups isomorphic to \(U_4(2)\). That upgrades the statement “25920 divides \(|\mathbb M|\)” from a bare divisibility coincidence to a real subgroup direction. It does **not** yet identify the repo’s concrete 40-point W33 action with a specific subgroup inside a computational Monster model.

## Exact arithmetic shadow

The verifier freezes the following identities:

\[
196883=47\cdot59\cdot71,
\]

\[
196884=1+196883=196560+18^2,
\]

\[
744=3\cdot248,
\qquad
1728=12^3,
\qquad
24=12\cdot2,
\qquad
248=240+2\cdot4.
\]

These are exact and useful as search constraints. They are not, by themselves, derivations of moonshine, the Griess product, the Leech lattice, or a physical mechanism.

## The actual breakthrough target

The next structural object is a **class-fusion-aware embedding certificate**:

\[
\iota:PSp(4,3)\hookrightarrow\mathbb M.
\]

A useful certificate must provide:

1. concrete Monster generators for the image of the W33 generators;
2. preservation of the W33 relations and order \(25920\);
3. the fusion of W33 conjugacy classes into Monster classes;
4. restriction data for at least one Monster module;
5. an explicit test of whether the W33 Steinberg \(81\)-module occurs in a restricted Monster representation.

This is the point where the project can move from numerical moonshine to representation-theoretic moonshine.

## New conjectural bridge: the 81-sector restriction problem

The repo has independently isolated an \(81\)-dimensional protected module as W33 Levi homology/Steinberg space. The Monster has rich 3-local geometry and documented elementary abelian 3-subgroups. This suggests the concrete, falsifiable question:

> Does the restriction of a natural integral Monster module to a chosen \(U_4(2)\cong PSp(4,3)\) subgroup contain the W33 Steinberg module of degree \(81\), and if so with what multiplicity and integral form?

No claim of occurrence is made here. The point is that this question is executable with character restriction or `mmgroup` once a subgroup representative and class fusion are fixed.

## Evidence firewall

Claims are assigned four levels:

- **A — arithmetic:** exact identities and divisibility.
- **B — documented group fact:** established subgroup or character-table information.
- **C — explicit structural certificate:** generators, class fusion, intertwiner, module restriction, or algebra map.
- **D — physical interpretation:** requires C-level mathematics plus an experimentally meaningful model.

No A-level identity should be narrated as C- or D-level mechanism.

## External research checked

- ATLAS data for the Monster order, primes, generators, and maximal subgroups.
- GAP/CTblLib data identifying \(U_4(2)\cong PSp(4,3)\).
- Published subgroup work documenting \(U_4(2)\) inside the Monster while distinguishing it from the non-embedding of the double cover \(2.U_4(2)\).
- Current computational Monster work based on `mmgroup`, which makes the proposed embedding and class-fusion certificate practically testable.

## Honest boundary

This pass does not construct the Monster, run `mmgroup`, calculate class fusion, or prove an \(81\)-dimensional constituent. It converts the Monster program from a collection of integer coincidences into a precise computational representation-theory agenda with a fail-closed claim policy.
