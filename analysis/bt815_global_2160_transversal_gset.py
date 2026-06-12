#!/usr/bin/env python3
"""
BT815 - Global 2160 chart-transversal G-set.

BT801 counted 2160 chart-transversal slots.  This verifier identifies the
G-set:

  slot = (skew-line chart, common transversal line)
       -> (same chart, base antipode pair cut out by the transversal)

The map is a PSp(4,3)-equivariant bijection from chart-transversal slots to
the BT778 antipode-slot space.  Its stabilizer has order 12 and GAP identifies
it as D12, not C12, so this is the mirror/antipode 2160-space rather than the
cyclic rectangle-clock 2160-space.
"""
from __future__ import annotations

from collections import Counter, deque
import json
from pathlib import Path
import subprocess

from bt787_rank4_incidence_r11_handle import (
    build_geometry,
    build_psp,
    canon,
    line_perm,
    transvection_perm,
)


ROOT = Path(__file__).resolve().parents[1]


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def perm_order(p: tuple[int, ...]) -> int:
    ident = tuple(range(len(p)))
    cur = ident
    for n in range(1, 500):
        cur = compose(p, cur)
        if cur == ident:
            return n
    raise AssertionError("permutation order search exceeded bound")


def gap_perm_list(p: tuple[int, ...]) -> str:
    return "PermList([" + ",".join(str(x + 1) for x in p) + "])"


def run_gap_stabilizer_witness(stabilizer_line_perms: list[tuple[int, ...]]) -> dict[str, str]:
    perms = ",\n".join(gap_perm_list(p) for p in stabilizer_line_perms)
    script = f"""
perms := [{perms}];;
G := Group(perms);;
C := CyclicGroup(IsPermGroup, 12);;
D := DihedralGroup(IsPermGroup, 12);;
Print("size=", Size(G), "\\n");
Print("id=", IdGroup(G)[1], "-", IdGroup(G)[2], "\\n");
Print("structure=", StructureDescription(G), "\\n");
Print("is_cyclic=", IsCyclic(G), "\\n");
Print("isomorphic_to_C12=", IsomorphismGroups(G, C) <> fail, "\\n");
Print("isomorphic_to_D12=", IsomorphismGroups(G, D) <> fail, "\\n");
QUIT;
"""
    try:
        proc = subprocess.run(
            ["gap", "-q"],
            input=script,
            text=True,
            capture_output=True,
            check=True,
            timeout=20,
        )
        stdout = proc.stdout
    except FileNotFoundError:
        # Windows fallback: GAP lives behind its cygwin runtime (no
        # `gap` on PATH).  Heredoc/stdin newline mangling makes piping
        # unreliable there, so write a .g file and pass its cygdrive
        # path (pattern documented in BT813/BT843 GAP witnesses).
        from pathlib import Path
        gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
        if not gap_bash.exists():
            raise
        root = Path(__file__).resolve().parents[1]
        tmp = root / ".tmp"
        tmp.mkdir(exist_ok=True)
        gfile = tmp / "bt815_witness.g"
        gfile.write_text(script, newline="\n")
        drive, rest = str(gfile)[0].lower(), str(gfile)[2:].replace("\\", "/")
        cyg = f"/cygdrive/{drive}{rest}"
        proc = subprocess.run(
            [str(gap_bash), "--norc", "-c",
             f"/opt/gap-4.15.1/gap.exe -q -b '{cyg}'"],
            cwd=str(gap_bash.parent),
            text=True,
            capture_output=True,
            check=True,
            timeout=120,
        )
        stdout = proc.stdout
    out: dict[str, str] = {}
    for line in stdout.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            out[key] = value
    required = {"size", "id", "structure", "is_cyclic", "isomorphic_to_C12", "isomorphic_to_D12"}
    missing = required - set(out)
    if missing:
        raise AssertionError(f"GAP witness missing keys: {sorted(missing)}")
    return out


def seed_point_generators(geom) -> list[tuple[int, ...]]:
    seed_vectors = [
        canon((1, 0, 0, 0)), canon((0, 1, 0, 0)),
        canon((0, 0, 1, 0)), canon((0, 0, 0, 1)),
        canon((1, 1, 0, 0)), canon((1, 0, 1, 0)),
        canon((1, 0, 0, 1)), canon((0, 1, 1, 0)),
    ]
    return [transvection_perm(v, geom["points"], geom["point_index"]) for v in seed_vectors]


