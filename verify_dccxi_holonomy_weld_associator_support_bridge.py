#!/usr/bin/env python3
"""Part DCCXI: holonomy weld-associator-support bridge.

DCCX identifies one welded carrier projector

    P = 1/2 [[1,-1],[-1,1]]

with seam complement

    Q = I - P = 1/2 [[1,1],[1,1]].

This verifier extracts the next finite coherence witness by pairing the welded
projector P with two involutions:

    O = diag(1,-1),
    S = [[0,1],[1,0]].

Using the Jordan product A∘B = (AB+BA)/2, we compute the associator

    Assoc(O,P,S) := (O∘P)∘S - O∘(P∘S)

and show it is a fixed signed support kernel with exact 6561 scale inherited
from DCCX.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dccx_holonomy_selector_carrier_weld_bridge import (  # noqa: E402
    build_bridge as build_dccx_bridge,
)


OUT_PATH = ROOT / "data" / "dccxi_holonomy_weld_associator_support_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    weld_projector_rank: int
    seam_projector_rank: int
    covariance_trace: int
    associator_rank: int
    scaled_support_abs_entry: int
    all_identities_hold: bool


def _mat_mul(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]],
        [a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]],
    ]


def _mat_add(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [a[0][0] + b[0][0], a[0][1] + b[0][1]],
        [a[1][0] + b[1][0], a[1][1] + b[1][1]],
    ]


def _mat_sub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [a[0][0] - b[0][0], a[0][1] - b[0][1]],
        [a[1][0] - b[1][0], a[1][1] - b[1][1]],
    ]


def _mat_scale(a: list[list[Fraction]], s: Fraction) -> list[list[Fraction]]:
    return [
        [a[0][0] * s, a[0][1] * s],
        [a[1][0] * s, a[1][1] * s],
    ]


def _jordan(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return _mat_scale(_mat_add(_mat_mul(a, b), _mat_mul(b, a)), Fraction(1, 2))


def _det2(a: list[list[Fraction]]) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _rank2(a: list[list[Fraction]]) -> int:
    zero = Fraction(0, 1)
    if a == [[zero, zero], [zero, zero]]:
        return 0
    if _det2(a) != zero:
        return 2
    return 1


def _to_fraction_matrix(raw: list[list[int]]) -> list[list[Fraction]]:
    return [[Fraction(raw[0][0], 1), Fraction(raw[0][1], 1)], [Fraction(raw[1][0], 1), Fraction(raw[1][1], 1)]]


def _to_str_matrix(a: list[list[Fraction]]) -> list[list[str]]:
    return [[str(a[0][0]), str(a[0][1])], [str(a[1][0]), str(a[1][1])]]


def build_bridge() -> dict[str, Any]:
    dccx = build_dccx_bridge()
    cov_raw = dccx["carrier_weld"]["covariance"]
    covariance = _to_fraction_matrix(cov_raw)

    tr = cov_raw[0][0] + cov_raw[1][1]
    if tr == 0:
        raise ValueError("DCCXI requires nonzero covariance trace from DCCX")

    # Weld and seam projectors from DCCX covariance kernel.
    P = _mat_scale(covariance, Fraction(1, tr))
    I = [[Fraction(1, 1), Fraction(0, 1)], [Fraction(0, 1), Fraction(1, 1)]]
    Q = _mat_sub(I, P)

    O = [[Fraction(1, 1), Fraction(0, 1)], [Fraction(0, 1), Fraction(-1, 1)]]

    S = [[Fraction(0, 1), Fraction(1, 1)], [Fraction(1, 1), Fraction(0, 1)]]

    # Jordan associator witness for the mixed involution triple (O,P,S).
    assoc = _mat_sub(_jordan(_jordan(O, P), S), _jordan(O, _jordan(P, S)))

    # Scale to DCCX trace to recover integer support kernel magnitudes.
    assoc_scaled = _mat_scale(assoc, Fraction(tr, 1))

    expected_assoc = [[Fraction(1, 2), Fraction(0, 1)], [Fraction(0, 1), Fraction(-1, 2)]]
    expected_scaled = [[6561, 0], [0, -6561]]

    identities = {
        "dccx_already_provides_rank_one_weld_projector_and_rank_one_seam_complement": (
            _rank2(P) == 1 and _rank2(Q) == 1 and _mat_add(P, Q) == I
        ),
        "orientation_involution_is_order_two": _mat_mul(O, O) == I,
        "jordan_associator_of_orientation_weld_swap_is_nonzero_fixed_support_kernel": (
            assoc == expected_assoc and _rank2(assoc) == 2
        ),
        "scaled_associator_support_matches_exact_6561_signed_diagonal_packet_magnitude": (
            assoc_scaled[0][0] == 6561
            and assoc_scaled[1][1] == -6561
            and assoc_scaled[0][1] == 0
            and assoc_scaled[1][0] == 0
        ),
        "associator_support_is_purely_signed_diagonal_with_zero_cross_channel_support": (
            assoc_scaled[0][1] == 0 and assoc_scaled[1][0] == 0
        ),
        "therefore_weld_coherence_defect_is_finite_deterministic_and_fully_supported_on_signed_channel_axis": (
            _rank2(P) == 1
            and _rank2(Q) == 1
            and assoc == expected_assoc
            and assoc_scaled == [[Fraction(6561, 1), Fraction(0, 1)], [Fraction(0, 1), Fraction(-6561, 1)]]
        ),
    }

    summary = BridgeSummary(
        weld_projector_rank=_rank2(P),
        seam_projector_rank=_rank2(Q),
        covariance_trace=tr,
        associator_rank=_rank2(assoc),
        scaled_support_abs_entry=6561,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "weld_associator": {
            "weld_projector": _to_str_matrix(P),
            "seam_projector": _to_str_matrix(Q),
            "orientation_involution": _to_str_matrix(O),
            "swap_involution": _to_str_matrix(S),
            "jordan_associator_O_P_S": _to_str_matrix(assoc),
            "scaled_support_kernel": [[int(assoc_scaled[0][0]), int(assoc_scaled[0][1])], [int(assoc_scaled[1][0]), int(assoc_scaled[1][1])]],
            "expected_scaled_support_kernel": expected_scaled,
        },
        "interpretation": {
            "verdict": (
                "The DCCX welded projector has one finite coherence-defect support witness under orientation composition: "
                "the Jordan associator on (O,P,S) is a fixed signed-diagonal kernel with exact 6561 magnitude and zero cross-channel support."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
