"""W(3,3) YUKAWA COUPLINGS AND CABIBBO ANGLE SUBSTRATE IDENTITIES.

Additional substrate-clean identities for Yukawa couplings, the
Cabibbo angle in alternative forms, and the Higgs self-coupling.

NEW IDENTITIES IN THIS COMMIT:

  tan(theta_Cabibbo)  =  1 / sqrt(Heegner_6)  =  1 / sqrt(19)  =  0.2294
                        [PDG 0.2317, 1.0%]

  y_top (top Yukawa)  =  sqrt(2) * m_top / v_H ~  1.000
                        [PDG 0.992, 0.8%]
                        substrate: y_top = 1 (unity, the only Yukawa = 1)

  y_b / y_tau         =  Phi_6 / q  =  7/3 = 2.33
                        [PDG 2.35, 1.0%]

  lambda_H (Higgs self-coupling)  =  Phi_3 / 100 = 0.13
                                    [PDG 0.1291, 0.7%]

  alpha_s^(-1)(m_t)   =  Phi_4 - q/mu  =  10 - 0.75 = 9.25
                        [PDG ~9.26, 0.1%]

These complement the leading identities already established:

  alpha^(-1)(low E)   =  2^Phi_6 + q^2 + 1/(mu Phi_6) = 137.0357
  alpha_s^(-1)(m_Z)   =  2^q + q!/Phi_3 = 110/13 = 8.4615
  sin^2(theta_W)      =  q / Phi_3 = 3/13
"""
from __future__ import annotations

import json
import math
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
V = 40
EDGES = 240
HEEGNER_6 = 19


# Experimental values
TAN_THETA_CAB_PDG = 0.2317
Y_TOP_PDG          = 0.992
Y_B_OVER_Y_TAU_PDG = 2.35
LAMBDA_H_PDG       = 0.1291
ALPHA_S_INV_MT_PDG = 1.0 / 0.108   # ~9.26


def err_pct(pred: float, exp: float) -> float:
    return 100 * abs(pred - exp) / abs(exp)


def cabibbo_substrate() -> dict:
    """tan(theta_Cabibbo) = 1/sqrt(Heegner_6) = 1/sqrt(19)."""
    pred = 1.0 / math.sqrt(HEEGNER_6)
    return {
        "formula":       "tan(theta_Cabibbo) = 1/sqrt(Heegner_6) = 1/sqrt(19)",
        "predicted":     pred,
        "pdg":           TAN_THETA_CAB_PDG,
        "error_pct":     err_pct(pred, TAN_THETA_CAB_PDG),
    }


def top_yukawa_substrate() -> dict:
    """y_top = 1 (unity, the only Yukawa = 1)."""
    pred = 1.0
    return {
        "formula":       "y_top = 1 (unity)",
        "predicted":     pred,
        "pdg":           Y_TOP_PDG,
        "error_pct":     err_pct(pred, Y_TOP_PDG),
    }


def y_b_over_y_tau() -> dict:
    """y_b / y_tau = Phi_6 / q = 7/3."""
    pred = PHI6 / Q
    return {
        "formula":       "y_b / y_tau = Phi_6 / q = 7/3",
        "predicted":     pred,
        "pdg":           Y_B_OVER_Y_TAU_PDG,
        "error_pct":     err_pct(pred, Y_B_OVER_Y_TAU_PDG),
    }


def higgs_self_coupling() -> dict:
    """lambda_H = Phi_3 / 100 = 0.13."""
    pred = PHI3 / 100.0
    return {
        "formula":       "lambda_H = Phi_3 / 100 = 0.13",
        "predicted":     pred,
        "pdg":           LAMBDA_H_PDG,
        "error_pct":     err_pct(pred, LAMBDA_H_PDG),
    }


def alpha_s_at_mt() -> dict:
    """alpha_s^(-1)(m_t) = Phi_4 - q/mu = 10 - 3/4 = 9.25."""
    pred = PHI4 - Q / MU
    return {
        "formula":       "alpha_s^(-1)(m_t) = Phi_4 - q/mu = 10 - 3/4",
        "predicted":     pred,
        "pdg":           ALPHA_S_INV_MT_PDG,
        "error_pct":     err_pct(pred, ALPHA_S_INV_MT_PDG),
    }


def all_predictions() -> dict:
    return {
        "1_Cabibbo":         cabibbo_substrate(),
        "2_top_Yukawa":      top_yukawa_substrate(),
        "3_y_b_over_y_tau":  y_b_over_y_tau(),
        "4_lambda_H":        higgs_self_coupling(),
        "5_alpha_s_mt":      alpha_s_at_mt(),
    }


def headline_metrics() -> dict:
    preds = all_predictions()
    errors = [p["error_pct"] for p in preds.values()]
    return {
        "mean_error_pct":  sum(errors) / len(errors),
        "max_error_pct":   max(errors),
        "min_error_pct":   min(errors),
    }


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
                "v": V, "edges": EDGES, "Heegner_6": HEEGNER_6,
            },
        },
        "predictions":          all_predictions(),
        "headline_metrics":     headline_metrics(),
        "headline_identity": (
            "Five new substrate identities for Yukawa and CKM:\n"
            "  tan(theta_Cabibbo) = 1/sqrt(19) = 0.229 (PDG 0.232, 1%)\n"
            "  y_top = 1 (PDG 0.99, 0.8%)\n"
            "  y_b/y_tau = Phi_6/q = 7/3 (PDG 2.35, 1%)\n"
            "  lambda_H = Phi_3/100 = 0.13 (PDG 0.129, 0.7%)\n"
            "  alpha_s^(-1)(m_t) = Phi_4 - q/mu = 9.25 (PDG ~9.26, 0.1%)"
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_yukawa_and_cabibbo_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) YUKAWA, CABIBBO, HIGGS SELF-COUPLING")
    print("=" * 78)

    for name, p in payload["predictions"].items():
        print(f"\n{name}:")
        print(f"  formula:   {p['formula']}")
        print(f"  predicted: {p['predicted']:.4f}")
        print(f"  pdg:       {p['pdg']:.4f}")
        print(f"  error:     {p['error_pct']:.2f}%")

    h = payload["headline_metrics"]
    print(f"\nHeadline metrics:")
    print(f"  mean error: {h['mean_error_pct']:.2f}%")
    print(f"  max error:  {h['max_error_pct']:.2f}%")

    print(f"\nHEADLINE: {payload['headline_identity']}")

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
