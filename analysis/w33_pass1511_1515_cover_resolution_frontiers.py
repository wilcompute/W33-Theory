#!/usr/bin/env python3
"""Passes 1511--1515: exact-cover disjointness, packing, involutions, and integrality gap.

This release corrects the sampled "intersecting family" conjecture by producing
literal disjoint covers, enumerates all disjoint partners of a canonical cover
inside the frozen 327-orbit frontier, proves the associated disjointness graph
has clique number three, classifies all C2 cover stabilizers, and proves that a
selected four-cover packing has no fifth integral layer despite an exact uniform
fractional layer.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import math
import statistics
import struct
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "analysis" / "w33_pass1505_exact_cover_census_frontier.py"
REPS = ROOT / "data" / "w33_pass1511_cover_orbit_representatives.json.gz.b64"
CPP_GRAPH = ROOT / "analysis" / "cpp" / "w33_pass1513_disjoint_cover_graph.cpp"
CPP_RESIDUAL = ROOT / "analysis" / "cpp" / "w33_pass1515_residual_exact_cover.cpp"
OUT = ROOT / "data" / "w33_pass1511_1515_cover_resolution_frontiers.json"
SCRIPT = Path(__file__).resolve()

PAIR_PARTNER = [
    9,18,25,27,35,41,65,74,78,86,93,99,118,122,128,133,137,147,164,166,
    181,187,199,204,217,238,239,243,257,265,269,272,285,298,301,307,323,
    345,365,378,386,387,390,405,416,422,426,427,435,445,461,466,474,497,
    500,502,506,524,537,538,
]

PACKING = [
    [0,16,24,32,47,52,66,69,76,81,89,95,117,126,136,145,152,156,165,173,
     184,186,201,209,216,230,240,248,256,267,274,289,296,304,312,320,325,
     327,334,341,357,362,367,385,392,402,417,440,462,463,467,470,481,483,
     487,508,510,521,536,539],
    [1,13,19,34,39,49,55,59,70,94,98,106,114,119,125,135,155,157,168,177,
     185,194,198,210,218,222,226,259,262,278,279,283,285,299,302,323,331,
     345,359,368,371,380,386,393,401,410,420,432,448,454,469,491,492,494,
     497,504,511,512,522,529],
    [5,11,20,40,44,48,63,71,75,82,86,88,111,123,131,133,142,163,172,178,
     188,192,202,204,231,233,237,257,260,273,280,288,293,298,303,335,346,
     349,353,365,373,374,378,382,390,405,407,414,430,439,444,449,457,466,
     489,503,506,516,534,538],
    [4,15,22,31,33,54,68,74,80,90,101,102,108,112,120,141,144,153,164,176,
     187,191,199,215,224,225,232,254,265,269,277,286,291,308,315,329,338,
     347,352,361,372,377,391,396,397,399,416,423,425,431,450,453,458,475,
     488,499,507,518,526,535],
]
PACKING_ORBITS = [0, 229, 30, 26]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compile_cpp(source: Path, output: Path) -> None:
    subprocess.run(["g++", "-O3", "-std=c++20", str(source), "-o", str(output)], check=True)


def cover_words(cover: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    words = [0] * 9
    for r in cover:
        words[r // 64] |= 1 << (r % 64)
    return tuple(words)


def exact_cover(M: np.ndarray, cover: list[int] | tuple[int, ...]) -> bool:
    return len(cover) == 60 and len(set(cover)) == 60 and np.array_equal(M[list(cover)].sum(axis=0), np.ones(240, dtype=np.int64))


def order_of_perm(p: tuple[int, ...]) -> int:
    seen = [False] * len(p)
    ans = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j, n = i, 0
        while not seen[j]:
            seen[j] = True
            n += 1
            j = p[j]
        ans = math.lcm(ans, n)
    return ans


def stabilizer_type(indices: list[int], G: list[tuple[int, ...]], compose) -> str:
    elems = [G[i] for i in indices]
    orders = sorted(order_of_perm(g) for g in elems)
    abelian = all(compose(a, b) == compose(b, a) for a in elems for b in elems)
    n = len(elems)
    if n == 2:
        return "C2"
    if n == 4:
        return "C4" if 4 in orders else "C2xC2"
    if n == 8 and abelian:
        return "C4xC2" if 4 in orders else "C2^3"
    if n == 8:
        return "D8" if orders.count(2) == 5 else "Q8"
    return f"order{n}"


def certificate() -> dict:
    p1505 = load_module(BASE, "p1505")
    base = p1505.load_base()
    points, edges, lines, frames, G, M, A, N, d, K = base.build_geometry()
    M = M.astype(np.int64)
    reps_payload = json.loads(gzip.decompress(base64.b64decode(REPS.read_text())).decode())
    records = reps_payload["representatives"]
    assert len(records) == 327

    with tempfile.TemporaryDirectory() as td_name:
        td = Path(td_name)
        instance = td / "instance.txt"
        frame_perm, line_perm = p1505.write_instance(instance, base, (points, edges, lines, frames, G, M, A, N, d, K))
        FA = np.array([frame_perm(line_perm(g)) for g in G], dtype=np.uint16)
        reps = [np.array(r["representative"], dtype=np.int64) for r in records]

        c0 = tuple(map(int, reps[0]))
        c1 = tuple(PAIR_PARTNER)
        pair_orbit = 29
        pair_images = np.sort(FA[:, reps[pair_orbit]], axis=1)
        pair_membership = bool(np.any(np.all(pair_images == np.array(c1, dtype=np.uint16), axis=1)))

        c0_mask = np.zeros(540, dtype=np.uint8)
        c0_mask[list(c0)] = 1
        all_disjoint: dict[tuple[int, ...], int] = {}
        unique_per_orbit: list[int] = []
        raw_per_orbit: list[int] = []
        for orbit_index, rep in enumerate(reps):
            images = np.sort(FA[:, rep], axis=1)
            good = images[c0_mask[images].sum(axis=1) == 0]
            raw_per_orbit.append(int(len(good)))
            unique = np.unique(good, axis=0)
            unique_per_orbit.append(int(len(unique)))
            assert len(good) == len(unique) * int(records[orbit_index]["stabilizer_order"])
            for row in unique:
                key = tuple(map(int, row))
                if key in all_disjoint:
                    assert all_disjoint[key] == orbit_index
                all_disjoint[key] = orbit_index
        sorted_disjoint = sorted(all_disjoint)
        binary = td / "disjoint.bin"
        with binary.open("wb") as f:
            f.write(struct.pack("<Q", len(sorted_disjoint)))
            for cover in sorted_disjoint:
                f.write(struct.pack("<9Q", *cover_words(cover)))

        graph_exe = td / "graph"
        compile_cpp(CPP_GRAPH, graph_exe)
        graph = json.loads(subprocess.check_output([str(graph_exe), str(binary)], text=True))
        disjoint_binary_sha256 = sha(binary)

        packing = [tuple(c) for c in PACKING]
        packing_exact = all(exact_cover(M, c) for c in packing)
        packing_pairwise_disjoint = all(not (set(packing[i]) & set(packing[j])) for i in range(4) for j in range(i + 1, 4))
        packing_membership = []
        packing_stabilizers = []
        for cover, orbit_index in zip(packing, PACKING_ORBITS):
            target = np.array(cover, dtype=np.uint16)
            images = np.sort(FA[:, reps[orbit_index]], axis=1)
            packing_membership.append(bool(np.any(np.all(images == target, axis=1))))
            mask = np.zeros(540, dtype=bool)
            mask[list(cover)] = True
            stab = np.flatnonzero(mask[FA[:, np.array(cover, dtype=np.int64)]].all(axis=1)).astype(int).tolist()
            packing_stabilizers.append({
                "orbit_index": orbit_index,
                "orbit_size": int(records[orbit_index]["orbit_size"]),
                "stabilizer_order": len(stab),
                "stabilizer_type": stabilizer_type(stab, G, base.compose),
                "group_indices": stab,
            })

        group_index = {g: i for i, g in enumerate(G)}
        identity = G[0]
        involutions = [i for i, g in enumerate(G) if i and base.compose(g, g) == identity]
        remaining = set(involutions)
        involution_class: dict[int, int] = {}
        while remaining:
            h_index = next(iter(remaining))
            h = G[h_index]
            conjugates = set()
            for g in G:
                x = base.compose(base.compose(g, h), base.invperm(g))
                conjugates.add(group_index[x])
            size = len(conjugates)
            for x in conjugates:
                involution_class[x] = size
            remaining -= conjugates

        c2_class_counts = Counter()
        c2_profile_counts = Counter()
        for record, cover in zip(records, reps):
            if int(record["stabilizer_order"]) != 2:
                continue
            mask = np.zeros(540, dtype=bool)
            mask[cover] = True
            stab = np.flatnonzero(mask[FA[:, cover]].all(axis=1)).astype(int).tolist()
            assert len(stab) == 2
            h = next(i for i in stab if i != 0)
            cls = involution_class[h]
            global_fixed = int(np.sum(FA[h] == np.arange(540)))
            cover_fixed = int(np.sum(mask & (FA[h] == np.arange(540))))
            c2_class_counts[cls] += 1
            c2_profile_counts[(cls, global_fixed, cover_fixed)] += 1

        for packing_record in packing_stabilizers:
            cover = np.array(packing[PACKING_ORBITS.index(packing_record["orbit_index"])], dtype=np.int64)
            mask = np.zeros(540, dtype=bool)
            mask[cover] = True
            involution_profiles = []
            for h in packing_record.pop("group_indices"):
                if h not in involution_class:
                    continue
                involution_profiles.append({
                    "class_size": involution_class[h],
                    "global_fixed_frames": int(np.sum(FA[h] == np.arange(540))),
                    "fixed_frames_in_cover": int(np.sum(mask & (FA[h] == np.arange(540)))),
                })
            packing_record["involution_profiles"] = sorted(involution_profiles, key=lambda x: (x["class_size"], x["global_fixed_frames"]))

        forbidden = td / "forbidden.txt"
        flat_packing = [r for cover in packing for r in cover]
        forbidden.write_text(str(len(flat_packing)) + "\n" + " ".join(map(str, flat_packing)) + "\n")
        trace = td / "residual_trace.bin"
        residual_exe = td / "residual"
        compile_cpp(CPP_RESIDUAL, residual_exe)
        residual_raw = json.loads(subprocess.check_output([str(residual_exe), str(instance), str(forbidden), str(trace)], text=True))
        residual = {k: v for k, v in residual_raw.items() if k != "seconds"}
        residual["trace_sha256"] = sha(trace)
        remaining_rows = [r for r in range(540) if r not in set(flat_packing)]
        residual_incidence = M[remaining_rows]
        residual_col_degrees = residual_incidence.sum(axis=0)
        residual_row_degrees = residual_incidence.sum(axis=1)
        fractional = np.full(len(remaining_rows), 1 / 5, dtype=float)
        fractional_image = residual_incidence.T @ fractional

    checks = {
        "pass1511_pair_both_exact": exact_cover(M, c0) and exact_cover(M, c1),
        "pass1511_pair_disjoint": len(set(c0) & set(c1)) == 0,
        "pass1511_partner_is_orbit29": pair_membership,
        "pass1511_frozen_prefix_representatives_all_contain_frame0": all(0 in set(map(int, rep)) for rep in reps),
        "pass1512_all_327_orbits_have_disjoint_partner": len(unique_per_orbit) == 327 and min(unique_per_orbit) > 0,
        "pass1512_unique_disjoint_count_13648": len(sorted_disjoint) == 13648,
        "pass1512_raw_group_images_32464": sum(raw_per_orbit) == 32464,
        "pass1513_graph_exact_values": graph == {
            "status": "PASS", "vertices": 13648, "edges": 188338, "triangles": 494,
            "k4_exists": False, "clique_number": 3, "isolated_vertices": 180,
            "min_degree": 0, "max_degree": 634, "first_triangle": graph["first_triangle"],
        },
        "pass1513_four_packing_exact": packing_exact,
        "pass1513_four_packing_pairwise_disjoint": packing_pairwise_disjoint,
        "pass1513_four_packing_orbit_membership": all(packing_membership),
        "pass1514_involution_classes_45_270": sorted(set(involution_class.values())) == [45, 270] and len(involutions) == 315,
        "pass1514_all_228_c2_orbits_use_class45": dict(c2_class_counts) == {45: 228},
        "pass1514_all_c2_fixed_profile_84_12": dict(c2_profile_counts) == {(45, 84, 12): 228},
        "pass1515_residual_300_by_240_regular_5_4": residual_incidence.shape == (300, 240) and np.all(residual_col_degrees == 5) and np.all(residual_row_degrees == 4),
        "pass1515_no_fifth_integral_cover": residual["found"] is False and residual["nodes"] == 2332 and residual["forced_steps"] == 18227,
        "pass1515_uniform_fractional_cover": np.allclose(fractional_image, np.ones(240)) and math.isclose(float(fractional.sum()), 60.0),
    }
    checks = {k: bool(v) for k, v in checks.items()}

    unique_by_stabilizer = {
        str(s): sum(unique_per_orbit[i] for i, r in enumerate(records) if int(r["stabilizer_order"]) == s)
        for s in (2, 4, 8)
    }
    values_by_stabilizer = {
        str(s): [unique_per_orbit[i] for i, r in enumerate(records) if int(r["stabilizer_order"]) == s]
        for s in (2, 4, 8)
    }

    payload = {
        "schema": "w33.pass1511_1515.cover_resolution_frontiers.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "pass1511_disjoint_pair_counterexample": {
            "theorem": "The exact-cover family is not intersecting: two explicit 60-frame covers partition all 240 edge columns and share zero frames. The earlier sampled intersecting-family signal was forced by the symmetry break: every frozen prefix representative contains frame 0.",
            "canonical_orbit": 0,
            "partner_orbit": pair_orbit,
            "canonical_cover": list(c0),
            "disjoint_partner": list(c1),
            "intersection_size": 0,
            "sampling_diagnosis": "The Pass 1505/1510 DFS prefixes fix frame 0 before recursion, so every sampled cover contains frame 0 and the sampled pool is pairwise intersecting by construction.",
        },
        "pass1512_disjoint_partner_frontier": {
            "theorem": "Every one of the 327 frozen PSp(4,3) cover orbit types contains a cover disjoint from the canonical cover.",
            "orbit_types_hit": 327,
            "distinct_disjoint_covers": len(sorted_disjoint),
            "raw_group_images": sum(raw_per_orbit),
            "unique_count_range_per_orbit": [min(unique_per_orbit), max(unique_per_orbit)],
            "unique_count_median_per_orbit": statistics.median(unique_per_orbit),
            "unique_counts_by_stabilizer_order": unique_by_stabilizer,
            "unique_ranges_by_stabilizer_order": {
                s: [min(v), max(v), statistics.median(v)] for s, v in values_by_stabilizer.items()
            },
            "disjoint_cover_set_sha256": disjoint_binary_sha256,
        },
        "pass1513_disjointness_graph_and_four_packing": {
            "theorem": "The 13648 known disjoint partners form a graph with 188338 edges and 494 triangles but no K4. Hence the largest packing containing the canonical cover inside the certified frontier has four covers.",
            "graph": graph,
            "packing_orbits": PACKING_ORBITS,
            "packing": [list(c) for c in packing],
            "packing_stabilizers": packing_stabilizers,
            "covered_frames": 240,
        },
        "pass1514_class45_involution_lock": {
            "theorem": "All 228 C2-stabilized orbit types use the small class-45 involution, fixing 84 frames globally and exactly 12 frames of the stabilized cover.",
            "group_order": len(G),
            "involution_total": len(involutions),
            "involution_class_sizes": sorted(set(involution_class.values())),
            "c2_orbit_class_counts": {str(k): v for k, v in sorted(c2_class_counts.items())},
            "c2_fixed_profile_counts": {f"class{c}_global{g}_cover{f}": n for (c, g, f), n in sorted(c2_profile_counts.items())},
        },
        "pass1515_residual_integrality_gap": {
            "theorem": "Removing the selected four covers leaves a 300-row, 240-column 4-uniform, 5-regular residual incidence system. The uniform weight 1/5 is a fractional exact cover of total weight 60, but exhaustive Algorithm X proves there is no integral exact cover, so the four-packing has no fifth layer.",
            "residual_rows": 300,
            "edge_columns": 240,
            "row_degree": 4,
            "column_degree": 5,
            "fractional_weight_per_row": "1/5",
            "fractional_total_weight": 60,
            "integral_search": residual,
        },
        "source_sha256": {
            str(SCRIPT.relative_to(ROOT)): sha(SCRIPT),
            str(REPS.relative_to(ROOT)): sha(REPS),
            str(CPP_GRAPH.relative_to(ROOT)): sha(CPP_GRAPH),
            str(CPP_RESIDUAL.relative_to(ROOT)): sha(CPP_RESIDUAL),
        },
        "checks": checks,
        "boundary": "The explicit four-packing is globally maximal relative to adding a fifth cover to that packing. The graph clique computation is exhaustive inside the frozen 327-orbit frontier. Neither statement proves that four is the global packing number over undiscovered cover orbits or over different four-packings.",
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = certificate()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Passes 1511-1515 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({
        "status": payload["status"],
        "checks": sum(payload["checks"].values()),
        "disjoint_partners": payload["pass1512_disjoint_partner_frontier"]["distinct_disjoint_covers"],
        "packing_size": len(payload["pass1513_disjointness_graph_and_four_packing"]["packing"]),
        "fifth_cover": payload["pass1515_residual_integrality_gap"]["integral_search"]["found"],
    }, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
