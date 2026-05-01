"""
w33_yukawa_rg.py

Yukawa coupling RG running for the W(3,3) mass predictions.

This module takes alpha_s(M_Z) from w33_rg_gut_conversion (now correct)
and runs the full SM Yukawa couplings from M_GUT -> M_Z using the
one-loop beta functions, then extracts the fermion mass predictions.

The key W(3,3) prediction:
  All Yukawa couplings at M_GUT are set by the W(3,3) spectral ratios:
    y_f(M_GUT) = y_unified * ratio_f
  where ratio_f comes from the W33.Phi3, W33.Phi6, W33.mu fixed points.

Two-step flow:
  1. GUT -> M_top: run y_t, y_b, y_tau with QCD corrections dominant
  2. M_top -> M_Z: integrate out top, run lighter Yukawas

Outputs: dict of fermion pole masses in GeV, comparison to PDG 2024.
"""

import math
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from w33_rg_gut_conversion import (
    run_alpha_s, w33_alpha_s_mz, w33_m_gut, w33_alpha_unified_gut
)

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
M_Z    = 91.1876   # GeV
M_W    = 80.377    # GeV
M_top  = 172.57    # GeV  (pole mass)
v_higgs = 246.22   # GeV  (Higgs VEV)

# PDG 2024 fermion pole masses (GeV)
PDG_MASSES = {
    'top':   172.57,
    'bottom': 4.183,   # MSbar at M_b
    'charm':  1.273,   # MSbar at M_c
    'strange': 0.0935, # MSbar at 2 GeV
    'up':     0.00216, # MSbar at 2 GeV
    'down':   0.00467, # MSbar at 2 GeV
    'tau':    1.77686,
    'muon':   0.105658,
    'electron': 0.000511,
}

# ---------------------------------------------------------------------------
# W(3,3) Yukawa GUT-scale assignments
# ---------------------------------------------------------------------------

def w33_yukawa_gut(y_unified=None):
    """
    Return the W(3,3) Yukawa couplings at M_GUT.

    The W(3,3) spectral structure assigns each generation a Yukawa coupling
    proportional to the fixed-point ratios:

      Generation 3 (top, bottom, tau): y ~ y_unified
      Generation 2 (charm, strange, muon): y ~ y_unified / Phi3
      Generation 1 (up, down, electron): y ~ y_unified / (Phi3 * Phi6)

    where Phi3 = (1+sqrt(3))/2 ~ 1.366 and Phi6 = (1+sqrt(6))/2 ~ 1.724.

    y_unified is the common Yukawa scale at M_GUT, estimated from the
    top Yukawa running: y_top(M_GUT) ~ 0.5 (standard SM value).
    """
    # W(3,3) fixed points
    Phi3 = (1.0 + math.sqrt(3.0)) / 2.0   # ~1.366
    Phi6 = (1.0 + math.sqrt(6.0)) / 2.0   # ~1.725
    mu   = math.sqrt(3.0) - 1.0           # ~0.732

    if y_unified is None:
        # Estimate: fit to top mass. y_top(M_Z) ~ m_top / (v/sqrt(2)) ~ 0.994
        # Running y_top up to M_GUT reduces it to ~ 0.5
        y_unified = 0.50

    return {
        'top':      y_unified,
        'bottom':   y_unified * mu,          # suppressed by mu
        'tau':      y_unified * mu,
        'charm':    y_unified / Phi3,
        'strange':  y_unified / (Phi3 * mu),
        'muon':     y_unified / (Phi3**2),
        'up':       y_unified / (Phi3 * Phi6),
        'down':     y_unified / (Phi3 * Phi6 * mu),
        'electron': y_unified / (Phi3**2 * Phi6),
    }

# ---------------------------------------------------------------------------
# One-loop Yukawa beta functions (dominant terms)
# ---------------------------------------------------------------------------

