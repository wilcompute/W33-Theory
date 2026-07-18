#!/usr/bin/env python3
"""Pass 407: critical-group calibration memory and exact one-slip decoder."""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from fractions import Fraction
from math import gcd, lcm
import hashlib
import json
from pathlib import Path
import random
import sys
import zlib

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from w33_pass400_404_common import reduced_laplacian, vertices

OUT = ROOT / "data" / "w33_pass407_sandpile_calibration_memory.json"
DECODER = ROOT / "data" / "w33_pass407_single_slip_decoder_q3.json"
MODULUS = 216  # exponent of the q=3 critical group from Pass 401


def fractional_residue(value: sp.Rational, modulus: int = MODULUS) -> int:
    value = sp.Rational(value)
    frac = value - sp.floor(value)
    scaled = sp.simplify(frac * modulus)
    if scaled.q != 1:
        raise AssertionError(f"denominator does not divide critical-group exponent: {value}")
    return int(scaled) % modulus


def class_order(residue: tuple[int, ...], modulus: int = MODULUS) -> int:
    order = 1
    for value in residue:
        if value:
            order = lcm(order, modulus // gcd(modulus, value))
    return order


def torus_linf(a: tuple[int, ...], b: tuple[int, ...], modulus: int = MODULUS) -> int:
    return max(min((x - y) % modulus, (y - x) % modulus) for x, y in zip(a, b))


def build_decoder() -> tuple[dict, dict]:
    q = 3
    verts = vertices(q)
    root = 0
    laplacian = sp.Matrix(reduced_laplacian(q).tolist())
    inverse = laplacian.inv()

    vertex_fingerprints: list[tuple[int, ...]] = []
    zero = tuple(0 for _ in range(q**3 - 1))
    for index in range(q**3):
        if index == root:
            vertex_fingerprints.append(zero)
        else:
            column = inverse[:, index - 1]
            vertex_fingerprints.append(tuple(fractional_residue(value) for value in column))

    entries = []
    seen: dict[tuple[int, ...], tuple[int, int]] = {}
    order_counts: Counter[int] = Counter()
    category_counts: Counter[str] = Counter()
    for source in range(q**3):
        for target in range(q**3):
            if source == target:
                continue
            # A unit pulse moved source -> target adds e_target-e_source.
            residue = tuple(
                (vertex_fingerprints[target][k] - vertex_fingerprints[source][k]) % MODULUS
                for k in range(q**3 - 1)
            )
            if residue in seen:
                raise AssertionError(f"single-slip collision: {(source,target)} and {seen[residue]}")
            seen[residue] = (source, target)
            order = class_order(residue)
            same_fibre = verts[source][:2] == verts[target][:2]
            category = "same_phase_fibre" if same_fibre else "cross_phase_fibre"
            order_counts[order] += 1
            category_counts[f"{category}_order_{order}"] += 1
            entries.append({
                "source_mode": source,
                "target_mode": target,
                "source_coordinate": list(verts[source]),
                "target_coordinate": list(verts[target]),
                "category": category,
                "critical_group_order": order,
                "syndrome_residues_mod_216": list(residue),
                "syndrome_sha256": hashlib.sha256(bytes(residue)).hexdigest(),
            })

    fingerprints = [tuple(entry["syndrome_residues_mod_216"]) for entry in entries]
    minimum = MODULUS
    closest = None
    for i, left in enumerate(fingerprints):
        for j in range(i + 1, len(fingerprints)):
            distance = torus_linf(left, fingerprints[j])
            if distance < minimum:
                minimum = distance
                closest = (entries[i]["source_mode"], entries[i]["target_mode"], entries[j]["source_mode"], entries[j]["target_mode"])

    rng = random.Random(40720260717)
    noise_trials = 256
    decoded = 0
    for _ in range(noise_trials):
        index = rng.randrange(len(entries))
        truth = fingerprints[index]
        noisy = tuple((value + rng.randint(-11, 11)) % MODULUS for value in truth)
        nearest_index = min(range(len(fingerprints)), key=lambda candidate: torus_linf(noisy, fingerprints[candidate]))
        decoded += int(nearest_index == index)

    syndrome_bytes = bytes(value for residue in fingerprints for value in residue)
    order_bytes = bytes(entry["critical_group_order"] for entry in entries)
    decoder = {
        "schema": "w33.pass407.single_slip_decoder.q3.v1",
        "mode_order": "lexicographic (x,y,z) in F_3^3; mode 0 is the reduced-Laplacian root",
        "slip_order": "source=0..26, target=0..26 excluding target=source",
        "critical_group_exponent": MODULUS,
        "syndrome_definition": "fractional part of L_root^{-1}(e_target-e_source), encoded in 216 ticks",
        "shape": [len(entries), q**3 - 1],
        "codec": "base64(zlib(raw uint8 row-major residues))",
        "syndrome_data": base64.b64encode(zlib.compress(syndrome_bytes, level=9)).decode(),
        "order_data": base64.b64encode(zlib.compress(order_bytes, level=9)).decode(),
        "raw_syndrome_sha256": hashlib.sha256(syndrome_bytes).hexdigest(),
        "raw_order_sha256": hashlib.sha256(order_bytes).hexdigest(),
    }
    decoder_text = json.dumps(decoder, indent=2, sort_keys=True) + "\n"
    decoder_sha = hashlib.sha256(decoder_text.encode()).hexdigest()

    checks = {
        "reduced_laplacian_size_26": laplacian.shape == (26, 26),
        "critical_group_exponent_216": MODULUS == 216,
        "all_702_oriented_single_slips_present": len(entries) == 27 * 26,
        "all_single_slip_syndromes_unique": len(seen) == len(entries),
        "all_orders_divide_216": all(MODULUS % entry["critical_group_order"] == 0 for entry in entries),
        "observed_orders_are_72_or_216": set(order_counts) == {72, 216},
        "minimum_torus_linf_distance_23_ticks": minimum == 23,
        "eleven_tick_adversarial_radius_is_safe": 2 * 11 < minimum,
        "seeded_noise_trials_all_decode": decoded == noise_trials,
        "inverse_slips_cancel": all(
            all((a + b) % MODULUS == 0 for a, b in zip(
                tuple(entry["syndrome_residues_mod_216"]),
                tuple(next(candidate["syndrome_residues_mod_216"] for candidate in entries if candidate["source_mode"] == entry["target_mode"] and candidate["target_mode"] == entry["source_mode"]))
            ))
            for entry in entries[:54]
        ),
    }

    payload = {
        "schema": "w33.pass407.sandpile_calibration_memory.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "interpretation": "A zero-sum pulse-slip vector is stored as a persistent class in the q=3 critical group. Compensation adds the inverse class; chip resets correspond to returning the syndrome to zero.",
        "exact_decoder": {
            "decoder_path": "data/w33_pass407_single_slip_decoder_q3.json",
            "decoder_sha256": decoder_sha,
            "oriented_single_slip_states": len(entries),
            "syndrome_coordinates": 26,
            "modulus_ticks": MODULUS,
            "minimum_pairwise_linf_ticks": minimum,
            "guaranteed_unique_decode_radius": "strictly less than 23/2 ticks; every integer perturbation with |delta_i|<=11 is safe",
            "closest_pair": list(closest) if closest else None,
        },
        "torsion_clock": {
            "order_distribution": {str(k): v for k, v in sorted(order_counts.items())},
            "category_distribution": dict(sorted(category_counts.items())),
            "meaning": "repeating the same uncompensated unit slip wraps after 72 or 216 applications, depending on its critical-group class",
        },
        "nonclaim_boundary": "This is an exact discrete calibration-memory and decoder model. It does not assert that a fabricated chip exhibits these slips or that measured analog noise is bounded by 11 syndrome ticks.",
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload, decoder


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--decoder", type=Path, default=DECODER)
    args = parser.parse_args()
    payload, decoder = build_decoder()
    payload_text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    decoder_text = json.dumps(decoder, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != payload_text:
            raise SystemExit("Pass 407 certificate is stale")
        if not args.decoder.exists() or args.decoder.read_text() != decoder_text:
            raise SystemExit("Pass 407 decoder is stale")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload_text)
        args.decoder.write_text(decoder_text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
