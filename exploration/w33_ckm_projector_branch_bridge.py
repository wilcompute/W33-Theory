"""Projector-side branch selector for the discrete CKM closure.

The discrete CKM dictionary already closed to one packet:

    amplitude = 7/13,
    common phase = 3pi/8 or 5pi/8   (mod pi).

That still leaves a branch question: why should the positive-J branch be read
as ``5/8`` rather than the conjugate ``3/8``?

The current repo already contains an exact operator-side answer in the
three-channel W(3,3) calculus:

- the nonnegative spectral projector ``E0 + E1`` has diagonal value ``5/8``;
- the negative spectral projector ``E2`` has diagonal value ``3/8``.

This module matches those projector weights to the two CKM branch classes from
the full discrete dictionary. The result is exact:

- positive CKM branch  <->  nonnegative projector diagonal ``5/8``;
- negative CKM branch  <->  negative projector diagonal ``3/8``.

So within the repo's current canonical ordering, the sign branch is no longer
an unexplained octant choice. The positive observed CKM branch is the
nonnegative spectral branch, while the conjugate branch is the pure negative
15-sector branch.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    exploration = ROOT / "exploration"
    if str(exploration) not in sys.path:
        sys.path.insert(0, str(exploration))
else:
    ROOT = Path(__file__).resolve().parents[1]
    exploration = ROOT / "exploration"
    if str(exploration) not in sys.path:
        sys.path.insert(0, str(exploration))

from w33_three_channel_operator_bridge import spectral_projector_coefficients
from w33_three_channel_operator_bridge import three_channel_entry_values


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_projector_branch_bridge_summary.json"


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def build_ckm_projector_branch_bridge_summary() -> dict[str, Any]:
    discrete = _load_json("w33_discrete_ckm_dictionary_bridge_summary.json")

    projector_coeffs = spectral_projector_coefficients()
    nonnegative_entries = three_channel_entry_values(projector_coeffs["E_nonnegative"])
    negative_entries = three_channel_entry_values(projector_coeffs["E2"])

    best = discrete["best_candidates"]
    positive_candidates = [item for item in best if item["unitary_jarlskog"] > 0.0]
    negative_candidates = [item for item in best if item["unitary_jarlskog"] < 0.0]

    positive_classes = sorted({item["phase_numerator"] % 8 for item in positive_candidates})
    negative_classes = sorted({item["phase_numerator"] % 8 for item in negative_candidates})

    positive_phase = positive_classes[0] / 8.0
    negative_phase = negative_classes[0] / 8.0
    nonnegative_diagonal = nonnegative_entries["diagonal"]
    negative_diagonal = negative_entries["diagonal"]

    return {
        "status": "ok",
        "projector_dictionary": {
            "nonnegative_projector": {
                "name": "E0_plus_E1",
                "rank": 25,
                "diagonal": nonnegative_diagonal,
                "edge": nonnegative_entries["edge"],
                "nonedge": nonnegative_entries["nonedge"],
            },
            "negative_projector": {
                "name": "E2",
                "rank": 15,
                "diagonal": negative_diagonal,
                "edge": negative_entries["edge"],
                "nonedge": negative_entries["nonedge"],
            },
        },
        "best_discrete_ckm_branches": {
            "positive_jarlskog_phase_classes_over_pi": [value / 8.0 for value in positive_classes],
            "negative_jarlskog_phase_classes_over_pi": [value / 8.0 for value in negative_classes],
            "positive_fundamental_phase_over_pi": positive_phase,
            "negative_fundamental_phase_over_pi": negative_phase,
        },
        "ckm_projector_branch_theorem": {
            "positive_ckm_branch_matches_nonnegative_projector_diagonal_5_over_8": (
                nonnegative_diagonal == "5/8" and abs(positive_phase - 5.0 / 8.0) < 1e-12
            ),
            "negative_ckm_branch_matches_negative_projector_diagonal_3_over_8": (
                negative_diagonal == "3/8" and abs(negative_phase - 3.0 / 8.0) < 1e-12
            ),
            "best_branch_classes_are_exactly_the_two_projector_diagonals_mod_half_turn": (
                positive_classes == [5]
                and negative_classes == [3]
                and nonnegative_diagonal == "5/8"
                and negative_diagonal == "3/8"
            ),
            "two_branch_weights_sum_to_one": (
                nonnegative_diagonal == "5/8" and negative_diagonal == "3/8"
            ),
        },
        "interpretive_read": (
            "Inference from the exact branch match: the octant ambiguity is not "
            "floating free. The positive CKM branch is the nonnegative "
            "projector branch, while the conjugate branch is the pure negative "
            "projector branch."
        ),
        "bridge_verdict": (
            "The remaining CKM branch ambiguity now has an operator label. In "
            "the current canonical ordering, the positive discrete CKM branch "
            "lands exactly at common phase 5/8, which is the diagonal weight of "
            "the nonnegative projector E0+E1. The conjugate branch lands at "
            "3/8, the diagonal weight of the negative projector E2. So the "
            "positive observed branch is the nonnegative spectral branch, while "
            "the opposite sign is the 15-sector branch."
        ),
        "source_files": [
            "data/w33_discrete_ckm_dictionary_bridge_summary.json",
            "exploration/w33_three_channel_operator_bridge.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_ckm_projector_branch_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
