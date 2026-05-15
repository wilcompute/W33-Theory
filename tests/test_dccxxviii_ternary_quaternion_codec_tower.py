"""Part DCCXXVIII -- Ternary-quaternion-codec tower tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxviii_ternary_quaternion_codec_tower import (  # noqa: E402
    CODEC,
    OUT_PATH,
    PAULI_GROUP_ORDER,
    Q,
    QP1,
    W33_E,
    W33_K,
    W33_V,
    build_bridge,
    commute_pairs_count,
    f3_symplectic_form,
    neighborhood_audit,
    projective_classes,
    quaternion_basis,
    qutrit_X,
    qutrit_Z,
    tower_table,
    write_bridge,
)


def test_ternary_size_3():
    assert Q == 3


def test_quaternion_size_4():
    assert QP1 == 4


def test_codec_size_12():
    assert CODEC == 12 == Q * QP1


def test_tower_has_three_layers():
    t = tower_table()
    assert len(t) == 3
    assert [layer["size"] for layer in t] == [3, 4, 12]


def test_quaternion_basis_4_elements():
    qb = quaternion_basis()
    assert len(qb) == 4
    assert set(qb.keys()) == {"1", "B23", "B31", "B12"}


def test_qutrit_X_is_shift():
    X = qutrit_X()
    e0 = np.array([1, 0, 0])
    Xe0 = X @ e0
    assert np.allclose(Xe0, [0, 1, 0])  # X |0> = |1>


def test_qutrit_Z_is_diagonal_clock():
    Z = qutrit_Z()
    omega = np.exp(2j * np.pi / 3)
    expected = np.diag([1, omega, omega ** 2])
    assert np.allclose(Z, expected)


def test_X_Z_commute_with_phase_omega():
    """X Z = omega^{-1} Z X (or omega depending on convention)."""
    X = qutrit_X()
    Z = qutrit_Z()
    omega = np.exp(2j * np.pi / 3)
    XZ = X @ Z
    ZX = Z @ X
    # Must equal omega^k * ZX for some k in {1, 2}
    matched = False
    for k in (1, 2):
        if np.allclose(XZ, (omega ** k) * ZX):
            matched = True
            break
    assert matched


def test_pauli_group_order_3_to_5():
    assert PAULI_GROUP_ORDER == 243


def test_projective_classes_count_40():
    reps = projective_classes()
    assert len(reps) == W33_V == 40


def test_two_qutrit_valency_12():
    reps = sorted(projective_classes())
    nbr = neighborhood_audit(reps)
    assert nbr["all_same"] is True
    assert nbr["common_valency"] == W33_K == 12


def test_two_qutrit_commuting_pairs_240():
    pc = commute_pairs_count()
    assert pc["commuting_pairs"] == W33_E == 240
    assert pc["vertices"] == 40
    assert pc["total_pairs"] == 40 * 39 // 2 == 780


def test_symplectic_form_antisymmetric_after_pair_relabelling():
    """omega(u, u) = 0 for all u (always isotropic)."""
    reps = list(projective_classes())
    for u in reps:
        assert f3_symplectic_form(u, u) == 0


def test_F3_to_4_lattice_minus_one_div_2_equals_40():
    assert (3**4 - 1) // 2 == 40


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_summary_matches_w33():
    b = build_bridge()
    s = b["summary"]
    assert s["matches_W33_v"] is True
    assert s["matches_W33_k"] is True
    assert s["matches_W33_E"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_and_one_line_present():
    b = build_bridge()
    assert "Tower Theorem" in b["theorem"]
    assert "40" in b["one_line"]


def test_honesty_boundary_credits_saniga_planat():
    b = build_bridge()
    boundary = b["honesty_boundary"]
    assert "Saniga" in boundary or "Planat" in boundary


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
        "ternary_quaternion_codec_tower",
        "quaternion_basis",
        "quaternion_multiplication_rule",
        "two_qutrit_pauli_check",
        "single_qutrit_commutation_phase",
        "identities",
        "theorem",
        "one_line",
        "honesty_boundary",
    ):
        assert key in data
