# Part DCCLV - Frobenius-Octahedral Edge-Phase Lift

## Why this part exists

DCCLIV selects `q = 3` by the Frobenius equation:

```text
q^5 - q = E(GQ(q,q)).
```

DCCXLIX identifies the six-level closure clock with the octahedron. This part
welds those facts to the W33 edge/QEC/root carrier.

## Exact carrier factorization

At `q = 3`:

```text
q^5 - q = 240.
```

The same `240` is:

```text
W33 edges
E8 roots
W33 CSS physical edge/code slots
Frobenius non-base elements of F_{3^5} over F_3.
```

The new factorization is:

```text
240 = 40 * 6
    = W33 projective points * octahedral antipodal edge-pair phases.
```

The directed lift is:

```text
480 = 40 * 12
    = W33 projective points * octahedron edges.
```

So DCCLV gives the phase-space reading of the 240/480 carrier split:

```text
unoriented edge/root/code carrier: 40 x 6
directed Hashimoto/fusion carrier: 40 x 12
```

## Why the six phases are octahedral

The octahedron has 12 edges. Under the antipodal map on the six signed
bivector vertices, those 12 edges split into 6 antipodal edge-pairs.

Those six local phase pairs are exactly:

```text
k/2 = 12/2 = 6
q! = 3! = 6
octahedral antipodal edge-pair count = 6.
```

This is the same six-shell that appears as the `+6` in:

```text
240 = 72 + 6 + 81 + 81.
```

## QEC reading

The W33 CSS carrier closes as:

```text
240 = 39 + 120 + 81
```

where:

```text
39  = independent vertex X checks
120 = independent triangle Z checks
81  = H1 logical sector.
```

DCCLV says that this 240-slot QEC carrier can be read as a vertex-phase
ledger:

```text
physical edge slot = W33 vertex selector + octahedral phase-pair.
```

The directed 480-slot fusion/Hashimoto carrier keeps the full local 12-channel
octahedral alphabet.

## Exact vs conditional

- **Exact:** the selected Frobenius carrier, W33 edge carrier, E8 root count,
  and CSS physical-slot count are all `240`, and they factor as `40 x 6`.
- **Exact:** the directed carrier is `480 = 40 x 12`, matching the full
  nonempty clique-chain dimension `40 + 240 + 160 + 40`.
- **Conditional:** this is a count-preserving phase/ledger lift, not a
  canonical incidence-preserving bijection from W33 edges to vertex-phase pairs.

## Executable artifact

- Verifier: `verify_dcclv_frobenius_octahedral_edge_phase_lift.py`
- Tests: `tests/test_dcclv_frobenius_octahedral_edge_phase_lift.py`
- Data: `data/dcclv_frobenius_octahedral_edge_phase_lift.json`
