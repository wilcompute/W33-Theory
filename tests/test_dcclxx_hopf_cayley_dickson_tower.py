"""Part DCCLXX -- Hopf / Cayley-Dickson tower tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxx_hopf_cayley_dickson_tower import (  # noqa: E402
    LAM,
    MU,
    OUT_PATH,
    PHI6,
    Q,
    build_bridge,
    cayley_dickson_tower,
    hopf_fibrations,
    hopf_total_dims_are_mersenne,
    tits_magic_square_O_corner,
    write_bridge,
)


def test_cayley_dickson_R_dim_1():
    tower = cayley_dickson_tower()
    assert tower[0]["dim"] == 1


def test_cayley_dickson_C_dim_eq_lambda():
    tower = cayley_dickson_tower()
    assert tower[1]["dim"] == LAM == 2


def test_cayley_dickson_H_dim_eq_mu():
    tower = cayley_dickson_tower()
    assert tower[2]["dim"] == MU == 4


def test_cayley_dickson_O_dim_eq_2_to_q():
    tower = cayley_dickson_tower()
    assert tower[3]["dim"] == 2 ** Q == 8


def test_cayley_dickson_S_dim_eq_qp1_squared():
    tower = cayley_dickson_tower()
    assert tower[4]["dim"] == (Q + 1) ** 2 == 16


def test_sedenion_not_division_algebra():
    tower = cayley_dickson_tower()
    assert tower[4]["is_division_algebra"] is False


def test_RCHO_are_division_algebras():
    tower = cayley_dickson_tower()
    for i in range(4):
        assert tower[i]["is_division_algebra"] is True


def test_hopf_total_dims_are_mersenne():
    check = hopf_total_dims_are_mersenne()
    assert check["values"] == [1, 3, 7, 15]
    assert all(check[f"S_{n}_eq_M_{i+1}"] for n, i in [(1, 0), (3, 1), (7, 2), (15, 3)])


def test_hopf_total_dim_S_3_eq_q():
    hopf = hopf_fibrations()
    assert hopf[1]["total_dim"] == Q == 3


def test_hopf_total_dim_S_7_eq_Phi_6():
    hopf = hopf_fibrations()
    assert hopf[2]["total_dim"] == PHI6 == 7


def test_hopf_total_dim_S_15_eq_15():
    """15 = g eigen-mult = M_4 = SM gauge gens."""
    hopf = hopf_fibrations()
    assert hopf[3]["total_dim"] == 15


def test_hopf_base_dim_S_2_eq_lambda():
    hopf = hopf_fibrations()
    assert hopf[1]["base_dim"] == LAM == 2


def test_hopf_base_dim_S_4_eq_mu():
    hopf = hopf_fibrations()
    assert hopf[2]["base_dim"] == MU == 4


def test_hopf_base_dim_S_8_eq_2_to_q():
    hopf = hopf_fibrations()
    assert hopf[3]["base_dim"] == 2 ** Q == 8


def test_4_hopf_fibrations():
    """Adams' Hopf Invariant One theorem (1960) -- exactly 4 fibrations."""
    assert len(hopf_fibrations()) == 4


def test_4_normed_division_algebras():
    """Hurwitz theorem -- exactly 4 normed division algebras."""
    tower = cayley_dickson_tower()
    division = [t for t in tower if t["is_division_algebra"]]
    assert len(division) == 4


def test_tits_magic_square_O_row_4_entries():
    magic = tits_magic_square_O_corner()
    assert len(magic) == 4
    results = [r["result"] for r in magic]
    assert results == ["F_4", "E_6", "E_7", "E_8"]


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Hopf-Cayley-Dickson" in b["theorem"]
    assert "division algebras" in b["one_line"]


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
        "cayley_dickson_tower",
        "hopf_fibrations",
        "hopf_total_dims_are_mersenne",
        "tits_magic_square_O_corner",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
