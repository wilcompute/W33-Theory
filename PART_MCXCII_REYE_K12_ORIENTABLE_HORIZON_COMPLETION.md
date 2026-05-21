# Part MCXCII: Reye-K12 Orientable Horizon Completion

## Claim Boundary

MCXCII is a finite oriented incidence-completion theorem. It starts from the
MCLXXXII fact that the antipodal Q4 quotient is Reye's `12_4,16_3`
configuration, then uses the 12 Reye points as the vertices of a K12 triangular
horizon.

It proves an explicit orientable twofold triple-system completion containing
the 16 Reye lines as triangular faces. It does not claim a continuum dynamics
law.

## Statement

MCLXXXII gave:

```text
Q4 antipodal quotient = Reye (12_4,16_3)
12 points             = tomotope edges / Q4 face-orbits
16 lines              = tomotope triangles / Q4 edge-orbits
48 incidences         = tomotope edge-triangle medial layer
```

MCXCII promotes those 12 Reye points to the vertex set of `K12`.

The verifier constructs an oriented face set with:

```text
16 Reye triangles,
28 residual completion triangles,
44 total triangles.
```

Every directed edge of `K12` appears exactly once, and every unordered edge
appears exactly twice:

```text
132 directed edges = 12 * 11,
66 unordered edges = C(12,2),
each unordered edge has two opposite directed appearances.
```

So this is an orientable triangular completion of the `K12` horizon containing
the tomotope/Reye skeleton as its first 16 triangular faces.

## Surface Data

The completed horizon has:

```text
V = 12,
E = C(12,2) = 66,
F = 44.
```

Euler characteristic:

```text
chi = V - E + F = 12 - 66 + 44 = -10.
```

Thus:

```text
g = (2 - chi)/2 = 6 = q!.
```

This is the K12 information-hole surface. Its hole cost is:

```text
2g = 12 = k.
```

## Horizon Code Reading

The `[72,66]_3` horizon code is now the K12 edge payload plus one parity/check
symbol per orientable information hole:

```text
payload = C(12,2) = 66,
parity  = genus = 6,
total   = 66 + 6 = 72.
```

So:

```text
[72,66]_3 = K12 edge payload + six genus-hole parity symbols.
```

## Residual Packet

The 16 Reye triangles account for the tomotope medial layer. In pair-count
terms:

```text
48 K12 edges appear in a Reye line,
18 K12 edges are non-Reye edges.
```

The orientable completion adds:

```text
28 residual triangles,
84 residual directed edge incidences.
```

The count `84` is one toroidal flag packet, so the completion sits exactly at
the interface of:

```text
tomotope/Reye medial skeleton,
K12 genus-six horizon,
toroidal flag residual.
```

## Source Alignment

- MathWorld, Graph Genus: records the complete-graph genus formula
  `gamma(K_n)=ceil((n-3)(n-4)/12)`.
  https://mathworld.wolfram.com/GraphGenus.html
- Ellingham and Stephens, *Triangular embeddings of complete graphs*: triangular
  embeddings of complete graphs are neighborly maps / twofold triple systems.
  https://math.vanderbilt.edu/ellingmn/paper/tricomp/a10.pdf
- Monson, Pellicer, and Williams, *The Tomotope*: identifies Reye's
  configuration inside the tomotope medial layer.
  https://bmonson.ext.unb.ca/fields/tom.pdf

## Artifacts

- Analysis: `analysis/w33_reye_k12_orientable_horizon_completion.py`
- Tests: `tests/test_w33_reye_k12_orientable_horizon_completion.py`
- Result: `PART_MCXCII_REYE_K12_ORIENTABLE_HORIZON_COMPLETION_results.json`
