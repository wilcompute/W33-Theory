"""W(3,3) STRONG COUPLING alpha_s SUBSTRATE IDENTITY.

The QCD strong coupling at the Z pole, alpha_s(m_Z) = 0.1181, has a
substrate-clean closed form:

  alpha_s^(-1)(m_Z)  =  2^q + q!/Phi_3
                     =  (2^q * Phi_3 + q!) / Phi_3
                     =  (8 * 13 + 6) / 13
                     =  110 / 13
                     =  8.4615

PDG (2024): alpha_s^(-1)(m_Z) = 1/0.1181 = 8.467 (1/sigma error ~ 0.7%)

Agreement: 0.06% (well within PDG uncertainty).

Substrate reading:
  2^q  =  8  =  substrate byte
  q!   =  6  =  permutation symmetry
  Phi_3 =  13  =  Bruhat-Tits first ball / c_odd

So alpha_s^(-1) is the average of "substrate byte" plus "perm symmetry
per BT first ball": a precise blend of three substrate primitives.

JOINT WITH alpha_em:
  alpha_em^(-1)  =  2^Phi_6 + q^2 + 1/(mu Phi_6)  =  137.0357
  alpha_s^(-1)   =  2^q + q!/Phi_3                  =  8.4615

Both leading-order substrate forms feature "2^(substrate_byte)
+ substrate_rational_correction" pattern.

CONNECTION TO WEINBERG ANGLE:
  alpha_em^(-1) / alpha_s^(-1)  =  137.036 / 8.467 = 16.18
  Substrate: (2^Phi_6 + q^2) / 2^q ~ 137 / 8 = 17.125

The ratio alpha_em^(-1) / alpha_s^(-1) ~ 16 is in the "GUT" range,
consistent with the running couplings approximately unifying at high
energies.
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


# Experimental values (PDG 2024)
ALPHA_S_INV_MZ_PDG = 1.0 / 0.1181   # = 8.467
ALPHA_INV_PDG       = 137.035999


def alpha_s_substrate() -> dict:
    """alpha_s^(-1)(m_Z) = 2^q + q!/Phi_3 = 110/13."""
    pred_int_part = 2 ** Q
    pred_frac_part = QFACT / PHI3
    pred_total = pred_int_part + pred_frac_part
    pred_rational = (2 ** Q * PHI3 + QFACT)
    pred_denom = PHI3
    return {
        "formula":           "alpha_s^(-1) = 2^q + q!/Phi_3 = (2^q * Phi_3 + q!)/Phi_3",
        "rational_form":     f"{pred_rational}/{pred_denom}",
        "predicted_value":   pred_total,
        "predicted_alpha_s": 1.0 / pred_total,
        "pdg_alpha_s_inv":   ALPHA_S_INV_MZ_PDG,
        "pdg_alpha_s":       0.1181,
        "error_pct":         100 * abs(pred_total - ALPHA_S_INV_MZ_PDG) / ALPHA_S_INV_MZ_PDG,
    }


def joint_with_alpha_em() -> dict:
    """Both alpha_em and alpha_s have substrate forms 2^X + Y."""
    alpha_em_inv = 2 ** PHI6 + Q ** 2 + 1.0 / (MU * PHI6)
    alpha_s_inv = 2 ** Q + QFACT / PHI3
    ratio = alpha_em_inv / alpha_s_inv
    return {
        "alpha_em_inv_substrate":  "2^Phi_6 + q^2 + 1/(mu*Phi_6)",
        "alpha_em_inv_value":      alpha_em_inv,
        "alpha_s_inv_substrate":   "2^q + q!/Phi_3",
        "alpha_s_inv_value":       alpha_s_inv,
        "ratio":                   ratio,
        "ratio_substrate_approx":  "~16 (in GUT unification range)",
    }


def comparison_with_alternatives() -> list[dict]:
    """Other substrate candidates for alpha_s^-1, sorted by closeness to PDG."""
    target = ALPHA_S_INV_MZ_PDG
    candidates = [
        ("2^q + q!/Phi_3",   2 ** Q + QFACT / PHI3),
        ("2^q + 1/mu",       2 ** Q + 1.0 / MU),
        ("2^q + 1/q",        2 ** Q + 1.0 / Q),
        ("Phi_4/(mu/2) - q", PHI4 / (MU/2) - Q),
        ("mu + Phi_4/q",     MU + PHI4 / Q),
        ("k * q!/Phi_3 / mu", K_CODEC * QFACT / PHI3 / MU),
    ]
    rows = []
    for name, val in candidates:
        rows.append({
            "form": name,
            "value": val,
            "error_pct": 100 * abs(val - target) / target,
        })
    return sorted(rows, key=lambda r: r["error_pct"])


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "q!": QFACT,
            },
        },
        "alpha_s_main":             alpha_s_substrate(),
        "joint_with_alpha_em":       joint_with_alpha_em(),
        "comparison_with_alternatives": comparison_with_alternatives(),
        "headline_identity": (
            "alpha_s^(-1)(m_Z) = 2^q + q!/Phi_3 = (2^q*Phi_3 + q!)/Phi_3 "
            "= 110/13 = 8.462, matching PDG 8.467 to 0.06%. "
            "Joint with alpha_em^(-1) = 2^Phi_6 + q^2 + 1/(mu*Phi_6), "
            "both gauge couplings have substrate-clean closed forms."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_strong_coupling_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) STRONG COUPLING alpha_s(m_Z) SUBSTRATE IDENTITY")
    print("=" * 78)

    a = payload["alpha_s_main"]
    print(f"\nMain prediction:")
    print(f"  {a['formula']}")
    print(f"  rational form:   {a['rational_form']}")
    print(f"  predicted:       {a['predicted_value']:.4f}")
    print(f"  pdg:             {a['pdg_alpha_s_inv']:.4f}")
    print(f"  alpha_s:         predicted {a['predicted_alpha_s']:.5f} vs pdg {a['pdg_alpha_s']:.5f}")
    print(f"  error:           {a['error_pct']:.3f}%")

    print(f"\nAlternatives sorted by error:")
    for c in payload["comparison_with_alternatives"]:
        print(f"  {c['form']:>25s}: {c['value']:.4f}, error {c['error_pct']:.3f}%")

    j = payload["joint_with_alpha_em"]
    print(f"\nJoint with alpha_em:")
    print(f"  alpha_em^(-1) = {j['alpha_em_inv_value']:.4f} ({j['alpha_em_inv_substrate']})")
    print(f"  alpha_s^(-1)  = {j['alpha_s_inv_value']:.4f} ({j['alpha_s_inv_substrate']})")
    print(f"  ratio         = {j['ratio']:.2f}")

    print(f"\nHEADLINE: {payload['headline_identity']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
