#!/usr/bin/env python3
"""
V38: Fermion Mass Hierarchy from Levi Yukawa Tower

Goal: Derive quark and lepton MASS RATIOS from the same Levi geometry
      that gave all mixing angles in V37.

The Yukawa tower was constructed in V31-V33:
  V31: Yukawa couplings from L3 spectral layer
  V32: Tower Yukawa structure
  V33: Sector Yukawa assignments

The Levi amplitude packet (a, b, sigma, delta) with
  a = 9/25,  b = 3/80,  sigma = 159/800,  delta = 129/800

should generate mass ratios through the tower eigenvalue cascade.

Working hypothesis:
  The three generations correspond to the three Levi-tower levels:
    m_1 ~ delta  (lightest: Levi minus-packet weight)
    m_2 ~ sigma  (middle:  Levi plus-packet weight)
    m_3 ~ a      (heaviest: full live selector scale)

From these seeds the inter-generation ratios are:
  m_2/m_1 = sigma/delta = 159/129 = 53/43 ~ 1.23  (tau/mu: PDG ~ 16.8 -- too small)
  m_3/m_1 = a/delta     = (9/25)/(129/800) = 7200/3225 = 480/215 = 96/43 ~ 2.23

These raw ratios are O(1) -- the physical mass hierarchy (10^5 between e and t)
requires iteration of the tower: each generation is suppressed by lambda^2 = (9/40)^2
relative to the next.

Generation suppression cascade:
  m_1/m_3 ~ (lambda)^(2*n)  where n is the number of tower steps.

For quarks:
  m_t/m_b ~ a/b = (9/25)/(3/80) = 9*80/(25*3) = 720/75 = 48/5 = 9.6
  PDG: m_t/m_b ~ 171/4.2 ~ 40.7  (ratio of 4.25x too small)

  With spectral correction sqrt(53/43):
  m_t/m_b ~ (a/b)*sqrt(53/43) ~ 9.6 * 1.11 ~ 10.66  (still 3.8x too small)

  The tower cascade: m_t ~ a,  m_b ~ b * (sigma/delta) = b * 53/43
  m_t/m_b = a / (b * 53/43) = (a/b) * (43/53) = 9.6 * 0.811 = 7.78  (worse)

  OPEN: The quark mass hierarchy requires additional tower iterations.
  The correct extraction uses the full Yukawa report from V33.

This scaffold:
1. Reads V33 sector Yukawa report
2. Tests generation-ratio hypotheses against PDG mass ratios
3. Maps the open bridges needed for a complete derivation
4. Reports which ratios are already within 10% and which require new bridges
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Exact Levi seeds
A_LIVE   = Fraction(9, 25)
B_LIVE   = Fraction(3, 80)
SIGMA    = Fraction(159, 800)
DELTA_F  = Fraction(129, 800)
LAMBDA   = Fraction(9, 40)
PLUS_PKT = Fraction(53, 1)
MINUS_PKT= Fraction(43, 1)

a  = float(A_LIVE)
b  = float(B_LIVE)
sg = float(SIGMA)
dl = float(DELTA_F)
lam= float(LAMBDA)

# PDG 2024 mass ratios (dimensionless, scheme-independent where possible)
# Using MS-bar masses at 2 GeV for light quarks, pole masses for heavy
PDG_MASS_RATIOS = {
    # Charged leptons
    'm_mu_over_m_e':     206.768,
    'm_tau_over_m_mu':   16.817,
    'm_tau_over_m_e':    3477.2,
    # Up-type quarks (MS-bar at MZ)
    'm_c_over_m_u':      500.0,    # approximate
    'm_t_over_m_c':      228.0,    # m_t(pole)/m_c(MS)
    'm_t_over_m_u':      114000.,  # approximate
    # Down-type quarks
    'm_s_over_m_d':      18.9,
    'm_b_over_m_s':      44.3,
    'm_b_over_m_d':      850.,
    # Cross-type
    'm_t_over_m_b':      40.7,     # pole masses
    'm_b_over_m_c':      3.74,
}


def levi_mass_ratio_hypotheses() -> list[dict]:
    """Test all natural Levi-amplitude mass ratio hypotheses against PDG."""
    results = []

    # Level amplitudes
    levels = {
        'a':     a,
        'b':     b,
        'sigma': sg,
        'delta': dl,
        'lam':   lam,
        'lam^2': lam**2,
        'lam^4': lam**4,
        'a/b':   a/b,
        'sigma/delta': sg/dl,
        'a/sigma': a/sg,
        'a/delta': a/dl,
        'sigma/b': sg/b,
        'delta/b': dl/b,
        'sqrt(a/b)': np.sqrt(a/b),
        '(a/b)^2': (a/b)**2,
        '(a/b)^3': (a/b)**3,
    }

    # Test each pair
    for obs, pdg_val in PDG_MASS_RATIOS.items():
        best_err  = 1e9
        best_expr = None
        best_theory = None
        for expr, val in levels.items():
            if val <= 0: continue
            err = abs(val - pdg_val) / pdg_val * 100
            if err < best_err:
                best_err   = err
                best_expr  = expr
                best_theory = val
        # Also test products and powers
        for e1, v1 in levels.items():
            for e2, v2 in levels.items():
                for combo, val in [
                    (f'{e1}*{e2}', v1*v2),
                    (f'{e1}/{e2}', v1/v2 if v2>0 else 1e9),
                    (f'1/{e2}', 1.0/v2 if v2>0 else 1e9),
                ]:
                    if val <= 0 or val > 1e8: continue
                    err = abs(val - pdg_val) / pdg_val * 100
                    if err < best_err:
                        best_err   = err
                        best_expr  = combo
                        best_theory = val

        results.append({
            'observable': obs,
            'pdg': pdg_val,
            'best_levi_expr': best_expr,
            'best_levi_value': round(best_theory, 4) if best_theory else None,
            'err_pct': round(best_err, 2),
            'pass_10pct': bool(best_err < 10.0),
        })
    return results


def tower_cascade() -> dict:
    """
    Test the generation-suppression cascade:
    Each generation is lighter than the next by a factor of lambda^2 in amplitude
    => lambda^4 in mass (squared coupling).
    """
    # Three-generation cascade
    # Heaviest: m_3 ~ a
    # Middle:   m_2 ~ a * lam^4
    # Lightest: m_1 ~ a * lam^8
    m3 = a
    m2 = a * lam**4
    m1 = a * lam**8

    ratio_32 = m3 / m2   # = 1/lam^4 ~ (40/9)^4 ~ 390
    ratio_21 = m2 / m1   # = 1/lam^4 ~ 390
    ratio_31 = m3 / m1   # = 1/lam^8 ~ 152100

    # Compare to PDG:
    # tau/mu ~ 16.8,  m_t/m_c ~ 228,  m_t/m_b ~ 40.7
    return {
        'cascade_model': 'm_i ~ a * lam^(4*(3-i))',
        'm3_m2_ratio': round(ratio_32, 1),
        'm2_m1_ratio': round(ratio_21, 1),
        'm3_m1_ratio': round(ratio_31, 1),
        'pdg_tau_mu': 16.817,
        'pdg_t_c':    228.0,
        'pdg_t_u':    114000.,
        'note': (
            'The lam^4 cascade gives inter-generation ratio ~390, '
            'which is too large for adjacent leptons (tau/mu~16.8) '
            'but in the right ballpark for quark hierarchies. '
            'The lepton hierarchy uses lam^2 steps; '
            'the quark hierarchy uses a mix of lam^2 and Levi packet ratios. '
            'Full derivation requires the Yukawa V33 sector report.'
        ),
    }


def load_v33_report() -> dict | None:
    p = DATA_DIR / 'V33_sector_yukawa_report.json'
    if p.exists():
        return json.loads(p.read_text())
    return None


def main() -> None:
    print('=' * 72)
    print('V38: FERMION MASS HIERARCHY FROM LEVI YUKAWA TOWER')
    print('=' * 72)
    print()
    print('Levi seeds:')
    print(f'  a={A_LIVE}={a:.5f}  b={B_LIVE}={b:.5f}')
    print(f'  sigma={SIGMA}={sg:.5f}  delta={DELTA_F}={dl:.5f}')
    print(f'  lambda={LAMBDA}={lam:.5f}  lam^2={lam**2:.5f}')
    print()

    # Generation cascade
    cascade = tower_cascade()
    print('Generation cascade (lam^4 suppression per step):')
    print(f"  m3/m2 = 1/lam^4 = {cascade['m3_m2_ratio']}  (PDG tau/mu={cascade['pdg_tau_mu']}, t/c={cascade['pdg_t_c']})")
    print(f"  m3/m1 = 1/lam^8 = {cascade['m3_m1_ratio']}  (PDG t/u~{cascade['pdg_t_u']:.0f})")
    print()

    # Best Levi hypotheses
    hypotheses = levi_mass_ratio_hypotheses()
    pass_count = sum(h['pass_10pct'] for h in hypotheses)
    print(f'Best Levi amplitude matches for mass ratios ({pass_count}/{len(hypotheses)} within 10%):')
    print(f"  {'Observable':<22} {'PDG':>10} {'Levi expr':<20} {'Theory':>10} {'Err%':>8}  ")
    print(f"  {'-'*22}  {'-'*10}  {'-'*20}  {'-'*10}  {'-'*8}  ")
    for h in hypotheses:
        ok = '✓' if h['pass_10pct'] else '○'
        print(f"  {h['observable']:<22} {h['pdg']:>10.2f}  "
              f"{h['best_levi_expr']:<20} {h['best_levi_value']:>10.4f} "
              f"{h['err_pct']:>7.1f}%  {ok}")
    print()

    # V33 Yukawa report
    v33 = load_v33_report()
    if v33:
        print('V33 Yukawa report found -- cross-referencing sector assignments...')
        # Print sector summary if available
        if 'sectors' in v33:
            for sec, data in v33['sectors'].items():
                print(f'  Sector {sec}: {data}')
    else:
        print('V33 Yukawa report not found in data/ -- run V33_SECTOR_YUKAWA.py first.')

    print()
    print('=' * 72)
    print(f'OPEN BRIDGES NEEDED:')
    fails = [h for h in hypotheses if not h['pass_10pct']]
    for h in fails:
        print(f"  {h['observable']:<25} (best err {h['err_pct']:.1f}%) -- "
              f"needs Yukawa tower iteration bridge")
    print('=' * 72)

    # Save report
    report = {
        'levi_seeds': {'a': str(A_LIVE), 'b': str(B_LIVE),
                       'sigma': str(SIGMA), 'delta': str(DELTA_F),
                       'lambda': str(LAMBDA)},
        'generation_cascade': cascade,
        'mass_ratio_hypotheses': hypotheses,
        'pass_count': pass_count,
        'total': len(hypotheses),
        'status': 'scaffold -- full derivation requires Yukawa tower bridge chain',
    }
    out = ROOT / 'V38_fermion_mass_hierarchy_report.json'
    out.write_text(json.dumps(report, indent=2))
    print(f'\nReport: {out.name}')


if __name__ == '__main__':
    main()
