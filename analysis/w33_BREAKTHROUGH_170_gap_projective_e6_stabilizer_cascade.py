"""W(3,3) BREAKTHROUGH 170: GAP projective E6 stabilizer cascade.

BT167/168 proved that the F4-normalizer quotient has 45 points and the
GQ(4,2) line geometry.  BT169 identified that quotient with the older
center-quad quotient.

BT170 uses GAP on the actual 45-point coset action induced by the compiler
generators.  The result is the honest stabilizer cascade:

    |image(G)| = 25920 = |Sp(4,3)| / 2 = |W(E6)| / 2
    point stabilizer = 576 = |W(F4)| / 2
    line stabilizer  = 960 = |W(D5)| / 2

The action is transitive on the 45 points and 27 GQ(4,2) lines, preserves
the line geometry, and has point-stabilizer suborbits 1+12+32.

So the compiler quotient has already reached the projective/index-2 E6 Weyl
half.  The missing factor of 2 is not swept under the rug: it is the next
outer-duality/reflection target needed to lift the projective action to the
full W(E6) action.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (  # noqa: E402
    GROUP_ORDER,
    build_group,
    generator_set,
    mat_inv,
    mat_mul,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import (  # noqa: E402
    macro_tail_sieve_packet,
)
from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    F4_WEYL_ORDER,
    closure_generated_by,
)
from analysis.w33_BREAKTHROUGH_167_f4_e6_rank3_coset_quotient import (  # noqa: E402
    K,
    double_coset_orbits,
    left_cosets,
)
from analysis.w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import (  # noqa: E402
    five_cliques,
)


PROJECTIVE_E6_ORDER = 25_920
W_E6_ORDER = 51_840
W_D5_ORDER = 1_920


def _forbidden_macros() -> list[tuple[tuple[int, ...], ...]]:
    """Load the BT158 forbidden macros, recomputing only if the artifact is absent."""

    artifact = ROOT / "data" / "w33_BREAKTHROUGH_158_macro_tail_sieve.json"
    if artifact.exists():
        packet = json.loads(artifact.read_text(encoding="utf-8"))
    else:
        packet = macro_tail_sieve_packet()
    return [
        tuple(tuple(entry for entry in row) for row in item["matrix"])
        for item in packet["forbidden_macros"]
    ]


def _coset_action_and_lines() -> dict:
    generators, _labels = generator_set(include_inverses=True)
    elems, _index, _parent, _parent_gen = build_group(generators)
    forbidden = _forbidden_macros()
    normalizer = closure_generated_by(forbidden)

    reps, _cosets, elem_to_coset = left_cosets(elems, normalizer)
    orbits = double_coset_orbits(reps, elem_to_coset, forbidden)
    coset_to_orbit_size = {
        coset_id: len(orbit) for orbit in orbits for coset_id in orbit
    }

    permutations = [
        [elem_to_coset[mat_mul(rep, generator)] for rep in reps]
        for generator in generators
    ]

    point_count = len(reps)
    adjacency = [[False] * point_count for _ in range(point_count)]
    for left_index, left in enumerate(reps):
        left_inv = mat_inv(left)
        for right_index, right in enumerate(reps):
            if left_index == right_index:
                continue
            relative = mat_mul(right, left_inv)
            if coset_to_orbit_size[elem_to_coset[relative]] == K:
                adjacency[left_index][right_index] = True

    lines = [tuple(line) for line in five_cliques(adjacency)]
    edge_count = sum(sum(row) for row in adjacency) // 2
    degree_distribution = Counter(sum(row) for row in adjacency)
    edge_line_count = Counter()
    for line in lines:
        for edge in combinations(line, 2):
            edge_line_count[tuple(sorted(edge))] += 1

    return {
        "full_group_order": len(elems),
        "normalizer_order": len(normalizer),
        "point_count": point_count,
        "line_count": len(lines),
        "edge_count": edge_count,
        "degree_distribution": dict(sorted(degree_distribution.items())),
        "edge_line_incidence_distribution": dict(
            sorted(Counter(edge_line_count.values()).items())
        ),
        "permutations": permutations,
        "lines": lines,
    }


def _gap_perm_list(permutations: list[list[int]]) -> str:
    return (
        "["
        + ",".join(
            "PermList([" + ",".join(str(point + 1) for point in permutation) + "])"
            for permutation in permutations
        )
        + "]"
    )


def _gap_lines(lines: list[tuple[int, ...]]) -> str:
    return (
        "["
        + ",".join(
            "[" + ",".join(str(point + 1) for point in line) + "]" for line in lines
        )
        + "]"
    )


def _gap_script(permutations: list[list[int]], lines: list[tuple[int, ...]]) -> str:
    return f"""
