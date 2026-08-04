from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bt3205", ROOT / "analysis" / "bt3205_3211_chromatic_closure.py"
)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


def test_exact_structural_certificate():
    data = MOD.certificate()
    assert data["status"] == "PASS_EXACT_STRUCTURAL_REDUCTION_WITHOUT_TEN_COLOR_DECISION"
    assert all(data["checks"].values())
    assert data["pass3205_defect_gram_outer_quotient"]["sorted_deficit_profiles"] == 195490
    assert data["pass3206_proof_solver"]["variables"] == 7800
    assert data["pass3206_proof_solver"]["clauses"] == 146289
    assert data["pass3208_p_adic"]["support_incidence_smith_diagonal"] == {"1": 44, "3": 1}


def test_fail_closed_model_checker_rejects_known_eleven_coloring():
    colors = MOD.load_coloring11().tolist()
    verdict = MOD.verify_ten_coloring(colors)
    assert not verdict["valid"]
    assert not verdict["checks"]["colors_0_to_9"]
