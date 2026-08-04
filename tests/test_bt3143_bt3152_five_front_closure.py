import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "PART_BT3143_BT3150_FIVE_FRONT_CLOSURE_source_summary.json"
SCRIPT = ROOT / "analysis" / "bt3144_3150_sparse_sync_isa.py"
REGISTRY = ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "3143-3152.json"


def load_script():
    spec = importlib.util.spec_from_file_location("bt3144_3150", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_source_summary_boundaries_and_exact_counts():
    data = json.loads(SUMMARY.read_text())
    assert data["pass_3143"]["status"] == "NO_INPUTS_DISCOVERED"
    assert data["pass_3144"]["dynamic_sparse_factors"] == 3697
    assert data["pass_3144"]["next_action_matches"] == 32
    assert data["pass_3146"]["distinct_observation_phase_traces"] == 41641
    assert data["pass_3146"]["worst_received_symbols_to_relock"] == 4
    assert data["pass_3147"]["previous_18_collision_set_universal"] is False
    assert data["pass_3147"]["previous_18_collision_set_order"] == 243
    assert data["pass_3147"]["minimum_collisions_among_universal_sets"] == 36
    assert data["pass_3147"]["universal_four_generator_sets"] == 24
    assert data["pass_3147"]["current"]["diameter"] == 19
    assert data["pass_3147"]["alternative"]["diameter"] == 20
    assert 3.7419 < data["pass_3147"]["collision_to_instruction_cost_ratio_break_even"] < 3.7420


def test_sync_clean_words_and_group_arithmetic():
    m = load_script()
    words = [tuple(m.SYNC_PAIR[(p+i) % 12] for i in range(2)) for p in range(12)]
    assert len(set(words)) == 12
    for g in m.D4:
        assert m.mul(g, m.inv(g)) == m.ID
        assert m.mul(m.inv(g), g) == m.ID


def test_small_burst_enumerator_is_fail_closed():
    m = load_script()
    candidates = m.generate_burst_candidates(window=2, received=20, max_edits=2)
    delays = m.burst_relock(candidates, window=2, received=20)
    assert len(candidates) == 4681
    assert max(delays) == 4
    assert all(d is not None for d in delays)


def test_registry_preserves_claim_boundary():
    data = json.loads(REGISTRY.read_text())
    assert data["range"] == "3143-3152"
    assert data["owner"] == "agent/pass3143-3152-five-front-closure"
    assert "laboratory" in data["claim_boundary"]
