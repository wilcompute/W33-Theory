"""Atiyah-Singer torus flux: index=charge*flux; 4D gauge anomaly
firewall on the proposed three-generation E6 27 construction.
Topological theorem is established prior art, not proved by this code.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round14_magnetic_three_generation.json"
def anomalies(indices):
    q=(1,-2,4);dim=(16,10,1);ind=(2,1,0)
    return {"mixed_gravity_U1":sum(indices[i]*dim[i]*q[i] for i in range(3)),
      "U1_cubic":sum(indices[i]*dim[i]*q[i]**3 for i in range(3)),
      "SO10_squared_U1":sum(indices[i]*ind[i]*q[i] for i in range(3))}
def run():
    M=3
    internal=[M*q for q in (1,-2,4)]
    external=[M]*3
    bad=anomalies(internal);good=anomalies(external)
    flavor={"mixed_gravity_U1F":M*(16+10+1),"U1F_cubic":M*(16+10+1)}
    checks={"external_flux_three_complete_27":external==[3]*3,
      "three_complete_27_cancel_SO10xU1_anomalies":not any(good.values()),
      "internal_flux_has_3_minus6_12_chiral_indices":internal==[3,-6,12],
      "internal_flux_surviving_4D_U1_anomalous":all(x!=0 for x in bad.values()),
      "gauged_external_flavor_U1F_anomalous_without_inflow":all(x>0 for x in flavor.values())}
    out={"schema":"w33.round14.mag_torus_index_anomaly_firewall.v1",
      "literature":"https://academic.oup.com/ptep/article/2024/5/053B06/7667937 (T2 index ind D_q=q M; M=3 gives three zero modes for charge1)",
      "topological_input":"A 6D chiral fermion on magnetized T² has 4D net chiral index q*M under standard assumptions. M=3 is freely CHOSEN, not derived from W33 q=3.",
      "E6_27_SO10_U1":[["16",16,1],["10",10,-2],["1",1,4]],
      "case_internal_E6_U1_flux":{"M":M,"net_chiral_indices":internal,"4D_SO10_U1_anomalies":bad,
       "verdict":"Fails naive 4D gauged-U1 anomaly cancellation without added boundary matter, inflow or Green-Schwarz mechanism; not three full 27s."},
      "case_external_uniform_U1F_flux":{"M":M,"net_chiral_indices":external,"4D_SO10_U1_anomalies":good,
       "gauged_U1F_anomalies":flavor,
       "verdict":"Produces an INDEX of three complete 27s for a uniform external flavor-U1 flux, but gauging U1F itself requires anomaly cancellation and full consistent 6D completion. Setting M=3 is input, not TOE prediction."},
      "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":checks,"internal":bad,"external":good}))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
