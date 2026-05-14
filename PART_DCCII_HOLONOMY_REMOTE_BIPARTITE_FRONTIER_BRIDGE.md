# Part DCCII — Holonomy Remote-Bipartite Frontier Bridge

## Why this part exists

`Part DCCI` split the active complement into one fan-adjacent sector and two remote rank-`6` sectors.

This part zooms in on the remote side and makes that split fully explicit.

## Exact remote reduction

The verifier proves that the remote 12-point shell is already the disjoint union of two exact `K_{3,3}` witness components:

- upper remote: `{3,4,5} \times {12,13,14}`,
- lower remote: `{6,7,8} \times {9,10,11}`.

Each component already has full restricted curvature rank `6`.

The current host still vanishes on both.

So the remote side of the remaining curved frontier is reduced to:

> the first nonzero row-entry witness in either exact remote `K_{3,3}` component.

## Executable artifact

Verifier:

```text
verify_dccii_holonomy_remote_bipartite_frontier_bridge.py
```

Tests:

```text
tests/test_dccii_holonomy_remote_bipartite_frontier_bridge.py
```

Generated summary:

```text
data/dccii_holonomy_remote_bipartite_frontier_bridge.json
```

---
*W33-Theory | Part DCCII | the remote side of the remaining curved frontier is exactly the first nonzero row-entry witness in one of two rank-`6` remote `K_{3,3}` components.*
