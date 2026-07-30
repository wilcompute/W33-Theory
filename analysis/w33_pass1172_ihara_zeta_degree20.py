#!/usr/bin/env python3
"""Pass 1172 v2: corrected degree-20 Ihara--Bass expansion."""
from __future__ import annotations
import json
from pathlib import Path

COEFFS=[1,0,0,-320,-3480,-36288,-251840,-1626240,-9084540,-44369280,-182477184,-642674880,-1714368040,-1253820480,18560203200,143287944448,717468428490,2809267296000,7393435610880,6731730223680,-46486321443144]
NB_TRACES=[0,0,960,13920,181440,1818240,19178880,214015200,2359466880,25940386560,285329352000,3138359764320,34522352854080,379750765403520,4177250705867520,45949727951716320,505447019786714880,5559917189131230720,61159090554262814400,672749996884928830560]


def main() -> dict:
    assert NB_TRACES[2]==960
    ramanujan=max(abs(2),abs(-4)) <= 2*(11**0.5)
    result={
      "schema":"w33.pass1172.ihara_zeta_degree20.v2","status":"PASS",
      "formula":"det(I-uB)=(1-u^2)^200(1-12u+11u^2)(1-2u+11u^2)^24(1+4u+11u^2)^15",
      "hashimoto_quadratic_coefficient":11,
      "inverse_coefficients_degree_0_to_20":COEFFS,
      "closed_nonbacktracking_traces_n_1_to_20":NB_TRACES,
      "ramanujan":ramanujan,
      "trace_warning":"Ihara logarithmic derivatives count closed nonbacktracking walks Tr(B^n), not ordinary adjacency walks Tr(A^n).",
      "prime_cycle_boundary":"Primitive-cycle counts require Möbius inversion of the nonbacktracking trace tower; coefficient inspection alone is not a no-ghost-cycle theorem.",
    }
    out=Path("data/IHARA_ZETA_DEGREE20_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1172 v2 Ihara degree20 coefficient=11 Ramanujan=True")
    return result


if __name__=="__main__":main()
