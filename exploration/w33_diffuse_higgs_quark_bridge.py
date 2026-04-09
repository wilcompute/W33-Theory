"""Exact quark-bearing structure of the diffuse Higgs pair.

This module packages the complementary role of H_1 and Hbar_1 relative to the
clean leptonic pair H_2, Hbar_2.

What is established here:
  - H_2 and Hbar_2 are the exact clean leptonic pair;
  - H_1 and Hbar_1 each have exactly 8 support entries, but those entries are
    not random:
      * H_1 carries an exact up-type colored packet plus a 2-entry leptonic
        completion;
      * Hbar_1 carries an exact down-type colored packet plus a 2-entry
        leptonic completion.

So the current exact Higgs-side scaffold splits sharply into:
  - clean leptonic pair: H_2, Hbar_2
  - diffuse quark-bearing pair: H_1, Hbar_1
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from exploration.w33_fermionic_connes_sector import build_clean_higgs_geometry_summary


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_diffuse_higgs_quark_bridge_summary.json"


def _entry_triplet(entry: dict[str, object]) -> tuple[str, str, int]:
    return (
        str(entry["left_slot"]),
        str(entry["right_slot"]),
        int(entry["value"]),
    )


@lru_cache(maxsize=1)
def build_diffuse_higgs_quark_summary() -> dict[str, Any]:
    summary = build_clean_higgs_geometry_summary()
    support = summary["yukawa_support"]

    h1 = support["H_1"]
    hbar1 = support["Hbar_1"]

    h1_up_packet = sorted(
        _entry_triplet(entry)
        for entry in h1
        if entry["left_slot"].startswith("Q_") or entry["right_slot"].startswith("u_c")
    )
    h1_leptonic_completion = sorted(
        _entry_triplet(entry)
        for entry in h1
        if _entry_triplet(entry) not in h1_up_packet
    )

    hbar1_down_packet = sorted(
        _entry_triplet(entry)
        for entry in hbar1
        if entry["left_slot"].startswith("Q_") or entry["right_slot"].startswith("d_c")
    )
    hbar1_leptonic_completion = sorted(
        _entry_triplet(entry)
        for entry in hbar1
        if _entry_triplet(entry) not in hbar1_down_packet
    )

    return {
        "status": "ok",
        "h1_support": [_entry_triplet(entry) for entry in h1],
        "hbar1_support": [_entry_triplet(entry) for entry in hbar1],
        "h1_up_packet": h1_up_packet,
        "h1_leptonic_completion": h1_leptonic_completion,
        "hbar1_down_packet": hbar1_down_packet,
        "hbar1_leptonic_completion": hbar1_leptonic_completion,
        "diffuse_higgs_quark_theorem": {
            "clean_pair_is_still_exactly_leptonic": bool(
                summary["geometry_theorem"]["clean_pair_support_is_exactly_leptonic"]
            ),
            "h1_has_exactly_eight_entries": len(h1) == 8,
            "hbar1_has_exactly_eight_entries": len(hbar1) == 8,
            "h1_splits_as_up_type_colored_six_plus_leptonic_two": (
                len(h1_up_packet) == 6 and len(h1_leptonic_completion) == 2
            ),
            "hbar1_splits_as_down_type_colored_six_plus_leptonic_two": (
                len(hbar1_down_packet) == 6 and len(hbar1_leptonic_completion) == 2
            ),
            "h1_is_the_up_type_diffuse_packet": sorted(h1_up_packet) == sorted(
                [
                    ("Q_1_2", "nu_c", -1),
                    ("Q_2_2", "nu_c", 1),
                    ("Q_3_2", "nu_c", -1),
                    ("L_1", "u_c_1", 1),
                    ("L_1", "u_c_2", -1),
                    ("L_1", "u_c_3", -1),
                ]
            ),
            "hbar1_is_the_down_type_diffuse_packet": sorted(hbar1_down_packet) == sorted(
                [
                    ("Q_1_1", "e_c", 1),
                    ("Q_2_1", "e_c", -1),
                    ("Q_3_1", "e_c", 1),
                    ("L_2", "d_c_1", -1),
                    ("L_2", "d_c_2", 1),
                    ("L_2", "d_c_3", 1),
                ]
            ),
            "exact_higgs_side_splits_into_clean_leptonic_pair_plus_diffuse_quark_pair": (
                summary["geometry_theorem"]["clean_pair_support_is_exactly_leptonic"]
                and len(h1_up_packet) == 6
                and len(hbar1_down_packet) == 6
            ),
        },
        "interpretive_read": (
            "Inference from the exact cubic/Yukawa support: the Higgs-side "
            "structure is already organized into a clean leptonic pair and a "
            "diffuse quark-bearing pair. The quark side is not absent; it is "
            "present only in the more entangled H_1, Hbar_1 channels."
        ),
        "bridge_verdict": (
            "The Higgs-side packet is now structurally resolved. H_2 and Hbar_2 "
            "form the exact clean leptonic pair, while H_1 and Hbar_1 form the "
            "diffuse quark-bearing pair. More sharply, H_1 is an exact up-type "
            "colored six-packet plus a two-entry leptonic completion, and "
            "Hbar_1 is the complementary down-type colored six-packet plus a "
            "two-entry leptonic completion. So the quark hierarchy is not in the "
            "clean layer, but it is already rigidly encoded in the diffuse pair."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_diffuse_higgs_quark_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
