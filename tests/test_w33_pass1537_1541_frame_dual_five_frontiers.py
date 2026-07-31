from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1537_1541_frame_dual_five_frontiers.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pass1537_1541", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_five_frontiers_exact_core():
    module = load_module()
    payload = module.certificate(max_layer=4, decoder_trials=20)
    assert payload["status"] == "PASS"
    assert all(payload["checks"].values())
    assert payload["pass1537_modular_intertwiners"]["mod2_module"] == "absolutely irreducible 14"
    assert payload["pass1537_modular_intertwiners"]["mod3_module"] == "1 direct-sum absolutely irreducible 14"
    assert payload["pass1538_integral_ternary_lift"]["Smith_normal_form_K"] == {"1": 44, "3": 1}
    assert payload["pass1538_integral_ternary_lift"]["oriented_lift"]["rank"] == 30
    assert payload["pass1539_resolution_cuts"]["GF2_rank"]["global_new"] == 240
    assert payload["pass1540_weight_enumerator_programme"]["exact_weight_identity"] == "w(X)=16|X|-2e(X)+4t(X)"
    assert payload["pass1541_decoder_falsifier"]["exact_decoder"]["weight2_conditional_unique_fraction"] == "212/239"
