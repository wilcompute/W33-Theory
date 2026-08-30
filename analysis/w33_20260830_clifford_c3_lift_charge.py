#!/usr/bin/env python3
"""Classify the order-3 restrictions of the nonsplit central C3 Clifford cover.

Input is the exact 648->216 lift-order certificate produced by
w33_20260829_clifford_c3_circuit_cover.py.  For q of order 3 in Q=K/Z and any
lift g in K, the cube g^3 lies in Z=C3 and is independent of the chosen lift.
The lift-order census therefore determines whether the restriction over <q>
is the split group C3 x C3 or the nonsplit cyclic group C9.

The audit derives:
  * 80 order-3 quotient elements, hence 40 cyclic C3 subgroups;
  * 32 split-oriented elements -> 16 split C3 subgroups;
  * 48 nonsplit-oriented elements -> 24 nonsplit C3 subgroups;
  * after choosing z in Z, inversion pairs force the 48 nonzero charges to
    split 24 with g^3=z and 24 with g^3=z^2.

Thus the central extension class restricts nontrivially to exactly 24/40=3/5
of the order-3 cyclic subgroups of the projective one-qutrit Clifford quotient.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json"
OUT = ROOT / "data/PART_W33_20260830_CLIFFORD_C3_LIFT_CHARGE.json"


def main():
    d = json.loads(IN.read_text())
    assert d["status"] == "PASS"
    ext = d["centralExtension"]
    assert ext["center"] == "C3"
    assert (ext["orderK"], ext["orderQuotient"], ext["split"]) == (648, 216, False)

    patterns = {
        (r["quotientOrder"], tuple(r["liftOrders"])): r["elements"]
        for r in d["cocycleWitness"]["liftOrderPatterns"]
    }
    split_elements = patterns[(3, (3, 3, 3))]
    nonsplit_elements = patterns[(3, (9, 9, 9))]
    assert (split_elements, nonsplit_elements) == (32, 48)

    # Every cyclic subgroup of order 3 has exactly two nonidentity generators.
    order3_elements = split_elements + nonsplit_elements
    assert order3_elements == 80
    assert split_elements % 2 == nonsplit_elements % 2 == 0
    split_subgroups = split_elements // 2
    nonsplit_subgroups = nonsplit_elements // 2
    total_subgroups = split_subgroups + nonsplit_subgroups
    assert (split_subgroups, nonsplit_subgroups, total_subgroups) == (16, 24, 40)

    # For q of order 3, pi^{-1}(<q>) has order 9.  If one/all lifts have order
    # 3 it has exponent 3 and is C3xC3.  If one/all lifts have order 9 it is C9.
    # The charge omega(q)=g^3 in Z is lift-independent because
    # (g z^a)^3 = g^3 z^(3a) = g^3 for central z of order 3.
    # Also omega(q^{-1})=omega(q)^{-1}.  The two generators of each nonsplit
    # C3 subgroup therefore carry opposite nonzero charges, forcing 24+24.
    charge_z = nonsplit_elements // 2
    charge_z2 = nonsplit_elements // 2
    assert (charge_z, charge_z2) == (24, 24)

    out = {
        "schema": "w33.20260830.clifford-c3-lift-charge.v1",
        "status": "PASS",
        "inputCertificate": IN.name,
        "extension": {
            "kernel": "C3",
            "orderK": 648,
            "orderQ": 216,
            "quotient": ext["quotient"],
            "globallySplit": False,
        },
        "liftCharge": {
            "definition": "for q of order 3 and any lift g, omega(q)=g^3 in Z=C3",
            "liftIndependent": True,
            "inversionLaw": "omega(q^-1)=omega(q)^-1",
            "zeroChargeOrder3Elements": split_elements,
            "nonzeroChargeOrder3Elements": nonsplit_elements,
            "afterChoosingCentralGenerator": {"charge_z": charge_z, "charge_z^2": charge_z2},
        },
        "order3Restrictions": {
            "order3Elements": order3_elements,
            "cyclicC3Subgroups": total_subgroups,
            "splitC3xC3Preimages": split_subgroups,
            "nonsplitC9Preimages": nonsplit_subgroups,
            "nontrivialRestrictionFraction": "24/40 = 3/5",
        },
        "cohomology": {
            "localGroup": "H^2(C3,C3) ~= C3 for the central/trivial action",
            "splitRestrictionClass": "0",
            "nonsplitRestrictionClass": "nonzero; its full preimage is C9",
            "statement": "The global extension class restricts nontrivially to exactly 24 of the 40 cyclic order-3 subgroups of Q.",
        },
        "theorem": "The nonsplit 648->216 Clifford extension is locally detected on 3/5 of the order-3 cyclic subgroups: 16 lift to C3xC3 and 24 lift to C9. The 48 nonsplit oriented generators carry the two nonzero central cube charges in an exact 24+24 inversion-paired split.",
        "boundary": "This is an exact finite-group/cohomology statement derived from the certified lift-order census. The C3 charge is an extension/deck charge; identifying it with a measured optical phase requires an additional physical intertwiner.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "order3Subgroups": total_subgroups,
        "split": split_subgroups,
        "nonsplit": nonsplit_subgroups,
        "nonzeroCharges": [charge_z, charge_z2],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
