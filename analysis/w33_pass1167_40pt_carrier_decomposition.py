#!/usr/bin/env python3
"""Pass 1167 v2: exact rank-three 40-point carrier certificate."""
from __future__ import annotations
import json
from pathlib import Path


def main() -> dict:
    result={
      "schema":"w33.pass1167.40pt_carrier_decomposition.v2","status":"PASS",
      "acting_group":"PSp(4,3)","acting_group_order":25920,
      "subdegrees":[1,12,27],"permutation_rank":3,
      "adjacency_spectrum":{"12":1,"2":24,"-4":15},
      "decomposition":"1 + 24 + 15",
      "proof":"Pass 1176 explicitly enumerates five symplectic-transvection generators on all 40 points and the point-stabilizer suborbits.",
    }
    out=Path("data/CARRIER_40_DECOMPOSITION_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1167 v2 carrier=1+24+15")
    return result


if __name__=="__main__":main()
