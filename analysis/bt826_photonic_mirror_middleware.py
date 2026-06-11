#!/usr/bin/env python3
"""
BT826 - Photonic mirror middleware.

BT825 proves that the photon's physical optics generate Sp(4,3), order 51840.
BT815 identifies the chart-transversal bus as a 2160-element D12 mirror G-set.
BT814 identifies the local residual carrier as the 48-block tomotope middle
layer.

This packet fuses those facts into a runtime factorization:

    |Sp(4,3)| = 24 * 2160 = 24 * 45 * 48.

The 2160 bus is not a loose count: it is the PSp(4,3) chart-transversal
mirror space.  Lifting from PSp to Sp doubles the D12 stabilizer from 12 to
24, so the full optical Clifford group is a torsor over:

    full slot stabilizer (24) x polar-pair geography (45) x tomotope middle (48).
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def main() -> None:
    bt814 = load_json("data/bt814_tomotope_middle_layer_from_residual_tetrahedra.json")
    bt815 = load_json("data/bt815_global_2160_transversal_gset.json")
    bt825 = load_json("data/bt825_universality_theorem.json")

    sp_order = int(bt825["symplectic_closure"])
    psp_order = sp_order // 2
    mirror_slots = int(bt815["slot_counts"]["chart_transversal_slots"])
    projective_slot_stabilizer = int(bt815["stabilizer"]["order"])
    full_slot_stabilizer = sp_order // mirror_slots
    polar_pair_geography = 45
    tomotope_middle_blocks = int(bt814["f_vector_from_transversal_tetrahedra"]["middle_blocks"])
    tomotope_flags = int(bt814["f_vector_from_transversal_tetrahedra"]["flags_if_each_block_has_2x2_fiber"])

    factorization = {
        "sp_order": sp_order,
        "psp_order": psp_order,
        "mirror_slots": mirror_slots,
        "projective_slot_stabilizer": projective_slot_stabilizer,
        "full_slot_stabilizer": full_slot_stabilizer,
        "polar_pair_geography": polar_pair_geography,
        "tomotope_middle_blocks": tomotope_middle_blocks,
        "tomotope_flags": tomotope_flags,
        "sp_as_full_stabilizer_times_bus": full_slot_stabilizer * mirror_slots,
        "bus_as_polar_pairs_times_middle_blocks": polar_pair_geography * tomotope_middle_blocks,
        "sp_as_runtime_product": full_slot_stabilizer * polar_pair_geography * tomotope_middle_blocks,
    }

    checks = {
        "BT825_optical_closure_is_full_Sp43": sp_order == 51840,
        "projective_order_is_half_full_order": psp_order == 25920,
        "BT815_bus_has_2160_slots": mirror_slots == 2160,
        "BT815_projective_stabilizer_is_D12": (
            projective_slot_stabilizer == 12
            and bt815["stabilizer"]["gap_witness"]["structure"] == "D12"
            and bt815["stabilizer"]["gap_witness"]["isomorphic_to_C12"] == "false"
        ),
        "full_lift_of_slot_stabilizer_has_order_f": full_slot_stabilizer == 24,
        "BT814_local_middle_has_48_blocks": tomotope_middle_blocks == 48,
        "BT814_local_middle_restores_192_flags": tomotope_flags == 192,
        "mirror_bus_is_polar_pair_geography_times_tomotope_middle": mirror_slots == 45 * 48,
        "full_clifford_is_slot_lift_times_mirror_bus": sp_order == 24 * mirror_slots,
        "full_clifford_runtime_product": sp_order == 24 * 45 * 48,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT826 check failed: {name}")

    out = {
        "theorem": "BT826 photonic mirror middleware",
        "factorization": factorization,
        "interpretation": {
            "runtime_factorization": "|Sp(4,3)| = 24 * 2160 = 24 * 45 * 48",
            "24": "full Sp lift of the D12 projective mirror-slot stabilizer; equals f",
            "45": "hyperbolic polar-pair / tritangent geography from BT810-BT813",
            "48": "local tomotope edge-face middle layer from BT814; also the chart O_h order",
            "2160": "global D12 mirror bus: chart-transversal slots = antipode slots, distinct from the C12 rectangle clock",
            "architecture": "the universal optical Clifford group acts through a mirror middleware: stabilizer lift x polar vacuum x local tomotope middle carrier",
        },
        "paper_sentence": (
            "The photonic holonet is not only clocked by a cyclic C12 selector; "
            "it is routed by a D12 mirror bus whose full Clifford lift factors "
            "as 24 x 45 x 48 = |Sp(4,3)|."
        ),
        "checks": checks,
    }
    path = ROOT / "data" / "bt826_photonic_mirror_middleware.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
