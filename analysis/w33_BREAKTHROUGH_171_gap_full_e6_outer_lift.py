"""W(3,3) BREAKTHROUGH 171: GAP full E6 outer lift.

BT170 proved that the compiler generators act on the 45-point GQ(4,2)
quotient through the projective/index-2 E6 half of order 25920.  That left a
precise gap: where is the missing factor of 2 needed for the full W(E6) action?

BT171 uses GAP's primitive degree-45 group library to close that gap.  The
compiler image is conjugate to PrimitiveGroup(45,4) = O(5,3).  The unique
library overgroup PrimitiveGroup(45,5) = O(5,3):C2 pulls back to a
line-preserving group on the same 45 quotient points with order 51840.

It also gives an explicit outer involution.  Adding that one order-2
permutation to the compiler image lifts the action from 25920 to 51840:

    <compiler action, outer involution> = full W(E6) action.

The outer witness is explicit, but not yet intrinsic.  The next target is to
derive the same involution from the W(3,3) / Q8 / octonion feedback architecture
without appealing to GAP's primitive-group atlas.
"""

from __future__ import annotations

from collections import Counter
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

from analysis.w33_BREAKTHROUGH_170_gap_projective_e6_stabilizer_cascade import (  # noqa: E402
    F4_WEYL_ORDER,
    PROJECTIVE_E6_ORDER,
    W_D5_ORDER,
    W_E6_ORDER,
    _coset_action_and_lines,
    _gap_lines,
    _gap_perm_list,
    _parse_gap_list,
    _parse_int,
)


def _parse_bool(output: str, key: str) -> bool:
    match = re.search(rf"{re.escape(key)}=(true|false)", output)
    if not match:
        raise RuntimeError(f"could not parse {key} from GAP output:\n{output}")
    return match.group(1) == "true"


def _parse_text(output: str, key: str) -> str:
    match = re.search(rf"{re.escape(key)}=([^\n]+)", output)
    if not match:
        raise RuntimeError(f"could not parse {key} from GAP output:\n{output}")
    return match.group(1)


def _parse_outer_list(output: str) -> list[int]:
    match = re.search(r"OUTER_LIST=\[(.*?)\]\s*\nFULL_GEN_ORDERS=", output, re.S)
    if not match:
        raise RuntimeError(f"could not parse OUTER_LIST from GAP output:\n{output}")
    return [int(value) - 1 for value in re.findall(r"\d+", match.group(1))]


def _cycle_structure(permutation: list[int]) -> dict:
    seen = set()
    lengths = []
    fixed_points = []
    transpositions = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        lengths.append(len(cycle))
        if len(cycle) == 1:
            fixed_points.append(cycle[0])
        elif len(cycle) == 2:
            transpositions.append(cycle)

    return {
        "cycle_length_distribution": dict(sorted(Counter(lengths).items())),
        "fixed_points": fixed_points,
        "transpositions": transpositions,
    }


def _gap_script(permutations: list[list[int]], lines: list[tuple[int, ...]]) -> str:
    return f"""
Gens := {_gap_perm_list(permutations)};;
Lines := {_gap_lines(lines)};;
LineSets := Set(List(Lines, l -> Set(l)));;
G := Group(Gens);;
S := SymmetricGroup(45);;
H4 := PrimitiveGroup(45,4);;
H5 := PrimitiveGroup(45,5);;
Preserves := function(gens)
  return ForAll(gens, g -> Set(List(LineSets, l -> Set(List(l, x -> x^g)))) = LineSets);
end;;
Print("GAP_VERSION=", GAPInfo.Version, "\\n");
Print("PROJECTIVE_ORDER=", Size(G), "\\n");
Print("H4_ORDER=", Size(H4), "\\n");
Print("H5_ORDER=", Size(H5), "\\n");
Print("H4_STRUCTURE=", StructureDescription(H4), "\\n");
Print("H5_STRUCTURE=", StructureDescription(H5), "\\n");
Print("IS_CONJUGATE_H4=", IsConjugate(S,G,H4), "\\n");
Print("H4_SUBGROUP_H5=", IsSubgroup(H5,H4), "\\n");
c := RepresentativeAction(S,G,H4);;
Full := H5^(c^-1);;
FullGens := GeneratorsOfGroup(Full);;
outer := First(Elements(Full), x -> not x in G);;
Lift := Group(Concatenation(Gens, [outer]));;
LineActionFull := Action(Full, LineSets, OnSets);;
Print("FULL_ORDER=", Size(Full), "\\n");
Print("PROJECTIVE_SUBGROUP_FULL=", IsSubgroup(Full,G), "\\n");
Print("FULL_PRESERVES_LINES=", Preserves(FullGens), "\\n");
Print("LIFT_ORDER=", Size(Lift), "\\n");
Print("LIFT_PRESERVES_LINES=", Preserves(GeneratorsOfGroup(Lift)), "\\n");
Print("FULL_POINT_ORBIT=", Length(Orbit(Full,1)), "\\n");
Print("FULL_POINT_STAB=", Size(Stabilizer(Full,1)), "\\n");
Print("FULL_LINE_ACTION_SIZE=", Size(LineActionFull), "\\n");
Print("FULL_LINE_ORBIT=", Length(Orbit(LineActionFull,1)), "\\n");
Print("FULL_LINE_STAB=", Size(Stabilizer(LineActionFull,1)), "\\n");
Print("FULL_RANK_POINT_ORBITS=", SortedList(List(Orbits(Stabilizer(Full,1), [1..45]), Length)), "\\n");
Print("OUTER_ORDER=", Order(outer), "\\n");
Print("OUTER_IN_PROJECTIVE=", outer in G, "\\n");
Print("OUTER_LIST=", ListPerm(outer,45), "\\n");
Print("FULL_GEN_ORDERS=", List(FullGens,Order), "\\n");
QUIT;
"""


