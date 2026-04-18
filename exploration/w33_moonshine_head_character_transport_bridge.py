"""The moonshine transport graph lifts exactly to Monster head character data.

For a McKay-Thompson series

    T_g(q) = q^(-1) + a_1 q + a_2 q^2 + a_3 q^3 + ...,

the first three exact moonshine decompositions are

    a_1 = 1 + chi_{196883}(g),
    a_2 = 1 + chi_{196883}(g) + chi_{21296876}(g),
    a_3 = 2 + 2 chi_{196883}(g) + chi_{21296876}(g) + chi_{842609326}(g).

So the first three nontrivial Monster character values are forced by the
q-series:

    chi_{196883}   = a_1 - 1,
    chi_{21296876} = a_2 - a_1,
    chi_{842609326}= a_3 - a_2 - a_1.

The repo bundles a CTblLib-derived integer character subset for 17 classes:

    1A, 2A, 2B, 3A, 3B, 3C, 5A, 5B, 7A, 7B, 11A, 13A, 13B, 17A, 19A, 29A, 41A.

On all of them, the q-series head inference agrees exactly with the bundled
Monster character values.  So the finite moonshine transport graph is not only
a q-series object; it already lifts to genuine Monster character transport on
the first three nontrivial irreducibles.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_moonshine_head_character_transport_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from scripts.w33_leech_monster import infer_monster_head_character_values, load_monster_ctbllib_charcols
from w33_supported_seed_moonshine_transport_bridge import build_summary as build_transport_summary


HEAD_DEGREES = [196883, 21296876, 842609326]
INTEGER_CLASS_ORDER = [
    "1A",
    "2A",
    "2B",
    "3A",
    "3B",
    "3C",
    "5A",
    "5B",
    "7A",
    "7B",
    "11A",
    "13A",
    "13B",
    "17A",
    "19A",
    "29A",
    "41A",
]


def _head_row(class_name: str, cols: dict[str, Any]) -> dict[str, Any]:
    inferred = infer_monster_head_character_values(class_name, max_n=3)
    if inferred is None:
        raise RuntimeError(f"Head character inference unavailable for {class_name}")

    irrep_rows = cols["irreps"]
    actual = {}
    for deg in HEAD_DEGREES:
        row = next(r for r in irrep_rows if int(r["deg"]) == deg)
        # The bundled CTblLib subset stores the identity trace implicitly as
        # the irreducible degree; non-identity classes are explicit columns.
        if class_name == "1A":
            actual[deg] = int(row["deg"])
        else:
            actual[deg] = int(row[class_name])

    matches = {deg: int(inferred[deg]) == int(actual[deg]) for deg in HEAD_DEGREES}

    return {
        "class_name": class_name,
        "inferred_head_characters": {str(deg): int(inferred[deg]) for deg in [1] + HEAD_DEGREES},
        "ctbllib_head_characters": {str(deg): int(actual[deg]) for deg in HEAD_DEGREES},
        "matches": {str(deg): bool(matches[deg]) for deg in HEAD_DEGREES},
        "all_match": all(matches.values()),
    }


def build_summary() -> dict[str, Any]:
    cols = load_monster_ctbllib_charcols()
    if cols is None:
        raise RuntimeError("Bundled Monster CTblLib character subset unavailable")

    transport = build_transport_summary()
    rows = [_head_row(cls, cols) for cls in INTEGER_CLASS_ORDER]
    special_rows = {row["class_name"]: row for row in rows}

    theorem = {
        "the_bundled_ctbllib_subset_has_exactly_17_integer_classes": sorted(cols["classes"].keys()) == sorted(INTEGER_CLASS_ORDER),
        "all_17_classes_match_on_chi_196883": all(row["matches"]["196883"] for row in rows),
        "all_17_classes_match_on_chi_21296876": all(row["matches"]["21296876"] for row in rows),
        "all_17_classes_match_on_chi_842609326": all(row["matches"]["842609326"] for row in rows),
        "the_exceptional_affine_node_3C_has_head_character_signature_minus1_248_minus248": (
            special_rows["3C"]["inferred_head_characters"]["196883"] == -1
            and special_rows["3C"]["inferred_head_characters"]["21296876"] == 248
            and special_rows["3C"]["inferred_head_characters"]["842609326"] == -248
        ),
        "the_higher_prime_endpoint_41A_has_head_character_signature_1_0_minus1": (
            special_rows["41A"]["inferred_head_characters"]["196883"] == 1
            and special_rows["41A"]["inferred_head_characters"]["21296876"] == 0
            and special_rows["41A"]["inferred_head_characters"]["842609326"] == -1
        ),
        "the_supported_seed_transport_graph_therefore_lifts_to_exact_monster_head_character_transport": (
            transport["supported_seed_moonshine_transport_theorem"][
                "the_supported_seed_moonshine_transport_graph_is_fully_closed"
            ]
            and all(row["all_match"] for row in rows)
        ),
    }
    theorem["the_moonshine_head_character_transport_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "moonshine_head_character_transport_dictionary": {
            "integer_character_classes": list(INTEGER_CLASS_ORDER),
            "rows": rows,
            "transport_theorem": transport["supported_seed_moonshine_transport_theorem"],
        },
        "moonshine_head_character_transport_theorem": theorem,
        "interpretation": (
            "The q-series transport graph is now lifted to genuine Monster character "
            "data on the first three nontrivial irreducibles. For every class in the "
            "bundled integer CTblLib subset, the head characters inferred from the "
            "first three moonshine coefficients agree exactly with the actual Monster "
            "table values. So the finite transport graph already exists on the "
            "character side, not only on the modular-function side."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 MOONSHINE HEAD CHARACTER TRANSPORT BRIDGE")
    print("=" * 72)
    for key, value in summary["moonshine_head_character_transport_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
