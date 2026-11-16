"""Robust equal-flux torus BF obstruction and conditional near-equal persistence.

Important: near-equal proxy masses are NOT computed unequal-flux eigenmasses.
The persistence claim uses continuity of the full constrained physical KK
operator; it is not a certified numerical N threshold.
"""
import importlib.util, json, math
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_robust_torus_BF_nearequal.json"
spec=importlib.util.spec_from_file_location("near",ROOT/"analysis"/"toe_20261116_near_equal_flux_BF_scaling.py")
near=importlib.util.module_from_spec(spec);spec.loader.exec_module(near)

def lower(lam):
    return lam-2-math.sqrt(4+16*lam)

def equal_exact(N):
    if N<1:raise ValueError("positive integer")
    lam=3*math.pi
    gap=-4-lower(lam)
    L3=(9*math.pi/2)*N
    return {"N0":N,"N1":N,"N2":N,"lambda1":lam,
            "physical_odd_scalar_mass2_L2":lower(lam),
            "BF_violation":gap,
            "L3_over_lp3":L3,
            "hypothetical_Ccrit_for_shift_C_lp_over_L_to_sixth":gap*L3*L3,
            "sphere_radius_over_lp":L3**(1/3)/math.sqrt(6),
            "torus_cycle_radius_over_lp":L3**(1/3)/math.sqrt(lam)}

def unequal_geometry(N):
    """Exact input fluxes + computed quantization geometry; equal mass only proxy."""
    if N<2:raise ValueError("N>=2")
    r=near.case(N)
    eta=float(Decimal(r["eta"]))
    k1,k2=4*(1+eta),4*(2-eta)
    L3=float(Decimal(r["L_cubed_in_Planck_units"]))
    # From M flux periods: A_T2/L²=16*pi*N1/(N0*k2*sqrt(8 eta)).
    N1,N0=N+1,N
    areaL2=16*math.pi*N1/(N0*k2*math.sqrt(8*eta))
    lam=4*math.pi**2/areaL2
    return {
        "N":N,"eta":eta,"sphere_curvatures":[k1,k2],
        "T2_area_over_L2":areaL2,"square_torus_first_lambda":lam,
        "equal_flux_formula_evaluated_at_lambda_PROXY_ONLY":lower(lam),
        "NOT_A_PHYSICAL_UNEQUAL_FLUX_EIGENMASS":True,
        "L_over_lp":L3**(1/3),
        "sphere_radii_over_lp":[L3**(1/3)/math.sqrt(k) for k in (k1,k2)],
        "torus_cycle_radius_over_lp":L3**(1/3)/math.sqrt(lam),
        "homogeneous_BF_gap":float(Decimal(r["BF_gap_below_minus4"]))
    }

def verify():
    rows=[equal_exact(N) for N in (1,10,100,1000,10000)]
    geom=[unequal_geometry(N) for N in (10,100,1000,10000)]
    target=math.sqrt(4+48*math.pi)-(3*math.pi+2)
    assert abs(rows[0]["BF_violation"]-target)<1e-12
    assert 1.0<target<1.1
    assert all(abs(z["BF_violation"]-target)<1e-12 for z in rows)
    assert all(abs(z["hypothetical_Ccrit_for_shift_C_lp_over_L_to_sixth"]/
                   (z["N0"]**2)-target*(9*math.pi/2)**2)<1e-9 for z in rows)
    assert all(a["square_torus_first_lambda"]<b["square_torus_first_lambda"]
               for a,b in zip(geom,geom[1:]))
    assert abs(geom[-1]["square_torus_first_lambda"]-3*math.pi)<.001
    assert all(z["L_over_lp"]>1 and min(z["sphere_radii_over_lp"])>1 for z in geom)
    return {
        "status":"PASS_EQUAL_FLUX_KK_BF_ORDER_ONE_AND_NEAR_EQUAL_GEOMETRIC_LIMIT",
        "equal_flux_mode":"Physical sphere-exchange odd scalar-transverse-Maxwell mode, L=1",
        "equal_flux_mass2_L2":lower(3*math.pi),
        "equal_flux_BF_gap":target,
        "equal_flux_critical_C_at_N":"Ccrit(N) = (sqrt(4+48*pi)-3*pi-2)*(9*pi*N/2)^2",
        "equal_flux_sample":rows,"near_equal_geometry":geom,
        "continuity_statement":"For a smooth family of physical gauge-fixed fluctuation operators, an isolated negative-BF mode with order-one margin at eta=1/2 remains below BF for all eta sufficiently near 1/2. This implies sufficiently large N in (N+1,N,N); no explicit N threshold is certified.",
        "eight_derivative_scope":"A bounded flux-independent coefficient C multiplying (lp/L)^6 cannot remove the equal-flux gap as N grows. Full 8-derivative coefficient, eigenmode mixing and corrected backgrounds have NOT been calculated.",
        "warning":"The near-equal lower-mass proxy is evaluated with the equal-flux closed-form dispersion and is NOT a solution of the unequal-flux coupled spectrum."
    }

if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["equal_flux_BF_gap"])
