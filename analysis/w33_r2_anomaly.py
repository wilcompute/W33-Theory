#!/usr/bin/env python3
"""
Testing whether the c=24 boundary generates R^2 -- and unifying the residue. The honest
result is a NEGATIVE that sharpens the picture: the conformal anomaly of the substrate's
c = f = 24 boundary CFT generates an R^2 term with coefficient of order c/(2880 pi^2) ~
10^-3, whereas Starobinsky inflation needs an R^2 coefficient ~ 6x10^8 (set by the scalaron
mass M ~ 2.8x10^13 GeV from A_s) -- about twelve orders too small. So the c=24 anomaly does
NOT derive R^2 gravity. But the exercise UNIFIES the scale residue: the R^2 coefficient, the
scalaron mass M, and the A_s exponent are the SAME single number, so the entire remaining
input of the cosmological tower is one quantity (the large R^2 coefficient / light scalaron),
not derived from the boundary CFT.

w33_starobinsky.py identified the substrate as Starobinsky (R^2) inflation. The natural
hope was that R^2 comes from integrating out the c=24 boundary (machine=world as a
derivation). This tests it.

THE R^2 COEFFICIENT (from Starobinsky). In S = (M_Pl^2/2) int (R + R^2/(6 M^2)), the R^2
coefficient is M_Pl^2/(12 M^2). With the scalaron mass fixed by the amplitude,
A_s = N^2 M^2/(24 pi^2 M_Pl^2)  ->  M = M_Pl sqrt(24 pi^2 A_s)/N ~ 2.8x10^13 GeV (reduced
M_Pl), the coefficient is M_Pl^2/(12 M^2) ~ 6x10^8.

THE CONFORMAL ANOMALY (what c=24 gives). Integrating out a CFT of central charge c induces
a local R^2 piece in the effective action with coefficient of order c/(2880 pi^2) (the
standard one-loop trace-anomaly normalisation). For c = f = 24 this is ~ 8x10^-4 -- an
O(1)/(4pi)^2 number. The ratio
    (Starobinsky coeff) / (anomaly coeff) ~ 6x10^8 / 8x10^-4 ~ 7x10^11,
so the boundary anomaly is ~12 orders of magnitude too weak. The c=24 anomaly does NOT
produce the large R^2 coefficient Starobinsky inflation requires. (This is the well-known
difficulty: the Starobinsky coefficient is large, ~10^8-10^9, and is not a one-loop number.)

THE UNIFICATION OF THE RESIDUE. The three apparently-separate residual inputs are ONE:
    R^2 coefficient = M_Pl^2/(12 M^2)   <->   scalaron mass M   <->   A_s = e^-20,
all related by A_s = N^2 M^2/(24 pi^2 M_Pl^2). So the entire remaining freedom of the
cosmological tower is a SINGLE number (equivalently the large R^2 coefficient, the light
scalaron, or the amplitude exponent N/q) -- and the boundary CFT anomaly does not fix it.
The scale residue is exactly one quantity, honestly not derived.

Honest scope: a genuine NEGATIVE -- the c=24 conformal anomaly generates R^2 only at O(1)/
(4pi)^2, twelve orders below the Starobinsky coefficient, so machine=world is not promoted
to a derivation via the anomaly. The positive content is the UNIFICATION: R^2 coefficient,
scalaron mass, and A_s exponent are one number, so the tower's residue is a single input.
The anomaly normalisation c/(2880 pi^2) is order-of-magnitude (scheme-dependent); the
twelve-order gap is robust to such factors.

Verifies the Starobinsky R^2 coefficient ~6x10^8, the anomaly coefficient ~8x10^-4, the
~12-order gap, and the identity (R^2 coeff <-> M <-> A_s).
"""
from __future__ import annotations

import json
import math


