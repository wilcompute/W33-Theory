"""New first-order near-equal torus-momentum asymptotic under exchange symmetry.

The actual unequal-flux constrained KK operator has NOT been built here.
At fixed mean mixed flux, sphere exchange eta <-> 1-eta forces any
isolated eigenbranch to be even in anisotropy delta=eta-1/2.
Thus the first-order term is entirely the quantized TORUS AREA shift.
This is conditional on no unexpected degeneracy/constraint bifurcation.
"""
import math,json,importlib.util
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_nearequal_KK_firstorder_exchange.json"
spec=importlib.util.spec_from_file_location("priornear",ROOT/"analysis"/"toe_20261116_near_equal_flux_BF_scaling.py")
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

LAMBDA0=3*math.pi
MASS0=LAMBDA0-2-math.sqrt(4+16*LAMBDA0)
DM_DLAMBDA=1-8/math.sqrt(4+16*LAMBDA0)
PREDICTION_COEFFICIENT=-LAMBDA0*DM_DLAMBDA/2

def near(N):
    if N<2:raise ValueError("N>=2")
    row=prior.case(N)
    eta=float(Decimal(row["eta"]))
    k2=4*(2-eta)
    area=16*math.pi*(N+1)/(N*k2*math.sqrt(8*eta))
    lam=4*math.pi**2/area
    proxy=lam-2-math.sqrt(4+16*lam)
    return {"N":N,"eta":eta,"relative_mixed_flux_detuning":1/N,
      "torus_area_over_AdS_L2":area,
      "lambda_from_exact_period_geometry":lam,
      "N_times_lambda_minus_lambda0":N*(lam-LAMBDA0),
      "equal_flux_formula_at_unequal_geometry_PROXY_NOT_EIGENMASS":proxy,
      "N_times_proxy_mass_minus_mass0":N*(proxy-MASS0),
      "warning":"At nonzero unequal flux the complete metric-C3 KK matrix is needed for an exact mass. The proxy differs from true mass at order delta^2 only IF the full isolated physical eigenbranch is analytic and exchange-even."}

def verify():
    rows=[near(N) for N in (10,100,1000,10000,100000)]
    assert abs(rows[-1]["N_times_lambda_minus_lambda0"]+LAMBDA0/2)<.0005
    assert abs(rows[-1]["N_times_proxy_mass_minus_mass0"]-PREDICTION_COEFFICIENT)<.0005
    assert all(z["lambda_from_exact_period_geometry"]<LAMBDA0 for z in rows)
    assert all(z["equal_flux_formula_at_unequal_geometry_PROXY_NOT_EIGENMASS"]<MASS0 for z in rows)
    return {"status":"PASS_EXCHANGE_SYMMETRY_NEAREQUAL_KK_FIRSTORDER_GEOMETRY",
      "zero_flux_ratio_mass":MASS0,
      "geometry_expansion":"lambda(N)=3*pi*(1-1/(2N))+O(1/N^2)",
      "conditional_true_physical_eigenmass_expansion":"m^2 L^2=m_equal^2 L^2-(3*pi/(2N))*(1-8/sqrt(4+48*pi))+O(1/N^2)",
      "coefficient_of_1_over_N":PREDICTION_COEFFICIENT,
      "proof_outline":"At fixed mean mixed flux, interchange of the two spheres sends eta-1/2 to its negative. An isolated scalar-Maxwell eigenbranch in a smooth constrained physical operator has no linear anisotropy term. Mean flux changes by 1/(2N), shifting the torus Laplacian linearly.",
      "assumptions":"Requires exact 11D spherical exchange covariance, no eigenvalue crossing at the selected mode, smooth gauge fixing and kinetic inner product. Unequal-flux KK operator and O(N^-2) term remain uncomputed.",
      "rows":rows}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"],x["coefficient_of_1_over_N"])
