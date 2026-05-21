"""Part MCLXXXVII: Self-entangled emergence square lock.

Goal: tie self-entanglement directly to emergence packets.

From MCLXIII:
  directed temporal changes D = 6,
  Bell now-context rays      R = 4.

From MCLXXXI:
  plaquette packet P = D*R = 24.

From MCLXXX and MCLXXXIII:
  Q4 router edges E_q4 = 32,
  monodromy M = 18432.

New lock:
  M = P*E_q4*P = (D*R)^2 * E_q4
    = (6*4)^2 * 32.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def self_entangled_emergence_square_lock_packet() -> dict[str, object]:
    mclxiii = _load(ROOT / "PART_MCLXIII_TEMPORAL_SELF_ENTANGLED_QUTRIT_results.json")
    mclxxx = _load(ROOT / "PART_MCLXXX_SELF_ENTANGLED_QUTRIT_Q4_ROUTER_results.json")
    mclxxxi = _load(ROOT / "PART_MCLXXXI_Q4_PLAQUETTE_DIRECTED_CHANGE_results.json")
    mclxxxiii = _load(ROOT / "PART_MCLXXXIII_Q4_TOMOTOPE_MONODROMY_BIQUADRATIC_LOCK_results.json")

    directed_changes = int(mclxiii["temporal_qutrit"]["directed_change_histories"])   # 6
    now_rays = int(mclxiii["now_computation"]["two_qutrit_surviving_projective_rays"])  # 4
    plaquettes = int(mclxxxi["plaquette_formula"]["face_count"])                       # 24
    q4_edges = int(mclxxx["q4_router"]["edges"])                                        # 32
    monodromy = int(mclxxxiii["tomotope_packet"]["monodromy_order"])                    # 18432

    checks = {
        "temporal_seed_is_6_times_4": directed_changes * now_rays == 24,
        "plaquette_equals_temporal_seed": plaquettes == directed_changes * now_rays,
        "router_edges_are_32": q4_edges == 32,
        "monodromy_is_18432": monodromy == 18432,
        "emergence_square_lock": monodromy == plaquettes * q4_edges * plaquettes,
        "expanded_square_lock": monodromy == (directed_changes * now_rays) ** 2 * q4_edges,
        "router_centered_ratio": monodromy // q4_edges == plaquettes * plaquettes == 576,
        "plaquette_centered_ratio": monodromy // plaquettes == q4_edges * plaquettes == 768,
        "symmetric_plaquette_factors": monodromy == 24 * 32 * 24,
    }

    return {
        "part": "MCLXXXVII",
        "theorem": "Self-entangled emergence square lock",
        "seed_packet": {
            "directed_changes": directed_changes,
            "now_rays": now_rays,
            "plaquette_seed": directed_changes * now_rays,
            "identity": "24 = 6*4",
        },
        "emergent_router_packet": {
            "plaquettes": plaquettes,
            "q4_edges": q4_edges,
            "monodromy": monodromy,
            "identity": "18432 = 24*32*24 = (6*4)^2*32",
        },
        "finite_universality_surrogate": {
            "statement": "self-entangled temporal seed (6x4) emerges as a squared plaquette shell coupled through Q4 router edges",
            "boundary": "finite combinatorial emergence lock; not a continuum field equation",
        },
        "claim_boundary": "finite self-entanglement-to-emergence factorization law",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = self_entangled_emergence_square_lock_packet()
    out_path = ROOT / "PART_MCLXXXVII_SELF_ENTANGLED_EMERGENCE_SQUARE_LOCK_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXXXVII: Self-Entangled Emergence Square Lock ===")
    print(packet["seed_packet"]["identity"])
    print(packet["emergent_router_packet"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
