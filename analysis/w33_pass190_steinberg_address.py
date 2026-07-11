#!/usr/bin/env python3
"""Pass 190: the Steinberg address -- where the protected memory lives mod 3.

The holonet's protected memory is the Steinberg module (dimension 81 =
3^4, projective in the defining characteristic).  This witness computes,
in GAP, the full mod-3 composition multiplicities of TEN natural carriers
-- points, lines, FLAGS(160), arcs(480), the eigenlattice shell(480),
trades(90), supports(45), and the three 540s -- by restricting each
permutation character to the 3-regular classes and decomposing against
the six 3-modular Brauer characters [1, 5, 10, 14, 25, 81].

The question answered exactly is which permutation modules contain St_81
as a modular composition factor, and with what multiplicity.  This alone
does not identify a preferred embedded register or a hardware protection
mechanism.
"""

from __future__ import annotations

from ast import literal_eval
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set
from analysis.w33_pass163_two480s_character_decomposition import (
    GAP_BASH,
    GAP_BINARY,
    build_carriers,
    cygwin_path,
    gap_tempdir,
)

OUT = ROOT / "data" / "w33_pass190_steinberg_address.json"


def main():
    if not GAP_BASH.exists():
        print("GAP is required for Pass 190")
        return 1
    checks = {}

    points, symplectic, images, sizes, names = build_carriers()
    _, adjacency, _ = build_w33()
    lines = w33_lines(adjacency)
    line_index = {line: n for n, line in enumerate(lines)}
    flags = [
        (p, n) for n, line in enumerate(lines) for p in sorted(line)
    ]
    checks["flag_count_160"] = len(flags) == 160
    flag_index = {f: n for n, f in enumerate(flags)}

    _, group = build_group(points, symplectic)
    two_gens = small_generating_set(group)

    combined_images = []
    for g in two_gens:
        base = images(g)  # 2795 entries, 1-indexed
        flag_block = [
            flag_index[
                (g[p], line_index[frozenset(g[x] for x in lines[ln])])
            ]
            + len(base)
            + 1
            for (p, ln) in flags
        ]
        combined_images.append(list(base) + flag_block)

    all_sizes = sizes + [160]
    all_names = names + ["flags"]

    blocks = []
    offset = 1
    for size in all_sizes:
        blocks.append((offset, offset + size - 1))
        offset += size

    program = []
    gens = ", ".join(
        "PermList([" + ",".join(str(v) for v in image) + "])"
        for image in combined_images
    )
    program.append(f"gens := [ {gens} ];;")
    program.append("G := Group(gens);;")
    program.append('Print("SIZE=", Size(G), ";\\n");')
    block_list = ", ".join(f"[{a},{b}]" for a, b in blocks)
    program.append(f"blocks := [ {block_list} ];;")
    program.append(
        "chis := List(blocks, b -> PermutationCharacter("
        "G, [b[1]..b[2]], OnPoints));;"
    )
    program.append("t := CharacterTable(G);;")
    program.append('lib := CharacterTable("U4(2)");;')
    program.append("tr := TransformingPermutationsCharacterTables(t, lib);;")
    program.append('Print("EQUIV=", tr <> fail, ";\\n");')
    program.append(
        "libchis := List(chis, chi -> ClassFunction(lib, "
        "Permuted(ValuesOfClassFunction(chi), tr.columns)));;"
    )
    program.append("m3 := lib mod 3;;")
    program.append("ib := Irr(m3);;")
    program.append('Print("M3DEGS=", List(ib, x -> x[1]), ";\\n");')
    program.append(
        "rest := List(libchis, chi -> RestrictedClassFunction(chi, m3));;"
    )
    program.append(
        "decs := Decomposition(List(ib, ValuesOfClassFunction), "
        "List(rest, ValuesOfClassFunction), \"nonnegative\");;"
    )
    program.append('Print("DECS=", decs, ";\\n");')
    program.append("QUIT;")

    workdir = gap_tempdir("w33_pass190_")
    script = workdir / "pass190.g"
    script.write_text("\n".join(program) + "\n", encoding="ascii")
    completed = subprocess.run(
        [
            str(GAP_BASH),
            "--login",
            "-c",
            f"{GAP_BINARY} -q '{cygwin_path(script)}'",
        ],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"GAP failed: {completed.stderr[:2000]}")
    text = completed.stdout.replace("\\\n", "").replace("\n", "")

    def extract(marker):
        start = text.index(marker) + len(marker)
        end = text.index(";", start)
        return literal_eval(
            text[start:end]
            .replace(" ", "")
            .replace("fail", "None")
            .replace("true", "True")
            .replace("false", "False")
        )

    size = extract("SIZE=")
    equivalent = extract("EQUIV=")
    m3degs = extract("M3DEGS=")
    decs = extract("DECS=")
    checks["group_order"] = size == 25920
    checks["computed_table_matches_U4_2_library"] = equivalent is True
    checks["m3_degrees"] = sorted(m3degs) == [1, 5, 10, 14, 25, 81]
    checks["decompositions_found"] = decs is not None and all(
        row is not None for row in decs
    )

    st_index = m3degs.index(81)
    table = {}
    consistent = True
    for name, dim, row in zip(all_names, all_sizes, decs):
        total = sum(m * d for m, d in zip(row, m3degs))
        if total != dim:
            consistent = False
        table[name] = {
            "dimension": dim,
            "multiplicities": [int(m) for m in row],
            "steinberg_multiplicity": int(row[st_index]),
        }
    checks["dimension_consistency"] = bool(consistent)

    st_column = {
        name: table[name]["steinberg_multiplicity"] for name in all_names
    }
    expected_multiplicities = {
        "points": [1, 1, 2, 1, 0, 0],
        "lines": [2, 0, 1, 2, 0, 0],
        "arcs": [4, 6, 10, 6, 4, 2],
        "shell": [6, 3, 9, 9, 0, 3],
        "trades": [2, 3, 2, 2, 1, 0],
        "supports": [2, 1, 1, 2, 0, 0],
        "skew_pairs": [11, 9, 9, 13, 2, 2],
        "hyperbolic_pairs": [7, 12, 13, 8, 6, 1],
        "gq42_arcs": [9, 10, 9, 11, 3, 2],
        "flags": [2, 1, 3, 3, 0, 1],
    }
    expected_steinberg = {
        "points": 0,
        "lines": 0,
        "arcs": 2,
        "shell": 3,
        "trades": 0,
        "supports": 0,
        "skew_pairs": 2,
        "hyperbolic_pairs": 1,
        "gq42_arcs": 2,
        "flags": 1,
    }
    checks["all_ten_multiplicity_rows_exact"] = {
        name: entry["multiplicities"] for name, entry in table.items()
    } == expected_multiplicities
    checks["steinberg_column_exact"] = st_column == expected_steinberg

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass190.steinberg_composition_census.v2",
        "status": "PASS" if all_pass else "FAIL",
        "gap_source": "live",
        "m3_degrees": m3degs,
        "carriers": table,
        "steinberg_column": st_column,
        "reading": (
            "the exact mod-3 composition tables of ten geometric "
            "carriers, restricted to 3-regular classes and decomposed "
            "against the Brauer characters: the Steinberg column is the "
            "exact composition-factor census for the Steinberg simple in "
            "the defining characteristic"
        ),
        "boundary": (
            "composition multiplicity is not by itself a selected embedding, "
            "logical register, error-correcting code, or device-protection claim"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
