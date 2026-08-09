#!/usr/bin/env python3
"""Passes 4411-4412 -- what the neutrino derivation actually fixes, and the scoreboard re-scored.

Pass 4401 found the Sigma m_nu prediction excluded in LCDM.  Pass 4402 worked out what it
implies for the mass ordering.  Neither asked the prior question: WHAT IS THE DERIVATION?

It is this, from `w33_BREAKTHROUGH_127_Trh_reheating_closure.py`:

    Sigma m_nu = (Phi_4^2 + 1) meV,   Phi_4 = q^2 + 1 = 10,   q = 3
               = (100 + 1) meV = 101 meV

So the geometry supplies the INTEGER 101.  The unit -- meV -- is supplied by hand.  The
repository already has a section warning about exactly this, "The Measured-Constant Layer
is Unit-Gauge Only", and this prediction sits squarely inside that warning.  Two things
follow, and the second is testable:

  4411a  A SUM CANNOT FIX AN ORDERING.  Pass 4402's inverted-ordering reading is an
         interpretation of the number, not a consequence of the derivation. Nothing in
         (q^2+1)^2 + 1 distinguishes m1 < m2 < m3 from m3 < m1 < m2. So the JUNO test
         proposed at 4402 tests a reading, not the theory.

  4411b  LOOK ELSEWHERE.  If many simple expressions in this geometry's standard constants
         land inside the physically allowed window, then hitting it is not evidence. This
         is measurable: enumerate the small expressions and count. It is the one check that
         can turn "101 is remarkable" into a number, and it has not been run.

  4412   The rest of the scoreboard, re-scored against 2026 bounds the way F16 was.

    py -3 analysis/w33_pass4411_4412_what_the_derivation_fixes.py
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

# The geometry's standard constants, as they appear across the repository.
CONSTANTS = {
    "q": 3, "v": 40, "k": 12, "lambda": 2, "mu": 4,
    "Phi_3": 13, "Phi_4": 10, "Phi_6": 7,
    "f": 24, "g": 15, "lines": 40, "flags": 160,
    "27": 27, "36": 36, "45": 45, "81": 81, "e6": 27, "spread": 40,
}

# The window a prediction had to land in to look successful when it was written:
# above the normal-ordering oscillation floor, below the then-current Planck bound.
WINDOW = (59.0, 120.0)          # meV

BOUNDS_NOW = (64.2, 163.0)      # LCDM / w0waCDM, meV, from Pass 4401


def expressions():
    """Small arithmetic expressions on the constants: a, a+-b, a*b, a^2+-b, (a+-b)^2+-c."""
    seen = {}
    items = sorted(set(CONSTANTS.values()))
    for a in items:
        for form, val in ((f"{a}", a), (f"{a}^2", a * a), (f"{a}^2+1", a * a + 1),
                          (f"{a}^2-1", a * a - 1), (f"2*{a}", 2 * a), (f"3*{a}", 3 * a)):
            seen.setdefault(val, form)
    for a, b in itertools.permutations(items, 2):
        for form, val in ((f"{a}+{b}", a + b), (f"{a}-{b}", a - b),
                          (f"{a}*{b}", a * b), (f"{a}^2+{b}", a * a + b),
                          (f"{a}^2-{b}", a * a - b), (f"({a}+{b})^2", (a + b) ** 2),
                          (f"{a}*{b}+1", a * b + 1), (f"{a}*{b}-1", a * b - 1)):
            if 0 < val < 1000:
                seen.setdefault(val, form)
    return seen


def main() -> int:
    print("=" * 78)
    print("Passes 4411-4412 -- what the derivation fixes, and the rest of the scoreboard")
    print("=" * 78)

    print(f"""
  PASS 4411a -- THE DERIVATION IS AN INTEGER TIMES A CHOSEN UNIT.

      Sigma m_nu = (Phi_4^2 + 1) meV = ((q^2+1)^2 + 1) meV = 101 meV,  q = 3

  The geometry supplies 101. The meV is put in by hand: nothing in W(3,3) carries a mass
  scale, and the repository's own section "The Measured-Constant Layer is Unit-Gauge Only"
  says why that matters. Any dimensionless integer can be made to match any measured
  quantity by a choice of unit, so the content of the prediction is entirely in the
  INTEGER and in the claim that meV is the right scale -- and the second half is not
  derived anywhere.

  AND A SUM CANNOT FIX AN ORDERING. Pass 4402 read 101 meV as nearly "inverted ordering
  with a massless lightest state", and proposed JUNO as an independent test. That reading
  is mine, not the derivation's: (q^2+1)^2 + 1 says nothing about which of m1, m2, m3 is
  smallest. The JUNO test would test my interpretation. I am withdrawing the implication
  that it tests the theory.""")

    # ---- 4411b: look elsewhere --------------------------------------------
    ex = expressions()
    lo, hi = WINDOW
    inside = {v: f for v, f in ex.items() if lo <= v <= hi}
    inside_now = {v: f for v, f in ex.items() if lo <= v <= BOUNDS_NOW[0]}
    print(f"\n  PASS 4411b -- LOOK ELSEWHERE\n")
    print(f"    distinct integers reachable by a small expression : {len(ex)}")
    print(f"    landing in the ORIGINAL window {lo:.0f}-{hi:.0f} meV        : {len(inside)}"
          f"   ({100 * len(inside) / len(ex):.1f}% of all reachable values)")
    print(f"    landing in the CURRENT LCDM window {lo:.0f}-{BOUNDS_NOW[0]:.1f} meV     : "
          f"{len(inside_now)}")
    sample = sorted(inside.items())[:14]
    print(f"\n    a sample of the {len(inside)} that would have 'worked' equally well:")
    print("      " + ",  ".join(f"{v} = {f}" for v, f in sample))

    density = len(inside) / (hi - lo + 1)
    print(f"""
    {len(inside)} of the {len(ex)} integers reachable by these small expressions fall inside the window
    the prediction had to hit -- a density of {density:.2f} per meV across a 62 meV window. Landing
    somewhere in that window is therefore not surprising on its own, and "101 = Phi_4^2 + 1"
    is not evidence at the strength the scoreboard's 1e-3 precision column implies.

    WHAT WOULD MAKE IT EVIDENCE, STATED CONSTRUCTIVELY. Either a derivation of the SCALE --
    a seesaw with M_R fixed by the geometry rather than a unit chosen to fit -- or a second,
    independent geometric quantity predicting the individual masses or the ordering. Both
    are real research programmes and neither is done. Until one is, this row belongs in the
    "candidate" column the original file honestly put it in, and the sharp reading Pass 4402
    gave it is not supported.""")

    # ---- 4412: the rest of the scoreboard ---------------------------------
    print("\n  PASS 4412 -- the other rows, re-scored\n")
    rows = [
        ("F7  m_H", "125 GeV = (mu+1)^q = 5^3", 125.0, "125.20 +/- 0.11 GeV (PDG)",
         "1.8 sigma LOW -- the tightest live tension on the board"),
        ("F9  r", "2/90 = 0.02222", 0.02222, "r < 0.034 (95%, Planck+SPT+ACT+BK, 2025)",
         "ALLOWED; headroom fell from 0.036 to 0.034 and LiteBIRD reaches 1e-3"),
        ("F10 m_chi WIMP", "2143 GeV", 2143.0,
         "XENONnT 3.1 t-yr: 1.7e-47 cm^2 min at 30 GeV; far weaker at 2 TeV",
         "NOT YET CONSTRAINED at this mass -- the row's own note is still right"),
        ("F16 Sigma m_nu", "101 meV", 101.0, "DESI DR2 + CMB: < 64.2 meV (LCDM, 95%)",
         "EXCLUDED in LCDM (Pass 4401); allowed only under w0waCDM"),
        ("Koide Q", "2/3", 2 / 3, "0.666660511 +/- 0.000006775 (PDG masses)",
         "HOLDS at 0.91 sigma (Pass 4406); limited entirely by the tau mass"),
    ]
    for tag, pred, _, obs, verdict in rows:
        print(f"    {tag:16s} predicts {pred:26s}")
        print(f"    {'':16s} measured {obs}")
        print(f"    {'':16s} -> {verdict}\n")

    print("""    TWO ROWS HAVE MOVED SINCE THE BOARD WAS WRITTEN AND ONE IS NOW IN TENSION.
    F16 is excluded in the standard cosmology. F7 -- the Higgs mass as exactly 5^3 GeV --
    is 1.8 sigma below the world average, which was not true when 125.09 +/- 0.24 was the
    number; the measurement moved up and its error shrank by a factor of two. That is the
    row to watch, because unlike F16 it has no model-dependence to hide behind: the Higgs
    mass is a direct measurement and HL-LHC will halve the error again.""")

    out = {
        "boundary": ("4411b's look-elsewhere count depends on the expression grammar "
                     "chosen, which is a judgement; a different grammar gives a different "
                     "density. The point survives the choice -- the window is crowded -- "
                     "but the specific number is not a unique measurement. 4412 re-scores "
                     "published bounds and derives nothing"),
        "pass_4411_derivation": {
            "formula": "(Phi_4^2 + 1) meV with Phi_4 = q^2 + 1 = 10",
            "geometry_supplies": 101,
            "unit_supplied_by": "hand -- no mass scale is derived anywhere in W(3,3)",
            "fixes_ordering": False,
            "withdrawn": ("Pass 4402's implication that JUNO tests the theory; JUNO tests "
                          "an interpretation of the number that the derivation does not "
                          "make"),
        },
        "pass_4411b_look_elsewhere": {
            "reachable_integers": len(ex),
            "window_meV": list(WINDOW),
            "hits_in_window": len(inside),
            "density_per_meV": round(density, 4),
            "hits_in_current_LCDM_window": len(inside_now),
            "conclusion": ("the window the prediction had to hit contains "
                           f"{len(inside)} values reachable by comparably simple "
                           "expressions, so landing in it is not evidence at the "
                           "precision the scoreboard claims"),
        },
        "pass_4412_rescored": [{"row": t, "predicts": p, "measured": o, "verdict": v}
                               for t, p, _, o, v in rows],
        "sources": [
            "r: Planck + SPT + ACT + BICEP/Keck, r < 0.034 (95%), 2025",
            "WIMP: XENONnT 3.1 tonne-year, arXiv:2502.18005",
            "Sigma m_nu: DESI DR2, arXiv:2503.14738 / 2503.14744",
            "m_H, lepton masses: PDG",
        ],
    }
    p = ROOT / "data" / "PART_W33_PASS4411_4412_DERIVATION_AND_BOARD.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
