#!/usr/bin/env python3
"""
The first milestone, cut loose: a few hundred photons on a tabletop decide whether the substrate is
real. Every falsifiable prediction is only as good as the experiment that could refute it, so this
pass turns the headline prediction into a concrete benchtop protocol with a decision number. The
substrate predicts a contextual fraction CF = 1/10 = 1/Phi_4 (a corpus value): of all measurement
rounds over the 40 Witting bases, a fraction 1/10 violate every non-contextual (classical) value
assignment -- a Kochen-Specker signal that a classical hidden-variable model cannot produce. The
experiment is calibration-free because the expected value is a substrate integer, not a fitted
constant. THE DECISION STATISTIC: distinguishing CF = 1/10 from the classical null CF = 0 is a
one-sided binomial test; to see the 1/10 signal at k sigma requires n >= k^2 p(1-p)/p^2 valid
coincidences, giving n >= 81 for 3 sigma and n >= 225 for 5 sigma. Folding in the optical survival
(78-88 percent from the loss budget) the raw photon budget for a 5 sigma certification is ~256-289
detected events -- minutes on any heralded single-photon source. THE COMPONENTS are all catalog
optics, no cryostat: a heralded SPDC source, one polarizing beam splitter (Stage A, the Witting
spatial Bell state), a symmetric 3-port fiber coupler / tritter plus a three-bin delay ladder and one
electro-optic modulator (Stage B, the temporal Bell qutrit), one Boerdijk-Coxeter loop (a fixed
waveplate at arccos(-2/3)), and four single-photon detectors. THE FALSIFICATION LOGIC is sharp: a
measured violation fraction consistent with 1/10 certifies the q=3 substrate's contextuality (the
magic fuel) with no free parameters; a fraction consistent with 0 refutes the identification. So the
first milestone is decided by a few hundred photons on a bench -- the cheapest possible test of a
candidate theory of everything, and the entry point to the whole architecture.

This designs the minimal benchtop experiment that could refute the substrate, computing the
shot-count decision statistics and listing the catalog-optics component chain.

THE PROTOCOL.
    observable     contextual fraction CF over the 40 Witting bases; substrate value 1/10 = 1/Phi_4.
    null           classical (non-contextual) model: CF = 0.
    decision       one-sided binomial; n >= k^2 p(1-p)/p^2 valid coincidences for a k-sigma signal:
                   n >= 81 (3 sigma), n >= 225 (5 sigma); raw ~256-289 photons at 78-88% survival.
    components     SPDC source; PBS (Stage A); tritter + 3-bin delay + EOM (Stage B); BC loop
                   (arccos(-2/3) waveplate); 4 single-photon detectors. No cryostat.
    falsify        CF ~ 1/10 -> substrate certified (calibration-free); CF ~ 0 -> identification refuted.

Honest scope: the contextual-fraction value 1/10 is a corpus result (the demonstrator/Witting work),
not re-derived here; what is computed here is the DECISION STATISTICS -- the shot counts to certify a
1/10 signal against the classical null at 3 and 5 sigma, with the optical-survival correction -- and
the protocol assembly. The component chain is the corpus demonstrator. So: a concrete, costed
falsification experiment whose decision number is a few hundred photons.

Verifies the binomial shot-count decision statistics (81 at 3 sigma, 225 at 5 sigma, ~256-289 raw
with loss) for certifying the CF = 1/10 substrate signal.
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    p = 1 / 10  # substrate contextual fraction = 1/Phi_4 (corpus value)
    print(
        "== the first milestone: a few hundred photons decide whether the substrate is real =="
    )
    print(
        f"\n[observable]  contextual fraction CF over the 40 Witting bases; substrate value = 1/10 = 1/Phi_4"
    )
    print(f"[null]        classical non-contextual model: CF = 0")

    # decision statistics: one-sided binomial, k-sigma
    shots = {}
    for k in (3, 5):
        n = math.ceil(k**2 * p * (1 - p) / p**2)
        shots[k] = n
        print(
            f"[decision]    {k}-sigma certification: n >= k^2 p(1-p)/p^2 = {n} valid coincidences"
        )
    assert shots[3] == 81 and shots[5] == 225

    raw = {}
    for eta in (0.88, 0.78):
        r = math.ceil(shots[5] / eta)
        raw[eta] = r
        print(
            f"              with optical survival eta = {eta}: raw 5-sigma budget ~ {r} photons"
        )
    assert 250 <= raw[0.88] <= 260 and 285 <= raw[0.78] <= 295

    out["decision"] = {
        "observable": "contextual fraction CF over the 40 Witting bases",
        "substrate_value": "1/10 = 1/Phi_4 (corpus)",
        "null": "CF = 0 (classical non-contextual)",
        "shots_3sigma": shots[3],
        "shots_5sigma": shots[5],
        "raw_photons_5sigma": {str(e): raw[e] for e in raw},
        "test": "one-sided binomial; n >= k^2 p(1-p)/p^2",
    }

    components = [
        "heralded SPDC single-photon source (e.g. ppKTP waveguide)",
        "1 polarizing beam splitter (Stage A: Witting spatial Bell state in C^4)",
        "1 symmetric 3-port fiber coupler (tritter) + three-bin delay ladder + 1 EOM (Stage B: temporal Bell qutrit)",
        "1 Boerdijk-Coxeter loop (fixed waveplate at arccos(-2/3) ~ 131.8 deg)",
        "4 single-photon detectors (SPADs). No cryostat; room temperature.",
    ]
    print("\n[components -- catalog optics, no cryostat]")
    for c in components:
        print(f"  - {c}")
    out["components"] = components

    print(
        "\n[falsification]  CF ~ 1/10 -> q=3 substrate certified (calibration-free, no free parameters);"
    )
    print("                 CF ~ 0   -> the substrate identification is refuted")
    out["falsification"] = {
        "certify_if": "measured CF consistent with 1/10",
        "refute_if": "measured CF consistent with 0",
        "calibration_free": True,
    }

    print(
        "\nRESULT: the first milestone is decided by a few hundred photons on a bench. The substrate"
    )
    print(
        "  predicts a contextual fraction CF = 1/10 = 1/Phi_4: a fraction one-tenth of all rounds over"
    )
    print(
        "  the 40 Witting bases violate every classical (non-contextual) value assignment -- a"
    )
    print(
        "  Kochen-Specker signal no hidden-variable model can fake -- and the expected value is a"
    )
    print(
        "  substrate integer, so the test is calibration-free. Distinguishing 1/10 from the classical"
    )
    print(
        "  null 0 is a one-sided binomial test needing n >= 81 valid coincidences for 3 sigma and 225"
    )
    print(
        "  for 5 sigma; at 78-88% optical survival that is ~256-289 detected photons -- minutes on a"
    )
    print(
        "  heralded source. The rig is all catalog optics with no cryostat: an SPDC source, one PBS,"
    )
    print(
        "  a tritter with a three-bin delay and an EOM, one Boerdijk-Coxeter loop, and four detectors."
    )
    print(
        "  A violation fraction near 1/10 certifies the q=3 substrate's contextuality (the machine's"
    )
    print(
        "  magic fuel) with zero free parameters; a fraction near 0 refutes the identification. This is"
    )
    print(
        "  the cheapest possible test of a candidate theory of everything -- and the entry point to the"
    )
    print(
        "  entire architecture. Honest: the 1/10 value is a corpus result; what is computed here is the"
    )
    print("  shot-count decision statistics and the protocol assembly.")

    out["summary"] = (
        "the first milestone, cut loose: a few hundred photons on a tabletop decide whether the "
        "substrate is real. The substrate predicts a contextual fraction CF = 1/10 = 1/Phi_4 (corpus): "
        "one-tenth of all rounds over the 40 Witting bases violate every classical non-contextual value "
        "assignment (a Kochen-Specker signal), and the expected value is a substrate integer so the "
        "test is calibration-free. Decision statistic: distinguishing CF=1/10 from the classical null "
        "CF=0 is a one-sided binomial test needing n >= k^2 p(1-p)/p^2 valid coincidences -- 81 for 3 "
        "sigma, 225 for 5 sigma; at 78-88% optical survival the raw 5-sigma budget is ~256-289 detected "
        "photons (minutes on a heralded source). Components (catalog optics, no cryostat): SPDC source; "
        "1 PBS (Stage A Witting spatial Bell state); tritter + 3-bin delay + EOM (Stage B temporal Bell "
        "qutrit); 1 Boerdijk-Coxeter loop (arccos(-2/3) waveplate); 4 single-photon detectors. "
        "Falsification: CF ~ 1/10 certifies the q=3 substrate contextuality (the magic fuel) with no "
        "free parameters; CF ~ 0 refutes it. The cheapest possible test of a candidate theory of "
        "everything, and the entry point to the whole architecture. HONEST: the 1/10 contextual-fraction "
        "value is a corpus result (not re-derived here); what is computed here is the shot-count "
        "decision statistics (81/225 valid coincidences, ~256-289 raw photons with loss) and the "
        "protocol assembly."
    )
    out["sources"] = [
        "contextual fraction 1/10 = 1/Phi_4 (corpus demonstrator / Witting work, bt1901/bt1904); "
        "one-sided binomial decision statistics (computed here); optical survival 78-88% (loss budget, "
        "BT1879/1882); demonstrator component chain (SPDC, PBS, tritter, delay, EOM, BC loop, SPADs)."
    ]
    with open("data/w33_demonstrator_experiment.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_demonstrator_experiment.json")


if __name__ == "__main__":
    main()
