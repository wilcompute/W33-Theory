"""Focused publication contract for the Pass7305--7320 frontier."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
INSERT = ROOT / "analysis" / "PASS7305_7320_intrinsic_naimark_pauli_scope_insert.tex"
PAPER_MANIFEST = ROOT / "analysis" / "PAPER_INSERT_MANIFEST.json"
FRONTIER_MANIFEST = ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex"
CARD_SOURCE = ROOT / "analysis" / "PASS7305_7320_index_insert.html"
MATERIALIZER = ROOT / "tools" / "materialize_pass7305_7320_frontier.py"
README = ROOT / "README.md"
TOKEN = "pass-7305-7320-intrinsic-naimark-pauli-scope"

SPEC = importlib.util.spec_from_file_location("pass7305_7320_materializer", MATERIALIZER)
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_shared_insert_is_registered_once_and_wrappers_stay_indirect() -> None:
    manifest = json.loads(PAPER_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["schema"] == "w33.paper_insert_manifest.v1"
    assert manifest["status"] == "PASS"
    assert manifest["shared_wrappers"] == ["w33_paper.tex", "photonic_holonet.tex"]
    assert len(manifest["entries"]) == 1
    entry = manifest["entries"][0]
    assert entry["id"] == TOKEN
    assert entry["insert"] == INSERT.relative_to(ROOT).as_posix()
    assert entry["public_card"] == CARD_SOURCE.relative_to(ROOT).as_posix()
    assert entry["owners"]["e8_d4_double_six_fusion"].endswith(
        "w33_pass7317_7320_e8_d4_double_six_fusion.g"
    )
    assert "Pass7249-7304 already owns the centered N rank-20" in entry["boundaries"][0]

    input_line = r"\input{analysis/PASS7305_7320_intrinsic_naimark_pauli_scope_insert}%"
    assert FRONTIER_MANIFEST.read_text(encoding="utf-8").count(input_line) == 1
    for wrapper_name in manifest["shared_wrappers"]:
        wrapper = (ROOT / wrapper_name).read_text(encoding="utf-8")
        assert wrapper.count(r"\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}%") == 1
        assert "PASS7305_7320_intrinsic_naimark_pauli_scope_insert" not in wrapper


def test_insert_names_prior_owners_and_keeps_the_new_claim_narrow() -> None:
    text = INSERT.read_text(encoding="utf-8")
    for owner in (
        "w33_pass3694_3700_spread_etf_axial_closure.py",
        "w33_pass4992",
        "w33_pass7163_7170_e8_hexagonal_lift.py",
        "w33_pass7182_d4_glue_spread_code.py",
        "w33_pass7184_spread_code_v20_v24_module.py",
        "w33_pass7225_7232_spread_code_doily_puncture.py",
        "w33_pass7241_7248_double_six_slice_generator.py",
        "PASS7249_7304_eight_frontier_attacks.md",
    ):
        assert owner in text
    for signature in (
        "0^{12}3^{15}",
        "K^TK=2592I_{36}",
        "2^{24}=16{,}777{,}216",
        "fifty-one commuting $K_4$ blocks",
        "not fifty-one pairwise-noncommuting physical Pauli classes",
        "T_0^TR_0=-2N_0",
        "rank $325$",
        "not a canonical map",
        "scaled $A_{35}$ difference lattice",
        "rules out identifying $K\\bmod12$",
    ):
        assert signature in text
    assert "already owns the\ncentered rank-twenty two-distance frame" in text
    assert "not board timing" in text
    assert "alpha(W(3,9))" in text and "is not determined" in text


def test_public_claims_match_all_five_frozen_certificates() -> None:
    decoder = load_json("data/PART_W33_PASS7305_7306_CSPREAD_INTRINSIC_DOUBLE_SIX.json")
    assert decoder["intrinsic_selector"]["definition"].endswith("{0:12,3:15}")
    assert decoder["intrinsic_selector"]["selected_words"] == 36
    assert decoder["intrinsic_pair_intersection_graph"]["parameters"] == "SRG(36,20,10,12)"

    isometry = load_json("data/PART_W33_PASS7307_7309_DOUBLE_SIX_NAIMARK_ISOMETRY.json")
    assert isometry["projector_resolution"]["split"] == "36 = 15 + 20 + 1"
    assert isometry["projector_resolution"]["cross_gram"].endswith("=0")
    assert isometry["integer_hardware_transform"]["shape"] == [87, 36]
    assert isometry["integer_hardware_transform"]["identity"] == "K^T K=2592I36=(36sqrt(2))^2 I36"

    hardware = load_json("data/PART_W33_PASS7310_7312_Q7_PAULI_VALIDATOR.json")
    assert hardware["exact_certificate"]["pairs"] == 528
    assert hardware["formal"]["assignments_covered"] == 2**24
    bram = hardware["synthesis"]["synchronous_bram_serial"]
    assert (bram["cells"]["SB_LUT4"], bram["flip_flops"], bram["block_rams"], bram["cycles"]) == (196, 48, 1, 1618)
    assert hardware["place_and_route_proxy"]["synchronous_bram_serial"]["final_fmax_mhz"] == 41.31
    assert "hardware device result" in hardware["place_and_route_proxy"]["scope"].lower()

    scope = load_json("data/PART_W33_PASS7313_7316_PAULI_TRACE_STABILIZER_SCOPE.json")
    triples = [
        (
            row["linear_sp_stabilizer_order"],
            row["projective_psp_stabilizer_order"],
            row["projective_pcsp_stabilizer_order"],
        )
        for row in scope["typed_stabilizers"]
    ]
    assert triples == [(18, 9, 18), (24, 12, 12), (2, 1, 2), (4, 2, 2)]
    q9 = scope["q9_trace_field_reduction"]
    assert (q9["selected_spread_blocks"], q9["selected_f3_projective_points"]) == (51, 204)
    assert q9["within_block_graph"] == "K4"
    assert q9["between_each_block_pair_graph"] == "4K2 perfect matching"
    assert "not 51 pairwise-noncommuting physical Pauli classes" in scope["boundaries"]["q9"]

    fusion = load_json("data/PART_W33_PASS7317_7320_E8_D4_DOUBLE_SIX_FUSION.json")
    assert fusion["gap"] == {"version": "4.12.1", "checks": 37}
    assert fusion["intrinsic_shell_descent"]["R_reconstructed_by_zero_shell_intersection"] is True
    assert fusion["e6_factorization"]["centered_identity"] == "T0^T R0=-2N0"
    signed = fusion["signed_e6_reconstruction"]
    assert (signed["triangle_edge_rank_F2"], signed["signed_gram_rank"], signed["signed_gram_spectrum"]) == (
        325,
        6,
        "12^6+0^30",
    )
    direct = fusion["direct_e8_root_crosscheck"]
    assert (direct["A2_perp_roots"], direct["A2_perp_projective_lines"]) == (72, 36)
    assert "not canonical" in direct["gauge"]
    firewall = fusion["integer_transform_mod12_firewall"]
    assert firewall["all_columns_identical_mod12"] is True
    assert "scaled A35" in firewall["difference_lattice"]
    assert "rules out" in firewall["e8_z12_boundary"]


def test_card_is_single_source_and_materializer_is_idempotent() -> None:
    assert M.CARD.count(M.MARKER) == 1
    root_sample = "<html><body><main><nav></nav><p>old</p></main></body></html>"
    first, mode = M.materialize_text(root_sample, front_door=True)
    assert mode == "inserted" and first.count(M.MARKER) == 1
    second, mode = M.materialize_text(first, front_door=True)
    assert mode == "already_materialized" and second == first
    assert second.index(M.MARKER) < second.index("<p>old</p>")

    docs_sample = "<html><body><main><p>old</p></main></body></html>"
    first, mode = M.materialize_text(docs_sample, front_door=False)
    assert mode == "inserted" and first.count(M.MARKER) == 1
    second, mode = M.materialize_text(first, front_door=False)
    assert mode == "already_materialized" and second == first
    assert second.index(M.MARKER) < second.index("</main>")

    with pytest.raises(ValueError, match="duplicate"):
        M.materialize_text(first.replace(M.MARKER, M.MARKER + M.MARKER), front_door=False)

    card = CARD_SOURCE.read_text(encoding="utf-8").strip()
    for public_path in (ROOT / "index.html", ROOT / "docs" / "index.html"):
        public = public_path.read_text(encoding="utf-8")
        assert public.count(f'id="{TOKEN}"') == 1
        assert card in public


def test_readme_and_lean_reproduction_surfaces_are_explicit() -> None:
    readme = README.read_text(encoding="utf-8")
    for needle in (
        "Intrinsic double-six and Naimark carrier",
        "E₆/E₈ shell fusion and mod-12 firewall",
        "Finite Pauli scope and q=7 validator",
        "The Pauli dictionary extends verbatim to every odd prime power",
        "|Sp(4,5)|=1,344,000",
        "w33_pass7305_7306_cspread_intrinsic_double_six.py",
        "w33_pass7313_7316_pauli_trace_and_stabilizer_scope.g",
        "w33_pass7317_7320_e8_d4_double_six_fusion.g",
        "materialize_pass7305_7320_frontier.py",
        "Pass7316AntisymplecticRescaling.lean",
    ):
        assert needle in readme

    lean = (ROOT / "formal" / "W33" / "Pass7316AntisymplecticRescaling.lean").read_text(encoding="utf-8")
    assert "theorem rescaled_multiplier" in lean
    assert "theorem antisymplectic_rescale" in lean
    assert (ROOT / "formal" / "W33.lean").read_text(encoding="utf-8").count(
        "import W33.Pass7316AntisymplecticRescaling"
    ) == 1
