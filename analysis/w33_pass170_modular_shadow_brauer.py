#!/usr/bin/env python3
"""Pass 170: the modular shadow -- H10 is the reduction of the hidden pair.

Pass 164 found the incidence-tower module H10 = C^perp/C is uniserial
with F2 composition factors 1, 8, 1.  This witness locates those factors
in the 2-modular decomposition matrix of U4(2) (GAP character table
library), with two findings:

1. THE 8 IS A CONJUGATE PAIR.  The 2-modular irreducible degrees of
   U4(2) are [1, 4, 4, 6, 14, 20, 20, 64]: there is no 8.  The
   F2-irreducible 8-dimensional E8-shadow module splits over the
   splitting field as a conjugate pair of 4s, so H10's Brauer factors
   are {1, 1, 4, 4bar}.

2. THE HIDDEN PAIR.  The two degree-5 ordinary irreducibles -- which
   appear in NONE of the nine permutation carriers of Pass 163 -- reduce
   mod 2 as 1 + 4 and 1 + 4bar.  Hence 5 + 5bar reduces with exactly
   H10's composition factors: the smallest faithful representations of
   the substrate group, invisible in every natural permutation geometry,
   materialize as the SO(10) quotient form.  The kinematic degree-10s
   instead reduce as 4 + 6 and 4bar + 6.
"""

from __future__ import annotations

from ast import literal_eval
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass163_two480s_character_decomposition import (
    GAP_BASH,
    GAP_BINARY,
    cygwin_path,
)

OUT = ROOT / "data" / "w33_pass170_modular_shadow_brauer.json"

GAP_PROGRAM = """
t := CharacterTable("U4(2)");;
Print("ORD=", List(Irr(t), x -> x[1]), ";\\n");
m2 := t mod 2;;
Print("MOD2=", List(Irr(m2), x -> x[1]), ";\\n");
Print("DEC2=", DecompositionMatrix(m2), ";\\n");
m3 := t mod 3;;
Print("MOD3=", List(Irr(m3), x -> x[1]), ";\\n");
Print("DEC3=", DecompositionMatrix(m3), ";\\n");
QUIT;
"""


def run_gap():
    workdir = Path(tempfile.mkdtemp(prefix="w33_pass170_"))
    script = workdir / "pass170.g"
    script.write_text(GAP_PROGRAM, encoding="ascii")
    completed = subprocess.run(
        [
            str(GAP_BASH),
            "--login",
            "-c",
            f"{GAP_BINARY} -q '{cygwin_path(script)}'",
        ],
        capture_output=True,
        text=True,
        timeout=900,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"GAP failed: {completed.stderr[:1500]}")
    text = completed.stdout.replace("\\\n", "").replace("\n", "")

    def extract(marker):
        start = text.index(marker) + len(marker)
        end = text.index(";", start)
        return literal_eval(text[start:end].replace(" ", ""))

    return {
        "ordinary": extract("ORD="),
        "mod2": extract("MOD2="),
        "dec2": extract("DEC2="),
        "mod3": extract("MOD3="),
        "dec3": extract("DEC3="),
    }


