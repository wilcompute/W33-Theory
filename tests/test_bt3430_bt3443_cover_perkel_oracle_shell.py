import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data/PART_BT3430_BT3441_COVER_PERKEL_ORACLE_SHELL_results.json"


def run_exact():
    subprocess.run([sys.executable, "analysis/bt3430_3441_validated_runner.py"], cwd=ROOT, check=True)
    return json.loads(RESULT.read_text())


def test_exact_packet_status_and_boundary():
    z = run_exact()
    assert z["status"] == "PASS_EXACT_LIGHTWEIGHT_FRONTS_HEAVY_LEDGER_GATED"
    assert z["evidence_boundary"]["chromatic"] == "10 <= chi(H) <= 11"


def test_interblock_all_fifteen_survive_abstract_constraints():
    z = run_exact()["pass3434_3435_interblock"]
    assert z["status"] == "PASS_ALL_15_CONNECTED_SIMPLE_AGGREGATE_REALIZATIONS"
    assert z["templates"] == 15 and z["distinct_spectra"] == 11
    assert all(row["residual_edges"] == 6480 for row in z["rows"])


def test_arithmetic_oracle_is_exhaustive():
    z = run_exact()["pass3436_3437_arithmetic_oracle"]
    assert z["species"] == 135
    assert z["tokens"] == 1350
    assert z["distinct_directed_destinations"] == 1242
    assert z["involution_cases"] == 345600


def test_shell_character_reversal_family():
    z = run_exact()["pass3438_3439_shell_character"]
    assert z["status"] == "PASS_CHARACTER_KRAWTCHOUK_REVERSAL_THROUGH_H17_4"
    r2 = z["instances"][2]
    assert r2["quotient_shells"] == [135, 207, 144, 48, 9, 1]
    assert r2["invariant_multiplicities"] == [1, 9, 48, 144, 207, 135]


def test_perkel_falsifiers_and_twenty_plane():
    z = run_exact()
    p = z["pass3440_perkel_57cell_audit"]
    assert p["perkel"]["distance_shells"] == [1, 6, 30, 20]
    assert p["equitable_partition_test"]["status"] == "PASS_NO_CONNECTED_PERKEL_EQUITABLE_12_30_15_PARTITION"
    assert not p["transitive_57_action_divisibility"]["PSp(4,3)"]
    assert not p["transitive_57_action_divisibility"]["ASp(4,3)"]
    assert z["pass3441_bonkers_rank20_shadow"]["dimensions"] == {"Perkel_minus3": 20, "cover_signature_minus4": 20}


def test_compiled_ledger_source_builds():
    subprocess.run([
        "g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-pedantic",
        "analysis/cpp/w33_pass3430_cover_ledger.cpp", "-o", "/tmp/w33_pass3430_cover_ledger"
    ], cwd=ROOT, check=True)
