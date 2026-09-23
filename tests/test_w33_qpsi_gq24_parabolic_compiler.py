from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_qpsi_gq24_parabolic_compiler.py"
DATA = ROOT / "data/w33_qpsi_gq24_parabolic_compiler.json"


def load_script():
    spec = importlib.util.spec_from_file_location("qpsi_gq24_compiler_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_certificate_is_exact_recomputation():
    recomputed = load_script().main(write=False)
    assert recomputed == json.loads(DATA.read_text())


def test_qpsi_clock_formula_parabolic_and_scope_are_frozen():
    out = json.loads(DATA.read_text())
    assert out["status"] == "PASS_QPSI_IS_AN_ANCHORED_GQ24_PARABOLIC_CLOCK"
    assert out["incidence_clock"]["formula"] == (
        "q_a(i) = 1 + 3*delta(a,i) - 3*A(a,i)"
    )
    assert out["incidence_clock"]["branching"] == "27 = 1_4 + 10_-2 + 16_1"
    assert out["cubic_neutrality"]["pattern_counts"] == {
        "(-2,-2,4)": 5,
        "(-2,1,1)": 40,
    }
    assert out["weyl_parabolic"]["W_E6_order"] == 51840
    assert out["weyl_parabolic"]["point_stabilizer_order"] == 1920
    assert out["weyl_parabolic"]["parabolic_type"] == "W(D5)"
    assert len(out["all_anchor_charts"]) == 27
    assert all(out["checks"].values())
    assert "does not physically select an anchor" in out["boundary"]
    obstruction = out["equivariant_compiler_obstruction"]
    assert obstruction["H27_maximum_rank"] == 9
    assert obstruction["H27_target_dimension"] == 27
    assert obstruction["K81_maximum_rank"] == 27
    assert obstruction["K81_target_dimension"] == 81
    assert obstruction["invertible_H27_equivariant_intertwiner_exists"] is False
    assert obstruction["invertible_K81_equivariant_compiler_exists"] is False
    assert "symmetry-changing" in obstruction["surviving_frontier"]
