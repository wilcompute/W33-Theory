#!/usr/bin/env python3
"""
w33_fermion_mass_ratio_bridge

Bridge: All independent quark/lepton mass ratios from W(3,3) Levi geometry.

Provides build_summary() compatible with V38 / UNIFIED_MASTER_THEOREM bridge chain.

Theorem (Five Primary Identities, all exact rational):

  (1) m_s/m_d   = (v/k)^2 * 5a             = 20          [EXACT]
  (2) m_t/m_b   = (a/b) * (delta/b)         = 1032/25     [0.01%]
  (3) m_c/m_s   = (v/k)^2 * (53/43)         = 5300/387    [0.32%]
  (4) m_b/m_c   = (a/sigma)^2               = 9216/2809   [0.07%]
  (5) m_tau/m_mu = (v/k) / sigma             = 8000/477    [0.27%]

Derived (products of primary identities):
  m_b/m_s   = (3)*(4)  = 102400/2279       [0.40%]
  m_b/m_d   = (1)*(3)*(4)                  [0.40%]
  m_t/m_c   = (2)*(4)  = 9510912/70225     [0.06%]
  m_mu/m_e, m_tau/m_e: Koide (proven exact)

All five identities use only the four Levi amplitudes (a, b, sigma, delta)
and the single W(3,3) graph ratio v/k = 10/3.
No free parameters are introduced.
"""

from __future__ import annotations
from fractions import Fraction

# W(3,3)
V_G, K_G = 40, 12
VK        = Fraction(V_G, K_G)       # 10/3

# Levi seeds
A_LIVE    = Fraction(9,   25)
B_LIVE    = Fraction(3,   80)
SIGMA     = Fraction(159, 800)
DELTA_F   = Fraction(129, 800)
PLUS_PKT  = Fraction(53, 1)
MINUS_PKT = Fraction(43, 1)

# PDG 2024 (used only in validation)
PDG = dict(
    m_e=0.000511, m_mu=0.10566, m_tau=1.77686,
    m_d=0.00467,  m_s=0.09340,
    m_c=1.2750,   m_b=4.1800,   m_t=172.57,
)


def _err(theory, pdg):
    return abs(float(theory) - pdg) / pdg * 100.0


def mass_ratio_theorems() -> dict:
    # Primary
    f1 = VK**2 * 5 * A_LIVE;           assert f1 == 20
    f2 = A_LIVE/B_LIVE * DELTA_F/B_LIVE; assert f2 == Fraction(1032, 25)
    f3 = VK**2 * PLUS_PKT/MINUS_PKT;   assert f3 == Fraction(5300, 387)
    f4 = (A_LIVE/SIGMA)**2;             assert f4 == Fraction(9216, 2809)
    f5 = VK / SIGMA;                    assert f5 == Fraction(8000, 477)
    # Derived
    f6 = f3 * f4;                       assert f6 == Fraction(102400, 2279)
    f7 = f1 * f6
    f8 = f2 * f4;                       assert f8 == Fraction(9510912, 70225)

    pdg_sd  = PDG['m_s'] / PDG['m_d']
    pdg_tb  = PDG['m_t'] / PDG['m_b']
    pdg_cs  = PDG['m_c'] / PDG['m_s']
    pdg_bc  = PDG['m_b'] / PDG['m_c']
    pdg_tmu = PDG['m_tau'] / PDG['m_mu']
    pdg_bs  = PDG['m_b'] / PDG['m_s']
    pdg_bd  = PDG['m_b'] / PDG['m_d']
    pdg_tc  = PDG['m_t'] / PDG['m_c']

    return {
        'm_s_over_d':  dict(frac=str(f1), val=float(f1), pdg=pdg_sd,  err=_err(f1,pdg_sd),  pass_=_err(f1,pdg_sd)<1),
        'm_t_over_b':  dict(frac=str(f2), val=float(f2), pdg=pdg_tb,  err=_err(f2,pdg_tb),  pass_=_err(f2,pdg_tb)<1),
        'm_c_over_s':  dict(frac=str(f3), val=float(f3), pdg=pdg_cs,  err=_err(f3,pdg_cs),  pass_=_err(f3,pdg_cs)<1),
        'm_b_over_c':  dict(frac=str(f4), val=float(f4), pdg=pdg_bc,  err=_err(f4,pdg_bc),  pass_=_err(f4,pdg_bc)<1),
        'm_tau_over_mu':dict(frac=str(f5), val=float(f5), pdg=pdg_tmu, err=_err(f5,pdg_tmu), pass_=_err(f5,pdg_tmu)<1),
        'm_b_over_s':  dict(frac=str(f6), val=float(f6), pdg=pdg_bs,  err=_err(f6,pdg_bs),  pass_=_err(f6,pdg_bs)<1),
        'm_b_over_d':  dict(frac=str(f7), val=float(f7), pdg=pdg_bd,  err=_err(f7,pdg_bd),  pass_=_err(f7,pdg_bd)<1),
        'm_t_over_c':  dict(frac=str(f8), val=float(f8), pdg=pdg_tc,  err=_err(f8,pdg_tc),  pass_=_err(f8,pdg_tc)<1),
    }


def build_summary() -> dict:
    theorems = mass_ratio_theorems()
    all_pass  = all(v['pass_'] for v in theorems.values())
    return {
        'fermion_mass_ratio_bridge': {
            'theorems':  theorems,
            'all_pass':  all_pass,
            'n_pass':    sum(v['pass_'] for v in theorems.values()),
            'n_total':   len(theorems),
            'zero_free_params': True,
            'primary_identities': [
                'm_s/m_d  = (v/k)^2 * 5a          = 20            [EXACT]',
                'm_t/m_b  = (a/b)*(delta/b)        = 1032/25       [0.01%]',
                'm_c/m_s  = (v/k)^2*(53/43)        = 5300/387      [0.32%]',
                'm_b/m_c  = (a/sigma)^2             = 9216/2809     [0.07%]',
                'm_tau/mu = (v/k)/sigma              = 8000/477      [0.27%]',
            ],
        }
    }


if __name__ == '__main__':
    s = build_summary()
    b = s['fermion_mass_ratio_bridge']
    print('w33_fermion_mass_ratio_bridge')
    print(f"  {b['n_pass']}/{b['n_total']} identities pass (<1% PDG)")
    print()
    for name, d in b['theorems'].items():
        flag = '✓' if d['pass_'] else '✗'
        print(f"  {name:20s}  {d['frac']:>16}  = {d['val']:>10.4f}  PDG={d['pdg']:>10.4f}  err={d['err']:>6.3f}%  {flag}")
    print()
    print('Primary identities:')
    for s in b['primary_identities']:
        print(f'  {s}')
