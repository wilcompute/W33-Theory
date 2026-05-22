"""Part MCXCVIII: Forecast-emergence ratio bridge law.

Continuation of MCXCVI-MCXCVII.

Established packets:
  M  = E*S^2 = 18432,
  A1 = E*P^2 = 4608.

New bridge:
  M/A1 = (S/P)^2.

At current packets S=24, P=12, so:
  M/A1 = 18432/4608 = 4 = (24/12)^2.

Equivalent closure:
  M = ((S/P)^2)*A1 = 4*A1.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def forecast_emergence_ratio_bridge_packet() -> dict[str, object]:
    mcxcvi = _load(ROOT / "PART_MCXCVI_UNIFIED_CLOSURE_GRAMMAR_results.json")
    mcxcvii = _load(ROOT / "PART_MCXCVII_OCTET_LIFT_FORECAST_results.json")

    s = int(mcxcvi["emergence_kernel"]["S"])                  # 24
    e = int(mcxcvi["emergence_kernel"]["E"])                  # 32
    m = int(mcxcvi["emergence_kernel"]["M"])                  # 18432
    p = int(mcxcvi["horizon_reye_kernel"]["P"])               # 12
    a1 = int(mcxcvii["forecast_packet"]["A1"])                # 4608

    ratio_mp = m // a1
    scale_sp = s // p

    checks = {
        "emergence_identity": m == e * s * s,
        "forecast_identity": a1 == e * p * p,
        "divisibility_m_over_a1": m % a1 == 0,
        "ratio_m_over_a1_is_4": ratio_mp == 4,
        "divisibility_s_over_p": s % p == 0,
        "ratio_s_over_p_is_2": scale_sp == 2,
        "ratio_bridge_law": ratio_mp == scale_sp * scale_sp,
        "equivalent_bridge_m_equals_ratio_times_a1": m == (scale_sp * scale_sp) * a1,
        "e_cancels_in_bridge": (m // e) == s * s and (a1 // e) == p * p,
        "numeric_identity": m == 4 * a1 == 18432,
    }

    return {
        "part": "MCXCVIII",
        "theorem": "Forecast-emergence ratio bridge law",
        "packets": {
            "S": s,
            "P": p,
            "E": e,
            "M": m,
            "A1": a1,
        },
        "bridge": {
            "M_over_A1": ratio_mp,
            "S_over_P": scale_sp,
            "identity": "M/A1 = (S/P)^2 = 4 and M = 4*A1",
        },
        "finite_universality_surrogate": {
            "statement": "the forecast packet and emergence packet are locked by a pure scale-ratio square law",
            "boundary": "finite arithmetic bridge law; not a continuum scaling theorem",
        },
        "claim_boundary": "finite ratio-square bridge between MCXCVII forecast and emergence packet",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = forecast_emergence_ratio_bridge_packet()
    out_path = ROOT / "PART_MCXCVIII_FORECAST_EMERGENCE_RATIO_BRIDGE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCVIII: Forecast-Emergence Ratio Bridge Law ===")
    print(packet["bridge"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
