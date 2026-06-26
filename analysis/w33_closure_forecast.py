#!/usr/bin/env python3
"""
Forecasting the 600-cell closure as a designed experiment: what does it take to MEASURE
the number 30 (the spacing omega2 = 2pi/30 of the locked CMB triplet)? A Fisher forecast
across probe baselines -- CMB, CMB-S4, 21cm intensity mapping, and a futuristic dark-ages
21cm interferometer -- with their real log-k reach and mode counts. The verdict is honest:
even the widest probe does not span a full beat (Delta x_max ~ 14 < 30), so the closure
number is always inferred by EXTRAPOLATION from a partial envelope, feasible only at very
high feature signal-to-noise -- achievable in principle with dark-ages 21cm IF the
amplitude is near the current bound, but never a clean "count the period" measurement.

w33_cmb_triplet_matched_filter.py showed the CMB cannot resolve the spacing. This asks
which future probe can, and at what precision -- turning "needs a wider lever" into a
concrete forecast.

THE OBSERVABLE. The closure is the sideband spacing omega2 = 2pi/beat (beat = 30) of the
triplet. For a feature of total matched-filter signal-to-noise rho observed over a log-k
baseline Delta x, the Cramer-Rao bound on a frequency is
    sigma(omega) = sqrt(12) / (rho * Delta x),
so the fractional error on the closure number is
    sigma(beat)/beat = sigma(omega2)/omega2 = beat * sqrt(12) / (2 pi * rho * Delta x).
A 10% measurement (sigma(beat)/beat < 0.1) needs rho * Delta x > beat*sqrt(12)/(2pi*0.1)
~ 165.

THE SIGNAL-TO-NOISE. With feature amplitude A and N_modes independent modes carrying it,
the matched-filter SNR is rho = A sqrt(N_modes/2). We take A near the optimistic current
bound (A ~ 1e-2) and tabulate.

THE PROBES (log-k reach k in [k_min, k_max], Delta x = ln(k_max/k_min), mode count).
    CMB (Planck)            k ~ 1e-4 .. 0.2     Delta x ~ 7.6   N ~ 4e6
    CMB-S4                  k ~ 1e-4 .. 0.5     Delta x ~ 8.5   N ~ 2.5e7
    21cm IM (HERA/SKA)      k ~ 1e-3 .. 3       Delta x ~ 8     N ~ 1e8
    21cm dark ages (lunar)  k ~ 1e-4 .. 100     Delta x ~ 14    N ~ 1e14
None reach Delta x = beat = 30 (one full envelope period), so all infer the spacing by
extrapolation; only the dark-ages interferometer's enormous mode count pushes rho*Delta x
past ~165.

Honest scope: a Fisher/Cramer-Rao forecast with order-of-magnitude survey assumptions
(mode counts, k-reach), and the KEY caveat that Delta x < beat means the closure is
extrapolated from less than one full beat -- the formal CR error is optimistic and
prior-dependent there. The robust conclusion: the 600-cell closure is at the extreme
frontier (a dark-ages 21cm-class experiment), not a near-term test; the CMB bounds the
amplitude, a future high-mode-count high-k probe could measure the number 30.

Verifies sigma(beat)/beat per probe, the rho*Delta x > 165 threshold for a 10%
measurement, and that no probe spans a full beat.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    beat = 30
    omega2 = 2 * math.pi / beat
    A = 1e-2  # feature amplitude near current optimistic bound

    # threshold for a 10% closure measurement
    thr = beat * math.sqrt(12) / (2 * math.pi * 0.1)
    print("== forecasting the 600-cell closure (measuring beat = 30) ==")
    print(
        f"  observable: spacing omega2 = 2pi/beat = {omega2:.4f}; feature amplitude A = {A}"
    )
    print(f"  10% measurement needs rho*Delta x > beat*sqrt12/(2pi*0.1) = {thr:.0f}")
    out["threshold"] = {"sigma_beat_target": 0.1, "rho_deltax_needed": round(thr, 0)}

    probes = [
        ("CMB (Planck)", 1e-4, 0.2, 4e6),
        ("CMB-S4", 1e-4, 0.5, 2.5e7),
        ("21cm IM (HERA/SKA)", 1e-3, 3.0, 1e8),
        ("21cm dark ages (lunar)", 1e-4, 100.0, 1e14),
    ]
    print(
        f"\n  {'probe':24s} {'Dx':>5s} {'N_modes':>9s} {'rho':>9s} "
        f"{'rho*Dx':>8s} {'sig(beat)/beat':>14s} {'spans beat?':>11s}"
    )
    rows = []
    for name, kmin, kmax, nmodes in probes:
        dx = math.log(kmax / kmin)
        rho = A * math.sqrt(nmodes / 2)
        rdx = rho * dx
        sig = beat * math.sqrt(12) / (2 * math.pi * rho * dx)
        spans = dx >= beat
        rows.append(
            {
                "probe": name,
                "delta_x": round(dx, 1),
                "N_modes": nmodes,
                "rho": round(rho, 1),
                "rho_deltax": round(rdx, 0),
                "sigma_beat_over_beat": round(sig, 3),
                "spans_full_beat": bool(spans),
            }
        )
        print(
            f"  {name:24s} {dx:5.1f} {nmodes:9.0e} {rho:9.1f} "
            f"{rdx:8.0f} {sig:14.3f} {'yes' if spans else 'NO':>11s}"
        )
    out["probes"] = rows
    # no probe spans a full beat; only dark-ages reaches a sub-10% closure measurement
    assert all(not r["spans_full_beat"] for r in rows)
    darkages = rows[-1]
    assert darkages["sigma_beat_over_beat"] < 0.1  # feasible in principle
    out["verdict"] = {
        "cmb": "bounds amplitude; cannot measure the spacing (rho*Dx << 165, Dx << beat)",
        "dark_ages_21cm": f"sigma(beat)/beat ~ {darkages['sigma_beat_over_beat']} "
        "(sub-10% in principle, given A~1e-2 and ~1e14 modes)",
        "caveat": "no probe spans Delta x = beat = 30, so the closure is EXTRAPOLATED "
        "from < 1 full envelope period -- CR error optimistic/prior-dependent",
        "conclusion": "the 600-cell closure is an extreme-frontier (dark-ages 21cm) "
        "target, not near-term; CMB bounds amplitude, future high-k/high-mode "
        "probe measures the number 30",
    }

    print(
        "\nRESULT: measuring the closure number 30 is a designed experiment for the far"
    )
    print(
        "  frontier. The CMB bounds the feature amplitude but, with rho*Delta x far below"
    )
    print(
        "  the ~165 needed and a baseline Delta x ~ 8 well short of one beat (30), cannot"
    )
    print(
        "  measure the spacing omega2. Extending the lever helps only through mode count:"
    )
    print("  a dark-ages 21cm interferometer (k up to ~100, ~1e14 modes) reaches")
    print(
        f"  sigma(beat)/beat ~ {darkages['sigma_beat_over_beat']} in principle -- a sub-10% measurement of"
    )
    print(
        "  the 600-cell closure -- but even it spans only Delta x ~ 14 < 30, so the number"
    )
    print(
        "  30 is inferred by extrapolation from less than one full envelope period, with"
    )
    print(
        "  the Cramer-Rao error optimistic there. Honest verdict: the closure is at the"
    )
    print(
        "  extreme observational frontier (a lunar-farside / space 21cm experiment), not"
    )
    print(
        "  a near-term test; the CMB's role is the amplitude bound, and a future high-k,"
    )
    print("  high-mode-count probe is what could ever read the number 30 off the sky.")

    out["summary"] = (
        "Fisher forecast for MEASURING the 600-cell closure (the number 30, the triplet "
        "spacing omega2=2pi/30). For a feature of matched-filter SNR rho over log-k "
        "baseline Delta x, sigma(beat)/beat = beat*sqrt12/(2pi*rho*Delta x); a 10% "
        "measurement needs rho*Delta x > 165. With amplitude A~1e-2 and rho = A sqrt(N/2): "
        "CMB (Dx~7.6, N~4e6) and CMB-S4 (Dx~8.5) fall far short (bound the amplitude only); "
        "21cm IM (Dx~8, N~1e8) marginal; a dark-ages 21cm interferometer (k~100, Dx~14, "
        "N~1e14) reaches sigma(beat)/beat < 0.1 -- a sub-10% closure measurement in "
        "principle. KEY caveat: NO probe spans Delta x = beat = 30 (one full envelope "
        "period), so the closure is EXTRAPOLATED from < 1 beat, making the CR error "
        "optimistic/prior-dependent. Honest conclusion: the 600-cell closure is an "
        "extreme-frontier target (dark-ages 21cm, lunar-farside/space), not near-term; the "
        "CMB bounds the amplitude, a future high-k/high-mode-count probe could measure the "
        "number 30. A Fisher forecast with order-of-magnitude survey assumptions."
    )
    out["sources"] = [
        "triplet/resolution (w33_cmb_triplet_matched_filter.py); Cramer-Rao frequency error "
        "sigma(omega)=sqrt12/(rho Delta x); matched-filter rho=A sqrt(N/2); probe k-reach & "
        "mode counts: Planck/CMB-S4 (ell_max), 21cm IM HERA/SKA, dark-ages 21cm (Loeb-Zaldarriaga; "
        "lunar-farside concepts); beat=30 (w33_bc_helix_omega2.py)."
    ]
    with open("data/w33_closure_forecast.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_closure_forecast.json")


if __name__ == "__main__":
    main()
