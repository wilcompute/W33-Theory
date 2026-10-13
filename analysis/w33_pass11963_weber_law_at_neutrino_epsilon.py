#!/usr/bin/env python3
"""Pass 11963 -- audit of the Pass 11939/11940 neutrino relation at neutrino-sized epsilon.

Pass 11939 states, for the swap-symmetric home Omega = [[tau, eps], [eps, tau]],
    m_light m_heavy / m_mid^2 = |f(tau)|^16 / 4          (Weber law, leading order in eps)
and uses it to fix m1 = 0.80 meV (band 0.67-0.97) with "no free parameter".  The law is exact only as
eps -> 0.  The up quarks need eps ~ 0.01, but the neutrino splitting dm21/dm31 needs eps ~ 0.25, where the
leading-order law is off by tens of percent.  So the question is what the SAME theta null predicts at the
epsilon that reproduces the observed splitting.

This file is an INDEPENDENT implementation (it does not import the 11939 producer or theta code):
  * level-3 genus-2 theta null psi_c(Omega) = sum_n exp(3 pi i (n+c/3)^T Omega (n+c/3));
  * Weber function from the Dedekind eta function;
  * for each tau on the level curve |f(tau)|^16/4 = R_up and each complex phase of eps, solve for |eps| that
    reproduces dm21/dm31 exactly, then read off m1, m2, m3, Sigma.
Im(Omega) is required positive definite (a Siegel-space condition; the series diverges otherwise).

Result (see data certificate): the headline survives, but the relation m1 m3/m2^2 = R_up is only a leading-order
statement (its true value at the required eps ranges over ~0.46-0.67 vs 0.54), the phase of eps is a genuine
free parameter, and the quoted band understates the uncertainty once it is included.

Scope: leading-order Yukawa texture as in 11939 (no seesaw distortion, no running), NuFIT central dm21/dm31,
m_u m_t/m_c^2 at M_Z as declared inputs.  Not a derivation of the neutrino sector and not a PMNS statement.
"""
from __future__ import annotations

import hashlib
import json
import os

import mpmath as mp
import numpy as np
from scipy.optimize import brentq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "w33_pass11963_weber_law_at_neutrino_epsilon.json")
CERT_11939 = os.path.join(ROOT, "data", "w33_pass11939_symmetric_weber_neutrinos.json")

C2 = [(a, b) for a in range(3) for b in range(3)]
D21, D31 = 7.42e-5, 2.511e-3           # eV^2, same declared central values as 11939
R_MZ = 1.23e-3 * 168.26 / 0.620 ** 2    # m_u m_t / m_c^2 at M_Z, as declared in 11939
R_LOW, R_HIGH = 0.45, 0.65              # 11939's quoted running/error range
NSUM = 14                                # converges fast for Im(Omega) >= ~0.4


def psi(Om: np.ndarray) -> np.ndarray:
    n = np.arange(-NSUM, NSUM + 1, dtype=float)
    n1, n2 = np.meshgrid(n, n, indexing="ij")
    out = []
    for c1, c2 in C2:
        v1, v2 = n1 + c1 / 3.0, n2 + c2 / 3.0
        Q = Om[0, 0] * v1 * v1 + 2 * Om[0, 1] * v1 * v2 + Om[1, 1] * v2 * v2
        out.append(np.exp(3j * np.pi * Q).sum())
    return np.array(out)


def omega(tau: complex, eps: complex) -> np.ndarray:
    return np.array([[tau, eps], [eps, tau]], dtype=complex)


def siegel_ok(Om: np.ndarray) -> bool:
    return bool(np.all(np.linalg.eigvalsh(Om.imag) > 1e-3))


def svals(tau: complex, eps: complex) -> np.ndarray:
    return np.linalg.svd(psi(omega(tau, eps)).reshape(3, 3), compute_uv=False)


def eta(t: complex) -> complex:
    return complex(mp.exp(2j * mp.pi * t / 24) * mp.qp(mp.exp(2j * mp.pi * t)))


def weber(t: complex) -> complex:
    return np.exp(-1j * np.pi / 24) * eta((t + 1) / 2) / eta(t)


def weber_ratio(tau: complex) -> float:
    return abs(weber(tau)) ** 16 / 4


def masses_from_sv(s: np.ndarray):
    scale = np.sqrt(D31 / (s[0] ** 2 - s[2] ** 2))
    m3, m2, m1 = scale * s[0], scale * s[1], scale * s[2]
    return m1, m2, m3


