"""GAP-owned regression for the Pass-2307 quadratic-Hom S3 theorem."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GAP = shutil.which("gap")
SCRIPT = ROOT / "analysis" / "w33_pass2307_quadratic_hom_s3_decomposition.g"
CERTIFICATE = ROOT / "data" / "w33_pass2307_quadratic_hom_s3_decomposition.json"
SOURCE_CERTIFICATE = ROOT / "data" / "w33_pass2301_complete_quadratic_hom_bases.json"


@pytest.fixture(scope="module")
def pass2307() -> tuple[str, dict, dict]:
    assert GAP is not None, "GAP is required for Pass 2307"
    result = subprocess.run(
        [GAP, "-q", str(SCRIPT)],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )
    return (
        result.stdout,
        json.loads(CERTIFICATE.read_text(encoding="utf-8")),
        json.loads(SOURCE_CERTIFICATE.read_text(encoding="utf-8")),
    )


def decompose(n: int, fixed: int, even: int, odd: int) -> list[int]:
    trace = even - odd
    return [(fixed + trace) // 2, (fixed - trace) // 2, (n - fixed) // 2]


def test_gap_character_witness_passes(pass2307: tuple[str, dict, dict]) -> None:
    output, certificate, _ = pass2307
    assert "Pass2307 status=PASS" in output
    assert "Symmetric [trivial,sign,standard]=[ 13, 3, 5 ]" in output
    assert "Alternating [trivial,sign,standard]=[ 3, 13, 4 ]" in output
    assert "Combined [trivial,sign,standard]=[ 16, 16, 9 ]" in output
    assert "outer_even_odd=[25,25] phase_fixed_rotating=[32,18]" in output
    assert certificate["status"] == "PASS"
    assert len(certificate["checks"]) == 19
    assert all(certificate["checks"].values())


def test_certificate_is_derived_from_pass2301(pass2307: tuple[str, dict, dict]) -> None:
    _, certificate, source = pass2307
    assert certificate["source"]["sha256_without_hash_field"] == source[
        "sha256_without_hash_field"
    ]
    target_order = [str(x) for x in certificate["target_order"]]
    for kind, output_key in (("Sym", "symmetric"), ("Lambda", "alternating")):
        rows = []
        for target in target_order:
            n = source["full_PSp_Hom_dimensions"][kind][target]
            fixed = source["mu6_simultaneous_bilinear_action"]["decomposition"][kind][
                target
            ]["fixed"]
            even = source["outer_involution_split"]["even_PGSp_extendible"][kind][
                target
            ]
            odd = source["outer_involution_split"]["odd_outer_twisted"][kind][target]
            row = decompose(n, fixed, even, odd)
            assert row == certificate[output_key]["per_target_multiplicities"][target]
            rows.append(row)
        assert [sum(row[i] for row in rows) for i in range(3)] == certificate[
            output_key
        ]["total_multiplicities"]


def test_s3_decomposition_explains_both_splits(
    pass2307: tuple[str, dict, dict]
) -> None:
    _, certificate, _ = pass2307
    trivial, sign, standard = certificate["combined"]["total_multiplicities"]
    assert [trivial, sign, standard] == [16, 16, 9]
    assert [trivial + standard, sign + standard] == [25, 25]
    assert [trivial + sign, 2 * standard] == [32, 18]
    assert certificate["combined"][
        "character_on_classes_identity_3cycle_reflection"
    ] == [50, 23, 0]


def test_publication_surfaces_name_the_s3_theorem() -> None:
    report = (ROOT / "PASS2307_QUADRATIC_HOM_S3_DECOMPOSITION.md").read_text(
        encoding="utf-8"
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    tex = (ROOT / "analysis" / "BT2307_quadratic_hom_s3_insert.tex").read_text(
        encoding="utf-8"
    )
    for text in (report, readme, index, tex):
        assert "16" in text and "9" in text
        assert "25" in text
        assert "S3" in text or "S_3" in text
    assert "not physical couplings" in report

