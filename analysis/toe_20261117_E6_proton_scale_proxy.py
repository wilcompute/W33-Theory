"""Gauge-mediated proton-decay scale proxy for the split E6
two-adjoint messenger benchmark, NOT a lifetime prediction.

After B background preserves SU5, the A adjoint SU5 3+2 VEV
A=r diag(2,2,2,-3,-3)/sqrt30 gives 12 X/Y vectors
mass M_X=g5*5*r/sqrt30 (canonical convention).
The messenger 27-sector masses are M+s*y*(SU5 weight)+t*u*Bq.
For benchmark M=y=u=1, Bpsi=-.2,Bchi=.2,
lightest fermion mass at A=0 is 0.2M.
At r/M=.05 and alpha5=1/25, M_X/M~.0324,
so merely having a heavy vectorlike messenger sector does not
guarantee proton-safe heavy SU5 gauge bosons.

Input proxy M_X>=1e15 GeV gives a REQUIREMENT on absolute messenger
scale, not a fit to the Super-K 2.4e34-year partial-lifetime bound:
flavor/hadronic/gauge unification, thresholds and proton operators
not derived. Standard dimension-six amplitude ~g5²/M_X².
"""
from pathlib import Path
import math,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261117_E6_two_adjoint_split_27_threshold import threshold
OUT=ROOT/"data"/"toe_20261117_E6_split_27_Xboson_proton_scale_proxy.json"
def verify():
    alpha=1/25
    g=math.sqrt(4*math.pi*alpha)
    B=threshold(-.2,.2,.25)
    assert B is not None
    vmin=min(x["min_fermion_mass_abs"] for x in B["irrep"])
    assert abs(vmin-.2)<1e-12
    rows=[]
    for r in (.015,.03,.05,.1):
        Mx_over_M=g*5*r/math.sqrt(30)
        req=1e15/Mx_over_M
        rows.append({"A_norm_over_messenger_scale":r,
           "g5":g,"X_vector_mass_over_M":Mx_over_M,
           "min_messenger_fermion_mass_over_M_at_A0":vmin,
           "ratio_Xmass_to_lightest_messenger":Mx_over_M/vmin,
           "required_messenger_scale_GeV_IF_MX_at_least_1e15":req,
           "basis_hypercharge_Xmass_ratio":"X/Y gap =5r/sqrt30; vector mass=g5*gap"})
    assert rows[2]["required_messenger_scale_GeV_IF_MX_at_least_1e15"]>3e16
    # At fixed r, exchange coefficient g5²/MX² =1/(5r/sqrt30)^2.
    for x in rows:
        r=x["A_norm_over_messenger_scale"]
        mx=x["X_vector_mass_over_M"]
        amp=g*g/(mx*mx)
        assert math.isclose(amp,30/(25*r*r),rel_tol=1e-12)
    return {"status":"PASS_SPLIT_E6_MESSENGER_X_BOSON_SCALE_PROXY",
       "illustrative_alpha5":alpha,"g5":g,"superK_e_plus_pi0_partial_lifetime_bound_years":"2.4e34 at 90% CL (published 2020; not itself converted into a single universal MX bound)",
       "reference_superK":"https://journals.aps.org/prd/abstract/10.1103/PhysRevD.102.112011",
       "conditional_input_MX_min_GeV":1e15,
       "dimension6_gauge_exchange":"At tree level A6~g5²/MX²; if MX=g5*(5r/sqrt30), coefficient is 6/(5r²) in chosen normalization, before flavor, Wilson matching and hadronic matrix elements.",
       "benchmarks":rows,
       "critical_obstacle":"Messenger M and SU5 gauge boson MX are NOT the same scale: MX/M can be much smaller than 1 for r/M<<1, so E6 messenger mass stability does not imply proton stability.",
       "no_lifetime_prediction":"A model-specific p->e+pi0 lifetime needs 3-family embeddings, X/Y coupling matrices, renormalized Wilson coefficients, hadronic matrix elements, all additional E6 gauge bosons and colored triplet operators. The M_X>=1e15 GeV proxy is an illustrative external engineering requirement, not a derived experimental inequality."}
if __name__=="__main__":
    v=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(v["status"],v["benchmarks"][2]["X_vector_mass_over_M"])