def _run_gap_full_lift(permutations: list[list[int]], lines: list[tuple[int, ...]]) -> dict:
    gap_path = shutil.which("gap")
    if gap_path is None:
        raise RuntimeError("GAP executable not found")

    with tempfile.TemporaryDirectory(prefix="w33_gap_bt171_") as tmp:
        script_path = Path(tmp) / "full_lift.g"
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
    outer = _parse_outer_list(output)
    cycle_structure = _cycle_structure(outer)
    return {
        "gap_version": _parse_text(output, "GAP_VERSION"),
        "projective_order": _parse_int(output, "PROJECTIVE_ORDER"),
        "h4_order": _parse_int(output, "H4_ORDER"),
        "h5_order": _parse_int(output, "H5_ORDER"),
        "h4_structure": _parse_text(output, "H4_STRUCTURE"),
        "h5_structure": _parse_text(output, "H5_STRUCTURE"),
        "is_conjugate_h4": _parse_bool(output, "IS_CONJUGATE_H4"),
        "h4_subgroup_h5": _parse_bool(output, "H4_SUBGROUP_H5"),
        "full_order": _parse_int(output, "FULL_ORDER"),
        "projective_subgroup_full": _parse_bool(output, "PROJECTIVE_SUBGROUP_FULL"),
        "full_preserves_lines": _parse_bool(output, "FULL_PRESERVES_LINES"),
        "lift_order": _parse_int(output, "LIFT_ORDER"),
        "lift_preserves_lines": _parse_bool(output, "LIFT_PRESERVES_LINES"),
        "full_point_orbit": _parse_int(output, "FULL_POINT_ORBIT"),
        "full_point_stabilizer": _parse_int(output, "FULL_POINT_STAB"),
        "full_line_action_order": _parse_int(output, "FULL_LINE_ACTION_SIZE"),
        "full_line_orbit": _parse_int(output, "FULL_LINE_ORBIT"),
        "full_line_stabilizer": _parse_int(output, "FULL_LINE_STAB"),
        "full_point_stabilizer_suborbits": _parse_gap_list(output, "FULL_RANK_POINT_ORBITS"),
        "outer_order": _parse_int(output, "OUTER_ORDER"),
        "outer_in_projective": _parse_bool(output, "OUTER_IN_PROJECTIVE"),
        "outer_permutation": outer,
        "outer_cycle_structure": cycle_structure,
        "full_generator_orders": _parse_gap_list(output, "FULL_GEN_ORDERS"),
        "gap_output_excerpt": "\n".join(output.strip().splitlines()[:24]),
    }


