from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "bt2820_2824_blueprint_truth_gate.py"
INSERT = ROOT / "analysis" / "BT2820_BT2824_blueprint_evidence_insert.tex"
OPERATING = ROOT / "data" / "PART_BT2821_M36_DISTILLATION_OPERATING_CURVE_results.json"
SUPPORT = ROOT / "data" / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"


def module():
    spec = importlib.util.spec_from_file_location("bt2820_2824", SCRIPT)
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
    assert len(checks) == 20
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]


def test_distillation_and_evidence_boundaries_are_both_present():
    mod = module()
    source = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    migrated = mod.upgrade(source)
    combined = migrated + "\n" + INSERT.read_text(encoding="utf-8")
    assert "exactly $48$ improving branches" in combined
    assert "p'=R(p)" in combined
    assert "fault-tolerant injection" in combined
    assert "not a measured Holonet" in migrated
    assert "two-copy no-go" not in migrated
    assert "does \\emph{not} supply a distillation protocol" not in migrated


def test_support_first_codec_is_exact_and_bounded():
    data = json.loads(SUPPORT.read_text(encoding="utf-8"))
    insert = INSERT.read_text(encoding="utf-8")
    assert data["status"] == "COMPLETE_EXACT"
    assert data["check_count"] == 43 and all(data["checks"].values())
    assert data["support_lift"]["tomotope_f_vector"] == [4, 12, 16, 8]
    assert data["selector_bridge"]["face_pairing_chart_count"] == 12
    assert "not by itself an" in insert
    assert "objectwise intertwiner" in insert


def test_operating_curve_certificate():
    data = json.loads(OPERATING.read_text(encoding="utf-8"))
    assert data["status"] == "EXACT_ONE_ROUND_DYNAMICS"
    assert data["fixed_points"] == ["0", "2/3", "1"]
    assert data["local_slopes"] == {"0": "2/3", "2/3": "6/5", "1": "2/3"}
    assert data["rational_samples"][0]["p_out"] == "7/15"
    assert data["rational_samples"][0]["accepted_outputs_per_input"] == "5/32"
    assert data["check_count"] == 11 and all(data["checks"].values())


def test_namespace_was_reserved_on_master():
    reservation = json.loads(
        (ROOT / "data" / "w33_pass_namespace_registry_v2.d" / "2820-2824.json").read_text()
    )
    assert reservation["range"] == "2820-2824"
    assert reservation["reserved_after"] == "canonical Pass 2808 PG(3,2) tetrahedral support lift"
    assert sorted(reservation["passes"]) == ["2820", "2821", "2822", "2823", "2824"]
