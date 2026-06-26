#!/usr/bin/env python3
"""
The matched filter on the locked triplet -- and an honest finding about what the CMB can
and cannot measure. The substrate signal is a RIGID triplet (carrier at omega1, sidebands
at omega1 +/- omega2, amplitude ratio 1 : b/2 : b/2), so a search co-adds all three lines
at the FIXED spacing omega2. The detection statistic for the spacing is the direct test
of the 600-cell closure (omega2 = 2pi/30). But the CMB's log-k window is too short to
RESOLVE the spacing: the beat period is 30 e-folds of ln k while the CMB spans only ~4-7,
so the sidebands blur into the carrier and the closure number 30 is NOT measurable from
the CMB alone -- it needs a wider lever (LSS, mu-distortions, 21 cm). This corrects the
over-optimistic "the spacing confirms closure" framing with the resolution reality.

w33_cmb_template_forecast.py fit the central line. Here we (a) add the sidebands as a
matched filter and quantify the S/N gain, and (b) ask whether the spacing omega2 -- the
closure observable -- is resolvable, and across which probes.

THE TRIPLET S/N GAIN (exact). With carrier amplitude A and sidebands A b/2, the Fisher
information on A from the full triplet vs the carrier alone is
    I_triplet / I_carrier = 1 + 2 (b/2)^2 = 1 + b^2/2,
so the amplitude error improves by sqrt(1 + b^2/2). For the fiducial envelope depth
b = 0.6 this is sqrt(1.18) = 1.086 -- a modest ~8% tightening (the sidebands carry little
power). The matched filter's real value is not raw sensitivity but that its detection
statistic is the SPACING omega2 = the 600-cell closure.

THE RESOLUTION REALITY (the honest finding). To separate a sideband at omega1 +/- omega2
from the carrier at omega1, the log-k window must be at least one beat period wide:
    Delta x >= 2 pi / omega2 = beat = 30   (e-folds of ln k).
The CMB TT window spans only Delta x ~ 4 (l = 30..2000) to ~7 (l = 2..2500), so
omega2 = 0.209 is far below the Fourier resolution delta omega ~ 2 pi / Delta x ~ 1 --
the three lines are UNRESOLVED; the sidebands appear as a slow amplitude/phase modulation
of the carrier, not as a measurable splitting. So the CMB BOUNDS the amplitude A (at the
q=3-fixed carrier frequency) but CANNOT measure the closure number 30.

THE LEVER ARM (what it takes). The spacing becomes resolvable only with a much wider
log-k baseline. Spectral mu-distortions probe k ~ 50-10^4 Mpc^-1 and 21 cm reaches
k ~ 100+, extending ln k by ~6 decades: Delta x_total ~ 14-18, approaching the
beat = 30 needed. So the 600-cell closure is a target for distortion/21 cm + CMB joint
analysis, not for the CMB alone. We tabulate the baselines below.

Honest scope: the S/N gain sqrt(1+b^2/2) is exact; the resolution thresholds use the
standard Fourier/Cramer-Rao scaling (order-of-magnitude). The headline is a HONEST
NEGATIVE that sharpens the program: the CMB bounds the amplitude, but measuring the
closure (the spacing omega2, hence the number 30) requires extending the log-k lever by
spectral distortions / 21 cm.

Verifies the triplet S/N gain, the resolution threshold Delta x >= beat, the CMB
non-resolution, and the lever-arm table to a resolvable baseline.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    theta = math.acos(-2 / 3)
    beat = 30
    w1, w2 = theta, 2 * math.pi / beat
    b = 0.6  # fiducial envelope depth

    # triplet S/N gain
    gain = math.sqrt(1 + b**2 / 2)
    print("== the locked triplet and its matched-filter S/N gain ==")
    print(
        f"  carrier omega1={w1:.4f} (A), sidebands omega1+/-omega2 (A*b/2 each), b={b}"
    )
    print(
        f"  I_triplet/I_carrier = 1 + b^2/2 = {1 + b**2/2:.3f}; "
        f"sigma_A improves x{gain:.3f} (~{100*(gain-1):.0f}% tighter)"
    )
    out["triplet_gain"] = {
        "b": b,
        "fisher_ratio": round(1 + b**2 / 2, 4),
        "sigma_A_improvement": round(gain, 4),
        "note": "modest; sidebands carry little power. Value is that the statistic is the spacing omega2.",
    }

    # resolution threshold: need Delta x >= 2pi/omega2 = beat to separate sidebands
    dx_needed = 2 * math.pi / w2
    print(
        f"\n[resolution threshold]  to resolve the spacing omega2={w2:.4f} need "
        f"Delta x >= 2pi/omega2 = {dx_needed:.1f} = beat = {beat}"
    )
    assert abs(dx_needed - beat) < 1e-9
    out["resolution_threshold"] = {
        "omega2": round(w2, 4),
        "delta_x_needed": round(dx_needed, 2),
        "equals_beat": beat,
        "meaning": "log-k window must span one full beat (30 e-folds) to split the triplet",
    }

    # the lever arm across probes: k-range -> Delta x = ln(k_max/k_min); resolution dω~2pi/Δx
    D_A = 14065.0
    probes = [
        ("CMB TT (l=30..2000)", 30 / D_A, 2000 / D_A),
        ("CMB wide (l=2..2500)", 2 / D_A, 2500 / D_A),
        ("+ LSS / Lyman-alpha (k~3)", 2 / D_A, 3.0),
        ("+ mu-distortions (k~1e4)", 2 / D_A, 1e4),
        ("+ 21cm / distortions (k~1e5)", 2 / D_A, 1e5),
    ]
    print(f"\n[lever arm]  spacing resolvable when Delta x >= {beat}")
    rows = []
    for name, kmin, kmax in probes:
        dx = math.log(kmax / kmin)
        dom = 2 * math.pi / dx  # Fourier resolution
        resolvable = dx >= beat
        # fractional error on the closure number ~ resolution / omega2 (Cramer-Rao order)
        sigma_beat_frac = dom / w2
        rows.append(
            {
                "probe": name,
                "delta_x": round(dx, 1),
                "freq_res": round(dom, 3),
                "resolves_omega2": bool(resolvable),
                "sigma(beat)/beat~": round(sigma_beat_frac, 2),
            }
        )
        flag = "RESOLVES" if resolvable else "blurred"
        print(
            f"  {name:32s} Dx={dx:5.1f}  dom={dom:.2f}  "
            f"sig(beat)/beat~{sigma_beat_frac:4.1f}  [{flag}]"
        )
    out["lever_arm"] = rows
    # CMB alone does NOT resolve; need extended lever toward Delta x ~ 30
    assert not rows[0]["resolves_omega2"]
    out["verdict"] = {
        "cmb_measures": "amplitude A at the q=3-fixed carrier (bound from forecast ~1e-3 optimistic)",
        "cmb_cannot_measure": "the spacing omega2 = the 600-cell closure number 30 (sub-resolution)",
        "needs": "wider log-k lever: spectral mu-distortions (k~1e4) + 21cm push Delta x toward beat=30",
    }

    print(
        "\nRESULT: the matched filter clarifies the division of labour. Co-adding the"
    )
    print(
        "  locked triplet (carrier + two sidebands at fixed spacing omega2) tightens the"
    )
    print(f"  amplitude by only sqrt(1+b^2/2) = {gain:.3f} (the sidebands carry little")
    print(
        "  power), so the CMB's job is to BOUND the amplitude A at the q=3-fixed carrier"
    )
    print(
        "  frequency. The closure itself -- the spacing omega2 = 2pi/30, the direct test"
    )
    print(
        "  of the 600-cell -- needs a log-k window at least one beat wide (Delta x >= 30"
    )
    print(
        "  e-folds), while the CMB spans only ~4-7, so the triplet is unresolved there."
    )
    print("  Measuring the number 30 is therefore a target for a joint analysis with")
    print("  spectral mu-distortions (k up to ~1e4) and 21 cm, which extend the lever")
    print("  toward the required baseline. Honest division: CMB bounds the coupling; a")
    print("  wide-lever probe measures the closure. The over-optimistic 'the spacing")
    print(
        "  confirms closure in the CMB' is corrected -- it confirms it only with reach."
    )

    out["summary"] = (
        "matched filter on the locked triplet -> an honest division of labour. Co-adding "
        "the carrier (omega1) and two sidebands (omega1 +/- omega2, amplitude A b/2) gives "
        "a Fisher S/N gain of only sqrt(1+b^2/2) = 1.086 for b=0.6 (sidebands carry little "
        "power), so the CMB's role is to BOUND the amplitude A at the q=3-fixed carrier. "
        "The closure observable -- the spacing omega2 = 2pi/30 (the 600-cell, the number "
        "30) -- requires a log-k window at least one beat wide, Delta x >= 2pi/omega2 = "
        "beat = 30 e-folds, while the CMB spans only Delta x ~ 4-7, so the triplet is "
        "UNRESOLVED (sidebands blur into a slow carrier modulation). Measuring the closure "
        "thus needs a wider lever: spectral mu-distortions (k~1e4) and 21 cm extend ln k "
        "by ~6 decades (Delta x ~ 14-18), approaching the required 30. Honest NEGATIVE "
        "that sharpens the program: CMB bounds the coupling; a wide-lever (distortion/21cm)"
        " joint analysis measures the closure number 30. S/N gain exact; resolution "
        "thresholds are standard Fourier/Cramer-Rao order-of-magnitude."
    )
    out["sources"] = [
        "triplet from product-to-sum (w33_cmb_template_forecast.py); Fisher info additivity; "
        "Fourier/Cramer-Rao frequency resolution delta omega ~ 2pi/Delta x; mu-distortion "
        "k-reach ~50-1e4 Mpc^-1 (Chluba; PIXIE); 21cm k-reach; 600-cell closure beat=30 "
        "(w33_bc_helix_omega2.py)."
    ]
    with open("data/w33_cmb_triplet_matched_filter.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cmb_triplet_matched_filter.json")


if __name__ == "__main__":
    main()
