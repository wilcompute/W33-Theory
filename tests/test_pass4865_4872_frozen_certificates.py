"""Frozen-certificate regression for Passes 4865--4872.

This is intentionally lightweight: the expensive exact producers remain the source
of truth, while CI checks that the promoted frozen certificates and manuscript
frontier cannot silently drift.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"

def load(name):
    return json.loads((DATA/name).read_text())

def test_pass4865_ternary_radical_filtration():
    d=load("PART_W33_PASS4865_TERNARY_LEVI_RADICAL_FILTRATION.json")
    assert d["ambient_Levi_H1_dimension_F3"]==64
    assert d["K33_generated_submodule_dimension"]==54
    assert d["canonical_edge_pairing"]["ambient_rank"]==35
    assert d["canonical_edge_pairing"]["ambient_radical_dimension"]==29
    assert d["PSp_submodule_lattice"]["proper_nonzero_submodule_dimensions"]==[14,19,24]
    assert d["PSp_submodule_lattice"]["composition_factor_dimensions_H1"]==[14,5,10,25,10]
    assert not d["extensions"]["0_to_29_to_54_to_25"]["PSp"]["splits"]
    assert not d["extensions"]["0_to_54_to_64_to_10"]["PGSp"]["splits"]
    assert d["nondegenerate_quotient"]["orthogonal_complement_dimension"]==10

def test_pass4866_steiner_clique_homology():
    d=load("PART_W33_PASS4866_STEINER_CLIQUE_HOMOLOGY_OBSTRUCTION.json")
    assert d["clique_complex"]["f_vector"]==[36,360,1200,1080,216]
    assert d["clique_complex"]["maximal_cliques"]=={"K3":120,"K5":216}
    assert d["clique_homology"]["F2_betti"]==[1,0,120,109,0]
    assert d["clique_homology"]["F3_betti"]==[1,0,120,109,0]
    assert d["even_triangle_boundary_span"]["F2_rank"]==324
    assert d["even_triangle_boundary_span"]["F3_rank"]==325
    assert d["adjoint_linear_bridge_obstruction"]["Hom_PSp_H2_to_Q10_dimension"]==0
    assert d["adjoint_linear_bridge_obstruction"]["Hom_PSp_Q10_to_H2_dimension"]==0

def test_pass4867_full_code_enumerator():
    d=load("PART_W33_PASS4867_CUT_ISING_FULL_CODE_ENUMERATOR.json")
    assert d["cut_space"]["size"]==2**35
    assert d["cut_space"]["minimum_nonzero"]==20
    assert d["cut_space"]["maximum"]==216
    assert d["cut_space"]["maximum_count"]==120
    assert d["full_code"]["size"]==2**36
    assert d["full_code"]["minimum"]==20
    assert d["full_code"]["maximum"]==216
    assert d["MacWilliams_dual_check"]["A0_to_A7"]["3"]==1080

def test_pass4869_marked_double_six_chart():
    d=load("PART_W33_PASS4869_MARKED_DOUBLE_SIX_K6_SYMPLECTIC_RESIDUE.json")
    assert d["marked_double_six"]=={"columns":6,"neighbor_orbit":20,"nonneighbor_orbit":15,"residue_vertices":35}
    assert d["symplectic_chart"]["nondegenerate_rank"]==6
    assert d["residue_automorphism_group"]["order"]==1440
    assert d["residue_automorphism_group"]["full_by_exhaustive_graph_automorphism_count"]

def test_pass4870_steiner_three_cover_and_quadratic_bridge():
    d=load("PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json")
    c=d["intrinsic_three_cover"]
    assert c["Steiner_triangles"]==120
    assert c["fibers"]==40 and c["fiber_size"]==3
    assert c["adjacency_lift_pairs"]==2160
    assert c["quotient"]=="SRG(40,12,2,4)"
    assert c["explicit_isomorphism_to_standard_W33"]
    assert c["PSp_action_on_quotient_order"]==25920
    q=d["quadratic_bridge"]
    assert q["Hom_PSp_Sym2H2_to_Q10_dimension"]==2
    assert q["orbit_fixed_space_table"]["pair_2160"]["Q10_fixed_dimension"]==2
    for name in ("diagonal","pair_120","pair_1620","pair_3240"):
        assert q["orbit_fixed_space_table"][name]["Q10_fixed_dimension"]==0

def test_pass4871_intrinsic_bracket():
    d=load("PART_W33_PASS4871_INTRINSIC_LEVI_ADJOINT_BRACKET.json")
    h=d["equivariant_alternating_products"]
    assert h["PSp_Hom_Lambda2Q_to_Q_dimension"]==1
    assert h["PGSp_Hom_Lambda2Q_to_Q_dimension"]==1
    assert h["unique_nonzero_map_rank"]==10
    assert d["Lie_checks"]=={"Jacobi_all_1000_basis_triples":True,"center_dimension":0,"derived_dimension":10,"perfect":True}

def test_pass4872_port_information_compiler():
    d=load("PART_W33_PASS4872_PORT_MATCHING_INFORMATION_COMPILER.json")
    assert d["local_selector"]["states"]==6
    assert d["45_point_table"]["optimal_global_fixed_binary_bits"]==117
    assert d["45_point_table"]["independent_local_binary_bits"]==135
    assert d["with_global_chirality"]["optimal_global_fixed_binary_bits"]==118

def test_shared_manuscript_frontier_promotes_packet_once():
    live=(ROOT/"analysis/W33_CURRENT_FRONTIER_MANIFEST.tex").read_text()
    legacy=(ROOT/"analysis/W33_CURRENT_FRONTIER_MANIFEST_THROUGH_4864.tex").read_text()
    insert=(ROOT/"analysis/PASS4865_4872_ternary_clique_cut_symplectic_insert.tex").read_text()
    quad=(ROOT/"analysis/PASS4870_steiner_w33_quadratic_bridge_insert.tex").read_text()
    assert "W33_CURRENT_FRONTIER_MANIFEST_THROUGH_4864" in live
    assert live.count("PASS4865_4872_ternary_clique_cut_symplectic_insert")==1
    assert live.count("PASS4870_steiner_w33_quadratic_bridge_insert")==1
    assert "W33_CURRENT_FRONTIER_MANIFEST" not in legacy
    assert "WDDPassFourEightSixFivePacketLoaded" in insert
    assert "WDDPassFourEightSevenZeroLoaded" in quad
    for wrapper in ("w33_paper.tex","photonic_holonet.tex","holonet_machine_blueprint.tex"):
        assert "W33_CURRENT_FRONTIER_MANIFEST" in (ROOT/wrapper).read_text()