def main():
    out = {}
    q = 3
    N = 60
    f = q**3 - q  # 24 = central charge
    A_s = math.exp(-20)
    M_Pl = 2.435e18  # reduced

    # scalaron mass and R^2 coefficient
    M = M_Pl * math.sqrt(24 * math.pi**2 * A_s) / N
    coeff_star = M_Pl**2 / (12 * M**2)
    print("== does the c=24 boundary anomaly generate R^2? ==")
    print(f"  scalaron mass M = M_Pl sqrt(24 pi^2 A_s)/N = {M:.3e} GeV")
    print(f"  Starobinsky R^2 coefficient M_Pl^2/(12 M^2) = {coeff_star:.3e}")
    out["starobinsky_R2"] = {
        "scalaron_mass_GeV": float(f"{M:.3e}"),
        "R2_coefficient": float(f"{coeff_star:.3e}"),
    }

    # conformal anomaly coefficient for c = 24
    coeff_anom = f / (2880 * math.pi**2)
    ratio = coeff_star / coeff_anom
    print(
        f"\n[conformal anomaly]  c = f = {f}; induced R^2 coeff ~ c/(2880 pi^2) = {coeff_anom:.3e}"
    )
    print(
        f"  ratio (Starobinsky/anomaly) = {ratio:.2e}  -> anomaly ~{math.log10(ratio):.0f} orders too weak"
    )
    assert ratio > 1e10  # robust negative
    out["conformal_anomaly"] = {
        "c": f,
        "anomaly_R2_coeff": float(f"{coeff_anom:.3e}"),
        "ratio_star_over_anomaly": float(f"{ratio:.3e}"),
        "orders_too_weak": round(math.log10(ratio), 1),
        "verdict": "c=24 anomaly does NOT generate the large Starobinsky R^2 coefficient",
    }

    # the unification: R^2 coeff <-> M <-> A_s are one number
    A_s_check = N**2 * M**2 / (24 * math.pi**2 * M_Pl**2)
    print(f"\n[residue unified]  R^2 coeff <-> scalaron M <-> A_s are ONE number:")
    print(f"  A_s = N^2 M^2/(24 pi^2 M_Pl^2) = {A_s_check:.3e}  (= e^-20 = {A_s:.3e})")
    assert abs(math.log(A_s_check) - math.log(A_s)) < 0.05
    out["residue_unified"] = {
        "identity": "A_s = N^2 M^2/(24 pi^2 M_Pl^2); R^2 coeff = M_Pl^2/12M^2",
        "one_number": "R^2 coefficient = scalaron mass = A_s exponent",
        "A_s_from_M": float(f"{A_s_check:.3e}"),
    }

    print("\nRESULT: an honest negative that unifies the residue. The substrate is")
    print(
        "  Starobinsky (R^2) inflation, but the c = f = 24 boundary conformal anomaly does"
    )
    print(
        "  NOT generate it: the anomaly induces an R^2 coefficient of order c/(2880 pi^2)"
    )
    print(
        "  ~ 8x10^-4, whereas Starobinsky needs ~ 6x10^8 (fixed by the scalaron mass M ~"
    )
    print("  2.8x10^13 GeV from A_s) -- about twelve orders of magnitude larger. So")
    print(
        "  machine=world is NOT promoted to a derivation through the boundary anomaly;"
    )
    print("  the large R^2 coefficient is a genuine input. The positive content is the")
    print(
        "  unification: the R^2 coefficient, the scalaron mass M, and the A_s exponent are"
    )
    print(
        "  the SAME single number (A_s = N^2 M^2/24 pi^2 M_Pl^2), so the entire remaining"
    )
    print(
        "  freedom of the cosmological tower is ONE quantity -- the light scalaron / large"
    )
    print(
        "  R^2 coefficient / amplitude exponent -- not the boundary central charge. The"
    )
    print(
        "  scale residue is exactly one number, honestly undetermined by the anomaly."
    )

    out["summary"] = (
        "testing whether the c=24 boundary generates R^2 -- an honest NEGATIVE that unifies "
        "the residue. The substrate is Starobinsky (R^2) inflation; its R^2 coefficient "
        "M_Pl^2/(12 M^2) ~ 6x10^8 is fixed by the scalaron mass M ~ 2.8x10^13 GeV (from A_s "
        "= N^2 M^2/24 pi^2 M_Pl^2). The conformal anomaly of the c = f = 24 boundary CFT "
        "induces an R^2 coefficient only of order c/(2880 pi^2) ~ 8x10^-4 -- about 12 orders "
        "of magnitude too weak (ratio ~ 7x10^11). So the c=24 anomaly does NOT generate the "
        "large Starobinsky coefficient, and machine=world is not promoted to a derivation "
        "via the anomaly (the large R^2 coefficient is the known model-building challenge, "
        "not a one-loop number). POSITIVE content: the R^2 coefficient, the scalaron mass M, "
        "and the A_s exponent are the SAME single number, so the entire residual freedom of "
        "the cosmological tower is ONE quantity (light scalaron / large R^2 coeff / amplitude "
        "exponent N/q), not the boundary central charge. The scale residue is exactly one "
        "number, honestly undetermined by the anomaly. The anomaly normalisation is "
        "order-of-magnitude/scheme-dependent but the 12-order gap is robust."
    )
    out["sources"] = [
        "Starobinsky R^2 inflation, A_s = N^2 M^2/(24 pi^2 M_Pl^2) (w33_starobinsky.py); "
        "scalaron mass M ~ 1.3e-5 M_Pl (COBE normalisation); conformal/trace anomaly induced "
        "R^2 ~ c/(2880 pi^2) (Birrell-Davies; Duff trace anomaly); c=f=24 boundary central "
        "charge (gravity dictionary, Monster CFT)."
    ]
    with open("data/w33_r2_anomaly.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_r2_anomaly.json")


if __name__ == "__main__":
    main()
