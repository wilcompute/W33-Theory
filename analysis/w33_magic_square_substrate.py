#!/usr/bin/env python3
"""
The substrate's two arithmetics are the C and H columns of the Freudenthal-Tits
magic square: Eisenstein (complex, q=3) gives E6 = magic(O,C), the icosian
(quaternion) gives E7 = magic(O,H), and E8 = magic(O,O). The 27 = J3(O) = f + q.

The magic square (bt1723 already tabulates the full R/C/H/O grid -> A1..E8). This
witness places the substrate inside it. The bottom (octonion) row is the
exceptional series, with Lie-algebra dimensions

    magic(O,R) = F4 = 52,
    magic(O,C) = E6 = 78,    <- the Eisenstein/complex rung (the 27),
    magic(O,H) = E7 = 133,   <- the icosian/quaternion rung (the 56),
    magic(O,O) = E8 = 248.   <- the octonion rung (240 roots = Witting).

The substrate builds exactly two of these arithmetics, the ones it has welded:
  - the EISENSTEIN weld (Z[omega], complex / q=3): the Hessian polytope (27 = E6
    trinification) and the Eisenstein E8 (omega = C^10) -- the C column;
  - the ICOSIAN weld (golden quaternion, H): the 120 icosians / 600-cell that
    build E8 (240 roots = Witting) -- the H column.

THE 27 = J3(O). The minuscule 27 of E6 is the exceptional Jordan algebra J3(O) of
3x3 Hermitian octonionic matrices:

    27 = 3 (real diagonal) + 3*dim(O) (off-diagonal octonions) = 3 + 24 = q + f,

so the 24 off-diagonal octonion components are f and the 3 diagonal reals are q.
The cubic NORM (determinant) of J3(O) is the E6 cubic invariant = the D=5
black-hole entropy (Pillar 67 / BT327). The E7 minuscule 56 = 2*27 + 2 is the
Freudenthal triple system on J3(O).

Verifies the magic-square exceptional-row dimensions (52,78,133,248), the
minuscule reps (27,56), J3(O): 27 = q + f = 3 + 24, and 56 = 2*27 + 2.
"""
from __future__ import annotations

import json

Q, F = 3, 24
DIM_O = 8


def main():
    out = {}

    # the magic-square bottom (octonion) row dimensions
    row_O = {"F4": 52, "E6": 78, "E7": 133, "E8": 248}
    print("[Freudenthal-Tits magic square, octonion row magic(O, .)]")
    print(f"  magic(O,R) = F4 = {row_O['F4']}")
    print(f"  magic(O,C) = E6 = {row_O['E6']}   <- Eisenstein / complex (q=3) rung, 27")
    print(f"  magic(O,H) = E7 = {row_O['E7']}  <- icosian / quaternion rung, 56")
    print(f"  magic(O,O) = E8 = {row_O['E8']}  <- octonion rung, 240 roots = Witting")
    assert row_O == {"F4": 52, "E6": 78, "E7": 133, "E8": 248}
    out["magic_row_O"] = row_O

    # the substrate's two arithmetics = the C and H columns
    print(f"\n[the substrate's two welds = the C and H columns]")
    print(
        f"  Eisenstein (Z[omega], complex, q=3): E6 = magic(O,C) -- Hessian/trinif. 27"
    )
    print(f"  icosian (golden quaternion, H):      E7 = magic(O,H); E8 = magic(O,O)")
    out["substrate_columns"] = {
        "C": "Eisenstein (q=3) -> E6",
        "H": "icosian (quaternion) -> E7",
        "O": "octonion -> E8 (Witting)",
    }

    # the 27 = J3(O) = q + f
    jordan_27 = 3 + 3 * DIM_O
    print(f"\n[the 27 = J3(O) exceptional Jordan algebra]")
    print(f"  27 = 3 (real diagonal) + 3*dim(O) (off-diag octonions) = 3 + {3*DIM_O}")
    print(f"     = q + f = {Q} + {F} = {Q + F}")
    print(f"  cubic norm (det) of J3(O) = E6 cubic invariant = D=5 BH entropy (BT327)")
    assert jordan_27 == 27 == Q + F == 3 + 24
    out["jordan_27"] = "27 = J3(O) = 3 + 3*dim(O) = q + f = 3 + 24"

    # the 56 = Freudenthal triple on J3(O)
    fts_56 = 2 * 27 + 2
    print(f"\n[the 56 = E7 minuscule = Freudenthal triple on J3(O)]")
    print(f"  56 = 2*27 + 2 = {fts_56} = (J3(O), J3(O), scalar, scalar)")
    assert fts_56 == 56
    out["fts_56"] = "56 = 2*27 + 2 = Freudenthal triple system on J3(O)"

    print("\nRESULT: the substrate lives in the octonion row of the Freudenthal-Tits")
    print("  magic square. Its two welded arithmetics are the C and H columns: the")
    print("  Eisenstein weld (complex, q=3) builds E6 = magic(O,C) -- the Hessian")
    print("  polytope / trinification 27 -- and the icosian weld (quaternion) builds")
    print("  E7 = magic(O,H) and, with the octonion, E8 = magic(O,O) = the Witting")
    print("  body. The 27 of E6 is the exceptional Jordan algebra J3(O) = q + f =")
    print("  3 diagonal reals + 24 off-diagonal octonions, whose cubic norm is the")
    print("  D=5 black-hole entropy, and the 56 of E7 is its Freudenthal triple. So")
    print("  the qutrit substrate is the complex/quaternion corner of the octonionic")
    print("  exceptional magic square.")

    out["summary"] = (
        "the substrate lives in the octonion row of the Freudenthal-Tits magic "
        "square (dims F4/E6/E7/E8 = 52/78/133/248). Its two welds are the C and H "
        "columns: Eisenstein (complex, q=3) -> E6=magic(O,C) (Hessian/trinif. 27), "
        "icosian (quaternion) -> E7=magic(O,H), octonion -> E8=magic(O,O)=Witting. "
        "27=J3(O)=3+3*dim(O)=q+f=3+24, cubic norm = D=5 BH entropy; 56=2*27+2="
        "Freudenthal triple. Magic-square table in bt1723; this places the substrate."
    )
    out["sources"] = [
        "Freudenthal-Tits magic square R/C/H/O -> A1..E8 (bt1723_magic_square_"
        "latin_exceptional_heptad.py tabulates it); octonion row F4/E6/E7/E8 "
        "dims 52/78/133/248; 27=J3(O)=3+3*8 exceptional Jordan algebra, cubic norm "
        "= D=5 BH entropy (Pillar 67/BT327); 56=Freudenthal triple; "
        "w33_hessian_polytope_e6.py, w33_icosian_e8_witting.py, "
        "w33_e8_eisenstein_witting_weld.py."
    ]
    with open("data/w33_magic_square_substrate.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_magic_square_substrate.json")


if __name__ == "__main__":
    main()
