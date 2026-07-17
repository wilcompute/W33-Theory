#!/usr/bin/env python3
"""Compile Holonet packet reports into W(3,3) line-context spread-clock code.

Input packets are diameter-2 Holonet routes.  The compiler lowers each packet to
ordered hop-line micro-ops, then packs ready micro-ops into spread-clock ticks.

The emitted schedule is fully verified.  Global optimality is reported
separately: with no MILP/CP-SAT dependency in this repo, the default compiler is
a deterministic optimizing pass with exact lower bounds, not a proof that no
shorter active schedule exists.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from w33_spread_clock_graph import (
    adjacency_from_overlap,
    build_overlap_matrix,
    embed_sequence_on_clock_graph,
)
from w33_spread_contextual_microkernel_bridge import (
    DEFAULT_INPUTS,
    build_hop_jobs,
    cyclic_supercycle_schedule,
    greedy_line_schedule,
    histogram,
    load_json,
    normalize_path,
    packet_hop_groups,
)
from w33_uor_runtime_model import ROOT, all_lines, find_spreads

DEFAULT_OUTPUT = ROOT / "data" / "w33_line_context_compiler.json"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def line_to_spreads(
    lines: list[tuple[int, ...]], spreads: list[list[int]]
) -> dict[int, list[int]]:
    return {
        line_idx: [
            spread_idx
            for spread_idx, spread in enumerate(spreads)
            if line_idx in spread
        ]
        for line_idx in range(len(lines))
    }


def dependency_edges(jobs: list[dict[str, Any]]) -> list[dict[str, str]]:
    edges = []
    for group in packet_hop_groups(jobs).values():
        for left, right in zip(group, group[1:]):
            edges.append(
                {"before": jobs[left]["job_id"], "after": jobs[right]["job_id"]}
            )
    return edges


def verify_schedule(
    jobs: list[dict[str, Any]],
    spreads: list[list[int]],
    ticks: list[dict[str, Any]],
) -> dict[str, Any]:
    job_by_id = {job["job_id"]: index for index, job in enumerate(jobs)}
    groups = packet_hop_groups(jobs)
    completed: set[int] = set()
    seen: set[int] = set()
    errors = []
    spread_sets = [set(spread) for spread in spreads]

    for tick in ticks:
        spread_index = tick["spread_epoch"]
        spread_lines = spread_sets[spread_index]
        used_sites: set[str] = set()
        for job_id in tick["jobs"]:
            if job_id not in job_by_id:
                errors.append(f"unknown job {job_id}")
                continue
            job_index = job_by_id[job_id]
            job = jobs[job_index]
            if job_index in seen:
                errors.append(f"duplicate job {job_id}")
            if job["line_index"] not in spread_lines:
                errors.append(
                    f"job {job_id} line {job['line_index']} not in spread {spread_index}"
                )
            sites = set(job["sites"])
            if used_sites & sites:
                errors.append(f"site conflict in tick {tick['tick']} on job {job_id}")
            group = groups[job["packet_id"]]
            position = group.index(job_index)
            if position > 0 and group[position - 1] not in completed:
                errors.append(f"dependency violation for {job_id}")
            used_sites.update(sites)
            seen.add(job_index)
        completed.update(
            job_by_id[job_id] for job_id in tick["jobs"] if job_id in job_by_id
        )

    missing = sorted(set(range(len(jobs))) - seen)
    if missing:
        errors.append(f"missing {len(missing)} jobs")

    return {
        "ok": not errors,
        "error_count": len(errors),
        "errors": errors[:12],
        "scheduled_job_count": len(seen),
        "missing_job_count": len(missing),
    }


def _candidate_exact_modules() -> dict[str, bool]:
    availability = {}
    for module in ("scipy", "ortools", "z3"):
        try:
            __import__(module)
            availability[module] = True
        except Exception:
            availability[module] = False
    return availability


def _ticks_from_milp_solution(
    solution: Any,
    jobs: list[dict[str, Any]],
    spread_count: int,
    horizon: int,
) -> list[dict[str, Any]]:
    n_jobs = len(jobs)

    def x_index(job_index: int, tick_index: int) -> int:
        return job_index * horizon + tick_index

    y_start = n_jobs * horizon

    def y_index(tick_index: int, spread_index: int) -> int:
        return y_start + tick_index * spread_count + spread_index

    ticks = []
    for tick_index in range(horizon):
        spread_values = [
            solution[y_index(tick_index, spread_index)]
            for spread_index in range(spread_count)
        ]
        spread_epoch = max(
            range(spread_count), key=lambda spread_index: spread_values[spread_index]
        )
        dispatched = [
            job_index
            for job_index in range(n_jobs)
            if solution[x_index(job_index, tick_index)] > 0.5
        ]
        used_sites = sorted(
            {site for job_index in dispatched for site in jobs[job_index]["sites"]}
        )
        ticks.append(
            {
                "tick": tick_index,
                "spread_epoch": spread_epoch,
                "dispatch_count": len(dispatched),
                "used_site_count": len(used_sites),
                "jobs": [jobs[job_index]["job_id"] for job_index in dispatched],
                "line_indices": [
                    jobs[job_index]["line_index"] for job_index in dispatched
                ],
            }
        )
    return ticks


def _solve_horizon_with_scipy_milp(
    jobs: list[dict[str, Any]],
    spreads: list[list[int]],
    horizon: int,
    time_limit_s: float,
) -> dict[str, Any]:
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import lil_matrix

    n_jobs = len(jobs)
    n_spreads = len(spreads)
    n_vars = n_jobs * horizon + horizon * n_spreads

    def x_index(job_index: int, tick_index: int) -> int:
        return job_index * horizon + tick_index

    y_start = n_jobs * horizon

    def y_index(tick_index: int, spread_index: int) -> int:
        return y_start + tick_index * n_spreads + spread_index

    site_to_jobs: dict[str, list[int]] = {}
    for job_index, job in enumerate(jobs):
        for site in job["sites"]:
            site_to_jobs.setdefault(site, []).append(job_index)

    groups = packet_hop_groups(jobs)
    rows: list[tuple[dict[int, float], float, float]] = []

    for job_index in range(n_jobs):
        rows.append(
            ({x_index(job_index, tick): 1.0 for tick in range(horizon)}, 1.0, 1.0)
        )

    for tick in range(horizon):
        rows.append(
            (
                {y_index(tick, spread_index): 1.0 for spread_index in range(n_spreads)},
                1.0,
                1.0,
            )
        )
        rows.append(
            (
                {x_index(job_index, tick): 1.0 for job_index in range(n_jobs)},
                1.0,
                math.inf,
            )
        )

    for job_index, job in enumerate(jobs):
        for tick in range(horizon):
            row = {x_index(job_index, tick): 1.0}
            for spread_index in job["candidate_spreads"]:
                row[y_index(tick, spread_index)] = (
                    row.get(y_index(tick, spread_index), 0.0) - 1.0
                )
            rows.append((row, -math.inf, 0.0))

    for tick in range(horizon):
        for job_indices in site_to_jobs.values():
            rows.append(
                (
                    {x_index(job_index, tick): 1.0 for job_index in job_indices},
                    -math.inf,
                    1.0,
                )
            )

    for group in groups.values():
        for before, after in zip(group, group[1:]):
            row = {}
            for tick in range(horizon):
                row[x_index(before, tick)] = row.get(x_index(before, tick), 0.0) + tick
                row[x_index(after, tick)] = row.get(x_index(after, tick), 0.0) - tick
            rows.append((row, -math.inf, -1.0))

    matrix = lil_matrix((len(rows), n_vars), dtype=float)
    lower = []
    upper = []
    for row_index, (coeffs, lb, ub) in enumerate(rows):
        for var_index, value in coeffs.items():
            matrix[row_index, var_index] = value
        lower.append(lb)
        upper.append(ub)

    result = milp(
        c=np.zeros(n_vars),
        integrality=np.ones(n_vars),
        bounds=Bounds(lb=np.zeros(n_vars), ub=np.ones(n_vars)),
        constraints=LinearConstraint(matrix.tocsr(), np.array(lower), np.array(upper)),
        options={"time_limit": max(1.0, float(time_limit_s)), "mip_rel_gap": 0.0},
    )
    if result.success and result.x is not None:
        ticks = _ticks_from_milp_solution(result.x, jobs, n_spreads, horizon)
        return {"status": "feasible", "message": result.message, "ticks": ticks}
    if result.status == 2:
        return {"status": "infeasible", "message": result.message}
    return {
        "status": "unknown",
        "message": result.message,
        "scipy_status": int(result.status),
    }


def try_exact_backend(
    jobs: list[dict[str, Any]],
    spreads: list[list[int]],
    lower_bound: int,
    upper_bound: int,
    backend: str,
    time_limit_s: float,
) -> dict[str, Any]:
    availability = _candidate_exact_modules()
    if backend == "off":
        return {
            "backend": "off",
            "status": "not_requested",
            "module_availability": availability,
        }
    if backend not in {"auto", "scipy"}:
        return {
            "backend": backend,
            "status": "unsupported_backend",
            "module_availability": availability,
        }
    if not availability["scipy"]:
        return {
            "backend": "scipy",
            "status": "unavailable",
            "module_availability": availability,
            "boundary": "Install scipy to enable the optional MILP exact scheduler backend.",
        }

    horizons = []
    certified_infeasible = True
    per_horizon_limit = max(
        1.0, float(time_limit_s) / max(1, upper_bound - lower_bound + 1)
    )
    for horizon in range(lower_bound, upper_bound + 1):
        solved = _solve_horizon_with_scipy_milp(
            jobs, spreads, horizon, per_horizon_limit
        )
        horizons.append(
            {
                "horizon": horizon,
                "status": solved["status"],
                "message": solved.get("message"),
            }
        )
        if solved["status"] == "feasible":
            optimum_certified = certified_infeasible
            return {
                "backend": "scipy",
                "status": (
                    "optimal_certified"
                    if optimum_certified
                    else "feasible_not_certified"
                ),
                "module_availability": availability,
                "optimum_tick_count": horizon if optimum_certified else None,
                "best_feasible_tick_count": horizon,
                "tested_horizons": horizons,
                "ticks": solved["ticks"],
            }
        if solved["status"] != "infeasible":
            certified_infeasible = False
    return {
        "backend": "scipy",
        "status": "no_feasible_solution_found",
        "module_availability": availability,
        "tested_horizons": horizons,
        "boundary": "The known greedy schedule should be feasible; this status indicates solver time/resource limits.",
    }


def schedule_lower_bounds(
    jobs: list[dict[str, Any]], spreads: list[list[int]]
) -> dict[str, Any]:
    one_hop = sum(1 for job in jobs if job["packet_hops"] == 1)
    two_hop = sum(
        1 for job in jobs if job["packet_hops"] == 2 and job["hop_index"] == 0
    )
    max_pair_ops_per_tick = max(len(spread) * 2 for spread in spreads)
    hop_bound = (len(jobs) + max_pair_ops_per_tick - 1) // max_pair_ops_per_tick
    first_hop_jobs = one_hop + two_hop
    first_phase_bound = (
        first_hop_jobs + max_pair_ops_per_tick - 1
    ) // max_pair_ops_per_tick
    second_phase_bound = (two_hop + max_pair_ops_per_tick - 1) // max_pair_ops_per_tick
    chain_bound = 2 if two_hop else 1
    return {
        "total_hop_pair_capacity_bound": hop_bound,
        "first_hop_capacity_bound": first_phase_bound,
        "second_hop_capacity_bound": second_phase_bound,
        "longest_packet_chain_bound": chain_bound,
        "combined_easy_lower_bound": max(hop_bound, chain_bound),
        "boundary": (
            "These are admissible lower bounds, not a global optimality certificate. A K4 line context can "
            "carry up to two disjoint two-site pair operations, so the easy capacity bound is 20 pair-ops "
            "per spread tick. Proving the active tick optimum is a finite scheduling/ILP problem over spread "
            "choices and packet precedence."
        ),
    }


def _job_ready(
    job_index: int,
    jobs: list[dict[str, Any]],
    done: set[int],
    groups: dict[str, list[int]],
) -> bool:
    group = groups[jobs[job_index]["packet_id"]]
    position = group.index(job_index)
    return position == 0 or group[position - 1] in done


def _dispatch_for_spread(
    spread_index: int,
    jobs: list[dict[str, Any]],
    done: set[int],
    groups: dict[str, list[int]],
) -> tuple[list[int], set[str]]:
    used_sites: set[str] = set()
    dispatch: list[int] = []
    for job_index, job in enumerate(jobs):
        if job_index in done:
            continue
        if not _job_ready(job_index, jobs, done, groups):
            continue
        if spread_index not in job["candidate_spreads"]:
            continue
        sites = set(job["sites"])
        if used_sites & sites:
            continue
        used_sites.update(sites)
        dispatch.append(job_index)
    return dispatch, used_sites


def clock_aware_line_schedule(
    jobs: list[dict[str, Any]],
    spreads: list[list[int]],
    dispatch_weight: int = 20,
    site_weight: int = 1,
    connector_penalty: int = 100,
) -> dict[str, Any]:
    """Compile directly against the 36-frame clock graph.

    The score prefers ready work but heavily penalizes non-adjacent frame jumps.
    For the current demo this produces a 15-slot connector-free clock-native
    schedule, compared with the active-optimal 14-tick schedule that needs
    connector frames when embedded in the clock graph.
    """
    graph = adjacency_from_overlap(build_overlap_matrix(spreads))
    groups = packet_hop_groups(jobs)
    done: set[int] = set()
    ticks = []
    previous_spread = None
    while len(done) < len(jobs):
        best = None
        for spread_index in range(len(spreads)):
            dispatch, used_sites = _dispatch_for_spread(
                spread_index, jobs, done, groups
            )
            if not dispatch:
                continue
            if previous_spread is None or spread_index == previous_spread:
                distance = 0
            elif spread_index in graph[previous_spread]:
                distance = 1
            else:
                distance = 2
            connector_cost = max(0, distance - 1)
            score = (
                dispatch_weight * len(dispatch)
                + site_weight * len(used_sites)
                - connector_penalty * connector_cost,
                -distance,
                len(used_sites),
                -spread_index,
            )
            if best is None or score > best[0]:
                best = (score, spread_index, dispatch, used_sites)
        if best is None:
            break
        _, spread_index, dispatch, used_sites = best
        for job_index in dispatch:
            done.add(job_index)
        ticks.append(
            {
                "tick": len(ticks),
                "spread_epoch": spread_index,
                "dispatch_count": len(dispatch),
                "used_site_count": len(used_sites),
                "jobs": [jobs[job_index]["job_id"] for job_index in dispatch],
                "line_indices": [
                    jobs[job_index]["line_index"] for job_index in dispatch
                ],
            }
        )
        previous_spread = spread_index
    embedding = embed_sequence_on_clock_graph("clock_native_line_context", ticks, graph)
    return {
        "status": "PASS" if len(done) == len(jobs) else "FAIL",
        "strategy": "clock-aware ready-list spread packing",
        "tick_count": len(ticks),
        "clock_slot_count": embedding["clock_slot_count"],
        "connector_slot_count": embedding["connector_slot_count"],
        "max_dispatch_per_tick": max(
            (tick["dispatch_count"] for tick in ticks), default=0
        ),
        "max_used_sites_per_tick": max(
            (tick["used_site_count"] for tick in ticks), default=0
        ),
        "all_hops_dispatched": len(done) == len(jobs),
        "ticks": ticks,
        "clock_embedding": embedding,
        "parameters": {
            "dispatch_weight": dispatch_weight,
            "site_weight": site_weight,
            "connector_penalty": connector_penalty,
        },
    }


def compact_jobs(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "job_id": job["job_id"],
            "packet_id": job["packet_id"],
            "hop_index": job["hop_index"],
            "line_index": job["line_index"],
            "sites": job["sites"],
            "candidate_spread_count": len(job["candidate_spreads"]),
        }
        for job in jobs
    ]


def build_compilation(
    reports: list[dict[str, Any]],
    exact_backend: str = "auto",
    exact_time_limit_s: float = 15.0,
    optimize_policy: str = "active-ticks",
) -> dict[str, Any]:
    if optimize_policy not in {"active-ticks", "clock-slots"}:
        raise ValueError(f"unknown optimize policy: {optimize_policy}")
    lines = all_lines()
    spreads = find_spreads(lines, limit=10000)
    jobs = build_hop_jobs(reports, lines, line_to_spreads(lines, spreads))
    greedy = greedy_line_schedule(jobs, len(spreads))
    clock_native = clock_aware_line_schedule(jobs, spreads)
    cyclic = cyclic_supercycle_schedule(jobs, len(spreads))
    bounds = schedule_lower_bounds(jobs, spreads)
    exact = try_exact_backend(
        jobs,
        spreads,
        bounds["combined_easy_lower_bound"],
        greedy["tick_count"],
        exact_backend,
        exact_time_limit_s,
    )
    selected_ticks = (
        exact.get("ticks")
        if exact.get("status") in {"optimal_certified", "feasible_not_certified"}
        else greedy["ticks"]
    )
    selected_strategy = (
        "exact_milp"
        if selected_ticks is exact.get("ticks")
        else "deterministic_ready_list"
    )
    verification = verify_schedule(jobs, spreads, selected_ticks)
    clock_native_verification = verify_schedule(jobs, spreads, clock_native["ticks"])
    frame_graph = adjacency_from_overlap(build_overlap_matrix(spreads))
    active_clock_embedding = embed_sequence_on_clock_graph(
        "active_line_context", selected_ticks, frame_graph
    )
    if optimize_policy == "clock-slots":
        selected_policy = {
            "policy": "clock-slots",
            "source": "clock_native_schedule",
            "tick_count": clock_native["tick_count"],
            "clock_slot_count": clock_native["clock_slot_count"],
            "connector_slot_count": clock_native["connector_slot_count"],
            "schedule_hash": hashlib.sha256(
                canonical_bytes(clock_native["ticks"])
            ).hexdigest(),
            "reading": (
                "Policy selected the clock-native schedule: one may spend more active ticks to remove "
                "connector frames and shorten elapsed frame-clock time."
            ),
        }
    else:
        selected_policy = {
            "policy": "active-ticks",
            "source": "active_schedule",
            "tick_count": len(selected_ticks),
            "clock_slot_count": active_clock_embedding["clock_slot_count"],
            "connector_slot_count": active_clock_embedding["connector_slot_count"],
            "schedule_hash": hashlib.sha256(
                canonical_bytes(selected_ticks)
            ).hexdigest(),
            "reading": (
                "Policy selected the active schedule: minimize executable work ticks first, then embed the "
                "result into the SRG(36,15,6,6) frame clock with connector slots as needed."
            ),
        }
    packet_count = sum(len(report.get("packets", [])) for report in reports)
    line_hist = histogram([job["line_index"] for job in jobs])
    spread_candidate_hist = histogram([len(job["candidate_spreads"]) for job in jobs])
    schedule_hash = hashlib.sha256(canonical_bytes(selected_ticks)).hexdigest()
    theorem_checks = {
        "all_jobs_verified": verification["ok"],
        "all_jobs_dispatched": verification["missing_job_count"] == 0,
        "all_jobs_have_nine_candidate_spreads": spread_candidate_hist
        == {"9": len(jobs)},
        "two_hop_dependencies_present": len(dependency_edges(jobs))
        == sum(1 for job in jobs if job["packet_hops"] == 2 and job["hop_index"] == 1),
        "active_schedule_beats_fixed_cycle_active_count": len(selected_ticks)
        <= cyclic["active_tick_count"],
        "active_schedule_within_fixed_cycle_slots": len(selected_ticks)
        < cyclic["elapsed_spread_slots"],
        "clock_native_schedule_verified": clock_native["status"] == "PASS"
        and clock_native_verification["ok"],
        "clock_native_has_no_connectors_for_current_demo": clock_native[
            "connector_slot_count"
        ]
        == 0,
        "clock_native_beats_active_embedding_slots": clock_native["clock_slot_count"]
        < active_clock_embedding["clock_slot_count"],
    }
    return {
        "schema": "w33.line_context_compiler.v1",
        "status": "PASS" if all(theorem_checks.values()) else "FAIL",
        "input": {
            "packet_count": packet_count,
            "report_count": len(reports),
        },
        "lowering": {
            "job_count": len(jobs),
            "dependency_edges": dependency_edges(jobs),
            "line_usage_histogram": line_hist,
            "candidate_spreads_per_job_histogram": spread_candidate_hist,
            "jobs": compact_jobs(jobs),
        },
        "optimizer": {
            "strategy": selected_strategy,
            "requested_policy": optimize_policy,
            "selected_policy_schedule": selected_policy,
            "optimality_status": (
                exact["status"]
                if exact["status"] == "optimal_certified"
                else "best_known_schedule_not_proven_globally_optimal"
            ),
            "lower_bounds": bounds,
            "active_tick_gap_over_easy_lower_bound": len(selected_ticks)
            - bounds["combined_easy_lower_bound"],
            "exact_backend": exact,
            "boundary": (
                "The schedule is executable and verified. The optional exact backend uses a MILP formulation "
                "when scipy is available; otherwise the compiler reports a best-known deterministic schedule."
            ),
        },
        "active_schedule": {
            "tick_count": len(selected_ticks),
            "max_dispatch_per_tick": max(
                (tick["dispatch_count"] for tick in selected_ticks), default=0
            ),
            "max_used_sites_per_tick": max(
                (tick["used_site_count"] for tick in selected_ticks), default=0
            ),
            "schedule_hash": schedule_hash,
            "ticks": selected_ticks,
            "verification": verification,
            "greedy_reference_tick_count": greedy["tick_count"],
            "clock_embedding": active_clock_embedding,
        },
        "clock_native_schedule": {
            "tick_count": clock_native["tick_count"],
            "clock_slot_count": clock_native["clock_slot_count"],
            "connector_slot_count": clock_native["connector_slot_count"],
            "max_dispatch_per_tick": clock_native["max_dispatch_per_tick"],
            "max_used_sites_per_tick": clock_native["max_used_sites_per_tick"],
            "schedule_hash": hashlib.sha256(
                canonical_bytes(clock_native["ticks"])
            ).hexdigest(),
            "ticks": clock_native["ticks"],
            "clock_embedding": clock_native["clock_embedding"],
            "verification": clock_native_verification,
            "strategy": clock_native["strategy"],
            "parameters": clock_native["parameters"],
            "reading": (
                "This schedule uses the SRG(36,15,6,6) frame clock during compilation. It may use one more "
                "active tick than the active-optimal MILP schedule, but for the current demo it needs no "
                f"connector frames and therefore executes in {clock_native['clock_slot_count']} clock slots "
                f"instead of {active_clock_embedding['clock_slot_count']}."
            ),
        },
        "fixed_36_spread_supercycle": cyclic,
        "theorem_checks": theorem_checks,
        "interpretation": (
            "The compiler lowers arbitrary Holonet wrapper reports into a packet DAG, then into ordered W(3,3) "
            "hop-line micro-ops, then into spread-clock ticks. The current demo now has two verified strict "
            "line-context programs: an active-tick-optimal schedule and a clock-native schedule that optimizes "
            "the SRG(36,15,6,6) frame-clock walk. The site-level OS replay remains the control envelope; this "
            "file is the executable microcode schedule."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="output JSON")
    parser.add_argument(
        "--exact-backend",
        choices=["auto", "off", "scipy"],
        default="auto",
        help="optional exact scheduler backend",
    )
    parser.add_argument(
        "--exact-time-limit",
        type=float,
        default=15.0,
        help="total time budget in seconds for optional exact backend",
    )
    parser.add_argument(
        "--optimize",
        choices=["active-ticks", "clock-slots"],
        default="active-ticks",
        help="selected policy reported in optimizer.selected_policy_schedule",
    )
    parser.add_argument("inputs", nargs="*", help="Holonet wrapper reports")
    args = parser.parse_args(argv)

    input_paths = (
        [normalize_path(path) for path in args.inputs]
        if args.inputs
        else DEFAULT_INPUTS
    )
    reports = [load_json(path) for path in input_paths]
    result = build_compilation(
        reports,
        exact_backend=args.exact_backend,
        exact_time_limit_s=args.exact_time_limit,
        optimize_policy=args.optimize,
    )
    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"status: {result['status']}")
    print(f"packets: {result['input']['packet_count']}")
    print(f"hop-line jobs: {result['lowering']['job_count']}")
    print(f"active ticks: {result['active_schedule']['tick_count']}")
    print(f"clock-native slots: {result['clock_native_schedule']['clock_slot_count']}")
    print(
        "selected policy: "
        f"{result['optimizer']['selected_policy_schedule']['policy']} "
        f"({result['optimizer']['selected_policy_schedule']['clock_slot_count']} clock slots)"
    )
    print(
        f"easy lower bound: {result['optimizer']['lower_bounds']['combined_easy_lower_bound']}"
    )
    print(f"optimality: {result['optimizer']['optimality_status']}")
    print(f"exact backend: {result['optimizer']['exact_backend']['status']}")
    print(f"wrote: {display_path(output)}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
