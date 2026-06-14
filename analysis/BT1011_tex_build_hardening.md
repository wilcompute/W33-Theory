# BT1011 — TeX build hardening

BT1011 adds a dedicated paper-build workflow rather than overloading the R3 smoke
workflow.

## Workflow

```text
.github/workflows/paper-build.yml
```

## Behavior

The workflow applies the R3 paper integrators:

```text
tools/integrate_bt990_r3_fat_tower_w33.py
tools/integrate_bt990_r3_fat_tower_holonet.py
tools/integrate_bt996_r3_edgewise_hodge_stack_w33.py
tools/integrate_bt996_holonet_edgewise_hodge.py
```

Then it builds:

```text
w33_paper.tex
photonic_holonet.tex
```

and uploads:

```text
w33_paper.pdf
photonic_holonet.pdf
```

## Reading

Paper builds are now isolated from R3 smoke tests. The R3 workflow can remain
cheap and fast, while the dedicated paper workflow owns PDF artifact production.

## Witnesses

```text
.github/workflows/paper-build.yml
data/bt1011_tex_build_hardening.json
```
