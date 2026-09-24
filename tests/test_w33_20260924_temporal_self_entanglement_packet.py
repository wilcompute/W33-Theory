import functools
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "analysis/w33_20260924_bell_shell_quadratic_history_intertwiner.py",
    "analysis/w33_20260924_bell_shell_quadratic_clifford_programs.py",
    "analysis/w33_20260924_temporal_quantum_memory_witness.py",
    "analysis/w33_20260924_modular_a2_event_clock.py",
    "analysis/w33_20260924_complex_temporal_holonomy.py",
]


@functools.lru_cache(maxsize=1)
def run_packet():
    for rel in SCRIPTS:
        subprocess.run([sys.executable, str(ROOT / rel)], cwd=ROOT, check=True,
                       capture_output=True, text=True)


def load(name):
    run_packet()
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))
def test_bell_shell_is_equivariant_quadratic_history_space():
    d = load("w33_20260924_bell_shell_quadratic_history_intertwiner.json")
    assert d["status"] == "PASS_BELL_SHELL_QUADRATIC_HISTORY_INTERTWINER"
    assert d["intertwiner"]["Q_torsor_to_sym2"] == [[0,1,0],[0,0,1],[1,0,0]]
    assert d["checks"]["Bell_stabilizer_order"] == 648
    assert d["checks"]["translation_kernel_order"] == 27
    assert d["checks"]["orbit_census_1_8_6_12"] == [1,8,6,12]


def test_27_histories_are_quadratic_clifford_programs():
    d = load("w33_20260924_bell_shell_quadratic_clifford_programs.json")
    assert d["status"] == "PASS_27_BELL_SHELL_QUADRATIC_CLIFFORD_PROGRAMS"
    assert d["checks"]["history_contexts"] == 27
    assert d["checks"]["distinct_symmetric_matrices"] == 27
    assert d["checks"]["max_additive_group_error"] < 3e-12
    assert d["checks"]["max_projective_pauli_conjugation_error"] < 3e-12
    assert d["checks"]["all_shears_symplectic"] is True
def test_reference_entanglement_separates_coherent_from_label_memory():
    d = load("w33_20260924_temporal_quantum_memory_witness.json")
    assert d["status"] == "PASS_REFERENCE_ENTANGLEMENT_TEMPORAL_MEMORY_WITNESS"
    assert abs(d["coherent_memory"]["negativity"] - 1) < 3e-12
    assert abs(d["classical_label_memory"]["negativity"]) < 3e-12
    assert abs(d["classical_label_memory"]["bell_fidelity"] - 1/3) < 3e-12
    assert d["depolarizing_memory"]["recovered_channel_entanglement_breaking_boundary"] == "p=3/4"
    assert "not a necessary-and-sufficient" in d["process_tensor_boundary"]


def test_modular_A2_event_clock_separates_change_and_arrow():
    d = load("w33_20260924_modular_a2_event_clock.json")
    assert d["status"] == "PASS_MODULAR_A2_RELATIONAL_EVENT_CLOCK"
    assert d["A2_weyl_bridge"]["exact_relation"] == "M01^T=S1 and M12^T=S2"
    assert d["A2_weyl_bridge"]["group_order"] == 6
    assert d["relational_history"]["stationarity_error"] == 0
    assert d["event_time"]["idle_three_updates"] == 0
    assert d["event_time"]["closed_three_state_cycle"] > 4.7
    assert d["arrow"]["equilibrium_cycle_affinity"] == 0
    assert d["arrow"]["biased_two_to_one_cycle_affinity"] > 2
def test_complex_temporal_holonomy_has_global_flat_phase_sector():
    d = load("w33_20260924_complex_temporal_holonomy.json")
    assert d["status"] == "PASS_COMPLEX_TEMPORAL_HOLONOMY_SEPARATION"
    c = d["known_chain_complex_crosscheck"]
    assert (c["graph_cycle_dimension"],c["triangle_boundary_rank"],c["H1_dimension"]) == (201,120,81)
    t = d["topological_phase_sector"]
    assert t["triangle_flat"] is True
    assert t["not_a_vertex_gradient"] is True
    assert t["gauge_shift_preserves_all_cycle_periods"] is True
    assert t["nonzero_periods_on_deterministic_201_cycle_basis"] > 0
    b = d["complex_connection"]["benchmarks"]
    assert b["coherent_only"]["real_cycle_holonomy"] == 0
    assert b["coherent_only"]["phase_cycle_holonomy"] != 0
    assert b["affinity_only"]["real_cycle_holonomy"] != 0
    assert b["affinity_only"]["phase_cycle_holonomy"] == 0
