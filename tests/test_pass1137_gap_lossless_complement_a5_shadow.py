"""Pass 1137: GAP-owned lossless complement switch and A5 shadow."""

from __future__ import annotations

import json
import shutil
import subprocess
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1137_lossless_complement_a5_shadow.g"
CERT_PATH = ROOT / "data" / "w33_pass1137_lossless_complement_a5_shadow.json"
NOTE_PATH = ROOT / "PASS1137_LOSSLESS_COMPLEMENT_A5_SHADOW.md"


@lru_cache(maxsize=1)
def _cert() -> dict:
    gap = shutil.which("gap")
    assert gap is not None, "GAP is required for Pass 1137"
    before = CERT_PATH.read_bytes()
    result = subprocess.run(
        [gap, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=90,
    )
    assert "PASS1137 GAP certificate PASS" in result.stdout
    assert "spectral supports 240/540; lossless recovery verified" in result.stdout  # {540:point-nonedge}
    assert "three W(E6)/S5 = PSp(4,3)/A5 carriers of degree 432" in result.stdout
    after = CERT_PATH.read_bytes()
    assert after == before, "the GAP certificate must be byte-deterministic"
    return json.loads(after)


def test_gap_certificate_is_exact_and_deterministic() -> None:
    cert = _cert()
    assert cert["schema"] == "w33.pass1137.lossless_complement_a5_shadow.v1"
    assert cert["status"] == "PASS"
    assert cert["gap"] == {"version": "4.12.1", "check_count": 38}
    assert cert["all_checks_pass"] is True


def test_gap_proves_the_lossless_240_540_spectral_switch() -> None:
    spectral = _cert()["finite_spectral_switch"]
    assert spectral["srg_parameters"] == [40, 12, 2, 4]
    assert spectral["srg_identity"] == "A^2=8I-2A+4J"
    assert spectral["operator"] == "D=A-I"
    assert spectral["positive_generator"] == "H=D^2"
    assert spectral["w33_specialization"] == "H=13I+4Abar"
    assert spectral["D_off_diagonal_support"] == 240
    assert spectral["H_off_diagonal_support"] == 540  # {540:point-nonedge}
    assert spectral["H_off_diagonal_entry_values"] == [0, 4]
    assert spectral["support_tags"] == {
        "D": "240 collinear point pairs",
        "H": "{540:point-nonedge}",
    }
    assert spectral["lossless_recovery"] == "288D=H^2-98H+385I"
    assert spectral["algebra_identity"] == "Q[D^2]=Q[D]"
    assert spectral["D_projector_ranks"] == {"11": 1, "1": 24, "-5": 15}
    assert spectral["H_nullities"] == {"121": 1, "1": 24, "25": 15}
    assert spectral["checks_pass"] is True


def test_gap_proves_all_three_degree_432_a5_shadows() -> None:
    group = _cert()["group_shadow"]
    assert group["e8_root_count"] == 240
    assert group["a2_triple_count"] == 2240
    assert group["e6_root_count"] == 72
    assert group["we6_order"] == 51840
    assert group["derived_order"] == 25920
    assert group["derived_index"] == 2
    assert group["a2_orbit_sizes"] == [
        1,
        1,
        27,
        27,
        27,
        27,
        27,
        27,
        240,
        270,
        270,
        432,
        432,
        432,
    ]
    orbits = group["orbits_432"]
    assert len(orbits) == 3
    expected_order_distribution = {
        "1": 1,
        "2": 25,
        "3": 20,
        "4": 30,
        "5": 24,
        "6": 20,
    }
    for orbit in orbits:
        assert orbit["orbit_size"] == 432
        assert orbit["stabilizer_order"] == 120
        assert orbit["stabilizer_id_group"] == [120, 34]
        assert orbit["stabilizer_identification"] == "S5"
        assert orbit["element_order_distribution"] == expected_order_distribution
        assert orbit["derived_intersection_order"] == 60
        assert orbit["derived_intersection_id_group"] == [60, 5]
        assert orbit["derived_intersection_identification"] == "A5"
        assert orbit["intersection_equals_stabilizer_derived"] is True
        assert orbit["derived_orbit_size"] == 432
        assert orbit["we6_coset_degree"] == 432
        assert orbit["psp_coset_degree"] == 432
        assert orbit["join_order"] == 51840
    assert group["pairwise_conjugate"] == [True, True, True]
    assert (
        group["carrier_identity"]
        == "Res_{PSp(4,3)}^{W(E6)} W(E6)/S5 = PSp(4,3)/A5"
    )
    assert group["carrier_degree"] == 432
    assert group["checks_pass"] is True


def test_publication_states_the_general_identity_and_scope_boundary() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    assert "D_\\lambda=A-\\frac{\\lambda}{2}I" in note
    assert "\\mathbb Q[D^2]=\\mathbb Q[D]" in note
    assert "PSp(4,3)/A_5" in note
    assert "do not by themselves assert" in note
    assert SCRIPT.name in note
    assert CERT_PATH.name in note
