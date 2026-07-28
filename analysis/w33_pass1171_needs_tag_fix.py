#!/usr/bin/env python3
"""Pass 1171 v2: corrected residual-module metadata."""
from __future__ import annotations
import json
from pathlib import Path

ERRATUM={
 "id":"ERR-1158-RESIDUAL","date":"2026-07-27",
 "file":"PASS1158_1162_BREAKTHROUGH_RELEASE.md",
 "object_type":"W(E6)-module, not orbit",
 "corrected_claim":"The exact 1952-dimensional W(E6)-submodule is obtained from the Pass-1135 kernel decomposition after removing the multiplicity-three 81_minus isotypic block.",
 "tags_now_present":{
   "acting_group":"W(E6), order 51840",
   "stabilizer_label_or_order":"not applicable: this object is a module, not a transitive G-set",
   "color_retained_or_forgotten":"uncolored; a C3-colored carrier must be named separately",
 },
 "exact_decomposition_source":"analysis/w33_pass1135_cubic_kernel_decomposition.py",
 "commutant_dimension":1109,
}


def main() -> dict:
    required=["acting_group","stabilizer_label_or_order","color_retained_or_forgotten"]
    assert all(k in ERRATUM["tags_now_present"] for k in required)
    out=Path("data/ERRATUM_PASS1158_RESIDUAL_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(ERRATUM,indent=2)+"\n")
    result={"schema":"w33.pass1171.needs_tag_fix.v2","status":"PASS","all_tags_present":True,"erratum":ERRATUM}
    print("PASS 1171 v2 residual typed as module, not orbit")
    return result


if __name__=="__main__":main()
