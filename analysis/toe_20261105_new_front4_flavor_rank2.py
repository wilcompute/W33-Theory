#!/usr/bin/env python3
"""TOE front 4: predictive rank-two neutrino/flavour ansatz falsifiers.

Use explicitly quoted NuFIT v6.1 (Nov 2025) NO/IO 3sigma
1D marginal intervals (conservative independent Cartesian superset).
Exact TM2 trimaximal solar sum rule and rank-two m_ee=0 are outside
these intervals; TM1 survives only this solar test. Compute rigorous
phase-independent positive lower bounds for 0nu2beta Majorana m_ee
given exactly one massless eigenstate, using independent intervals.
No claim of current observation of 0nu2beta or proof Majorana.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_new_front4_flavor_rank2_selection.json"
# NuFIT6.1 2025 without SK atmospheric 3sigma ranges,
# published November 2025 at https://nu-fit.org/ .
# Range table v61.tbl-parameters.pdf; delta m3l conventions:
# NO dm31 positive, IO dm32 negative.
R={
 "s12":(.2893,.3295),
 "s13_NO":(math.sin(math.radians(8.26))**2,math.sin(math.radians(8.95))**2),
 "s13_IO":(math.sin(math.radians(8.32))**2,math.sin(math.radians(8.99))**2),
 "dm21":(7.236e-5,7.823e-5),
 "dm31_NO":(2.450e-3,2.576e-3),
 "abs_dm32_IO":(2.421e-3,2.547e-3)}
def tm(s13):
    return {"TM1_solar_s12":1-2/(3*(1-s13)),
            "TM2_solar_s12":1/(3*(1-s13))}
def floorNO():
    s12lo,s12hi=R["s12"]
    s13lo,s13hi=R["s13_NO"]
    a=math.sqrt(R["dm21"][0])*s12lo*(1-s13hi)
    b=math.sqrt(R["dm31_NO"][1])*s13hi
    return a,b,max(0,a-b)
def floorIO():
    s12lo,s12hi=R["s12"]
    s13lo,s13hi=R["s13_IO"]
    # IO m3=0, m2²=|dm32²|, m1²=m2²-dm21².
    a=math.sqrt(R["abs_dm32_IO"][0]-R["dm21"][1])*(1-s12hi)*(1-s13hi)
    b=math.sqrt(R["abs_dm32_IO"][1])*s12hi*(1-s13lo)
    return a,b,max(0,a-b)
def monte_carlo(order,n=45000):
    rng=np.random.default_rng(112261+int(order=="IO"))
    u=rng.random((n,4))
    s12=R["s12"][0]+u[:,0]*(R["s12"][1]-R["s12"][0])
    s13=R["s13_"+order][0]+u[:,1]*(R["s13_"+order][1]-R["s13_"+order][0])
    dm21=R["dm21"][0]+u[:,2]*(R["dm21"][1]-R["dm21"][0])
    high=R["dm31_NO"] if order=="NO" else R["abs_dm32_IO"]
    dm3=high[0]+u[:,3]*(high[1]-high[0])
    if order=="NO":
        a=np.sqrt(dm21)*s12*(1-s13)
        b=np.sqrt(dm3)*s13
    else:
        a=np.sqrt(dm3-dm21)*(1-s12)*(1-s13)
        b=np.sqrt(dm3)*s12*(1-s13)
    # Exact minimum over arbitrary Majorana phases at each sample
    return float(np.min(abs(a-b))),float(np.max(a+b))
def main():
    tm2min=tm(R["s13_NO"][0])["TM2_solar_s12"]
    tm2max=tm(R["s13_NO"][1])["TM2_solar_s12"]
    tm1min=tm(R["s13_NO"][1])["TM1_solar_s12"]
    tm1max=tm(R["s13_NO"][0])["TM1_solar_s12"]
    assert tm2min>R["s12"][1]
    assert R["s12"][0]<tm1min<tm1max<R["s12"][1]
    a,b,lowNO=floorNO()
    c,e,lowIO=floorIO()
    assert lowNO>.001 and lowIO>.01
    sampleNO=monte_carlo("NO")
    sampleIO=monte_carlo("IO")
    assert sampleNO[0]>=lowNO-1e-14
    assert sampleIO[0]>=lowIO-1e-14
    mnuNOmin=math.sqrt(R["dm21"][0])+math.sqrt(R["dm31_NO"][0])
    mnuIOmin=math.sqrt(R["abs_dm32_IO"][0]-R["dm21"][1])+math.sqrt(R["abs_dm32_IO"][0])
    results={"status":"PASS_RANK2_FLAVOR_TM2_AND_MEE_ZERO_RECTANGLE_EXCLUSION",
      "source":"NuFIT v6.1 (2025), 3sigma 1D intervals (without SK-atm); September 2026 independent Bari is narrower; intentionally use conservative Cartesian products",
      "ranges_used":{k:list(v) for k,v in R.items()},
      "TM2_exact_model_solar_prediction_range":[tm2min,tm2max],
      "TM1_exact_model_solar_prediction_range":[tm1min,tm1max],
      "TM2_outside_3sigma_s12_projection":True,
      "TM1_not_excluded_by_solar_angle_alone":True,
      "TBM_s13_zero_excluded":R["s13_NO"][0]>0,
      "rank_two_see_saw_massless_lightest_prediction":{"normal_ordering":{
         "m_ee_two_positive_amplitude_bounds": [a,b],
         "strict_lower_bound_mee_eV":lowNO,
         "sampled_minimum_mee_eV":sampleNO[0],
         "minimal_mass_sum_eV":mnuNOmin},
        "inverted_ordering":{
         "m_ee_two_positive_amplitude_bounds":[c,e],
         "strict_lower_bound_mee_eV":lowIO,
         "sampled_minimum_mee_eV":sampleIO[0],
         "minimal_mass_sum_eV":mnuIOmin}},
      "consequence":"With rank two and one exactly massless Majorana neutrino, m_ee=0 is excluded throughout supplied independent conservative 3sigma ranges for both orderings. Exact TM2 second PMNS column trimaximal is also excluded by 3sigma solar+reactor intervals. Existing general type-I seesaw with arbitrary free Yukawas is not excluded.",
      "not_claimed":"0nu2beta detection; exclusion of all texture zero models; an actual statistical joint 3sigma fit; mass ordering established; first-principles masses or CP",
      "literature":["NuFIT v6.1 (2025) https://www.nu-fit.org/?q=node/309","Bari preliminary 2026.a https://global-nu.org/results.html","TM1 TM2 conventional trimaximal mixing literature"]}
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print("FLAVOR_PASS TM2",round(tm2min,6),round(tm2max,6),
         "s12_max",R["s12"][1],"meeNO",lowNO,"meeIO",lowIO,flush=True)
    return results
if __name__=="__main__":main()