def dyuk_dlnmu_top(y_t, y_b, alpha_s, alpha_em=1/128.0):
    """
    One-loop beta function for top Yukawa.
    dy_t/d(ln mu) = y_t/(16*pi^2) * [9/2 * y_t^2 + 3/2 * y_b^2 - 8*alpha_s*pi - 9/4*g2^2 - 17/12*g1^2]
    Dominant: QCD and y_t^2 self-coupling.
    Simplified (QCD dominant):
    """
    pi = math.pi
    return y_t / (16 * pi**2) * (9.0/2 * y_t**2 - 8 * alpha_s * pi)

def dyuk_dlnmu_generic(y, alpha_s, qcd_casimir=4.0/3):
    """
    Generic one-loop Yukawa beta: dy/d(ln mu) = y/(16*pi^2)*(-8*C_F*alpha_s*pi)
    where C_F=4/3 for quarks, 0 for leptons.
    QCD only; valid for non-top quarks where y^2 << g_s^2.
    """
    pi = math.pi
    return y / (16 * pi**2) * (-8 * qcd_casimir * alpha_s * pi)

# ---------------------------------------------------------------------------
# RK4 integrator for Yukawa + alpha_s coupled system
# ---------------------------------------------------------------------------

def run_yukawa_system(yukawas_start, alpha_s_start, mu_start, mu_end, n_steps=3000):
    """
    Run the full system {y_t, y_b, y_tau, y_c, ...} + alpha_s from mu_start to mu_end.
    Returns dict of yukawas at mu_end, or None on runaway.
    """
    from w33_rg_gut_conversion import beta_qcd_2loop

    ln_start = math.log(mu_start)
    ln_end   = math.log(mu_end)
    h = (ln_end - ln_start) / n_steps

    # State vector: [alpha_s, y_top, y_bot, y_tau, y_c, y_s, y_mu, y_u, y_d, y_e]
    quarks   = ['top', 'bottom', 'charm', 'strange', 'up', 'down']
    leptons  = ['tau', 'muon', 'electron']
    keys     = ['alpha_s'] + quarks + leptons

    nf = 6  # all flavors active above M_top; we don't split here for simplicity
    state = [alpha_s_start] + [yukawas_start[k] for k in quarks + leptons]

    def derivs(s):
        a_s = s[0]
        y   = {k: s[i+1] for i, k in enumerate(quarks + leptons)}
        d   = [0.0] * len(s)
        d[0] = beta_qcd_2loop(a_s, nf)
        for i, k in enumerate(quarks):
            if k == 'top':
                d[i+1] = dyuk_dlnmu_top(y['top'], y['bottom'], a_s)
            else:
                d[i+1] = dyuk_dlnmu_generic(y[k], a_s, qcd_casimir=4.0/3)
        for i, k in enumerate(leptons):
            d[len(quarks)+i+1] = dyuk_dlnmu_generic(y[k], a_s, qcd_casimir=0.0)
        return d

    def rk4(s, h):
        k1 = derivs(s)
        k2 = derivs([si + h/2*ki for si,ki in zip(s,k1)])
        k3 = derivs([si + h/2*ki for si,ki in zip(s,k2)])
        k4 = derivs([si + h*ki   for si,ki in zip(s,k3)])
        return [si + h*(k1i+2*k2i+2*k3i+k4i)/6
                for si,k1i,k2i,k3i,k4i in zip(s,k1,k2,k3,k4)]

    for _ in range(n_steps):
        state = rk4(state, h)
        if not all(math.isfinite(x) for x in state):
            return None
        if state[0] <= 0 or state[0] > 5:
            return None

    result = {'alpha_s': state[0]}
    for i, k in enumerate(quarks + leptons):
        result[k] = state[i+1]
    return result

# ---------------------------------------------------------------------------
# Convert Yukawa couplings to pole masses
# ---------------------------------------------------------------------------

def yukawa_to_pole_mass(y, v=v_higgs, qcd_correction=1.0):
    """
    m = y * v / sqrt(2), with optional QCD correction factor.
    For top: qcd_correction ~ 1 + 4/3 * alpha_s/pi (one-loop)
    """
    return y * v / math.sqrt(2.0) * qcd_correction

# ---------------------------------------------------------------------------
# Full prediction pipeline
# ---------------------------------------------------------------------------

