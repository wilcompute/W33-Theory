#!/usr/bin/env python3
"""Bridge W(3,3) spreads, contextuality, and the Holonet line microkernel.

The existing UOR spread scheduler proves a site-level envelope: every spread is
a full 40-site partition, so any packet path is contained in any spread by site
cover alone.  The physical synchronisation layer is stricter.  A one-hop packet
uses the unique W(3,3) line through its two endpoints, and a two-hop packet uses
two such line operations through a relay.

This verifier checks that stricter line-context scheduler.  It also records the
exact equality between:

    36 W(3,3) spreads = 36 max satisfiable KS contexts.

The equality is promoted only as an audited bridge: the script does not claim a
canonical bijection between optimal noncontextual assignments and spreads.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_uor_runtime_model import ROOT, all_lines, find_spreads, point_id

DEFAULT_INPUTS = [
    ROOT / "data" / "holonet_wrap_demo_factorial.json",
    ROOT / "data" / "holonet_wrap_rule110_demo.json",
]
DEFAULT_CONTEXTUALITY = ROOT / "data" / "w33_contextual_fraction.json"
DEFAULT_SITE_SCHEDULER = ROOT / "data" / "holonet_os_scheduler_trace.json"
DEFAULT_OUTPUT = ROOT / "data" / "w33_spread_contextual_microkernel_bridge.json"

W33 = {"q": 3, "v": 40, "k": 12, "lambda": 2, "mu": 4, "phi4": 10}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_path(path: str | Path) -> Path:
    path = Path(path)
    return path if path.is_absolute() else ROOT / path


def point_index_map() -> dict[str, int]:
    return {point_id(point): idx for idx, point in enumerate(hn.POINTS)}


def spread_diagnostics(
    lines: list[tuple[int, ...]], spreads: list[list[int]]
) -> dict[str, Any]:
    line_occurrences = {idx: 0 for idx in range(len(lines))}
    spread_cover_ok = True
    spread_sizes = []
    for spread in spreads:
        spread_sizes.append(len(spread))
        seen_points: set[int] = set()
        for line_idx in spread:
            line = set(lines[line_idx])
            if seen_points & line:
                spread_cover_ok = False
            seen_points.update(line)
            line_occurrences[line_idx] += 1
        if len(seen_points) != len(hn.POINTS):
            spread_cover_ok = False
    occurrence_histogram = {
        str(value): list(line_occurrences.values()).count(value)
        for value in sorted(set(line_occurrences.values()))
    }
    return {
        "spread_count": len(spreads),
        "spread_size_histogram": {
            str(value): spread_sizes.count(value) for value in sorted(set(spread_sizes))
        },
        "all_spreads_are_disjoint_site_partitions": spread_cover_ok,
        "line_spread_membership_histogram": occurrence_histogram,
        "line_spread_incidence_count": sum(line_occurrences.values()),
    }


def line_for_pair(
    left: str,
    right: str,
    lines: list[tuple[int, ...]],
    site_to_idx: dict[str, int],
) -> int:
    left_idx = site_to_idx[left]
    right_idx = site_to_idx[right]
    candidates = [
        idx for idx, line in enumerate(lines) if left_idx in line and right_idx in line
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"expected a unique line for hop {left}->{right}, got {candidates}"
        )
    return candidates[0]


def build_hop_jobs(
    reports: list[dict[str, Any]],
    lines: list[tuple[int, ...]],
    line_to_spreads: dict[int, list[int]],
) -> list[dict[str, Any]]:
    site_to_idx = point_index_map()
    jobs: list[dict[str, Any]] = []
    for report_index, report in enumerate(reports):
        for packet in report.get("packets", []):
            packet_id = f"{packet['label']}:{packet['index']}@{report_index}"
            path = packet["path"]
            for hop_index, (left, right) in enumerate(zip(path, path[1:])):
                line_idx = line_for_pair(left, right, lines, site_to_idx)
                jobs.append(
                    {
                        "job_id": f"{packet_id}:h{hop_index}",
                        "packet_id": packet_id,
                        "report_index": report_index,
                        "hop_index": hop_index,
                        "packet_hops": packet["hops"],
                        "line_index": line_idx,
                        "sites": [left, right],
                        "candidate_spreads": line_to_spreads[line_idx],
                    }
                )
    return jobs


def point_to_line_index(lines: list[tuple[int, ...]]) -> list[set[int]]:
    memberships = [set() for _ in range(len(hn.POINTS))]
    for line_idx, line in enumerate(lines):
        for point_idx in line:
            memberships[point_idx].add(line_idx)
    return memberships


def exact_cover_points(
    chosen_lines: set[int],
    lines: list[tuple[int, ...]],
    memberships: list[set[int]],
) -> list[int] | None:
    """Find selected points covering every chosen line exactly once."""
    covered: set[int] = set()
    selected: list[int] = []

    def search() -> bool:
        if len(covered) == len(chosen_lines):
            return True
        best_candidates: list[tuple[int, set[int]]] | None = None
        for line_idx in chosen_lines - covered:
            candidates = []
            for point_idx in lines[line_idx]:
                point_cover = memberships[point_idx] & chosen_lines
                if point_cover & covered:
                    continue
                candidates.append((point_idx, point_cover))
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_candidates = candidates
                if not candidates:
                    break
        if not best_candidates:
            return False
        best_candidates.sort(key=lambda row: (-len(row[1]), row[0]))
        for point_idx, point_cover in best_candidates:
            selected.append(point_idx)
            old_covered = set(covered)
            covered.update(point_cover)
            if search():
                return True
            covered.clear()
            covered.update(old_covered)
            selected.pop()
        return False

    return selected.copy() if search() else None


def point_star_witnesses(lines: list[tuple[int, ...]]) -> dict[str, Any]:
    memberships = point_to_line_index(lines)
    all_line_indices = set(range(len(lines)))
    witnesses = []
    for point_idx, incident_lines in enumerate(memberships):
        unsatisfied = set(incident_lines)
        selected = exact_cover_points(
            all_line_indices - unsatisfied, lines, memberships
        )
        if selected is None:
            witnesses.append(
                {
                    "point": point_id(hn.POINTS[point_idx]),
                    "status": "FAIL",
                    "unsatisfied_lines": sorted(unsatisfied),
                }
            )
            continue
        selected_set = set(selected)
        line_sums = [len(selected_set & set(line)) for line in lines]
        witnesses.append(
            {
                "point": point_id(hn.POINTS[point_idx]),
                "status": "PASS",
                "unsatisfied_lines": sorted(unsatisfied),
                "selected_point_count": len(selected),
                "selected_points": [point_id(hn.POINTS[idx]) for idx in selected],
                "unsatisfied_line_sums": [
                    line_sums[idx] for idx in sorted(unsatisfied)
                ],
                "line_sum_histogram": {
                    str(value): line_sums.count(value)
                    for value in sorted(set(line_sums))
                },
            }
        )
    statuses = [row["status"] for row in witnesses]
    selected_counts = [
        row["selected_point_count"] for row in witnesses if row["status"] == "PASS"
    ]
    unsat_sum_profiles = [
        tuple(row["unsatisfied_line_sums"])
        for row in witnesses
        if row["status"] == "PASS"
    ]
    line_sum_histograms = [
        tuple(sorted(row["line_sum_histogram"].items()))
        for row in witnesses
        if row["status"] == "PASS"
    ]
    return {
        "status": "PASS" if set(statuses) == {"PASS"} else "FAIL",
        "witness_count": len(witnesses),
        "unique_unsatisfied_point_stars": len(
            {tuple(row["unsatisfied_lines"]) for row in witnesses}
        ),
        "selected_point_count_histogram": histogram(selected_counts),
        "unsatisfied_line_sum_profile_histogram": {
            str(profile): unsat_sum_profiles.count(profile)
            for profile in sorted(set(unsat_sum_profiles))
        },
        "line_sum_histogram_profiles": {
            str(profile): line_sum_histograms.count(profile)
            for profile in sorted(set(line_sum_histograms))
        },
        "sample_witnesses": witnesses[:5],
        "reading": (
            "For every W(3,3) point, deleting the four incident line contexts leaves an exact-cover "
            "assignment satisfying the other 36 contexts. The four deleted lines are overfull with "
            "line sum 2, so the contextual defect is a movable point-star double-occupancy defect."
        ),
    }


def packet_hop_groups(jobs: list[dict[str, Any]]) -> dict[str, list[int]]:
    groups: dict[str, list[int]] = {}
    for idx, job in enumerate(jobs):
        groups.setdefault(job["packet_id"], []).append(idx)
    for group in groups.values():
        group.sort(key=lambda idx: jobs[idx]["hop_index"])
    return groups


def two_hop_intersections(jobs: list[dict[str, Any]]) -> list[int]:
    intersections = []
    for group in packet_hop_groups(jobs).values():
        if len(group) != 2:
            continue
        first = set(jobs[group[0]]["candidate_spreads"])
        second = set(jobs[group[1]]["candidate_spreads"])
        intersections.append(len(first & second))
    return intersections


def ready(
    job_index: int,
    jobs: list[dict[str, Any]],
    done: set[int],
    groups: dict[str, list[int]],
) -> bool:
    job = jobs[job_index]
    group = groups[job["packet_id"]]
    position = group.index(job_index)
    return position == 0 or group[position - 1] in done


def schedule_for_spread(
    spread_index: int,
    jobs: list[dict[str, Any]],
    done: set[int],
    groups: dict[str, list[int]],
) -> tuple[list[int], set[str]]:
    used_sites: set[str] = set()
    dispatch: list[int] = []
    for idx, job in enumerate(jobs):
        if idx in done:
            continue
        if not ready(idx, jobs, done, groups):
            continue
        if spread_index not in job["candidate_spreads"]:
            continue
        sites = set(job["sites"])
        if used_sites & sites:
            continue
        used_sites.update(sites)
        dispatch.append(idx)
    return dispatch, used_sites


def greedy_line_schedule(
    jobs: list[dict[str, Any]], spread_count: int
) -> dict[str, Any]:
    groups = packet_hop_groups(jobs)
    done: set[int] = set()
    ticks = []
    while len(done) < len(jobs):
        best_spread = None
        best_dispatch: list[int] = []
        best_sites: set[str] = set()
        for spread_index in range(spread_count):
            dispatch, used_sites = schedule_for_spread(spread_index, jobs, done, groups)
            score = (len(dispatch), len(used_sites), -spread_index)
            best_score = (len(best_dispatch), len(best_sites), -(best_spread or 0))
            if best_spread is None or score > best_score:
                best_spread = spread_index
                best_dispatch = dispatch
                best_sites = used_sites
        if best_spread is None or not best_dispatch:
            break
        for job_index in best_dispatch:
            done.add(job_index)
        ticks.append(
            {
                "tick": len(ticks),
                "spread_epoch": best_spread,
                "dispatch_count": len(best_dispatch),
                "used_site_count": len(best_sites),
                "jobs": [jobs[idx]["job_id"] for idx in best_dispatch],
                "line_indices": [jobs[idx]["line_index"] for idx in best_dispatch],
            }
        )
    return {
        "status": "PASS" if len(done) == len(jobs) else "FAIL",
        "tick_count": len(ticks),
        "max_dispatch_per_tick": max(
            (tick["dispatch_count"] for tick in ticks), default=0
        ),
        "max_used_sites_per_tick": max(
            (tick["used_site_count"] for tick in ticks), default=0
        ),
        "all_hops_dispatched": len(done) == len(jobs),
        "ticks": ticks,
    }


def cyclic_supercycle_schedule(
    jobs: list[dict[str, Any]], spread_count: int, max_slots: int = 720
) -> dict[str, Any]:
    groups = packet_hop_groups(jobs)
    done: set[int] = set()
    active_ticks = []
    elapsed_slots = 0
    while len(done) < len(jobs) and elapsed_slots < max_slots:
        spread_index = elapsed_slots % spread_count
        dispatch, used_sites = schedule_for_spread(spread_index, jobs, done, groups)
        if dispatch:
            for job_index in dispatch:
                done.add(job_index)
            active_ticks.append(
                {
                    "slot": elapsed_slots,
                    "spread_epoch": spread_index,
                    "dispatch_count": len(dispatch),
                    "used_site_count": len(used_sites),
                    "jobs": [jobs[idx]["job_id"] for idx in dispatch],
                }
            )
        elapsed_slots += 1
    return {
        "status": "PASS" if len(done) == len(jobs) else "FAIL",
        "elapsed_spread_slots": elapsed_slots,
        "active_tick_count": len(active_ticks),
        "idle_slot_count": elapsed_slots - len(active_ticks),
        "all_hops_dispatched": len(done) == len(jobs),
        "active_ticks": active_ticks,
    }


def histogram(values: list[int]) -> dict[str, int]:
    return {str(value): values.count(value) for value in sorted(set(values))}


def build_bridge(
    reports: list[dict[str, Any]],
    contextuality: dict[str, Any],
    site_scheduler: dict[str, Any],
) -> dict[str, Any]:
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    line_to_spreads = {
        line_idx: [
            spread_idx
            for spread_idx, spread in enumerate(spreads)
            if line_idx in spread
        ]
        for line_idx in range(len(lines))
    }
    star_witnesses = point_star_witnesses(lines)
    jobs = build_hop_jobs(reports, lines, line_to_spreads)
    two_hop_overlap_counts = two_hop_intersections(jobs)
    greedy = greedy_line_schedule(jobs, len(spreads))
    cyclic = cyclic_supercycle_schedule(jobs, len(spreads))
    packet_count = sum(len(report.get("packets", [])) for report in reports)
    one_hop_packets = sum(
        1
        for report in reports
        for packet in report.get("packets", [])
        if packet["hops"] == 1
    )
    two_hop_packets = sum(
        1
        for report in reports
        for packet in report.get("packets", [])
        if packet["hops"] == 2
    )
    contextual_max = int(contextuality["max_satisfiable_contexts"])
    contextual_den = int(contextuality["contextual_fraction"]["denominator"])
    contextual_num = int(contextuality["contextual_fraction"]["numerator"])
    contextual_fraction = Fraction(contextual_num, contextual_den)

    theorem_checks = {
        "forty_line_contexts": len(lines) == W33["v"],
        "thirty_six_spreads": len(spreads) == contextual_max == 36,
        "spread_count_equals_ks_classical_ceiling": len(spreads) == contextual_max,
        "contextual_deficit_equals_mu": contextual_den - contextual_max == W33["mu"],
        "contextual_fraction_is_one_over_phi4": contextual_fraction
        == Fraction(1, W33["phi4"]),
        "each_spread_is_ten_disjoint_lines": all(
            len(spread) == W33["phi4"] for spread in spreads
        ),
        "each_line_lives_in_nine_spreads": set(
            len(values) for values in line_to_spreads.values()
        )
        == {W33["q"] ** 2},
        "all_hop_lines_have_nine_candidate_spreads": set(
            len(job["candidate_spreads"]) for job in jobs
        )
        == {W33["q"] ** 2},
        "two_hop_packets_are_two_phase": set(two_hop_overlap_counts) == {0},
        "all_point_stars_realize_contextual_deficit": star_witnesses["status"]
        == "PASS",
        "forty_movable_point_star_defects": star_witnesses["witness_count"] == W33["v"]
        and star_witnesses["unique_unsatisfied_point_stars"] == W33["v"],
        "point_star_defects_are_double_occupancy": star_witnesses[
            "unsatisfied_line_sum_profile_histogram"
        ]
        == {"(2, 2, 2, 2)": W33["v"]},
        "line_microkernel_dispatches_all_hops": greedy["status"] == "PASS",
        "cyclic_supercycle_dispatches_all_hops": cyclic["status"] == "PASS",
        "site_scheduler_is_strictly_coarser": site_scheduler["tick_count"]
        < greedy["tick_count"],
    }

    return {
        "schema": "w33.spread_contextual_microkernel_bridge.v1",
        "status": "PASS" if all(theorem_checks.values()) else "FAIL",
        "w33_parameters": W33,
        "spread_layer": spread_diagnostics(lines, spreads),
        "contextuality_layer": {
            "line_contexts": contextual_den,
            "max_satisfiable_contexts": contextual_max,
            "contextual_deficit": contextual_den - contextual_max,
            "contextual_fraction": contextuality["contextual_fraction"],
            "point_star_witnesses": star_witnesses,
            "source": str(DEFAULT_CONTEXTUALITY.relative_to(ROOT)),
        },
        "packet_layer": {
            "packet_count": packet_count,
            "one_hop_packets": one_hop_packets,
            "two_hop_packets": two_hop_packets,
            "hop_line_operations": len(jobs),
            "hop_line_formula_for_current_demo": (
                "56 = v + k + mu"
                if len(jobs) == W33["v"] + W33["k"] + W33["mu"]
                else None
            ),
            "candidate_spreads_per_hop_histogram": histogram(
                [len(job["candidate_spreads"]) for job in jobs]
            ),
            "two_hop_same_spread_intersection_histogram": histogram(
                two_hop_overlap_counts
            ),
        },
        "site_scheduler_boundary": {
            "source": str(DEFAULT_SITE_SCHEDULER.relative_to(ROOT)),
            "tick_count": site_scheduler["tick_count"],
            "packet_count": site_scheduler["packet_count"],
            "max_dispatch_per_tick": site_scheduler["max_dispatch_per_tick"],
            "reading": (
                "The site scheduler is a control-envelope proof: because every spread covers all 40 sites, "
                "every packet path is site-contained in every spread. It is not yet the stricter line-context clock."
            ),
        },
        "line_context_microkernel": {
            "job_count": len(jobs),
            "greedy_active_schedule": greedy,
            "fixed_36_spread_supercycle": cyclic,
            "reading": (
                "A hop line is executable in exactly 9 of the 36 spread frames. A two-hop route cannot execute "
                "as one disjoint spread operation because its two hop lines meet at the relay; it must be split "
                "into two ordered line-context micro-ops."
            ),
        },
        "theorem_checks": theorem_checks,
        "interpretation": (
            "The same integer 36 appears as the number of full W(3,3) spread frames and as the maximum number "
            "of line contexts a noncontextual KS assignment can satisfy. The verified architectural consequence "
            "is not a claimed bijection; it is a boundary: 36 full frames are the classical line-clock horizon, "
            "while the missing 4 contexts are the mu=4 contextual obstruction. The obstruction can be localized "
            "at any one W33 point as the four incident line clocks, and those clocks are overfull rather than empty. "
            "The Holonet wrapper therefore has two levels: a coarse site scheduler and a stricter line-context microkernel."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="output JSON")
    parser.add_argument(
        "--contextuality", default=str(DEFAULT_CONTEXTUALITY), help="contextuality JSON"
    )
    parser.add_argument(
        "--site-scheduler",
        default=str(DEFAULT_SITE_SCHEDULER),
        help="site scheduler JSON",
    )
    parser.add_argument("inputs", nargs="*", help="Holonet wrapper reports")
    args = parser.parse_args(argv)

    input_paths = (
        [normalize_path(path) for path in args.inputs]
        if args.inputs
        else DEFAULT_INPUTS
    )
    reports = [load_json(path) for path in input_paths]
    contextuality = load_json(normalize_path(args.contextuality))
    site_scheduler = load_json(normalize_path(args.site_scheduler))
    result = build_bridge(reports, contextuality, site_scheduler)

    output = normalize_path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"status: {result['status']}")
    print(
        f"spreads = KS ceiling: {result['spread_layer']['spread_count']} = {result['contextuality_layer']['max_satisfiable_contexts']}"
    )
    print(f"contextual deficit: {result['contextuality_layer']['contextual_deficit']}")
    print(f"hop-line jobs: {result['packet_layer']['hop_line_operations']}")
    print(
        f"line microkernel ticks: {result['line_context_microkernel']['greedy_active_schedule']['tick_count']}"
    )
    print(
        f"cyclic spread slots: {result['line_context_microkernel']['fixed_36_spread_supercycle']['elapsed_spread_slots']}"
    )
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
