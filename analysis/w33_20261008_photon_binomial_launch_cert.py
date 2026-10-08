"""95%-probability launch budgets for the earlier photonic n-detection test.

Earlier packets only bounded errors conditional on *n successful photons*;
this inverts an exact binomial tail to bound how many independent launches
are required to collect n successes with >=0.95 probability. Union bound
combines success collection and conditional correct classification:
Pr(success >= n) >= 0.975; Pr(error | n successes) <=0.025,
then Pr(correct total) >=0.95. The conditional n uses alpha=0.025.
"""
import math,json
from pathlib import Path
from scipy.stats import binom
R=Path(__file__).resolve().parents[1];D=R/"data";OUT=D/"w33_20261008_photon_binomial_launch_cert.json"
source=json.loads((D/"w33_20261008_photon_likelihood_information.json").read_text())
def exact_minimum_launches(n,p,target=.975):
 lo=n;hi=max(n+1,math.ceil(3*n/p))
 def chance(N):return float(binom.sf(n-1,N,p))
 assert chance(hi)>=target,(n,p,hi)
 while lo<hi:
  mid=(lo+hi)//2
  if chance(mid)>=target:hi=mid
  else:lo=mid+1
 N=lo
 assert chance(N)>=target and (N==n or chance(N-1)<target)
 return N,chance(N),chance(N-1)
def build():
 rows=[]
 for dark,system in ((0,0),(.05,.01),(.1,.02),(.2,.05)):
  for stages in (36,72,144):
   row=next(x for x in source["experiments"] if x["stages"]==stages and x["survival_per_stage"]==.99)
   nominal=row["min_full_anonymous_sorted_linf_margin"]
   robust=(1-dark)*nominal-2*system
   if robust<=0:continue
   n=math.ceil(8*math.log(54/.025)/(robust**2))
   p=.99**stages
   launch,lower,pre=exact_minimum_launches(n,p,.975)
   rows.append({"dark_count_fraction":dark,"per_output_systematic_error_bound":system,
          "stages":stages,"per_launch_success_probability":p,
          "observed_margin_lower_bound":robust,
          "successful_detections_for_conditional_error_at_most_0.025":n,
          "exact_minimal_launches_for_collection_probability_at_least_0.975":launch,
          "binomial_collection_probability_at_launches":lower,
          "binomial_collection_probability_one_fewer":pre,
          "joint_success_probability_lower_bound":.95,
          "expected_launches_to_collect_n":math.ceil(n/p)})
 winners={}
 for dark,eps in ((0,0),(.05,.01),(.1,.02),(.2,.05)):
  eligible=[r for r in rows if r["dark_count_fraction"]==dark and r["per_output_systematic_error_bound"]==eps]
  best=min(eligible,key=lambda r:r["exact_minimal_launches_for_collection_probability_at_least_0.975"])
  winners[f"dark{dark}_eps{eps}"]={"stages":best["stages"],
         "minimum_95pct_joint_launch_budget":best["exact_minimal_launches_for_collection_probability_at_least_0.975"],
         "required_successful_detections":best["successful_detections_for_conditional_error_at_most_0.025"]}
 return {"rows":rows,"winners":winners,
  "proof":"Union bound: collection failure <=0.025 using exact Binomial tail, conditional classifier error <=0.025 using Hoeffding of sorted empirical frequencies. Hence overall failure <=0.05. Assumes i.i.d. launched-photon survival and successful detections drawn independently from fixed model with known uniform background and bounded mismatch.",
  "not_physically_calibrated":True,
  "no_claim_of_actual_hardware":True}
if __name__=="__main__":
 x=build();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps(x["winners"],indent=2),flush=True);print("PHOTON_LAUNCH_CERT_PASS")
