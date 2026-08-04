#!/usr/bin/env python3
"""Exact PSp(4,3) decomposition of the 720 minimum-defect support carrier.

The support patterns are the 720 undirected edges of the 45-block
SRG(45,32,22,24): the 240 filled triangles partition those edges three at a
time.  This script constructs the literal action, hands its two generators to
GAP, and freezes the irreducible multiplicities and orbital rank.
"""
from __future__ import annotations

from ast import literal_eval
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

import numpy as np

from analysis.w33_pass158_chiral_trade_lattice_two_480s import build_group, build_w33
from analysis.w33_pass161_gq42_ihara_inheritance import small_generating_set, support_graph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT3381_MINIMUM_DEFECT_EDGE_CHARACTER_results.json"


def build_edge_carrier():
    points, adjacency, symplectic = build_w33()
    supports, graph45 = support_graph(adjacency)
    support_index = {support: index for index, support in enumerate(supports)}
    edges = [
        (i, j)
        for i in range(45)
        for j in range(i + 1, 45)
        if graph45[i, j]
    ]
    assert len(edges) == 720
    edge_index = {edge: index for index, edge in enumerate(edges)}

    _, group = build_group(points, symplectic)
    generators = small_generating_set(group)
    assert len(generators) == 2

    images = []
    for perm in generators:
        support_image = [
            support_index[frozenset(perm[x] for x in support)]
            for support in supports
        ]
        edge_image = []
        for i, j in edges:
            a, b = sorted((support_image[i], support_image[j]))
            edge_image.append(edge_index[(a, b)] + 1)
        images.append(edge_image)
    return images


def run_gap(images):
    gap = shutil.which("gap")
    if gap is None:
        raise RuntimeError("GAP executable is required")
    gens = ", ".join(
        "PermList([" + ",".join(map(str, image)) + "])" for image in images
    )
    program = f"""
gens := [ {gens} ];;
G := Group(gens);;
chi := PermutationCharacter(G,[1..720],OnPoints);;
irr := Irr(G);;
degrees := List(irr,x->x[1]);;
mults := List(irr,x->ScalarProduct(chi,x));;
rank := ScalarProduct(chi,chi);;
subdegrees := List(Orbits(Stabilizer(G,1),[1..720]),Length);;
Sort(subdegrees);
Print("SIZE=",Size(G),";\\n");
Print("DEGREES=",degrees,";\\n");
Print("MULTS=",mults,";\\n");
Print("RANK=",rank,";\\n");
Print("SUBDEGREES=",subdegrees,";\\n");
QUIT;
"""
    with tempfile.TemporaryDirectory(prefix="bt3381_gap_") as directory:
        path = Path(directory) / "bt3381.g"
        path.write_text(program, encoding="ascii")
        completed = subprocess.run(
            [gap, "-q", str(path)],
            capture_output=True,
            text=True,
            timeout=1200,
            check=False,
        )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-4000:])
    text = completed.stdout.replace("\\\n", "").replace("\n", "")

    def extract(marker):
        start = text.index(marker) + len(marker)
        end = text.index(";", start)
        return literal_eval(text[start:end].replace(" ", ""))

    return {
        "group_order": extract("SIZE="),
        "irreducible_degrees": extract("DEGREES="),
        "multiplicities": extract("MULTS="),
        "orbital_rank": extract("RANK="),
        "subdegrees": extract("SUBDEGREES="),
    }


def build_certificate():
    result = run_gap(build_edge_carrier())
    degrees = result["irreducible_degrees"]
    multiplicities = result["multiplicities"]
    checks = {
        "group_order_25920": result["group_order"] == 25920,
        "twenty_irreducibles": len(degrees) == 20,
        "degree_720": sum(d * m for d, m in zip(degrees, multiplicities)) == 720,
        "rank_matches_multiplicity_squares": (
            sum(m * m for m in multiplicities) == result["orbital_rank"]
        ),
        "transitive": result["subdegrees"][0] == 1,
        "subdegrees_sum_720": sum(result["subdegrees"]) == 720,
    }
    assert all(checks.values())
    return {
        "schema": "w33.bt3381.minimum_defect_edge_character.v1",
        "status": "PASS",
        "carrier": "720 undirected edges of SRG(45,32,22,24)",
        **result,
        "constituents": [
            {"index": index, "degree": degree, "multiplicity": multiplicity}
            for index, (degree, multiplicity) in enumerate(zip(degrees, multiplicities))
            if multiplicity
        ],
        "checks": checks,
    }


def main():
    payload = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
