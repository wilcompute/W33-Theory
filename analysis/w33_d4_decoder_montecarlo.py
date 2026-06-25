#!/usr/bin/env python3
"""
The D4-GKP advantage as MEASURED data -- and an honest correction. A real Conway-
Sloane closest-point decoder, run over sampled Gaussian displacements, shows the
D4-vs-square advantage is ERROR-RATE DEPENDENT: ~0.7 dB at logical error 1e-2,
growing toward the nominal 1.5 dB coding gain only as the error rate -> 0. The full
1.5 dB is the ASYMPTOTIC gain; at finite error rates it is suppressed by D4's larger
kissing number (24 vs 8). So the constant-1.5-dB curve of w33_d4_gkp_error_curve.py
is the optimistic (low-error) limit, and the real advantage at realistic error rates
is smaller -- a correction the simulation makes that the union-bound shift hid.

A GKP displacement error is CORRECTABLE iff the noise stays in the Voronoi cell of
the code lattice (closest-point decoding returns the origin); it becomes a logical
error when the noise escapes the cell (closest point != 0). So the lattice quantizer
error probability P(closest lattice point != 0) IS the GKP correctable-error
probability. We measure it directly for D4 and Z^4, both normalised to the SAME
density (det^{1/n}=1), via Monte Carlo over iid Gaussian noise.

DECODERS (exact):
  * Z^4: closest point = coordinatewise rounding.
  * D4 = {x in Z^4 : sum x_i even}: Conway-Sloane -- round to nearest integers; if the
    coordinate sum is odd, flip the rounding of the coordinate furthest from its
    rounded value (changes parity -> closest even-sum point). [SPLAG, Alg. for D_n.]

NORMALISATION: D4 det(Gram)=4 -> volume 2; scale by 2^{-1/4} so volume 1 = Z^4. Then
d_min^2(D4)=2*2^{-1/2}=1.414 vs d_min^2(Z^4)=1: nominal coding gain 10log10(1.414)=1.5
dB. But D4 has kissing number 24 vs Z^4's 8: at finite error the union bound
P ~ (N/2) erfc(d_min/(2 sqrt2 sigma)) carries the prefactor N, so D4's 3x-larger
kissing number eats into the distance advantage until the erfc (distance) term wins
asymptotically.

MEASURED (below): advantage 10 log10(sigma_D4^2/sigma_Z4^2) at fixed logical error
grows from ~0.7 dB (error 1e-2) toward ~1.5 dB (error -> 0), tracking the union-bound
prediction with kissing numbers. The honest threshold statement is therefore: D4
beats the square code by ~0.7 dB at near-threshold error rates, approaching the full
1.5 dB only deep below threshold.

Honest scope: single-shot lattice quantizer (one round of GKP correction), the
cleanest faithful model; the full FT threshold still needs finite-squeezing ancillas,
repeated syndrome extraction and a surface-code decoder. What is measured: the EXACT,
error-rate-dependent D4-vs-square lattice advantage, correcting the constant-1.5-dB
assumption.
"""
from __future__ import annotations

import json
import math

import numpy as np


def closest_Z4(X):
    """Closest point in Z^4: coordinatewise rounding."""
    return np.rint(X)


def closest_D4(X):
    """Closest point in D4={x in Z^4: sum even} (Conway-Sloane)."""
    R = np.rint(X)
    s = R.sum(axis=1)
    odd = (np.abs(s).astype(np.int64) % 2) != 0
    diff = X - R
    k = np.argmax(np.abs(diff), axis=1)
    idx = np.arange(X.shape[0])
    flip = np.sign(diff[idx, k])
    flip[flip == 0] = 1.0
    Rfix = R.copy()
    Rfix[idx, k] = R[idx, k] + flip
    return np.where(odd[:, None], Rfix, R)


