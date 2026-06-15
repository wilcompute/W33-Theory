# BT1122 — Patch-helper build path

BT1122 wires the safe BT1119 patch helpers into the paper build path.

## Updated build script

```text
tools/bt1094_build_papers.py
```

now runs, in order:

```text
python tools/bt1119_patch_w33_sections.py
python tools/bt1119_patch_holonet_sections.py
python tools/bt1106_emit_section_report.py
python tools/bt1100_tex_path_sanity.py
```

before attempting TeX compilation.

## Why this matters

The build path no longer depends on the older monolithic integration helper.  It uses the small idempotent patch helpers that were added specifically to avoid connector filtering and unsafe full-source replacement.

## Boundary

BT1122 updates the build path.  It does not claim that the papers compile in this chat environment.
