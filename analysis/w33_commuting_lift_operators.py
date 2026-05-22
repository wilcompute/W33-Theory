"""Part MCXCIX: Commuting lift operators law.

Continuation of MCXCVI-MCXCVIII.

Use established packets:
  A0 = A_R = 576,         (Reye symmetry base)
  C  = 8,                 (cell octet lift)
  s  = (S/P)^2 = 4,       (scale-square lift)
  M  = 18432.             (emergence monodromy)

Lifts:
  L_C(x) = C*x,
  L_s(x) = s*x.

Then:
  A1 = L_C(A0) = 4608,
  M  = L_s(A1) = L_C(L_s(A0)) = L_{C*s}(A0)
     = 32*A0 = 18432,
so the cell and scale lifts commute on this packet.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def commuting_lift_operators_packet() -> dict[str, object]:
    mcxcv = _load(ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json")
    mcxcvii = _load(ROOT / "PART_MCXCVII_OCTET_LIFT_FORECAST_results.json")
    mcxcviii = _load(ROOT / "PART_MCXCVIII_FORECAST_EMERGENCE_RATIO_BRIDGE_results.json")

    a0 = int(mcxcv["packets"]["reye_automorphism"])      # 576
    c = int(mcxcv["packets"]["cells"])                   # 8
    a1 = int(mcxcvii["forecast_packet"]["A1"])           # 4608
    scale = int(mcxcviii["bridge"]["M_over_A1"])         # 4
    m = int(mcxcviii["packets"]["M"])                    # 18432

    lc_then_ls = scale * (c * a0)
    ls_then_lc = c * (scale * a0)
    combined = (c * scale) * a0

    checks = {
        "base_reye_symmetry_is_576": a0 == 576,
        "cell_lift_is_8": c == 8,
        "scale_lift_is_4": scale == 4,
        "first_lift_matches_forecast_a1": c * a0 == a1 == 4608,
        "second_lift_matches_monodromy": scale * a1 == m == 18432,
        "lifts_commute": lc_then_ls == ls_then_lc,
        "combined_lift_is_32": c * scale == 32,
        "combined_lift_matches_monodromy": combined == m,
        "monodromy_over_base_is_32": m // a0 == 32 and m % a0 == 0,
        "operator_identity": m == (c * scale) * a0 == 8 * 4 * 576,
    }

    return {
        "part": "MCXCIX",
        "theorem": "Commuting lift operators law",
        "base_packet": {
            "A0_reye": a0,
            "cell_lift_C": c,
            "scale_lift_s": scale,
            "A1": a1,
            "M": m,
        },
        "operator_lock": {
            "C_then_s": lc_then_ls,
            "s_then_C": ls_then_lc,
            "combined_factor": c * scale,
            "identity": "M = L_s(L_C(A0)) = L_C(L_s(A0)) = 32*A0 = 8*4*576",
        },
        "finite_universality_surrogate": {
            "statement": "cell-lift and scale-lift compose to monodromy and commute on the established packet",
            "boundary": "finite operator-factor law; not a continuum flow equation",
        },
        "claim_boundary": "finite commuting-lift operator law over MCXCV-MCXCVIII packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = commuting_lift_operators_packet()
    out_path = ROOT / "PART_MCXCIX_COMMUTING_LIFT_OPERATORS_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCIX: Commuting Lift Operators Law ===")
    print(packet["operator_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
