## Pass 4202 — extremality versus universality, exhausted

Pass 4201 left three data points suggesting that spectrally optimal presentations of the
frame algebra cannot compute, and computing ones cannot be optimal. Three points is a
slogan. This exhausts the search.

Every subset of the ten natural generators, sizes 4 through 8: is the simple Cayley graph
on the 81 frames regular and connected, and does the set generate all of `ASp(4,3)`?

```text
size   regular & connected   of which generate the full group
  4            1                        0
  5            2                        0
  6            1                        0
  7            0                        0
  8            0                        0
```

> **Zero.** Every regular presentation generates a **proper** subgroup; every universal
> presentation has an **irregular** graph.

### What that means for three failed passes

Passes 3060, 3080 and 3120 tried to decide whether the instruction layer satisfies the
graph Riemann Hypothesis, and failed in three different ways. The reason is now visible and
it is not a matter of technique:

> **The Ramanujan property and the graph RH are not merely unproven for a universal
> instruction set here — they are not *defined* for one.** Both are properties of regular
> graphs, and no universal presentation in this family has a regular graph.

Three failed computations were not three mistakes about a hard question. They were three
attempts to measure a quantity the object does not have.

### And it explains the shape of two other results

- Pass 3121: `18` collisions out of 324 outgoing edges is the irreducible price of
  containing a Clifford operation. Collisions are exactly what destroys regularity.
- Pass 3122: the abelian 8-regular graph is Ramanujan, diameter 4, and cannot compute —
  a routing layer, not a compute layer.

All three are the same fact seen from different sides: **the structure that makes a
generating set universal is the structure that makes its graph irregular.**

### Scope, stated plainly

Exhaustive over the ten generators this project uses, at sizes four through eight. It is
**not** a statement about every conceivable generating set of `ASp(4,3)` — a generator
outside this pool could behave differently, and the natural next question is whether one
exists.

---

## Ledger

| claim | status |
|---|---|
| no regular universal presentation, sizes 4–8 | **exhaustive over this pool** |
| regular sets generate 81, 243, and one more proper subgroup | proved |
| Ramanujan / graph RH are undefined for a universal ISA here | follows |
| the three failed passes measured a non-existent quantity | explains 3060, 3080, 3120 |
| tension is structural, not incidental | three routes agree |

## Still open

- A generating set of `ASp(4,3)` outside this pool with a regular Cayley graph, or a proof
  that none exists over all generating sets.
