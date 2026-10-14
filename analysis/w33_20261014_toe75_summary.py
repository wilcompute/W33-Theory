"""TOE75 independent summary of GitHub-regenerated all-five-front data.

Do NOT confuse numerical multistart minima with the rigorous V=0
Theta(4,4,4) 120° theorem. Print orbit classifications and V>0
optimized phase data with explicit no-global-interacting caveat.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(stem):
    return json.loads((ROOT/("data/w33_20261014_toe75_"+stem+".json")).read_text())

def main():
    g=read("structural")
    u=read("continuous_interacting")
    t=read("exact_120_flux")
    q=g["quantum_geometry"]
    assert q["candidate_neighbors_outside_all_seven_orbits"]>=1
    assert q["new_orbit_information"]["one_additional_orbit_size"]>0
    assert len(u["interaction_scans"])==4
    a=t["global_120_advantage_below_best_Z2"]
    assert 0.02069<a<0.02070
    rows=[]
    for z in u["interaction_scans"]:
        rows.append({
          "V":z["V"],
          "2d_local_phase_pi_units":z["best_local_two_dimensional_phase_pi_units"],
          "2d_local_advantage_below_Z2":z["best_local_advantage_over_Z2"],
          "1d_boundary_phase_pi_units":z["one_dimensional_continuous_optimizer_phase_pi_units"],
          "1d_boundary_advantage":z["boundary_optimized_advantage_over_Z2"],
          "finite_beta_boundary_advantages":z["beta_resolved_boundary_optimized_minus_Z2_free_energy_advantage"]})
    summary={
      "status":"PASS_TOE75_VERIFIED_QUANTUM_AND_CHIRAL_120_DISCOVERY",
      "additional_cover_neighbors_outside_seven_previous_orbits":q["candidate_neighbors_outside_all_seven_orbits"],
      "fully_enumerated_one_new_orbit":q["new_orbit_information"],
      "other_20_neighbors_still_unclassified":q["not_yet_classified_candidate_remainder"],
      "complete_PGSp_orbits_previously_known":7,
      "native_theta_V0_exact_global_chiral_120":{
        "phase_pairs_pi_units":t["global_minimum_phase_pairs_pi_units"],
        "ground_energy":t["global_minimum_energy_analytic"],
        "improvement_below_Z2":a},
      "interacting_numerical_local_optimizations":rows,
      "limits":"No theorem that every exact-cover orbit has been found; no interacting U1 global minimization and no physical 4D or dynamical gauge claims."}
    (ROOT/"data/w33_20261014_toe75_verified_summary.json").write_text(
      json.dumps(summary,indent=2)+"\n")
    print(summary["status"])
    print("QUANTUM",json.dumps(summary["fully_enumerated_one_new_orbit"]),
          "unclassified_remainder",summary["other_20_neighbors_still_unclassified"])
    print("FREE120",summary["native_theta_V0_exact_global_chiral_120"])
    for row in rows:
        print("MATTER",row["V"],"local",row["2d_local_phase_pi_units"],
              "gain",row["2d_local_advantage_below_Z2"],
              "thermal_boundary_advantages",row["finite_beta_boundary_advantages"])

if __name__=="__main__":main()
