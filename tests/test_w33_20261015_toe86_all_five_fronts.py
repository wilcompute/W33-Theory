"""Exact regression tests for TOE86's five independent research fronts."""
from functools import lru_cache
import json
from pathlib import Path
import pytest

from analysis import w33_20261015_toe86_geometry_integral_routing as G
from analysis import w33_20261015_toe86_hom_intertwiners as I
from analysis import w33_20261015_toe86_qutrit_temporal_null as T
from analysis import w33_20261015_toe86_pair_polarization as P
from analysis import w33_20261015_toe86_pair_integral as S

ROOT=Path(__file__).resolve().parents[1]

@lru_cache(maxsize=None)
def fresh(track):
    return {"geometry":G.certificate,
            "hom":I.certificate,
            "temporal":T.certificate,
            "polarization":P.calculate,
            "pair_integral":S.certificate}[track]()

def test_468_pair_census_full_normalizer():
    c=fresh("geometry")["orbit_pair_census"]
    assert c["all_pairs_tested"]==780
    assert c["covering_admissible_pair_count"]==468
    assert c["native_normalizer_point_stabilizer_order"]==48
    assert c["total_normalizer_order"]==1296
    assert c["equivalence_class_count"]==13
    assert c["all_pair_face_rank_F2_distribution"]=={"83":36,"95":72,"97":360}
    assert sum(x["size"] for x in c["classes"])==468

def test_integral_homology_exact_snf_all_classes():
    x=fresh("geometry")["integral_smith"]
    assert x["rank_over_Q"]==83
    assert x["torsion_invariant_factors"]==[]
    assert x["H1_integral_free_rank"]==26
    assert x["H2_integral_free_rank"]==16
    a=fresh("pair_integral")
    assert a["pairs_classified"]==468
    assert a["class_count"]==13
    assert a["torsion_pattern_pair_counts"]=={
        "[]":36,"[3, 3]":360,"[6, 6]":72}
    assert all(x["H1_free_rank_Z"] == 109-x["rational_rank"]
               for x in a["classes"])

def test_shared_direction_over_every_equivalence_class():
    x=fresh("polarization")
    assert x["checked_full_normalizer_classes"]==13
    assert x["pairs_covered_by_equivariance"]==468
    assert x["matching_H1_H2_min_direction_pairs"]==468
    assert x["rank_F3_pair_count_by_equivalence"]=={"83":36,"95":432}
    assert all(len(cls["minimum_H1_direction_indices"])==1
               and cls["identical_min_direction_sets"] for cls in
               x["class_representative_signatures"])

def test_intertwiner_rigor_full_group_verification():
    x=fresh("hom")
    assert x["logical_H1_dimension"]==26
    assert x["face_relation_H2_dimension"]==16
    assert x["constraint_rows"]==832
    a=x["hom_H2_to_H1"]
    assert a["rank"]==396
    assert a["nullity"]==20
    assert len(a["example_intertwiner_support"])==9

def test_ideal_clifford_exact_permutation_and_linear_routing():
    x=fresh("geometry")["encoded_clifford_permutation_compiler"]
    a=x["compiled_generators"]
    assert len(a)==3
    assert [u["unrestricted_SWAP_count_optimal"] for u in a]==[90]*3
    assert [u["linear_nearest_neighbor_SWAP_count_optimal"] for u in a]==[
        4740,1828,498]
    assert [u["linear_odd_even_SWAP_layers"] for u in a]==[120,65,24]
    assert [u["local_qutrit_inversion_count"] for u in a]==[54,30,18]
    assert all(u["signed_order_three_verified"] for u in a)

def test_temporal_cptp_chosen_null_and_exact_binomial_design():
    x=fresh("temporal")
    null,alt,coherent=x["settings"]
    assert null["normalized_Choi_partial_transpose_negativity"]==0
    assert alt["normalized_Choi_partial_transpose_negativity"]==pytest.approx(.25,abs=1e-12)
    assert coherent["normalized_Choi_partial_transpose_negativity"]==pytest.approx(1,abs=1e-12)
    assert null["clock_superposition_revival_probability"]==pytest.approx(1/3,abs=1e-12)
    assert alt["clock_superposition_revival_probability"]==pytest.approx(.5,abs=1e-12)
    d=x["pre_registered_binomial_design"]
    assert d["n_shots"]==256 and d["success_threshold_inclusive"]==110
    assert d["exact_null_tail_probability"]<.001
    assert d["exact_alternative_detection_power"]>.98

@pytest.mark.parametrize("track,file",[
 ("geometry","w33_20261015_toe86_geometry_integral_routing.json"),
 ("hom","w33_20261015_toe86_hom_intertwiners.json"),
 ("polarization","w33_20261015_toe86_pair_polarization.json"),
 ("pair_integral","w33_20261015_toe86_pair_integral.json")
])
def test_frozen_exact_certificates(track,file):
    frozen=json.loads((ROOT/"data"/file).read_text(encoding="utf-8"))
    assert fresh(track)==frozen
