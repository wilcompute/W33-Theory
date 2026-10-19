"""Exact W33 clique-census / Motzkin-Straus 4/7 regression."""
import importlib.util
import sys
from pathlib import Path


def test_tick_commutator_laplacian_and_extremum():
    root = Path(__file__).resolve().parents[1]
    folder = root / "analysis"
    sys.path.insert(0,str(folder))
    path = folder / "w33_20261019_tick_commutator_extremum.py"
    spec = importlib.util.spec_from_file_location("tick_commutator_extremum",path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.certify()
    assert result["all_checks_pass"]
    assert result["maximum_mutually_noncommuting_directions"] == 7
    assert result["maximal_clique_size_histogram"] == {4:90,7:2880}
    assert result["sharp_simplex_interaction_maximum"] == "4/7"
