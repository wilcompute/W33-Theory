from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "bt2808_2812_blueprint_truth_gate.py"
INSERT = ROOT / "analysis" / "BT2808_BT2812_blueprint_evidence_insert.tex"


def module():
    spec = importlib.util.spec_from_file_location("bt2808_2812", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_migration_is_idempotent_and_complete():
    mod = module()
    source = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    migrated = mod.upgrade(source)
    assert mod.upgrade(migrated) == migrated
    checks = mod.truth_checks(migrated)
    assert len(checks) == 16
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]


def test_distillation_and_evidence_boundaries_are_both_present():
    mod = module()
    source = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    migrated = mod.upgrade(source)
    combined = migrated + "\n" + INSERT.read_text(encoding="utf-8")
    assert "exactly $48$ improving branches" in combined
    assert "improves for $0<p<2/3$" in combined
    assert "fault-tolerant injection" in combined
    assert "not a measured Holonet" in migrated
    assert "two-copy no-go" not in migrated
    assert "does \\emph{not} supply a distillation protocol" not in migrated


def test_pass_stack_is_collision_free_and_explicit():
    reservation = json.loads(
        (ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2808-2812.json").read_text()
    )
    assert reservation["range"] == "2808-2812"
    assert reservation["stacked_on"] == "PR #207 / Passes 2803-2807"
    assert sorted(reservation["passes"]) == ["2808", "2809", "2810", "2811", "2812"]
