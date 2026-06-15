#!/usr/bin/env python3
from pathlib import Path

W33 = [
"\\input{sections/sec_bt1083_1085_matter_bridge}\n",
"\\input{sections/sec_bt1086_1088_core_reservoir}\n",
"\\input{sections/sec_bt1089_1090_natural_core_intertwiner}\n",
"\\input{sections/sec_bt1092_1093_explicit_quotient_cube}\n",
"\\input{sections/sec_bt1095_1096_A12_K_matrix}\n"
]
HOL = [
"\\input{paper/sections/sec_bt1083_1085_holonet_bridge}\n",
"\\input{paper/sections/sec_bt1086_1088_holonet_reservoir_runtime}\n",
"\\input{paper/sections/sec_bt1089_1090_holonet_core_intertwiner}\n",
"\\input{paper/sections/sec_bt1092_1093_holonet_quotient_cube}\n",
"\\input{paper/sections/sec_bt1095_1096_holonet_A12_K_matrix}\n"
]

def add(path, marker, rows):
    p = Path(path); s = p.read_text()
    block = "".join(r for r in rows if r.strip() not in s)
    if block and marker in s: p.write_text(s.replace(marker, block + marker, 1))

if __name__ == "__main__":
    add("paper/w33_preprint.tex", "\\section{The TOE Singularity Theorem}", W33)
    add("photonic_holonet.tex", "\\subsection{The ethos}", HOL)