def main():
    if not GAP_BASH.exists():
        print("GAP is required for Pass 170")
        return 1
    checks = {}
    data = run_gap()

    ordinary = data["ordinary"]
    mod2 = data["mod2"]
    dec2 = data["dec2"]
    checks["twenty_ordinary_irreducibles"] = len(ordinary) == 20
    checks["ordinary_degrees_match_pass163"] = sorted(ordinary) == sorted(
        [1, 5, 5, 6, 10, 10, 15, 15, 20, 24, 30, 30, 30, 40, 40, 45, 45, 60, 64, 81]
    )
    # the E8-shadow module is F2-irreducible of dimension 8 (Pass 157),
    # but over the splitting field it is a conjugate pair of 4s: the
    # 2-modular degree list contains 4 twice and no 8
    checks["brauer_degrees_are_known_list"] = sorted(mod2) == [
        1,
        4,
        4,
        6,
        14,
        20,
        20,
        64,
    ]

    # every 2-regular restriction is reproduced: row_i . mod2degs = deg_i
    # only on 2-regular classes the degree is unchanged, so this holds:
    checks["dec2_degree_consistency"] = all(
        sum(m * d for m, d in zip(row, mod2)) == ordinary[i]
        for i, row in enumerate(dec2)
    )

    trivial_index = next(i for i, d in enumerate(mod2) if d == 1)
    four_indices = [i for i, d in enumerate(mod2) if d == 4]
    checks["two_conjugate_4s"] = len(four_indices) == 2

    ten_rows = [(i, dec2[i]) for i, d in enumerate(ordinary) if d == 10]
    checks["two_degree_10_ordinaries"] = len(ten_rows) == 2
    six_index = next(i for i, d in enumerate(mod2) if d == 6)
    kinematic_reduction = all(
        row[six_index] == 1 and sum(row[f] for f in four_indices) == 1 and sum(row) == 2
        for _, row in ten_rows
    )
    checks["kinematic_10s_reduce_to_4_plus_6"] = bool(kinematic_reduction)

    # the hidden pair: the two degree-5 ordinaries reduce to 1 + 4 and
    # 1 + 4bar, so 5 + 5bar reduces with factors {1, 1, 4, 4bar} = the
    # Brauer factors of Pass 164's uniserial H10
    five_rows = [(i, dec2[i]) for i, d in enumerate(ordinary) if d == 5]
    checks["two_degree_5_ordinaries"] = len(five_rows) == 2
    shadow_law = (
        len(five_rows) == 2
        and all(
            row[trivial_index] == 1
            and sum(row[f] for f in four_indices) == 1
            and sum(row) == 2
            for _, row in five_rows
        )
        and five_rows[0][1][four_indices[0]] != five_rows[1][1][four_indices[0]]
    )
    checks["shadow_law_5_plus_5bar_gives_1_1_4_4bar"] = bool(shadow_law)

    # the eigenspace characters mod 2
    fifteen_rows = [(i, dec2[i]) for i, d in enumerate(ordinary) if d == 15]
    twentyfour_rows = [(i, dec2[i]) for i, d in enumerate(ordinary) if d == 24]
    checks["context_rows_extracted"] = (
        len(fifteen_rows) == 2 and len(twentyfour_rows) == 1
    )

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass170.modular_shadow_brauer.v1",
        "status": "PASS" if all_pass else "FAIL",
        "gap_source": "live (CTblLib U4(2), Brauer tables mod 2 and mod 3)",
        "ordinary_degrees": ordinary,
        "brauer_degrees_mod2": mod2,
        "brauer_degrees_mod3": data["mod3"],
        "decomposition_rows": {
            "degree_10_ordinaries": [{"index": i, "row": row} for i, row in ten_rows],
            "degree_15_ordinaries": [
                {"index": i, "row": row} for i, row in fifteen_rows
            ],
            "degree_24_ordinary": [
                {"index": i, "row": row} for i, row in twentyfour_rows
            ],
        },
        "shadow_law": {
            "statement": (
                "the two degree-5 ordinary irreducibles of U4(2) reduce "
                "mod 2 as 1 + 4 and 1 + 4bar, so 5 + 5bar reduces with "
                "Brauer factors {1, 1, 4, 4bar} -- exactly the factors of "
                "Pass 164's uniserial H10 (whose F2-factor 8 is the "
                "conjugate pair 4 + 4bar over the splitting field)"
            ),
            "holds": bool(shadow_law),
            "reading": (
                (
                    "the hidden pair: the two degree-5 irreducibles appear in "
                    "NONE of the nine permutation carriers of Pass 163 (all "
                    "multiplicities zero), yet their 2-modular reduction "
                    "carries exactly the composition factors of the SO(10) "
                    "shadow. The smallest faithful representations of the "
                    "substrate group, invisible in every natural permutation "
                    "geometry, materialize as the incidence quotient form. "
                    "The kinematic degree-10s instead reduce as 4 + 6 and "
                    "4bar + 6."
                )
                if shadow_law
                else "the reduction pattern differs; see decomposition rows"
            ),
        },
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
