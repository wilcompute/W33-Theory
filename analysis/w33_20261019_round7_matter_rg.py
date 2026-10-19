"""Fronts 1 and 5: anomaly-safe trinification 27 and a CONDITIONAL
one-loop transmutation scale. This does NOT derive physical SM couplings.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round7_matter_rg.json"
# E6 27 -> (3,bar3,1) + (bar3,1,3) + (1,3,bar3);
# SU3^3 anomaly coefficient +1 for 3, -1 for bar3.
REP=[("3","bar3","1"),("bar3","1","3"),("1","3","bar3")]
d={"1":1,"3":3,"bar3":3}
a={"1":0,"3":1,"bar3":-1}
def calc():
    anomaly={}
    flavors={}
    for i,name in enumerate(("C","L","R")):
        contributions=[int(a[r[i]]*math.prod(d[r[j]] for j in range(3) if j!=i)) for r in REP]
        anomaly[name]={"sector_contributions":contributions,"total":sum(contributions)}
        # Effective 6 Weyl SU3 (anti)triplets=3 Dirac flavor-equivalents
        # per gauge factor, counting spectator-group multiplicity.
        Weyl=sum(math.prod(d[r[j]] for j in range(3) if j!=i) for r in REP if r[i]!="1")
        flavors[name]={"charged_Weyl_triplets":int(Weyl),
           "effective_Dirac_flavors":Weyl/2,
           "one_loop_b0":int(11-2/3*(Weyl/2)),
           "Witten_SU2_embedding_number_doublets":int(Weyl)}
    # SU9 fundamental 9 would have A=+1, conjugate bar9 A=-1
    # and vectorlike 9+9bar cancels (but doubles dof)
    G0=1e12
    params=[]
    for g in (.35,.5,.65):
        b0=flavors["C"]["one_loop_b0"]
        lam=G0*math.exp(-8*math.pi**2/(b0*g*g))
        params.append({"UV_mu_GeV":G0,"UV_SU3_coupling_g":g,
            "Lambda_one_loop_GeV":lam,
            "ratio_Lambda_over_UV":lam/G0})
    # The 1-loop RG equation dg/dlog(mu)=-b0 g^3/(16pi²)
    # integrates: 1/g²(mu2)=1/g²(mu1)+(b0/(8pi²))ln(mu2/mu1)
    g0=.5;mu0=G0;b0=9
    rg=[]
    for factor in (0.1,1,10,100):
        mu=mu0*factor
        inv=1/g0**2+b0/(8*math.pi**2)*math.log(factor)
        g=1/math.sqrt(inv)
        lam=mu*math.exp(-8*math.pi**2/(b0*g*g))
        rg.append({"mu_ratio":factor,"g_mu":g,"Lambda_GeV":lam,
              "relative_RG_invariant_error":abs(lam/params[1]["Lambda_one_loop_GeV"]-1)})
    checks={"trinification_chiral_27_anomaly_free":all(v["total"]==0 for v in anomaly.values()),
            "trinification_dimension_27":sum(math.prod(d[t] for t in r) for r in REP)==27,
            "effective_nflavors_three_each":all(f["effective_Dirac_flavors"]==3 for f in flavors.values()),
            "one_loop_b0_nine_for_three_SU3s":all(f["one_loop_b0"]==9 for f in flavors.values()),
            "SU2_Witten_anomaly_even":all(f["Witten_SU2_embedding_number_doublets"]%2==0 for f in flavors.values()),
            "one_loop_lambda_is_RG_invariant":max(f["relative_RG_invariant_error"] for f in rg)<1e-12,
            "UV_coupling_changes_generated_scale":params[-1]["Lambda_one_loop_GeV"]>1e7*params[0]["Lambda_one_loop_GeV"]}
    out={"schema":"w33.round7.trinification_anomaly_and_one_loop_rg.v1",
      "trinification_27_representations":REP,
      "group_representation_status":"A chiral (3,bar3,1)+(bar3,1,3)+(1,3,bar3) is an ANOMALY-FREE 27 under a conventional SU3_C x SU3_L x SU3_R gauge hypothesis. It is E6 prior art, not a W33-derived new matter multiplet. It does NOT realize a fundamental SU9 nine-mode fermion bath in E8 adjoint.",
      "local_SU3_cubic_anomalies":anomaly,
      "one_loop_flavor_count_and_beta":flavors,
      "SU9_fundamental_chiral_anomaly":"An isolated left-handed SU9 fundamental 9 has nonzero cubic gauge anomaly A=+1, so cannot by itself be a consistent chiral SU9 gauge matter theory. A 9+bar9 vectorlike pair has zero anomaly, but its doubled field content and mass are external assumptions. If SU9 is not gauged, cubic gauge anomaly is not applicable.",
      "scale_mechanism":"Standard 4D asymptotically-free SU3 gauge sector with b0=11N/3 - 2Nf/3=9 for N=3,Nf=3: beta(g)=-b0 g^3/(16pi²). Integrating gives Lambda=mu exp[-8pi²/(b0*g(mu)²)]. A gauge interaction can break continuous scaling through dimensional transmutation, but W33 counts alone determine neither g(mu0) nor the reference UV scale, so no absolute Lambda or physical mass is predicted.",
      "conditional_transmutation_examples":params,
      "RG_invariant_check":rg,
      "scope":"One-loop illustrative gauge model; ignores threshold masses, scalar contributions, gravity, electroweak breaking, 2-loop terms, full UV completion, gauge-group quotients, SM chiral spectrum and measured couplings. NOT a TOE prediction.",
      "prior_repo":"Existing repo Pass11687-91 E8 trinification, Pass11461-65 explicit physical maps, Pass10949 E8(-24).",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"anomaly":anomaly,
       "Lambdas":[x["Lambda_one_loop_GeV"] for x in params]},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":calc()
