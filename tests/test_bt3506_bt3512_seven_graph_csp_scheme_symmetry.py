from analysis.bt3506_3512_seven_graph_csp_scheme_symmetry import build_certificate
from analysis.bt3506_m57_permutation_csp import model_statistics


EXPECTED_SHA = "15ab9b21e744e755917e0b4c40ec806b43c5463b8a11cfbfac7bdbb4a9c8dfe7"


def test_seven_front_certificate():
    result = build_certificate()
    assert result["status"] == "PASS_7_FRONTS"
    assert result["semantic_sha256"] == EXPECTED_SHA

    stats = result["front_3506_m57_csp"]
    assert stats["independent_permutation_entries"] == 86240
    assert stats["CP_SAT_directed_integer_variables_with_explicit_inverses"] == 172480
    assert stats["one_hot_boolean_baseline"] == 4743200
    assert stats["row_triples_for_curvature_separation"] == 27720

    descendants = result["front_3507_descendant_atlas"]
    assert descendants["Clebsch_to_Petersen"]["child_parameters"] == [10, 3, 0, 1]
    chain = descendants["Golay_Witt_chain"]
    assert chain["Higman_Sims"] == [100, 22, 0, 6]
    assert chain["HS_second_subconstituent"]["parameters"] == [77, 16, 0, 4]
    assert chain["M22_point_avoidance"]["parameters"] == [56, 10, 0, 2]

    scheme = result["front_3508_scheme_blindness"]
    assert scheme["all_parameter_spectral_absolute_krein_tests_pass"] is True
    assert scheme["rows"][1]["parameters"] == [57, 14, 1, 4]
    assert scheme["rows"][1]["krein"]["q11"] == ["38", "1273/49", "1140/49"]

    transplant = result["front_3509_spectral_transplant"]
    assert transplant["universal_reflection"].endswith("U^2=I")
    assert transplant["examples_coefficients_low_to_high"]["[0, 0, 1]"] == [-2, 8]

    firewall = result["front_3510_symmetry_firewall"]
    assert firewall["PSL2_19_order"] == 3420
    assert firewall["Borel_19_semidirect_9_order"] == 171

    curvature = result["front_3511_bonkers_nonabelian_curvature"]
    assert curvature["pair_matchings"] == {"count": 15, "cycle_type": "2^3"}
    assert curvature["triangle_holonomies"] == {"count": 20, "cycle_type": "2^3"}


def test_csp_exporter_counts_match_certificate():
    stats = model_statistics(56)
    assert stats["independent_permutation_entries"] == 86240
    assert stats["directed_integer_variables"] == 172480
    assert stats["one_hot_nonfixed_boolean_baseline"] == 4743200
    assert stats["row_triples"] == 27720