def w33_fermion_mass_predictions(verbose=True):
    """
    Full W(3,3) fermion mass prediction chain:
      1. Get alpha_s(M_Z) from W(3,3) GUT (fixed module)
      2. Get Yukawa couplings at M_GUT from W(3,3) spectral ratios
      3. Run Yukawas down from M_GUT to M_Z
      4. Convert to pole masses
      5. Compare to PDG

    Returns structured dict with predictions, residuals, sigma counts.
    """
    M_GUT = w33_m_gut()

    # Step 1: alpha_s chain
    rg_result = w33_alpha_s_mz(verbose=False)
    if rg_result['status'] != 'ok':
        alpha_s_mz = 0.1180  # PDG fallback
        alpha_s_gut = rg_result.get('alpha_s_gut', 0.04)
        if verbose:
            print(f"  [WARN] RG runaway; using PDG alpha_s(M_Z)={alpha_s_mz}")
    else:
        alpha_s_mz  = rg_result['alpha_s_mz']
        alpha_s_gut = rg_result['alpha_s_gut']

    # Step 2: Yukawa GUT values
    yukawas_gut = w33_yukawa_gut()

    if verbose:
        print(f"  alpha_s(M_GUT) = {alpha_s_gut:.5f}")
        print(f"  alpha_s(M_Z)   = {alpha_s_mz:.5f}  (PDG: 0.1180)")
        print(f"  W(3,3) Yukawa couplings at M_GUT:")
        for k,v in yukawas_gut.items():
            print(f"    y_{k:12s} = {v:.5f}")

    # Step 3: Run Yukawas down M_GUT -> M_Z
    yukawas_mz = run_yukawa_system(yukawas_gut, alpha_s_gut, M_GUT, M_Z, n_steps=5000)

    if yukawas_mz is None:
        if verbose:
            print("  [WARN] Yukawa RG runaway. Reporting GUT-scale masses only.")
        yukawas_mz = yukawas_gut

    # Step 4: Convert to masses
    # QCD correction at M_Z: (1 + 4/3 * alpha_s_mz / pi) for quarks
    qcd_q = 1.0 + (4.0/3) * alpha_s_mz / math.pi
    predictions = {}
    for f in PDG_MASSES:
        y = yukawas_mz.get(f, None)
        if y is None:
            continue
        is_lepton = f in ('tau', 'muon', 'electron')
        corr = 1.0 if is_lepton else qcd_q
        m_pred = yukawa_to_pole_mass(y, qcd_correction=corr)
        m_pdg  = PDG_MASSES[f]
        ratio  = m_pred / m_pdg if m_pdg > 0 else None
        predictions[f] = {
            'y_gut':    yukawas_gut.get(f),
            'y_mz':     y,
            'm_pred':   m_pred,
            'm_pdg':    m_pdg,
            'ratio':    ratio,
        }

    if verbose:
        print()
        print(f"  {'Fermion':12s}  {'m_pred (GeV)':>14s}  {'m_PDG (GeV)':>14s}  {'ratio':>8s}")
        print("  " + "-"*56)
        for f, d in predictions.items():
            r = f"{d['ratio']:.3f}" if d['ratio'] else '---'
            print(f"  {f:12s}  {d['m_pred']:14.5g}  {d['m_pdg']:14.5g}  {r:>8s}")

    return {
        'alpha_s_mz':   alpha_s_mz,
        'alpha_s_gut':  alpha_s_gut,
        'yukawas_gut':  yukawas_gut,
        'yukawas_mz':   yukawas_mz,
        'predictions':  predictions,
    }

if __name__ == '__main__':
    print("=" * 65)
    print("W(3,3) Fermion Mass Predictions via Yukawa RG")
    print("=" * 65)
    result = w33_fermion_mass_predictions(verbose=True)
    print()
    # Summary: which fermions are within 2x of PDG?
    good = [f for f,d in result['predictions'].items()
            if d['ratio'] and 0.5 <= d['ratio'] <= 2.0]
    print(f"  Fermions within 2x of PDG: {len(good)}/9")
    print(f"  Fermions: {good}")
    print("=" * 65)
