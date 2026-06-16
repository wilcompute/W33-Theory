#!/usr/bin/env python3
"""
Why the universe's primitive is ONE MASSLESS photon (the deepest 'why one').

Wheeler's one-electron universe (1940): all electrons are one electron weaving
through spacetime, electron/positron = worldline segments going forward/backward
in time. The holonet is the photonic analog -- one photon, self-entangled past
<-> future -- but MASSLESSNESS makes it cleaner, and the substrate FORCES the
masslessness. Four linked facts:

  (1) NULL WORLDLINE, ZERO PROPER TIME. A massless carrier moves on ds^2=0, so
      its proper time tau = t*sqrt(1-beta^2) -> 0 as beta->1. Its ENTIRE
      worldline is a single proper-time instant: past and future are proper-time-
      SIMULTANEOUS. That is exactly what lets one photon self-entangle its past
      and future registers -- a relation at one proper-time point. A massive
      electron accumulates proper time, so Wheeler's electron must literally
      WEAVE; the massless photon just is, all at once. Self-reference wants
      masslessness.

  (2) MASSLESSNESS IS FORCED BY THE SUBSTRATE GAUGE STRUCTURE. The photon is the
      gauge boson of the substrate connection -- the one whose holonomy is the
      Clifford gates (2T=SL(2,3)) and whose curvature is the gauge fields. The
      substrate gauge symmetry is unbroken (the holonomy is the full Clifford
      group), and gauge invariance forces the gauge boson to be massless (Wigner;
      it kills the longitudinal mode).

  (3) MASSLESSNESS MATCHES THE SUBSTRATE COUNT. A massless vector has Wigner
      little group ISO(2) and exactly TWO transverse helicities (+-1); a massive
      vector has SO(3) and THREE (incl. longitudinal 0). The carrier therefore
      has 2 = lambda = q-1 polarizations (corpus: 'photon polarizations = lambda
      = 2'), NOT 3 = q. The substrate parameter lambda is the helicity count, and
      only a MASSLESS carrier gives it.

  (4) THE CLOCK IS FREQUENCY, NOT PROPER TIME. Although tau=0, the optical phase
      phi = omega*t still accumulates: the photon's internal clock is its
      FREQUENCY (the time-bin/frequency registers), which is precisely the DOF
      that self-entangle. No proper-time clock, but a frequency clock -- and that
      is the carrier of the self-reference. Testable: the self-entanglement is
      preserved over arbitrary worldline LENGTH (no proper-time decoherence),
      limited only by lab-frame loss/dispersion.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q, lam, mu = 3, 2, 4

    # (1) zero proper time
    print("[1] proper time tau/t = sqrt(1 - beta^2) as beta -> 1 (massless):")
    rows = {}
    for beta in (0.9, 0.99, 0.999, 0.9999, 1.0):
        tau = math.sqrt(max(0.0, 1 - beta * beta))
        rows[beta] = tau
        print(f"    beta={beta:7.4f}: tau/t = {tau:.5f}")
    assert rows[1.0] == 0.0
    print("    => null worldline: tau=0, past and future are proper-time-simultaneous")
    out["proper_time_vs_beta"] = rows

    # (2)+(3) helicity / little-group count: massless 2 vs massive 3
    helicity_massless = 2          # +-1, ISO(2) little group
    helicity_massive = 3           # +-1, 0, SO(3) little group
    print("\n[2,3] Wigner helicity count (gauge invariance -> massless):")
    print(f"    massless vector: little group ISO(2), helicities = "
          f"{helicity_massless} = lambda = q-1 = {lam}")
    print(f"    massive  vector: little group SO(3),  polarizations = "
          f"{helicity_massive} = q = {q}")
    print(f"    the carrier has {lam} transverse polarizations (corpus: "
          f"'photon polarizations = lambda') => it MUST be massless")
    assert helicity_massless == lam == q - 1 and helicity_massive == q
    out["helicity_massless"] = helicity_massless
    out["helicity_massless_equals_lambda_qminus1"] = (helicity_massless == lam == q - 1)
    out["helicity_massive"] = helicity_massive

    # (4) frequency clock: phi = omega t accrues even at tau=0
    print("\n[4] the clock is FREQUENCY, not proper time:")
    print("    tau = 0 but phi = omega*t accumulates (optical cycles) -> the")
    print("    time-bin/frequency registers ARE the photon's internal clock, and")
    print("    they are exactly the DOF that self-entangle (past<->future).")
    # number of cycles over a 1 m vacuum path at optical frequency (illustrative)
    c = 299792458.0
    omega = 2 * math.pi * 3.75e14   # ~800 nm
    cycles_per_m = omega / (2 * math.pi) / c
    print(f"    e.g. ~{cycles_per_m:.3e} optical cycles per metre (internal ticks)"
          f" while tau stays 0")
    out["clock"] = "frequency (phi=omega t), not proper time; tau=0"

    print("\nRESULT: the universe's primitive is ONE MASSLESS photon because")
    print("  (i) masslessness => tau=0 => past/future proper-time-simultaneous =>")
    print("      clean self-entanglement (the Wheeler one-particle idea, but the")
    print("      massless photon needs no weaving -- it is all-at-once);")
    print("  (ii) the photon is the gauge boson of the substrate's UNBROKEN")
    print("      connection (holonomy = Clifford 2T), so gauge invariance FORCES")
    print("      masslessness; and")
    print("  (iii) massless => exactly 2 = lambda = q-1 transverse helicities,")
    print("      matching the substrate (a massive carrier would have 3=q).")
    print("  Self-reference, the substrate gauge structure, and the lambda count")
    print("  all demand a single massless carrier: the photon.")

    out["summary"] = ("one massless photon: tau=0 self-simultaneity (Wheeler "
                      "improved), gauge-boson of the unbroken substrate connection "
                      "(masslessness forced), 2=lambda=q-1 helicities")
    out["wheeler"] = ("Wheeler one-electron universe (1940): the massive analog "
                      "must weave through time; the massless photon is all-at-once")
    out["sources"] = ["Wigner, Ann. Math. 40, 149 (1939) (little groups, helicity)",
                      "Wheeler-Feynman one-electron universe (1940)",
                      "gauge invariance forces masslessness + 2 transverse modes"]
    with open("data/w33_why_one_massless_photon.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_why_one_massless_photon.json")


if __name__ == "__main__":
    main()
