#!/usr/bin/env python3
"""Measured logical retention/GC/recomputation ledger for HoloVM continuations.

The older reversible-storage model gives a Bennett-style analytic trade surface.
This file complements it with *actual process-kernel events* over an executing
continuation graph.  For several checkpoint intervals it records:

  * STRONG checkpoint pins;
  * live-root releases;
  * exact canonical blob bytes retained after each collection;
  * exact canonical blob bytes made unreachable and swept;
  * actual deterministic recomputation from retained checkpoints;
  * W33 route hops for each guest transition; and
  * a CONDITIONAL Landauer lower bound for the swept logical payload bits.

The last number is deliberately not a hardware-energy claim.  Landauer's bound
k_B T ln 2 applies to irreversible reset of an unknown physical bit.  A Python
GC removing a content-addressed blob does not establish that the corresponding
number of independent physical bits were reset, nor that the device operated at
the chosen temperature.  We report the multiplication only as a conditional
lower bound if those extra physical assumptions were later demonstrated.

Literature boundary: Bennett reversible checkpointing supplies the time/space
trade idea; Landauer supplies the irreversible-reset lower bound.  The measured
blob counts, process roots and replay distances here belong to this repository's
concrete HoloVM implementation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from typing import Any

from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_process_kernel import ProcessHandle
from w33_holovm_syscall_abi import HoloVMKernel
from w33_merkle_capability_memory import canonical_json, digest
from w33_temporal_merkle_gc import TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, GEOMETRY, Instruction, Program

K_B = 1.380649e-23  # J/K, exact SI definition
DEFAULT_TEMPERATURE_K = 300.0


@dataclass(frozen=True)
class PolicyResult:
    interval: int
    steps: int
    checkpoint_generations: tuple[int, ...]
    strong_checkpoint_pins: int
    live_releases: int
    gc_events: int
    swept_blobs: int
    swept_payload_bytes: int
    logical_unreachable_payload_bits: int
    conditional_landauer_joules_at_300K: float
    retained_byte_ticks: int
    peak_retained_payload_bytes: int
    final_retained_payload_bytes: int
    recomputation_steps_total: int
    recomputation_steps_mean: float
    recomputation_replays_verified: int
    route_hops_total: int
    route_hops_max: int

    def descriptor(self) -> dict[str, Any]:
        return asdict(self)


def _payload_bytes(kernel: HoloVMKernel) -> int:
    return sum(len(canonical_json(row)) for row in kernel.archive.blobs.values())


def conditional_landauer(bits: int, temperature_k: float = DEFAULT_TEMPERATURE_K) -> float:
    if type(bits) is not int or bits < 0:
        raise ValueError("bits must be a natural number")
    if not math.isfinite(temperature_k) or temperature_k <= 0:
        raise ValueError("temperature must be positive finite")
    return bits * K_B * temperature_k * math.log(2.0)


def _loop_program() -> Program:
    # Infinite two-PC guest.  Every step increments r0, while alternating PCs
    # forces the W33 layout/router to execute real (generally nonzero) portal
    # transitions instead of making the diameter check vacuous at one portal.
    return Program(
        (
            Instruction("INC", 0, 1),
            Instruction("INC", 0, 0),
        ),
        name="holovm-thermo-two-pc-increment-loop",
    )


def _clone_kernel(source: HoloVMKernel) -> HoloVMKernel:
    out = HoloVMKernel()
    out.archive.blobs = dict(source.archive.blobs)
    out.registry.references = dict(source.registry.references)
    out.programs = dict(source.programs)
    return out


def run_policy(interval: int, *, steps: int = 16) -> PolicyResult:
    if type(interval) is not int or interval <= 0:
        raise ValueError("checkpoint interval must be a positive integer")
    if type(steps) is not int or steps <= 0:
        raise ValueError("steps must be positive")

    program = _loop_program()
    memory = BitStore()
    state = genesis(
        program,
        memory,
        (0, 0),
        session=f"thermo-i{interval}",
        carrier=Carrier.CIRCUIT_ST81,
    )
    passport = digest({
        "schema": "w33.holovm-thermo-demo-passport.v1",
        "program": program.image_id,
        "interval": interval,
    })
    kernel = HoloVMKernel()
    live = kernel.ADMIT(
        "live:0",
        program,
        state,
        memory,
        FibreProductAddress(0, 0, 0),
        passport,
    )

    checkpoint_handles: dict[int, ProcessHandle] = {}
    pin0 = kernel.PIN(live, "checkpoint:0", "STRONG")
    checkpoint_handles[0] = ProcessHandle(pin0, live.root)

    retained_byte_ticks = 0
    peak = _payload_bytes(kernel)
    swept_blobs = 0
    swept_bytes = 0
    route_hops_total = 0
    route_hops_max = 0
    releases = 0
    gc_events = 0

    previous_process, _ = kernel.RESUME(live)
    for generation in range(1, steps + 1):
        run = kernel.RUN(live, fuel=1, owner=f"live:{generation}")
        current = run.process
        route = GEOMETRY.route(previous_process.state.portal, current.state.portal)
        hops = len(route) - 1
        route_hops_total += hops
        route_hops_max = max(route_hops_max, hops)

        if generation % interval == 0 or generation == steps:
            ref = kernel.PIN(run.handle, f"checkpoint:{generation}", "STRONG")
            checkpoint_handles[generation] = ProcessHandle(ref, run.handle.root)

        # Relinquish only the old live reference. Checkpoint references, when
        # present, keep their exact closures reachable.
        kernel.RELEASE(live.reference_id, collect=False)
        releases += 1
        plan = TemporalMerkleGC(kernel.archive, kernel.registry).plan()
        sweep_keys = set(plan["sweep"])
        event_swept_bytes = sum(len(canonical_json(kernel.archive.blobs[k])) for k in sweep_keys)
        collected = TemporalMerkleGC(kernel.archive, kernel.registry).collect()
        gc_events += 1
        swept_blobs += collected["collected"]
        swept_bytes += event_swept_bytes

        live = run.handle
        previous_process = current
        now = _payload_bytes(kernel)
        retained_byte_ticks += now
        peak = max(peak, now)

    final_bytes = _payload_bytes(kernel)

    # Actual replay verification: for every logical failure generation choose
    # the newest retained checkpoint not later than the target, clone the final
    # archive/registry, and execute the exact missing number of steps.
    checkpoint_generations = tuple(sorted(checkpoint_handles))
    replay_steps = 0
    replay_verified = 0
    for target_generation in range(1, steps + 1):
        base_generation = max(g for g in checkpoint_generations if g <= target_generation)
        distance = target_generation - base_generation
        replay_steps += distance
        clone = _clone_kernel(kernel)
        base_handle = checkpoint_handles[base_generation]
        if distance:
            replay = clone.RUN(base_handle, fuel=distance, owner=f"recovery:{target_generation}")
            recovered = replay.process
        else:
            recovered, _ = clone.RESUME(base_handle)
        recovered_memory = clone.RESUME(replay.handle if distance else base_handle)[1]
        if (
            recovered.generation == target_generation
            and recovered_memory.decode(recovered.state.roots[0]) == target_generation
        ):
            replay_verified += 1
        else:
            raise AssertionError("checkpoint recomputation did not reconstruct target generation")

    logical_bits = swept_bytes * 8
    return PolicyResult(
        interval=interval,
        steps=steps,
        checkpoint_generations=checkpoint_generations,
        strong_checkpoint_pins=len(checkpoint_generations),
        live_releases=releases,
        gc_events=gc_events,
        swept_blobs=swept_blobs,
        swept_payload_bytes=swept_bytes,
        logical_unreachable_payload_bits=logical_bits,
        conditional_landauer_joules_at_300K=conditional_landauer(logical_bits),
        retained_byte_ticks=retained_byte_ticks,
        peak_retained_payload_bytes=peak,
        final_retained_payload_bytes=final_bytes,
        recomputation_steps_total=replay_steps,
        recomputation_steps_mean=replay_steps / steps,
        recomputation_replays_verified=replay_verified,
        route_hops_total=route_hops_total,
        route_hops_max=route_hops_max,
    )


def dominates(a: PolicyResult, b: PolicyResult) -> bool:
    return (
        a.retained_byte_ticks <= b.retained_byte_ticks
        and a.recomputation_steps_total <= b.recomputation_steps_total
        and (
            a.retained_byte_ticks < b.retained_byte_ticks
            or a.recomputation_steps_total < b.recomputation_steps_total
        )
    )


def pareto(rows: list[PolicyResult]) -> list[PolicyResult]:
    return [b for b in rows if not any(a is not b and dominates(a, b) for a in rows)]


def verify() -> dict[str, Any]:
    intervals = (1, 2, 4, 8)
    rows = [run_policy(i, steps=16) for i in intervals]
    frontier = pareto(rows)
    by_interval = {row.interval: row for row in rows}

    retention_monotone = all(
        by_interval[a].retained_byte_ticks >= by_interval[b].retained_byte_ticks
        for a, b in zip(intervals, intervals[1:])
    )
    recompute_monotone = all(
        by_interval[a].recomputation_steps_total <= by_interval[b].recomputation_steps_total
        for a, b in zip(intervals, intervals[1:])
    )
    frontier_intervals = {row.interval for row in frontier}
    exact_sweep_accounting = all(
        row.logical_unreachable_payload_bits == 8 * row.swept_payload_bytes
        for row in rows
    )
    sparse_policies_really_collect = all(
        by_interval[i].swept_payload_bytes > 0 for i in (2, 4, 8)
    )
    checks = {
        "all_actual_recovery_replays_reconstruct_every_generation": all(row.recomputation_replays_verified == row.steps for row in rows),
        "every_policy_releases_one_live_root_per_step": all(row.live_releases == row.steps for row in rows),
        "every_release_cycle_runs_exact_collection": all(row.gc_events == row.steps for row in rows),
        "all_actual_W33_guest_routes_obey_diameter_two": all(row.route_hops_max <= 2 for row in rows),
        "routing_workload_is_nontrivial": all(row.route_hops_total > 0 for row in rows),
        "larger_checkpoint_intervals_reduce_or_equal_retained_byte_ticks": retention_monotone,
        "larger_checkpoint_intervals_increase_or_equal_recomputation": recompute_monotone,
        "interval_one_has_zero_recomputation": by_interval[1].recomputation_steps_total == 0,
        "interval_one_has_zero_sweep_because_every_generation_is_strong": by_interval[1].swept_payload_bytes == 0 and by_interval[1].strong_checkpoint_pins == 17,
        "logical_sweep_accounting_is_exact_for_zero_and_nonzero_cases": exact_sweep_accounting,
        "sparser_checkpoint_policies_really_collect_payload": sparse_policies_really_collect,
        "conditional_Landauer_formula_is_exactly_kBTln2_per_logical_bit": all(
            math.isclose(
                row.conditional_landauer_joules_at_300K,
                row.logical_unreachable_payload_bits * K_B * DEFAULT_TEMPERATURE_K * math.log(2.0),
                rel_tol=1e-15,
            ) for row in rows
        ),
        "W33_diameter2_and_line_size4_policies_are_on_measured_pareto_surface": 2 in frontier_intervals and 4 in frontier_intervals,
        "geometry_does_not_select_a_unique_energy_optimum_without_physical_weights": len(frontier_intervals) >= 2,
    }
    return {
        "schema": "w33.holovm-thermodynamic-ledger.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "temperature_K_for_conditional_bound": DEFAULT_TEMPERATURE_K,
        "policies": [row.descriptor() for row in rows],
        "pareto_intervals": sorted(frontier_intervals),
        "geometry_probe": {
            "W33_diameter": 2,
            "W33_line_size": 4,
            "routing_is_exercised": all(row.route_hops_total > 0 for row in rows),
            "both_geometry_aligned_intervals_are_pareto": 2 in frontier_intervals and 4 in frontier_intervals,
            "conclusion": (
                "The geometry-aligned checkpoint periods are viable Pareto points in this workload, but the finite geometry alone does not choose between retention and recomputation. "
                "A unique optimum requires measured byte-retention, recomputation, I/O and physical erasure costs."
            ),
        },
        "thermodynamic_boundary": (
            "swept_payload_bytes is an exact canonical-software payload measurement. logical_unreachable_payload_bits = 8*bytes is bookkeeping. "
            "Zero swept bytes at interval 1 is the measured dense-checkpoint limit, not missing data. "
            "The reported k_B T ln 2 product is only the lower bound that would apply if those bits corresponded to independent unknown physical bits irreversibly reset at 300 K; this software run does not establish that premise."
        ),
        "literature": {
            "Bennett_1989": "Time/Space Trade-Offs for Reversible Computation",
            "Landauer_principle": "irreversible reset of one unknown bit has lower bound k_B T ln 2",
        },
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
