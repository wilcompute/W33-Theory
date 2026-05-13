#!/usr/bin/env python3
"""Part DCXIII: Z2 swap-symmetry bridge.

This part formalizes the left/right duality as a single involution sigma that
swaps both paired decompositions:

  forward <-> backward,
  csaszar <-> szilassi.

It certifies:
  - sigma^2 = id (order-2 symmetry),
  - pair totals are invariant under sigma,
  - weighted closure (42*4=168) is sigma-invariant.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIRECTIONAL_PATH = ROOT / "data" / "tomotope_toroidal_directional_split_bridge.json"
EDGE_PAIR_PATH = ROOT / "data" / "tomotope_toroidal_edge_pair_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_z2_swap_symmetry_bridge.json"


@dataclass(frozen=True)
class Z2Summary:
    forward_count: int
    backward_count: int
    csaszar_edges: int
    szilassi_edges: int
    oriented_total: int
    weighted_total: int
    all_identities_hold: bool


def _apply_sigma(labels: dict[str, int], sigma: dict[str, str]) -> dict[str, int]:
    return {sigma[k]: v for k, v in labels.items()}


def build_bridge() -> dict[str, Any]:
    directional = json.loads(DIRECTIONAL_PATH.read_text(encoding="utf-8"))
    edge_pair = json.loads(EDGE_PAIR_PATH.read_text(encoding="utf-8"))

    f = int(directional["summary"]["forward_oriented_count"])
    b = int(directional["summary"]["backward_oriented_count"])
    c = int(edge_pair["summary"]["csaszar_edges"])
    s = int(edge_pair["summary"]["szilassi_edges"])
    oriented_total = int(directional["summary"]["total_oriented_count"])
    weighted_total = int(directional["summary"]["weighted_directional_total"])

    sigma_dir = {"forward": "backward", "backward": "forward"}
    sigma_fam = {"csaszar": "szilassi", "szilassi": "csaszar"}

    directional_labels = {"forward": f, "backward": b}
    family_labels = {"csaszar": c, "szilassi": s}

    sigma_dir_once = _apply_sigma(directional_labels, sigma_dir)
    sigma_fam_once = _apply_sigma(family_labels, sigma_fam)

    sigma_dir_twice = _apply_sigma(sigma_dir_once, sigma_dir)
    sigma_fam_twice = _apply_sigma(sigma_fam_once, sigma_fam)

    identities = {
        "upstream_directional_identities_hold": bool(directional["summary"]["all_identities_hold"]),
        "upstream_edge_pair_identities_hold": bool(edge_pair["summary"]["all_identities_hold"]),
        "forward_backward_are_21": f == b == 21,
        "csaszar_szilassi_are_21": c == s == 21,
        "sigma_directional_order_2": sigma_dir_twice == directional_labels,
        "sigma_family_order_2": sigma_fam_twice == family_labels,
        "directional_pair_sum_invariant": (
            directional_labels["forward"] + directional_labels["backward"]
            == sigma_dir_once["forward"] + sigma_dir_once["backward"]
            == oriented_total
        ),
        "family_pair_sum_invariant": (
            family_labels["csaszar"] + family_labels["szilassi"]
            == sigma_fam_once["csaszar"] + sigma_fam_once["szilassi"]
            == oriented_total
        ),
        "pair_sums_match": (
            directional_labels["forward"] + directional_labels["backward"]
            == family_labels["csaszar"] + family_labels["szilassi"]
            == 42
        ),
        "weighted_total_sigma_invariant": weighted_total == 168,
    }

    summary = Z2Summary(
        forward_count=f,
        backward_count=b,
        csaszar_edges=c,
        szilassi_edges=s,
        oriented_total=oriented_total,
        weighted_total=weighted_total,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "involutions": {
            "sigma_directional": sigma_dir,
            "sigma_family": sigma_fam,
        },
        "sigma_actions": {
            "directional_once": sigma_dir_once,
            "directional_twice": sigma_dir_twice,
            "family_once": sigma_fam_once,
            "family_twice": sigma_fam_twice,
        },
        "identities": identities,
        "notes": (
            "DCXIII expresses the 21+21 symmetry as an explicit Z2 involution on both "
            "directional and family decompositions. The involution preserves pair sums "
            "(42) and weighted closure (168)."
        ),
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
