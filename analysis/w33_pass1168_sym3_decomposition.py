#!/usr/bin/env python3
"""Pass 1168 v2: honest dimension census for Sym^3(1+24+15)."""
from __future__ import annotations
import json
from math import comb
from pathlib import Path


def main() -> dict:
    terms={
      "Sym3(1)":1,"Sym3(24)":comb(26,3),"Sym3(15)":comb(17,3),
      "Sym2(1)x24":24,"Sym2(1)x15":15,"Sym2(24)x1":comb(25,2),
      "Sym2(15)x1":comb(16,2),"Sym2(24)x15":comb(25,2)*15,
      "Sym2(15)x24":comb(16,2)*24,"1x24x15":24*15,
    }
    assert sum(terms.values())==comb(42,3)==11480
    result={
      "schema":"w33.pass1168.sym3_dimension_census.v2","status":"PASS",
      "terms":terms,"total_dimension":sum(terms.values()),
      "scope_barrier":"The 2240 A2-root-triple carrier is not Sym^3(C^40). Its 45-dimensional cubic image is exactly 1+20+24 by Pass 1135. Equality 45=dim so(10) is only a count coincidence until an explicit D5-equivariant isomorphism is constructed.",
      "rejected_claim":"Dimension equality alone does not identify the image with the SO(10) adjoint.",
    }
    out=Path("data/SYM3_DECOMPOSITION_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1168 v2 Sym3 dimension census only")
    return result


if __name__=="__main__":main()
