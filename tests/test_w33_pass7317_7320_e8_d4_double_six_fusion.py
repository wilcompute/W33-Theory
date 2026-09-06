"""GAP-backed regression for the Pass7317--7320 E8/E6 carrier bridge."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass7317_7320_e8_d4_double_six_fusion.g"
CERT = ROOT / "data" / "PART_W33_PASS7317_7320_E8_D4_DOUBLE_SIX_FUSION.json"
GAP = shutil.which("gap")
pytestmark = pytest.mark.skipif(GAP is None, reason="GAP is required for Pass7317--7320")


@lru_cache(maxsize=1)
def certificate() -> dict:
    assert GAP is not None
    before = CERT.read_bytes()
    run = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    assert "Passes 7317--7320: PASS (37/37)" in run.stdout
    assert "signed Gram rank 6" in run.stdout
    after = CERT.read_bytes()
    assert after == before
    return json.loads(after)


def test_intrinsic_shells_reconstruct_the_e6_incidence_carrier() -> None:
    cert = certificate()
    assert cert["status"] == "PASS"
    assert cert["gap"] == {"version": "4.12.1", "checks": 37}
    shell = cert["intrinsic_shell_descent"]
    assert [shell["minimum_words"], shell["selected_weight15_words"]] == [27, 36]
    assert shell["R_shape"] == [27, 36]
    assert [shell["R_row_degree"], shell["R_column_degree"], shell["R_rank"]] == [16, 12, 21]
    assert shell["R_reconstructed_by_zero_shell_intersection"] is True


def test_rank20_shadow_has_exact_e6_mediated_factorization() -> None:
    factor = certificate()["e6_factorization"]
    assert factor["raw_identity"] == "T^T R=2(J-N)"
    assert factor["centered_identity"] == "T0^T R0=-2N0"
    assert factor["centered_ranks"] == [20, 20, 20]
    assert "sqrt(18)" in factor["normalized_identity"]


def test_intrinsic_steiner_parity_recovers_signed_projective_e6() -> None:
    signed = certificate()["signed_e6_reconstruction"]
    assert signed["H36"] == "SRG(36,20,10,12)"
    assert [signed["edges"], signed["triangles"]] == [360, 1200]
    assert [signed["empty_triple_intersection_triangles"], signed["four_line_triple_intersection_triangles"]] == [120, 1080]
    assert [signed["triangle_edge_rank_F2"], signed["switching_kernel_dimension"]] == [325, 35]
    assert [signed["signed_gram_rank"], signed["signed_gram_spectrum"]] == [6, "12^6+0^30"]
    assert signed["code_only_input"] is True


def test_chosen_a2_anchor_maps_the_shell_to_actual_e8_roots() -> None:
    direct = certificate()["direct_e8_root_crosscheck"]
    assert [direct["A2_perp_roots"], direct["A2_perp_projective_lines"]] == [72, 36]
    assert direct["A2_anchor_gram"] == [[2, -1], [-1, 2]]
    assert direct["gram_off_diagonal_profile"] == {"-1": 120, "0": 270, "1": 240}
    assert [direct["signed_gram_rank"], direct["signed_gram_spectrum"]] == [6, "12^6+0^30"]
    assert direct["all_roots_A2_orthogonal"] is True
    assert "not canonical" in direct["gauge"]


def test_integer_transform_has_z12_firewall_and_a35_residual() -> None:
    firewall = certificate()["integer_transform_mod12_firewall"]
    assert firewall["K_shape"] == [87, 36]
    assert firewall["K_gram"] == "2592I36"
    assert firewall["all_columns_identical_mod12"] is True
    assert firewall["row_residue_census"] == {"9": 40, "8": 45, "6": 2}
    assert firewall["residue_removed_gram"] == "Z^T Z=18I36+42J36"
    assert "scaled A35" in firewall["difference_lattice"]
    assert "rules out" in firewall["e8_z12_boundary"]


def test_sources_are_byte_frozen_and_embedding_boundary_is_explicit() -> None:
    cert = certificate()
    for source in cert["source_certificates"]:
        assert hashlib.sha256((ROOT / source["path"]).read_bytes()).hexdigest() == source["sha256"]
    assert "not asserted to be an invariant subset" in cert["boundary"]
