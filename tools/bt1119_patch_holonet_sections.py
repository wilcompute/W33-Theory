#!/usr/bin/env python3
from pathlib import Path

ROWS = [
"\\input{paper/sections/sec_bt1083_1085_holonet_bridge}\n",
"\\input{paper/sections/sec_bt1086_1088_holonet_reservoir_runtime}\n",
"\\input{paper/sections/sec_bt1089_1090_holonet_core_intertwiner}\n",
"\\input{paper/sections/sec_bt1092_1093_holonet_quotient_cube}\n",
"\\input{paper/sections/sec_bt1095_1096_holonet_A12_K_matrix}\n",
"\\input{paper/sections/sec_bt1098_1100_holonet_realform_spectrum_ci}\n",
"\\input{paper/sections/sec_bt1101_1102_holonet_whitening_structure}\n",
"\\input{paper/sections/sec_bt1104_1106_holonet_projector_coupling_report}\n",
"\\input{paper/sections/sec_bt1107_1109_holonet_coupling_generation_report}\n",
"\\input{paper/sections/sec_bt1110_1112_holonet_weight_closure_report}\n",
"\\input{paper/sections/sec_bt1113_1116_holonet_weight_coupling_factorization}\n",
"\\input{paper/sections/sec_bt1117_1119_holonet_k3_yukawa_patch_report}\n"
]

p = Path("photonic_holonet.tex")
s = p.read_text()
block = "".join(r for r in ROWS if r.strip() not in s)
marker = "\\subsection{The ethos}"
if block and marker in s:
    p.write_text(s.replace(marker, block + marker, 1))
