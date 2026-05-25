"""W(3,3) SUBSTRATE IDENTITY FINDER.

Brute-force search for the simplest substrate-rational expressions
matching PDG-measured physical constants.  Each measured value is
compared against:

  1. All rationals a/b where a, b are products of <=2 substrate
     primitives.
  2. All a + b/c where a, b, c are substrate primitives (small).
  3. Powers of q with substrate-primitive exponents.

We print only matches better than the existing best-known identity,
allowing automatic identification of NEW substrate identities.

Substrate primitives:
  {q=3, mu=4, q!=6, k=12, Phi_3=13, Phi_4=10, Phi_6=7,
   p_Ih=11, v=40, |E|=240, q^q=27, q^(q+1)=81, f=24, g_neg=15,
   T_6=21, Heegner_n (1,2,3,7,11,19,43,67,163), Ogg_n}.
"""
from __future__ import annotations

import math
from itertools import product
from pathlib import Path
import json


# Substrate primitive integers
PRIMITIVES = {
    "q":        3,
    "mu":       4,
    "q!":       6,
    "k":        12,
    "Phi_3":    13,
    "Phi_4":    10,
    "Phi_6":    7,
    "p_Ih":     11,
    "v":        40,
    "|E|":      240,
    "q^q":      27,
    "q^(q+1)":  81,
    "f":        24,
    "g_neg":    15,
    "T_6":      21,
    "(mu+1)":   5,
    "q^2":      9,
    "2^q":      8,
    "2^mu":     16,
    "mu^4":     256,
    "(q!)^2":   36,
    "Heegner_6": 19,
    "Heegner_7": 43,
    "Heegner_67": 67,
    "Ogg_7":    17,
    "Ogg_12":   41,
    "Ogg_13":   47,
    "1":        1,
    "2":        2,
}


# PDG / observed values (with type: "exact", "ratio", or "log")
TARGETS = {
    "alpha^-1":              ("ratio", 137.035999),
    "alpha^-1(m_Z)":        ("ratio", 127.94),
    "alpha_s^-1(m_Z)":      ("ratio", 8.467),
    "sin^2 theta_W":         ("ratio", 0.23121),
    "m_p / m_e":             ("ratio", 1836.15),
    "m_mu / m_e":            ("ratio", 206.768),
    "m_W / m_p":             ("ratio", 85.7),
    "v_Higgs (GeV)":         ("ratio", 246.22),
    "m_W (GeV)":             ("ratio", 80.379),
    "m_Z (GeV)":             ("ratio", 91.188),
    "m_H (GeV)":             ("ratio", 125.10),
    "m_tau (GeV)":           ("ratio", 1.77686),
    "V_us^2":                ("ratio", 0.0503),
    "V_cb^2":                ("ratio", 0.00169),
    "delta_CKM (deg)":       ("ratio", 68.5),
    "tan(theta_Cab)":        ("ratio", 0.2317),
    "Lambda_CKM Wolfenstein": ("ratio", 0.2245),
    "A_Wolfenstein":         ("ratio", 0.836),
    "R_b":                   ("ratio", 0.392),
    "Delta_m^2 ratio":       ("ratio", 33.96),
    "sin^2 theta_12":        ("ratio", 0.307),
    "sin^2 theta_23":        ("ratio", 0.546),
    "sin^2 theta_13":        ("ratio", 0.022),
    "y_top":                 ("ratio", 0.992),
    "y_b/y_tau":             ("ratio", 2.35),
    "lambda_H":              ("ratio", 0.1291),
    "n_s (CMB tilt)":        ("ratio", 0.9649),
    "sigma_8":               ("ratio", 0.812),
    "Omega_DM/Omega_b":      ("ratio", 5.41),
    "Omega_Lambda/Omega_DM": ("ratio", 2.58),
    "m_s/m_d":               ("ratio", 20.0),
    "m_s/m_u":               ("ratio", 43.3),
    "m_top/m_b":             ("ratio", 41.3),
    "m_s (MeV)":             ("ratio", 93.5),
    "Lambda_QCD/m_p":        ("ratio", 0.354),
    "eta_B * 10^10":         ("ratio", 6.10),
}


