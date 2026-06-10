# BT732 — Selector Sibling Sparse Export Certificate

BT731 exported the full compressed sparse row stream for `1110_011` / `1110_r0`.

BT732 extends the intrinsic selected-mask family:

| channel | sheet | rows | columns | entries/row | rank over F_1000003 | raw SHA256 | gzip SHA256 | payload status |
|---|---:|---:|---:|---:|---:|---|---|---|
| `011_far` | `1110_r0` | 2160 | 160 | 8 | 81 | `454e864ad1b82703cec4917e08c48332306cb8813581b5de8bf25149a77d69a0` | `404414067307e989bafd4692793a40f9da4ae741fd7d3f80f1d0093a4348855f` | full payload in BT731 |
| `101_middle` | `1110_r1` | 2160 | 160 | 8 | 81 | `729e33db5ead8b401c195688fd169531458dd9c6ebdd32a4b8d3d6030687668f` | `154b317ae1ae5b08e6b16a39a1a90c516d2230e3688f6d55cd51f89650457f2d` | full payload in `data/PART_BT732_SELECTOR_1110_101_COMPRESSED_ROWS.json` |
| `110_active` | `1110_r2` | 2160 | 160 | 8 | 81 | `ec10fe71db60f712a1a8a0b7cc84b7e882ce1a624c61181b959fff10af14bf1a` | `cbca3146149f73928cfcab33e6d2d8bf03e8cd2f6de9720b9a1d04d7bf1b5bf9` | certificate only; full inline payload deferred |

## Interpretation

All three intrinsic channels for selected mask `1110` are independently rank-complete Hodge selector sheets. This matches the prior BT724 intrinsic-channel certificate:

```text
011/far    -> 1110_r0
101/middle -> 1110_r1
110/active -> 1110_r2
```

and confirms that the selected mask does not depend on a single residual channel to reach the protected rank-81 Levi cycle sector.

## Boundary

The `1110_r2` full payload was generated locally and hash-certified, but the base64 stream is large enough that a compact certificate is safer than risking a truncated repository artifact. The next executable step is to add a repo-side generator that writes all three payloads from `analysis/bt713_selector_sheet_rank_filter.py` deterministically inside the repository checkout.
