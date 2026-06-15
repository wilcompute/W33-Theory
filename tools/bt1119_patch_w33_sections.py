#!/usr/bin/env python3
from pathlib import Path

ROWS = [
"\\input{sections/sec_bt1083_1085_matter_bridge}\n",
"\\input{sections/sec_bt1086_1088_core_reservoir}\n",
"\\input{sections/sec_bt1089_1090_natural_core_intertwiner}\n",
"\\input{sections/sec_bt1092_1093_explicit_quotient_cube}\n",
"\\input{sections/sec_bt1095_1096_A12_K_matrix}\n",
"\\input{sections/sec_bt1098_1100_realform_spectrum_ci}\n",
"\\input{sections/sec_bt1101_1102_whitening_structure}\n",
"\\input{sections/sec_bt1104_1106_projector_coupling_report}\n",
"\\input{sections/sec_bt1107_1109_coupling_generation_report}\n",
"\\input{sections/sec_bt1110_1112_weight_closure_report}\n",
"\\input{sections/sec_bt1113_1116_weight_coupling_factorization}\n",
"\\input{sections/sec_bt1117_1119_k3_yukawa_patch_report}\n"
]

p = Path("paper/w33_preprint.tex")
s = p.read_text()
block = "".join(r for r in ROWS if r.strip() not in s)
marker = "\\section{The TOE Singularity Theorem}"
if block and marker in s:
    p.write_text(s.replace(marker, block + marker, 1))
