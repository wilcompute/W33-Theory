#!/usr/bin/env python3
"""
The substrate's falsifiability ledger: every sharp, near-term prediction with the
experiment that settles it and the value that kills the theory.

A theory of everything is only worth the experiments that can refute it. This
consolidates the sharp predictions accumulated across the program -- cosmology,
neutrinos, dark matter, colliders, and the TABLETOP demonstrator -- into one
decision table. Each row is a number, an experiment, an era, and a falsifier.
"""
from __future__ import annotations

import json

# (observable, substrate value, experiment, ~era, falsified if)
LEDGER = [
    ("n_s", "29/30 = 0.9667", "Planck (done)", "now", "outside 0.9649 +- 0.0042"),
    (
        "r (tensor/scalar)",
        "1/300 = 0.0033",
        "LiteBIRD/CMB-S4",
        "~2030",
        "r > 0.01 or null at 1e-3",
    ),
    ("f_NL^local", "1/72 = 0.0139", "CMB-S4/LiteBIRD", "~2030", "|f_NL| >> 1"),
    (
        "running dn_s/dlnk",
        "-1/1800 = -5.6e-4",
        "CMB-S4",
        "~2032",
        "outside -2/N^2 band",
    ),
    (
        "m_betabeta (0nubb)",
        "~2.3 meV",
        "nEXO/LEGEND-1000",
        "~2030s",
        "NH excluded / m_bb too big",
    ),
    (
        "Sum m_nu",
        "58 meV (NH)",
        "DESI + CMB-S4",
        "~2028",
        "inverted ordering or > 0.1 eV",
    ),
    ("delta_CP (PMNS)", "14pi/13 ~ 194 deg", "DUNE/HK", "~2030", "far from 194 deg"),
    (
        "dark matter",
        "confining SU(4) hadron, tens of GeV",
        "LZ/XENONnT",
        "~2028",
        "WIMP-like signal at 308 GeV / null",
    ),
    (
        "dark-confinement GW",
        "LISA-band peak ~1e-4 Hz",
        "LISA",
        "~2035",
        "no stochastic background there",
    ),
    ("2nd Higgs scalar", "~3.2 TeV / ~159 GeV", "HL-LHC", "~2029+", "no resonance"),
    ("proton lifetime", "~1e37 yr", "Hyper-K", "~2030s", "decay seen below 1e35"),
    (
        "DEMONSTRATOR pump",
        "Chern C = lambda = 2 (quantized)",
        "tabletop photonics",
        "NOW",
        "pump quantum != 2",
    ),
    (
        "DEMONSTRATOR context",
        "contextual fraction = 1/Phi_4 = 1/10",
        "tabletop photonics",
        "NOW",
        "CF != 1/10",
    ),
    (
        "DEMONSTRATOR clock",
        "BC angle arccos(-2/3) = 131.8 deg",
        "tabletop photonics",
        "NOW",
        "beat angle != arccos(-2/3)",
    ),
]


def main():
    out = {}
    print("[substrate falsifiability ledger]\n")
    hdr = f"  {'observable':24s} {'value':30s} {'experiment':18s} {'era':6s}"
    print(hdr)
    print("  " + "-" * 84)
    for obs, val, exp, era, fal in LEDGER:
        print(f"  {obs:24s} {val:30s} {exp:18s} {era:6s}")
    out["ledger"] = [
        {"observable": o, "value": v, "experiment": e, "era": era, "falsified_if": f}
        for o, v, e, era, f in LEDGER
    ]

    now = [r for r in LEDGER if r[3] == "now" or r[3] == "NOW"]
    n_demo = sum(1 for r in LEDGER if r[0].startswith("DEMONSTRATOR"))
    print(f"\n  total sharp predictions: {len(LEDGER)}")
    print(
        f"  testable NOW (incl. {n_demo} tabletop demonstrator measurements): "
        f"{len(now)}"
    )
    print(f"  decisive era: ~2028-2035 (CMB-S4, LiteBIRD, nEXO, DUNE, LISA, HL-LHC)")
    out["n_predictions"] = len(LEDGER)
    out["n_demonstrator"] = n_demo
    assert len(LEDGER) >= 12 and n_demo == 3

    print("\nRESULT: the substrate program is falsifiable on a definite timetable.")
    print("  Beyond the already-matched n_s, it stakes itself on tiny, sharp numbers")
    print("  -- r = 1/300, f_NL = 1/72, running = -1/1800, m_betabeta = 2.3 meV,")
    print("  delta_CP = 194 deg, a tens-of-GeV confining dark hadron, and a dark-")
    print("  confinement GW peak in the LISA band -- each killable by a named")
    print("  experiment in 2028-2035. Crucially, THREE predictions are testable on")
    print("  the tabletop holonet demonstrator RIGHT NOW: the quantized pump Chern")
    print("  C = lambda = 2, the contextual fraction 1/Phi_4 = 1/10, and the BC clock")
    print("  angle arccos(-2/3). The machine we are building is itself an experiment")
    print("  on the theory of everything.")

    out["summary"] = (
        "falsifiability ledger: ~14 sharp predictions, each with "
        "experiment+era+falsifier; cosmology (r=1/300, f_NL=1/72, "
        "running=-1/1800), neutrinos (m_bb=2.3 meV, Sum=58 meV, "
        "delta_CP=194), dark matter (confining SU(4) hadron + LISA GW), "
        "colliders (2nd Higgs, proton decay), and 3 NOW-testable "
        "demonstrator measurements (pump C=lambda=2, CF=1/10, BC angle "
        "arccos(-2/3)). Decisive era 2028-2035."
    )
    out["sources"] = [
        "consolidation of w33 cosmology/neutrino/dark witnesses + the "
        "demonstrator (w33_demonstrator_measures_substrate.py); CMB-S4/"
        "LiteBIRD/nEXO/DUNE/LISA/HL-LHC reach"
    ]
    with open("data/w33_falsifiability_ledger.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_falsifiability_ledger.json")


if __name__ == "__main__":
    main()
