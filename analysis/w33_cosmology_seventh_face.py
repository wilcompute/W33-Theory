#!/usr/bin/env python3
"""
The seventh face: inflationary cosmology reads off the Eisenstein object too. The
e-fold number is N = 2(v - Phi_4) = 2 * h(E8) = 60 -- twice the E8 Coxeter number
(equivalently twice the top Witting degree) -- and the CMB observables n_s, r, f_NL,
running are functions of N and the Witting degree k=12. So the inflation sector joins
selection, constants, gauge, neutrino, code and demonstrator as a face of the one
q=3 Eisenstein structure.

The scorecard (w33_measurable_scorecard_2026.py) lists N=60 and the inflation
predictions but treats them as their own layer. This witness shows the cosmological
inputs are Eisenstein invariants:

THE E-FOLD NUMBER.
  N = 2(v - Phi_4) where v = (q+1)Phi_4 = 40 is the GQ(3,3) point count and
  Phi_4 = q^2+1 = 10; so v - Phi_4 = 40 - 10 = 30 = h(E8) = the top Witting degree
  = Phi_3+Phi_4+Phi_6 (the cyclotomic sum). Hence
      N = 2 * h(E8) = 2 * 30 = 60.
The number of e-folds is twice the E8 Coxeter number.

THE OBSERVABLES (functions of N and the Witting degree k=12 = dim SM):
  n_s        = 1 - 2/N        = 1 - 2/60   = 29/30,
  r          = k/N^2          = 12/3600    = 1/300,
  f_NL       = 5/(6N)         = 5/360      = 1/72,
  dn_s/dlnk  = -2/N^2         = -2/3600    = -1/1800.
Every cosmological prediction is a closed expression in the Eisenstein invariants
N = 2 h(E8) and k (a Witting degree).

So the inflation sector is the seventh face: the e-fold number is set by the E8
Coxeter number / the GQ point count, and the tilt, tensor ratio, non-Gaussianity and
running follow. Cosmology proper -- not just the cosmological constant -- is the
Eisenstein object seen from one more side.

Honest scope: these are the substrate's standing inflation predictions (single-field,
N=60); this witness adds that their inputs (N, k) are Witting/cyclotomic invariants,
tying the cosmology face to the same object. The observational status is in the
scorecard (all currently consistent; r and the tilt are the live handles).

Verifies N = 2(v-Phi_4) = 2 h(E8) = 60 and the four observables as closed forms.
"""
from __future__ import annotations

import json
from fractions import Fraction as F


def main():
    out = {}
    q = 3
    Phi4 = q * q + 1  # 10
    v = (q + 1) * Phi4  # 40 = GQ points
    hE8 = (q * q + q + 1) + Phi4 + (q * q - q + 1)  # 13+10+7 = 30
    k = q * (q + 1)  # 12 = Witting degree / dim SM

    # the e-fold number = 2 h(E8) = 2(v - Phi_4)
    N = 2 * (v - Phi4)
    print("[the e-fold number]")
    print(
        f"  v = (q+1)Phi_4 = {v}; Phi_4 = {Phi4}; v - Phi_4 = {v-Phi4} = h(E8) "
        f"= Phi_3+Phi_4+Phi_6"
    )
    print(f"  N = 2(v - Phi_4) = 2*h(E8) = 2*{hE8} = {N}")
    assert v - Phi4 == hE8 == 30 and N == 2 * hE8 == 60
    out["e_folds"] = {
        "N": N,
        "formula": "2(v-Phi_4) = 2 h(E8)",
        "v": v,
        "Phi_4": Phi4,
        "hE8": hE8,
    }

    # the four observables as closed forms in N and k
    n_s = 1 - F(2, N)  # 29/30
    r = F(k, N * N)  # 1/300
    f_NL = F(5, 6 * N)  # 1/72
    running = F(-2, N * N)  # -1/1800
    print("\n[the CMB observables (functions of N and k=12)]")
    print(f"  n_s        = 1 - 2/N      = {n_s}")
    print(f"  r          = k/N^2       = {r}  (k = {k} = Witting degree = dim SM)")
    print(f"  f_NL       = 5/(6N)      = {f_NL}")
    print(f"  dn_s/dlnk  = -2/N^2      = {running}")
    assert (
        n_s == F(29, 30)
        and r == F(1, 300)
        and f_NL == F(1, 72)
        and running == F(-1, 1800)
    )
    out["observables"] = {
        "n_s": "29/30 = 1-2/N",
        "r": "1/300 = k/N^2",
        "f_NL": "1/72 = 5/(6N)",
        "running": "-1/1800 = -2/N^2",
    }

    print("\n[the connection]")
    print(
        f"  N = 2 h(E8) ties inflation to the E8 Coxeter number / top Witting degree;"
    )
    print(f"  r = k/N^2 uses the Witting degree k=12=dim SM. Cosmology = a 7th face.")
    out["connection"] = (
        "N=2 h(E8)=2(v-Phi4); r uses k=12 (Witting degree); cosmology is face 7"
    )

    print("\nRESULT: inflationary cosmology is the seventh face of the q=3 Eisenstein")
    print("  object. The number of e-folds is N = 2(v - Phi_4) = 2 h(E8) = 60 -- twice")
    print("  the E8 Coxeter number (the top Witting degree, the cyclotomic sum")
    print("  13+10+7), built from the GQ point count v=40 and Phi_4=10. The spectral")
    print(
        "  tilt n_s = 1-2/N = 29/30, the tensor ratio r = k/N^2 = 1/300 (with k=12 the"
    )
    print(
        "  Witting degree = dim SM), the non-Gaussianity f_NL = 5/(6N) = 1/72, and the"
    )
    print(
        "  running -2/N^2 = -1/1800 then follow. So cosmology proper -- the inflationary"
    )
    print("  observables, not just the cosmological constant -- reads off the same")
    print("  Eisenstein invariants as selection, constants, gauge, neutrino, code and")
    print("  demonstrator: seven faces of one object.")

    out["summary"] = (
        "SEVENTH FACE -- inflationary cosmology reads off the Eisenstein object. The "
        "e-fold number N = 2(v-Phi_4) = 2 h(E8) = 60 (twice the E8 Coxeter number = the "
        "top Witting degree = cyclotomic sum 13+10+7), built from the GQ point count "
        "v=40 and Phi_4=10. The observables are closed forms in N and the Witting degree "
        "k=12=dim SM: n_s=1-2/N=29/30, r=k/N^2=1/300, f_NL=5/(6N)=1/72, running=-2/N^2="
        "-1/1800. So cosmology proper joins selection/constants/gauge/neutrino/code/"
        "demonstrator: SEVEN faces of one q=3 Eisenstein object."
    )
    out["sources"] = [
        "inflation predictions N=60, n_s=1-2/N, r=k/N^2, f_NL=5/(6N), running=-2/N^2 "
        "(w33_measurable_scorecard_2026.py, w33_inflation_dscft.py); v=(q+1)Phi_4=40, "
        "h(E8)=30=Phi_3+Phi_4+Phi_6=v-Phi_4; k=12=dim SM=Witting degree; "
        "w33_eisenstein_grand_synthesis.py, w33_gauge_sixth_face.py."
    ]
    with open("data/w33_cosmology_seventh_face.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cosmology_seventh_face.json")


if __name__ == "__main__":
    main()
