from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass1360_1364_gelfand_terwilliger.py"
DATA = ROOT / "data" / "w33_pass1360_1364_gelfand_terwilliger.json"


@pytest.fixture(scope="module")
def result():
    spec = importlib.util.spec_from_file_location("pass1360_1364", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.build()


def test_frozen_certificate(result):
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n"
    assert hashlib.sha256(encoded.encode()).hexdigest() == (
        "501863c5aafb0b32c37f295778243c0e1227b7fd981723f9d51a536e98f8c52a"
    )
    assert DATA.read_text(encoding="utf-8") == encoded


def test_gelfand_pair(result):
    record = result["pass1360_gelfand_pair"]
    assert record["group_order"] == 51840
    assert record["selector_stabilizer_order"] == 432
    assert record["subdegrees"] == [1, 2, 36, 27, 54]
    assert record["double_coset_sizes"] == [432, 864, 15552, 11664, 23328]
    assert record["gelfand_pair"] is True
    assert record["multiplicity_free_degrees"] == [1, 15, 24, 20, 60]


def test_terwilliger_center_and_word_closure(result):
    record = result["pass1361_terwilliger"]
    assert record["dimension_over_Q"] == 79
    assert record["center_dimension_over_Q"] == 10
    assert record["maximum_word_length"] == 6
    assert record["nonzero_elementary_triple_products"] == 53
    assert record["beyond_elementary_triple_span"] == 26


def test_orbital_schur_defect(result):
    record = result["pass1362_orbital_schur_closure"]
    assert record["stabilizer_orbitals_on_XxX"] == 83
    assert record["terwilliger_dimension"] == 79
    assert record["codimension"] == 4
    assert record["schur_closure_dimension"] == 83
    assert record["defect_localization"] == {"2,2": 2, "4,4": 2}


def test_two_prime_split_fingerprint(result):
    record = result["pass1363_two_prime_split_fingerprint"]
    profiles = record["profiles"]
    assert [profile["prime"] for profile in profiles] == [1000003, 1000033]
    assert profiles[0]["blocks"] == profiles[1]["blocks"]
    assert [block["simple_block_size"] for block in record["stable_blocks"]] == [
        1, 1, 1, 2, 2, 3, 3, 3, 4, 5
    ]
    assert [block["module_multiplicity"] for block in record["stable_blocks"]] == [
        3, 12, 14, 1, 2, 4, 4, 8, 8, 1
    ]
