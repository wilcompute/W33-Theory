"""Part MCCI: Post-monodromy octet lift law.

Continuation of MCXCIX and MCC.

Given:
  A0 = 576,
  A1 = 4608 = 8*A0,
  M  = 18432 = 4*A1 = 32*A0.

Define one further cell-octet lift:
  A2 = 8*A1.

New lock:
  A2 = 36864 = 64*A0 = 2*M.

So one extra octet lift past MCXCIX lands exactly at twice monodromy.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def post_monodromy_octet_lift_packet() -> dict[str, object]:
    mcxcix = _load(ROOT / "PART_MCXCIX_COMMUTING_LIFT_OPERATORS_results.json")
    mcc = _load(ROOT / "PART_MCC_SHELL_OPERATOR_IDENTIFICATION_results.json")

    a0 = int(mcxcix["base_packet"]["A0_reye"])      # 576
    c = int(mcxcix["base_packet"]["cell_lift_C"])   # 8
    a1 = int(mcxcix["base_packet"]["A1"])           # 4608
    m = int(mcxcix["base_packet"]["M"])             # 18432
    e = int(mcc["packets"]["E_shell"])              # 32
    s = int(mcc["packets"]["S"])                    # 24

    a2 = c * a1

    checks = {
        "base_packet_is_consistent": a1 == c * a0 and m == 4 * a1,
        "a2_is_octet_lift_of_a1": a2 == c * a1,
        "a2_is_36864": a2 == 36864,
        "a2_over_a0_is_64": a2 // a0 == 64 and a2 % a0 == 0,
        "a2_over_a1_is_8": a2 // a1 == 8 and a2 % a1 == 0,
        "a2_over_m_is_2": a2 // m == 2 and a2 % m == 0,
        "a2_equals_2m": a2 == 2 * m,
        "a2_equals_2e_s_square": a2 == 2 * e * s * s,
        "m_equals_e_s_square": m == e * s * s,
        "power_chain_identity": a2 == (c * c) * a0 == 64 * a0,
    }

    return {
        "part": "MCCI",
        "theorem": "Post-monodromy octet lift law",
        "packets": {
            "A0": a0,
            "A1": a1,
            "M": m,
            "A2": a2,
            "C": c,
            "E": e,
            "S": s,
        },
        "forecast_lock": {
            "identity": "A2=8*A1=64*A0=36864=2*M=2*E*S^2",
        },
        "finite_universality_surrogate": {
            "statement": "one additional octet lift beyond the commuting-lift packet lands at exactly twice monodromy",
            "boundary": "finite packet forecast law; not a continuum evolution equation",
        },
        "claim_boundary": "finite post-monodromy octet-lift forecast over MCXCIX-MCC packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = post_monodromy_octet_lift_packet()
    out_path = ROOT / "PART_MCCI_POST_MONODROMY_OCTET_LIFT_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCI: Post-Monodromy Octet Lift Law ===")
    print(packet["forecast_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
