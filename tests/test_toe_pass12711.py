"""Pass 12711 (exploration)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "data", "explore_pass12711_ternary_noise.json")))


def test_noise_threshold():
    assert 6 < D["noisy_radix"]["ternary_beats_binary_from_snr"] < 12
    assert D["noisy_radix"]["best_cost_r"][0] == 2 and D["noisy_radix"]["best_cost_r"][-1] == 3


def test_mixed_cost():
    b = D["noisy_radix"]["best_mixed_cost"]
    assert max(b["0.1"].values()) >= 7 and max(b["1.0"].values()) == 3


def test_weights():
    w = D["weights"]
    assert abs(w["2"]["D"] - 0.3634) < 2e-3 and abs(w["3"]["D"] - 0.1902) < 2e-3
    p0 = w["3"]["probs"][1]
    assert 0.44 < p0 < 0.48
    assert w["3"]["SQNR_dB_per_entropy_bit"] - w["2"]["SQNR_dB_per_entropy_bit"] < 0.5
