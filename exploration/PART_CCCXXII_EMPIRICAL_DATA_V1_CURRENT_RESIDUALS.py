#!/usr/bin/env python3
"""
PART CCCXXII - Empirical Data v1 / Current Residuals
====================================================

Purpose:
    Finish the first empirical closure pass by inserting current, cited measured
    values for the safest initial physical comparison: charged-lepton Koide.

External data policy:
    Values in this file are current-source data points, not derived from W33.
    They must remain versioned and source-tagged.

Current data used (PDG/pdgLive, accessed 2026-05-05):
    electron mass: 0.51099895069 ± 0.00000000016 MeV
    muon mass:     105.6583755  ± 0.0000023 MeV
    tau mass:      1776.93      ± 0.09 MeV
    effective leptonic weak mixing angle: 0.23148 ± 0.00012

Primary empirical comparison:
    Koide ratio
        Q = (me + mmu + mtau) / (sqrt(me)+sqrt(mmu)+sqrt(mtau))^2

    W33 target:
        Q_W33 = 2/3

Result:
        Q_data = 0.6666644634026365
        residual = Q_data - 2/3 = -2.2032640301e-6
        propagated sigma ≈ 5.0809581952e-6
        z ≈ -0.43363

Interpretation:
    Under this simple PDG-mass scheme, the Koide target 2/3 is compatible with
    the current charged-lepton masses at <1 sigma.  This is a real dimensionless
    empirical success candidate, but it must be locked to the mass scheme and
    source version.

Weak mixing boundary:
    W33 candidate target sin^2(theta_W)=3/8 is a unification-boundary value.
    pdgLive effective leptonic weak angle at the Z pole is about 0.23148 ±0.00012.
    A raw direct comparison is therefore not a pass/fail test; it is a reminder
    that an RG/unification map is mandatory before calling this empirical.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# W33 exact targets.
KOIDE_TARGET = Fraction(2, 3)
SIN2_THETA_W_GUT_TARGET = Fraction(3, 8)

# External measured values, source-tagged in output.
M_E = 0.51099895069
SIGMA_E = 0.00000000016
M_MU = 105.6583755
SIGMA_MU = 0.0000023
M_TAU = 1776.93
SIGMA_TAU = 0.09
SIN2_EFF_LEPT = 0.23148
SIGMA_SIN2_EFF_LEPT = 0.00012


def koide(me: float, mmu: float, mtau: float) -> float:
    root_sum = math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)
    return (me + mmu + mtau) / (root_sum * root_sum)


def central_derivative(func, vals: List[float], idx: int, h: float) -> float:
    vp = list(vals)
    vm = list(vals)
    vp[idx] += h
    vm[idx] -= h
    return (func(*vp) - func(*vm)) / (2 * h)


KOIDE_DATA = koide(M_E, M_MU, M_TAU)
KOIDE_RESIDUAL = KOIDE_DATA - float(KOIDE_TARGET)
_DERIV_STEPS = [1e-9, 1e-5, 1e-4]
_DERIVS = [central_derivative(koide, [M_E, M_MU, M_TAU], i, _DERIV_STEPS[i]) for i in range(3)]
KOIDE_SIGMA = math.sqrt((_DERIVS[0] * SIGMA_E) ** 2 + (_DERIVS[1] * SIGMA_MU) ** 2 + (_DERIVS[2] * SIGMA_TAU) ** 2)
KOIDE_Z = KOIDE_RESIDUAL / KOIDE_SIGMA

SIN2_RAW_RESIDUAL = SIN2_EFF_LEPT - float(SIN2_THETA_W_GUT_TARGET)
SIN2_RAW_Z = SIN2_RAW_RESIDUAL / SIGMA_SIN2_EFF_LEPT


@dataclass(frozen=True)
class EmpiricalResidual:
    id: str
    observable: str
    theory_value: str | float
    measured_value: float
    uncertainty: float
    residual: float
    z_score: float
    scheme: str
    status: str
    interpretation: str
    source: str


def residual_records() -> List[EmpiricalResidual]:
    return [
        EmpiricalResidual(
            id="M1_KOIDE_CHARGED_LEPTON_PDGLIVE_2026",
            observable="charged-lepton Koide ratio",
            theory_value="2/3",
            measured_value=KOIDE_DATA,
            uncertainty=KOIDE_SIGMA,
            residual=KOIDE_RESIDUAL,
            z_score=KOIDE_Z,
            scheme="PDG/pdgLive charged-lepton masses in MeV; simple independent uncertainty propagation",
            status="PASS_WITHIN_1_SIGMA_UNDER_THIS_SCHEME",
            interpretation="Dimensionless W33 target 2/3 is compatible with current charged-lepton masses under this scheme.",
            source="PDG/pdgLive electron, muon, tau mass entries accessed 2026-05-05",
        ),
        EmpiricalResidual(
            id="M1_SIN2_THETA_W_RAW_Z_POLE_NOT_RG_TEST",
            observable="effective leptonic weak mixing angle at Z pole vs GUT-boundary target",
            theory_value="3/8",
            measured_value=SIN2_EFF_LEPT,
            uncertainty=SIGMA_SIN2_EFF_LEPT,
            residual=SIN2_RAW_RESIDUAL,
            z_score=SIN2_RAW_Z,
            scheme="raw direct comparison only; no RG/unification running applied",
            status="RG_REQUIRED_NOT_A_DIRECT_PASS_FAIL_TEST",
            interpretation="The 3/8 value is a unification-boundary target, not a direct Z-pole prediction. A running map is mandatory.",
            source="PDG/pdgLive sin^2(theta_eff^lept) entry accessed 2026-05-05",
        ),
    ]


def empirical_data_current_audit() -> Dict[str, object]:
    checks = {
        "koide_target": KOIDE_TARGET == Fraction(2, 3),
        "sin2_target": SIN2_THETA_W_GUT_TARGET == Fraction(3, 8),
        "koide_value_window": 0.66666 < KOIDE_DATA < 0.66667,
        "koide_residual_small": abs(KOIDE_RESIDUAL) < 3e-6,
        "koide_sigma_positive": KOIDE_SIGMA > 0,
        "koide_within_one_sigma": abs(KOIDE_Z) < 1,
        "sin2_raw_is_not_gut": abs(SIN2_RAW_Z) > 100,
        "records": len(residual_records()) == 2,
    }
    assert all(checks.values())

    return {
        "schema_version": "empirical_data_v1_current_residuals",
        "module": "PART_CCCXXII_EMPIRICAL_DATA_V1_CURRENT_RESIDUALS",
        "status": "first current-source residual table for W33 empirical program",
        "external_sources": {
            "electron_mass": "PDG/pdgLive e mass 0.51099895069 ± 0.00000000016 MeV",
            "muon_mass": "PDG/pdgLive mu mass 105.6583755 ± 0.0000023 MeV",
            "tau_mass": "PDG/pdgLive tau mass 1776.93 ± 0.09 MeV",
            "weak_mixing": "PDG/pdgLive sin^2(theta_eff^lept) average 0.23148 ± 0.00012",
        },
        "input_values": {
            "m_e_MeV": M_E,
            "sigma_m_e_MeV": SIGMA_E,
            "m_mu_MeV": M_MU,
            "sigma_m_mu_MeV": SIGMA_MU,
            "m_tau_MeV": M_TAU,
            "sigma_m_tau_MeV": SIGMA_TAU,
            "sin2_eff_lept": SIN2_EFF_LEPT,
            "sigma_sin2_eff_lept": SIGMA_SIN2_EFF_LEPT,
        },
        "residuals": [asdict(record) for record in residual_records()],
        "koide_derivatives": {
            "dQ_dme": _DERIVS[0],
            "dQ_dmmu": _DERIVS[1],
            "dQ_dmtau": _DERIVS[2],
        },
        "checks": checks,
        "theorem_statement": (
            "The first current-source empirical residual table confirms that the W33 Koide target Q=2/3 is compatible with current "
            "charged-lepton masses under the stated PDG/pdgLive mass scheme, with z about -0.43.  The weak-mixing target 3/8 remains "
            "an RG-boundary claim, not a direct Z-pole prediction."
        ),
        "honesty_boundary": (
            "Only Koide is evaluated here as a direct dimensionless comparison.  Weak mixing requires a specified RG/unification map before "
            "it can be used as pass/fail evidence for or against the W33 interpretation."
        ),
    }


def main() -> int:
    audit = empirical_data_current_audit()
    out = ROOT / "empirical_data_v1_current_residuals.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    mirror = ROOT / "PART_CCCXXII_empirical_data_v1_current_residuals_results.json"
    mirror.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    print(f"Wrote {mirror}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
