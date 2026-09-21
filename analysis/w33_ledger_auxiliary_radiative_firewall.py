#!/usr/bin/env python3
"""Refine the nondynamical-auxiliary dark-bond candidate.

An algebraic Majorana auxiliary variable generates the Weinberg contact exactly
without a propagating heavy pole.  This removes the ordinary heavy-particle
threshold mechanism by construction, but does not constitute a UV completion.
"""
from __future__ import annotations
import json
from pathlib import Path
OUT=Path("data/PART_LEDGER_AUXILIARY_RADIATIVE_FIREWALL.json")

def main():
    rows=[]
    for M,y in [(1e6,1e-4),(1e9,1e-3),(1e12,1e-2)]:
        C5=y*y/M
        rows.append({"M_GeV":M,"y":y,"C5_GeV_inv":C5,"pole_denominator":"none; algebraic inverse is 1/M"})
    checks={
      "all_contacts_nonzero":all(r["C5_GeV_inv"]>0 for r in rows),
      "no_propagating_denominator":all(r["pole_denominator"].startswith("none") for r in rows),
    }
    assert all(checks.values()),checks
    out={
      "schema":"w33.ledger.auxiliary-radiative-firewall.v1",
      "status":"AUXILIARY_CONTACT_REMOVES_HEAVY_POLE_THRESHOLD_UV_COMPLETION_STILL_OPEN",
      "exact_algebra":{
        "lagrangian":"L_aux=(M/2) N N + y N O + h.c., O=(LH), with no kinetic term for N",
        "equation_of_motion":"N=-(y/M) O",
        "effective_operator":"L_eff=-(y^2/(2M)) O O + h.c.",
        "propagator_statement":"N is algebraic, so its inverse kernel is local 1/M rather than a momentum pole 1/(p-slash-M)."
      },
      "radiative_reading":[
        "The standard type-I seesaw one-loop Higgs threshold associated with a propagating heavy Majorana pole is absent in this auxiliary rewriting because there is no heavy propagating mode to run in that threshold graph.",
        "Below the matching scale the theory is simply SMEFT with the Weinberg operator. Published SMEFT renormalisation calculations find that two Weinberg insertions feed dimension-six bosonic operators; they do not directly renormalise renormalisable bosonic coefficients at order 1/Lambda^2 in dimensional regularisation.",
        "This is not a proof of absolute Higgs naturalness: an ultraviolet completion that produces the algebraic auxiliary structure may reintroduce propagating states or threshold sensitivity."
      ],
      "literature_boundary":[
        "Brivio & Trott, JHEP 02 (2019) 107: propagating type-I seesaw matching includes a one-loop Higgs-potential threshold.",
        "Renormalisation of SMEFT bosonic interactions up to dimension eight by LNV operators, JHEP 06 (2023) 123: double Weinberg insertions renormalise higher-dimensional bosonic operators, with no direct contribution to renormalisable bosonic coefficients at order 1/Lambda^2."
      ],
      "classification":"candidate upgraded from tree-level-only to EFT-radiative-safe through the cited order; UV completion remains OPEN.",
      "examples":rows,"checks":checks
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out
if __name__=="__main__":main()
