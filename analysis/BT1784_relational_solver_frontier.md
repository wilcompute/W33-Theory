# BT1784 relational solver frontier

The relational solve over the BT1781 tables was started at the schema level.

Current committed data contains the table dimensions and accepted tuple counts, but not the actual accepted tuples. That is enough to define the join problem, but not enough to count or classify global solutions.

Schema:

```text
9 variables: R0,R1,R2,C0,C1,C2,D0,D1,D2
12 values per variable
18 ternary constraints, one for each nonconcurrent Hesse row-column-diagonal triangle
9980 accepted local triples total
```

Important result: BT1781 already proves unary arc consistency is saturated. Every one of the nine variables still supports all 12 values. Therefore a relational solver must use actual ternary tuple contents and higher-order joins; counts alone cannot decide uniqueness of the incumbent.

Join plan for the next executable solver:

```text
1. materialize all 18 accepted ternary tables, not just counts
2. project each ternary table to its three binary faces
3. enforce pair consistency across shared variable pairs
4. run incumbent-first DFS in row/column/diagonal order
5. quotient surviving solutions by BT1758 plateau symmetries
```

Boundary: this pass reaches the exact relational-solver frontier but does not certify incumbent uniqueness, because the accepted tuple lists were not available in committed data.
