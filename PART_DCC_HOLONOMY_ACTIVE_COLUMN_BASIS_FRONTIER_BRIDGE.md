# Part DCC — Holonomy Active-Column Basis Frontier Bridge

## Why this part exists

`Part DCXCIX` showed that the remaining curved frontier is universal across the active curvature columns.

The next question is whether those columns are only a support family, or already the exact full-rank basis block carrying the live wall.

This part proves that they are.

## Exact active-basis reduction

The verifier proves:

- the off-diagonal curvature block has rank `36`,
- the `36` active columns already realize full restricted rank `36`,
- the remaining `9` columns are a rigid inert complement split into the three triples

$$
\{36,40,44\},\qquad \{37,41,42\},\qquad \{38,39,43\}.
$$

So the remaining curved frontier is no longer “somewhere in 45 sign channels.”

It is:

> the first nonzero row entry on the exact full-rank 36-column active complement.

## Executable artifact

Verifier:

```text
verify_dcc_holonomy_active_column_basis_frontier_bridge.py
```

Tests:

```text
tests/test_dcc_holonomy_active_column_basis_frontier_bridge.py
```

Generated summary:

```text
data/dcc_holonomy_active_column_basis_frontier_bridge.json
```

---
*W33-Theory | Part DCC | the remaining curved frontier sits on the exact full-rank 36-column active complement, with the other 9 columns forming a rigid inert triple decomposition.*
