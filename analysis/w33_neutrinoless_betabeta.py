#!/usr/bin/env python3
"""
Neutrinoless double beta decay from the 128 seesaw: the cyclotomic PMNS angles plus
the Z3 Majorana phases (120, 240 deg) give m_betabeta ~ 2.3 meV -- a sharp,
near-term-testable prediction -- with the Dirac phase delta_CP = 14 pi / 13.

The dark-128 seesaw (w33_neutrino_seesaw_128.py) fixes the light neutrinos: normal
ordering with the corpus sum Sum m_nu = 58 meV, the cyclotomic mixing angles
    sin^2 th12 = (q+1)/Phi_3 = 4/13,  sin^2 th23 = Phi_6/Phi_3 = 7/13,
    sin^2 th13 = lambda/(Phi_3 Phi_6) = 2/91,
and the Z3-graded Majorana phases alpha21 = 2 pi/3 = 120 deg, alpha31 = 4 pi/3 =
240 deg (the same Z3 that triples the generations). The 0nubb effective mass is
    m_betabeta = | c12^2 c13^2 m1 + s12^2 c13^2 m2 e^{i alpha21}
                   + s13^2 m3 e^{i alpha31} |.
With the NH spectrum (m1 ~ 0, m2 = sqrt(Dm^2_sol), m3 = sqrt(Dm^2_atm)) this gives
m_betabeta ~ 2.3 meV, matching the corpus scorecard value -- testable by nEXO /
LEGEND (few-meV reach). The Dirac CP phase is delta_CP = 14 pi/13 ~ 194 deg
(2 pi Phi_6/Phi_3), the same phase that drives leptogenesis/cogenesis.

Verifies m_betabeta ~ 2.3 meV from the cyclotomic angles + Z3 phases + NH masses.
"""
from __future__ import annotations

import json
import math

# cyclotomic PMNS (corpus)
s12sq, s23sq, s13sq = 4 / 13, 7 / 13, 2 / 91
c12sq, c13sq = 1 - s12sq, 1 - s13sq

# Z3-graded Majorana phases
alpha21 = 2 * math.pi / 3  # 120 deg
alpha31 = 4 * math.pi / 3  # 240 deg
delta_cp_deg = 14 * 180 / 13  # 14 pi/13 in degrees


def main():
    out = {}

    # normal-ordering masses (eV) from the measured splittings
    dm2_sol = 7.5e-5  # eV^2
    dm2_atm = 2.5e-3  # eV^2
    m1 = 0.0
    m2 = math.sqrt(dm2_sol)  # ~8.66 meV
    m3 = math.sqrt(dm2_atm)  # ~50 meV
    sum_mnu_meV = (m1 + m2 + m3) * 1e3
    print(
        f"[NH neutrino masses]  m1~0, m2 = {m2*1e3:.2f} meV, m3 = {m3*1e3:.2f} meV; "
        f"Sum = {sum_mnu_meV:.1f} meV (corpus 58)"
    )
    assert abs(sum_mnu_meV - 58) < 3

    # 0nubb effective mass with Z3 Majorana phases
    term1 = c12sq * c13sq * m1
    term2 = s12sq * c13sq * m2 * complex(math.cos(alpha21), math.sin(alpha21))
    term3 = s13sq * m3 * complex(math.cos(alpha31), math.sin(alpha31))
    m_bb = abs(term1 + term2 + term3) * 1e3  # meV
    print(f"\n[0nubb effective mass]")
    print(
        f"  m_betabeta = |c12^2 c13^2 m1 + s12^2 c13^2 m2 e^(i 120) "
        f"+ s13^2 m3 e^(i 240)|"
    )
    print(
        f"  = {m_bb:.2f} meV   (corpus scorecard 2.3 meV; nEXO/LEGEND reach "
        f"~few meV)"
    )
    assert 1.8 < m_bb < 2.8
    out["m_betabeta_meV"] = round(m_bb, 2)
    out["sum_m_nu_meV"] = round(sum_mnu_meV, 1)

    # Dirac CP phase
    print(
        f"\n[Dirac CP phase]  delta_CP = 14 pi/13 = 2 pi Phi_6/Phi_3 = "
        f"{delta_cp_deg:.0f} deg  (obs ~197 +- 25; T2K/NOvA)"
    )
    print(
        f"  the same CP phase that drives leptogenesis/cogenesis "
        f"(w33_cogenesis.py)."
    )
    out["delta_CP_deg"] = round(delta_cp_deg, 0)
    out["majorana_phases_deg"] = [120, 240]

    print("\nRESULT: the 128 seesaw makes neutrinoless double beta decay a sharp")
    print("  prediction. The cyclotomic PMNS angles (4/13, 7/13, 2/91) plus the Z3")
    print("  Majorana phases (120, 240 deg) and the NH masses give the effective mass")
    print("  m_betabeta ~ 2.3 meV -- within reach of nEXO/LEGEND -- and the Dirac")
    print("  phase delta_CP = 14 pi/13 ~ 194 deg is the same phase that drives the")
    print("  cogenesis asymmetry. So the right-handed neutrino in the dark 128 fixes")
    print("  the neutrino masses, the 0nubb rate, the CP phase, AND the matter")
    print("  asymmetry -- one field, four falsifiable handles.")

    out["summary"] = (
        "0nubb from the 128 seesaw: cyclotomic PMNS (s12^2=4/13, "
        "s23^2=7/13, s13^2=2/91) + Z3 Majorana phases (120,240 deg) + NH "
        "masses (Sum=58 meV) -> m_betabeta ~ 2.3 meV (nEXO/LEGEND "
        "reach); delta_CP=14pi/13~194 deg = the cogenesis CP phase. One "
        "N_R fixes masses, 0nubb, CP phase, and the matter asymmetry."
    )
    out["sources"] = [
        "0nubb effective mass formula; cyclotomic PMNS (corpus); Z3 "
        "Majorana phases 120/240 deg (corpus); delta_CP=14pi/13; "
        "w33_neutrino_seesaw_128.py, w33_cogenesis.py"
    ]
    with open("data/w33_neutrinoless_betabeta.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_neutrinoless_betabeta.json")


if __name__ == "__main__":
    main()
