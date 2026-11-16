"""Order-by-order BF stability and spinor deck-charge controls for the D9 M/IIB family.

Source: repository 2026-11-16 M uplift, near-equal-flux verifier,
and IIB conifold dual.  This program does NOT compute 11D eight-derivative
coefficients; it gives the exact coefficient they would need to overcome.
"""
from __future__ import annotations
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
import importlib.util
import json
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_R4_threshold_spinor_modes.json"
spec=importlib.util.spec_from_file_location(
    "near_equal_flux",ROOT/"analysis"/"toe_20261116_near_equal_flux_BF_scaling.py")
prior=importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)

def correction_threshold(N: int) -> dict:
    """Required coefficient C if a shift +C*(lp/L)^6 is postulated."""
    record=prior.case(N)
    with localcontext() as ctx:
        ctx.prec=55
        gap=Decimal(record["BF_gap_below_minus4"])
        L3=Decimal(record["L_cubed_in_Planck_units"])
        coeff=gap*L3*L3
        pi=Decimal("3.1415926535897932384626433832795028841971693993751058")
        asymptotic=Decimal(3645)*pi*pi/4
        return {
            "N":N,
            "homogeneous_BF_gap":str(+gap),
            "required_dimensionless_correction_coefficient_C":str(+coeff),
            "large_N_coefficient_Ccrit":str(+asymptotic),
            "ratio_to_asymptotic":str(+(coeff/asymptotic)),
            "critical_condition":"C >= exact gap*(L/lp)^6; this is only for a hypothetical +C*(lp/L)^6 mass shift"
        }

def spinor_deck_table(N:int) -> dict:
    """Mode e^(ik psi_std/2), psi_std period 4*pi, deck shift 4*pi/N."""
    if N<1:raise ValueError("N>=1")
    lifts=[("ordinary",Fraction(0))]
    if N%2==0:lifts.append(("alternate",Fraction(1,2)))
    selection=[]
    for name,shift in lifts:
        residue=[k for k in range(N) if (Fraction(k,N)+shift).denominator==1]
        allowed=[k for k in (-1,1) if (Fraction(k,N)+shift).denominator==1]
        selection.append({"spin_lift":name,"invariant_mode_residues_mod_N":residue,
                          "cover_Killing_spinor_modes_from_k_plusminus_1":allowed})
    return {"N":N,"lifts":selection,
            "surviving_cover_Killing_spinor_mode":any(x["cover_Killing_spinor_modes_from_k_plusminus_1"] for x in selection),
            "fiber_winding_homotopy_group":f"Z_{N}",
            "scope":"Deck invariance only. Does not identify an 11D fermionic KK mode with a physical (p,q)-string winding state."}

def curvature_characteristic_control() -> dict:
    """Algebraic pointwise test for constant-curvature product R_ab=K e_a wedge e_b."""
    # For a constant-curvature factor R^a_b = K e^a wedge e^b:
    # every summand in Tr R^(2n) is a closed walk a0..a2n=a0;
    # wedge product repeats the intermediate basis one-form, hence vanishes.
    # Flat torus curvature is zero. Mixed curvature blocks are absent.
    return {
        "background":"AdS5 x S2 x S2 x flat T2 with product Levi-Civita connection",
        "tr_R2_pointwise":"0",
        "tr_R4_pointwise":"0",
        "X8_of_background":"0",
        "C3_X8_action_quadratic_warning":"X8(background)=0 does not imply its variation or the full C3 X8 quadratic coupling vanishes.",
        "8_derivative_warning":"Need R4 plus G4-dependent and derivative-flux supersymmetric completion, corrected background and BF mass matrix."
    }

def verify() -> dict:
    cases=[correction_threshold(N) for N in (10,100,1000,10000,100000)]
    ratios=[float(a["ratio_to_asymptotic"]) for a in cases]
    assert ratios[-1]>0.9999 and ratios[-1]<1
    assert all(x<y for x,y in zip(ratios,ratios[1:]))
    assert abs(float(cases[-1]["large_N_coefficient_Ccrit"])-8993.67701049)<1e-6
    spins=[spinor_deck_table(N) for N in range(1,17)]
    assert [v["N"] for v in spins if v["surviving_cover_Killing_spinor_mode"]]==[1,2]
    for N in range(2,17):
        expected=({0} if N%2 else {0,N//2})
        found={v for row in spins[N-1]["lifts"] for v in row["invariant_mode_residues_mod_N"]}
        assert found==expected
    return {"status":"PASS_BF_R4_COEFFICIENT_THRESHOLD_AND_SPINOR_DECK_FILTER",
            "computed_coefficient_is_not_a_physical_R4_mass_correction":True,
            "critical_C_asymptotic_exact":"3645*pi^2/4",
            "critical_C_asymptotic_numeric":float(cases[-1]["large_N_coefficient_Ccrit"]),
            "largeN_cases":cases,"deck_modes":spins,
            "background_X8_control":curvature_characteristic_control(),
            "proven_vs_open":"Proven: classical threshold, deck selection, background curvature forms. Open: actual R4 coefficient and full M/IIB spin-winding dual spectrum."}

if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2)+"\n",encoding="utf-8")
    print(cert["status"],round(cert["critical_C_asymptotic_numeric"],6))
