#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "paper/sections/sec_bt1083_1085_matter_bridge.tex",
    "paper/sections/sec_bt1086_1088_core_reservoir.tex",
    "paper/sections/sec_bt1089_1090_natural_core_intertwiner.tex",
    "paper/sections/sec_bt1092_1093_explicit_quotient_cube.tex",
    "paper/sections/sec_bt1095_1096_A12_K_matrix.tex",
    "paper/sections/sec_bt1098_1100_realform_spectrum_ci.tex",
    "paper/sections/sec_bt1101_1102_whitening_structure.tex",
    "paper/sections/sec_bt1104_1106_projector_coupling_report.tex",
    "paper/sections/sec_bt1107_1109_coupling_generation_report.tex",
    "paper/sections/sec_bt1113_1116_weight_coupling_factorization.tex",
    "paper/sections/sec_bt1083_1085_holonet_bridge.tex",
    "paper/sections/sec_bt1086_1088_holonet_reservoir_runtime.tex",
    "paper/sections/sec_bt1089_1090_holonet_core_intertwiner.tex",
    "paper/sections/sec_bt1092_1093_holonet_quotient_cube.tex",
    "paper/sections/sec_bt1095_1096_holonet_A12_K_matrix.tex",
    "paper/sections/sec_bt1098_1100_holonet_realform_spectrum_ci.tex",
    "paper/sections/sec_bt1101_1102_holonet_whitening_structure.tex",
    "paper/sections/sec_bt1104_1106_holonet_projector_coupling_report.tex",
    "paper/sections/sec_bt1107_1109_holonet_coupling_generation_report.tex",
    "paper/sections/sec_bt1113_1116_holonet_weight_coupling_factorization.tex",
]

def main():
    missing = [p for p in FILES if not (ROOT / p).exists()]
    report = {
        "name": "BT1116 section report",
        "passed": not missing,
        "count": len(FILES),
        "missing": missing,
        "note": "path existence report only"
    }
    out = ROOT / "data" / "bt1106_section_report.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not missing else 1

if __name__ == "__main__":
    raise SystemExit(main())
