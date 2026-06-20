#!/usr/bin/env python3
"""BT1371: explicit Q6 edge / tomotope flag orbit-coordinate table."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from collections import deque
from pathlib import Path

from bt1368_q6_tomotope_equivariant_flag_lift import (
    Perm,
    build_q6_candidate,
    build_tomotope_aut_group,
    gap_perm_list,
    q6_edges,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1371_q6_tomotope_explicit_orbit_address_table.json"


def orbit_rows(perms: list[Perm], size: int) -> list[list[int]]:
    unseen = set(range(size))
    out = []
    while unseen:
        start = min(unseen)
        orbit = {start}
        frontier = [start]
        while frontier:
            x = frontier.pop()
            for perm in perms:
                y = perm[x]
                if y not in orbit:
                    orbit.add(y)
                    frontier.append(y)
        row = sorted(orbit)
        out.append(row)
        unseen -= orbit
    return sorted(out, key=lambda row: row[0])


def run_gap_iso_table(tom_autos: list[Perm], q6_autos: list[Perm]) -> list[int]:
    script = f"""
Tall := [{','.join(gap_perm_list(p) for p in tom_autos)}];;
Qall := [{','.join(gap_perm_list(p) for p in q6_autos)}];;
T := Group(Tall);;
Q := Group(Qall);;
iso := IsomorphismGroups(T,Q);;
imgs := List(Tall, t -> Position(Qall, Image(iso,t)));;
Print("isomorphic=", iso <> fail, "\\n");
Print("image_indices=");
for i in [1..Length(imgs)] do
  if i > 1 then Print(","); fi;
  Print(imgs[i]);
od;
Print("\\n");
QUIT;
"""
    gap = shutil.which("gap")
    if gap:
        proc = subprocess.run(
            [gap, "-q"],
            input=script,
            text=True,
            capture_output=True,
            check=True,
            timeout=60,
        )
        stdout = proc.stdout
    else:
        gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
        if not gap_bash.exists():
            raise FileNotFoundError("GAP is required for BT1371")
        tmp = ROOT / ".tmp"
        tmp.mkdir(exist_ok=True)
        gfile = tmp / "bt1371_q6_tomotope_iso_table.g"
        gfile.write_text(script, newline="\n")
        drive = str(gfile)[0].lower()
        rest = str(gfile)[2:].replace("\\", "/")
        cyg = f"/cygdrive/{drive}{rest}"
        proc = subprocess.run(
            [str(gap_bash), "--norc", "-c", f"/opt/gap-4.15.1/gap.exe -q -b '{cyg}'"],
            cwd=str(gap_bash.parent),
            text=True,
            capture_output=True,
            check=True,
            timeout=120,
        )
        stdout = proc.stdout
    values = {}
    lines = stdout.splitlines()
    for index, line in enumerate(lines):
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip()
            if (
                key.strip() == "image_indices"
                and len([x for x in value.split(",") if x]) < 96
            ):
                tail = []
                for extra in lines[index + 1 :]:
                    if "=" in extra:
                        break
                    tail.append(extra.strip())
                    if len([x for x in ",".join([value] + tail).split(",") if x]) >= 96:
                        break
                values["image_indices"] = ",".join([value] + tail).strip(",")
    if values.get("isomorphic") != "true":
        raise AssertionError(stdout)
    return [int(x) - 1 for x in values["image_indices"].split(",") if x]


def bits6(x: int) -> str:
    return format(x, "06b")


def build_result() -> dict[str, object]:
    tom_autos, _tom_gens, tom = build_tomotope_aut_group()
    q6_autos, _q6_gens, q6 = build_q6_candidate(tom["order_profile"])  # type: ignore[arg-type]
    image_indices = run_gap_iso_table(tom_autos, q6_autos)
    edges = q6_edges()
    tom_orbits = orbit_rows(tom_autos, 192)
    q6_orbits = orbit_rows(q6_autos, 192)
    if [len(row) for row in tom_orbits] != [96, 96] or [
        len(row) for row in q6_orbits
    ] != [96, 96]:
        raise AssertionError("orbit drift")

    table_by_flag: dict[int, dict[str, object]] = {}
    for orbit_id, (tom_orbit, q6_orbit) in enumerate(zip(tom_orbits, q6_orbits)):
        base_flag = tom_orbit[0]
        base_edge = q6_orbit[0]
        for flag in tom_orbit:
            witnesses = [
                idx for idx, perm in enumerate(tom_autos) if perm[base_flag] == flag
            ]
            if len(witnesses) != 1:
                raise AssertionError((orbit_id, base_flag, flag, witnesses))
            tom_group_index = witnesses[0]
            q_group_index = image_indices[tom_group_index]
            edge_index = q6_autos[q_group_index][base_edge]
            a, b, dim = edges[edge_index]
            table_by_flag[flag] = {
                "tomotope_flag": flag,
                "orbit": orbit_id,
                "tomotope_group_index": tom_group_index,
                "q6_group_index": q_group_index,
                "q6_edge_index": edge_index,
                "q6_direction": dim,
                "q6_endpoint_a": bits6(a),
                "q6_endpoint_b": bits6(b),
            }

    full_table = [table_by_flag[i] for i in range(192)]
    edge_values = [row["q6_edge_index"] for row in full_table]
    inverse_table = {
        int(row["q6_edge_index"]): int(row["tomotope_flag"]) for row in full_table
    }

    equivariance_failures = []
    for tom_group_index, tom_perm in enumerate(tom_autos):
        q_perm = q6_autos[image_indices[tom_group_index]]
        for flag, row in table_by_flag.items():
            lhs = table_by_flag[tom_perm[flag]]["q6_edge_index"]
            rhs = q_perm[int(row["q6_edge_index"])]
            if lhs != rhs:
                equivariance_failures.append([tom_group_index, flag, lhs, rhs])
                break
        if equivariance_failures:
            break

    checks = {
        "table_has_192_rows": len(full_table) == 192,
        "table_is_bijective_on_q6_edges": len(set(edge_values)) == 192,
        "inverse_table_has_192_rows": len(inverse_table) == 192,
        "gap_iso_maps_all_96_group_elements": len(image_indices) == 96
        and len(set(image_indices)) == 96,
        "equivariance_holds_for_all_group_elements": not equivariance_failures,
        "orbit_sizes_are_two_96s": [len(row) for row in tom_orbits] == [96, 96]
        and [len(row) for row in q6_orbits] == [96, 96],
    }

    return {
        "bt": 1371,
        "title": "Q6 tomotope explicit orbit address table",
        "verified": all(checks.values()),
        "source": {
            "tomotope_group": tom,
            "q6_group": q6,
            "gap_image_indices_first_12": image_indices[:12],
        },
        "address_table": full_table,
        "inverse_table_sample": dict(sorted(inverse_table.items())[:16]),
        "equivariance_failures": equivariance_failures,
        "interpretation": (
            "BT1368's existence certificate is now an explicit 192-row address "
            "table.  A tomotope flag and a Q6 edge are the same runtime address "
            "after choosing the GAP isomorphism and the two regular orbit bases."
        ),
        "boundary": (
            "The table depends on the chosen GAP isomorphism and orbit basepoints. "
            "Changing those choices conjugates the address table but preserves "
            "equivariance."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "rows": len(result["address_table"]),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
