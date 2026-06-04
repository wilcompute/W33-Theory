"""W(3,3) BREAKTHROUGH 169: GAP F4/center-quad crosswalk.

BT168 proved that the F4-normalizer quotient of the compiler group realizes
GQ(4,2).  TheTheory.txt points out that the older center-quad quotient already
realizes the same 45-point / 27-line geometry directly from W(3,3).

This verifier uses GAP, as requested, to find an explicit line-preserving
isomorphism between those two quotient geometries:

    F4-normalizer coset quotient  <->  W33 center-quad quotient.

The witness is not claimed canonical or unique.  It is an explicit GAP
crosswalk proving the two independently reconstructed geometries are the same
finite incidence object.
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

from analysis.w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import (  # noqa: E402
    five_cliques,
    quotient_adjacency,
)
from exploration.w33_center_quad_gq42_e6_bridge import quotient_incidence  # noqa: E402


def center_quad_adjacency_and_lines() -> tuple[list[list[bool]], list[tuple[int, ...]]]:
    _point_to_lines, line_to_points = quotient_incidence()
    lines = [tuple(points) for _line_id, points in sorted(line_to_points.items())]
    adjacency = [[False] * 45 for _ in range(45)]
    for line in lines:
        for left, right in combinations(line, 2):
            adjacency[left][right] = True
            adjacency[right][left] = True
    return adjacency, lines


def _gap_bool_matrix(matrix: list[list[bool]]) -> str:
    return (
        "["
        + ",".join(
            "[" + ",".join("true" if entry else "false" for entry in row) + "]"
            for row in matrix
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


def _gap_script(
    source_adjacency: list[list[bool]],
    target_adjacency: list[list[bool]],
    source_lines: list[tuple[int, ...]],
    target_lines: list[tuple[int, ...]],
) -> str:
    return f"""
A := {_gap_bool_matrix(source_adjacency)};;
B := {_gap_bool_matrix(target_adjacency)};;
LinesA := {_gap_lines(source_lines)};;
LinesB := {_gap_lines(target_lines)};;
n := 45;;
img := List([1..n], i -> 0);;
pre := List([1..n], i -> 0);;
img[1] := 1;; pre[1] := 1;;

IsCompatible := function(v,t)
  local u,tu;
  if pre[t] <> 0 then return false; fi;
  for u in [1..n] do
    tu := img[u];
    if tu <> 0 then
      if A[v][u] <> B[t][tu] then return false; fi;
    fi;
  od;
  return true;
end;;

Candidates := function(v)
  return Filtered([1..n], t -> IsCompatible(v,t));
end;;

ChooseVertex := function()
  local best,bestc,v,c;
  best := 0; bestc := 10^9;
  for v in [1..n] do
    if img[v] = 0 then
      c := Length(Candidates(v));
      if c < bestc then best := v; bestc := c; fi;
      if c = 0 then return v; fi;
    fi;
  od;
  return best;
end;;

LineSet := function(lines)
  return Set(List(lines, l -> Set(l)));
end;;

PreservesLines := function(mapping)
  local mapped;
  mapped := Set(List(LinesA, l -> Set(List(l, x -> mapping[x]))));
  return mapped = LineSet(LinesB);
end;;

W33Search := function(depth)
  local v,cands,t,recursive_result;
  if depth = n then
    if PreservesLines(img) then return ShallowCopy(img); fi;
    return fail;
  fi;
  v := ChooseVertex();
  cands := Candidates(v);
  for t in cands do
    img[v] := t; pre[t] := v;
    recursive_result := W33Search(depth+1);
    if recursive_result <> fail then return recursive_result; fi;
    img[v] := 0; pre[t] := 0;
  od;
  return fail;
end;;

Print("GAP_VERSION=", GAPInfo.Version, "\\n");
W33IsoResult := W33Search(1);;
if W33IsoResult = fail then
  Print("NO_ISOMORPHISM\\n");
else
  Print("ISOMORPHISM_FOUND\\n");
  Print(W33IsoResult, "\\n");
  Print("LINES_PRESERVED=", PreservesLines(W33IsoResult), "\\n");
