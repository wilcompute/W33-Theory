"""Frozen and recomputed F20-equivariant full 600-cell chiral quantum
support bridge, using the complete 48000 selector census."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_W33_H4_chiral_4regular_embedding import main as embed
from w33_20261008_H4_chiral_W33_CSS_check_cycles import main as cycles

def saved(name):return json.loads((ROOT/"data"/name).read_text())

def test_all_48000_equivariant_60_address_bijections_exact():
 x=saved("w33_20261008_F20_48000_selectors_chiral_union_census.json")
 assert x["F20_equivariant_60_address_bijections_exhausted"]==48000
 assert x["W33_edge_line_adjacency_edge_count"]==120
 assert x["full_edge_containment_achieved"]
 assert x["highest_W33_edges_respecting_H4_chiral_pair_union"]==120
 assert x["intersection_size_histogram"]=={"0":1920,"20":8688,"40":15384,"60":13920,"80":6576,"100":1392,"120":120}
 assert sum(x["intersection_size_histogram"].values())==48000
 assert len(set(x["best_map_W33_to_A5_coset_index"]))==60

def test_full_explicit_W33_120_to_real_H4_bichiral_adjacency_embedding():
 x=embed()
 assert x["perfect_selectors"]==120
 assert x["5point_to_6point_A5_group_isom_verified_all_3600_products"]
 assert len(set(x["concrete_selected_60_W33_edge_to_600cell_antipodal_pair_address"]))==60
 assert x["actual_600cell_plus_graph_incident_W33_edges"]==60
 assert x["actual_600cell_minus_graph_incident_W33_edges"]==60
 assert x["order5_W33_normalizer_r_preserves_both_edge_colors"]
 assert x["order4_W33_normalizer_s_exchanges_two_edge_colors"]
 assert x["W33_60_edge_line_graph_is_4regular_spanning_subgraph_of_24regular_H4_pair_union"]
 assert not x["W33_graph_is_not_the_entire_degree12_H4_plus_or_minus_graph"]==False

def test_all_40_triangles_and_20_octagons_h4_supports():
 x=cycles()
 assert x["X_checks_all_three_H4_union_adjacencies_verified"]
 assert x["Z_checks_all_eight_H4_union_adjacencies_verified"]
 assert x["X_check_chiral_plus_degree_hist"]=={0:10,1:10,2:10,3:10}
 assert x["Z_check_cycle_chiral_plus_edge_hist"]=={2:5,4:10,6:5}
 assert (x["GF2_rank_X"],x["GF2_rank_Z"])==(39,19)
 assert x["encoded_qubits"]==2 and x["distance"]==6
 assert x["all_check_supports_transport_via_actual_60_address_embedding"]
 assert not x["H4_native_tetrahedral_faces_identified_with_W33_20_octagons"]
