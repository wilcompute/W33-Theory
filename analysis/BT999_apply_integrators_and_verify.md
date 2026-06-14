# BT999 — Apply integrators and verify paper build packet

BT999 packages the paper application step into a reproducible checkout command.

## Script

```text
tools/bt999_apply_integrators_and_verify.sh
```

The script applies:

```text
tools/integrate_bt990_r3_fat_tower_w33.py
tools/integrate_bt990_r3_fat_tower_holonet.py
tools/integrate_bt990_open_frontiers.py
tools/integrate_bt996_r3_edgewise_hodge_stack_w33.py
tools/integrate_bt996_holonet_edgewise_hodge.py
```

Then it verifies markers in:

```text
w33_paper.tex
photonic_holonet.tex
OPEN_FRONTIERS.md
```

and writes:

```text
data/bt999_integrator_marker_check.json
```

If `latexmk` is available, it also builds:

```text
w33_paper.tex
photonic_holonet.tex
```

## Boundary

The GitHub connector committed the apply-and-verify script and manifest, but it
does not provide a full checkout/LaTeX runtime. Therefore the actual compile must
be run by this script in a checkout or CI job.

## Witnesses

```text
tools/bt999_apply_integrators_and_verify.sh
data/bt999_apply_integrators_and_verify_manifest.json
```
