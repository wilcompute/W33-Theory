"""Near-equal flux: robust NONHOMOGENEOUS BF obstruction vs vanishing radion gap.

For integer flux family (N1,N2,N0)=(N+1,N,N),
the homogeneous radion gap is 45/N² + O(N^-3) and could in
principle compete with an O(lp^6) mass correction of O(N^-2).
But square-torus KK mode at the EQUAL-flux limit has
lambda=3*pi and m_-² L²=3*pi-2-sqrt(4+48*pi) ~= -5.01694,
with an O(1) BF deficit. For any regular, self-adjoint
physical KK family smoothly tending to that limit, an
eigenvalue stays below -4 for sufficiently large N. This
continuity argument is independent of the uncomputed detailed
first-order eigenvector mixing; a calculable finite-N bound
requires an operator-norm bound ||H_N-H_infty||.

Even with a hypothetical uniformly bounded eight-derivative
dimensionless correction C*(lp/L)^6, it cannot cure the
nonhomogeneous O(1) gap as N->infinity, while it could
alter the O(N^-2) homogeneous radion sign. We compute both
quantitative thresholds, keeping the proxy distinct from
the physical KK eigenvalue.
"""
import sys,math,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_near_equal_flux_BF_scaling import case as near
OUT=ROOT/"data"/"toe_20261116_flux_8derivative_KK_persistence.json"

def f(lam):
    return lam-2-math.sqrt(4+16*lam)

PI=math.pi
LAMBDA_EQUAL=3*PI
M_EQUAL=f(LAMBDA_EQUAL)
GAP_EQUAL=-4-M_EQUAL
UNIFORM_GAP=math.sqrt(4+32*PI*math.sqrt(3))-2*PI*math.sqrt(3)-2
assert GAP_EQUAL>1.0 and 0<UNIFORM_GAP<GAP_EQUAL

def case(N):
    v=near(N)
    eta=float(Decimal(v["eta"]))
    k1=4*(1+eta);k2=4*(2-eta)
    # The square-torus first eigenmode lam=4*pi^2 / (area/L^2).
    # Quantization area/L^2=16*pi*(N+1)/[N*k2*sqrt(8eta)].
    area=16*PI*(N+1)/(N*k2*math.sqrt(8*eta))
    lam=4*PI*PI/area
    L3=float(Decimal(v["L_cubed_in_Planck_units"]))
    epsilon=L3**-2
    proxy_m=f(lam)
    proxy_gap=-4-proxy_m
    hom_gap=float(Decimal(v["BF_gap_below_minus4"]))
    return {"N":N,"eta":eta,"lambda_first":lam,
        "equal_operator_at_deformed_geometry_proxy_m2L2":proxy_m,
        "equal_operator_proxy_gap":proxy_gap,
        "exact_homogeneous_BF_gap":hom_gap,
        "eight_derivative_expansion_epsilon":epsilon,
        "minimum_C_to_lift_homogeneous_by_C_epsilon":hom_gap/epsilon,
        "minimum_C_to_lift_PROXY_KK_by_C_epsilon":proxy_gap/epsilon,
        "physical_KK_gap_is_NOT_computed":True}

def verify():
    rows=[case(N) for N in (10,100,1000,10000)]
    for row in rows:
        assert row["lambda_first"]<12
        assert row["equal_operator_proxy_gap"]>.9
        assert row["exact_homogeneous_BF_gap"]>0
    assert abs(rows[-1]["equal_operator_proxy_gap"]-GAP_EQUAL)<.001
    assert abs(rows[-1]["minimum_C_to_lift_homogeneous_by_C_epsilon"] - (3645*PI*PI/4))<50
    asymC=GAP_EQUAL*(9*PI/2)**2
    assert asymC>200
    return {"status":"PASS_NEAREQUAL_HOMOGENEOUS_VS_TORUS_BF_NONUNIFORM_LIMITS",
        "equal_flux_first_square_mode":{"lambda":LAMBDA_EQUAL,
          "mass_m2L2":M_EQUAL,"BF_gap":GAP_EQUAL},
        "equal_flux_all_torus_shapes_minimum_BF_gap":UNIFORM_GAP,
        "controlled_eight_derivative_thresholds":{
         "homogeneous_required_coefficient_as_N_to_inf":"(3645*pi^2)/4 = approx 8993.677, dimensionless coefficient in +C*(lp/L)^6 convention",
         "square_KK_PROXY_required_coefficient":"C/N^2 > (9*pi/2)^2 * gap = approx "+str(asymC),
         "actual_C_required_for_KK_gap":"Not computable without complete 11D fluctuation operator and higher derivative action.",
         "bounded_N_independent_C_cannot_remove_O1_KK_gap":"True IF physical unequal-flux mode converges smoothly to the equal-flux KK mode and the EFT correction remains uniformly O(C/N^2)."},
        "spectral_continuity_theorem":"For canonical self-adjoint gauge-constrained physical matrices H_N with ||H_N-H_equal|| ->0, Weyl's inequality gives an eigenvalue <=m_equal+||H_N-H_equal||. As soon as operator difference <gap_equal, it lies below -4.",
        "limitations":"A physical operator-norm K/N bound, full E6-metric/C3 KK matrix, flux-dependent R4 coefficients and corrected compactification have not been computed.",
        "finite_N_geometry_and_proxy":rows}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"],GAP_EQUAL,rows[-1]["equal_operator_proxy_gap"] if (rows:=r["finite_N_geometry_and_proxy"]) else "")
