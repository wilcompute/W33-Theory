# BT1100 — No-network TeX/path sanity check

BT1100 adds a deterministic paper check that does not require TeX installation, GitHub Actions timing, or internet access.

## Script

```text
tools/bt1100_tex_path_sanity.py
```

The script checks:

```text
1. W33 insertion marker exists,
2. holonet insertion marker exists,
3. latest integration helper exists,
4. every expected W33 input section resolves to an existing file,
5. every expected holonet input section resolves to an existing file,
6. staged section files have simple balanced braces,
7. staged section labels are unique.
```

## Expected W33 sections

```text
paper/sections/sec_bt1083_1085_matter_bridge.tex
paper/sections/sec_bt1086_1088_core_reservoir.tex
paper/sections/sec_bt1089_1090_natural_core_intertwiner.tex
paper/sections/sec_bt1092_1093_explicit_quotient_cube.tex
paper/sections/sec_bt1095_1096_A12_K_matrix.tex
```

## Expected holonet sections

```text
paper/sections/sec_bt1083_1085_holonet_bridge.tex
paper/sections/sec_bt1086_1088_holonet_reservoir_runtime.tex
paper/sections/sec_bt1089_1090_holonet_core_intertwiner.tex
paper/sections/sec_bt1092_1093_holonet_quotient_cube.tex
paper/sections/sec_bt1095_1096_holonet_A12_K_matrix.tex
```

## Boundary

This is not a TeX compiler.  It is a no-network structural check designed to catch missing paths, missing markers, duplicate labels, and obvious brace hazards before the full TeX workflow runs.
