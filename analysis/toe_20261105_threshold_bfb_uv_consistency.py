#!/usr/bin/env python3
"""Front 3: threshold-matched gauge-only two-loop EFT and scalar BFB veto.

Use high-energy unbroken X=3(B-3Le), with breaking vevs and S,T,Nc
masses below mu0=1e10 GeV. Vectorlike Q can instead have SM-and-X
vectorlike Dirac mass above mu0. Integrate exact gauge-only two-loop
one-light/one-heavy sharp threshold with continuous K,g2,g3 matching.
One-loop piecewise analytic check, BFB scalar quartic copositivity,
and exact discrete Z9 dimension-six DeltaB operator selection.
Yukawa/scalar two-loop RG and detailed proton amplitudes not done.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_threshold_gauge_scalar_stability_proton.json"
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261105_two_loop_gauge_matrix_nonabelian import inventory,beta_one_mat,two_loop_parts,B_NA_SM,DELTA_NA,delta_b,integrate
from toe_20261105_joint_flavor_u1_z9_seesaw_scalar_quality import sm_qqql,spec
D=16*math.pi**2
LOW=1e10;HIGH=1.3163003690605982e15
def step(y,mu1,mu2,active,two):
    if mu1==mu2:return y
    rows=inventory(active)
    B=beta_one_mat(rows)
    b=delta_b(active)
    bna=B_NA_SM+(DELTA_NA if active else np.zeros((2,2)))
    def rhs(t,y):
        K=np.array([[y[0],y[1]],[y[1],y[2]]],float)
        g2,g3=y[3:]
        assert np.linalg.det(K)>0 and min(g2,g3)>0
        dk=-B/(8*math.pi**2)
        feedback=np.zeros(2)
        if two:
            corr,feedback=two_loop_parts(rows,K,g2,g3)
            dk-=corr/(128*math.pi**4)
        gg=np.array([g2,g3])
        dg=2*gg**2*b/D
        if two:dg+=2*gg**2*(bna@gg+feedback)/D**2
        return [dk[0,0],dk[0,1],dk[1,1],*dg]
    sol=solve_ivp(rhs,(0,math.log(mu2/mu1)),y,rtol=3e-10,atol=3e-11)
    assert sol.success,sol.message
    return sol.y[:,-1]
def run(mq,two):
    y=np.array([1/.36**2,0.,1/.045**2,.56**2,.67**2])
    mid=max(LOW,min(HIGH,mq))
    y=step(y,LOW,mid,False,two)
    at_mid=y.copy()
    y=step(y,mid,HIGH,True,two)
    K=np.array([[y[0],y[1]],[y[1],y[2]]])
    assert min(np.linalg.eigvalsh(K))>0
    return {"MQ_GeV":mq,"K_UV":K.tolist(),"K_min_eigenvalue":float(min(np.linalg.eigvalsh(K))),
        "g2_UV":math.sqrt(y[3]),"g3_UV":math.sqrt(y[4]),
        "K_at_threshold":[[at_mid[0],at_mid[1]],[at_mid[1],at_mid[2]]]}
def bfb(lamT,lamS,lamTS):
    inequality=lamTS+2*math.sqrt(lamT*lamS)
    allowed=lamT>0 and lamS>0 and inequality>=-1e-14
    if lamTS<0:
        xt=-lamTS/(2*lamT) # x=|T|²/|S|²
        chosen=lamT*xt*xt+lamTS*xt+lamS
    else:chosen=lamS
    assert (chosen>=-1e-13)==allowed
    return {"lambdaT":lamT,"lambdaS":lamS,"lambdaTS":lamTS,
      "bounded_from_below_quartic":allowed,
      "copositivity_margin":inequality,
      "quartic_at_analytic_test_direction":chosen}
def main():
    full2=integrate(two=True)
    full1=integrate(two=False)
    rows=[]
    mqlist=(LOW,3e10,1e11,1e12,3e12,1e13)
    for mq in mqlist:
        r2=run(mq,True);r1=run(mq,False)
        r2["K_UV_oneloop"]=r1["K_UV"]
        rows.append(r2)
    assert np.max(abs(np.array(rows[0]["K_UV"])-np.array(full2["K_high"])))<5e-8
    Bv=beta_one_mat(inventory(True))-beta_one_mat(inventory(False))
    for row in rows:
        mq=row["MQ_GeV"]
        delta=np.array(row["K_UV_oneloop"])-np.array(full1["K_high"])
        expect=Bv/(8*math.pi**2)*math.log(mq/LOW)
        assert np.max(abs(delta-expect))<4e-8
    checks=[bfb(.11,.12,z) for z in (-.35,-.24,-.2,0.,.3)]
    assert sum(z["bounded_from_below_quartic"] for z in checks)==3
    # Verify the actual protective residual charges from prior model.
    protected=sm_qqql(spec())
    assert len(protected)==3 and all(z["all_nonzero_mod_Z9"] for z in protected)
    out={"status":"PASS_SHARP_VECTORLIKE_THRESHOLD_TWOLOOP_SCALAR_BFB_PROTON_GUARDS",
       "reference_mu_GeV":LOW,"UV_mu_GeV":HIGH,"heavy_vectorlike_mass_scan":rows,
       "one_loop_B_vectorlike_increment":Bv.tolist(),
       "one_loop_exact_sharp_decoupling_identity":"K_UV(MQ)-K_UV(MQ=mu0)=B_Q/(8pi²) ln(MQ/mu0) with all light fields active.",
       "two_loop_reference_no_threshold_matches_prior_baseline":True,
       "tree_level_scalar_quartic_potential":"lambdaT*abs(T)^4+lambdaS*abs(S)^4+lambdaTS*abs(T)^2*abs(S)^2",
       "tree_level_bounded_below_examples":checks,
       "exact_Z9_proton_dim6_charge_screens":protected,
       "lowest_PQ_breaker_still":"Sdag T² (dimension 3); scalar potential contains a physical phase-sensitive cubic regardless of quartic BFB",
       "model_consistency_assumptions":"Unbroken U1X above mu0=1e10; both scalar vevs and physical scalars and sterile neutrino masses below mu0; vectorlike SM,X-Dirac mass MQ may exceed mu0 without X breaking. These scales are independent fiducial inputs.",
       "missing_from_true_complete_uv":"No Yukawa beta functions, no full scalar quartic RG/bounce metastability, no finite matching beyond sharp leading-log decoupling, no threshold for broken gauge boson, no actual proton decay Wilson coefficients/renormalization, no LFV limits, no precision matching to data.",
       "references":["Davidson Gorbahn PRD114 055020 2026","E6 G2 SU3A embedding EPJC 2026 threshold uncertainty"]}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("THRESHOLD_BFB_PASS",[(f"{x['MQ_GeV']:.0e}",round(x["K_min_eigenvalue"],4)) for x in rows],"quartic",[z["bounded_from_below_quartic"] for z in checks],flush=True)
    return out
if __name__=="__main__":main()