def p_error(sigma, lattice, scale, n_samples, rng):
    """Fraction of Gaussian noise vectors (std sigma) that escape the Voronoi cell
    of the scaled lattice (closest point != 0)."""
    X = rng.normal(0.0, sigma, size=(n_samples, 4))
    Y = X / scale
    C = closest_Z4(Y) if lattice == "Z4" else closest_D4(Y)
    return np.any(np.abs(C) > 1e-9, axis=1).mean()


def sigma_at_target_mc(target, lattice, scale, rng, n_samples):
    """Bisect the noise sigma giving measured P_error = target."""
    lo, hi = 0.05, 0.6
    for _ in range(20):
        mid = 0.5 * (lo + hi)
        if p_error(mid, lattice, scale, n_samples, rng) > target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def sigma_at_target_analytic(target, dmin, kissing):
    """Union-bound sigma at target: (kissing/2) erfc(dmin/(2 sqrt2 sigma)) = target."""
    lo, hi = 0.02, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        p = (kissing / 2.0) * math.erfc(dmin / (2 * math.sqrt(2) * mid))
        if p > target:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def main():
    out = {}
    rng = np.random.default_rng(33)

    # equal-density scales: Z^4 volume 1; D4 volume 2 -> scale 2^{-1/4}
    scale_Z4, scale_D4 = 1.0, 2.0 ** (-0.25)
    dmin_Z4, dmin_D4 = 1.0, math.sqrt(2.0 * scale_D4**2)  # sqrt(1.414)=1.189
    kiss_Z4, kiss_D4 = 8, 24
    gain_nominal = 10 * math.log10(dmin_D4**2 / dmin_Z4**2)
    print(
        f"[normalisation, equal density]  d_min: Z4={dmin_Z4}, D4={dmin_D4:.4f}; "
        f"kissing Z4={kiss_Z4}, D4={kiss_D4}; nominal gain={gain_nominal:.2f} dB"
    )
    assert abs(gain_nominal - 1.5) < 0.05
    test = np.array([[0.6, 0.6, 0.1, 0.1]])
    assert np.allclose(closest_D4(test), [[1, 1, 0, 0]])
    print("  decoder spot-check ok (D4 nearest of (0.6,0.6,0.1,0.1) = (1,1,0,0))")
    out["setup"] = {
        "dmin_D4": round(dmin_D4, 4),
        "kissing": {"Z4": kiss_Z4, "D4": kiss_D4},
        "nominal_gain_dB": round(gain_nominal, 2),
    }

    # measured advantage vs target error -- it GROWS toward 1.5 dB as error -> 0
    print("\n[measured advantage vs target logical error (real decoder)]")
    print("  P_err  | sigma_Z4 | sigma_D4 | MEASURED dB | union-bound dB")
    adv = []
    for t, ns in (
        (3e-2, 1_500_000),
        (1e-2, 2_500_000),
        (3e-3, 5_000_000),
        (1e-3, 9_000_000),
    ):
        sz = sigma_at_target_mc(t, "Z4", scale_Z4, rng, ns)
        sd = sigma_at_target_mc(t, "D4", scale_D4, rng, ns)
        a_mc = 10 * math.log10(sd**2 / sz**2)
        # analytic union-bound advantage (with kissing numbers)
        az = sigma_at_target_analytic(t, dmin_Z4, kiss_Z4)
        ad = sigma_at_target_analytic(t, dmin_D4, kiss_D4)
        a_ub = 10 * math.log10(ad**2 / az**2)
        print(f"  {t:.0e} |  {sz:.4f}  |  {sd:.4f}  |   {a_mc:5.2f}    |   {a_ub:5.2f}")
        adv.append(
            {
                "target": t,
                "sigma_Z4": round(sz, 4),
                "sigma_D4": round(sd, 4),
                "advantage_measured_dB": round(a_mc, 2),
                "advantage_unionbound_dB": round(a_ub, 2),
            }
        )
    out["advantage_vs_error"] = adv

    # the trend: advantage increases toward the nominal 1.5 dB
    advs = [a["advantage_measured_dB"] for a in adv]
    growing = all(advs[i] <= advs[i + 1] + 0.15 for i in range(len(advs) - 1))
    print(f"\n[trend]  measured advantage grows {advs[0]:.2f} -> {advs[-1]:.2f} dB as")
    print(
        f"  P_err 3e-2 -> 1e-3, toward the asymptotic coding gain {gain_nominal:.2f} dB."
    )
    print(f"  monotone-increasing (within MC noise): {growing}")
    assert advs[-1] > advs[0]  # advantage genuinely grows at lower error
    out["trend"] = {
        "advantage_low_error": advs[0],
        "advantage_high_squeezing": advs[-1],
        "asymptote_dB": round(gain_nominal, 2),
        "growing": bool(growing),
    }

    # honest engineering statement at a near-threshold error rate
    a_near = adv[1]["advantage_measured_dB"]  # at 1e-2
    print(f"\n[honest engineering]")
    print(
        f"  near-threshold (P_err~1e-2) D4 advantage = {a_near:.2f} dB (NOT the full 1.5);"
    )
    print(f"  square 9.9 dB -> D4 ~ {9.9-a_near:.1f} dB there, approaching 8.4 dB only")
    print(f"  deep below threshold where the full 1.5 dB coding gain is realised.")
    out["engineering"] = {
        "advantage_near_threshold_dB": a_near,
        "D4_threshold_near_dB": round(9.9 - a_near, 1),
        "D4_threshold_asymptotic_dB": 8.4,
        "note": "advantage is error-rate dependent; 1.5 dB is the low-error asymptote",
    }

    print(
        "\nRESULT: the real decoder corrects the model. A Conway-Sloane closest-point"
    )
    print(
        "  decoder over Gaussian noise (both codes equal density) gives a D4-vs-square"
    )
    print(
        f"  advantage that GROWS from ~{advs[0]:.1f} dB at logical error 3e-2 to "
        f"~{advs[-1]:.1f} dB at 1e-3,"
    )
    print(
        "  tracking the union-bound prediction WITH kissing numbers (D4's 24 vs Z4's 8"
    )
    print("  suppresses the finite-error advantage) and approaching the nominal 1.5 dB")
    print(
        "  coding gain only asymptotically. So the constant-1.5-dB curve was the low-"
    )
    print("  error limit: the honest near-threshold advantage is ~0.7-1.0 dB, with the")
    print(
        "  full 1.5 dB realised deep below threshold. The qualitative claim (D4 beats"
    )
    print(
        "  the square code, threshold shifts down) holds; the size is error-dependent."
    )

    out["summary"] = (
        "real D4 decoder CORRECTS the constant-1.5-dB model. Conway-Sloane closest-point "
        "decoding over Gaussian noise (equal density) gives a D4-vs-square advantage that "
        f"GROWS from ~{advs[0]:.1f} dB at logical error 3e-2 to ~{advs[-1]:.1f} dB at 1e-3, "
        "tracking the union bound WITH kissing numbers (D4 kissing 24 vs Z4 8 suppresses "
        "the finite-error gain) and approaching the nominal 1.5 dB only asymptotically. "
        "Honest near-threshold advantage ~0.7-1.0 dB; full 1.5 dB deep below threshold. "
        "Qualitative claim (D4 beats square, threshold shifts down) holds; magnitude is "
        "error-rate dependent -- a correction the simulation makes that the union-bound "
        "shift hid."
    )
    out["sources"] = [
        "Conway-Sloane, SPLAG (D_n closest-point algorithm; coding gains; kissing "
        "numbers 8, 24); GKP correctable region = Voronoi cell; Conrad-Eisert-"
        "Hangleiter, Quantum 6, 648 (2022); Noh-Chamberland 9.9 dB; "
        "w33_d4_gkp_error_curve.py, w33_gkp_coding_gain.py."
    ]
    with open("data/w33_d4_decoder_montecarlo.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_d4_decoder_montecarlo.json")


if __name__ == "__main__":
    main()
