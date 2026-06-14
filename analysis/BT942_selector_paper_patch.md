# BT942 — Selector paper patch

BT942 adds a concise paper-facing appendix for the BT924--BT941 E8 selector thread.

## Files

```text
paper/BT942_e8_selector_appendix.tex
tools/integrate_bt942_selector_appendix.py
data/bt942_selector_paper_patch.json
```

## Scope

The appendix summarizes:

- BT924: integer Smith form and the valuation-one rank-eight sector;
- BT925: canonical mod-2 bilinear form on H;
- BT926--BT930: vertex and tetracode metric E8 witnesses plus basis-dependent maps;
- BT931--BT941: support selector candidate, tetracode symmetry, and remaining proof obligations.

## Honest boundary

The root `W36_PAPER.tex` is not directly overwritten in this connector pass. The patch is available as an idempotent integrator:

```bash
python tools/integrate_bt942_selector_appendix.py
```

The appendix states that existence of compatible E8 gauges is now established, but canonical selector uniqueness remains open.
