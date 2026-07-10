#!/usr/bin/env python3
"""Pass 163: the two 480s decomposed -- a dynamics/kinematics selection rule.

Pass 158 proved the 480 Hashimoto arcs and the 480 eigenlattice shell
vectors are non-isomorphic transitive PSp(4,3)-sets with orbital ranks
24 = f and 40 = v.  This witness explains those ranks at the level of
irreducible characters.  It exports NINE natural substrate carriers --

  points(40), lines(40), arcs(480), L2-shell(480), trades(90),
  supports(45), skew line pairs(540), hyperbolic pairs(540),
  GQ(4,2) arcs(540)

-- as one combined permutation action on 2795 points, hands it to GAP,
and obtains the exact decomposition of every permutation character into
the 20 irreducibles of PSp(4,3) = U4(2), together with the full 9 x 9
intertwiner Gram matrix (= joint orbital ranks, cross-validating Passes
158 and 161).

The physics question: the point character decomposes as
1 + chi_24 + chi_15 (the gauge and chiral eigenspace irreducibles).
Which carriers contain the chiral sentinel chi_15, which contain the
gauge chi_24, and is the arc spectrum (dynamics, the Ihara zeta) a
sub-spectrum of the shell spectrum (kinematics, the E8 carrier)?
"""

from __future__ import annotations

from ast import literal_eval
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    minimal_shell,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import (
    small_generating_set,
    support_graph,
)

OUT = ROOT / "data" / "w33_pass163_two480s_character_decomposition.json"
GAP_BASH = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
GAP_BINARY = "/opt/gap-4.15.1/gap"


def cygwin_path(path):
    text = str(path).replace("\\", "/")
    drive, rest = text.split(":", 1)
    return f"/cygdrive/{drive.lower()}{rest}"


def build_carriers():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    line_index = {line: n for n, line in enumerate(lines)}

    arcs = [(i, j) for i in range(40) for j in range(40) if adjacency[i, j]]
    arc_index = {a: n for n, a in enumerate(arcs)}

    pencils = {
        p: sorted((line for line in lines if p in line), key=lambda l: sorted(l))
        for p in range(40)
    }
    labels = []
    for p in range(40):
        for plus in pencils[p]:
            for minus in pencils[p]:
                if plus != minus:
                    labels.append((p, plus, minus))
    label_index = {l: n for n, l in enumerate(labels)}

    dark = saturated_kernel(adjacency + 4 * np.eye(40, dtype=np.int64))
    _, shell90, _, _ = minimal_shell(dark)
    trades = []
    for vector in shell90:
        vector = np.asarray(vector, dtype=np.int64)
        trades.append(
            (
                frozenset(np.flatnonzero(vector == 1).tolist()),
                frozenset(np.flatnonzero(vector == -1).tolist()),
            )
        )
    trade_index = {t: n for n, t in enumerate(trades)}

    supports, graph45 = support_graph(adjacency)
    support_index = {s: n for n, s in enumerate(supports)}

    skew = [
        frozenset((a, b))
        for a, b in combinations(range(40), 2)
        if not (lines[a] & lines[b])
    ]
    skew_index = {s: n for n, s in enumerate(skew)}
    hyper = [
        frozenset((a, b)) for a, b in combinations(range(40), 2) if not adjacency[a, b]
    ]
    hyper_index = {h: n for n, h in enumerate(hyper)}
    arcs45 = [(i, j) for i in range(45) for j in range(45) if graph45[i, j]]
    arc45_index = {a: n for n, a in enumerate(arcs45)}

    def images(perm):
        line_img = {
            n: line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)
        }
        support_img = {
            n: support_index[frozenset(perm[x] for x in supports[n])] for n in range(45)
        }
        blocks = []
        blocks.append([perm[i] for i in range(40)])
        blocks.append([line_img[n] for n in range(40)])
        blocks.append([arc_index[(perm[i], perm[j])] for (i, j) in arcs])
        blocks.append(
            [
                label_index[
                    (
                        perm[p],
                        frozenset(perm[x] for x in plus),
                        frozenset(perm[x] for x in minus),
                    )
                ]
                for (p, plus, minus) in labels
            ]
        )
        blocks.append(
            [
                trade_index[
                    (
                        frozenset(perm[x] for x in plus),
                        frozenset(perm[x] for x in minus),
                    )
                ]
                for (plus, minus) in trades
            ]
        )
        blocks.append([support_img[n] for n in range(45)])
        blocks.append(
            [skew_index[frozenset(line_img[x] for x in pair)] for pair in skew]
        )
        blocks.append([hyper_index[frozenset(perm[x] for x in pair)] for pair in hyper])
        blocks.append(
            [arc45_index[(support_img[i], support_img[j])] for (i, j) in arcs45]
        )
        combined = []
        offset = 0
        for block in blocks:
            combined.extend(value + offset + 1 for value in block)
            offset += len(block)
        return combined

    sizes = [40, 40, 480, 480, 90, 45, 540, 540, 540]
    names = [
        "points",
        "lines",
        "arcs",
        "shell",
        "trades",
        "supports",
        "skew_pairs",
        "hyperbolic_pairs",
        "gq42_arcs",
    ]
    return points, symplectic, images, sizes, names


