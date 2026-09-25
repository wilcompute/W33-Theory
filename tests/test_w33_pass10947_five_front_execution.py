import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / "analysis/w33_pass10947_five_front_execution.py"
CERT = ROOT / "data/w33_pass10947_five_front_execution.json"


def load():
    return json.loads(CERT.read_text(encoding="utf-8"))


def test_producer_replays():
    subprocess.run(
        [sys.executable, str(PRODUCER)], cwd=ROOT, check=True,
        capture_output=True, text=True, timeout=45,
    )


def test_cubic_vm_microcode_is_exact_and_routed():
    x = load()["front1_cubic_VM_microcode"]
    assert x["parallel_depth"] == 7
    assert x["primitive_counts"]["total"] == 10
    assert x["clean_ancillas"] == 2
    assert x["ancillas_returned_to_zero"] is True
    assert x["VM_P7_pair_edges_used"] == [[0, 1]]
    assert x["VM_bridge_generator_used"] is False
    assert len(x["truth_table"]) == 9


def test_encoded_factories_and_malignant_triples():
    x = load()["front2_verified_Golay_factories"]
    assert x["encoded_states"]["logical_coset_sizes"] == [243, 243, 243]
    assert x["encoded_states"]["X_and_Z_stabilizer_checks"] == 7290
    assert x["factory"]["extended_locations"] == 552
    assert x["factory"]["accepted_late_hazard_locations"] == 279
    m = x["malignant_triples"]
    assert m["candidate_late_hazard_triples_enumerated"] == 3580779
    assert m["malignant_distinct_coordinate_triples"] == 2576205
    assert abs(m["conservative_bound_crosses_physical_p_at"] - 0.000531703523611593) < 1e-15


def test_quotient_projector_centralizer():
    x = load()["front3_quotient_centralizer"]
    assert x["channel_dimensions"] == [18, 18, 18]
    assert x["linear_commutants_over_Qomega"]["End_H27_Q_dimension"] == 162
    assert x["linear_commutants_over_Qomega"]["End_H27xC3_Q_dimension"] == 54
    assert x["discrete_carrier_group"]["order"] == 162
    assert x["parabolic_36_plus_18_projector"]["centralizer_order"] == 54


def test_sparse_router_and_projective_cubic_lift():
    router = load()["front4_M36_physical_router"]
    assert router["all_36_M36_rays_checked"] == 36
    assert router["optimization"]["star_active_counts_by_dark_mode"] == [1, 1, 1, 0]
    assert router["optimization"]["winner"] == "star crossbar"
    assert len(router["family_program_table"]) == 4

    lift = load()["front5_coloring_cubic_compatibility"]
    assert lift["coloring_group"]["order"] == 108
    assert lift["cubic_support_lift"]["order"] == 324
    assert lift["cubic_support_lift"]["three_support_lifts_per_coloring_operation"] is True
    assert lift["signed_cubic_lift"]["diagonal_sign_lifts_per_support_permutation"] == 64
    assert lift["signed_cubic_lift"]["full_monomial_signed_lift_order"] == 20736
    assert lift["non_split_firewall"]["order108_strict_section_exists"] is False


def test_visible_surfaces_are_unique():
    docs = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text(encoding="utf-8")
    assert docs.count('id="pass10947-cubic-vm-golay-router-extension"') == 1
    assert tail.count("PASS10947_FIVE_FRONT_EXECUTION_INSERT") == 1