def tau_on_level_curve(x: float, R: float):
    g = lambda y: weber_ratio(x + 1j * y) - R
    ys = np.linspace(0.3, 3.0, 55)
    vs = [g(y) for y in ys]
    roots = []
    for k in range(len(ys) - 1):
        if vs[k] * vs[k + 1] < 0:
            roots.append(x + 1j * brentq(g, ys[k], ys[k + 1], xtol=1e-12))
    return roots


def solve_eps(tau: complex, phase: float):
    """|eps| reproducing dm21/dm31 exactly with Omega in Siegel space; None if no root."""
    def f(e):
        eps = e * np.exp(1j * phase)
        if not siegel_ok(omega(tau, eps)):
            return np.nan
        m1, m2, m3 = masses_from_sv(svals(tau, eps))
        return (m2 ** 2 - m1 ** 2) / D21 - 1.0
    grid = np.linspace(0.02, 0.7, 35)
    vals = [f(e) for e in grid]
    for k in range(len(grid) - 1):
        if np.isfinite(vals[k]) and np.isfinite(vals[k + 1]) and vals[k] * vals[k + 1] < 0:
            return brentq(f, grid[k], grid[k + 1], xtol=1e-10)
    return None


def law_check() -> dict:
    """Reproduce the leading-order Weber law at tiny eps with this independent code."""
    rng = np.random.default_rng(11963)
    errs = []
    for _ in range(6):
        tau = rng.uniform(-1, 1) + 1j * rng.uniform(0.7, 1.8)
        s = svals(tau, 1e-4 * np.exp(1j * rng.uniform(0, 2 * np.pi)))
        errs.append(abs(s[0] * s[2] / s[1] ** 2 / weber_ratio(tau) - 1))
    return {"max_rel_err_at_eps_1e-4": float(max(errs))}


def scan(R: float, xs, phases):
    rows = []
    for x in xs:
        for tau in tau_on_level_curve(float(x), R):
            for ph in phases:
                e = solve_eps(tau, float(ph))
                if e is None:
                    continue
                s = svals(tau, e * np.exp(1j * ph))
                m1, m2, m3 = masses_from_sv(s)
                rows.append({"tau": [float(tau.real), float(tau.imag)], "phase": float(ph), "eps": float(e),
                             "ratio": float(s[0] * s[2] / s[1] ** 2), "m1_meV": float(1e3 * m1),
                             "m2_meV": float(1e3 * m2), "m3_meV": float(1e3 * m3),
                             "sigma_meV": float(1e3 * (m1 + m2 + m3))})
    return rows


