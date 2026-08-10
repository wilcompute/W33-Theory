from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "analysis"))


def load():
    return json.loads((DATA / "w33_pass1345_1349_basic_mixed_selector_runtime_fusion.json").read_text(encoding="utf-8"))


def test_release_status_and_scope():
    data = load()
    assert data["status"] == "PASS_WITH_EXTERNAL_RUNTIME_BOUNDARY"
    assert all(data["checks"].values())


def test_modular_cartan_and_basic_dimensions():
    records = json.loads((DATA / "w33_pass1345_modular_basic_algebras.json").read_text(encoding="utf-8"))["records"]
    assert {p: records[p]["basic_algebra_dimension"] for p in records} == {"2": 23, "3": 26, "5": 15}
    for record in records.values():
        assert record["cartan_equals_D_transpose_D"]
        assert record["decomposition_rows_unique_from_trace_congruences"]


def test_ext_quivers_and_minimal_relations():
    records = json.loads((DATA / "w33_pass1345_modular_basic_algebras.json").read_text(encoding="utf-8"))["records"]
    assert records["2"]["quiver_and_associated_graded_relations"]["ext1_adjacency"] == [[0, 0], [0, 4]]
    assert records["3"]["quiver_and_associated_graded_relations"]["ext1_adjacency"] == [[1,0,1,0],[0,0,1,0],[1,1,1,0],[0,0,0,0]]
    counts = {
        p: {degree: len(relations) for degree, relations in records[p]["quiver_and_associated_graded_relations"]["minimal_relations"].items()}
        for p in records
    }
    assert counts == {"2": {"2": 12, "4": 3, "5": 1}, "3": {"2": 8, "3": 2, "4": 3}, "5": {"2": 4}}


def test_mixed_26x4_constants_and_closure():
    summary = load()["pass1346_mixed_hecke_triality"]
    manifest = json.loads((ROOT / summary["mixed_constants_file"]).read_text(encoding="utf-8"))
    assert summary["generated_algebra_dimension"] == 18
    assert summary["commutator_span_dimension"] == 8
    assert summary["mixed_denominator_lcm"] == 64
    assert manifest["logical_full_sha256"] == summary["mixed_constants_sha256"]
    assert len(manifest["left_chunks"]) == len(manifest["right_chunks"]) == 4
    left_rows=[]
    for info in manifest["left_chunks"]:
        chunk=json.loads((ROOT/info["path"]).read_text(encoding="utf-8"))
        left_rows.extend(chunk["rows"])
    assert len(left_rows)==26
    assert all(len(row)==4 and all(len(vector)==18 for vector in row) for row in left_rows)


def test_cycle_copy_observables_are_one_hot():
    manifest=json.loads((DATA/"w33_pass1347_cycle_copy_observables.json").read_text(encoding="utf-8"))
    records={length:json.loads((ROOT/info["path"]).read_text(encoding="utf-8"))["record"] for length,info in manifest["record_files"].items()}
    assert records["7"]["cosine_quadrature"]["basis_invariant_frobenius_energy"] == "131/3456"
    assert records["8"]["cosine_quadrature"]["basis_invariant_frobenius_energy"] == "5/144"
    for record in records.values():
        signatures = record["copy_energy_readout_signatures"]
        assert len(signatures) == 3
        for i, signature in enumerate(signatures):
            assert all((value != "0") == (j == i) for j, value in enumerate(signature))


def test_exact_rational_atlas_standard_model():
    record = load()["pass1348_runtime_closure"]["exact_rational_model"]
    assert record["standard_generator_orders"] == {"c": 2, "d": 9, "cd": 10}
    assert record["class_trace_vector"] == record["expected_character"]
    assert record["matrix_sha256"] == "8d0c52cf1f962471be1ab6dc4d98af5bc397fe003cbf9660a819ac0572689deb"


def test_runtime_ledger_is_fail_closed():
    observation = load()["pass1348_runtime_closure"]["observed_external_runtime"]
    assert observation["atlasrep_gap"]["status"] == "queued"
    assert observation["historical_manuscripts"]["photonic_holonet"]["compile_status"] == "PASS_WITH_TYPED_MISSING_INSERT_STUBS"
    assert observation["historical_manuscripts"]["w33_paper"]["compile_status"] == "CI_QUEUED_NOT_CLAIMED"


def test_modular_triality_mechanisms_are_distinct():
    data = load()["pass1349_modular_triality_fusion"]
    assert data["mixed_denominator_lcm"] == 64
    assert data["records"]["2"]["mixed_hecke_descent"] == "OBSTRUCTED"
    assert data["records"]["2"]["species20_transport_rank"] == 2
    assert data["records"]["3"]["species20_transport_rank"] == 3
    assert data["records"]["3"]["combined_radical_power_dimensions"] == [7, 2, 0]
    assert data["records"]["5"]["combined_radical_power_dimensions"] == [0]


def test_rebuild_killshot_figure_is_present_and_typed():
    text = (ROOT / "analysis" / "w33_killshot_dashboard_fig.tex").read_text(encoding="utf-8")
    assert "label{fig:killshot-dashboard}" in text


def test_certificate_files_exist():
    for name in [
        "w33_pass1345_modular_basic_algebras.json",
        "w33_pass1346_mixed_26x4_constants.json",
        "w33_pass1346_mixed_26x4_metadata.json",
        "w33_pass1346_left_mixed_constants_0.json",
        "w33_pass1346_right_mixed_constants_0.json",
        "w33_pass1347_cycle_copy_observables.json",
        "w33_pass1347_cycle_copy_observables_length7.json",
        "w33_pass1347_cycle_copy_observables_length8.json",
        "w33_pass1348_runtime_observation.json",
        "w33_pass1349_modular_triality_fusion.json",
        "w33_pass1348_manuscript_build_observation.json",
    ]:
        assert (DATA / name).exists()
