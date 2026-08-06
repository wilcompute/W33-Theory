import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis" / "w33_pass3989_3996_wigner_smith_causal_memory.py"
FROZEN = ROOT / "data" / "PART_3993_3996_WIGNER_SMITH_CAUSAL_MEMORY.json"


def load_module():
    spec = importlib.util.spec_from_file_location("pass3993_memory", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_wigner_smith_certificate_matches_frozen():
    module = load_module()
    assert module.build() == json.loads(FROZEN.read_text(encoding="utf-8"))


def test_delay_spectrum_and_self_similar_moments():
    data = json.loads(FROZEN.read_text(encoding="utf-8"))
    theorem = data["wigner_smith_theorem"]
    assert theorem["proper_delay_sectors_in_units_of_theta_prime"] == {"0":1,"10":24,"16":15}
    assert theorem["mean_delay_in_units_of_theta_prime"] == 12
    assert theorem["delay_variance_in_units_of_theta_prime_squared"] == 12
    shells = data["self_similar_delay_shells"]["multiplicities_m1_to_m4"]
    for m, distribution in shells.items():
        m_int = int(m)
        total = sum(distribution.values())
        mean = sum(int(delay)*mult for delay, mult in distribution.items()) / total
        variance = sum((int(delay)-mean)**2*mult for delay, mult in distribution.items()) / total
        assert total == 40**m_int
        assert mean == 12*m_int
        assert variance == 12*m_int
