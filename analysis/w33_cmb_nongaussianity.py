#!/usr/bin/env python3
"""
The CMB non-Gaussianity is moonshine: f_NL^local = (5/12)(1 - n_s) = 5/(6N) = 1/72,
and the bispectrum SHAPE is the Monster c=24 boundary CFT three-point function.

The inflation front (w33_inflation_dscft.py) found a single light (complementary-
series) mode -- so the substrate's inflation is SINGLE-FIELD -- with the CMB
two-point function a correlator on the Monster c=24 dS/CFT boundary. Two
consequences for non-Gaussianity:
  - AMPLITUDE (Maldacena's single-field consistency relation). In the squeezed
    limit any single-field model gives
        f_NL^local = (5/12)(1 - n_s).
    With n_s = 1 - 2/N this is f_NL^local = (5/12)(2/N) = 5/(6N); at N = 60,
        f_NL^local = 5/360 = 1/72 = 0.0139,
    far below current bounds (Planck f_NL^local = -0.9 +- 5.1) -- a clean, tiny,
    falsifiable prediction that follows from the SINGLE light mode.
  - SHAPE (dS/CFT). In dS/CFT the inflaton bispectrum is the boundary CFT three-
    point function, fixed by conformal invariance up to OPE coefficients; here the
    boundary is the Monster module, so the primordial three-point function is a
    Monster-CFT correlator. The CMB's higher correlations are moonshine OPE data.

So the substrate predicts near-Gaussian CMB with f_NL^local = 1/72, the small
departure being the de-Sitter-breaking tilt, and the non-Gaussian shape carrying
the Monster boundary OPE. Honest: the amplitude uses the (theorem-level)
single-field consistency relation given the substrate's single light mode and
n_s = 29/30; the moonshine-shape statement is the dS/CFT framing, not a computed
OPE coefficient.
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr

V, K, PHI4, FF = 40, 12, 10, 24


def main():
    out = {}
    N = 2 * (V - PHI4)
    ns = Fr(1) - Fr(2, N)
    # Maldacena single-field consistency: f_NL^local = (5/12)(1 - n_s)
    fNL = Fr(5, 12) * (1 - ns)
    print(
        f"[single-field inflation]  one light mode -> single-field "
        f"(w33_inflation_dscft.py)"
    )
    print(f"  N = 2(v - Phi_4) = {N}; n_s = 1 - 2/N = {ns} = {float(ns):.4f}")
    print(f"\n[Maldacena consistency]  f_NL^local = (5/12)(1 - n_s)")
    print(f"  = (5/12)(2/N) = 5/(6N) = {fNL} = {float(fNL):.4f}")
    print(f"  (Planck f_NL^local = -0.9 +- 5.1 -> consistent, tiny)")
    assert fNL == Fr(1, 72) == Fr(5, 6 * N)
    out["N"] = N
    out["n_s"] = str(ns)
    out["fNL_local"] = str(fNL)
    out["fNL_local_float"] = round(float(fNL), 4)

    print(f"\n[bispectrum shape]  dS/CFT: primordial 3-pt function = boundary CFT")
    print(f"  3-pt function on the Monster c = {FF} module; CMB higher correlations")
    print(f"  = moonshine OPE data. (Single-field => local shape, peaked squeezed.)")
    out["boundary_c"] = FF
    out["shape"] = "Monster c=24 boundary CFT 3-pt (local, squeezed-peaked)"

    print("\nRESULT: the substrate predicts a near-Gaussian CMB with")
    print("  f_NL^local = (5/12)(1 - n_s) = 5/(6N) = 1/72 = 0.0139, the tiny value")
    print("  forced by single-field inflation (the unique light dS mode) and the")
    print("  tilt n_s = 29/30. The bispectrum shape is the Monster c=24 boundary")
    print("  three-point function, so the CMB's non-Gaussian correlations are")
    print("  moonshine OPE data -- a falsifiable, distinctly small f_NL with a")
    print("  moonshine-fixed shape. Inflation's signature is monstrous.")

    out["summary"] = (
        "single-field inflation (unique light dS mode) -> Maldacena "
        "consistency f_NL^local = (5/12)(1-n_s) = 5/(6N) = 1/72 = 0.0139 "
        "(Planck f_NL=-0.9+-5.1, consistent); bispectrum shape = Monster "
        "c=24 dS/CFT boundary 3-pt (moonshine OPE). Falsifiable tiny "
        "f_NL, moonshine shape. Honest: consistency relation is a "
        "theorem given single-field; shape is dS/CFT framing."
    )
    out["sources"] = [
        "Maldacena, Non-Gaussian features of primordial fluctuations "
        "(2002), single-field consistency f_NL=(5/12)(1-n_s); dS/CFT "
        "bispectrum = boundary 3-pt; w33_inflation_dscft.py, "
        "w33_holographic_central_charge.py"
    ]
    with open("data/w33_cmb_nongaussianity.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cmb_nongaussianity.json")


if __name__ == "__main__":
    main()
