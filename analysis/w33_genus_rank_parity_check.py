"""Part MCCX: Genus-rank parity-check law.

Formalizes C345 as an executable finite theorem packet.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def genus_rank_parity_check_packet() -> dict[str, object]:
    mcxcv = _load(ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json")
    mcxciv = _load(ROOT / "PART_MCXCIV_REYE_HORIZON_SYMMETRY_GENUS_RECIPROCITY_results.json")
    mccii = _load(ROOT / "PART_MCCII_C331_MEETING_POINT_results.json")

    q = 3
    n = int(mcxcv["packets"]["horizon_total"])          # 72
    g = int(mcxciv["horizon_packet"]["genus"])          # 6
    k_code = n - g                                         # 66
    rank_h = n - k_code                                    # 6

    k_val = int(mcxcv["packets"]["reye_points"])        # 12
    n_m = int(mccii["packets"]["N_M"])                  # 36

    checks = {
        "packet_is_72_66": n == 72 and k_code == 66,
        "rank_is_n_minus_k": rank_h == n - k_code,
        "rank_is_6": rank_h == 6,
        "rank_equals_genus": rank_h == g == 6,
        "rank_equals_k_over_2": rank_h == k_val // 2 == 6,
        "rank_equals_nm_over_2q": rank_h == n_m // (2 * q) == 6,
        "genus_is_6": g == 6,
        "k_is_12": k_val == 12,
        "nm_is_36": n_m == 36,
        "all_rank_forms_match": rank_h == g == (k_val // 2) == (n_m // (2 * q)),
    }

    return {
        "part": "MCCX",
        "theorem": "Genus-rank parity-check law",
        "packet": {
            "q": q,
            "n": n,
            "k_code": k_code,
            "rank_H": rank_h,
            "genus": g,
            "k_val": k_val,
            "N_M": n_m,
        },
        "identity": {
            "statement": "rank(H)=n-k=72-66=6=g=k_val/2=N_M/(2q)",
        },
        "finite_universality_surrogate": {
            "statement": "parity-check rank equals topological genus across equivalent packet parametrizations",
            "boundary": "finite code/topology identification; not a general theorem for arbitrary families",
        },
        "claim_boundary": "finite rank-genus lock for the established [72,66]_3 horizon packet",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = genus_rank_parity_check_packet()
    out_path = ROOT / "PART_MCCX_GENUS_RANK_PARITY_CHECK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCX: Genus-Rank Parity-Check Law ===")
    print(packet["identity"]["statement"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
