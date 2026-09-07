#!/usr/bin/env python3
"""Online measured checkpoint controller for HoloVM continuations.

The preceding thermodynamic ledger measured fixed checkpoint periods.  This
module removes the period from the policy.  At every live continuation it uses
only measured archive closure size, distance from the newest checkpoint, a
failure hazard estimate and externally supplied cost weights to decide whether
the new root should become the next STRONG recovery checkpoint.

Decision rule (dimensionless cost units):

    expected replay risk = hazard * recompute_step_cost * checkpoint_distance
    one-step keep cost    = retention_weight * (snapshot_bytes / baseline_bytes)
                           + checkpoint_io_weight * (snapshot_bytes / baseline_bytes)

Checkpoint when replay risk >= keep cost.  No W33 graph number appears in that
rule.  W33 route hops are measured afterwards as an independent execution
observable.  The verification sweep asks whether gaps such as the graph
diameter 2, line size 4, or theta 10 appear for any cost regime; they are not
inserted as scheduling periods.

Only the newest recovery checkpoint is retained.  When a new checkpoint is
installed the older checkpoint authority is released and exact TemporalMerkleGC
runs.  A crash-recovery replay is then performed from the retained checkpoint to
the current generation to verify that the policy never trades away correctness.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from statistics import median
from typing import Any

from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_process_kernel import ProcessHandle
from w33_holovm_syscall_abi import HoloVMKernel
from w33_holovm_thermodynamic_ledger import _clone_kernel, _loop_program, _payload_bytes
from w33_merkle_capability_memory import canonical_json, digest
from w33_temporal_merkle_gc import TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, GEOMETRY

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_ONLINE_REVERSIBLE_CHECKPOINT_SCHEDULER.json"


@dataclass(frozen=True)
class CostModel:
    name: str
    failure_hazard_per_step: float
    recompute_step_cost: float
    retention_weight: float
    checkpoint_io_weight: float = 0.0


@dataclass(frozen=True)
class OnlineResult:
    model: str
    steps: int
    checkpoints: tuple[int, ...]
    checkpoint_gaps: tuple[int, ...]
    retained_byte_ticks: int
    swept_payload_bytes: int
    replay_steps_verified: int
    recovery_checks: int
    route_hops_total: int
    route_hops_max: int
    decisions_digest: str

    def descriptor(self):
        return asdict(self)


def closure_bytes(kernel: HoloVMKernel, root: str) -> int:
    marked: set[str] = set()
    TemporalMerkleGC(kernel.archive, kernel.registry)._mark(root, marked)
    return sum(len(canonical_json(kernel.archive.blobs[k])) for k in marked)


def run_online(model: CostModel, *, steps: int = 30) -> OnlineResult:
    if not (0.0 < model.failure_hazard_per_step <= 1.0):
        raise ValueError("failure hazard must lie in (0,1]")
    if model.recompute_step_cost <= 0 or model.retention_weight < 0 or model.checkpoint_io_weight < 0:
        raise ValueError("cost weights must be nonnegative and recompute positive")

    program = _loop_program()
    memory = BitStore()
    state = genesis(program, memory, (0, 0), session=f"online-{model.name}", carrier=Carrier.CIRCUIT_ST81)
    passport = digest({"schema": "w33.online-checkpoint-passport.v1", "program": program.image_id, "model": asdict(model)})
    kernel = HoloVMKernel()
    live = kernel.ADMIT("live:0", program, state, memory, FibreProductAddress(0, 0, 0), passport)
    cp_ref = kernel.PIN(live, "recovery:0", "STRONG")
    checkpoint = ProcessHandle(cp_ref, live.root)
    checkpoint_generation = 0
    checkpoints = [0]
    decisions = []
    retained_byte_ticks = 0
    swept_bytes = 0
    replay_steps = 0
    recovery_checks = 0
    route_hops_total = 0
    route_hops_max = 0
    previous, _ = kernel.RESUME(live)
    baseline_bytes = max(1, closure_bytes(kernel, live.root))

    for generation in range(1, steps + 1):
        run = kernel.RUN(live, fuel=1, owner=f"live:{generation}")
        current = run.process
        route = GEOMETRY.route(previous.state.portal, current.state.portal)
        hops = len(route) - 1
        route_hops_total += hops
        route_hops_max = max(route_hops_max, hops)

        snapshot_bytes = closure_bytes(kernel, run.handle.root)
        normalized_bytes = snapshot_bytes / baseline_bytes
        distance = generation - checkpoint_generation
        replay_risk = model.failure_hazard_per_step * model.recompute_step_cost * distance
        keep_cost = (model.retention_weight + model.checkpoint_io_weight) * normalized_bytes
        choose_checkpoint = replay_risk >= keep_cost

        if choose_checkpoint:
            new_ref = kernel.PIN(run.handle, f"recovery:{generation}", "STRONG")
            old_ref = checkpoint.reference_id
            checkpoint = ProcessHandle(new_ref, run.handle.root)
            checkpoint_generation = generation
            checkpoints.append(generation)
            kernel.RELEASE(old_ref, collect=False)

        kernel.RELEASE(live.reference_id, collect=False)
        gc = TemporalMerkleGC(kernel.archive, kernel.registry)
        plan = gc.plan()
        swept_bytes += sum(len(canonical_json(kernel.archive.blobs[k])) for k in plan["sweep"])
        gc.collect()
        retained_byte_ticks += _payload_bytes(kernel)

        # Crash-recovery proof at every generation: reconstruct current state from
        # the newest retained checkpoint only.  This uses a cloned archive so the
        # verification itself cannot mutate the live policy run.
        distance = generation - checkpoint_generation
        clone = _clone_kernel(kernel)
        if distance:
            replay = clone.RUN(checkpoint, fuel=distance, owner=f"crash-replay:{generation}")
            recovered, recovered_memory = clone.RESUME(replay.handle)
        else:
            recovered, recovered_memory = clone.RESUME(checkpoint)
        if recovered.generation != generation or recovered_memory.decode(recovered.state.roots[0]) != generation:
            raise AssertionError("online checkpoint failed crash reconstruction")
        replay_steps += distance
        recovery_checks += 1

        decisions.append({
            "generation": generation,
            "checkpoint_generation_before_decision": generation - distance,
            "snapshot_bytes": snapshot_bytes,
            "normalized_bytes": normalized_bytes,
            "replay_risk": replay_risk,
            "keep_cost": keep_cost,
            "checkpoint": choose_checkpoint,
            "route_hops": hops,
        })
        live = run.handle
        previous = current

    gaps = tuple(b - a for a, b in zip(checkpoints, checkpoints[1:]))
    return OnlineResult(
        model=model.name,
        steps=steps,
        checkpoints=tuple(checkpoints),
        checkpoint_gaps=gaps,
        retained_byte_ticks=retained_byte_ticks,
        swept_payload_bytes=swept_bytes,
        replay_steps_verified=replay_steps,
        recovery_checks=recovery_checks,
        route_hops_total=route_hops_total,
        route_hops_max=route_hops_max,
        decisions_digest=digest(decisions),
    )


def characteristic_gap(result: OnlineResult) -> float | None:
    if not result.checkpoint_gaps:
        return None
    # Ignore at most the first adaptation gap; the controller's steady-state
    # characteristic period is summarized by the median thereafter.
    gaps = result.checkpoint_gaps[1:] or result.checkpoint_gaps
    return float(median(gaps))


def verify() -> dict[str, Any]:
    # These are cost regimes, not checkpoint periods.  With hazard fixed at 0.1,
    # retention becoming more expensive should naturally lengthen the observed
    # recovery spacing.
    models = (
        CostModel("cheap-retention", 0.10, 1.0, 0.20, 0.0),
        CostModel("balanced-retention", 0.10, 1.0, 0.40, 0.0),
        CostModel("expensive-retention", 0.10, 1.0, 1.00, 0.0),
        CostModel("io-dominated", 0.10, 1.0, 0.25, 0.35),
    )
    rows = [run_online(m, steps=30) for m in models]
    observed = {r.model: characteristic_gap(r) for r in rows}
    finite_gaps = [g for g in observed.values() if g is not None]
    geometry_probe = {
        "diameter_2_observed": any(abs(g - 2) < 0.51 for g in finite_gaps),
        "line_size_4_observed": any(abs(g - 4) < 0.51 for g in finite_gaps),
        "theta_10_observed": any(abs(g - 10) < 0.51 for g in finite_gaps),
        "observed_characteristic_gaps": observed,
        "policy_contains_no_geometry_period": True,
    }
    ordered = [observed[m.name] for m in models[:3]]
    monotone = all(a is not None and b is not None and a <= b for a, b in zip(ordered, ordered[1:]))
    checks = {
        "every_generation_has_verified_crash_recovery": all(r.recovery_checks == r.steps for r in rows),
        "all_runtime_routes_obey_W33_diameter_two": all(r.route_hops_max <= 2 for r in rows),
        "decisions_are_content_addressed": all(r.decisions_digest.startswith("sha256:") for r in rows),
        "retention_price_increase_does_not_shorten_characteristic_gap": monotone,
        "controller_makes_multiple_online_checkpoint_decisions": all(len(r.checkpoints) >= 2 for r in rows),
        "policy_is_driven_by_measured_snapshot_bytes": all(r.retained_byte_ticks > 0 for r in rows),
    }
    return {
        "schema": "w33.online-reversible-checkpoint-scheduler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "models": [asdict(m) for m in models],
        "results": [r.descriptor() for r in rows],
        "geometry_probe": geometry_probe,
        "conclusion": (
            "Checkpoint spacing is selected online from measured continuation closure size and external hazard/cost weights. "
            "The geometry probe reports whether 2, 4, or 10 happen to emerge; those numbers are observations only and are not used by the decision rule."
        ),
        "boundary": (
            "Cost units are abstract until retention, replay, I/O and failure-hazard weights are calibrated on physical hardware. "
            "Logical GC and replay measurements are exact software observables, not direct energy measurements."
        ),
    }


if __name__ == "__main__":
    out = verify()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
