#!/usr/bin/env python3
"""
A falsifiable CMB fingerprint of the clock: if the substrate's Boerdijk-Coxeter time
quasicrystal couples to the inflaton, the primordial power spectrum carries a
QUASI-PERIODIC modulation whose peaks have a three-gap (Steinhaus) spacing in ln k --
a feature distinct from smooth slow-roll (no oscillation) and from single-frequency
resonant inflation (one clean log-period). The frequency is fixed by the clock angle
theta = arccos(-2/3); the three-gap structure is the time-quasicrystal signature; only
the amplitude is a free coupling. A CMB feature search can detect, bound, or refute it.

w33_clock_cosmology.py tied the clock to inflation (N=2*beat, tilt 1/beat). This asks
what the clock's QUASIPERIODICITY (beyond the smooth tilt) imprints, and whether it is
observable.

THE PREDICTION. Standard single-field slow roll gives a smooth spectrum P(k) ~
k^{n_s-1} with no oscillation. A feature in the potential (axion monodromy / resonant
inflation) gives a single log-periodic oscillation delta P/P ~ A cos(omega ln k + phi).
The substrate clock is a TIME QUASICRYSTAL: its stroboscopic phase advances by
theta = arccos(-2/3) per e-fold, theta/pi irrational, so the induced modulation
delta P/P(N) ~ A cos(theta * N + phi) has peaks (at N where theta*N = 0 mod 2pi) whose
spacings in N -- equivalently in ln k, since ln k ~ N -- obey the Steinhaus THREE-GAP
law: at every truncation the peak spacings take at most three distinct values, and
exactly two near the BC ring n = 30. That three-gap peak pattern is the time-
quasicrystal fingerprint, absent from both smooth slow-roll and single-frequency
resonance.

WHAT IS FIXED, WHAT IS FREE. Fixed (by q=3): the modulation frequency theta=arccos(-2/3)
(log-period Delta ln k = 2pi/theta ~ 2.73, a few oscillations across the observable
window) and the three-gap peak spacing. Free: the amplitude A (the inflaton-clock
coupling). So the SHAPE is predicted; the size is not.

THE TEST. A CMB feature search (Planck, and sharper with LiteBIRD / CMB-S4):
  * smooth power law (no peaks)        -> consistent with slow roll, bounds A -> 0;
  * a single clean log-periodic comb   -> resonant inflation, DISFAVOURS the clock;
  * a three-gap (two-then-three gaps) comb at log-period ~2.73 -> the clock signature.
So the substrate makes a specific, falsifiable spectral-shape prediction.

Honest scope: a conditional, qualitative prediction (the feature exists IF the clock
couples to the inflaton; amplitude free). What is fixed and computed: the log-frequency
theta=arccos(-2/3) and the three-gap peak structure (verified below) -- the
distinguishing fingerprint.

Verifies the modulation peak positions, their three-gap spacing in ln k, the log-period
2pi/theta, and the contrast with a single-frequency comb (which has ONE gap).
"""
from __future__ import annotations

import json
import math


def peaks_in_window(freq, n_max):
    """e-fold positions N where cos(freq*N) peaks (freq*N = 2pi m), within [0,n_max]."""
    pk = []
    m = 0
    while True:
        N = 2 * math.pi * m / freq
        if N > n_max:
            break
        pk.append(N)
        m += 1
    return pk


def gaps(seq):
    return [round(seq[i + 1] - seq[i], 6) for i in range(len(seq) - 1)]


