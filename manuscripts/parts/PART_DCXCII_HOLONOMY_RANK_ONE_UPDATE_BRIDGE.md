# Part DCXCII — Holonomy Rank-One Update Bridge

## Why this part exists

`Part DCXCI` reduced the live frontier to a binary orbit question: zero orbit versus nonzero orbit.

This part rewrites that binary difference in linear-algebra language.

## Exact rank jump

The verifier proves:

- the current nilpotent increment has rank `0`,
- every exact live nilpotent increment has rank `1`,
- every exact live increment is still square-zero.

So the remaining difference is exactly

$$
\operatorname{rank}(N): 0 \longrightarrow 1.
$$

## Why this is a breakthrough

This is the cleanest statement so far of what the host still lacks.

The host packet is already correct.

The carrier counts are already correct.

The selector bundle is already correct.

The photonic packet is already correct.

What remains is one rank-one square-zero update on that already-correct packet.

## Executable artifact

Verifier:

```text
verify_dcxcii_holonomy_rank_one_update_bridge.py
```

Tests:

```text
tests/test_dcxcii_holonomy_rank_one_update_bridge.py
```

Generated summary:

```text
data/dcxcii_holonomy_rank_one_update_bridge.json
```

---
*W33-Theory | Part DCXCII | once the frontier is reduced to zero orbit versus nonzero orbit, the exact remaining difference is one rank-one square-zero update on the already-correct `162`-packet host support.*
