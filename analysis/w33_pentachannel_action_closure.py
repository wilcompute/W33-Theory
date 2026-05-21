"""Part MCLXVIII: Pentachannel action closure law.

Outside-the-box attack-all-at-once packet:
we collapse five previously separate channels into one exact conserved finite
action quantum A*.

Channels (all exact in prior parts):
  1) temporal-harmonic compiler      (MCLXVII)
  2) geometric frame closure          (MCLXVII)
  3) Bell-cloud local topology        (MCLXVI)
  4) holographic/Morita spectral lock (MCLXV, MCLXII)
  5) Seidel/triangle shell            (MCLIX, MCLXV)

Main closure:
  A* = 360
     = 9*40                      (history cells * frame closure)
     = 40*(10-1)                (rays * non-anchor context count)
     = 20*18                    (S_holo * lambda_spine)
     = 15*24                    (sigma0 * mult_gap)
     = (3/2)*240                (3/2 * Seidel energy)

The result is a finite pentachannel universality surrogate: one shared action
quantum controls all five layers simultaneously.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def pentachannel_action_closure_packet() -> dict[str, object]:
    mclxvii = _load(ROOT / "PART_MCLXVII_ONE_QUTRIT_TEMPORAL_COMPILER_results.json")
    mclxvi = _load(ROOT / "PART_MCLXVI_TEMPORAL_BELL_COCONTEXT_CLOUD_results.json")
    mclxv = _load(ROOT / "PART_MCLXV_VACUUM_INCREMENT_ACTION_LOCK_results.json")
    mclxii = _load(ROOT / "PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json")
    mclix = _load(ROOT / "PART_MCLIX_SEIDEL_MATRIX_results.json")

    histories = Fraction(mclxvii["seed"]["history_cells"])
    rays = Fraction(mclxvii["compiled_substrate"]["projective_rays"])
    contexts = Fraction(mclxvii["compiled_substrate"]["complete_context_count"])
    frame_closure = Fraction(mclxvii["compiled_substrate"]["frame_closure"])

    bell_spreads = Fraction(mclxvi["bell_line"]["spread_count_containing_bell"])
    cloud_total = Fraction(mclxvi["cocontext_cloud"]["total_companion_incidences"])
    cloud_distinct = Fraction(mclxvi["cocontext_cloud"]["distinct_companion_lines"])

    s_holo = Fraction(mclxv["constants"]["S_holo"])
    lambda_spine = Fraction(mclxv["constants"]["lambda_spine"])
    sigma0 = Fraction(mclxv["constants"]["sigma_0"])
    mult_gap = Fraction(mclxv["constants"]["mult_gap"])
    nu_gap = Fraction(mclxv["constants"]["nu_gap"])

    seidel_energy = Fraction(mclxv["constants"]["E_seidel"])
    triangles = Fraction(mclix["n_triangles"])
    critical_radius = Fraction(mclxii["deformation_envelope"]["one_parameter_critical_radius"]["fraction"])

    action_temporal = histories * frame_closure
    action_geometric = rays * (contexts - 1)
    action_holographic = s_holo * lambda_spine
    action_uv = sigma0 * mult_gap
    action_seidel = Fraction(3, 2) * seidel_energy
    action_values = [action_temporal, action_geometric, action_holographic, action_uv, action_seidel]
    action_star = action_temporal

    checks = {
        "all_five_channel_actions_are_identical": all(value == action_star for value in action_values),
        "shared_action_is_360": action_star == 360,
        "history_times_frame_closure_is_action_star": histories * frame_closure == action_star,
        "rays_times_nonanchor_contexts_is_action_star": rays * (contexts - 1) == action_star,
        "holographic_spine_is_action_star": s_holo * lambda_spine == action_star,
        "uv_shell_is_action_star": sigma0 * mult_gap == action_star,
        "seidel_rescaled_action_is_action_star": Fraction(3, 2) * seidel_energy == action_star,
        "bell_cloud_factors_as_9_times_9": cloud_total == bell_spreads * histories == 81,
        "bell_cloud_compression_factor_is_4_to_action": action_star / cloud_total == Fraction(40, 9),
        "triangle_energy_bridge_holds": Fraction(3, 2) * triangles == seidel_energy,
        "radius_times_spine_exceeds_gap_threshold": critical_radius * nu_gap == Fraction(25, 18) * Fraction(5, 6)
        and critical_radius * nu_gap > 1,
        "cloud_distinct_plus_shell_intersections_plus_bell_is_w33_line_total": cloud_distinct + 12 + 1 == 40,
    }

    return {
        "part": "MCLXVIII",
        "theorem": "Pentachannel action closure law",
        "action_star": {
            "value": str(action_star),
            "channels": {
                "temporal_harmonic": str(action_temporal),
                "geometric_frame": str(action_geometric),
                "holographic_morita": str(action_holographic),
                "uv_gap_shell": str(action_uv),
                "seidel_rescaled": str(action_seidel),
            },
            "identities": [
                "360 = 9*40",
                "360 = 40*(10-1)",
                "360 = 20*18",
                "360 = 15*24",
                "360 = (3/2)*240",
            ],
        },
        "bell_cloud_bridge": {
            "bell_spreads": int(bell_spreads),
            "history_cells": int(histories),
            "total_companion_incidences": int(cloud_total),
            "distinct_companions": int(cloud_distinct),
            "identity": "81 = 9*9 = 27*3",
            "action_to_cloud_ratio": str(action_star / cloud_total),
        },
        "finite_universality_surrogate": {
            "harmonic": "9 history cells",
            "geometric": "40 rays with 10 maximal contexts",
            "topological": "Bell cloud 81 on 27 lines",
            "spectral": "20*18 lock",
            "transport": "15*24 lock",
            "single_shared_action": str(action_star),
            "boundary": "finite simultaneous closure certificate; not a formal classical TM universality proof",
        },
        "claim_boundary": (
            "finite five-channel simultaneous closure on W33 packets; no continuum or formal TM universality proof"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = pentachannel_action_closure_packet()
    out_path = ROOT / "PART_MCLXVIII_PENTACHANNEL_ACTION_CLOSURE_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXVIII: Pentachannel Action Closure Law ===")
    print("A* =", packet["action_star"]["value"])
    print(" / ".join(packet["action_star"]["identities"]))
    print(packet["bell_cloud_bridge"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
