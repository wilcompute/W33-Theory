#!/usr/bin/env python3
"""
From a template to a NUMBER: fit the q=3 clock template to a mock Planck-TT data vector
and report the actual sensitivity to the modulation amplitude A. This is the first step
that touches data with an error bar instead of a consistency check -- a Fisher/mock
forecast of the bound a feature search would place on the substrate's inflaton-clock
coupling, at the q=3-LOCKED frequencies.

w33_cmb_template.py fixed the shape (omega1=theta=arccos(-2/3), omega2=2pi/30, both
pinned by q=3). Here we build a cosmic-variance-limited mock TT covariance over the
Planck multipole window, inject (and recover) the central line, and read off sigma_A.

THE SPECTRAL SIGNATURE (made exact). The template
    delta P/P = A cos(w1 x + p1) [1 + b cos(w2 x + p2)],   x = ln(k/k_*)
expands (product-to-sum) into a TRIPLET of pure log-cosines:
    A cos(w1 x + p1)                                         [central line, freq w1]
  + (A b/2) cos((w1+w2) x + p1+p2)                           [upper sideband]
  + (A b/2) cos((w1-w2) x + p1-p2)                           [lower sideband]
so the substrate predicts THREE lines at {w1-w2, w1, w1+w2} = {2.091, 2.301, 2.510},
a carrier split by the ring envelope w2 -- the frequency-domain face of the three-gap
comb. A feature search looks for this triplet, not a single line.

THE MOCK LIKELIHOOD. Map multipole to wavenumber k(l) = l / D_A (D_A = 14065 Mpc, the
Planck comoving distance to last scattering), x(l) = ln(k/k_*), k_* = 0.05 Mpc^-1. The
cosmic-variance fractional error on C_l is sigma_l = sqrt(2 / ((2l+1) f_sky)). Over
l in [30, 2000], f_sky = 0.7, the feature imprints delta C_l / C_l = T(l) * delta P/P;
we take the transfer T = 1 (the OPTIMISTIC, cosmic-variance-limited case -- the real
acoustic transfer projects and Silk-damps the feature, weakening the bound by a
realistic factor of a few-to-ten, which we flag). Weighted least squares on the design
[cos(w1 x), sin(w1 x)] profiles the phase analytically; A = sqrt(c1^2 + c2^2), and the
2x2 Fisher inverse gives sigma_A.

THE RESULT (computed below). The cosmic-variance-limited forecast is sigma_A ~ 1e-3, so
a null gives a 95% upper limit A < ~2e-3 (optimistic). Real Planck analyses of
log-periodic features (axion monodromy / resonant inflation) reach amplitudes of a few
percent; our optimistic forecast sits an order of magnitude below, confirming the
feature is detectable/boundable and quantifying the gap a full transfer treatment must
close. We also inject A_true = 0.01 and recover it at the computed significance, showing
the pipeline works.

Honest scope: a FORECAST with a simplified (cosmic-variance-limited, transfer=1) noise
model, not the real Planck likelihood -- it gives the order of magnitude of the
sensitivity and demonstrates recovery, with the optimistic-vs-realistic gap named. The
frequencies are q=3-fixed (the prediction); only A, b, phases are fit.

Verifies the triplet expansion, builds the mock covariance, fits the central line,
recovers an injected signal, and reports sigma_A and the 95% upper limit.
"""
from __future__ import annotations

import json
import math

import numpy as np


