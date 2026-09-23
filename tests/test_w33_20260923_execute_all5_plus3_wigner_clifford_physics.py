from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260923_execute_all5_plus3_wigner_clifford_physics.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_five_plus3_wigner_clifford", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_execute_all5_plus3_wigner_clifford_physics():
    m = load_module()
    out = m.main(write=False)
    assert out["status"] == "PASS_ALL_FIVE_PLUS_THREE_EXECUTED_WITH_EXACT_FINITE_BOUNDARIES"
    assert all(out["checks"].values())

    # 1. Wigner/reversible-quantum selection.
    assert out["next1"]["prime_checks"]["3"]["all_quantum_implementable_iff_p3"] is True
    assert out["next1"]["prime_checks"]["5"]["forbidden_count"] == 2

    # 2. Exact G25/qutrit matrix dictionary.
    assert out["next2"]["CHEVIE_parent_order"] == 648
    assert out["next2"]["same_generator_matrices_exact"] is True

    # 3. C2 reaches the exact E8 anti-linear Lie involution.
    assert out["next3"]["E8_action"]["J_squared"] == 1
    assert out["next3"]["E8_action"]["fixed_real_form"] == "E8(8), split real form"

    # 4. Character-mismatch action has unique zero at q=3.
    assert out["next4"]["closed_form"] == "S(q)=sum_{m in F_q^*} E(m)=2(q-3)"
    assert out["next4"]["cases"]["3"]["zero_action"] is True
    assert out["next4"]["cases"]["9"]["zero_action"] is False

    # 5. Prime-power completion including an explicit GF(9) Frobenius witness.
    assert out["next5"]["GF9_clock_identities_checked"] == 81
    assert out["next5"]["cases"]["3"]["saturated"] is True
    assert out["next5"]["cases"]["9"]["index"] == 4
    assert out["next5"]["cases"]["25"]["index"] == 12

    # Outside-box probes.
    assert out["outside1"]["doubled"]["cells"] == [80, 400, 400, 80]
    assert out["outside1"]["doubled"]["betti"] == [1, 81, 81, 1]
    assert out["outside2"]["order"] == 12
    assert out["outside2"]["exact_checks"]["U_F^12=I"] is True
    assert out["outside3"]["absolute_probability_contrast"] > 0.5
