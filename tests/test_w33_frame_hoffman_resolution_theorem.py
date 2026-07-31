from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "analysis" / "w33_frame_hoffman_resolution_theorem.py"
SPEC = spec_from_file_location("w33_frame_hoffman_resolution_theorem", MODULE_PATH)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_exact_frame_hoffman_resolution_theorem():
    result = MODULE.verify()
    assert all(result["checks"].values())
    assert result["frame_graph"]["spectrum"] == {
        "32": 1,
        "14": 44,
        "8": 15,
        "4": 81,
        "2": 84,
        "-4": 315,
    }
    assert result["hoffman"]["chromatic_lower_bound"] == 9
    assert result["hoffman"]["independence_upper_bound"] == 60
    assert result["incidence"]["rank_Q"] == 225