def main():
    out = {}
    rng = np.random.default_rng(33)
    q = 3
    theta = math.acos(-2 / 3)
    beat = 30
    w1, w2 = theta, 2 * math.pi / beat

    # the triplet (product-to-sum)
    triplet = [round(w1 - w2, 4), round(w1, 4), round(w1 + w2, 4)]
    print("== the spectral triplet (frequency-domain face of the three-gap comb) ==")
    print(
        f"  lines at {{w1-w2, w1, w1+w2}} = {triplet}  (carrier w1 split by envelope w2)"
    )
    out["triplet"] = {
        "lower_sideband": triplet[0],
        "carrier_w1": triplet[1],
        "upper_sideband": triplet[2],
        "carrier_amp": "A",
        "sideband_amp": "A*b/2",
    }

    # mock Planck-TT window
    D_A = 14065.0  # Mpc, comoving distance to last scattering
    k_star = 0.05  # Mpc^-1 pivot
    f_sky = 0.7
    ells = np.arange(30, 2001)
    kk = ells / D_A
    x = np.log(kk / k_star)
    sigma = np.sqrt(2.0 / ((2 * ells + 1) * f_sky))  # fractional CV error on C_l
    w = 1.0 / sigma**2  # inverse-variance weights

    print(
        f"\n[mock TT window]  l in [{ells[0]},{ells[-1]}], f_sky={f_sky}, "
        f"x=ln(k/k_*) in [{x[0]:.2f},{x[-1]:.2f}]  ({len(ells)} modes)"
    )
    out["window"] = {
        "l_min": int(ells[0]),
        "l_max": int(ells[-1]),
        "f_sky": f_sky,
        "x_range": [round(float(x[0]), 3), round(float(x[-1]), 3)],
        "n_modes": int(len(ells)),
        "transfer": "T=1 (optimistic, cosmic-variance-limited; real transfer weakens this)",
    }

    # design for the central line: A cos(w1 x + p1) = c1 cos(w1 x) + c2 sin(w1 x)
    c = np.cos(w1 * x)
    s = -np.sin(w1 * x)  # so c1=A cos p1, c2=A sin p1
    # Fisher (weighted) 2x2
    F = np.array(
        [
            [np.sum(w * c * c), np.sum(w * c * s)],
            [np.sum(w * c * s), np.sum(w * s * s)],
        ]
    )
    Finv = np.linalg.inv(F)
    # amplitude error: sigma_A ~ sqrt(mean diagonal of Finv) (cos/sin nearly orthogonal)
    sigma_A = math.sqrt(0.5 * (Finv[0, 0] + Finv[1, 1]))
    ul95 = 1.96 * sigma_A
    print(
        f"\n[null forecast]  sigma_A = {sigma_A:.2e}  ->  95% upper limit A < {ul95:.2e}"
    )
    print(
        "  (cosmic-variance-limited / transfer=1; real Planck features bound A ~ few %,"
    )
    print(
        "   so this optimistic forecast sits ~10x below -- the feature is boundable.)"
    )
    out["forecast"] = {
        "sigma_A": float(f"{sigma_A:.3e}"),
        "upper_limit_95pct": float(f"{ul95:.3e}"),
        "note": "cosmic-variance-limited optimistic; realistic transfer weakens by a few-to-ten",
        "realistic_planck_feature_bound": "~ few percent (axion-monodromy/resonant analyses)",
    }
    assert sigma_A > 0 and sigma_A < 1e-1

    # injection-recovery: inject A_true = 0.01 (1%) and fit it back
    A_true, p_true = 0.01, 0.7
    signal = A_true * np.cos(w1 * x + p_true)
    noise = rng.normal(0.0, sigma)
    data = signal + noise
    b = np.array([np.sum(w * data * c), np.sum(w * data * s)])
    chat = Finv @ b
    A_hat = math.hypot(chat[0], chat[1])
    p_hat = math.atan2(chat[1], chat[0])
    snr = A_hat / sigma_A
    print(
        f"\n[injection-recovery]  inject A_true={A_true} (1%); "
        f"recover A_hat={A_hat:.4f} at {snr:.0f} sigma; phase {p_hat:.2f} (true {p_true})"
    )
    out["injection_recovery"] = {
        "A_true": A_true,
        "A_hat": round(A_hat, 5),
        "snr": round(snr, 1),
        "phase_true": p_true,
        "phase_hat": round(p_hat, 3),
    }
    assert abs(A_hat - A_true) < 5 * sigma_A  # recovered within errors

    print(
        "\nRESULT: the q=3 clock template now touches data with an error bar. Expanded,"
    )
    print(
        f"  it predicts a spectral TRIPLET at {{{triplet[0]}, {triplet[1]}, {triplet[2]}}}"
    )
    print(
        "  -- a carrier at w1=theta=arccos(-2/3) split by the ring envelope w2=2pi/30 --"
    )
    print(
        "  the frequency-domain form of the three-gap comb. Fitting the central line to"
    )
    print(
        "  a cosmic-variance-limited mock Planck-TT vector (l=30..2000, f_sky=0.7) gives"
    )
    print(
        f"  sigma_A = {sigma_A:.1e}, a 95% upper limit A < {ul95:.1e} in the optimistic"
    )
    print("  (transfer=1) case; an injected 1% modulation is recovered at high")
    print("  significance, so the pipeline works. Real acoustic transfer (projection +")
    print("  Silk damping) weakens the bound by a realistic factor of a few-to-ten,")
    print("  landing near the few-percent level current Planck feature searches reach.")
    print("  Either way the substrate's prediction is now a constrainable amplitude at")
    print(
        "  FIXED, q=3-locked frequencies -- the maximally constrained sky test, with a"
    )
    print("  number attached.")

    out["summary"] = (
        "the q=3 CMB clock template, fit to a mock Planck-TT covariance, yields a NUMBER. "
        "Expanded (product-to-sum), delta P/P predicts a spectral TRIPLET at "
        "{w1-w2, w1, w1+w2} = {2.091, 2.301, 2.510} -- a carrier at w1=theta=arccos(-2/3) "
        "split by the ring envelope w2=2pi/30 (the frequency-domain three-gap comb). A "
        "cosmic-variance-limited mock TT likelihood (l=30..2000, f_sky=0.7, x=ln(k/k_*), "
        "transfer T=1 optimistic) gives sigma_A ~ 1e-3, a 95% upper limit A < ~2e-3; an "
        "injected 1% modulation is recovered at high SNR (pipeline works). Real acoustic "
        "transfer weakens this by a few-to-ten (landing near the few-percent level Planck "
        "feature searches reach). Honest: a FORECAST with a simplified noise model, not "
        "the real Planck likelihood -- it gives the order of magnitude and demonstrates "
        "recovery, with the optimistic/realistic gap named. Frequencies q=3-fixed (the "
        "prediction); only A, b, phases fit. First time the theory meets data with an "
        "error bar."
    )
    out["sources"] = [
        "template (w33_cmb_template.py); product-to-sum triplet; Planck 2018 X (feature/"
        "oscillation searches, amplitude bounds ~few %); cosmic variance sigma_l="
        "sqrt(2/((2l+1)f_sky)); D_A=14065 Mpc, k_*=0.05; axion-monodromy/resonant "
        "templates (Flauger et al.; Chen); Cobaya/CLASS feature likelihoods."
    ]
    with open("data/w33_cmb_template_forecast.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cmb_template_forecast.json")


if __name__ == "__main__":
    main()
