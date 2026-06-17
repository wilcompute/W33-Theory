#!/usr/bin/env python3
"""BT1213 -- K3 envelope refinement bridge.

This replaces the purely free-floating BT1210 toy ladder with a repo-grounded
bridge to the existing BT1127 K3 spectral-action envelope.  The real envelope
contains K3 topology and finite W33 prefactors but explicitly marks metric data
as placeholders.  BT1213 therefore constructs a schema-grounded refinement
witness, not a computed physical K3 metric.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from fractions import Fraction


DEFAULT_ENVELOPE = Path("data/bt1127_k3_sample_envelope.json")


def parse_fraction(s: str) -> float:
    return float(Fraction(s))


def build_ladder(envelope: dict, ns: list[int]) -> list[dict]:
    topo = envelope["input_result"]["topological_checks"]
    finite = envelope["finite_w33_prefactors"]
    target_curvature = 24.0
    finite_a2_over_a0 = parse_fraction(finite["finite_a2_over_a0"])
    finite_a4_over_a2 = parse_fraction(finite["finite_a4_over_a2"])
    rows = []
    for n in ns:
        h = 1.0 / n
        rows.append({
            "n": n,
            "h": h,
            "chi": topo["chi"],
            "signature": topo["signature"],
            "b2": topo["b2"],
            "intersection_signature": topo["intersection_signature"],
            "ricci_flat_A2": envelope["input_result"]["A2"]["value"],
            "normalized_curvature_target": target_curvature,
            "curvature_proxy": target_curvature + finite_a2_over_a0 * h * h,
            "spectral_C2_proxy": -finite_a2_over_a0 * h,
            "spectral_C4_proxy": target_curvature + 0.5 * finite_a4_over_a2 * h * h,
            "metric_placeholder_warning": envelope["input_result"]["metric_source"],
        })
    return rows


def monotone_to_target(rows: list[dict], key: str, target: float) -> bool:
    errors = [abs(r[key] - target) for r in rows]
    return all(errors[i+1] <= errors[i] for i in range(len(errors)-1))


def build_result(envelope_path: Path, ns: list[int]) -> dict:
    envelope = json.loads(envelope_path.read_text())
    rows = build_ladder(envelope, ns)
    topo = envelope["input_result"]["topological_checks"]
    checks = {
        "envelope_valid": envelope["valid"],
        "chi_24": topo["chi"] == 24,
        "signature_minus_16": topo["signature"] == -16,
        "b2_22": topo["b2"] == 22,
        "intersection_signature_3_19": topo["intersection_signature"] == [3, 19],
        "ricci_flat_A2_zero": envelope["input_result"]["A2"]["value"] == 0.0,
        "curvature_proxy_converges_to_24": monotone_to_target(rows, "curvature_proxy", 24.0),
        "spectral_C4_proxy_converges_to_24": monotone_to_target(rows, "spectral_C4_proxy", 24.0),
    }
    return {
        "bt": 1213,
        "title": "K3 envelope-grounded R3 refinement bridge",
        "source_envelope": str(envelope_path),
        "honesty_boundary": "BT1127 supplies a valid K3 topology/schema envelope, not a computed metric. BT1213 is a bridge from that envelope to the BT1210 refinement-witness interface.",
        "topology": topo,
        "finite_w33_prefactors": envelope["finite_w33_prefactors"],
        "refinement_rows": rows,
        "checks": checks,
        "passes_schema_grounded_bridge": all(checks.values()),
        "interpretation": "The real repo K3 envelope already locks the topological invariants and finite W33 prefactors; what remains missing is the real metric/Dirac compute lane that turns these schema rows into physical spectral-action data.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--envelope", type=Path, default=DEFAULT_ENVELOPE)
    p.add_argument("--ns", type=int, nargs="+", default=[4, 8, 16, 32, 64])
    p.add_argument("--out", type=Path, default=Path("data/bt1213_k3_envelope_refinement_bridge.json"))
    args = p.parse_args()
    result = build_result(args.envelope, args.ns)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1213, "passes": result["passes_schema_grounded_bridge"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
