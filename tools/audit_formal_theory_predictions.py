#!/usr/bin/env python3
"""
Numerical audit of the headline "predictions" in `W33_FORMAL_THEORY.pdf`.

This script compares the W33 formulas to the experimental values *as quoted in the PDF*
and reports absolute/relative deviations and (when an uncertainty is given) the sigma gap.

Notes:
  - Many quantities here are scheme/scale dependent (e.g., α, sin²θW). Treat this as a
    bookkeeping check, not an endorsement of any physical identification.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext


getcontext().prec = 60


def _sqrt(d: Decimal) -> Decimal:
    return d.sqrt()


@dataclass(frozen=True)
class Datum:
    name: str
    predicted: Decimal
    observed: Decimal | None = None
    sigma: Decimal | None = None  # 1σ uncertainty, if available


def _fmt(d: Decimal | None, places: int = 12) -> str:
    if d is None:
        return "—"
    q = Decimal(10) ** (-places)
    return str(d.quantize(q))


def _main() -> int:
    v = Decimal("246.22")  # GeV (value used in the PDF)

    alpha_inv_pred = Decimal(81) + Decimal(56) + (Decimal(40) / Decimal(1111))
    sin2_pred = Decimal(40) / Decimal(173)
    dm_ratio_pred = Decimal(27) / Decimal(5)
    mt_pred = v * _sqrt(Decimal(40) / Decimal(81))
    mh_pred = (v / Decimal(2)) * _sqrt(Decimal(81) / Decimal(78))
    cab_pred = Decimal(9) / Decimal(40)
    koide_pred = Decimal(2) / Decimal(3)
    cosmo_pred = Decimal(121) + (Decimal(1) / Decimal(2)) + (Decimal(1) / Decimal(27))

    # Experimental values as quoted in `W33_FORMAL_THEORY.pdf`.
    data = [
        Datum(
            name="alpha^-1",
            predicted=alpha_inv_pred,
            observed=Decimal("137.035999084"),
            sigma=Decimal("0.000000021"),
        ),
        Datum(
            name="sin^2(theta_W)",
            predicted=sin2_pred,
            observed=Decimal("0.23121"),
            sigma=Decimal("0.00004"),
        ),
        Datum(
            name="Omega_DM/Omega_b",
            predicted=dm_ratio_pred,
            observed=Decimal("5.408"),
            sigma=Decimal("0.05"),
        ),
        Datum(
            name="m_t [GeV]",
            predicted=mt_pred,
            observed=Decimal("172.76"),
            sigma=Decimal("0.30"),
        ),
        Datum(
            name="m_H [GeV]",
            predicted=mh_pred,
            observed=Decimal("125.25"),
            sigma=Decimal("0.17"),
        ),
        Datum(
            name="sin(theta_C)",
            predicted=cab_pred,
            observed=Decimal("0.22501"),
            sigma=Decimal("0.00067"),
        ),
        Datum(
            name="Koide Q",
            predicted=koide_pred,
            observed=Decimal("0.666661"),
            sigma=None,
        ),
        Datum(
            name="-log10(Lambda/M_Pl^4)",
            predicted=cosmo_pred,
            observed=None,
            sigma=None,
        ),
    ]

    header = [
        "quantity",
        "predicted",
        "observed (PDF)",
        "abs diff",
        "rel diff",
        "sigma",
    ]
    rows: list[list[str]] = [header]

    for d in data:
        if d.observed is None:
            abs_diff = None
            rel_diff = None
            sigmas = None
        else:
            abs_diff = d.predicted - d.observed
            rel_diff = abs_diff / d.observed
            sigmas = (abs_diff / d.sigma) if d.sigma else None

        rows.append(
            [
                d.name,
                _fmt(d.predicted, places=12),
                _fmt(d.observed, places=12),
                _fmt(abs_diff, places=12),
                _fmt(rel_diff, places=12),
                _fmt(sigmas, places=6),
            ]
        )

    col_widths = [max(len(r[i]) for r in rows) for i in range(len(header))]
    for r_i, r in enumerate(rows):
        line = "  ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(r))
        print(line)
        if r_i == 0:
            print("  ".join("-" * w for w in col_widths))

    # Internal consistency check for the Higgs-sector gauge-boson mass step used in the PDF.
    # (The PDF states: g^2 = 4π α / sin^2θW, then mW = g v/2, mZ = mW/cosθW.)
    alpha_pred = Decimal(1) / alpha_inv_pred
    pi = Decimal(
        "3.14159265358979323846264338327950288419716939937510"
    )
    g2 = (Decimal(4) * pi * alpha_pred) / sin2_pred
    g = _sqrt(g2)
    mW = g * v / Decimal(2)
    cos2 = Decimal(1) - sin2_pred
    mZ = mW / _sqrt(cos2)
    print()
    print("Derived (using α and sin²θW above):")
    print(f"  g   = {_fmt(g, places=12)}")
    print(f"  mW  = {_fmt(mW, places=6)} GeV")
    print(f"  mZ  = {_fmt(mZ, places=6)} GeV")

    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
