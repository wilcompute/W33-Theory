"""
KAC-MOODY / AFFINE E8: central charge and vacuum shift utilities.

Provides small helpers to compute the Sugawara central charge for the
affine Lie algebra E8 at level `k` and the corresponding vacuum shift
`-c/24`. Also compares the level-1 vacuum shift with the affine E8
character computed in `w33_affine_e8`.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json

from w33_affine_e8 import affine_e8_series


def central_charge_E8(k: int) -> Fraction:
    """Return the Sugawara central charge c = k * dim(g) / (k + h^vee)

    For E8: dim(g)=248, h^vee=30.
    """
    return Fraction(248 * k, k + 30)


def vacuum_shift_for_k(k: int) -> Fraction:
    """Return the vacuum shift -c/24 as a Fraction for level `k`."""
    c = central_charge_E8(k)
    return -c / 24


def derive_all_kac_moody(k: int = 1, q_order: int = 10) -> dict:
    """Produce a JSON-serializable report comparing Sugawara data with
    the affine E8 character computation.
    """
    c = central_charge_E8(k)
    shift = vacuum_shift_for_k(k)
    # affine_e8_series returns {'shift': Fraction, 'series': [...]}
    affine = affine_e8_series(q_order=q_order)
    return {
        "k": k,
        "central_charge": str(c),
        "vacuum_shift": str(shift),
        "affine_shift": str(affine["shift"]),
        "summary_chain": {
            "sugawara_shift_matches_affine_level1": (k == 1 and affine["shift"] == shift),
            "leading_affine_coeff_is_one": affine["series"][0] == 1,
        },
    }


def main() -> None:
    out = derive_all_kac_moody(k=1, q_order=10)
    p = Path(__file__).resolve().parent.parent / "data" / "w33_kac_moody_e8.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"Wrote {p}")


if __name__ == "__main__":
    main()
