#!/usr/bin/env python3
"""Pass 239: where the [[(q+1)(q^2+1), q^2+1, q+1]] family sits among the
quantum coding bounds.

Passes 224/229/238 pin the family parameters exactly:
    n = (q+1)(q^2+1),  k = q^2+1,  d = q+1,
    rate      R = k/n = 1/(q+1),
    rel. dist delta = d/n = 1/(q^2+1),
    stabiliser (check) weight w = 2(q+1)  [Pass 226 conjecture, exact 8 at q=3].

This witness computes the family's asymptotics and locates it against the
standard quantum bounds -- an honest accounting of what the substrate's codes
are and are not.

Key exact facts, verified for q = 3,5,7,11,13:
  * k * d = (q^2+1)(q+1) = n  EXACTLY -- the family lies on the conservation
    curve k*d = n;
  * scaling n ~ q^3, so k ~ n^{2/3} and d ~ n^{1/3}: many logicals, modest
    distance (cf. surface code k=1, d~n^{1/2});
  * Quantum Singleton k <= n - 2(d-1) holds with slack (not MDS);
  * the Bravyi-Poulin-Terhal locality bound k d^{2/(D-1)} <= O(n) forces the
    minimum embedding dimension D >= 3 (not 2D-local);
  * rate -> 0 and rel. distance -> 0, so the family is NOT asymptotically good
    -- its value is the transversal Clifford + cubic-magic gate structure
    (Passes 204/230/234), not the raw parameters.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass239_qldpc_bounds.json"


def params(q):
    n = (q + 1) * (q * q + 1)
    k = q * q + 1
    d = q + 1
    w = 2 * (q + 1)
    return n, k, d, w


def min_embedding_dim(n, k, d):
    """smallest integer D with k * d^{2/(D-1)} <= n (BPT-type locality)."""
    D = 2
    while D < 12:
        if k * d ** (2.0 / (D - 1)) <= n + 1e-9:
            return D
        D += 1
    return D


def main():
    checks = {}
    table = {}
    for q in (3, 5, 7, 11, 13):
        n, k, d, w = params(q)
        # k*d = n exactly
        kd_eq_n = (k * d == n)
        # quantum Singleton: k <= n - 2(d-1)
        singleton_rhs = n - 2 * (d - 1)
        singleton_ok = k <= singleton_rhs
        Dmin = min_embedding_dim(n, k, d)
        table[str(q)] = {
            "n": n, "k": k, "d": d, "check_weight": w,
            "rate": f"1/{q+1}", "rate_val": k / n,
            "rel_distance": f"1/{q*q+1}", "rel_distance_val": d / n,
            "k_times_d": k * d, "k_times_d_eq_n": bool(kd_eq_n),
            "singleton_bound_rhs": singleton_rhs,
            "singleton_slack": singleton_rhs - k,
            "singleton_ok": bool(singleton_ok),
            "min_embedding_dim_BPT": Dmin,
        }
        checks[f"q{q}_kd_eq_n"] = bool(kd_eq_n)
        checks[f"q{q}_singleton_ok"] = bool(singleton_ok)
        checks[f"q{q}_needs_dim_ge_3"] = Dmin >= 3

    # asymptotic scaling exponents (n ~ q^3): k ~ n^{2/3}, d ~ n^{1/3}
    # check via large q least-squares on log-log
    qs = [11, 13, 17, 19, 23, 29]
    import statistics
    logn = [math.log((q + 1) * (q * q + 1)) for q in qs]
    logk = [math.log(q * q + 1) for q in qs]
    logd = [math.log(q + 1) for q in qs]

    def slope(xs, ys):
        mx, my = statistics.mean(xs), statistics.mean(ys)
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        den = sum((x - mx) ** 2 for x in xs)
        return num / den

    k_exp = slope(logn, logk)
    d_exp = slope(logn, logd)
    checks["k_scales_n_two_thirds"] = abs(k_exp - 2 / 3) < 0.02
    checks["d_scales_n_one_third"] = abs(d_exp - 1 / 3) < 0.02

    # comparison: surface code [[n,1,~sqrt n]] vs this family
    comparison = {
        "surface_code": {"k": "1", "d_scaling": "n^{1/2}", "rate": "1/n -> 0"},
        "good_qLDPC": {"k": "Theta(n)", "d_scaling": "Theta(n)", "rate": "const"},
        "this_family": {"k": "n^{2/3}", "d_scaling": "n^{1/3}", "rate": "1/(q+1) -> 0",
                        "note": "k*d = n exactly; transversal Clifford + cubic magic"},
    }

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass239.qldpc_bounds.v1",
        "status": "PASS" if all_pass else "FAIL",
        "theorem": (
            "The family [[(q+1)(q^2+1), q^2+1, q+1]] satisfies k*d = n exactly "
            "(it lies on the conservation curve), with k ~ n^{2/3} logical "
            "qubits and d ~ n^{1/3} distance. It obeys the quantum Singleton "
            "bound with slack, requires embedding dimension D >= 3 (not "
            "2D-local by BPT), and is NOT asymptotically good (rate and rel. "
            "distance both -> 0). Its worth is the gate structure -- "
            "transversal Clifford (Pass 204) plus the cubic-magic Yukawa "
            "(Pass 230) -- not the raw parameters."
        ),
        "per_q": table,
        "asymptotics": {"k_exponent": round(k_exp, 4), "d_exponent": round(d_exp, 4),
                        "reading": "k ~ n^{2/3}, d ~ n^{1/3}, k*d = n"},
        "comparison": comparison,
        "reading": (
            "This is a high-rate-of-logicals (k ~ n^{2/3}) but modest-distance "
            "(d ~ n^{1/3}) code family sitting exactly on k*d = n -- between the "
            "surface code (k=1) and good qLDPC (k,d linear). It is a "
            "transversal-gate code, not a parameter-optimal one: the substrate "
            "trades asymptotic goodness for a native fault-tolerant gate set "
            "whose logical group is the Standard-Model SO(10)."
        ),
        "checks": {k2: bool(v) for k2, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
