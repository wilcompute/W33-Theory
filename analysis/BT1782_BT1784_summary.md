# BT1782-BT1784 summary

Executed all three requested next moves after BT1779-BT1781.

## BT1782: non-induced selected adjacency

Added `analysis/bt1782_noninduced_selected_adjacency.py`.

The completion graph is now encoded as the non-induced selected-adjacency product:

```text
C10 square K3
30 vertices
60 selected links
30 strand links
30 cross-section links
degree 4 at every vertex
```

Interpretation: C10 is the BC-ring backbone, and K3 is the three-strand triangular cross-section selector. This avoids the BT1779 induced-subgraph obstruction.

## BT1783: D5 rephased hexagon bus

Added `analysis/bt1783_d5_rephased_hexagon_bus.py`.

BT1780 showed inversion is cyclewise, not globally phased in the original labels. BT1783 independently rephases the eight Coxeter 5-cycles with shifts:

```text
[2,0,3,1,3,0,3,4]
```

After this gauge choice, the inversion witness acts uniformly as:

```text
q -> -q mod 5
```

Thus the five bus phases carry a clean D5-equivariant structure.

## BT1784: relational solver frontier

Added `analysis/BT1784_relational_solver_frontier.md`.

The relational solver can now be specified exactly, but the committed data contains accepted tuple counts rather than materialized tuple lists. BT1781 proves unary arc consistency is saturated: every slot still has all 12 values. Therefore uniqueness cannot be certified from counts alone; the next executable solver must materialize the 18 accepted ternary tables, project binary faces, enforce pair consistency, and then run DFS modulo BT1758 plateau symmetries.
