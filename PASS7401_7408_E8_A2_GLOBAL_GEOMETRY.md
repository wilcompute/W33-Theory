# Passes 7401–7408 — Global E8 A2 Geometry and the 2240 Eisenstein W(3,3) Leaves

## Status

**THEOREM-GRADE / machine verified.**

Verifier: `analysis/w33_pass7401_7408_e8_a2_global_geometry.py`

Certificate: `data/PASS7401_7408_E8_A2_GLOBAL_GEOMETRY_results.json`

## What is new

The current Eisenstein bridge proves that one fixed-point-free order-three structure J on E8 selects 40 of the 1120 A2 root subsystems and that orthogonality on those 40 is W(3,3). This pass removes the choice of J and computes the **global A2 geometry of E8**.

Starting from the 240 roots, the verifier independently rebuilds all

\[
\boxed{1120}
\]

A2 root subsystems and joins two when their rank-two planes are orthogonal.

The resulting graph Gamma_A2(E8) has

\[
\boxed{1120\text{ vertices},\qquad k=120,\qquad |E|=67200.}
\]

Its spectrum is

\[
\boxed{120^1,\quad20^{84},\quad8^{300},\quad(-4)^{700},\quad(-40)^{35}.}
\]

It is edge-regular but not strongly regular:

\[
\boxed{\lambda=2}
\]

for every adjacent pair, while nonadjacent pairs have exactly

\[
\boxed{10,\ 16,\ \text{or }40}
\]

common neighbors.

The five relation valencies are

\[
\boxed{1,\ 120,\ 648,\ 270,\ 81.}
\]

The verifier checks closure under multiplication by the orthogonality adjacency matrix; the induced five-dimensional multiplication operator has the five distinct eigenvalues

\[
120,\ 20,\ 8,\ -4,\ -40,
\]

so the five relations form a commutative rank-five association scheme.

## Unique A2^4 completion

Because every orthogonal pair has exactly two common A2 neighbors, and those two are themselves orthogonal, every orthogonal pair lies in one and only one 4-clique.

Hence:

\[
\boxed{\text{every }2A_2\text{ extends to a unique }4A_2.}
\]

The complete line census is

\[
\boxed{11200\text{ copies of }A_2^4.}
\]

Each line contains 4 A2's and every A2 lies on exactly 40 lines:

\[
\boxed{(1120_{40},\,11200_4).}
\]

The edge count closes exactly:

\[
11200\binom42=11200\cdot6=\boxed{67200}.
\]

This recovers the classical 2A2 and 4A2 reflection-subsystem counts directly from the 240-root model.

## All Eisenstein W(3,3) leaves

Pass 1020 already identified the centralizer of a regular order-three element:

\[
C_{W(E_8)}(J)\cong G_{32}\cong C_3\times Sp_4(3),\qquad |C|=155520.
\]

The later normalizer computation gives

\[
|N_{W(E_8)}(\langle J\rangle)|=311040.
\]

Therefore the conjugacy family of cyclic Eisenstein structures has size

\[
\boxed{\frac{|W(E_8)|}{311040}=\frac{696729600}{311040}=2240.}
\]

Equivalently, there are 4480 regular order-three elements and each cyclic subgroup contributes the pair J,J^{-1}:

\[
\boxed{4480=2\cdot2240.}
\]

So the phrase “E8 contains a family of W(3,3)'s” can now be made exact:

\[
\boxed{E_8\text{ contains }2240\text{ conjugate Eisenstein }W(3,3)\text{ leaves.}}
\]

## Global incidence replication numbers

Each leaf contains 40 A2 points, 240 orthogonal 2A2 pairs, 40 A2^4 lines, and 90 J-stable D4's. Double counting gives

\[
\boxed{r_{A_2}=80,\qquad r_{2A_2}=8,\qquad r_{4A_2}=8,\qquad r_{D_4}=64.}
\]

Thus every A2 lies on 80 W33 leaves, every orthogonal A2 pair lies on 8 leaves, every A2^4 line lies on 8 leaves, and every D4 lies on 64 leaves.

## Why this matters for the project

A single W(3,3) is not an isolated 40-point coincidence inside E8. It is a 40-point induced slice of a much larger 1120-point association geometry intrinsic to the complete E8 root system.

More sharply:

\[
\boxed{W(3,3)\hookrightarrow\Gamma_{A_2}(E_8)}
\]

as one of 2240 conjugate Eisenstein leaves, and its line-completion law is inherited from the global unique 2A2->4A2 completion.

That turns the current bridge from “one chosen complex structure produces W33” into a **global incidence design of all such complex structures**.

## Prior art / rediscovery boundary

This pass does **not** reclaim the known facts that E8 has 1120 A2 subsystems, 67200 2A2 subsystems, or 11200 4A2 subsystems. Those classical reflection-subgroup counts are independently reproduced by the verifier.

It also does not reclaim the Springer/Reeder order-three centralizer or the repo's earlier G32 theorem.

New here is the welded structure:

1. the explicit 1120-vertex orthogonality association scheme and spectrum;
2. unique 2A2->4A2 completion in the root model;
3. the exact 2240-leaf family;
4. the replication numbers 80,8,8,64;
5. the interpretation of every W33 leaf as a 40-point slice of one global E8 A2 geometry.

## External references checked

- M. Reeder, *Elliptic centralizers in Weyl groups and their coinvariant representations*, Representation Theory 15 (2011), 63–111.
- Classical reflection-subgroup census for W(E8), including A2, 2A2, 4A2, and D4 classes.
- Springer's regular-element theorem as used in the repo's Pass 1020.

## Evidence boundary

Everything through the association scheme, unique A2^4 completion, and raw counts is reconstructed directly from the 240 roots.

The count 2240 imports the previously certified normalizer order 311040. The D4 replication imports the current certified 90 J-stable D4's per leaf.

No Standard Model, coupling, or hardware claim follows from these finite-geometric statements by itself.
