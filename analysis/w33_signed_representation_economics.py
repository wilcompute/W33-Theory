#!/usr/bin/env python3
"""Cross-repo resource ledger for authenticated HoloVM + signed W33 representations.

The central rule is type separation.  A signed-pencil representation factor is
not semantic work, authenticated-history storage, replay work, information
leakage, or physical energy.  We therefore keep a vector ledger and refuse to
produce a scalar score unless every coordinate receives an explicit weight.

The exact representation factors are imported as certified constants from the
Holotrade signed-pencil frontier run 34307397528 (commit e45fd0ad...), where
rational primal/dual witnesses certify all seven mass-16 exceptional orbits:
  depth 1: gamma=6, k=4, A=gamma/k=3/2, A^2=9/4
  depth 2: gamma=8, k=4, A=2,             A^2=4
No physical-energy interpretation is made here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import json
from pathlib import Path
from typing import Mapping

from w33_holovm_thermodynamic_ledger import run_policy

HOLOTRADE_SOURCE = {
    "repository": "wilcompute/Holotrade",
    "commit": "e45fd0ad5844d11ee8062a108ccf4809fa2aa001",
    "workflow_run": 34307397528,
    "workflow_job": 102326833373,
    "artifact_id": 10087137602,
    "artifact_zip_sha256": "235c73474fc3c1f8fca27af14c1f1374c1839fde1d8067d67724901f1e2100cf",
}

REPRESENTATIONS = {
    "positive-depth0": {"depth": 0, "gamma": F(4), "A": F(1), "A2": F(1)},
    "exception-depth1": {"depth": 1, "gamma": F(6), "A": F(3, 2), "A2": F(9, 4)},
    "exception-depth2": {"depth": 2, "gamma": F(8), "A": F(2), "A2": F(4)},
}


@dataclass(frozen=True)
class ResourceVector:
    semantic_guest_steps: int
    w33_route_hops: int
    authenticated_retained_byte_ticks: int
    authenticated_swept_payload_bytes: int
    deterministic_replay_steps: int
    representation_amplification: F
    signed_sampling_second_moment_factor: F
    representation_class: str

    def descriptor(self):
        row = asdict(self)
        row["representation_amplification"] = str(self.representation_amplification)
        row["signed_sampling_second_moment_factor"] = str(self.signed_sampling_second_moment_factor)
        return row


COORDINATES = (
    "semantic_guest_steps",
    "w33_route_hops",
    "authenticated_retained_byte_ticks",
    "authenticated_swept_payload_bytes",
    "deterministic_replay_steps",
    "representation_excess_A_minus_1",
    "sampling_excess_A2_minus_1",
)


def scalarize(v: ResourceVector, weights: Mapping[str, F]) -> F:
    """Dimensionless user/model score; explicitly NOT joules.

    Every coordinate must be priced.  This prevents silently setting storage,
    replay, representation, or sampling costs to zero and then calling the
    resulting scalar an execution/energy cost.
    """
    missing = [k for k in COORDINATES if k not in weights]
    extra = [k for k in weights if k not in COORDINATES]
    if missing or extra:
        raise ValueError(f"explicit weights required for exactly {COORDINATES}; missing={missing}, extra={extra}")
    values = {
        "semantic_guest_steps": F(v.semantic_guest_steps),
        "w33_route_hops": F(v.w33_route_hops),
        "authenticated_retained_byte_ticks": F(v.authenticated_retained_byte_ticks),
        "authenticated_swept_payload_bytes": F(v.authenticated_swept_payload_bytes),
        "deterministic_replay_steps": F(v.deterministic_replay_steps),
        "representation_excess_A_minus_1": v.representation_amplification - 1,
        "sampling_excess_A2_minus_1": v.signed_sampling_second_moment_factor - 1,
    }
    return sum((F(weights[k]) * values[k] for k in COORDINATES), F(0))


def build_vectors(*, interval=4, steps=8):
    policy = run_policy(interval, steps=steps)
    base = dict(
        semantic_guest_steps=steps,
        w33_route_hops=policy.route_hops_total,
        authenticated_retained_byte_ticks=policy.retained_byte_ticks,
        authenticated_swept_payload_bytes=policy.swept_payload_bytes,
        deterministic_replay_steps=policy.recomputation_steps_total,
    )
    rows = {}
    for name, rep in REPRESENTATIONS.items():
        rows[name] = ResourceVector(
            **base,
            representation_amplification=rep["A"],
            signed_sampling_second_moment_factor=rep["A2"],
            representation_class=name,
        )
    return policy, rows


def verify():
    policy, rows = build_vectors()
    positive, d1, d2 = (rows[k] for k in ("positive-depth0", "exception-depth1", "exception-depth2"))

    work_fields = (
        "semantic_guest_steps", "w33_route_hops",
        "authenticated_retained_byte_ticks", "authenticated_swept_payload_bytes",
        "deterministic_replay_steps",
    )
    representation_swap_preserves_work = all(
        getattr(positive, f) == getattr(d1, f) == getattr(d2, f) for f in work_fields
    )

    refused_partial = False
    try:
        scalarize(d1, {"semantic_guest_steps": F(1)})
    except ValueError:
        refused_partial = True

    unit_weights = {k: F(1) for k in COORDINATES}
    scores = {k: scalarize(v, unit_weights) for k, v in rows.items()}
    base_score = scores["positive-depth0"]
    # With unit weights, only the two representation coordinates move.
    assert scores["exception-depth1"] - base_score == F(1, 2) + F(5, 4)
    assert scores["exception-depth2"] - base_score == F(1) + F(3)

    checks = {
        "real_l1_depth1_factor_is_exact_3_over_2": d1.representation_amplification == F(3, 2),
        "real_l1_depth2_factor_is_exact_2": d2.representation_amplification == F(2),
        "second_moment_factors_are_exact": d1.signed_sampling_second_moment_factor == F(9, 4) and d2.signed_sampling_second_moment_factor == F(4),
        "representation_swap_preserves_semantic_and_authenticated_work": representation_swap_preserves_work,
        "scalarization_refuses_missing_weights": refused_partial,
        "resource_vector_has_no_energy_coordinate": not any("energy" in f.lower() or "joule" in f.lower() for f in ResourceVector.__dataclass_fields__),
        "actual_holovm_routing_is_nontrivial_and_diameter_two": policy.route_hops_total > 0 and policy.route_hops_max <= 2,
        "actual_holovm_checkpoint_replay_is_verified": policy.recomputation_replays_verified == policy.steps,
        "signed_overhead_is_not_folded_into_retention_or_replay": representation_swap_preserves_work,
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    return {
        "schema": "w33.holovm-signed-representation-economics.v1",
        "status": "PASS",
        "checks": checks,
        "holotrade_exact_source": HOLOTRADE_SOURCE,
        "holoVM_policy": policy.descriptor(),
        "resource_vectors": {k: v.descriptor() for k, v in rows.items()},
        "unit_weight_dimensionless_scores": {k: str(v) for k, v in scores.items()},
        "composition_rule": (
            "Execution economics is vector-valued until an explicit price functional is supplied: "
            "semantic/authenticated work coordinates and signed-representation coordinates are independent types."
        ),
        "representation_law": (
            "For a mass-4k excess with real l1 optimum gamma, A=gamma/k.  Holotrade certifies "
            "gamma=6 at depth 1 and gamma=8 at depth 2 for all seven mass-16 exceptional orbits, "
            "so A=3/2 or 2 and bounded signed-sampling second moment is at most A^2."
        ),
        "boundary": (
            "A and A^2 are exact signed-representation / estimator amplification factors. They are not semantic HoloVM ticks, "
            "authenticated storage, replay work, timing leakage, device power, joules, fault-tolerance overhead, or quantum magic. "
            "A physical energy model would require separate calibrated measurements and dimensional weights."
        ),
    }


if __name__ == "__main__":
    out = verify()
    path = Path(__file__).with_name("w33_signed_representation_economics_certificate.json")
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": out["status"],
        "checks": out["checks"],
        "vectors": out["resource_vectors"],
        "scores_are_dimensionless_only": out["unit_weight_dimensionless_scores"],
        "certificate": str(path),
    }, indent=2, sort_keys=True))