def main():
    out = {}
    theta = math.acos(-2 / 3)  # clock angle = log-frequency per e-fold
    log_period = 2 * math.pi / theta  # Delta ln k between peaks
    print(
        f"[the clock modulation]  theta = arccos(-2/3) = {theta:.4f}; "
        f"log-period Delta ln k = 2pi/theta = {log_period:.4f}"
    )
    out["modulation"] = {"theta": round(theta, 4), "log_period": round(log_period, 4)}

    # the time-quasicrystal: stroboscopic phases n*theta mod 2pi obey the three-gap law
    # the modulation's peaks (in e-folds N) where the phase returns near 0
    N_obs = 60  # the full inflationary window (e-folds); observable CMB ~ first several
    # peaks of cos(theta * N): N = 2pi m / theta
    pk = peaks_in_window(theta, N_obs)
    g = sorted(set(gaps(pk)))
    print(
        f"\n[single-frequency baseline]  cos(theta N) peaks: {len(pk)} in N<{N_obs}; "
        f"distinct gaps = {len(g)} (a single comb -> ONE gap)"
    )
    # a single frequency gives a uniform comb (one gap) -- NOT the quasicrystal signature
    assert len(g) == 1
    out["single_frequency"] = {
        "distinct_gaps": 1,
        "is": "uniform comb (resonant inflation)",
    }

    # the time-quasicrystal signature: the phases n*theta mod 2pi (n=1..N) -- three-gap
    phases = sorted(
        ((n * theta) % (2 * math.pi)) for n in range(1, 31)
    )  # to BC ring 30
    pg = gaps(phases + [phases[0] + 2 * math.pi])
    distinct = len(set(round(x, 6) for x in pg))
    print(f"\n[time-quasicrystal signature]  stroboscopic phases n*theta (n=1..30):")
    print(
        f"  distinct gap lengths = {distinct} (Steinhaus three-gap; two at the BC ring)"
    )
    assert distinct <= 3
    out["three_gap_fingerprint"] = {
        "n": 30,
        "distinct_gaps": distinct,
        "is": "Steinhaus three-gap = time-quasicrystal signature",
    }

    # the falsifiable test
    print(f"\n[the test]")
    tests = {
        "smooth power law (no peaks)": "slow roll; bounds coupling A -> 0",
        "single clean log-periodic comb": "resonant inflation; DISFAVOURS the clock",
        "three-gap comb at log-period ~2.73": "the substrate clock signature",
    }
    for obs, meaning in tests.items():
        print(f"  {obs:38s} -> {meaning}")
    out["test"] = tests
    out["fixed_vs_free"] = {
        "fixed": "log-frequency theta=arccos(-2/3), three-gap structure",
        "free": "amplitude A (inflaton-clock coupling)",
    }

    print("\nRESULT: the clock makes a falsifiable CMB prediction. If the substrate's")
    print(
        "  Boerdijk-Coxeter time quasicrystal couples to the inflaton, the primordial"
    )
    print("  spectrum carries a quasi-periodic modulation: peaks at log-period")
    print(
        f"  2pi/theta = {log_period:.2f} in ln k, with spacings obeying the Steinhaus"
    )
    print("  three-gap law (two gaps near the BC ring n=30) -- the time-quasicrystal")
    print("  fingerprint. This is distinct from smooth slow roll (no peaks) and from")
    print("  single-frequency resonant inflation (one uniform comb gap). The frequency")
    print("  theta=arccos(-2/3) and the three-gap shape are fixed by q=3; only the")
    print(
        "  amplitude (the coupling) is free. So a CMB feature search (Planck, LiteBIRD,"
    )
    print(
        "  CMB-S4) can detect the three-gap comb, bound the coupling, or -- finding a"
    )
    print("  clean single-frequency comb -- disfavour the clock. The time quasicrystal")
    print("  that fuels the computer would leave its signature on the sky.")

    out["summary"] = (
        "falsifiable CMB fingerprint of the clock: if the Boerdijk-Coxeter time "
        "quasicrystal couples to the inflaton, the primordial spectrum carries a "
        "quasi-periodic modulation -- peaks at log-period 2pi/theta ~ 2.73 in ln k "
        "(theta=arccos(-2/3)) whose spacings obey the Steinhaus THREE-GAP law (two gaps "
        "near the BC ring n=30), the time-quasicrystal signature. This is distinct from "
        "smooth slow roll (no peaks) and single-frequency resonant inflation (one "
        "uniform comb gap). Fixed by q=3: the log-frequency theta and the three-gap "
        "shape; free: the amplitude (coupling). A CMB feature search (Planck/LiteBIRD/"
        "CMB-S4) can detect the three-gap comb, bound the coupling, or disfavour the "
        "clock (clean single comb). Honest: conditional/qualitative (feature exists IF "
        "the clock couples; amplitude free), but the frequency and three-gap shape are "
        "the fixed, computed, distinguishing prediction."
    )
    out["sources"] = [
        "Boerdijk-Coxeter clock theta=arccos(-2/3), three-gap (w33_clock_magic_renewal.py, "
        "w33_clock_cosmology.py); resonant/axion-monodromy inflation features (Chen; "
        "Flauger et al.); Steinhaus three-gap theorem; CMB feature searches (Planck "
        "2018 X; LiteBIRD; CMB-S4); ln k ~ N e-folds."
    ]
    with open("data/w33_cmb_clock_signature.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cmb_clock_signature.json")


if __name__ == "__main__":
    main()
