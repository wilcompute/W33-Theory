from PART_CXLI_HEAVY_THRESHOLD_LOG_MATCH import (
    PHI3,
    PHI6,
    half_log_catalog_matches,
    heavy_threshold_log_match_audit,
    primitive_threshold_templates,
)


def test_primitive_templates_pin_k3_at_ppm_scale():
    templates = {t.label: t for t in primitive_threshold_templates()}
    assert abs(templates["24/13 primitive sqrt(mu/Phi6)"].relative_k3_error_ppm) < 10
    assert abs(templates["13/7 primitive sqrt((k-1)/q)"].relative_k3_error_ppm) < 20


def test_primitive_template_signs_match_required_thresholds():
    templates = {t.label: t for t in primitive_threshold_templates()}
    assert templates["24/13 primitive sqrt(mu/Phi6)"].delta_gut_template < 0
    assert templates["13/7 primitive sqrt((k-1)/q)"].delta_gut_template > 0


def test_catalog_scanner_finds_alpha_integer_over_edge_count_for_24_over_13():
    rows = half_log_catalog_matches(24 / 13, max_results=3)
    formulas = {r["formula"] for r in rows}
    assert "1/2 log(alpha_integer/E)" in formulas


def test_catalog_scanner_finds_37_over_10_for_13_over_7():
    rows = half_log_catalog_matches(PHI3 / PHI6, max_results=3)
    formulas = {r["formula"] for r in rows}
    assert "1/2 log(v-mu+1/Phi4)" in formulas
    assert "1/2 log(k-1/q)" in formulas


def test_audit_contains_primitive_and_best_templates():
    audit = heavy_threshold_log_match_audit()
    assert len(audit["primitive_templates"]) == 2
    assert len(audit["best_catalog_templates"]) == 2
    assert "k3_24_over_13" in audit["scanner_top_matches"]
    assert "k3_13_over_7" in audit["scanner_top_matches"]


def test_loop_unit_is_one_loop_scale():
    audit = heavy_threshold_log_match_audit()
    loop_unit = audit["inputs"]["loop_unit_alpha_over_2pi"]
    assert 0.006 < loop_unit < 0.007
