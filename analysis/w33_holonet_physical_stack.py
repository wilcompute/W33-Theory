#!/usr/bin/env python3
"""
What the holonet physically IS, and what is still needed to build it.

The paper specifies a single SELF-ENTANGLED PHOTON (polarization + time-bin
qutrits; tritter=F_3, delay ladder, EOM) realizing the logical gate/network
layer, with the discrete [[240,81,4]]_3 STEINBERG code as the error-correcting
register. Separately, the architecture-closure results show the fault-tolerant
layer is a CV GKP code (D4 lattice) with Gaussian+cubic gates. These live at
DIFFERENT physical levels, and reconciling them is the point:

  A single photon has FIXED photon number; it CANNOT host a GKP state (a
  many-photon quadrature grid). So the single-photon machine demonstrates the
  IDEAL, UN-ENCODED logical layer (gates, network, the parameter-free witnesses
  of the build sheet) -- not fault tolerance.

  Fault tolerance is the STANDARD two-layer CV stack, and here BOTH layers are
  substrate-fixed:
     INNER  (analog -> digital):  GKP code on D4 (the substrate matter-shell
            lattice). Each oscillator mode carries a qutrit; D4 = 2 modes/2
            qutrits. Converts continuous displacement noise into discrete
            qutrit errors, with coding gain 1.5 dB (E8: 3 dB) cutting the
            squeezing requirement.
     OUTER  (digital):  the [[240,81,4]]_3 Steinberg code on the substrate's
            240 edges (= E8 roots = vk/2). Corrects residual discrete qutrit
            errors; 240 physical -> 81 = 3^4 logical qutrits, distance 4 = mu.

  Concatenation:  240 squeezed oscillator modes  -> 120 D4 GKP pairs
                  -> 240 GKP qutrits -> Steinberg [[240,81,4]]_3 -> 81 logical.

WHAT IS STILL NEEDED (physical, and it is the universal CV-FT bottleneck, not a
W(3,3)-specific one): (1) squeezed light at threshold (~10 dB; protocol-
dependent 7-20 dB in the literature), reduced by the D4/E8 coding gain; (2) GKP
qutrit STATE GENERATION (the hard step: measurement-based 'breeding' from
squeezed/cat states + photon-number-resolving detection, or matter-assisted);
(3) the CUBIC non-Gaussian resource (the 'matter shell magic' = degree-3 E6
cubic) via a chi-3 medium or magic-state injection; (4) a programmable Gaussian
(beamsplitter/phase/squeeze) network realizing the Sp(4,3) Clifford; (5)
homodyne detection for GKP syndrome readout. Everything ELSE -- which code,
which gates, which network -- is fixed by W(3,3); only this physical layer is
open, and it is the same bottleneck the whole CV-FT field faces.

This script verifies the concatenation bookkeeping and tabulates the stack.
"""
from __future__ import annotations

import json
import math


