from __future__ import annotations

from exploration.w33_tomotope_klitzing_six_table_lock import parse_klitzing_html


def test_parse_six_table_lock_on_minimal_fixture() -> None:
    text = (
        "<html><body>"
        "<table><tr><td>GC( x3o3o *b4o )</td></tr><tr><td>(partial a)</td></tr><tr><td>(partial b)</td></tr></table>"
        "<table><tr><td>rect(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>trunc(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>exp(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>omni(mod_b(e(x3o3o *b4o)))</td></tr></table>"
        "</body></html>"
    )

    summary = parse_klitzing_html(text)

    assert summary["table_count"] == 2
    assert summary["checks"]["partial_a_found"] is True
    assert summary["checks"]["partial_b_found"] is True
    assert summary["checks"]["all_four_operation_anchors_found"] is True
    assert summary["checks"]["partial_a_and_b_share_single_table"] is True
    assert summary["checks"]["four_operations_share_single_table"] is True
    assert summary["checks"]["operations_order_rect_trunc_exp_omni"] is True
    assert summary["all_checks_pass"] is True


def test_gc_symbol_regex_tolerates_whitespace() -> None:
    text = (
        "<table>"
        "<tr><td>GC(   x3o3o    *b4o   )</td></tr>"
        "<tr><td>(partial a)</td></tr>"
        "<tr><td>(partial b)</td></tr>"
        "</table>"
        "<table>"
        "<tr><td>rect(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>trunc(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>exp(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>omni(mod_b(e(x3o3o *b4o)))</td></tr>"
        "</table>"
    )
    summary = parse_klitzing_html(text)
    assert summary["hits"]["gc_symbol"] is not None


def test_gc_symbol_regex_tolerates_anchor_wrapping() -> None:
    text = (
        "<table>"
        "<tr><td>GC(<a href='x'>x3o3o *b4o</a>)</td></tr>"
        "<tr><td>(partial a)</td></tr>"
        "<tr><td>(partial b)</td></tr>"
        "</table>"
        "<table>"
        "<tr><td>rect(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>trunc(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>exp(mod_b(e(x3o3o *b4o)))</td></tr>"
        "<tr><td>omni(mod_b(e(x3o3o *b4o)))</td></tr>"
        "</table>"
    )
    summary = parse_klitzing_html(text)
    assert summary["hits"]["gc_symbol"] is not None
    assert summary["checks"]["gc_symbol_found"] is True
