#!/usr/bin/env python3
from pathlib import Path

W33 = [
"\\input{sections/sec_bt1098_1100_realform_spectrum_ci}\n",
"\\input{sections/sec_bt1101_1102_whitening_structure}\n",
"\\input{sections/sec_bt1104_1106_projector_coupling_report}\n",
"\\input{sections/sec_bt1107_1109_coupling_generation_report}\n",
"\\input{sections/sec_bt1110_1112_weight_closure_report}\n"
]
HOL = [
"\\input{paper/sections/sec_bt1098_1100_holonet_realform_spectrum_ci}\n",
"\\input{paper/sections/sec_bt1101_1102_holonet_whitening_structure}\n",
"\\input{paper/sections/sec_bt1104_1106_holonet_projector_coupling_report}\n",
"\\input{paper/sections/sec_bt1107_1109_holonet_coupling_generation_report}\n",
"\\input{paper/sections/sec_bt1110_1112_holonet_weight_closure_report}\n"
]

def add(path, marker, rows):
    p = Path(path); s = p.read_text()
    block = "".join(r for r in rows if r.strip() not in s)
    if block and marker in s: p.write_text(s.replace(marker, block + marker, 1))

if __name__ == "__main__":
    add("paper/w33_preprint.tex", "\\section{The TOE Singularity Theorem}", W33)
    add("photonic_holonet.tex", "\\subsection{The ethos}", HOL)