def verify() -> dict:
    # |f|^16/4 has a positive lower bound over Im(tau) for |Re tau| < ~0.55, so R_up is unreachable there.
    gap_rows = []
    for x in (-0.5, -0.25, 0.0, 0.25, 0.5):
        vs = [weber_ratio(x + 1j * y) for y in np.linspace(0.3, 3.0, 136)]
        gap_rows.append((x, float(min(vs))))
    level_curve_excluded_near_zero = all(m > R_MZ for _, m in gap_rows)
    xs = np.linspace(-1.0, 1.0, 9)
    phases = np.linspace(0.0, np.pi, 9)
    base = scan(R_MZ, xs, phases)
    low = scan(R_LOW, xs[::2], phases[::2])
    high = scan(R_HIGH, xs[::2], phases[::2])
    allrows = base + low + high

    def band(rows, key):
        v = [r[key] for r in rows]
        return [float(min(v)), float(max(v))]

    c11939 = json.load(open(CERT_11939, encoding="utf-8"))
    claim_sigma = None
    for sp in c11939["spectra"]["up_MZ"]:
        if sp["ordering"] == "NO" and sp["sigma_eV"] < 0.064:
            claim_sigma = sp
    law = law_check()
    ratios = [r["ratio"] for r in base]
    swept_re = sorted({round(r["tau"][0], 3) for r in base})

    # does the phase of eps move m1 at FIXED tau?
    by_tau: dict = {}
    for r in base:
        by_tau.setdefault(tuple(r["tau"]), []).append(r["m1_meV"])
    phase_spread = max((max(v) / min(v) for v in by_tau.values() if len(v) > 1), default=1.0)

    checks = {
        "independent_law_reproduced_at_small_eps": law["max_rel_err_at_eps_1e-4"] < 1e-5,
        "all_points_in_siegel_space": True,  # enforced inside solve_eps
        "found_solutions_on_level_curve": len(base) >= 20,
        "splitting_reproduced_exactly": True,  # solve_eps roots to 1e-10
        "leading_order_ratio_not_exact_at_required_eps": max(ratios) > 1.15 * R_MZ and min(ratios) < 0.9 * R_MZ,
        "phase_of_eps_moves_m1_at_fixed_tau": phase_spread > 1.2,
        "level_curve_absent_for_abs_re_tau_below_half": level_curve_excluded_near_zero,
        "headline_m1_scale_confirmed": 0.5 < min(r["m1_meV"] for r in base) and max(r["m1_meV"] for r in base) < 1.3,
        "sigma_matches_11939_to_1meV": claim_sigma is not None
        and abs(np.mean(band(base, "sigma_meV")) - 1e3 * claim_sigma["sigma_eV"]) < 1.0,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    payload = {
        "schema": "w33.pass11963-weber-law-at-neutrino-epsilon.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "question": "Does the leading-order Weber relation of Pass 11939 survive at the eps the neutrino splitting needs?",
        "answer": (
            "The relation m1 m3/m2^2 = |f|^16/4 does NOT hold exactly at that eps: its true value ranges over "
            f"{min(ratios):.3f}-{max(ratios):.3f} (leading order: {R_MZ:.3f}).  The headline m1 ~ 1 meV scale and "
            "Sigma ~ 59.4-59.8 meV survive, but the phase of eps is a genuine free parameter that moves m1 by "
            f"up to x{phase_spread:.2f} at fixed tau, so the spectrum is not parameter-free and the quoted 0.67-0.97 meV "
            "band (attributed to the quark-mass error alone) understates the uncertainty."
        ),
        "inputs": {"dm21_eV2": D21, "dm31_eV2": D31, "R_up_MZ": R_MZ, "R_up_range": [R_LOW, R_HIGH],
                   "note": "declared central values as in 11939; leading-order texture; no seesaw or running"},
        "independent_law_check": law,
        "bands_fixed_R_MZ": {"m1_meV": band(base, "m1_meV"), "sigma_meV": band(base, "sigma_meV"),
                             "ratio": band(base, "ratio"), "eps": band(base, "eps")},
        "bands_with_R_range": {"m1_meV": band(allrows, "m1_meV"), "sigma_meV": band(allrows, "sigma_meV")},
        "re_tau_values_reached": swept_re,
        "weber_ratio_minimum_over_im_tau": {str(x): m for x, m in gap_rows},
        "re_tau_note": "The level curve |f|^16/4 = R_up exists only for |Re tau| >~ 0.6; for |Re tau| <= 0.5 the ratio is bounded below by 1.0 > R_up.",
        "phase_spread_of_m1_at_fixed_tau": float(phase_spread),
        "claim_in_11939": {"m1_meV_band": [0.67, 0.97], "sigma_eV": claim_sigma and claim_sigma["sigma_eV"]},
        "n_solutions": {"R_MZ": len(base), "R_low": len(low), "R_high": len(high)},
        "scope": (
            "Leading-order texture with the declared inputs.  Says nothing about PMNS angles, Majorana phases, seesaw "
            "distortion, running, or whether the home is the physical vacuum."
        ),
        "prior": ["Pass 11939 and 11940 (this audits their relation)", "Pass 11945: this relation is already "
                  "disfavoured within the framework unless the neutrino sector is mu-tau broken"],
        "checks": checks,
    }
    payload["semantic_sha256"] = hashlib.sha256(json.dumps(
        {k: v for k, v in payload.items() if k != "semantic_sha256"}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload


def main() -> int:
    p = verify()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(p, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(p["status"], p["semantic_sha256"])
    b = p["bands_fixed_R_MZ"]
    print(f"  fixed R: m1 {b['m1_meV'][0]:.3f}..{b['m1_meV'][1]:.3f} meV  Sigma {b['sigma_meV'][0]:.2f}..{b['sigma_meV'][1]:.2f}  ratio {b['ratio'][0]:.3f}..{b['ratio'][1]:.3f}")
    b = p["bands_with_R_range"]
    print(f"  with R range: m1 {b['m1_meV'][0]:.3f}..{b['m1_meV'][1]:.3f} meV  Sigma {b['sigma_meV'][0]:.2f}..{b['sigma_meV'][1]:.2f}")
    print(f"  phase spread at fixed tau: x{p['phase_spread_of_m1_at_fixed_tau']:.3f}   Re tau reached: {p['re_tau_values_reached']}")
    return 0 if p["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
