# BT731 — Selector `1110_011` Sparse Export Certificate

This artifact completes the first actual sparse-row export promised after BT728.

## Selected sheet

- mask: `1110`
- channel: `011 / far`
- residual sheet: `r0`
- sheet label: `1110_r0`

## Exported data

The exported payload is stored in:

```text
data/PART_BT731_SELECTOR_1110_011_COMPRESSED_ROWS.json
```

It contains the complete `1110_r0` row stream as `gzip+base64`.

Row format after decompression:

```text
col:+,col:-,col:+,...
```

with one row per centered local `K_{3,3}` rectangle.

## Verification

- rows: `2160`
- columns: `160`
- entries per row: `8`
- rank over `F_1000003`: `81`
- unique Levi 8-cycles seen during generation: `1620`
- cycle presentation multiplicity: `32`
- uncompressed SHA256: `454e864ad1b82703cec4917e08c48332306cb8813581b5de8bf25149a77d69a0`
- compressed SHA256: `404414067307e989bafd4692793a40f9da4ae741fd7d3f80f1d0093a4348855f`

## Boundary

This is the first full compressed row export for one intrinsic channel. BT728 only recorded the export contract. BT731 contains the actual row payload for `1110_011`; the sibling channels `1110_101` and `1110_110` remain unexported as full row streams.