fi;
QUIT;
"""


def _run_gap(script: str) -> tuple[str, list[int]]:
    gap_path = shutil.which("gap")
    if gap_path is None:
        raise RuntimeError("GAP executable not found")

    with tempfile.TemporaryDirectory(prefix="w33_gap_iso_") as tmp:
        script_path = Path(tmp) / "crosswalk.g"
        script_path.write_text(script, encoding="utf-8")
        completed = subprocess.run(
            [gap_path, "-q", str(script_path)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=90,
        )

    output = completed.stdout
    if "ISOMORPHISM_FOUND" not in output or "LINES_PRESERVED=true" not in output:
        raise RuntimeError(f"GAP did not return a line-preserving isomorphism:\n{output}")

    mapping_match = re.search(r"ISOMORPHISM_FOUND\s*\n\s*\[(.*?)\]\s*\nLINES_PRESERVED", output, re.S)
    if not mapping_match:
        raise RuntimeError(f"could not parse GAP mapping:\n{output}")
    mapping = [int(value) - 1 for value in re.findall(r"\d+", mapping_match.group(1))]
    if len(mapping) != 45:
        raise RuntimeError(f"expected 45-point mapping, parsed {len(mapping)} entries")
    return output, mapping


def _preserves_adjacency(
    source_adjacency: list[list[bool]],
    target_adjacency: list[list[bool]],
    mapping: list[int],
) -> bool:
    return all(
        source_adjacency[left][right] == target_adjacency[mapping[left]][mapping[right]]
        for left in range(45)
        for right in range(left + 1, 45)
    )


def _preserves_lines(
    source_lines: list[tuple[int, ...]],
    target_lines: list[tuple[int, ...]],
    mapping: list[int],
) -> bool:
    mapped = {tuple(sorted(mapping[point] for point in line)) for line in source_lines}
    target = {tuple(sorted(line)) for line in target_lines}
    return mapped == target


def gap_f4_centerquad_crosswalk_packet() -> dict:
    f4_adjacency, _reps = quotient_adjacency()
    f4_lines = [tuple(line) for line in five_cliques(f4_adjacency)]
    center_adjacency, center_lines = center_quad_adjacency_and_lines()

    script = _gap_script(f4_adjacency, center_adjacency, f4_lines, center_lines)
    gap_output, mapping = _run_gap(script)

    point_image_distribution = Counter(mapping)
    mapped_line_ids = []
    center_line_to_id = {tuple(sorted(line)): index for index, line in enumerate(center_lines)}
    for line in f4_lines:
        mapped_line_ids.append(center_line_to_id[tuple(sorted(mapping[point] for point in line))])

    checks = {
        "gap_found_isomorphism": "ISOMORPHISM_FOUND" in gap_output,
        "gap_preserved_lines": "LINES_PRESERVED=true" in gap_output,
        "mapping_has_45_entries": len(mapping) == 45,
        "mapping_is_permutation": point_image_distribution == Counter(range(45)),
        "python_adjacency_check": _preserves_adjacency(f4_adjacency, center_adjacency, mapping),
        "python_line_check": _preserves_lines(f4_lines, center_lines, mapping),
        "source_and_target_have_27_lines": len(f4_lines) == len(center_lines) == 27,
        "mapped_lines_are_permutation": Counter(mapped_line_ids) == Counter(range(27)),
    }

    return {
        "breakthrough": 169,
        "title": "GAP F4/center-quad quotient crosswalk",
        "gap_version": re.search(r"GAP_VERSION=([^\n]+)", gap_output).group(1),
        "source": "F4-normalizer coset quotient from BT168",
        "target": "W33 center-quad quotient from exploration/w33_center_quad_gq42_e6_bridge.py",
        "point_mapping_f4_to_centerquad": mapping,
        "line_mapping_f4_to_centerquad": mapped_line_ids,
        "point_count": 45,
        "line_count": 27,
        "incidence_count": 135,
        "gap_output_excerpt": "\n".join(gap_output.strip().splitlines()[:6]),
        "architectural_reading": (
            "GAP gives an explicit line-preserving isomorphism from the new "
            "F4-normalizer compiler quotient to the older W33 center-quad "
            "quotient. Therefore BT167/168 and the center-quad bridge are not "
            "merely parameter twins: they are the same finite 45-point / "
            "27-line GQ(4,2) incidence object up to the displayed witness."
        ),
        "boundary": (
            "The mapping is an explicit GAP witness, not a proof of uniqueness "
            "or a canonical labeling. It anchors the compiler quotient to the "
            "center-quad quotient; Witting packet equivalence is already covered "
            "by the existing packet quotient audit."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = gap_f4_centerquad_crosswalk_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 169: GAP F4/CENTER-QUAD CROSSWALK")
    print("=" * 78)
    print()
    print(f"GAP version       = {packet['gap_version']}")
    print(f"point count       = {packet['point_count']}")
    print(f"line count        = {packet['line_count']}")
    print(f"incidence count   = {packet['incidence_count']}")
    print(f"first 12 images   = {packet['point_mapping_f4_to_centerquad'][:12]}")
    print(f"verified          = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_169_gap_f4_centerquad_crosswalk.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
