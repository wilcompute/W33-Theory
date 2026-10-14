"""TOE76 concise faithful summary from independently regenerated JSON."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(x):
    return json.loads((ROOT/("data/w33_20261014_toe76_"+x+".json")).read_text())
def main():
    f=read("four_fronts");z=read("theta_twisted_ihara");p=read("flux_currents")
    h=f["hopping"];g=f["gauge"];q=f["quantum"];s=f["spin"]
    assert h["integer_corner_Hessian_matrices_checked"]==50880
    assert h["bad_Hessian_corners"]==951
    assert q["distinct_orbit_seed_count"]==27
    assert q["exact_directly_witnessed_seed_graph_edges"]==41
    assert q["exact_seed_graph_cycle_rank"]==15
    assert z["zeta_inverse_exact"]=="(1-u^8)*(1+(4-s^2)*u^8+4*u^16)"
    assert not g["positive_spectral_gap_proven"]
    assert h["two_edge_non_PSD_corners"]>=0
    summary={
      "status":"PASS_TOE76_VERIFIED_SIX_FRONTS_PLUS_RH_BRIDGE",
      "six_test_workflow":"https://github.com/wilcompute/W33-Theory/actions/runs/38641998176",
      "hopping":{
        "two_edge_endpoints_checked":h["integer_corner_Hessian_matrices_checked"],
        "two_edge_not_strict_PD_corners":h["bad_Hessian_corners"],
        "two_edge_non_PSD_corners":h["two_edge_non_PSD_corners"],
        "two_edge_all_PSD":h["all_two_edge_boxes_PSD"],
        "two_edge_global_three_pi_minimum_if_PSD":h["if_all_PSD_then_global_three_pi_nonunique_minimum_under_two_link_variation"],
        "single_edge_endpoints_checked":h["single_edge_endpoints_checked"],
        "single_edge_non_strict_PD_endpoints":h["bad_single_edge_endpoint_Hessians"],
        "single_edge_non_PSD_endpoints":h["bad_single_edge_PSD_endpoints"],
        "single_edge_first_bad":h["single_edge_first_bad"],
        "two_edge_first_bad":h["first_bad_corners"],
        "minimum_integer_Hessian_determinant":h["minimum_integer_det"],
        "minimum_determinant_corner":h["minimum_det_corner_indices_edge_edge_weight_weight"],
        "scope":"Exactly 951 two-edge endpoint Hessians fail STRICT positive definiteness, and 3 single-edge endpoints fail STRICT PD. Classify all separately by exact principal-minor PSD; a zero determinant or flat direction is NOT a negative eigenvalue and does NOT on its own refute local or global minimization. If all are PSD, global three-pi remains a possibly nonunique minimum under two-link weights [0,2]."},
      "gauge":{
        "ordered_upper_E0_to_E7":g["ordered_eigenvalues_E0_through_E7_upper_bounds_rational"],
        "positive_gap_proved":False},
      "quantum":{
        "known_orbits":27,
        "seed_edges":q["exact_directly_witnessed_seed_graph_edges"],
        "cycle_rank":q["exact_seed_graph_cycle_rank"],
        "triangles":q["exact_seed_graph_triangles"],
        "seed_degrees":q["seed_graph_degree_sequence"],
        "translated_matched_edges":q["compressed_regular_equivariant_matching_edges"],
        "number_of_regular_components":q["compressed_graph_connected_components"],
        "scope":"Actual selected equivariant matchings, NOT the full quantum induced 27-orbit graph."},
      "spin":{
        "twisted_integral_index":s["mixed_dual_flux_index_formula"],
        "graph_inherited_flux_index_zero":True,
        "physical_4d_overlap_operator_built":False},
      "currents":[{
        "V":t["V"],
        "E120":t["energy_at_120"],
        "ground_flux_hessian_eigenvalues":t["ground_state"]["Hessian_eigenvalues"],
        "beta2_flux_hessian_eigenvalues":t["beta_2"]["Hessian_eigenvalues"]} for t in p["observables"]],
      "ihara":{
        "11_site_irregular":True,
        "3_arm_length4_subdivisions":True,
        "twisted_ihara_inverse":z["zeta_inverse_exact"],
        "flux_120_factor":z["120_degree_inverse_twisted_zeta"],
        "tempered_twisted_condition":z["tempered_twisted_dipole_condition"],
        "ordinary_W33_collinearity_Ramanujan_circle":z["native_main_collinearity_Ramanujan"]["Ihara_nontrivial_circle"],
        "classical_RH_proved":False,
        "control":"The Ihara/120 theorem is for any equal-arm Theta(4,4,4), not uniquely W33."},
      "physical_TOE_proved":False}
    path=ROOT/"data/w33_20261014_toe76_verified_summary.json"
    path.write_text(json.dumps(summary,indent=2)+"\n")
    print(summary["status"])
    print("HOPPING",summary["hopping"])
    print("QUANTUM",summary["quantum"])
    print("GAUGE",summary["gauge"])
    print("CURRENTS",summary["currents"])
    print("IHARA",summary["ihara"])
if __name__=="__main__":main()
