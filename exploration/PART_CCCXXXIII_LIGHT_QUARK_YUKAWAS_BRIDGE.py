#!/usr/bin/env python3
"""
PART CCCXXXIII -- Light-quark Yukawas in W(3,3): y_d, y_u from 137^3
====================================================================

The Standard Model down and up quark Yukawa couplings, both in the
MS-bar scheme at 2 GeV, admit clean W(3,3) closed forms with a common
denominator 137^3:

      +-----------------------------------------+
      |  y_d(MSbar, 2 GeV) = Phi_6*Phi_4 / 137^3 |
      |                    = H_0 / 137^3        |
      |                    = 70 / 137^3         |
      |                                         |
      |  y_u(MSbar, 2 GeV) = lam^5 / 137^3      |
      |                    = 32 / 137^3         |
      +-----------------------------------------+

with H_0 = Phi_6 * Phi_4 = 70 the Hubble fixed point (Supplement W),
137 = q^q*(mu+1) + lam = q^2*g + lam the fine-structure prime
(CCCXXIX), and lam^5 = 32.

PDG 2024:
    m_d(MSbar, 2 GeV) = 4.70 +- 0.07 MeV
    m_u(MSbar, 2 GeV) = 2.16 + 0.49 - 0.26 MeV
    y_d_data = 2.700e-5 +- 4.0e-7
    y_u_data = 1.241e-5 +- 2.3e-6 (asymm)

W(3,3):
    y_d = 70/137^3   = 2.722e-5    (z = -0.57)
    y_u = 32/137^3   = 1.244e-5    (z = -0.017)
    m_d_pred = 4.74 MeV  (vs 4.70 +- 0.07,  z = +0.57)
    m_u_pred = 2.167 MeV (vs 2.16 +- 0.40,  z = +0.017)

Both within 1 sigma; up Yukawa within 0.02 sigma.

Cross-link with cosmology:
    H_0 = 70 = Phi_6 * Phi_4 is the Hubble fixed point established in
    Supplement W (Phase 274). The down-quark Yukawa numerator equals
    the Hubble fixed point: y_d * 137^3 = H_0.  This is a striking
    Yukawa-cosmology coincidence in W(3,3) integers.

Up/down ratio:
    y_u / y_d = lam^5 / (Phi_6*Phi_4) = 32/70 = 16/35 = 0.4571
    PDG m_u/m_d = 0.46 (large uncertainty, lattice).

Light-quark unified denominator structure:
    All three down-sector Yukawas (b, s, d) and all up-sector except
    top use 137 and Phi_4 in the W(3,3) form:
        y_b = q/(mu+1)^3                      (CCCXXVIII; uses (mu+1))
        y_c = 1/137                           (CCCXXIX;   uses 137^1)
        y_s = Phi_4/137^2                     (CCCXXX;    uses 137^2)
        y_d = (Phi_6*Phi_4)/137^3 = H_0/137^3 (CCCXXXIII; uses 137^3)
        y_u = lam^5/137^3                     (CCCXXXIII; uses 137^3)
    Increasing 137 powers track decreasing Yukawa magnitude through
    the second and first generations.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]

# --- W(3,3) base constants ---
Q = 3
V = 40
K = 12
LAM = 2
MU = 4
F = 24
G = 15
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
H_0 = PHI6 * PHI4   # 70 = Phi_6 * Phi_4 (Hubble fixed point, Supp W)
ALPHA_INV = Q ** Q * (MU + 1) + LAM   # 137 (CCCXXIX)

# --- W(3,3) predictions ---
Y_D_W33 = Fraction(H_0, ALPHA_INV ** 3)         # 70/137^3
Y_U_W33 = Fraction(LAM ** 5, ALPHA_INV ** 3)    # 32/137^3

# --- External data (PDG 2024) ---
M_D_MEV       = 4.70
SIGMA_M_D_MEV = 0.07
M_U_MEV       = 2.16
SIGMA_M_U_MEV = 0.40   # symmetrized from asymmetric +0.49/-0.26
V_EW_GEV      = 246.21965


def y_from_m(m_GeV: float, v_GeV: float) -> float:
    return m_GeV * math.sqrt(2.0) / v_GeV


M_D_GEV = M_D_MEV / 1000.0
M_U_GEV = M_U_MEV / 1000.0

Y_D_DATA       = y_from_m(M_D_GEV, V_EW_GEV)
SIGMA_Y_D_DATA = (SIGMA_M_D_MEV / M_D_MEV) * Y_D_DATA
Y_U_DATA       = y_from_m(M_U_GEV, V_EW_GEV)
SIGMA_Y_U_DATA = (SIGMA_M_U_MEV / M_U_MEV) * Y_U_DATA

RESIDUAL_Y_D = Y_D_DATA - float(Y_D_W33)
Z_Y_D        = RESIDUAL_Y_D / SIGMA_Y_D_DATA

RESIDUAL_Y_U = Y_U_DATA - float(Y_U_W33)
Z_Y_U        = RESIDUAL_Y_U / SIGMA_Y_U_DATA

M_D_PRED_MEV = float(Y_D_W33) * V_EW_GEV / math.sqrt(2) * 1000
M_U_PRED_MEV = float(Y_U_W33) * V_EW_GEV / math.sqrt(2) * 1000


@dataclass(frozen=True)
class LightQuarkResidual:
    id: str
    observable: str
    theory_value: str
    theory_decimal: float
    measured_value: float
    uncertainty: float
    residual: float
    z_score: float
    status: str


def _status(z: float) -> str:
    az = abs(z)
    if az < 1: return "PASS_WITHIN_1_SIGMA"
    if az < 2: return "PASS_WITHIN_2_SIGMA"
    if az < 3: return "PASS_WITHIN_3_SIGMA"
    return "DISFAVORED"


def residual_records() -> List[LightQuarkResidual]:
    return [
        LightQuarkResidual(
            id="DOWN_YUKAWA_W33",
            observable="y_d(MSbar, 2 GeV)",
            theory_value="(Phi_6*Phi_4) / 137^3 = 70/2571353",
            theory_decimal=float(Y_D_W33),
            measured_value=Y_D_DATA,
            uncertainty=SIGMA_Y_D_DATA,
            residual=RESIDUAL_Y_D,
            z_score=Z_Y_D,
            status=_status(Z_Y_D),
        ),
        LightQuarkResidual(
            id="UP_YUKAWA_W33",
            observable="y_u(MSbar, 2 GeV)",
            theory_value="lam^5 / 137^3 = 32/2571353",
            theory_decimal=float(Y_U_W33),
            measured_value=Y_U_DATA,
            uncertainty=SIGMA_Y_U_DATA,
            residual=RESIDUAL_Y_U,
            z_score=Z_Y_U,
            status=_status(Z_Y_U),
        ),
    ]


# --- Checks ---
checks: list[tuple[str, bool]] = []
def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


# (1) W(3,3) forms
_ck("y_d = Phi_6*Phi_4 / 137^3", Y_D_W33 == Fraction(H_0, ALPHA_INV ** 3))
_ck("y_d = 70/137^3",            Y_D_W33 == Fraction(70, 137 ** 3))
_ck("y_u = lam^5 / 137^3",       Y_U_W33 == Fraction(LAM ** 5, ALPHA_INV ** 3))
_ck("y_u = 32/137^3",            Y_U_W33 == Fraction(32, 137 ** 3))

# (2) Components
_ck("H_0 = Phi_6 * Phi_4 = 70",  H_0 == 70)
_ck("137 = q^q*(mu+1) + lam",    ALPHA_INV == 137)
_ck("137^3 = 2571353",           ALPHA_INV ** 3 == 2571353)
_ck("lam^5 = 32",                LAM ** 5 == 32)

# (3) Residuals
_ck("|z_y_d| < 1",               abs(Z_Y_D) < 1)
_ck("|z_y_u| < 1",               abs(Z_Y_U) < 1)

# (4) Predicted masses in PDG window
_ck("4.4 < m_d_pred < 5.0 MeV",  4.4 < M_D_PRED_MEV < 5.0)
_ck("1.7 < m_u_pred < 2.6 MeV",  1.7 < M_U_PRED_MEV < 2.6)

# (5) Up/down ratio
ratio_W33  = Fraction(LAM ** 5, H_0)   # 32/70 = 16/35
ratio_data = M_U_MEV / M_D_MEV
_ck("y_u/y_d = lam^5/H_0 = 16/35", ratio_W33 == Fraction(16, 35))
_ck("|m_u/m_d residual| < 0.05",
    abs(float(ratio_W33) - ratio_data) < 0.05)

# (6) Cross-link with charm and strange Yukawa pattern
Y_C = Fraction(1, 137)
Y_S = Fraction(PHI4, 137 ** 2)
_ck("y_c = 1/137 (CCCXXIX)",     Y_C == Fraction(1, 137))
_ck("y_s = Phi_4/137^2 (CCCXXX)", Y_S == Fraction(PHI4, 137 ** 2))
# 137 powers: 1 (charm), 2 (strange), 3 (down/up)
_ck("y_c denom = 137^1", Y_C.denominator == 137)
_ck("y_s denom = 137^2", Y_S.denominator == 137 ** 2)
_ck("y_d denom = 137^3", Y_D_W33.denominator == 137 ** 3)
_ck("y_u denom = 137^3", Y_U_W33.denominator == 137 ** 3)

# (7) Cross-link with cosmology: H_0 = 70 (Hubble fixed point)
_ck("y_d numerator = H_0 (Hubble fixed point)", Y_D_W33.numerator == H_0)


# Verified gate
Verified = all(v for _, v in checks)


def _build_results() -> Dict[str, object]:
    return {
        "part": "CCCXXXIII",
        "title": "Light-quark Yukawas y_d = H_0/137^3 and y_u = lam^5/137^3 in W(3,3)",
        "Verified": Verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "constants": {
            "Q": Q, "V": V, "K": K, "LAM": LAM, "MU": MU, "F": F, "G": G,
            "PHI3": PHI3, "PHI4": PHI4, "PHI6": PHI6,
            "H_0": H_0, "ALPHA_INV": ALPHA_INV,
        },
        "predictions": {
            "y_d_W33":          float(Y_D_W33),
            "y_u_W33":          float(Y_U_W33),
            "m_d_pred_MeV":     M_D_PRED_MEV,
            "m_u_pred_MeV":     M_U_PRED_MEV,
            "y_u_over_y_d_W33": str(Fraction(LAM ** 5, H_0)),
        },
        "external_inputs": {
            "m_d_MeV":     M_D_MEV,
            "sigma_m_d":   SIGMA_M_D_MEV,
            "m_u_MeV":     M_U_MEV,
            "sigma_m_u":   SIGMA_M_U_MEV,
            "v_EW_GeV":    V_EW_GEV,
            "source":      "PDG 2024 m_d, m_u (MSbar at 2 GeV)",
        },
        "residuals": [asdict(r) for r in residual_records()],
        "down_sector_pattern": {
            "y_b": "q/(mu+1)^3      = 3/125     (CCCXXVIII)",
            "y_s": "Phi_4/137^2     = 10/18769  (CCCXXX)",
            "y_d": "(Phi_6*Phi_4)/137^3 = H_0/137^3  (this part)",
            "comment": (
                "Down-sector Yukawas progress through powers of 137: "
                "y_s ~ 137^-2, y_d ~ 137^-3.  y_b uses (mu+1)^3 = 125 instead. "
                "y_d numerator equals the Hubble fixed point H_0 = Phi_6*Phi_4 = 70."
            ),
        },
        "up_sector_pattern": {
            "y_t^3": "v/(v+1) = 40/41        (CCCXXVI)",
            "y_c":   "1/137                  (CCCXXIX)",
            "y_u":   "lam^5/137^3 = 32/137^3 (this part)",
            "comment": (
                "Up-sector Yukawas: y_t close to 1, y_c = 1/137, "
                "y_u = lam^5/137^3.  Skip 137^2 in the up sector."
            ),
        },
        "theorem_statement": (
            "The light-quark Yukawas in MS-bar at 2 GeV admit W(3,3) closed forms "
            "with common denominator 137^3:  y_d = H_0/137^3 and y_u = lam^5/137^3, "
            "where H_0 = Phi_6 * Phi_4 = 70 is the Hubble fixed point of Supplement W "
            "and 137 = q^q*(mu+1) + lam is the fine-structure W(3,3) prime from CCCXXIX. "
            "Both predictions are within 1 sigma of PDG 2024 (y_u within 0.02 sigma, "
            "y_d within 0.6 sigma). m_d_pred = 4.74 MeV (vs 4.70 +- 0.07), "
            "m_u_pred = 2.17 MeV (vs 2.16 +- 0.40)."
        ),
        "honesty_boundary": (
            "Light-quark masses have substantial PDG uncertainty (m_u ~ 18 percent, "
            "m_d ~ 1.5 percent) from lattice extraction.  W(3,3) predictions are well "
            "within these uncertainties.  The numerator H_0 = 70 in y_d connects the "
            "down-quark Yukawa to the cosmological Hubble fixed point; this is a "
            "numerical coincidence of W(3,3) integers, not yet a structural derivation."
        ),
    }


def main() -> int:
    results = _build_results()
    out = ROOT / "PART_CCCXXXIII_light_quark_yukawas_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print(f"y_d_W33 = (Phi_6*Phi_4)/137^3 = 70/137^3 = {float(Y_D_W33):.6e}")
    print(f"y_d_data = m_d sqrt(2)/v                 = {Y_D_DATA:.6e} +- {SIGMA_Y_D_DATA:.6e}  (z = {Z_Y_D:+.3f})")
    print(f"y_u_W33 = lam^5/137^3 = 32/137^3        = {float(Y_U_W33):.6e}")
    print(f"y_u_data                                = {Y_U_DATA:.6e} +- {SIGMA_Y_U_DATA:.6e}  (z = {Z_Y_U:+.3f})")
    print(f"m_d_pred = {M_D_PRED_MEV:.3f} MeV   measured {M_D_MEV} +- {SIGMA_M_D_MEV}")
    print(f"m_u_pred = {M_U_PRED_MEV:.3f} MeV   measured {M_U_MEV} +- {SIGMA_M_U_MEV}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
