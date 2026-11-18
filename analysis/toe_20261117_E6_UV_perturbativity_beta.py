"""One-loop E6 gauge beta-function for concrete two-adjoint, two-Higgs,
four-messenger-vectorlike-pair and three-family field inventory.

N=1 SUSY E6: C2(adj)=12, Dynkin T(27)=3, T(78)=12.
b = -3*C2(G)+sum chiral T(R)
  = -36 +2*12 + (4+2)*2*3 +3*3 = +33.
The beta convention is d alpha^-1 /d ln mu= -b/(2pi).
At alpha_GUT=1/25 and common threshold M:
alpha^-1(mu)=25 -33/(2pi)*ln(mu/M).
Landau pole mu/M=exp(50pi/33)~118.2. Planck gauge
coupling may become nonperturbatively large near M_Pl.

This is a CONDITIONAL simple common-threshold estimate, not a
full broken-phase E6 threshold/matching or two-loop running.
All vectorlike fields might not be present above same M, and
the Higgs multiplet may be heavy at different scales.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_E6_split_sector_1loop_UV_beta.json"
def evalpoint(M,alpha0=1/25,planck=2.435e18,b=33):
    ln=math.log(planck/M)
    inv=1/alpha0-b*ln/(2*math.pi)
    pole_ratio=math.exp(2*math.pi/(b*alpha0)) if b>0 else math.inf
    return {"messenger_common_threshold_GeV":M,
      "reduced_planck_GeV":planck,"ln_scale_span":ln,
      "inverse_alpha_at_planck":inv,
      "alpha_at_planck_one_loop":(1/inv if inv>0 else None),
      "one_loop_landau_pole_below_planck":inv<=0,
      "pole_over_messenger_scale":pole_ratio,
      "note":"All multiplets assumed simultaneously active above M, matching alpha=1/25 at M. Strong-coupling values not reliable at one loop."}
def verify():
    inventory=[
      {"field":"E6_N1_vector_multiplet","n":1,"Dynkin":"-3*C2(E6)","contribution":-36},
      {"field":"two_chiral_E6_adjoints_A_B","n":2,"Dynkin":"T(78)=12","contribution":24},
      {"field":"four_27_bar27_messenger_pairs","n":4,"Dynkin":"2*T(27)=6","contribution":24},
      {"field":"two_27_bar27_Higgs_singlet_breaking_pairs","n":2,"Dynkin":"2*T(27)=6","contribution":12},
      {"field":"three_27_family_multiplets","n":3,"Dynkin":"T(27)=3","contribution":9}
    ]
    b=sum(item["contribution"] for item in inventory)
    assert b==33
    rows=[evalpoint(m,b=b) for m in (1e16,2e16,3.09e16,4e16,1e17)]
    assert rows[0]["one_loop_landau_pole_below_planck"]
    assert not rows[2]["one_loop_landau_pole_below_planck"]
    assert rows[2]["alpha_at_planck_one_loop"]>.3
    # Avoid strong coupling by alpha(Planck) < alpha_max:
    minM={}
    for amax in (1.,.3,.1):
        upper_ln=(1/.04-1/amax)*2*math.pi/b
        minM[str(amax)]=2.435e18/math.exp(upper_ln)
        assert minM[str(amax)]>0
    return {
      "status":"PASS_E6_TWO_ADJOINT_FOUR_MESSENGER_UV_BETA_PROXY",
      "N1_SUSY_one_loop_beta_b":b,
      "inventory":inventory,
      "UV_example_alpha_at_messenger_scale":.04,
      "landau_pole_ratio":math.exp(50*math.pi/33),
      "benchmarks":rows,
      "minimum_common_M_GeV_for_alpha_at_Planck_below":minM,
      "interpretation":"This field inventory has POSITIVE E6 beta b=33 (IR free / UV strong). A full renormalizable E6 GUT with all sectors simultaneously light at a single threshold cannot assume perturbativity to arbitrarily high UV. The numbers are CONDITIONAL and sensitive to masses, matching and extra fields.",
      "other_obstacles":"Decoupling exotics, E6 gauge boson masses and proton decay, higher loops, spinor/Higgs Yukawas, soft-breaking spectrum, threshold matching, complete scalar Hessian, global symmetry and anomaly constraints."
    }
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],z["N1_SUSY_one_loop_beta_b"],z["landau_pole_ratio"])