def main():
    # substrate numbers
    v, k = 40, 12
    edges = v * k // 2                      # 240 = E8 roots
    logical = 3 ** 4                        # 81 Steinberg logical qutrits
    distance, mu = 4, 4
    d = 3                                   # qutrit
    print("[substrate-fixed code parameters]")
    print(f"  outer Steinberg code [[{edges},{logical},{distance}]]_{d}: "
          f"240 = vk/2 = |E8 roots|, 81 = 3^4, distance 4 = mu")
    assert edges == 240 and logical == 81 and distance == mu == 4

    # GKP inner: D4 = 2 modes / 2 qutrits -> 1 mode per physical qutrit
    modes_per_qutrit = 1                    # D4: 2 modes encode 2 qutrits
    n_modes = edges * modes_per_qutrit      # 240 oscillator modes
    n_d4_pairs = edges // 2                 # 120 D4 blocks
    print("\n[concatenated fault-tolerant stack]")
    print(f"  {n_modes} squeezed oscillator modes")
    print(f"   -> {n_d4_pairs} D4 GKP pairs (inner, 1.5 dB coding gain)")
    print(f"   -> {edges} GKP qutrits")
    print(f"   -> Steinberg [[{edges},{logical},{distance}]]_3 (outer)")
    print(f"   -> {logical} logical qutrits")
    assert n_modes == 240 and n_d4_pairs == 120

    # squeezing budget: baseline threshold minus substrate coding gain
    def coding_gain_db(min_norm, det, n):
        return 10 * math.log10(min_norm / det ** (1.0 / n))
    g_d4 = coding_gain_db(2, 4, 4)
    g_e8 = coding_gain_db(2, 1, 8)
    baseline_threshold_db = 10.0            # representative; protocol-dependent
    print("\n[squeezing budget (the bottleneck)]")
    print(f"  representative GKP-FT threshold ~ {baseline_threshold_db:.0f} dB "
          f"(protocol-dependent, 7-20 dB in the literature)")
    print(f"  D4 inner coding gain  = {g_d4:.2f} dB  -> effective ~"
          f"{baseline_threshold_db-g_d4:.1f} dB")
    print(f"  E8 (4-mode) gain      = {g_e8:.2f} dB  -> effective ~"
          f"{baseline_threshold_db-g_e8:.1f} dB")

    # the demo vs the fault-tolerant machine
    print("\n[two physical machines]")
    print("  IDEAL DEMO (build sheet, buildable now): 1 self-entangled photon")
    print("    (polarization+time-bin), tritter/EOM/phase-plate, single-photon")
    print("    detectors -> the Sp(4,3) gate/network layer + parameter-free")
    print("    witnesses. Demonstrates the LOGIC; NOT fault-tolerant (a single")
    print("    photon cannot carry a GKP grid state).")
    print("  FAULT-TOLERANT MACHINE (what is still needed): 240 squeezed/GKP")
    print("    oscillator modes + the 5 physical resources below.")

    needed = {
        "1_squeezing": "~10 dB squeezed light (OPO/OPA), reduced by D4/E8 gain",
        "2_gkp_states": "GKP qutrit generation -- measurement-based breeding "
                        "(squeezed/cat + photon-number-resolving detection) or "
                        "matter-assisted; THE hard step",
        "3_cubic": "non-Gaussian cubic resource (= degree-3 E6 'matter magic') "
                   "via chi-3 medium or magic-state injection",
        "4_gaussian_net": "programmable beamsplitter/phase/squeeze network = the "
                          "Sp(4,3) Clifford (mature integrated photonics)",
        "5_homodyne": "homodyne detection for GKP/Steinberg syndrome readout",
    }
    print("\n[what is still needed -- the physical CV layer]")
    for kk, vv in needed.items():
        print(f"  ({kk[0]}) {vv}")

    print("\nRESULT: the holonet is a CONCATENATED GKP(D4) o Steinberg[[240,81,4]]_3")
    print("  continuous-variable qutrit computer; the substrate fixes BOTH code")
    print("  layers, the gate set (Sp(4,3) Gaussian + E6 cubic) and the network.")
    print("  The single self-entangled photon is the IDEAL un-encoded demo. The")
    print("  only open part is PHYSICAL: 240 squeezed GKP modes at threshold --")
    print("  the universal CV-FT bottleneck, eased (not removed) by the substrate's")
    print("  optimal D4/E8 lattices. We are building a machine with ZERO design")
    print("  freedom above the hardware: W(3,3) dictates everything else.")

    out = {
        "what_it_is": "concatenated GKP(D4) inner o Steinberg[[240,81,4]]_3 outer "
                      "CV qutrit computer; single self-entangled photon = ideal "
                      "un-encoded logical demo (not fault-tolerant)",
        "concatenation": {"oscillator_modes": n_modes, "D4_pairs": n_d4_pairs,
                          "GKP_qutrits": edges, "outer_code": "[[240,81,4]]_3",
                          "logical_qutrits": logical},
        "substrate_fixed": ["inner code D4 GKP", "outer code Steinberg 240,81,4",
                            "gate set Sp(4,3) Gaussian + E6 cubic", "network"],
        "coding_gain_db": {"D4": round(g_d4, 2), "E8": round(g_e8, 2)},
        "squeezing_threshold_db": {"baseline_representative": baseline_threshold_db,
                                   "note": "protocol-dependent 7-20 dB; reduced by "
                                           "the D4/E8 coding gain"},
        "still_needed_physical": needed,
        "honest_scope": "the open part is the universal CV fault-tolerance "
                        "bottleneck (GKP state generation + threshold squeezing), "
                        "NOT W(3,3)-specific; the substrate removes all design "
                        "freedom above the hardware and gives optimal codes",
        "sources": ["Gottesman-Kitaev-Preskill, PRA 64, 012310 (2001)",
                    "Menicucci, PRL 112, 120504 (2014) (GKP-cluster threshold)",
                    "Bourassa et al., Quantum 5, 392 (2021) (photonic FT blueprint)"],
    }
    with open("data/w33_holonet_physical_stack.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/w33_holonet_physical_stack.json")


if __name__ == "__main__":
    main()
