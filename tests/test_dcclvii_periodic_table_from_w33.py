"""Part DCCLVII -- Periodic table from W(3,3) tests."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclvii_periodic_table_from_w33 import (  # noqa: E402
    LAM,
    NOBLE_GASES,
    OUT_PATH,
    PHI4,
    PHI6,
    Q,
    build_bridge,
    magnetic_count,
    noble_gas_table,
    orbital_capacity,
    orbital_table,
    periodic_row_lengths,
    write_bridge,
)


def test_s_capacity_is_2():
    assert orbital_capacity(0) == 2 == LAM


def test_p_capacity_is_6():
    assert orbital_capacity(1) == 6 == math.factorial(Q)


def test_d_capacity_is_10():
    assert orbital_capacity(2) == 10 == PHI4


def test_f_capacity_is_14():
    assert orbital_capacity(3) == 14 == 2 * PHI6


def test_magnetic_counts_at_p_d_f():
    assert magnetic_count(1) == 3 == Q
    assert magnetic_count(2) == 5
    assert magnetic_count(3) == 7 == PHI6


def test_row_lengths_are_2n_squared():
    rows = periodic_row_lengths()
    expected_per_pair = [2, 8, 8, 18, 18, 32, 32]
    assert [r["length"] for r in rows] == expected_per_pair


def test_He_atomic_number():
    He = next(g for g in NOBLE_GASES if g[0] == "He")
    assert He[1] == 2 == LAM


def test_Ne_atomic_number():
    Ne = next(g for g in NOBLE_GASES if g[0] == "Ne")
    assert Ne[1] == 10 == PHI4


def test_Ar_atomic_number():
    Ar = next(g for g in NOBLE_GASES if g[0] == "Ar")
    assert Ar[1] == 18 == 2 * Q ** 2


def test_Kr_atomic_number_is_T_8():
    Kr = next(g for g in NOBLE_GASES if g[0] == "Kr")
    assert Kr[1] == 36 == math.comb(Q ** 2, 2)


def test_Xe_atomic_number_is_2_q_to_q():
    Xe = next(g for g in NOBLE_GASES if g[0] == "Xe")
    assert Xe[1] == 54 == 2 * Q ** Q


def test_Rn_atomic_number():
    Rn = next(g for g in NOBLE_GASES if g[0] == "Rn")
    assert Rn[1] == 86 == 2 * Q ** Q + 2 * (Q + 1) ** 2


def test_orbital_table_5_rows():
    assert len(orbital_table()) == 5


def test_noble_gas_table_7_rows():
    assert len(noble_gas_table()) == 7


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Periodic-Table" in b["theorem"]
    assert "q!" in b["one_line"] or "Phi" in b["one_line"]


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "orbital_table",
        "periodic_row_lengths",
        "noble_gas_table",
        "shell_sums_2n_squared",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