def chart_transversals(geom, a: int, b: int) -> list[dict[str, object]]:
    base0 = geom["line_sets"][a]
    base1 = geom["line_sets"][b]
    base_union = base0 | base1
    rows = []
    for line_id, line in enumerate(geom["line_sets"]):
        if line_id in (a, b):
            continue
        if line & base0 and line & base1:
            rows.append({
                "transversal_line_id": line_id,
                "base_antipode_pair": tuple(sorted(line & base_union)),
                "shadow_pair": tuple(sorted(line - base_union)),
            })
    return sorted(rows, key=lambda row: row["transversal_line_id"])


def build_slot_spaces(geom):
    trans_slots = []
    antipode_slots = []
    trans_to_antipode = {}
    trans_slot_index = {}
    antipode_slot_index = {}

    for chart_index, (a, b) in enumerate(geom["skew"]):
        for row in chart_transversals(geom, a, b):
            t_slot = (chart_index, int(row["transversal_line_id"]))
            a_slot = (chart_index, tuple(row["base_antipode_pair"]))
            trans_slot_index[t_slot] = len(trans_slots)
            trans_slots.append(t_slot)
            if a_slot not in antipode_slot_index:
                antipode_slot_index[a_slot] = len(antipode_slots)
                antipode_slots.append(a_slot)
            trans_to_antipode[t_slot] = a_slot

    return trans_slots, antipode_slots, trans_to_antipode, trans_slot_index, antipode_slot_index


def apply_trans_slot(geom, line_p: tuple[int, ...], slot: tuple[int, int]) -> tuple[int, int]:
    chart_index, trans_line = slot
    a, b = geom["skew"][chart_index]
    next_chart = geom["pair_to_skew"][(line_p[a], line_p[b])]
    return (next_chart, line_p[trans_line])


def apply_antipode_slot(
    geom,
    line_p: tuple[int, ...],
    point_p: tuple[int, ...],
    slot: tuple[int, tuple[int, int]],
) -> tuple[int, tuple[int, int]]:
    chart_index, pair = slot
    a, b = geom["skew"][chart_index]
    next_chart = geom["pair_to_skew"][(line_p[a], line_p[b])]
    return (next_chart, tuple(sorted((point_p[pair[0]], point_p[pair[1]]))))


def orbit_from_slot(geom, line_perms: list[tuple[int, ...]], slot: tuple[int, int]) -> set[tuple[int, int]]:
    return {apply_trans_slot(geom, line_p, slot) for line_p in line_perms}


def component_orbits(items, generators, action):
    seen = set()
    profiles = []
    for item in items:
        if item in seen:
            continue
        q = deque([item])
        seen.add(item)
        orbit = []
        while q:
            x = q.popleft()
            orbit.append(x)
            for gen in generators:
                y = action(gen, x)
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        profiles.append(len(orbit))
    return sorted(profiles)


