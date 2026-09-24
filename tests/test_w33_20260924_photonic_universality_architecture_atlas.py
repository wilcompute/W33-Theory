import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_20260924_photonic_universality_architecture_atlas.py"


def load_module():
    spec = importlib.util.spec_from_file_location("atlas10942", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_six_resource_models_are_kept_distinct():
    mod = load_module()
    ids = [a["id"] for a in mod.architectures]
    assert len(ids) == len(set(ids)) == 6
    assert "ADQC_FLYING_QUTRIT_HEAD" in ids
    assert "ONE_PARTICLE_MODE_REGISTER" in ids


def test_terminology_firewall_separates_single_resource_claims():
    out = load_module().out
    f = out["terminology_firewall"]
    assert len(set(f.values())) == len(f)
    assert "one photon" in f["single_photon_register"]


def test_primary_architecture_moves_scale_into_memories():
    out = load_module().out
    decision = out["holonet_decision"]
    assert decision["new_primary_architecture"] == "ADQC_FLYING_QUTRIT_HEAD"
    assert "scalable tensor-product memory" in decision["discard"]
    assert "81-state Pauli-frame controller" in decision["retain"]
    adqc = next(a for a in out["architectures"] if a["id"] == "ADQC_FLYING_QUTRIT_HEAD")
    assert adqc["quantum_memory"] == "stationary qutrit nodes"
    assert "measurement basis" in adqc["program_surface"]


def test_single_particle_mode_register_carries_scaling_warning():
    out = load_module().out
    mode = next(a for a in out["architectures"] if a["id"] == "ONE_PARTICLE_MODE_REGISTER")
    assert "3^n" in mode["scaling"]
    assert "rejected as scalable memory" in mode["holonet_fit"]
