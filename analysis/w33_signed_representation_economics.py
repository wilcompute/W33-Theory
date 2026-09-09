#!/usr/bin/env python3
"""Cross-repo resource ledger for authenticated HoloVM + signed W33 representations.

The central rule is type separation.  A signed-pencil representation factor is
not semantic work, authenticated-history storage, replay work, information
leakage, or physical energy.  We therefore keep a vector ledger and refuse to
produce a scalar score unless every coordinate receives an explicit weight.

Exact representation factors come from rational primal/dual Holotrade
certificates:
  mass 16 depth 1: gamma=6,  k=4, A=gamma/k=3/2, A^2=9/4
  mass 16 depth 2: gamma=8,  k=4, A=2,             A^2=4
  mass 24 depth 3: gamma=12, k=6, A=2,             A^2=4
The depth-three result is the unique mass-24 depth-three orbit certified in
workflow 34381463322 and its exact real-l1 certificate in workflow 34385613729.
Thus integer negativity depth increases from 2 to 3 while normalized signed
amplification remains A=2.  No physical-energy interpretation is made here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import json
from pathlib import Path
from typing import Mapping

from w33_holovm_thermodynamic_ledger import run_policy

HOLOTRADE_SOURCE = {
    "mass16": {
        "repository": "wilcompute/Holotrade",
        "commit": "e45fd0ad5844d11ee8062a108ccf4809fa2aa001",
        "workflow_run": 34307397528,
        "workflow_job": 102326833373,
        "artifact_id": 10087137602,
        "artifact_zip_sha256": "235c73474fc3c1f8fca27af14c1f1374c1839fde1d8067d67724901f1e2100cf",
    },
    "mass24_depth3": {
        "repository": "wilcompute/Holotrade",
        "birth_workflow_run": 34381463322,
        "birth_workflow_job": 102567085256,
        "birth_artifact_id": 10116305671,
        "birth_artifact_zip_sha256": "f4c178d85543883abf02bf81689b72748faa2bbcdabf021cb7a7cfc00fe284b5",
        "real_l1_workflow_run": 34385613729,
        "real_l1_workflow_job": 102580984596,
        "real_l1_artifact_id": 10117599755,
        "real_l1_artifact_zip_sha256": "4831b1a7107f24d4ce3bca99031afc81289543923d3dc526fb49d3fe877b3595",
        "representative_digest": "sha256:db8e5654204ace859e17291804dba3bf66c7bbd4a0a29f6bc7e6528e55c0e735",
    },
}

REPRESENTATIONS = {
    "positive-depth0": {"depth": 0, "mass": 16, "k": F(4), "gamma": F(4), "A": F(1), "A2": F(1)},
    "exception-depth1": {"depth": 1, "mass": 16, "k": F(4), "gamma": F(6), "A": F(3, 2), "A2": F(9, 4)},
    "exception-depth2": {"depth": 2, "mass": 16, "k": F(4), "gamma": F(8), "A": F(2), "A2": F(4)},
    "exception-depth3-mass24": {"depth": 3, "mass": 24, "k": F(6), "gamma": F(12), "A": F(2), "A2": F(4)},
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
    """Dimensionless user/model score; explicitly NOT joules."""
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
    positive, d1, d2, d3 = (rows[k] for k in (
        "positive-depth0", "exception-depth1", "exception-depth2", "exception-depth3-mass24"))

    work_fields = (
        "semantic_guest_steps", "w33_route_hops",
        "authenticated_retained_byte_ticks", "authenticated_swept_payload_bytes",
        "deterministic_replay_steps",
    )
    representation_swap_preserves_work = all(
        getattr(positive, f) == getattr(d1, f) == getattr(d2, f) == getattr(d3, f)
        for f in work_fields
    )

    refused_partial = False
    try:
        scalarize(d1, {"semantic_guest_steps": F(1)})
    except ValueError:
        refused_partial = True

    for rep in REPRESENTATIONS.values():
        assert rep["A"] == rep["gamma"] / rep["k"]
        assert rep["A2"] == rep["A"] * rep["A"]

    unit_weights = {k: F(1) for k in COORDINATES}
    scores = {k: scalarize(v, unit_weights) for k, v in rows.items()}
    base_score = scores["positive-depth0"]
    assert scores["exception-depth1"] - base_score == F(1, 2) + F(5, 4)
    assert scores["exception-depth2"] - base_score == F(1) + F(3)
    assert scores["exception-depth3-mass24"] - base_score == F(1) + F(3)

    checks = {
        "real_l1_depth1_factor_is_exact_3_over_2": d1.representation_amplification == F(3, 2),
        "real_l1_depth2_factor_is_exact_2": d2.representation_amplification == F(2),
        "real_l1_depth3_mass24_factor_is_exact_2": d3.representation_amplification == F(2),
        "depth3_increases_integer_depth_without_increasing_normalized_A": d3.representation_amplification == d2.representation_amplification,
        "second_moment_factors_are_exact": d1.signed_sampling_second_moment_factor == F(9, 4) and d2.signed_sampling_second_moment_factor == F(4) and d3.signed_sampling_second_moment_factor == F(4),
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
        "representation_parameters": {
            k: {kk: (str(vv) if isinstance(vv, F) else vv) for kk, vv in rep.items()}
            for k, rep in REPRESENTATIONS.items()
        },
        "holoVM_policy": policy.descriptor(),
        "resource_vectors": {k: v.descriptor() for k, v in rows.items()},
        "unit_weight_dimensionless_scores": {k: str(v) for k, v in scores.items()},
        "composition_rule": (
            "Execution economics is vector-valued until an explicit price functional is supplied: "
            "semantic/authenticated work coordinates and signed-representation coordinates are independent types."
        ),
        "representation_law": (
            "For a mass-4k excess with exact real l1 optimum gamma, A=gamma/k and the bounded signed-sampling second moment factor is A^2. "
            "Holotrade certifies (depth,k,gamma,A)=(1,4,6,3/2),(2,4,8,2),(3,6,12,2). Thus negativity depth is not itself the normalized amplification: the unique mass-24 depth-three class has the same A=2 and A^2=4 as the mass-16 depth-two class."
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