def gap_full_e6_outer_lift_packet() -> dict:
    action = _coset_action_and_lines()
    gap = _run_gap_full_lift(action["permutations"], action["lines"])

    cycle_dist = gap["outer_cycle_structure"]["cycle_length_distribution"]
    checks = {
        "projective_order_is_bt170_half": gap["projective_order"] == PROJECTIVE_E6_ORDER,
        "gap_h4_is_same_order_as_projective": gap["h4_order"] == PROJECTIVE_E6_ORDER,
        "gap_h5_is_full_w_e6_order": gap["h5_order"] == W_E6_ORDER,
        "compiler_image_conjugate_to_gap_h4": gap["is_conjugate_h4"] is True,
        "gap_h4_sits_inside_gap_h5": gap["h4_subgroup_h5"] is True,
        "pulled_back_full_order_is_w_e6": gap["full_order"] == W_E6_ORDER,
        "projective_subgroup_has_index_two": gap["projective_subgroup_full"] is True
        and gap["full_order"] // gap["projective_order"] == 2,
        "full_group_preserves_gq_lines": gap["full_preserves_lines"] is True,
        "compiler_plus_outer_generates_full_group": gap["lift_order"] == W_E6_ORDER,
        "compiler_plus_outer_preserves_lines": gap["lift_preserves_lines"] is True,
        "full_point_action_is_transitive": gap["full_point_orbit"] == 45,
        "full_point_stabilizer_is_w_f4": gap["full_point_stabilizer"] == F4_WEYL_ORDER,
        "full_line_action_is_faithful": gap["full_line_action_order"] == W_E6_ORDER,
        "full_line_action_is_transitive": gap["full_line_orbit"] == 27,
        "full_line_stabilizer_is_w_d5": gap["full_line_stabilizer"] == W_D5_ORDER,
        "full_rank_three_suborbits_are_1_12_32": gap["full_point_stabilizer_suborbits"] == [1, 12, 32],
        "outer_witness_is_order_two": gap["outer_order"] == 2,
        "outer_witness_is_not_projective": gap["outer_in_projective"] is False,
        "outer_witness_is_permutation": sorted(gap["outer_permutation"]) == list(range(45)),
        "outer_cycle_shape_is_7_fixed_19_transpositions": cycle_dist == {1: 7, 2: 19},
    }

    return {
        "breakthrough": 171,
        "title": "GAP full E6 outer lift",
        "gap_version": gap["gap_version"],
        "projective_order": gap["projective_order"],
        "full_order": gap["full_order"],
        "h4_structure": gap["h4_structure"],
        "h5_structure": gap["h5_structure"],
        "point_count": 45,
        "line_count": 27,
        "full_point_stabilizer": gap["full_point_stabilizer"],
        "full_line_stabilizer": gap["full_line_stabilizer"],
        "full_point_stabilizer_suborbits": gap["full_point_stabilizer_suborbits"],
        "outer_order": gap["outer_order"],
        "outer_permutation_zero_based": gap["outer_permutation"],
        "outer_permutation_one_based": [point + 1 for point in gap["outer_permutation"]],
        "outer_cycle_structure_zero_based": gap["outer_cycle_structure"],
        "full_generator_orders": gap["full_generator_orders"],
        "gap_output_excerpt": gap["gap_output_excerpt"],
        "architectural_reading": (
            "GAP identifies the BT170 projective compiler image with the "
            "degree-45 primitive group O(5,3), then pulls back the overgroup "
            "O(5,3):C2 to the same quotient labels. The pulled-back overgroup "
            "preserves the 27 GQ(4,2) lines, has order 51840, point stabilizer "
            "1152, line stabilizer 1920, and is generated by the compiler "
            "image plus one explicit order-2 outer involution. This closes the "
            "finite W(E6) stabilizer cascade for the 45-point quotient."
        ),
        "boundary": (
            "The outer involution is an explicit GAP primitive-library witness. "
            "The intrinsic W(3,3) construction of the same involution remains "
            "the next target, likely through the Q8/octonion/J3(O) feedback loop."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = gap_full_e6_outer_lift_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 171: GAP FULL E6 OUTER LIFT")
    print("=" * 78)
    print()
    print(f"GAP version             = {packet['gap_version']}")
    print(f"projective order        = {packet['projective_order']}")
    print(f"full order              = {packet['full_order']}")
    print(f"H4 structure            = {packet['h4_structure']}")
    print(f"H5 structure            = {packet['h5_structure']}")
    print(f"point stabilizer        = {packet['full_point_stabilizer']}")
    print(f"line stabilizer         = {packet['full_line_stabilizer']}")
    print(f"outer order             = {packet['outer_order']}")
    print(f"outer cycle structure   = {packet['outer_cycle_structure_zero_based']['cycle_length_distribution']}")
    print(f"verified                = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")
    print()
    print("BOUNDARY:")
    print(f"  {packet['boundary']}")

    out = Path("data") / "w33_BREAKTHROUGH_171_gap_full_e6_outer_lift.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
