import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3989_3996_maximum_code_orbit_census.py"
FROZEN = ROOT / "data" / "PART_3989_MAXIMUM_CODE_ORBIT_CENSUS.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass3989_census", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_complete_maximum_code_census_matches_frozen():
    module = load_module()
    assert module.build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_three_orbits_and_stabilizers():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    assert data["maximum_cliques_total"] == 945
    assert [x["orbit_size"] for x in data["maximum_clique_orbits"]] == [540, 270, 135]
    assert [x["stabilizer_order"] for x in data["maximum_clique_orbits"]] == [96, 192, 384]
    assert all(x["intersection_two_component_parameters"] == [[45,16,8,4],[6,4,2,4],[6,4,2,4]] for x in data["maximum_clique_orbits"])
