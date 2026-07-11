from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = {
    181: "w33_pass181_adjoint_shadow_mod3.json",
    182: "w33_pass182_line_octahedron_dictionary.json",
    183: "w33_pass183_incidence_square_ledger.json",
    184: "w33_pass184_mod3_trade_factors.json",
    185: "w33_pass185_octahedron_clock.json",
    186: "w33_pass186_pentad_core_scheme.json",
    187: "w33_pass187_f2_layer_sandwich.json",
    188: "w33_pass188_icosahedron_test.json",
    189: "w33_pass189_uniserial_certificate.json",
    190: "w33_pass190_steinberg_address.json",
    191: "w33_pass191_supercycle_pullback.json",
    192: "w33_pass192_signed_trade_edge_s4.json",
}
SCRIPTS = {
    181: "w33_pass181_adjoint_shadow_mod3.py",
    182: "w33_pass182_line_octahedron_dictionary.py",
    185: "w33_pass185_octahedron_clock.py",
    188: "w33_pass188_icosahedron_test.py",
    191: "w33_pass191_supercycle_pullback.py",
    192: "w33_pass192_signed_trade_edge_s4.py",
}


def load(pass_number: int) -> dict:
    return json.loads(
        (ROOT / "data" / DATA_FILES[pass_number]).read_text(encoding="utf-8")
    )


def test_all_twelve_certificates_pass_every_owned_check():
    for pass_number in range(181, 193):
        payload = load(pass_number)
        assert payload["status"] == "PASS", pass_number
        assert payload["checks"], pass_number
        assert all(payload["checks"].values()), pass_number


def test_complete_order_eight_distribution_and_boundary():
    payload = load(183)
    assert payload["ledger"]["all_order8_q_numerators_mod16"] == {
        "address": {"3": 32768, "11": 32768},
        "route": {"3": 512, "11": 512},
        "code_P": {"5": 32768, "13": 32768},
        "code_L": {"5": 512, "13": 512},
    }
    assert "finite abelian groups" in payload["mechanism"]["exact_sequence"]
    assert "quadratic form remains open" in payload["mechanism"]["reading"]
    assert "numerical corroboration" in payload["ledger"]["milgram_boundary"]


def test_module_claims_distinguish_simple_brick_and_hom():
    hom = load(181)
    assert hom["trade_modules_mod3"]["address_L4"]["hom_from_adjoint"] == 1
    assert hom["trade_modules_mod3"]["gauge_L2"]["hom_from_adjoint"] == 1
    assert hom["trade_modules_mod3"]["route_Q43"]["hom_from_adjoint"] == 0
    factors = load(184)
    assert factors["factor_table"]["address_L4"]["quotient_irreducible_exhaustive"]
    assert factors["factor_table"]["gauge_L2"]["quotient_end_dim"] == 1
    assert "brick, not that it is irreducible" in factors["boundary"]


def test_exact_double_six_and_uniserial_theorems():
    double_six = load(188)
    assert double_six["verdict"]["is_icosahedron"] is False
    assert double_six["verdict"]["exact_graph"] == (
        "K6,6 minus a perfect matching (the 6-crown)"
    )
    assert double_six["symmetry"]["group"] == "S6 on either intrinsic six"
    uniserial = load(189)
    assert uniserial["endomorphism_fields"] == {"8": "F4", "14": "F2"}
    assert any(
        "exactly 8 invariant binary codes" in statement
        for statement in uniserial["corollaries"]
    )


def test_live_gap_steinberg_census_is_locked_without_overclaim():
    payload = load(190)
    assert payload["steinberg_column"] == {
        "points": 0,
        "lines": 0,
        "arcs": 2,
        "shell": 3,
        "trades": 0,
        "supports": 0,
        "skew_pairs": 2,
        "hyperbolic_pairs": 1,
        "gq42_arcs": 2,
        "flags": 1,
    }
    assert "composition multiplicity" in payload["boundary"]
    assert "selected embedding" in payload["boundary"]


def test_4320_obstruction_and_native_three_fibre():
    payload = load(191)
    theorem = payload["theorem"]
    assert theorem["product_orbit_sizes"] == [360, 720, 3240]
    assert theorem["double_six_subdegrees_over_an_axis"] == [3, 6, 27]
    assert theorem["pair_stabilizer_orders"] == [72, 36, 8]
    assert "full S3 with kernel 36" in theorem["native_completion_fibre"]
    assert "not a transitive orbit structure" in theorem["reading"]


def test_signed_trade_edge_codec_and_s4_lift():
    payload = load(192)
    assert payload["signed_edge_codec"] == {
        "signed_trades": 240,
        "lines_times_edges": "40*6=240",
        "sign_reversal": "edge complement inside the matched four-point line",
        "equivariance_cases": 480,
    }
    assert payload["line_stabilizer_exact_sequence"]["orders"] == [27, 648, 24]
    assert payload["actions"]["six_signed_trades"].startswith("S4/V4")
    assert "not the regular S3 action" in payload["controller_boundary"]["reading"]


@pytest.mark.parametrize("pass_number", sorted(SCRIPTS))
def test_fast_fresh_witnesses_match_committed_certificates(pass_number: int):
    completed = subprocess.run(
        [sys.executable, str(ROOT / "analysis" / SCRIPTS[pass_number])],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert json.loads(completed.stdout) == load(pass_number)


def test_paper_holonet_and_public_surfaces_lock_the_boundaries():
    paper = (ROOT / "w33_paper.tex").read_text(encoding="utf-8")
    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    practical = (ROOT / "holonet_practical_implications.tex").read_text(
        encoding="utf-8"
    )
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "4320=3240+720+360=120(27+6+3)" in paper
    assert "1\\longrightarrow C_3^3\\longrightarrow H" in paper
    assert "not} a free $S_3$" in paper
    assert "3240+720+360=120(27+6+3)" in photonic
    assert "six signed states" in practical
    for anchor in (
        "pass181-185-audited-module-axis-boundaries",
        "pass183-order-eight-distribution-ledger",
        "pass186-188-exact-double-six-crowns",
        "pass187-189-f2-uniserial-module",
        "pass190-steinberg-composition-census",
        "pass191-double-six-subdegrees",
        "pass192-signed-trade-edge-s4-lift",
    ):
        assert index.count(f'id="{anchor}"') == 1


def test_synthesis_lists_every_regenerating_witness():
    synthesis = (ROOT / "PASS181_192_AUDITED_CHIRAL_COMPLETION_SYNTHESIS.md").read_text(
        encoding="utf-8"
    )
    for pass_number in range(181, 193):
        assert f"w33_pass{pass_number}" in synthesis
