"""Regression tests for PART CCCXCVI photonic life runtime architecture."""

from __future__ import annotations

import importlib.util
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXCVI_PHOTONIC_LIFE_RUNTIME_ARCHITECTURE.py"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("photonic_life_runtime_cccxcvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 45


def test_graph_two_graph_and_h1_counts():
    results = build_results()
    graph = results["graph_audit"]
    assert graph["points"] == 40
    assert graph["degree_values"] == [12]
    assert graph["edges"] == 240
    assert graph["triples_by_edge_count"] == {
        "0": 3240,
        "1": 4320,
        "2": 2160,
        "3": 160,
    }
    assert graph["odd_triples"] == 4480
    assert graph["direct_open_turns"] == 4320
    assert graph["beta1"] == 81


def test_incidence_gram_recovers_adjacency_coefficients():
    mod = load_module()
    graph = mod.graph_audit()
    assert graph["incidence_gram_diag_values"] == [336]
    assert graph["incidence_gram_adjacent_values"] == [20]
    assert graph["incidence_gram_nonadjacent_values"] == [16]
    assert mod.TWO_GRAPH_ADJ_COEFF == mod.MU == 4
    assert mod.INCIDENCE_GRAM_DIAG_COEFF == mod.E + 2 * mod.V == 320
    assert mod.INCIDENCE_GRAM_J_COEFF == mod.LAM**mod.MU == 16


def test_probabilistic_photonic_layer():
    results = build_results()
    probabilistic = results["probabilistic_layer"]
    assert probabilistic["p_fusion"] == "1/2"
    assert probabilistic["p_klm"] == "1/4"
    assert probabilistic["expected_fusion_attempts"] == 480
    assert probabilistic["expected_klm_attempts"] == 960
    assert probabilistic["critical_edge_split"] == "120+120"


def test_deterministic_and_classical_layers():
    results = build_results()
    deterministic = results["deterministic_layer"]
    classical = results["classical_layer"]
    assert deterministic["full_stabilizer_weight"] == 13
    assert deterministic["critical_stabilizer_weight"] == 7
    assert deterministic["pauli_frame_states"] == 81
    assert deterministic["projective_pauli_frames"] == 40
    assert classical["measurement_word_trits"] == 40
    assert classical["exact_word_bound"] == "2^63 < 3^40 < 2^64"
    assert classical["directed_environment_fanout"] == 480


def test_topological_toric_minimal_triangulation_layer():
    results = build_results()
    topo = results["topological_layer"]
    assert topo["toric_logical_qubits"] == 2
    assert topo["toric_ground_state_degeneracy"] == 4
    assert topo["csaszar"] == {"vertices": 7, "edges": 21, "faces": 14, "genus": 1}
    assert topo["heawood_oscillator"]["vertices"] == 14
    assert topo["heawood_oscillator"]["cycle_rank"] == 8
    assert topo["heawood_oscillator"]["frequency_squared"] == 2
    assert topo["heawood_oscillator"]["branch_size"] == 6


def test_response_pipeline_open_closed_ratio():
    results = build_results()
    pipeline = results["response_pipeline"]
    assert pipeline["odd_triples"] == 4480
    assert pipeline["open_turns"] == 4320
    assert pipeline["closed_triangles"] == 160
    assert pipeline["open_to_closed_ratio"] == 27
    assert pipeline["incidence_gram"] == "M M^T = 320 I + 16 J + 4 A"
    assert pipeline["h1_beta1"] == 81
    assert pipeline["z3_terms_checked"] == 8347
    assert pipeline["g1g2_pairs"] == 81 * 81
    assert pipeline["g1g1_nonzero_brackets"] == 810
    assert pipeline["actual_z3_path"] == "artifacts/verify_e8_z3grading_from_structure_constants.json"


def test_imported_e8_operation_pipeline_artifacts():
    results = build_results()
    audit = results["e8_operation_audit"]
    assert audit["h1_complete_certificate"] is True
    assert audit["h1_free_rank"] == 81
    assert audit["h1_rank_Q"] == 120
    assert audit["h1_unit_relations"] == 120
    assert audit["e8_dims"] == {"g0": 86, "g1": 81, "g2": 81, "total": 248}
    assert len(audit["grade_rules"]) == 6
    assert len(audit["bracket_gate_required_conditions"]) == 4
    assert audit["z3_verifier_present"] is True
    assert audit["z3_status"] == "ok"
    assert audit["z3_terms_checked"] == 8347
    assert audit["z3_grade_violations"] == 0
    assert audit["g1g2_status"] == "ok"
    assert audit["g1g2_pairs"] == 81 * 81
    assert audit["g1g2_cartan_outputs"] == 81
    assert audit["g1g1_status"] == "ok"
    assert audit["g1g1_nonzero_brackets"] == 810
    assert audit["g1g1_firewall_bad_couplings"] == 162


def test_runtime_regimes_are_separated():
    results = build_results()
    regimes = {layer["regime"] for layer in results["runtime_layers"]}
    assert {"quantum", "probabilistic", "deterministic", "classical", "topological", "response"} <= regimes
    names = {layer["name"] for layer in results["runtime_layers"]}
    assert {
        "two_qutrit_phase_space",
        "photonic_assembly",
        "mbqc_feedforward",
        "measurement_record",
        "topological_surface_code",
        "two_graph_response",
    } <= names


def test_docs_index_exposes_photonic_runtime_architecture():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Photonic Life Runtime Architecture" in text
    assert "8347" in text
    assert "40</code>-trit" in text