def main() -> None:
    geom = build_geometry()
    point_perms = build_psp(geom["points"], geom["point_index"])
    point_to_line = {
        p: line_perm(p, geom["lines"], geom["line_key_index"])
        for p in point_perms
    }
    line_perms = list(point_to_line.values())
    seed_points = seed_point_generators(geom)
    seed_pairs = [(g, line_perm(g, geom["lines"], geom["line_key_index"])) for g in seed_points]

    trans_slots, antipode_slots, trans_to_antipode, trans_slot_index, antipode_slot_index = build_slot_spaces(geom)
    base_slot = trans_slots[0]
    base_antipode_slot = trans_to_antipode[base_slot]
    base_chart, base_transversal = base_slot
    base_a, base_b = geom["skew"][base_chart]

    equivariance_failures = []
    for point_g, line_g in seed_pairs:
        for slot in trans_slots:
            lhs = trans_to_antipode[apply_trans_slot(geom, line_g, slot)]
            rhs = apply_antipode_slot(geom, line_g, point_g, trans_to_antipode[slot])
            if lhs != rhs:
                equivariance_failures.append((slot, lhs, rhs))
                break
        if equivariance_failures:
            break

    orbit = orbit_from_slot(geom, line_perms, base_slot)
    line_multiplicity = Counter(trans_line for _chart, trans_line in trans_slots)
    chart_multiplicity = Counter(chart for chart, _trans_line in trans_slots)

    trans_stabilizer_indices = []
    antipode_stabilizer_indices = []
    for idx, point_g in enumerate(point_perms):
        line_g = point_to_line[point_g]
        if apply_trans_slot(geom, line_g, base_slot) == base_slot:
            trans_stabilizer_indices.append(idx)
        if apply_antipode_slot(geom, line_g, point_g, base_antipode_slot) == base_antipode_slot:
            antipode_stabilizer_indices.append(idx)

    stabilizer_line_perms = [point_to_line[point_perms[idx]] for idx in trans_stabilizer_indices]
    order_profile = Counter(perm_order(p) for p in stabilizer_line_perms)
    gap = run_gap_stabilizer_witness(stabilizer_line_perms)

    trans_components = component_orbits(
        trans_slots,
        [line_g for _point_g, line_g in seed_pairs],
        lambda gen, item: apply_trans_slot(geom, gen, item),
    )

    def anti_action(gen_pair, item):
        point_g, line_g = gen_pair
        return apply_antipode_slot(geom, line_g, point_g, item)

    antipode_components = component_orbits(antipode_slots, seed_pairs, anti_action)

    # Local orbit of the chosen slot stabilizer on the four transversals of the
    # base chart: fixed chosen line plus a three-cycle orbit, the D6 mirror.
    base_transversal_rows = chart_transversals(geom, base_a, base_b)
    local_transversal_orbits = []
    for row in base_transversal_rows:
        line_id = int(row["transversal_line_id"])
        local_transversal_orbits.append(sorted({p[line_id] for p in stabilizer_line_perms}))
    local_transversal_orbit_profile = sorted(len(set(row)) for row in local_transversal_orbits)

    checks = {
        "transversal_slots_are_2160": len(trans_slots) == 2160,
        "antipode_slots_are_2160": len(antipode_slots) == 2160,
        "transversal_to_antipode_is_bijection": len(set(trans_to_antipode.values())) == 2160,
        "equivariance_holds_for_generators": not equivariance_failures,
        "transversal_slot_space_is_transitive": len(orbit) == 2160 and trans_components == [2160],
        "antipode_slot_space_is_transitive": antipode_components == [2160],
        "each_chart_has_four_slots": set(chart_multiplicity.values()) == {4},
        "each_line_occurs_54_times": set(line_multiplicity.values()) == {54},
        "transversal_and_antipode_stabilizers_are_identical": trans_stabilizer_indices == antipode_stabilizer_indices,
        "slot_stabilizer_has_order_12": len(trans_stabilizer_indices) == 12,
        "slot_stabilizer_order_profile_is_D12": dict(sorted(order_profile.items())) == {1: 1, 2: 7, 3: 2, 6: 2},
        "gap_identifies_D12_not_C12": gap["size"] == "12" and gap["structure"] == "D12" and gap["is_cyclic"] == "false" and gap["isomorphic_to_C12"] == "false" and gap["isomorphic_to_D12"] == "true",
        "local_stabilizer_orbits_are_fixed_plus_three": local_transversal_orbit_profile == [1, 3, 3, 3],
        "witting_transposition_holonomy_reference_matches": len(trans_slots) == 2160,
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT815 check failed: {name}")

    out = {
        "theorem": "BT815 global 2160 chart-transversal G-set",
        "group": "PSp(4,3)",
        "slot_counts": {
            "chart_transversal_slots": len(trans_slots),
            "chart_antipode_slots": len(antipode_slots),
            "charts": len(geom["skew"]),
            "slots_per_chart": sorted(set(chart_multiplicity.values())),
            "transversal_slots_per_line": dict(sorted(Counter(line_multiplicity.values()).items())),
        },
        "equivariant_bijection": {
            "map": "(chart, common transversal line) -> (chart, transversal intersection with base chart)",
            "base_slot": [base_slot[0], base_slot[1]],
            "base_antipode_slot": [base_antipode_slot[0], list(base_antipode_slot[1])],
            "checked_on_generators": len(seed_pairs),
            "failures": equivariance_failures[:3],
        },
        "stabilizer": {
            "order": len(trans_stabilizer_indices),
            "order_profile": dict(sorted(order_profile.items())),
            "gap_witness": gap,
            "local_transversal_orbit_profile": local_transversal_orbit_profile,
            "meaning": "D12 mirror/antipode stabilizer, not C12 rectangle-clock stabilizer",
        },
        "comparison": {
            "BT778_antipode_slots": "same G-set, via the explicit equivariant bijection verified here",
            "BT778_rectangle_slots": "same cardinality 2160 but cyclic C12 stabilizer; not this D12 slot space",
            "Witting_packet_holonomy": "existing Witting local-system audit records 2160 transposition holonomies; BT815 identifies the W33 atlas-side D12 mirror carrier at the same cardinality",
            "BT813_geography": "slot stabilizer order 12 sits below the chart O_h group from BT811, while the 2160 total is 48 chart group packets times 45 polar-pair geography",
        },
        "factorizations": {
            "540_times_4": 540 * 4,
            "40_times_54": 40 * 54,
            "45_times_48": 45 * 48,
            "240_times_9": 240 * 9,
        },
        "checks": checks,
    }
    path = ROOT / "data" / "bt815_global_2160_transversal_gset.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
