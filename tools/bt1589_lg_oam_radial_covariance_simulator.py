#!/usr/bin/env python3
"""BT1589: Laguerre-Gaussian radial-shell covariance for the OAM recenter ABI."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1589_lg_oam_radial_covariance_simulator.json"
MD = ROOT / "analysis" / "BT1589_lg_oam_radial_covariance_simulator.md"

TRANSLATIONS = [
    (0, 0),
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
]
WITNESS_GATES = ["I", "X", "Z", "F3", "S"]
RECENTERED_THRESHOLD = 0.20


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def recenter_class(shift: tuple[int, int]) -> str:
    x_shift, z_shift = shift
    if x_shift == 0 and z_shift == 0:
        return "centered_frame"
    if x_shift != 0 and z_shift == 0:
        return "oam_shift_only"
    if x_shift == 0 and z_shift != 0:
        return "phase_shift_only"
    return "mixed_shift_phase"


def correction_ops(shift: tuple[int, int]) -> list[str]:
    x_shift, z_shift = shift
    ops: list[str] = []
    if x_shift:
        ops.append("X")
    if z_shift:
        ops.append("Z")
    return ops


def identity(size: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(size)] for i in range(size)]


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [
        [
            round(sum(row[k] * b[k][j] for k in range(len(b))), 12)
            for j in range(len(b[0]))
        ]
        for row in a
    ]


def compose(mats: list[list[list[float]]], size: int) -> list[list[float]]:
    out = identity(size)
    for mat in mats:
        out = matmul(out, mat)
    return out


def matrix_eta(mat: list[list[float]]) -> float:
    diag = [mat[i][i] for i in range(len(mat))]
    return round(1.0 - sum(diag) / len(diag), 12)


def max_abs_delta(a: list[list[float]], b: list[list[float]]) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(len(a)) for j in range(len(a[i])))


def row_sums(mat: list[list[float]]) -> list[float]:
    return [round(sum(row), 12) for row in mat]


def leakage_matrix(eta: float, size: int) -> list[list[float]]:
    if eta == 0:
        return identity(size)
    off_diag = eta / (size - 1)
    return [
        [round(1.0 - eta, 12) if i == j else round(off_diag, 12) for j in range(size)]
        for i in range(size)
    ]


def main() -> None:
    abi = load_json("data/bt1587_oam_recenter_transaction_abi.json")
    leakage = load_json("data/bt1577_radial_leakage_bound_from_oam_phase_ops.json")

    eta_by_op = leakage["operation_bounds"]
    radial_shells = [0, 1, 2]
    matrix_by_op = {
        op: leakage_matrix(eta, len(radial_shells)) for op, eta in eta_by_op.items()
    }

    rows = []
    for shift in TRANSLATIONS:
        shift_ops = correction_ops(shift)
        recenter_mat = compose(
            [matrix_by_op[op] for op in shift_ops], len(radial_shells)
        )
        recenter_eta = matrix_eta(recenter_mat)
        klass = recenter_class(shift)
        for gate in WITNESS_GATES:
            gate_mat = matrix_by_op[gate]
            total_mat = matmul(recenter_mat, gate_mat)
            reverse_mat = matmul(gate_mat, recenter_mat)
            rows.append(
                {
                    "affine_shift": list(shift),
                    "recenter_class": klass,
                    "correction_ops": shift_ops or ["I"],
                    "witness_gate": gate,
                    "core_gate_eta": eta_by_op[gate],
                    "recenter_eta": recenter_eta,
                    "effective_eta": matrix_eta(total_mat),
                    "row_sums": row_sums(total_mat),
                    "commutator_defect": round(
                        max_abs_delta(total_mat, reverse_mat), 12
                    ),
                    "expanded_transaction_words": abi["counts"][
                        "centered_transaction_words"
                    ],
                    "expanded_ticks": abi["counts"]["centered_transaction_words"] * 72,
                    "claim_level": "symbolic LG radial-shell covariance",
                }
            )

    class_counts = Counter(row["recenter_class"] for row in rows)
    expanded_counts = {
        klass: count * abi["counts"]["centered_transaction_words"]
        for klass, count in class_counts.items()
    }
    class_tick_counts = {klass: count * 72 for klass, count in expanded_counts.items()}
    class_eta_max = {
        klass: max(
            row["effective_eta"] for row in rows if row["recenter_class"] == klass
        )
        for klass in sorted(class_counts)
    }
    worst = max(rows, key=lambda row: row["effective_eta"])
    checks = {
        "abi_verified": abi["verified"] is True,
        "leakage_verified": leakage["verified"] is True,
        "three_lg_shells": radial_shells == [0, 1, 2],
        "nine_affine_shifts": len(TRANSLATIONS) == 9,
        "five_witness_gates": set(WITNESS_GATES) == set(eta_by_op),
        "radial_type_rows_45": len(rows) == 45,
        "expanded_word_cases_1080": sum(expanded_counts.values()) == 9 * 5 * 24 == 1080,
        "expanded_tick_budget_77760": sum(class_tick_counts.values()) == 77760,
        "all_row_stochastic": all(
            all(abs(value - 1.0) < 1e-9 for value in row["row_sums"]) for row in rows
        ),
        "all_commutators_zero": all(row["commutator_defect"] == 0.0 for row in rows),
        "core_gate_threshold_preserved": all(
            row["core_gate_eta"] <= leakage["default_threshold"] for row in rows
        ),
        "recentered_threshold_survives": worst["effective_eta"] < RECENTERED_THRESHOLD,
        "worst_is_mixed_f3": worst["recenter_class"] == "mixed_shift_phase"
        and worst["witness_gate"] == "F3",
    }
    result = {
        "bt": 1589,
        "title": "LG/OAM radial-shell covariance simulator",
        "verified": all(checks.values()),
        "source_packets": {
            "abi": "data/bt1587_oam_recenter_transaction_abi.json",
            "leakage": "data/bt1577_radial_leakage_bound_from_oam_phase_ops.json",
        },
        "model": {
            "radial_shells": radial_shells,
            "channel_family": "L(eta): diagonal 1-eta, off-diagonal eta/2 on three LG radial shells",
            "composition_law": "eta_total = eta_a + eta_b - (3/2)*eta_a*eta_b",
            "core_gate_threshold": leakage["default_threshold"],
            "recentered_threshold": RECENTERED_THRESHOLD,
        },
        "counts": {
            "radial_type_rows": len(rows),
            "expanded_word_cases": sum(expanded_counts.values()),
            "expanded_ticks": sum(class_tick_counts.values()),
        },
        "class_type_counts": dict(sorted(class_counts.items())),
        "class_word_counts": dict(sorted(expanded_counts.items())),
        "class_tick_counts": dict(sorted(class_tick_counts.items())),
        "class_eta_max": class_eta_max,
        "worst_case": worst,
        "rows": rows,
        "interpretation": (
            "The radial leakage envelopes form one commuting LG shell channel family. "
            "Therefore recentering and the centered witness gates are shell-covariant: "
            "the 216-action ABI needs a recenter leakage tax, not 216 independent radial "
            "calibrations. The worst symbolic envelope is mixed recentering followed by F3."
        ),
        "honesty_boundary": (
            "This is a symbolic Laguerre-Gaussian radial-shell simulator. It is not a "
            "measured beam profile, detector calibration, or optical-loss claim."
        ),
        "checks": checks,
    }
    OUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    MD.write_text(
        "# BT1589 LG/OAM Radial-Shell Covariance Simulator\n\n"
        "BT1589 models the OAM recenter ABI on three Laguerre-Gaussian radial shells. "
        "The leakage matrices form a commuting `L(eta)` channel family, so recentering "
        "and centered witness gates compose by `eta_total = eta_a + eta_b - 3 eta_a eta_b/2`. "
        f"The worst symbolic case is `{worst['recenter_class']} + {worst['witness_gate']}` "
        f"with eta `{worst['effective_eta']}`, below the recentered threshold "
        f"`{RECENTERED_THRESHOLD}`.\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "bt": 1589,
                "verified": result["verified"],
                "rows": len(rows),
                "worst_eta": worst["effective_eta"],
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
