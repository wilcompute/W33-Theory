#!/usr/bin/env python3
"""Pass 492: Hjelmslev projective-line bridge for the Z/p^n depth law.

The measured non-generating-character depths from Pass 491 are
    Z/9 -> 12, Z/25 -> 30, Z/27 -> 36.
Pass 491 observed that they fit p^(n-1)(p+1).  This pass proves the
geometric identity
    p^(n-1)(p+1) = p * |P^1(Z/p^(n-1))|,
where |P^1(Z/p^m)| = p^m + p^(m-1) for m >= 1.

This does NOT prove that every determinant depth equals that number.  It
identifies the conjectured law with a canonical Hjelmslev boundary count and
preregisters new falsifiers before expensive determinant calculations.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass492_hjelmslev_depth_bridge.json"


@dataclass(frozen=True)
class Observation:
    p: int
    n: int
    depth: int

    @property
    def q(self) -> int:
        return self.p ** self.n


def p1_local_count(p: int, m: int) -> int:
    """Number of free rank-one direct summands of (Z/p^m)^2.

    Primitive vectors: p^(2m)-p^(2m-2).
    Units act freely, with |(Z/p^m)^x|=p^m-p^(m-1).
    Quotient: p^m+p^(m-1).
    """
    if p < 2 or m < 1:
        raise ValueError("require p >= 2 and m >= 1")
    primitive = p ** (2 * m) - p ** (2 * m - 2)
    units = p**m - p ** (m - 1)
    assert primitive % units == 0
    quotient = primitive // units
    closed = p**m + p ** (m - 1)
    assert quotient == closed
    return quotient


def candidate_depth(p: int, n: int) -> int:
    if n < 2:
        raise ValueError("the non-generating-character tower starts at n >= 2")
    return p * p1_local_count(p, n - 1)


def build_payload() -> dict:
    observed = [Observation(3, 2, 12), Observation(5, 2, 30), Observation(3, 3, 36)]
    checks: dict[str, bool] = {}
    rows = []
    for o in observed:
        p1 = p1_local_count(o.p, o.n - 1)
        cand = candidate_depth(o.p, o.n)
        direct = o.q + o.q // o.p
        ramification = o.n * o.p ** (o.n - 1) * (o.p - 1)
        row = {
            "ring": f"Z/{o.q}",
            "p": o.p,
            "n": o.n,
            "observed_depth": o.depth,
            "P1_Zmod_p_to_n_minus_1": p1,
            "p_times_P1": cand,
            "q_plus_q_over_p": direct,
            "v_lambda_q": ramification,
        }
        rows.append(row)
        checks[f"{row['ring']}_hjelmslev_identity"] = cand == direct == o.p ** (o.n - 1) * (o.p + 1)
        checks[f"{row['ring']}_observation_matches"] = o.depth == cand

    odd_prime_grid = [(p, n) for p in (3, 5, 7, 11, 13) for n in range(2, 7)]
    checks["candidate_even_for_all_tested_odd_primes"] = all(candidate_depth(p, n) % 2 == 0 for p, n in odd_prime_grid)

    predictions = []
    for p, n in ((7, 2), (5, 3), (3, 4), (11, 2)):
        q = p**n
        predictions.append({
            "ring": f"Z/{q}",
            "p": p,
            "n": n,
            "predicted_min_depth": candidate_depth(p, n),
            "Hjelmslev_P1_count": p1_local_count(p, n - 1),
            "status": "PREREGISTERED_UNMEASURED",
        })

    checks["vertical_tower_scales_by_p"] = all(
        candidate_depth(p, n + 1) == p * candidate_depth(p, n)
        for p in (3, 5, 7, 11) for n in range(2, 6)
    )
    checks["bottom_rung_is_p_times_projective_line"] = all(
        candidate_depth(p, 2) == p * (p + 1) for p in (3, 5, 7, 11, 13)
    )

    return {
        "schema": "w33.pass492.hjelmslev_depth_bridge.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "For every prime p and n>=2, p^(n-1)(p+1) equals "
            "p*|P^1(Z/p^(n-1))|.  The projective-line count follows by "
            "dividing the primitive-vector count p^(2m)-p^(2m-2) by the "
            "free unit action p^m-p^(m-1), giving p^m+p^(m-1)."
        ),
        "interpretation": (
            "The Pass-491 candidate failure depth is a Hjelmslev boundary "
            "cardinality one ring level below the coefficient ring, multiplied "
            "by the residue characteristic.  Thus the candidate is geometric, "
            "not an arbitrary interpolation."
        ),
        "observed_fit": rows,
        "preregistered_falsifiers": predictions,
        "boundary": (
            "The projective-line identity is proved.  Equality between this "
            "count and determinant depth remains a conjecture supported by "
            "three measured rings.  Any preregistered ring whose minimum depth "
            "differs from the listed value falsifies the conjecture."
        ),
        "checks": checks,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    args = ap.parse_args()
    payload = build_payload()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 492 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
