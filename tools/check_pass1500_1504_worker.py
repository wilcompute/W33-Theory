#!/usr/bin/env python3
"""Fail-closed worker-to-certificate verifier for Passes 1500--1504."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("worker", choices=["1500", "1501", "1502", "1503", "1504"])
    parser.add_argument("worker_json", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    worker = json.loads(args.worker_json.read_text())
    cert = json.loads(args.certificate.read_text())
    assert worker["sha256"] == cert["worker_sha256"][args.worker]
    assert worker["theorem"].startswith(f"Pass {args.worker} ")
    if args.worker == "1500":
        assert worker["primes"]["2"]["radical_power_dimensions"] == [45, 16, 0]
        assert worker["primes"]["3"]["radical_power_dimensions"] == [72, 49, 27, 14, 4, 0]
    elif args.worker == "1501":
        assert worker["exact_inverse_verified"] is True
        assert worker["all_83_orbital_multiplicity_actions_sha256"] == cert["pass1501_tensor_fourier"]["all_83_actions_sha256"]
    elif args.worker == "1502":
        assert worker["bridge_rank_distribution"] == {"70": 16, "76": 4, "81": 76}
        assert worker["rank81_bridge_count"] == 76
    elif args.worker == "1503":
        assert worker["orbital_order_contained_in_maximal_overorder"] is True
        assert worker["global_index_factorization"] == {"2": 36, "3": 113}
        assert worker["maximal_order_reduced_trace_discriminant"] == "1"
    else:
        assert worker["strict_morita_context"] is True
        assert worker["linking_envelope_dimension"] == 40401
        assert worker["unique_linear_relation_among_76_bridges"]["sha256"] == cert["pass1504_linking_algebra"]["relation_sha256"]
    print(f"PASS worker {args.worker} matches compact certificate")


if __name__ == "__main__":
    main()
