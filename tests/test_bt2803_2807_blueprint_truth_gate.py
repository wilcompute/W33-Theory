from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "bt2803_2807_blueprint_truth_gate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("bt2803_2807", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_migration_is_idempotent_and_complete():
    module = load_module()
    source = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    migrated = module.upgrade(source)
    assert module.upgrade(migrated) == migrated
    checks = module.truth_checks(migrated)
    assert len(checks) == 14
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]


def test_migration_removes_stale_promotion_language():
    module = load_module()
    source = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    migrated = module.upgrade(source)
    assert "its instruction set\nhas eight opcodes" not in migrated
    assert "complete only for identical two-copy binary" not in migrated
    assert "not a measured Holonet" in migrated
    assert "Arbitrary logical Clifford decoder gauges" in migrated


def test_namespace_reservation_matches_packet():
    import json

    reservation = json.loads(
        (ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2803-2807.json").read_text()
    )
    assert reservation["range"] == "2803-2807"
    assert sorted(reservation["passes"]) == ["2803", "2804", "2805", "2806", "2807"]
