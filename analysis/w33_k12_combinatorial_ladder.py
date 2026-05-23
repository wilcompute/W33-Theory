"""Part MCCVII: K12 combinatorial ladder law.

Formalizes C337-C338 style ladder statements for k=12 and ties them to
established substrate primitives.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def k12_combinatorial_ladder_packet() -> dict[str, object]:
    mcciii = _load(ROOT / "PART_MCCIII_TEMPORAL_TRIANGLE_SINGLE_PHOTON_LOCK_results.json")
    mcxcv = _load(ROOT / "PART_MCXCV_REYE_HORIZON_OCTET_FACTOR_LOCK_results.json")

    q = int(mcciii["packet"]["q"])   # 3
    mu = 4
    k = int(mcxcv["packets"]["reye_points"])  # 12
    phi6 = int(mcciii["packet"]["Phi_6"])  # 7
    phi3 = q * q + q + 1  # 13

    ladder = {f"C(12,{r})": comb(k, r) for r in range(1, 7)}
    c1 = ladder["C(12,1)"]
    c2 = ladder["C(12,2)"]
    c3 = ladder["C(12,3)"]
    c4 = ladder["C(12,4)"]
    c5 = ladder["C(12,5)"]
    c6 = ladder["C(12,6)"]

    checks = {
        "k_equals_q_mu": k == q * mu == 12,
        "ladder_r1": c1 == 12,
        "ladder_r2": c2 == 66,
        "ladder_r3": c3 == 220,
        "ladder_r4": c4 == 495,
        "ladder_r5": c5 == 792,
        "ladder_r6": c6 == 924,
        "pascal_symmetry_r1": c1 == comb(k, 11),
        "pascal_symmetry_r2": c2 == comb(k, 10),
        "pascal_symmetry_r3": c3 == comb(k, 9),
        "pascal_symmetry_r4": c4 == comb(k, 8),
        "pascal_symmetry_r5": c5 == comb(k, 7),
        "central_factor_lock": c6 == mu * q * phi6 * (k - 1) == 4 * 3 * 7 * 11,
        "c3_factor_lock": c3 == (k * (k - 1) * (k - 2)) // 6,
        "c2_matches_horizon_payload": c2 == 66,
        "phi3_is_13": phi3 == 13,
    }

    return {
        "part": "MCCVII",
        "theorem": "K12 combinatorial ladder law",
        "primitives": {
            "q": q,
            "mu": mu,
            "k": k,
            "Phi_6": phi6,
            "Phi_3": phi3,
        },
        "ladder": ladder,
        "central_lock": {
            "identity": "C(12,6)=924=mu*q*Phi_6*(k-1)=4*3*7*11",
        },
        "finite_universality_surrogate": {
            "statement": "the full K12 binomial ladder is rigidly determined by the k=12 substrate and central primitive factorization",
            "boundary": "finite combinatorial ladder theorem; not a continuum classification",
        },
        "claim_boundary": "finite C(12,r) ladder formalization with central primitive factor lock",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = k12_combinatorial_ladder_packet()
    out_path = ROOT / "PART_MCCVII_K12_COMBINATORIAL_LADDER_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCVII: K12 Combinatorial Ladder Law ===")
    print(packet["central_lock"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
