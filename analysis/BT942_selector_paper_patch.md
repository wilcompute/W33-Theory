# BT942 — Selector appendix source

BT942 adds a concise paper-facing appendix source for the BT924--BT941 E8 selector thread.

## Files

```text
paper/BT942_e8_selector_appendix.tex
data/bt942_selector_paper_patch.json
```

## Correct routing after BT946/BT947

Wil corrected the manuscript split:

```text
photonic_holonet.tex = current main narrative / architecture paper
w33_paper.tex       = heavy-math manuscript target
```

The appendix belongs in `w33_paper.tex`, not `W36_PAPER.tex`.

## Current integrator

```bash
python tools/integrate_bt942_selector_appendix_w33.py
```

For verification/compile in a full checkout:

```bash
python tools/bt947_w33_selector_appendix_verify.py
```

## Scope

The appendix summarizes:

- BT924: integer Smith form and the valuation-one rank-eight sector;
- BT925: canonical mod-2 bilinear form on H;
- BT926--BT930: vertex and tetracode metric E8 witnesses plus basis-dependent maps;
- BT931--BT941: support selector candidate, tetracode symmetry, and remaining proof obligations.

## Honest boundary

The appendix states that existence of compatible E8 gauges is now established, but canonical selector uniqueness remains open.
