"""Independent Clifford/Q8 and mixed-state collision-identity regression."""
import importlib.util
from pathlib import Path

def test_three_q8_cosets_and_unitary_second_design():
    file = Path(__file__).resolve().parents[1] / "analysis" / "w33_20261109_q8_design_purity.py"
    spec = importlib.util.spec_from_file_location("w33_q8_design", file)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    cert = obj.main()
    assert cert["SL2_3_order"] == 24
    assert cert["Q8_order"] == 8
    assert cert["Q8_coset_count"] == 3
    assert cert["maximal_eight_cliques_equal_Q8_cosets"]
    assert cert["maximal_clique_sizes"] == {5:144, 6:24, 8:3}
    assert all(row["frame_potential_2"] == 2.0 for row in cert["family_checks"])
    assert all(row["max_collision_purity_error"] < 2e-11 for row in cert["family_checks"])