Gens := {_gap_perm_list(permutations)};;
Lines := {_gap_lines(lines)};;
LineSets := Set(List(Lines, l -> Set(l)));;
G := Group(Gens);;
LineAction := Action(G, LineSets, OnSets);;
Print("GAP_VERSION=", GAPInfo.Version, "\\n");
Print("SIZE=", Size(G), "\\n");
Print("POINT_ORBIT=", Length(Orbit(G,1)), "\\n");
Print("POINT_STAB=", Size(Stabilizer(G,1)), "\\n");
Print("LINE_ACTION_SIZE=", Size(LineAction), "\\n");
Print("LINE_ORBIT=", Length(Orbit(LineAction,1)), "\\n");
Print("LINE_STAB=", Size(Stabilizer(LineAction,1)), "\\n");
Print("RANK_POINT_ORBITS=", SortedList(List(Orbits(Stabilizer(G,1), [1..45]), Length)), "\\n");
Print("PRESERVES_LINES=", ForAll(Gens, g -> Set(List(LineSets, l -> Set(List(l, x -> x^g)))) = LineSets), "\\n");
Print("GENERATOR_COUNT=", Length(Gens), "\\n");
Print("GENERATOR_ORDERS=", List(Gens, Order), "\\n");
QUIT;
"""


def _parse_int(output: str, key: str) -> int:
    match = re.search(rf"{re.escape(key)}=(\d+)", output)
    if not match:
        raise RuntimeError(f"could not parse {key} from GAP output:\n{output}")
    return int(match.group(1))


def _parse_gap_list(output: str, key: str) -> list[int]:
    match = re.search(rf"{re.escape(key)}=\[(.*?)\]", output)
    if not match:
        raise RuntimeError(f"could not parse {key} from GAP output:\n{output}")
    return [int(value) for value in re.findall(r"\d+", match.group(1))]


def _run_gap(permutations: list[list[int]], lines: list[tuple[int, ...]]) -> dict:
    gap_path = shutil.which("gap")
    if gap_path is None:
        raise RuntimeError("GAP executable not found")

    with tempfile.TemporaryDirectory(prefix="w33_gap_bt170_") as tmp:
        script_path = Path(tmp) / "coset_action.g"
        script_path.write_text(_gap_script(permutations, lines), encoding="utf-8")
        completed = subprocess.run(
            [gap_path, "-q", str(script_path)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
        )

    output = completed.stdout
    version = re.search(r"GAP_VERSION=([^\n]+)", output)
    if version is None:
        raise RuntimeError(f"could not parse GAP version:\n{output}")

    return {
        "gap_version": version.group(1),
        "image_order": _parse_int(output, "SIZE"),
        "point_orbit": _parse_int(output, "POINT_ORBIT"),
        "point_stabilizer": _parse_int(output, "POINT_STAB"),
        "line_action_order": _parse_int(output, "LINE_ACTION_SIZE"),
        "line_orbit": _parse_int(output, "LINE_ORBIT"),
        "line_stabilizer": _parse_int(output, "LINE_STAB"),
        "point_stabilizer_suborbits": _parse_gap_list(output, "RANK_POINT_ORBITS"),
        "preserves_lines": "PRESERVES_LINES=true" in output,
        "generator_count": _parse_int(output, "GENERATOR_COUNT"),
        "generator_orders": _parse_gap_list(output, "GENERATOR_ORDERS"),
        "gap_output_excerpt": "\n".join(output.strip().splitlines()[:11]),
    }


def gap_projective_e6_stabilizer_cascade_packet() -> dict:
    action = _coset_action_and_lines()
    gap = _run_gap(action["permutations"], action["lines"])

    kernel_size = action["full_group_order"] // gap["image_order"]
    checks = {
        "full_compiler_group_order_is_w_e6": action["full_group_order"] == GROUP_ORDER == W_E6_ORDER,
        "normalizer_order_is_w_f4": action["normalizer_order"] == F4_WEYL_ORDER == 1152,
        "coset_point_count_is_45": action["point_count"] == 45,
        "gq_line_count_is_27": action["line_count"] == 27,
        "gq_edges_are_270": action["edge_count"] == 270,
        "lines_reconstruct_degree_12_graph": action["degree_distribution"] == {12: 45}
        and action["edge_line_incidence_distribution"] == {1: 270},
        "gap_image_order_is_projective_e6_half": gap["image_order"] == PROJECTIVE_E6_ORDER == W_E6_ORDER // 2,
        "kernel_is_central_twofold": kernel_size == 2,
        "point_action_is_transitive": gap["point_orbit"] == 45,
        "point_stabilizer_is_projective_f4_half": gap["point_stabilizer"] == F4_WEYL_ORDER // 2 == 576,
        "line_action_is_faithful_same_order": gap["line_action_order"] == gap["image_order"],
        "line_action_is_transitive": gap["line_orbit"] == 27,
        "line_stabilizer_is_projective_d5_half": gap["line_stabilizer"] == W_D5_ORDER // 2 == 960,
        "point_orbit_stabilizer_product": gap["point_orbit"] * gap["point_stabilizer"] == gap["image_order"],
        "line_orbit_stabilizer_product": gap["line_orbit"] * gap["line_stabilizer"] == gap["image_order"],
        "rank_three_suborbits_are_1_12_32": gap["point_stabilizer_suborbits"] == [1, 12, 32],
        "compiler_generators_preserve_gq_lines": gap["preserves_lines"] is True,
        "sixteen_order_three_generators": gap["generator_count"] == 16
        and set(gap["generator_orders"]) == {3},
    }

    return {
        "breakthrough": 170,
        "title": "GAP projective E6 stabilizer cascade",
        "full_compiler_group_order": action["full_group_order"],
        "projective_image_order": gap["image_order"],
        "central_kernel_size": kernel_size,
        "normalizer_order": action["normalizer_order"],
        "point_count": action["point_count"],
        "line_count": action["line_count"],
        "point_stabilizer": gap["point_stabilizer"],
        "line_stabilizer": gap["line_stabilizer"],
        "point_stabilizer_suborbits": gap["point_stabilizer_suborbits"],
        "generator_count": gap["generator_count"],
        "generator_orders": gap["generator_orders"],
        "gap_version": gap["gap_version"],
        "gap_output_excerpt": gap["gap_output_excerpt"],
        "stabilizer_cascade": {
            "full_compiler_group": W_E6_ORDER,
            "projective_e6_half": PROJECTIVE_E6_ORDER,
            "central_kernel": 2,
            "projective_f4_point_stabilizer": F4_WEYL_ORDER // 2,
            "projective_d5_line_stabilizer": W_D5_ORDER // 2,
            "point_orbit": 45,
            "line_orbit": 27,
        },
        "architectural_reading": (
            "GAP proves that the compiler generators act on the 45-point "
            "F4-normalizer quotient through a projective/index-2 E6 Weyl half "
            "of order 25920. The action is transitive on the 45 quotient "
            "points and on the 27 GQ(4,2) lines; its point stabilizer has "
            "order 576 and suborbits 1,12,32, while its line stabilizer has "
            "order 960. Thus the repo's F4 pocket, GQ(4,2) quotient, and "
            "E6 tritangent scale are connected by an explicit GAP-verified "
            "projective stabilizer cascade."
        ),
        "boundary": (
            "This packet deliberately does not claim the full W(E6) action on "
            "the quotient. The GAP action has order 25920, so the missing "
            "factor of 2 is an outer-duality/reflection lift that remains the "
            "next target."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = gap_projective_e6_stabilizer_cascade_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 170: GAP PROJECTIVE E6 STABILIZER CASCADE")
    print("=" * 78)
    print()
    print(f"GAP version              = {packet['gap_version']}")
    print(f"full compiler group      = {packet['full_compiler_group_order']}")
    print(f"projective image order   = {packet['projective_image_order']}")
    print(f"central kernel size      = {packet['central_kernel_size']}")
    print(f"point stabilizer         = {packet['point_stabilizer']}")
    print(f"line stabilizer          = {packet['line_stabilizer']}")
    print(f"point suborbits          = {packet['point_stabilizer_suborbits']}")
    print(f"verified                 = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")
    print()
    print("BOUNDARY:")
    print(f"  {packet['boundary']}")

    out = Path("data") / "w33_BREAKTHROUGH_170_gap_projective_e6_stabilizer_cascade.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
