# BT665 — Codec/G2 Integration Status

BT660-BT664 are now staged for paper use.

## Current files

- `analysis/BT660_secondary_codec_q4_relation.md`
- `analysis/BT661_three_pair_g2_channel_candidate.md`
- `analysis/BT662_secondary_codec_g2_channel_insert.tex`
- `tools/integrate_bt662_insert.py`
- `analysis/BT663_six_carrier_k33_g2_relation.md`
- `analysis/BT664_nine_codec_gauge_selection.md`

## Local checkout run order

```bash
python tools/integrate_bt659_insert.py
python tools/integrate_bt662_insert.py
python analysis/bt574_latex_sanity_verifier.py
python tools/build_w33_preprint.py --compile
```

## Safe manuscript statement

The raw Levi complement is

```text
4K4.
```

The secondary codec chain is

```text
4K4 -> Q4 -> K4,4.
```

The six-carrier channel is

```text
6 = 2_far + 2_middle + 2_active.
```

The K3,3 / W(G2) structure is currently a secondary carrier-label quotient, not a proven flag-level Weyl action.

## Boundary

Do not claim that the raw complement is Q4.  Do not claim a full W(G2) action on the 160 Levi flags from this layer alone.
