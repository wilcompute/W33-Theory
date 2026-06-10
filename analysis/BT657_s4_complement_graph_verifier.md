# BT657 — S4 Complement Graph Verifier

This executes the first BT656 next step: build the explicit 16-flag complement graph and test the Q4 hypothesis.

## Deterministic setup

Use the same W33 model as the Levi/Hodge stack:

- points are projective points of F3^4;
- adjacency is symplectic orthogonality;
- W33 lines are the 40 maximal K4 cliques;
- Levi flags are point-line incidences;
- the Levi flag graph is the line graph of the point-line Levi graph, so two flags are adjacent iff they share a point or share a W33 line.

A deterministic S4 subgroup of PSp(4,3) has orbit profile

```text
8,8,24,24,24,24,24,24.
```

The complement of the six regular 24-orbits has size

```text
8+8=16.
```

## Graph test

Let C16 be the induced subgraph of the Levi flag graph on this 16-flag complement.

The verifier result is:

```text
|V(C16)| = 16
|E(C16)| = 24
regular degree = 3
connected components = 4
component sizes = 4,4,4,4
component graph type = K4 + K4 + K4 + K4
```

Therefore:

```text
C16 is not Q4.
```

because Q4 has 16 vertices, 32 edges, degree 4, and is connected.

It is also not K4,4 or Q4/{pm} under the Levi flag adjacency.

## What the 16 complement actually is

The 16 complement flags are four complete W33 line fibers:

```text
4 lines * 4 flags per line = 16 flags.
```

Each line fiber is a K4 inside the flag graph because the four flags share the same W33 line.

Thus the corrected decomposition is

```text
160 = 6*24 + 4*4.
```

Read as:

```text
six regular S4 sign carriers + four tetrahedral line-fiber codec cells.
```

## Boundary

BT655's Q4/codec-boundary interpretation survives only at the count/module level.  The actual Levi-flag adjacency on the 16 complement flags is 4K4, not Q4.  A Q4 structure, if present, must use a different boundary relation than raw Levi flag adjacency.
