#!/usr/bin/env python3
from pathlib import Path
import argparse

ROWS = [
"\\input{paper/sections/sec_bt1083_1085_matter_bridge}\n",
"\\input{paper/sections/sec_bt1086_1088_core_reservoir}\n",
"\\input{paper/sections/sec_bt1089_1090_natural_core_intertwiner}\n",
"\\input{paper/sections/sec_bt1092_1093_explicit_quotient_cube}\n",
"\\input{paper/sections/sec_bt1095_1096_A12_K_matrix}\n",
"\\input{paper/sections/sec_bt1098_1100_realform_spectrum_ci}\n",
"\\input{paper/sections/sec_bt1101_1102_whitening_structure}\n",
"\\input{paper/sections/sec_bt1104_1106_projector_coupling_report}\n",
"\\input{paper/sections/sec_bt1107_1109_coupling_generation_report}\n",
"\\input{paper/sections/sec_bt1110_1112_weight_closure_report}\n",
"\\input{paper/sections/sec_bt1113_1116_weight_coupling_factorization}\n",
"\\input{paper/sections/sec_bt1117_1119_k3_yukawa_patch_report}\n",
"\\input{paper/sections/sec_bt1120_1122_k3_yukawa_build_path}\n"
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    p = Path("w33_paper.tex")
    s = p.read_text()
    block = "".join(r for r in ROWS if r.strip() not in s)
    marker = "\\end{document}"
    print(f"target={p}")
    print(f"planned_inserts={sum(1 for r in ROWS if r.strip() not in s)}")
    if not block:
        return
    if marker not in s:
        raise SystemExit("marker not found: \\end{document}")
    if args.dry_run:
        print(block)
        return
    p.write_text(s.replace(marker, block + marker, 1))


if __name__ == "__main__":
    main()
