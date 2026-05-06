# Open-Turn and Complement-Duality Correction

This note updates the response architecture after Parts CCCLXX and CCCLXXIV.

## Direct W33 open turns

A direct Hashimoto open turn in W33 is an ordered path

```text
a -> b -> c
```

with

```text
a adjacent b,
b adjacent c,
a not adjacent c.
```

Therefore its underlying three-vertex induced subgraph has exactly two W33 edges.

So the direct canonical identification is

```text
open turns in G  <->  oriented two-edge triples in G.
```

There are

```text
2160 two-edge triples in G
```

and each has two endpoint orientations around its unique middle vertex, so

```text
2 * 2160 = 4320 open turns in G.
```

## One-edge triples

The one-edge triples in W33 also have count

```text
4320.
```

But they are not the direct open turns of G.

They are complement-dual:

```text
one-edge triples in G  <->  two-edge triples in complement(G).
```

After orienting around the unique middle vertex in the complement graph, they give the open turns of the complement graph.

## Corrected architecture statement

Use this rule:

```text
Direct G open dynamics: oriented two-edge triples in G.
Complement-dual open dynamics: one-edge triples in G, viewed as two-edge triples in complement(G).
Triangle/closed dynamics: three-edge triples in G.
```

This keeps the direct Hashimoto decomposition separate from the complement-dual parity decomposition.
