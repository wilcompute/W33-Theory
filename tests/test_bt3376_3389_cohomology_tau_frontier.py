from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_certificate_matches_frozen_json():
    module = load_module(
        ROOT / "analysis/bt3376_3389_cohomology_tau_frontier.py",
        "bt3376_3389_exact",
    )
    observed = module.build_certificate()
    frozen = json.loads(
        (ROOT / "data/PART_BT3376_BT3389_COHOMOLOGY_TAU_results.json").read_text(encoding="utf-8")
    )
    assert observed == frozen
    assert observed["status"] == "PASS"
    assert all(observed["checks"].values())


def test_load_bearing_invariants():
    module = load_module(
        ROOT / "analysis/bt3376_3389_cohomology_tau_frontier.py",
        "bt3376_3389_invariants",
    )
    result = module.build_certificate()["sections"]
    word = result["word_metric"]
    tau = result["tau_barycentric"]
    voltage = result["cohomology_voltage"]
    assert word["flat_space"]["diameter"] == 480
    assert word["cohomology_quotient"]["cayley_diameter_lower_bound"] == 389
    assert tau["Q15_barycenters"]["fiber_profile"] == {"size_1": 81, "size_2": 27}
    assert tau["barycentric_walk"]["three_shell_matrix"] == [[2, 8, 0], [2, 4, 4], [0, 4, 6]]
    assert tau["hidden_phase_sector"]["spectrum"] == {"-5": 2, "-2": 9, "1": 12, "4": 4}
    assert voltage["minimum_defect_equivariant_presentation"]["cohomology_rank"] == 2180
    assert voltage["minimum_defect_voltage_lift"]["connected_components"] == 81
    assert voltage["minimum_defect_voltage_lift"]["vertices_per_component"] == 135
    assert voltage["minimum_defect_voltage_lift"]["cubic_moment_deficit"] == 378


def test_manifest_is_recursive_unique_and_preserves_legacy_required_reachability():
    module = load_module(
        ROOT / "analysis/w33_pass5364_publication_dag_audit.py",
        "pass5364_publication_dag",
    )
    report = module.audit(require_index=False)
    assert report["status"] == "PASS"
    frontier = report["frontier"]
    assert frontier["manifest_node_count"] >= 2
    assert frontier["leaf_count"] == len(set(frontier["leaves"]))
    assert frontier["legacy_required_missing"] == []


def test_live_wrappers_use_one_generated_manifest():
    config = json.loads((ROOT / "data/w33_current_frontier_manifest_v1.json").read_text(encoding="utf-8"))
    marker = r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%"
    for wrapper_name, body_name in config["front_doors"].items():
        text = (ROOT / wrapper_name).read_text(encoding="utf-8")
        assert text.count(marker) == 1
        assert text.count(rf"\input{{{body_name}}}") == 1


def test_integrator_helpers_are_idempotent():
    module = load_module(ROOT / "tools/integrate_bt3376_bt3389.py", "bt3376_3389_integrator")
    required = ["analysis/A", "analysis/B"]
    wrapper = "\\AtBeginDocument{%\n  \\input{analysis/A}%\n  \\input{analysis/B}%\n}%\n\\input{body.tex}\n"
    once, mode = module.consolidate_wrapper(wrapper, required)
    twice, second_mode = module.consolidate_wrapper(once, required)
    assert mode == "consolidated_direct_inputs"
    assert second_mode == "already_consolidated"
    assert once == twice
    assert once.count(module.MANIFEST_INPUT) == 1

    html = "<main><p>x</p></main>"
    insert = '<section id="bt3376-3389-cohomology-tau-frontier">y</section>'
    once_html, html_mode = module.integrate_index(html, insert)
    twice_html, second_html_mode = module.integrate_index(once_html, insert)
    assert html_mode == "inserted"
    assert second_html_mode == "already_materialized"
    assert once_html == twice_html

    stale = '<main><section id="bt3376-3389-cohomology-tau-frontier">old</section></main>'
    updated, update_mode = module.integrate_index(stale, insert)
    stable, stable_mode = module.integrate_index(updated, insert)
    assert update_mode == "updated"
    assert stable_mode == "already_materialized"
    assert updated == stable
    assert ">old<" not in updated

    nested_old = (
        '<main><section id="bt3376-3389-cohomology-tau-frontier">'
        '<section>old nested</section></section><p>tail</p></main>'
    )
    nested_updated, nested_mode = module.integrate_index(nested_old, insert)
    assert nested_mode == "updated"
    assert "old nested" not in nested_updated
    assert "<p>tail</p>" in nested_updated

    config = json.loads((ROOT / "data/w33_current_frontier_manifest_v1.json").read_text())
    sections = module.configured_public_sections(config, ROOT)
    sources = {section["source"] for section in sections}
    keys = {(section["kind"], section["token"]) for section in sections}
    assert "analysis/BT3528_BT3534_borel_star_moore_functor_transplant_index_insert.html" in sources
    assert "analysis/PASS4544_4551_module_cubic_enumerator_zeta_index_insert.html" in sources
    assert ("marker", "<!-- BT3418-BT3429-CLEBSCH-D5-SUPPLEMENT -->") in keys
    assert ("id", "pass4579-4586-o8plus-exceptional") in keys
    assert ("id", "pass4624-4631-packet-incidence-f4") in keys


def test_source_insert_and_auditor_exist():
    assert (ROOT / "analysis/BT3387_cohomology_tau_frontier_insert.tex").is_file()
    assert (ROOT / "analysis/BT3387_cohomology_tau_frontier_index_insert.html").is_file()
    assert (ROOT / "tools/audit_w33_current_frontier.py").is_file()
    assert (ROOT / "analysis/w33_pass5364_publication_dag_audit.py").is_file()
