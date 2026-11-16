"""Five-dimensional twisted-K AHSS on circle bundles Y(p,q)->S2 x S2.

Unlike the prior UNT WISTED K-theory Gysin calculation this studies an
OPTIONAL integral 3-form twist H=k*z, with H^3(Y,Z)=Z<z>.
It determines E_infinity and total group orders, NOT unresolved
additive extensions. The Type IIB background in the previous repo
derivation had H3=0; the nonzero twists below are counterfactual probes.
"""
from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_twisted_K_AHSS_extensions.json"
spec=importlib.util.spec_from_file_location("circle",ROOT/"analysis"/"toe_20261116_circle_bundle_ring_winding_lattice.py")
circle=importlib.util.module_from_spec(spec)
spec.loader.exec_module(circle)

def page(p:int,q:int,k:int) -> dict:
    """AHSS for complex K with H=kz. Signs of k do not change group types."""
    top=circle.circle_ring(p,q)
    g=top["gcd"]
    if k==0:
        return {"charges":[p,q],"H_twist_integer":0,"gcd":g,
                "d3_H0_to_H3":0,"d3_free_H2_to_H5":0,
                "E_infty_even":{"H0":"Z","H2":f"Z + Z_{g}","H4":f"Z_{g}"},
                "E_infty_odd":{"H3":"Z","H5":"Z"},
                "K0_exact":"Z^2" +(f" + Z_{g}^2" if g>1 else ""),
                "K1_exact":"Z^2",
                "extension_caveat":"Untwisted calculation independently resolved by K-Gysin"}
    kabs=abs(k)
    # Sq^3_Z=beta Sq^2 r2 is 2-torsion. On Y, its nonzero target
    # groups H3=Z and H5=Z are torsion-free, so it vanishes here.
    # Hence d3(1)=k*z and d3(t)=k*[Y], d3(u)=0.
    result={
        "charges":[p,q],"H_twist_integer":k,"gcd":g,
        "d3_H0_to_H3":k,"d3_free_H2_to_H5":k,
        "d3_H2_torsion_to_H5":0,
        "Sq3_integral_on_relevant_degrees":0,
        "E_infty_even":{"H0":0,"H2":f"Z_{g}","H4":f"Z_{g}"},
        "E_infty_odd":{"H3":f"Z_{kabs}","H5":f"Z_{kabs}"},
        "K0_finite_order":g*g,
        "K1_finite_order":kabs*kabs,
        "extension_caveat":"E_infty gives associated graded, not Z_g+Z_g vs Z_g^2 or Z_(g^2), similarly for k; extensions unresolved."
    }
    if g==1:
        result["K0_exact"]="0"
        result["K1_exact"]=f"Z_{kabs} + Z_{kabs}" if kabs>1 else "0"
        result["extension_caveat"]="For primitive c1, Y is diffeomorphic to S2 x S3; Kunneth with the H=k generator of H3 resolves K1=Z_k^2."
    if kabs==1:
        result["K1_exact"]="0"
    result["Freed_Witten_probe"]={
       "unit_3cycle_integral_H":k,
       "oriented_3cycle_W3":0,
       "isolated_D3_wrap_unit_3cycle_obstructed_if_no_endpoints":True,
       "scope":"In this OPTIONAL H background, an oriented 3-cycle carrying integral H cannot support a stand-alone spin D-brane without canceling data; not an assertion for H=0 IIB vacuum."
    }
    return result

def verify()->dict:
    shapes=[(1,1),(3,0),(3,3),(4,4),(6,10)]
    rows=[page(p,q,k) for p,q in shapes for k in (0,1,2,3)]
    for row in rows:
        g=row["gcd"];k=abs(row["H_twist_integer"])
        if k:
            assert row["K0_finite_order"]==g*g
            assert row["K1_finite_order"]==k*k
            assert row["d3_free_H2_to_H5"] in (-k,k)
        else:
            assert row["K0_exact"].startswith("Z^2")
    assert page(1,1,3)["K1_exact"]=="Z_3 + Z_3"
    assert page(3,3,1)["K0_finite_order"]==9
    assert page(3,3,1)["K1_exact"]=="0"
    return {
        "status":"PASS_TWISTED_K_AHSS_ASSOCIATED_GRADED_WITH_EXPLICIT_EXTENSION_BOUNDARY",
        "nonzero_twist_is_hypothetical_not_present_in_current_IIB_solution":True,
        "groups_in_zero_background_H": "Prior untwisted K_Gysin: K0=Z^2+Z_g^2, K1=Z^2",
        "d3_formula":"d3=SqZ^3+H cup, H=k*z, with integral SqZ^3 zero on relevant torsion-free targets",
        "cup_pairings":"<t cup z,[Y]>=1, u cup z=0",
        "cases":rows,
        "claim_limits":"Associated graded only for gcd>1 and twist |k|>0. No full twisted K groups or physically conserved charges until extensions, higher operations, differential refinements, Page and dynamical data are resolved."
    }

if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"],"cases",len(cert["cases"]))
