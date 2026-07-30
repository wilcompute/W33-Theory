#!/usr/bin/env python3
"""Pass 1170 v2: exact decomposition first; modular validation second."""
from __future__ import annotations
import json
from pathlib import Path

EXACT_KERNEL={
 "1":(1,13),"6":(6,16),"15":(15,5),"15a":(15,4),"20":(20,21),
 "24":(24,2),"30":(30,9),"60a":(60,4),"64":(64,10),"81_minus":(81,3),"90":(90,1),
}


def main() -> dict:
    dimension=sum(d*m for d,m in EXACT_KERNEL.values())
    assert dimension==2195
    result={
      "schema":"w33.pass1170.meataxe_validation_plan.v2","status":"PASS",
      "kernel_dimension":dimension,
      "exact_characteristic_zero_decomposition":{k:{"degree":d,"multiplicity":m} for k,(d,m) in EXACT_KERNEL.items()},
      "source":"Pass 1135 exact class-algebra character inner products",
      "modular_validation":{
        "prime":7,"semisimple":True,
        "reason":"7 does not divide 51840, so Maschke guarantees semisimplicity.",
        "field_warning":"Maschke does not guarantee that every complex irreducible remains absolutely irreducible over GF(7); splitting fields and modular character matching must still be checked.",
        "purpose":"Validate explicit generator matrices against the already-known characteristic-zero multiplicities, not discover an unknown dimension decomposition.",
      },
      "image_module":"1+20+24",
      "scope_barrier":"The 45-dimensional image is not identified with the SO(10) adjoint without an explicit D5 action and equivariant map.",
    }
    out=Path("data/MEATAXE_KERNEL_PLAN_2026_07_27.json");out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1170 v2 exact kernel decomposition precedes MeatAxe")
    return result


if __name__=="__main__":main()
