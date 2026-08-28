# W(3,3) optimal near-ovoid defect-dipole theorem

**Date:** 2026-08-28  
**Verifier:** `analysis/w33_20260828_optimal_near_ovoid_dipole.py`  
**Certificate:** `data/PART_W33_20260828_OPTIMAL_NEAR_OVOID_DIPOLE.json`

## Result

For a 10-point set `S` in the symplectic generalized quadrangle `W(3,3)`, define its ovoid deficiency to be the number of W33 lines missed by `S`. The minimum is

\[
\boxed{\operatorname{def}(W(3,3))=3}.
\]

The new result is the complete classification of every optimum.

Every optimal 10-set has line profile

\[
\boxed{0^3\,1^{34}\,2^3}.
\]

Its three missed lines are the three non-hinge lines through a unique point `a`. Its three doubled lines are the three non-hinge lines through a unique point `b`. The two centers are collinear, and their common line is the unique line omitted from both defect pencils; that hinge line is met exactly once.

Thus an optimum is a finite **defect dipole**

\[
\boxed{
(a\;\text{miss pencil})
\;--\;\ell_{ab}\;--\;
(b\;\text{double pencil})
}
\]

with three missing arms at one endpoint and three doubled arms at the other.

For every ordered collinear pair `(a,b)` there are exactly six completions. Since W33 has

\[
40\cdot 12=480
\]

ordered collinear pairs,

\[
\boxed{480\cdot 6=2880}
\]

optimal near-ovoids exist.

The projective inner group is transitive on all of them:

\[
\boxed{PSp(4,3)\curvearrowright 2880\text{ optima transitively},}
\]

and an optimum has stabilizer

\[
\boxed{C_3\times C_3}
\]

of order 9.

Fixing an oriented defect dipole `(a,b)`, its order-54 stabilizer acts transitively on the six local completions. The induced six-state group has order 18 and splits explicitly as

\[
\boxed{C_3\times S_3},
\]

with kernel `C3` in the order-54 edge stabilizer.

## Why the classification is exact

Let `N` be the 40-by-40 line/point incidence matrix and `A_L` the line-collinearity graph. Then

\[
NN^T=A_L+4I,
\]

where `A_L` is again `SRG(40,12,2,4)`. Define

\[
K=(A_L-12I)(A_L-2I)=96E_{-4}.
\]

Then

\[
\boxed{KN=0}.
\]

If a 10-set has line-count vector `1+d`, then `Kd=0`. This gives a cheap exact obstruction before any subset search.

* deficiency 0: a direct exact-cover backtracker finds no binary solution;
* deficiency 1: the 40 columns of `K` are distinct, so no one-minus/one-plus defect can cancel;
* deficiency 2: every two-column signature is unique and no doubled column matches one, so both possible excess partitions are impossible;
* deficiency 3: among all `C(40,3)=9880` triple signatures there are exactly `9720` singleton classes and `40` classes of size four. The `(+2,+1)` and `(+3)` excess partitions have no matching signature, leaving only three doubled lines.

Each size-four collision class is exactly the four punctured line-pencils based at the four points of one W33 line. Therefore missed and doubled triples must be two different members of the same class, which is exactly the defect-dipole theorem.

An exact binary backtracker finds six completions for one oriented dipole. A deterministic transvection generation of `PSp(4,3)` gives order 25920 and is transitive on the 480 ordered collinear pairs, so six completions occur for every dipole. The orbit of one completion has size 2880, closing the global count independently.

## Cross-track consequence

Holotrade had already proved `def(3)=3` by CP-SAT and found one profile `0^3 1^34 2^3`. This theorem removes the solver from the structural statement and upgrades one witness to a complete classification.

It also supplies a new warning for the current six-state frontier. The six local near-ovoid completions form a **transitive** `C3 x S3` six-state carrier. The current Hall–Janko / `P1(F9)` involution quotient also has six states, but its split-projective centralizer has the different `2+4` orbit geometry. Equal cardinality therefore does not identify those two six-state objects; an intertwiner would still be required.

## Evidence boundary

Everything above is finite combinatorics and exact permutation/incidence algebra. No physical interpretation is asserted. In particular, the words *dipole*, *hinge*, and *completion* name the verified incidence structure only.
