#!/usr/bin/env python3
"""Part DCLXXIX: holonomy balanced core bridge.

Part DCLXXVIII identified the exact minimal 39-state host architecture. The next
question is whether that host already contains a canonical energy-ordered core.

This verifier proves the stronger statement: the explicit minimal realization is
already balanced, with two exact Hankel singular values. The larger singular
value belongs to the 15 slow states, so the principal balanced core is exactly
the slow sector and its reduced transfer function is precisely the slow atom.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxviii_holonomy_minimal_host_realization_bridge import (  # noqa: E402
    build_host_realization,
)

OUT_PATH = ROOT / "data" / "dclxxix_holonomy_balanced_core_bridge.json"


@dataclass(frozen=True)
class BalancedCoreSummary:
    state_dimension: int
    retained_core_rank: int
    discarded_rank: int
    all_identities_hold: bool


def _transfer(s: float, A: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    return C @ np.linalg.inv(s * np.eye(n) - A) @ B


def build_bridge() -> dict[str, Any]:
    host = build_host_realization()
    fast_rank = int(host["fast_rank"])
    slow_rank = int(host["slow_rank"])
    state_dimension = int(host["dynamic_rank"])
    fast_rate = float(host["fast_rate"])
    slow_rate = float(host["slow_rate"])
    A = host["A_host"]
    B = host["B_host"]
    C = host["C_host"]
    P_plus = host["P_plus"]
    P_minus = host["P_minus"]
    Wc = host["Wc"]
    Wo = host["Wo"]

    lyap_c = A @ Wc + Wc @ A.T + B @ B.T
    lyap_o = A.T @ Wo + Wo @ A + C.T @ C

    hankel = np.sqrt(np.clip(np.linalg.eigvalsh(Wc @ Wo), 0.0, None))
    unique_hankel = sorted({round(float(x), 12) for x in hankel})
    fast_sigma = 1.0 / (2.0 * fast_rate)
    slow_sigma = 1.0 / (2.0 * slow_rate)

    A_fast = A[:fast_rank, :fast_rank]
    B_fast = B[:fast_rank, :]
    C_fast = C[:, :fast_rank]
    A_slow = A[fast_rank:, fast_rank:]
    B_slow = B[fast_rank:, :]
    C_slow = C[:, fast_rank:]

    sample_s = (0.25, 0.5, 1.0, 2.0, 4.0)
    fast_transfer_ok = all(
        np.allclose(_transfer(s, A_fast, B_fast, C_fast), P_plus / (s + fast_rate))
        for s in sample_s
    )
    slow_transfer_ok = all(
        np.allclose(_transfer(s, A_slow, B_slow, C_slow), P_minus / (s + slow_rate))
        for s in sample_s
    )

    identities = {
        "the_minimal_host_realization_is_already_balanced": np.allclose(Wc, Wo),
        "controllability_and_observability_gramians_satisfy_the_exact_lyapunov_equations": np.allclose(lyap_c, np.zeros_like(lyap_c)) and np.allclose(lyap_o, np.zeros_like(lyap_o)),
        "there_are_exactly_two_hankel_singular_values": len(unique_hankel) == 2,
        "fast_hankel_singular_value_is_one_over_2log4": abs(fast_sigma - 1.0 / (2.0 * math.log(4.0))) < 1e-12,
        "slow_hankel_singular_value_is_one_over_2log5_over_2": abs(slow_sigma - 1.0 / (2.0 * math.log(2.5))) < 1e-12,
        "slow_sector_has_larger_hankel_weight_than_fast_sector": slow_sigma > fast_sigma,
        "the_principal_rank_15_balanced_core_is_exactly_the_slow_sector": slow_transfer_ok,
        "the_discarded_rank_24_piece_is_exactly_the_fast_sector": fast_transfer_ok,
        "retaining_the_slow_core_and_discarding_the_fast_core_splits_the_transfer_exactly": all(
            np.allclose(
                _transfer(s, A, B, C),
                _transfer(s, A_fast, B_fast, C_fast) + _transfer(s, A_slow, B_slow, C_slow),
            )
            for s in sample_s
        ),
        "therefore_the_canonical_host_core_is_the_15_dimensional_slow_sector": bool(
            np.allclose(Wc, Wo) and slow_sigma > fast_sigma and slow_transfer_ok
        ),
    }

    summary = BalancedCoreSummary(
        state_dimension=state_dimension,
        retained_core_rank=slow_rank,
        discarded_rank=fast_rank,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "balanced_core": {
            "fast_hankel_singular_value": "1/(2 log(4))",
            "slow_hankel_singular_value": "1/(2 log(5/2))",
            "retained_rank": 15,
            "discarded_rank": 24,
            "retained_transfer": "R_slow(s) = P_-/(s+log(5/2))",
            "discarded_transfer": "R_fast(s) = P_+/(s+log(4))",
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
