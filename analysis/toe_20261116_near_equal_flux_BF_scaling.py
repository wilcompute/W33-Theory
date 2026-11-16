"""Exact asymptotics and high-precision control for nearly equal M fluxes.

The committed M uplift gives m_low^2 L^2=4-sqrt(64+320(eta-1/2)^2)
and (N1/N2)^2=eta(2-eta)^2/((1-eta)(1+eta)^2).
This script probes the BF violation for integer fluxes (N+1,N)
without unstable floating-point subtraction. It does not add
the higher-derivative M-theory corrections.
"""
from decimal import Decimal,localcontext
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_near_equal_flux_BF_scaling.json"

def ratio_squared(eta):
    return eta*(2-eta)**2/((1-eta)*(1+eta)**2)

def case(N, precision=65):
    if N<1:raise ValueError("N>=1")
    with localcontext() as ctx:
        ctx.prec=precision
        D=Decimal
        r=D(N+1)/D(N)
        target=r*r
        lo,hi=D("0.5"),D("0.999999999999999999999999999999")
        for _ in range(270):
            mid=(lo+hi)/2
            if ratio_squared(mid)<target:lo=mid
            else:hi=mid
        eta=(lo+hi)/2
        dd=eta-D("0.5")
        rad=(D(64)+D(320)*dd*dd).sqrt()
        gap=D(320)*dd*dd/(rad+D(8))
        mass=D(-4)-gap
        # eleven-dimensional large-radius family with horizontal N0=N
        # L^3/lp^3=(pi/8)*N*(4(1+eta))*(4(2-eta)).
        k1=D(4)*(1+eta);k2=D(4)*(2-eta)
        import math
        pi=D("3.14159265358979323846264338327950288419716939937510582097494459")
        L3=pi/D(8)*N*k1*k2
        corr6=1/(L3*L3) # (lp/L)^6; scaling proxy only
        return {
          "N2":N,"N1":N+1,"N0":N,
          "eta":str(+eta),
          "m_low2L2":str(+mass),
          "BF_gap_below_minus4":str(+gap),
          "N_squared_times_BF_gap":str(+(gap*N*N)),
          "L_cubed_in_Planck_units":str(+L3),
          "lp_over_L_to_sixth":str(+corr6),
          "BF_gap_over_lp_L_sixth":str(+(gap/corr6)),
        }

def verify():
    cases=[case(N) for N in (10,100,1000,10000,100000)]
    scaled=[float(v["N_squared_times_BF_gap"]) for v in cases]
    assert scaled[-1]>44.99 and scaled[-1]<45
    assert all(scaled[i]<scaled[i+1] for i in range(len(scaled)-1))
    assert all(Decimal(v["BF_gap_below_minus4"])>0 for v in cases)
    # exact Taylor logic: R'(1/2)=2/3; gap~20 delta^2;
    # R=1+1/N implies delta~3/(2N), hence 45/N^2.
    return {
      "status":"PASS_NEAR_EQUAL_FLUX_BF_GAP_AND_ORDER_OF_LIMITS",
      "input_charge_ratios":"N1=N+1, N2=N, N0=N",
      "exact_derivative_ratio_at_eta_half":"2/3",
      "exact_limit_N_squared_times_gap":"45",
      "higher_derivative_caveat":"(lp/L)^6 is O(N^-2) on this family, the same parametric order as the BF gap; coefficients/signs of R^4 and induced terms are not calculated.",
      "cases":cases
    }
if __name__=="__main__":
    data=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(data["status"],[(x["N2"],x["N_squared_times_BF_gap"]) for x in data["cases"]])