def search_simple_rationals(target: float, tol_pct: float = 1.0):
    """Search for a/b where a, b are PRIMITIVES (or product of two)."""
    candidates = []
    items = list(PRIMITIVES.items())

    # Form 1: a/b with single primitives
    for name_a, a in items:
        for name_b, b in items:
            if b == 0:
                continue
            val = a / b
            err = 100 * abs(val - target) / target if target != 0 else float('inf')
            if err < tol_pct:
                candidates.append({
                    "form": f"{name_a}/{name_b}",
                    "value": val,
                    "error_pct": err,
                    "complexity": 2,
                })

    # Form 2: a * b / c
    for (na, a), (nb, b), (nc, c) in product(items, items, items):
        if c == 0:
            continue
        if a * b > 10000 or c > 1000:  # skip extreme cases
            continue
        val = (a * b) / c
        err = 100 * abs(val - target) / target if target != 0 else float('inf')
        if err < tol_pct:
            candidates.append({
                "form": f"{na}*{nb}/{nc}",
                "value": val,
                "error_pct": err,
                "complexity": 3,
            })

    # Form 3: sqrt(a/b)
    for (na, a), (nb, b) in product(items, items):
        if b == 0 or a / b <= 0:
            continue
        val = math.sqrt(a / b)
        err = 100 * abs(val - target) / target if target != 0 else float('inf')
        if err < tol_pct:
            candidates.append({
                "form": f"sqrt({na}/{nb})",
                "value": val,
                "error_pct": err,
                "complexity": 3,
            })

    # Form 4: a + b/c
    for (na, a), (nb, b), (nc, c) in product(items, items, items):
        if c == 0:
            continue
        val = a + b / c
        err = 100 * abs(val - target) / target if target != 0 else float('inf')
        if err < tol_pct:
            candidates.append({
                "form": f"{na} + {nb}/{nc}",
                "value": val,
                "error_pct": err,
                "complexity": 3,
            })

    # Form 5: a - b/c
    for (na, a), (nb, b), (nc, c) in product(items, items, items):
        if c == 0:
            continue
        val = a - b / c
        err = 100 * abs(val - target) / target if target != 0 else float('inf')
        if err < tol_pct:
            candidates.append({
                "form": f"{na} - {nb}/{nc}",
                "value": val,
                "error_pct": err,
                "complexity": 3,
            })

    # Sort by complexity then error
    candidates.sort(key=lambda c: (c["complexity"], c["error_pct"]))
    return candidates[:3]  # Top 3 candidates


def search_log_q_power(target: float, tol_pct: float = 5.0):
    """For target close to 0 or to large numbers, search log_q exponent."""
    if target <= 0:
        return []
    log_q_val = math.log(target) / math.log(3)
    candidates = []
    for name, exp in PRIMITIVES.items():
        for sign in [+1, -1]:
            pred_log = sign * exp
            err = abs(pred_log - log_q_val)
            if err < tol_pct / 100:  # log absolute error
                candidates.append({
                    "form": f"q^({sign:+d}*{name})",
                    "log_q": pred_log,
                    "target_log_q": log_q_val,
                    "log_diff": err,
                })
    candidates.sort(key=lambda c: c["log_diff"])
    return candidates[:3]


def main():
    print("=" * 78)
    print("W(3,3) SUBSTRATE IDENTITY FINDER")
    print("=" * 78)

    results = {}
    for name, (kind, val) in TARGETS.items():
        if kind == "ratio":
            cands = search_simple_rationals(val, tol_pct=2.0)
            if cands:
                best = cands[0]
                results[name] = {
                    "target": val,
                    "best_form": best["form"],
                    "best_value": best["value"],
                    "best_error_pct": best["error_pct"],
                    "alternatives": [c["form"] for c in cands[1:]],
                }
                print(f"\n  {name:>25s} = {val:>10.4f}")
                print(f"    => {best['form']} = {best['value']:.4f} (err {best['error_pct']:.3f}%)")
                if cands[1:]:
                    for c in cands[1:]:
                        print(f"       alt: {c['form']} = {c['value']:.4f} (err {c['error_pct']:.3f}%)")
            else:
                results[name] = {"target": val, "best_form": None}
                print(f"\n  {name:>25s} = {val:>10.4f}  (no match within 2%)")

    out = Path("data") / "w33_substrate_identity_finder.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"\n{'='*78}\nSummary: {len(results)} targets searched, "
          f"{sum(1 for r in results.values() if r['best_form'])} found matches.")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
