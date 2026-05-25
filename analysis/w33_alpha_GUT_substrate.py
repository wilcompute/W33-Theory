"""W(3,3) GAUGE UNIFICATION AT m_GUT: alpha^-1_GUT = f = gauge_mult.

At the GUT scale m_GUT ~ 10^16 GeV (substrate: m_Pl * q^(-q!)), all
three Standard Model gauge couplings converge to a near-common value
alpha_GUT ~ 1/24 to 1/26 (depending on the GUT scheme).  The substrate
predicts exactly:

  alpha_GUT^(-1)  =  f  =  gauge_mult  =  24

This unifies all three running couplings at the substrate-clean
gauge multiplicity primitive.

SUBSTRATE GAUGE-COUPLING SCALES:

  Scale         alpha_em^(-1)         alpha_s^(-1)        Substrate prediction
  ----------    ---------------       --------------       -----------------
  low (Thomson) 2^Phi_6 + q^2 + small  -                   137.036
                (= 137)
  m_Z           2^Phi_6 = 128          2^q + q!/Phi_3 = 8.46 128, 8.46
  m_GUT         f = 24                 f = 24              24 = f = gauge_mult

So the running gauge couplings transition from
alpha^(-1)(0) = 2^Phi_6 + q^2 = 137
through alpha^(-1)(m_Z) = 2^Phi_6 = 128 (q^2 less)
to alpha^(-1)(m_GUT) = f = 24

The reduction from m_Z to m_GUT is 128 - 24 = 104 = ... ~ 4 * Heegner_67 - 164.
Actually 104 = 8 * 13 = 2^q * Phi_3.

So Delta alpha^(-1) (m_Z -> m_GUT) ~ 2^q * Phi_3 = 104.

PHYSICAL CONNECTION:

In Grand Unified Theories (SU(5), SO(10), E_6), the three SM gauge
couplings g_1 (U(1)), g_2 (SU(2)), g_3 (SU(3)) unify at the GUT scale.
At the unification point:

  alpha_GUT  ~  1/24 to 1/26

The substrate value alpha_GUT^(-1) = f = 24 = gauge_mult is at the
LOWER end of this range, suggesting an E_6 or SU(5)-like unification.

The substrate scale m_GUT = m_Pl * q^(-q!) = 3^(-6) * 1.22e19 = 1.67e16 GeV
matches the SU(5) GUT scale, providing a self-consistent substrate
GUT scenario.
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
F = 24


# Conventional GUT values (model-dependent)
ALPHA_GUT_INV_RANGE = (24, 26)
M_PL_GEV = 1.2209e19


def alpha_unification() -> dict:
    pred = F
    in_range = ALPHA_GUT_INV_RANGE[0] <= pred <= ALPHA_GUT_INV_RANGE[1]
    return {
        "claim": "alpha_GUT^(-1) = f = gauge_mult = 24",
        "predicted":   pred,
        "GUT_range":   ALPHA_GUT_INV_RANGE,
        "in_range":    in_range,
        "substrate":   "f = gauge_mult (Hashimoto gauge sector multiplicity)",
    }


def m_GUT_substrate() -> dict:
    pred_mass = M_PL_GEV * (Q ** (-QFACT))
    return {
        "formula":           "m_GUT = m_Pl * q^(-q!)",
        "substrate":         "q^(-6) m_Pl",
        "predicted_GeV":     pred_mass,
        "typical_observation": "~10^15 - 10^16 GeV (SU(5)/SO(10) gauge unification)",
        "match":             "1.67e16 GeV; consistent with SU(5)/SO(10) range",
    }


def coupling_running_substrate() -> list[dict]:
    return [
        {
            "scale": "Thomson (low energy)",
            "alpha_em^-1":  2 ** PHI6 + Q ** 2 + 1.0 / (MU * PHI6),
            "form":         "2^Phi_6 + q^2 + 1/(mu Phi_6)",
            "value":        "137.036",
        },
        {
            "scale": "m_Z (electroweak)",
            "alpha_em^-1":  2 ** PHI6,
            "form":         "2^Phi_6",
            "value":        "128",
        },
        {
            "scale": "m_GUT (gauge unification)",
            "alpha_em^-1":  F,
            "form":         "f = gauge_mult",
            "value":        "24",
        },
    ]


def running_reduction() -> dict:
    delta_low_to_mZ = (2 ** PHI6 + Q ** 2) - 2 ** PHI6   # = q^2 = 9
    delta_mZ_to_GUT = 2 ** PHI6 - F                       # = 128 - 24 = 104
    return {
        "low_to_m_Z":    {"delta": delta_low_to_mZ, "substrate": "q^2 = 9"},
        "m_Z_to_m_GUT":  {"delta": delta_mZ_to_GUT, "substrate": "2^q * Phi_3 = 8 * 13 = 104"},
        "total_low_to_GUT": {"delta": (2**PHI6 + Q**2) - F, "substrate": "2^Phi_6 + q^2 - f = 137 - 24 = 113"},
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6, "f": F,
                "m_Pl_GeV": M_PL_GEV,
            },
        },
        "alpha_unification":      alpha_unification(),
        "m_GUT_substrate":         m_GUT_substrate(),
        "coupling_running":         coupling_running_substrate(),
        "running_reduction":        running_reduction(),
        "headline": (
            "GAUGE UNIFICATION SUBSTRATE PREDICTION:\n"
            "  alpha_GUT^(-1) = f = gauge_mult = 24\n"
            "  m_GUT = m_Pl * q^(-q!) = 1.67e16 GeV (SU(5) range)\n"
            "Running ladder: 137 (low E) -> 128 (m_Z) -> 24 (m_GUT)\n"
            "Reductions: q^2 = 9 (low->mZ), 2^q*Phi_3 = 104 (mZ->GUT)"
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_alpha_GUT_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) GAUGE UNIFICATION AT m_GUT")
    print("=" * 78)

    a = payload["alpha_unification"]
    print(f"\nPrediction: {a['claim']}")
    print(f"  predicted: {a['predicted']}")
    print(f"  GUT range: {a['GUT_range']}")
    print(f"  in range: {a['in_range']}")

    g = payload["m_GUT_substrate"]
    print(f"\nGUT scale:")
    print(f"  {g['formula']} = {g['predicted_GeV']:.2e} GeV")
    print(f"  {g['match']}")

    print(f"\nCoupling running ladder:")
    for c in payload["coupling_running"]:
        print(f"  {c['scale']:>20s}: alpha^-1 = {c['value']:>8s}  ({c['form']})")

    r = payload["running_reduction"]
    print(f"\nRunning reductions:")
    for key, info in r.items():
        print(f"  {key}: delta = {info['delta']} ({info['substrate']})")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
