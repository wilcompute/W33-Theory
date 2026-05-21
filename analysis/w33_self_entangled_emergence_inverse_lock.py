"""Part MCLXXXVIII: Self-entangled emergence inverse lock.

Continuation of MCLXXXVII.

Forward lock was:
  M = S^2 * E_q4,
with S = D*R = 24 (D=6 directed changes, R=4 now-rays), E_q4=32, M=18432.

New inverse lock:
  S = sqrt(M / E_q4) = 24,
  D = S / R = 6.

So the temporal self-entanglement seed is exactly recoverable from the emergent
packet plus the Bell now-context ray count.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def self_entangled_emergence_inverse_lock_packet() -> dict[str, object]:
    mclxiii = _load(ROOT / "PART_MCLXIII_TEMPORAL_SELF_ENTANGLED_QUTRIT_results.json")
    mclxxxvii = _load(ROOT / "PART_MCLXXXVII_SELF_ENTANGLED_EMERGENCE_SQUARE_LOCK_results.json")

    monodromy = int(mclxxxvii["emergent_router_packet"]["monodromy"])  # 18432
    q4_edges = int(mclxxxvii["emergent_router_packet"]["q4_edges"])    # 32
    now_rays = int(mclxiii["now_computation"]["two_qutrit_surviving_projective_rays"])  # 4
    directed_ground_truth = int(mclxiii["temporal_qutrit"]["directed_change_histories"])  # 6

    seed_square = monodromy // q4_edges
    seed = math.isqrt(seed_square)
    recovered_directed = seed // now_rays

    checks = {
        "monodromy_divides_by_q4_edges": monodromy % q4_edges == 0,
        "seed_square_is_576": seed_square == 576,
        "seed_square_is_perfect_square": seed * seed == seed_square,
        "recovered_seed_is_24": seed == 24,
        "recovered_directed_is_integer": seed % now_rays == 0,
        "recovered_directed_is_6": recovered_directed == 6,
        "recovered_directed_matches_mclxiii": recovered_directed == directed_ground_truth,
        "inverse_forward_consistency": monodromy == (seed * seed) * q4_edges,
        "factor_identity": monodromy == (recovered_directed * now_rays) ** 2 * q4_edges,
    }

    return {
        "part": "MCLXXXVIII",
        "theorem": "Self-entangled emergence inverse lock",
        "emergent_input": {
            "monodromy": monodromy,
            "q4_edges": q4_edges,
            "identity": "18432 = S^2*32",
        },
        "recovered_seed": {
            "seed_square": seed_square,
            "seed": seed,
            "now_rays": now_rays,
            "recovered_directed_changes": recovered_directed,
            "identity": "S = sqrt(18432/32) = 24, D = 24/4 = 6",
        },
        "finite_universality_surrogate": {
            "statement": "self-entangled temporal seed is exactly invertible from emergent monodromy and router shell",
            "boundary": "finite inverse-factorization law; not a continuum inverse problem theorem",
        },
        "claim_boundary": "finite emergence-to-seed inversion law",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = self_entangled_emergence_inverse_lock_packet()
    out_path = ROOT / "PART_MCLXXXVIII_SELF_ENTANGLED_EMERGENCE_INVERSE_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXVIII: Self-Entangled Emergence Inverse Lock ===")
    print(packet["recovered_seed"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
