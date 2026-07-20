#!/usr/bin/env python3
"""Pass 500: Galois phase-cycle overlay for the BT1653 time-bin compiler.

For K+=Q(zeta_9+zeta_9^-1), write t=zeta_9+zeta_9^-1 and represent a real
cyclotomic determinant gap as A+B t+C t^2.  The three real embeddings indexed by
u in {1,2,4} give a 3x3 Vandermonde system.  Reconstructing the integer
coefficient vector first, then taking the exact relative norm, recovers the
lambda-depth.  This is materially different from multiplying noisy analog
amplitudes and calling the result p-adic.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass500_galois_phase_cycle_compiler.json"
HARDWARE_OUT = ROOT / "hardware" / "w33_pass500_galois_phase_cycle_overlay.json"

_spec = importlib.util.spec_from_file_location(
    "p499", ROOT / "analysis" / "w33_pass499_product_ring_discriminator.py")
P499 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(P499)
CYC = P499.Cyc9

REAL_REPS = (1, 2, 4)
TIME_BINS = (2032, 2033, 2034)
REFERENCE_BINS = (2035, 2036, 2037)


def real_mul(x, y):
    acc = [0] * 5
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            acc[i + j] += a * b
    for k in range(4, 2, -1):
        c = acc[k]
        if c:
            acc[k] = 0
            acc[k - 2] += 3 * c
            acc[k - 3] -= c
    return tuple(acc[:3])


def real_pow(x, n):
    out = (1, 0, 0)
    base = x
    while n:
        if n & 1:
            out = real_mul(out, base)
        base = real_mul(base, base)
        n >>= 1
    return out


def real_to_cyc(v):
    A, B, D = v
    return (A + 2 * D, B - D, -B + D, 0, -D, -B)


def cyc_to_real(v):
    a0, a1, a2, a3, a4, a5 = v
    A, B, D = a0 + 2 * a4, -a5, -a4
    if a3 != 0 or a1 != B - D or a2 != -B + D:
        raise ValueError("element is not in Z[zeta_9]^+")
    return (A, B, D)


def vp(n, p):
    n = abs(int(n))
    if n == 0:
        return 10**9
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def relative_norm_from_real(v):
    z = real_to_cyc(v)
    acc = CYC.one()
    for u in REAL_REPS:
        acc = CYC.mul(acc, CYC.sigma(u, z))
    if any(acc[1:]):
        raise ArithmeticError("relative norm did not land in Z")
    return acc[0]


def embedding_matrix(dps=100):
    mp.mp.dps = dps
    rows = []
    for u in REAL_REPS:
        t = 2 * mp.cos(2 * mp.pi * u / 9)
        rows.append([mp.mpf(1), t, t * t])
    return mp.matrix(rows)


def evaluate_real(v, dps=100):
    V = embedding_matrix(dps)
    col = mp.matrix([[mp.mpf(v[0])], [mp.mpf(v[1])], [mp.mpf(v[2])]])
    out = V * col
    return [out[i] for i in range(3)]


def reconstruct_with_noise(v, depth, noise_exp=-24):
    mp.mp.dps = 100
    V = embedding_matrix(100)
    vals = evaluate_real(v, 100)
    eps = mp.mpf(10) ** noise_exp
    noise = [eps, -eps / 2, eps / 3]
    measured = mp.matrix([[vals[i] + noise[i]] for i in range(3)])
    estimate = mp.inverse(V) * measured
    recovered = tuple(int(mp.nint(estimate[i])) for i in range(3))
    rel = relative_norm_from_real(recovered)
    recovered_depth = 2 * vp(rel, 3)
    return {
        "target_depth": depth,
        "coefficients": list(v),
        "measurements": [mp.nstr(x, 40) for x in vals],
        "noise_bound": mp.nstr(eps, 8),
        "recovered_coefficients": list(recovered),
        "coefficient_recovery_exact": recovered == v,
        "relative_norm": str(rel),
        "recovered_depth": recovered_depth,
        "depth_recovered": recovered_depth == depth,
    }


def compile_row(time_bin, reference_bin, u):
    return {
        "time_bin": time_bin,
        "word11": format(time_bin, "011b"),
        "region": "GUARD",
        "fano_page": 6,
        "guard_slot": time_bin - 1600 - 6 * 64,
        "route": "galois_phase_cycle_analyzer",
        "galois_representative": u,
        "central_phase_radians": f"2*pi*{u}/9",
        "reference_time_bin": reference_bin,
        "reference_word11": format(reference_bin, "011b"),
        "measurement": "signed determinant-gap embedding",
        "trigger": f"galois_real_embedding_{u}",
    }


def main_payload():
    mu = (2, -1, 0)
    synthetic = [reconstruct_with_noise(real_pow(mu, depth // 2), depth)
                 for depth in (8, 12, 18, 24)]

    p499 = P499.main_payload()
    actual_delta = tuple(p499["witness"]["delta"])
    actual_real = cyc_to_real(actual_delta)
    actual_rel = relative_norm_from_real(actual_real)
    actual_depth = 2 * vp(actual_rel, 3)
    coeff_digits = max(len(str(abs(x))) for x in actual_real)

    rows = [compile_row(tb, rb, u)
            for tb, rb, u in zip(TIME_BINS, REFERENCE_BINS, REAL_REPS)]
    custody_payload = {
        "source": "analysis/w33_pass499_product_ring_discriminator.py",
        "witness_b": p499["witness"]["b"],
        "witness_c": p499["witness"]["c"],
        "delta": p499["witness"]["delta"],
        "rows": rows,
    }
    custody_hash = hashlib.sha256(
        json.dumps(custody_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    required_significant_digits = coeff_digits + 3
    checks = {
        "three_real_embeddings": len(REAL_REPS) == 3,
        "guard_bins_reserved": TIME_BINS == (2032, 2033, 2034),
        "reference_bins_reserved": REFERENCE_BINS == (2035, 2036, 2037),
        "all_synthetic_coefficients_recovered": all(x["coefficient_recovery_exact"] for x in synthetic),
        "all_synthetic_depths_recovered": all(x["depth_recovered"] for x in synthetic),
        "actual_depth_24": actual_depth == 24,
        "actual_relative_norm_half_valuation": vp(actual_rel, 3) == 12,
        "actual_real_basis_roundtrip": real_to_cyc(actual_real) == actual_delta,
        "custody_hash_present": len(custody_hash) == 64,
    }
    return {
        "schema": "w33.pass500.galois_phase_cycle_compiler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "source_compiler": "tools/bt1653_time_bin_hardware_compiler.py",
        "overlay": {
            "target": "2048-bin time-bin envelope",
            "phase_rows": rows,
            "coefficient_basis": "1,t,t^2 with t=zeta_9+zeta_9^-1",
            "minimal_polynomial": "t^3-3t+1",
            "reconstruction": "invert three real embeddings, round integer coefficients, compute exact relative norm",
            "custody_sha256": custody_hash,
        },
        "synthetic_noisy_recovery": synthetic,
        "actual_product_ring_witness": {
            "real_coefficients": [str(x) for x in actual_real],
            "coefficient_digits": coeff_digits,
            "relative_norm": str(actual_rel),
            "relative_norm_3_valuation": vp(actual_rel, 3),
            "recovered_lambda_depth": actual_depth,
            "minimum_significant_digits_for_direct_analog_rounding": required_significant_digits,
        },
        "hardware_verdict": (
            "The three-setting Galois cycle is an exact algebraic compiler, but the order-81 "
            f"witness requires roughly {required_significant_digits} significant digits for direct analog "
            "coefficient rounding. A practical device therefore needs digital/modular accumulation."
        ),
        "honesty_boundary": (
            "The overlay, exact reconstruction, and bounded-noise synthetic tests are certified. "
            "No claim is made that current photonic hardware can supply the required significant digits."
        ),
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    ap.add_argument("--hardware-output", type=Path, default=HARDWARE_OUT)
    args = ap.parse_args()
    payload = main_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    hardware = json.dumps(payload["overlay"], indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 500 certificate drift")
        if not args.hardware_output.exists() or args.hardware_output.read_text() != hardware:
            raise SystemExit("Pass 500 hardware overlay drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.hardware_output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        args.hardware_output.write_text(hardware)
    print(json.dumps({"status": payload["status"],
                      "checks": sum(payload["checks"].values()),
                      "total": len(payload["checks"]),
                      "actual_depth": payload["actual_product_ring_witness"]["recovered_lambda_depth"]}, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