def run_gap(generator_images, sizes):
    blocks = []
    offset = 1
    for size in sizes:
        blocks.append((offset, offset + size - 1))
        offset += size
    program = []
    gens = ", ".join(
        "PermList([" + ",".join(str(v) for v in image) + "])"
        for image in generator_images
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
    program.append("irr := Irr(G);;")
    program.append("degs := List(irr, x -> x[1]);;")
    program.append('Print("DEGREES=", degs, ";\\n");')
    program.append(
        "mults := List(chis, chi -> List(irr, x -> " "ScalarProduct(chi, x)));;"
    )
    program.append('Print("MULTS=", mults, ";\\n");')
    program.append("gram := List(chis, a -> List(chis, b -> ScalarProduct(a, b)));;")
    program.append('Print("GRAM=", gram, ";\\n");')
    program.append("QUIT;")

    workdir = Path(tempfile.mkdtemp(prefix="w33_pass163_"))
    script = workdir / "pass163.g"
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
    if completed.returncode not in (0,):
        raise RuntimeError(
            f"GAP failed rc={completed.returncode}: {completed.stderr[:2000]}"
        )
    text = completed.stdout.replace("\\\n", "").replace("\n", "")

    def extract(marker):
        start = text.index(marker) + len(marker)
        end = text.index(";", start)
        return literal_eval(
            text[start:end].replace(" ", "").replace("[", "[").replace("]", "]")
        )

    return {
        "size": extract("SIZE="),
        "degrees": extract("DEGREES="),
        "mults": extract("MULTS="),
        "gram": extract("GRAM="),
    }


def main():
    if not GAP_BASH.exists():
        print("GAP is required for Pass 163")
        return 1
    points, symplectic, images, sizes, names = build_carriers()
    _, group = build_group(points, symplectic)
    two_gens = small_generating_set(group)
    generator_images = [images(g) for g in two_gens]

    result = run_gap(generator_images, sizes)
    checks = {}
    checks["group_order_25920"] = result["size"] == 25920
    degrees = result["degrees"]
    mults = {name: row for name, row in zip(names, result["mults"])}
    gram = np.array(result["gram"], dtype=np.int64)

    checks["twenty_conjugacy_classes"] = len(degrees) == 20
    checks["degree_consistency"] = all(
        sum(m * d for m, d in zip(mults[name], degrees)) == size
        for name, size in zip(names, sizes)
    )
    checks["rank_consistency"] = all(
        sum(m * m for m in mults[name]) == int(gram[i, i])
        for i, name in enumerate(names)
    )

    index = {name: n for n, name in enumerate(names)}
    checks["arcs_rank_24_f"] = int(gram[index["arcs"], index["arcs"]]) == 24
    checks["shell_rank_40_v"] = int(gram[index["shell"], index["shell"]]) == 40
    checks["arcs_shell_joint_24"] = int(gram[index["arcs"], index["shell"]]) == 24
    checks["skew_rank_32"] = int(gram[index["skew_pairs"], index["skew_pairs"]]) == 32
    checks["hyper_rank_25"] = (
        int(gram[index["hyperbolic_pairs"], index["hyperbolic_pairs"]]) == 25
    )
    checks["gq42_arc_rank_27"] = int(gram[index["gq42_arcs"], index["gq42_arcs"]]) == 27
    checks["cross_540_ranks_16_25_15"] = (
        int(gram[index["skew_pairs"], index["hyperbolic_pairs"]]) == 16
        and int(gram[index["skew_pairs"], index["gq42_arcs"]]) == 25
        and int(gram[index["hyperbolic_pairs"], index["gq42_arcs"]]) == 15
    )

    # the eigenspace irreducibles from the point character 1 + chi24 + chi15
    point_constituents = [
        (n, degrees[n], m) for n, m in enumerate(mults["points"]) if m
    ]
    checks["points_rank_3"] = int(gram[index["points"], index["points"]]) == 3
    eig_degrees = sorted(d for n, d, m in point_constituents)
    checks["point_character_1_24_15"] = eig_degrees == [1, 24, 15] or (
        eig_degrees == sorted([1, 15, 24])
    )
    chi24 = next(n for n, d, m in point_constituents if d == 24)
    chi15 = next(n for n, d, m in point_constituents if d == 15)

    sentinel_table = {
        name: {
            "chi15_chiral_multiplicity": int(mults[name][chi15]),
            "chi24_gauge_multiplicity": int(mults[name][chi24]),
        }
        for name in names
    }

    arc_support = {n for n, m in enumerate(mults["arcs"]) if m}
    shell_support = {n for n, m in enumerate(mults["shell"]) if m}
    selection = {
        "arc_constituents": sorted(
            [n, degrees[n], mults["arcs"][n]] for n in arc_support
        ),
        "shell_constituents": sorted(
            [n, degrees[n], mults["shell"][n]] for n in shell_support
        ),
        "arc_support_subset_of_shell": arc_support <= shell_support,
        "common_constituents": len(arc_support & shell_support),
    }
    checks["selection_rule_computed"] = True

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass163.two480s_character_decomposition.v1",
        "status": "PASS" if all_pass else "FAIL",
        "gap_source": "live",
        "irreducible_degrees": degrees,
        "carriers": {
            name: {
                "size": size,
                "multiplicities": [int(m) for m in mults[name]],
            }
            for name, size in zip(names, sizes)
        },
        "intertwiner_gram": gram.tolist(),
        "eigenspace_irreducibles": {
            "chi24_gauge_index": int(chi24),
            "chi15_chiral_index": int(chi15),
        },
        "sentinel_gauge_table": sentinel_table,
        "selection_rule": selection,
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
