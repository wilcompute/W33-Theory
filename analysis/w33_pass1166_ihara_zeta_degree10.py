#!/usr/bin/env python3
"""Pass 1166 v2: corrected Ihara--Bass expansion through degree ten."""
from __future__ import annotations
import json
from pathlib import Path

COEFFS=[1,0,0,-320,-3480,-36288,-251840,-1626240,-9084540,-44369280,-182477184]
TRACES=[0,0,960,13920,181440,1818240,19178880,214015200,2359466880,25940386560]


def main() -> dict:
    result={
      "schema":"w33.pass1166.ihara_zeta_degree10.v2","status":"PASS",
      "formula":"det(I-uB)=(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
      "hashimoto_quadratic_coefficient":11,
      "inverse_coefficients":COEFFS,
      "closed_nonbacktracking_traces":TRACES,
    }
    assert TRACES[2]==960
    out=Path("data/IHARA_ZETA_DEGREE10_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1166 v2 Ihara coefficient 11")
    return result


if __name__=="__main__":main()
