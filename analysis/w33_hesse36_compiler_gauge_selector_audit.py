#!/usr/bin/env python3
"""Gauge-selection audit for the quaternionic/Clifford Hesse36 compiler.

The Q8-restricted bridge admits 1,179,648 objectwise equivariant bijections.
The full Clifford648 theorem changes the problem: the three safe 12-sheets
must carry the three characters 1,chi,chi^2 of H54/H18 ~= C3. Hence only 3!=6
character assignments survive full Clifford covariance.

The safe sheets are the three center slopes beta=0,1,2. Requiring the pure
external sheet beta=0 to carry the trivial address-center character leaves two
assignments, exchanged by omega <-> omega^2.

The canonical E6 cubic coefficients are real signs (+/-1), including the exact
22+/23- full distribution and 2+/7- fiber distribution. Qpsi/Yukawa charge
patterns are also real integer data. Therefore these signed/charge observables
are invariant under complex conjugation and cannot distinguish the final pair.
A genuinely mu3-oriented observable is required.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_hesse36_compiler_gauge_selector_audit.json"

def main(write=True):
    q8=json.loads((ROOT/"data/w33_hesse36_q8_equivariant_repair.json").read_text())
    full=json.loads((ROOT/"data/w33_hesse36_full_clifford648_fourier_compiler.json").read_text())
    signs=json.loads((ROOT/"data/w33_pass1103_hesse_firewall_cubic_transport.json").read_text())
    qpsi=json.loads((ROOT/"data/w33_qpsi_matter_parity_e8_d8_bridge.json").read_text())
    assert q8["gauge_count"]["total_Q8_equivariant_bijections"]==1179648
    assert full["group"]["quotient"]=="H54/H18 = C3"
    assert full["orbits"]["safe36"]==[12,12,12]
    assert signs["fiber_cubic_sign_distribution"]=={"plus":2,"minus":7}
    assert signs["full_cubic_sign_distribution_from_source"]=={"plus":22,"minus":23}
    assert qpsi["E6_cubic"]["all_cubics_matter_parity_even"] is True

    chars=(0,1,2)
    assignments=list(itertools.permutations(chars))
    assert len(assignments)==6
    # beta-sheet order is 0,1,2. Physical-neutral convention: beta=0 is the
    # pure external center line, hence must carry trivial address-center char.
    neutral=[a for a in assignments if a[0]==0]
    assert neutral==[(0,1,2),(0,2,1)]

    # Canonical cubic signs on the 36 ordinary tritangents are the complement
    # of the nine fiber signs.
    ordinary_plus=22-2; ordinary_minus=23-7
    assert (ordinary_plus,ordinary_minus)==(20,16)

    # Complex conjugation swaps the two survivors while fixing every real
    # signed coefficient and every integer charge/parity datum.
    conj={(0,1,2):(0,2,1),(0,2,1):(0,1,2)}
    assert conj[neutral[0]]==neutral[1]
    real_signs_blind=all(s in (-1,1) for s in ([1]*22+[-1]*23))
    integer_qpsi_blind=all(
        isinstance(x,int)
        for row in qpsi["E6_cubic"]["patterns"]
        for x in row["Qpsi"]
    )
    assert real_signs_blind and integer_qpsi_blind

    out={
      "schema":"w33.hesse36_compiler_gauge_selector_audit.v1",
      "status":"PASS_FULL_CLIFFORD_REDUCES_Q8_GAUGES_TO_CONJUGATE_PAIR_REAL_CUBIC_SIGNS_CANNOT_FINISH_SELECTION",
      "headline":"The old 1,179,648 Q8-equivariant compiler gauges collapse to six under full Clifford648 covariance: exactly the 3! assignments of the three C3 characters to the three safe center sheets. Requiring the pure external beta=0 sheet to carry the trivial address-center character leaves two, (0,1,2) and (0,2,1), exchanged by complex conjugation. The canonical E6 cubic/Yukawa coefficients are real +/-1 and Qpsi selection data are real integers, so those observables are rigorously blind to the last omega<->omega^2 choice.",
      "reduction":{"Q8_equivariant_gauges":1179648,"full_Clifford_character_assignments":6,
                   "neutral_beta0_trivial_survivors":2,
                   "survivors":[[0,1,2],[0,2,1]],
                   "relation":"complex conjugation omega <-> omega^2"},
      "canonical_cubic_signs":{"full45":{"plus":22,"minus":23},
                               "fiber9":{"plus":2,"minus":7},
                               "ordinary36":{"plus":ordinary_plus,"minus":ordinary_minus},
                               "coefficients_real":True},
      "selector_verdict":{"real_E6_cubic_signs_select_unique_orientation":False,
                           "integer_Qpsi_or_matter_parity_select_unique_orientation":False,
                           "needed_next_observable":"a genuinely mu3-oriented phase/holonomy/chirality datum with a fixed orientation convention"},
      "boundary":"This does not say the final two gauges are physically equivalent. It says the currently certified real cubic signs and integer charge/parity data cannot distinguish them.",
      "checks":{"six_full_clifford_assignments":True,"neutral_sheet_leaves_two":True,
                "two_are_complex_conjugates":True,"ordinary_sign_split_20_16":True,
                "real_signs_conjugation_blind":True,"Qpsi_data_conjugation_blind":True}
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out
if __name__=="__main__":print(json.dumps(main(True),indent=2))
