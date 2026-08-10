#!/usr/bin/env python3
"""Read-only verifier or full regenerator for the RH motive/global release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATES = (
    "w33_motivic_24_15_packet_certificate.json",
    "w33_all_prime_frobenius_census_certificate.json",
    "w33_renormalized_boundary_formula_certificate.json",
    "w33_fixed_E_debranges_falsifier_certificate.json",
    "w33_preregistered_higher_moment_search_certificate.json",
)


def builders():
    from analysis.w33_all_prime_frobenius_census import build_census, build_certificate, csv_text
    from analysis.w33_fixed_E_debranges_falsifier import build_certificate as build_fixed_E
    from analysis.w33_motivic_24_15_packet import build_certificate as build_motive
    from analysis.w33_preregistered_higher_moment_search import build_certificate as build_operator
    from analysis.w33_renormalized_boundary_formula import build_certificate as build_boundary

    def build_census_bundle():
        rows, _ = build_census()
        (ROOT / "data" / "w33_elliptic_frobenius_census_p10000.csv").write_text(csv_text(rows, encoding="utf-8"), encoding="utf-8"
        )
        return build_certificate()

    return {
        CERTIFICATES[0]: build_motive,
        CERTIFICATES[1]: build_census_bundle,
        CERTIFICATES[2]: build_boundary,
        CERTIFICATES[3]: build_fixed_E,
        CERTIFICATES[4]: build_operator,
    }


def verify_certificate(name: str, payload: dict) -> dict:
    checks = payload.get("checks", {})
    if payload.get("status") != "PASS" or not checks or not all(checks.values()):
        raise SystemExit(f"{name}: failed certificate")
    return {"status": "PASS", "check_count": len(checks)}


def verify_census_replay() -> dict:
    from analysis.w33_all_prime_frobenius_census import build_census

    rows, summary = build_census()
    signatures = summary["W33_signature"]["matching_primes"]
    if len(rows) != 1229 or signatures != [11]:
        raise SystemExit("Frobenius census replay failed row-count or signature lock")
    p5 = next(row for row in rows if row["p"] == 5)
    if (int(p5["E_2_a_p"]), int(p5["E_-4_a_p"])) != (-3, 2):
        raise SystemExit("Frobenius census replay failed p=5 witness")
    return {"status": "PASS", "row_count": len(rows), "signature_primes": signatures}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    data_dir = ROOT / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    build_map = builders() if args.regenerate else {}
    summary = {}

    for name in CERTIFICATES:
        path = data_dir / name
        if args.regenerate:
            payload = build_map[name]()
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
        summary[name] = verify_certificate(name, payload)
        print(f"[PASS] {name}: {summary[name]['check_count']} checks")

    summary["frobenius_census_replay"] = verify_census_replay()
    output = data_dir / "w33_rh_motive_global_release_summary.json"
    output.write_text(json.dumps({"status": "PASS", "artifacts": summary}, indent=2), encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
