"""TOE74: independent finite-size quantitative comparison of U1 grid vs Z2
corners and seven-cover 2-flip neighbor incidence. Source regen only.
This script deliberately prints tolerances and gap to sampled corners, and
detects near-degenerate Z2 minimizers before assigning a unique winner.
"""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe74_quantum_neighbors import certificate as cover
from w33_20261014_toe74_u1_manybody_finite_t import certificate as fermion

def certificate():
    Q=cover();F=fermion()
    mapping=[]
    for row in Q["neighborhood_summary"]:
        i=row["seed_index"]
        mapping.append({
          "seed":i,"number_of_20_loop_neighbors":row["local_20_loop_degree"],
          "links_to_other_six_seeds":row["links_to_other_six_given_representatives"],
          "local_18_19_loop_counts":[row["local_18_loop_changes"],row["local_19_loop_changes"]]})
    mat=[]
    for data in F["V_scans"]:
        V=data["V"];corners=data["full_spectrum_four_corner_free_energies"]
        corners_sorted=sorted(corners,key=lambda c:c["ground"])
        baseline=corners_sorted[0]["ground"]
        paired=[c["phase_pi_units"] for c in corners_sorted
                if abs(c["ground"]-baseline)<1e-9]
        best=data["min_grid_holonomy"]
        gain=baseline-best["energy"]
        assert gain>=-1e-7
        thermal=[]
        for beta in F["finite_temperature_inverse_beta"]:
            key=str(beta)
            ordered=sorted(corners,key=lambda c:c["canonical_log_partition_free_energy"][key])
            thermal.append({"beta":beta,
                "winning_Z2_corners":[c["phase_pi_units"] for c in ordered if
                      abs(c["canonical_log_partition_free_energy"][key]-
                          ordered[0]["canonical_log_partition_free_energy"][key])<1e-9],
                "Helmholtz_F_spread":max(c["canonical_log_partition_free_energy"][key] for c in corners)-
                                    min(c["canonical_log_partition_free_energy"][key] for c in corners)})
        mat.append({"V":V,"sampled_U1_minimum_phase_pi_units":best["phase_pi_units"],
            "sampled_U1_minimum_energy":best["energy"],
            "ground_Z2_best_energy":baseline,
            "sampled_U1_below_all_Z2_corners_by":gain,
            "all_Z2_ground_energy_corners_at_1e-9_tolerance":paired,
            "all_four_Z2_corner_energies":[{"corner":z["phase_pi_units"],"E0":z["ground"]}
                for z in corners],
            "finite_beta_Z2_preferences":thermal})
    return {
     "status":"PASS_TOE74_QUANTIFIED_INTERIOR_AND_ORBIT_NEIGHBORS",
     "seven_seed_actual_flip_degree":mapping,
     "second_order_neighbor_representatives":Q["distinct_second_order_neighbor_covers_over_seven_seeds"],
     "outside_seven_exact_representatives":Q["distinct_new_covers_outside_seven_representatives"],
     "eleven_site_static_U1_finite_manybody":mat,
     "caveat":"U1 minimum only over 5x5 grid, not continuous global optimum. Corner minimizer ties must be treated as such. Static gauge parameters, no dynamical gauge vacuum and no thermodynamic symmetry-breaking claim."}
if __name__=="__main__":
    o=certificate()
    (ROOT/"data/w33_20261014_toe74_verified_quantitative_summary.json").write_text(json.dumps(o,indent=2)+"\n")
    print(o["status"])
    print("GRAPH",json.dumps({"degrees":[r["number_of_20_loop_neighbors"] for r in o["seven_seed_actual_flip_degree"]],
                 "links":[r["links_to_other_six_seeds"] for r in o["seven_seed_actual_flip_degree"]],
                 "new_representatives":o["outside_seven_exact_representatives"]}))
    for r in o["eleven_site_static_U1_finite_manybody"]:
        print("U1-V",r["V"],"sampled",r["sampled_U1_minimum_phase_pi_units"],"advantage",r["sampled_U1_below_all_Z2_corners_by"],
              "tied_Z2",r["all_Z2_ground_energy_corners_at_1e-9_tolerance"],
              "thermal",[e["winning_Z2_corners"] for e in r["finite_beta_Z2_preferences"]])
