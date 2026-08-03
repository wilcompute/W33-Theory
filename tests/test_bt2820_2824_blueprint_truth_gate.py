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


def test_modular_wrapper_and_parts_are_exact():
    mod = module()
    wrapper = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    assert wrapper == mod.WRAPPER
    assert mod.upgrade(wrapper) == wrapper
    texts, assembled = mod.read_parts()
    assert len(texts) == 6
    assert all(texts)
    assert assembled.count("\\begin{document}") == 1
    assert assembled.count("\\end{document}") == 1
    assert [path.name for path in mod.PARTS] == [f"part_{i:02d}.tex" for i in range(6)]


def test_truth_gate_is_complete_and_rejects_stale_m36_text():
    mod = module()
    wrapper = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    checks = mod.truth_checks(wrapper)
    assert len(checks) == 25
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]
    _, assembled = mod.read_parts()
    assert "Exactly $48$ deep-grade branches improve fidelity" in assembled
    assert "p'=\\frac{p(4-p)}{3(p^2-2p+2)}" in assembled
    assert "No distillation protocol for $M_{36}$ is known" not in assembled


def test_distillation_and_evidence_boundaries_are_both_present():
    mod = module()
    _, assembled = mod.read_parts()
    combined = assembled + "\n" + INSERT.read_text(encoding="utf-8")
    assert "exactly $48$ improving branches" in combined
    assert "p'=R(p)" in combined
    assert "fault-tolerant injection" in combined
    assert "not a measured\nHolonet" in assembled or "not a measured Holonet" in " ".join(assembled.split())


def test_certificate_hashes_every_source_fragment():
    mod = module()
    wrapper = (ROOT / "holonet_machine_blueprint.tex").read_text(encoding="utf-8")
    payload = mod.build_payload(wrapper, mod.truth_checks(wrapper))
    assert payload["status"] == "PASS"
    assert payload["check_count"] == 25
    assert list(payload["part_sha256"]) == [str(path.relative_to(ROOT)) for path in mod.PARTS]
    assert len(set(payload["part_sha256"].values())) == 6


def test_support_first_codec_is_exact_and_bounded():
    data = json.loads(SUPPORT.read_text(encoding="utf-8"))
    insert = INSERT.read_text(encoding="utf-8")
    assert data["status"] == "COMPLETE_EXACT"
    assert data["check_count"] == 43 and all(data["checks"].values())
    assert data["support_lift"]["tomotope_f_vector"] == [4, 12, 16, 8]
    assert data["selector_bridge"]["face_pairing_chart_count"] == 12
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
