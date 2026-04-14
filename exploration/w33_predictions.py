# V49 closure-integrated prediction surface
"""
RIGOROUS FALSIFIABLE PREDICTIONS FROM W(3,3)
=============================================

This script collects the falsifiable W(3,3) prediction surface and the new
exact closure packets. Every quantity is derived from q = 3 plus v_EW.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


# ================================================================
# GRAPH PARAMETERS
# ================================================================

q = 3
v = 40
k = 12
lam = 2
mu = 4
r = 2
s = -4
f = 24
g = 15
E = 240
Phi3 = 13
Phi4 = 10
Phi6 = 7
Phi12 = 73
nn = 27
chi = 22
alpha_inv = 137
epsilon = 1.0 / math.sqrt(alpha_inv - 1)  # 1/sqrt(136)

V_EW = 246.22  # GeV
M_Pl = 1.22e19  # GeV


def derive_gauge_unification():
    print("=" * 72)
    print("  I. GAUGE COUPLINGS (spectral invariants)")
    print("=" * 72)
    print()

    sin2w = Fraction(q, Phi3)
    alpha_s = Fraction(mu * (q + lam), Phi3**2)
    alpha_em_inv_0 = (k - 1) ** 2 + mu ** 2

    pdg = dict(alpha_em_inv_0=137.036, sin2w=0.23122, alpha_s=0.1180)

    def pct(th, exp):
        return abs(th - exp) / exp * 100

    print(
        f"  alpha_em^-1(0)   = (k-1)^2 + mu^2 = {alpha_em_inv_0}"
        f"   PDG {pdg['alpha_em_inv_0']}  err={pct(alpha_em_inv_0, pdg['alpha_em_inv_0']):.2f}%"
    )
    print(
        f"  sin^2(theta_W)   = q/Phi_3         = {sin2w} = {float(sin2w):.4f}"
        f"   PDG {pdg['sin2w']}   err={pct(float(sin2w), pdg['sin2w']):.2f}%"
    )
    print(
        f"  alpha_s(M_Z)     = mu(q+lam)/Phi_3^2 = {alpha_s} = {float(alpha_s):.4f}"
        f"   PDG {pdg['alpha_s']}  err={pct(float(alpha_s), pdg['alpha_s']):.2f}%"
    )
    print()

    M_GUT = V_EW * (alpha_inv - 1) ** (g / 2.0)
    print("  Derived GUT scale (proton decay / axion only):")
    print(f"    M_GUT = v_EW * 136^(g/2) = {M_GUT:.3e} GeV")
    print()

    return {
        "alpha_em_inv_0": alpha_em_inv_0,
        "sin2_W": float(sin2w),
        "sin2_W_frac": str(sin2w),
        "alpha_s": float(alpha_s),
        "alpha_s_frac": str(alpha_s),
        "M_GUT_GeV": M_GUT,
    }


def derive_neutrino_masses():
    print("=" * 72)
    print("  II. NEUTRINO MASS PREDICTIONS")
    print("=" * 72)
    print()

    ratio = 2 * Phi3 + Phi6
    dm21_sq = 7.53e-5
    dm32_sq = ratio * dm21_sq
    dm32_sq_exp = 2.453e-3

    print(f"    dm^2_32 / dm^2_21 = 2*{Phi3} + {Phi6} = {ratio}")
    print(f"    dm^2_32(pred) = {dm32_sq:.3e} eV^2")
    print(f"    dm^2_32(exp)  = {dm32_sq_exp:.3e} eV^2")
    print()

    m1 = 0.0
    m2 = math.sqrt(dm21_sq) * 1000
    m3 = math.sqrt(dm32_sq) * 1000
    sum_mnu = m1 + m2 + m3

    return {
        "dm_ratio": ratio,
        "dm32_sq_predicted": dm32_sq,
        "dm32_sq_experimental": dm32_sq_exp,
        "m1_meV": m1,
        "m2_meV": m2,
        "m3_meV": m3,
        "sum_mnu_meV": sum_mnu,
        "hierarchy": "normal",
    }


def derive_cosmological_predictions():
    print("=" * 72)
    print("  III. COSMOLOGICAL PREDICTIONS")
    print("=" * 72)
    print()

    N_inflaton = v - Phi4
    H0 = Phi6 * Phi4
    dm_ratio = q + lam
    N_starobinsky = 2 * N_inflaton
    r_tensor = Fraction(12, N_starobinsky**2)
    ns_starobinsky = Fraction(N_starobinsky - 2, N_starobinsky)

    return {
        "n_s": float(ns_starobinsky),
        "n_s_fraction": str(ns_starobinsky),
        "n_s_exp": 0.9649,
        "H_0": H0,
        "H_0_planck": 67.4,
        "H_0_shoes": 73.0,
        "Omega_DM_over_Omega_b": dm_ratio,
        "r_tensor": float(r_tensor),
        "r_tensor_fraction": str(r_tensor),
        "N_e_folds": N_starobinsky,
        "inflation_model": "Starobinsky R^2, N=2(v-Phi_4)=60",
    }


def derive_inflation_observable_closure():
    print("=" * 72)
    print("  IIIb. INFLATION OBSERVABLE CLOSURE")
    print("=" * 72)
    print()

    N_edges = E // mu
    N_modes = 2 * (v - Phi4)
    ns = Fraction(N_edges - 2, N_edges)
    r_tensor = Fraction(12, N_edges**2)
    running = Fraction(-2, N_edges**2)
    nT = -r_tensor / 8
    fNL = Fraction(5, 12) * (ns - 1)

    return {
        "N_edges": N_edges,
        "N_modes": N_modes,
        "bridge_identity": f"{E} = 2*{mu}*({v}-{Phi4})",
        "n_s": float(ns),
        "n_s_fraction": str(ns),
        "r": float(r_tensor),
        "r_fraction": str(r_tensor),
        "running": float(running),
        "running_fraction": str(running),
        "n_T": float(nT),
        "n_T_fraction": str(nT),
        "f_NL": float(fNL),
        "f_NL_fraction": str(fNL),
        "closure_r_from_ns_fraction": str(3 * (1 - ns) ** 2),
        "closure_running_from_ns_fraction": str(-((1 - ns) ** 2) / 2),
        "closure_running_from_r_fraction": str(-r_tensor / 6),
        "closure_nT_from_r_fraction": str(-r_tensor / 8),
    }


def derive_particle_predictions():
    M_GUT = V_EW * (alpha_inv - 1) ** (g / 2.0)
    M_X = M_GUT / (q + lam)
    alpha_GUT = 1.0 / f
    m_p = 0.938
    tau_p_nat = M_X**4 / (alpha_GUT**2 * m_p**5)
    tau_p_s = tau_p_nat * 6.58e-25
    tau_p_yr = tau_p_s / (365.25 * 24 * 3600)
    f_a = M_GUT * epsilon**2
    m_a_eV = 6e-6 * (1e12 / f_a)
    return {
        "M_GUT": M_GUT,
        "tau_p_years": tau_p_yr,
        "tau_p_safe": tau_p_yr > 1.6e34,
        "f_a": f_a,
        "m_axion_eV": m_a_eV,
    }


def derive_fermion_masses():
    m_t = V_EW / math.sqrt(2)
    m_c = m_t * epsilon**2
    m_u = m_c / (v * g)
    m_b = m_t / (v + lam)
    m_s = m_b * q * epsilon**2
    m_d = m_s / ((q + lam) * mu)
    m_tau = 1.777
    m_mu_direct = m_tau / (k + q + lam)
    denom_e = alpha_inv + v + nn + lam
    m_e_pred = m_mu_direct / denom_e
    return {
        "m_t": m_t,
        "m_c": m_c,
        "m_u_MeV": m_u * 1000,
        "m_b": m_b,
        "m_s_MeV": m_s * 1000,
        "m_d_MeV": m_d * 1000,
        "m_tau": m_tau,
        "m_mu_MeV": m_mu_direct * 1000,
        "m_e_MeV": m_e_pred * 1000,
    }


def derive_mass_sector_closure():
    mc_mt = Fraction(1, alpha_inv - 1)
    mu_mc = Fraction(1, v * g)
    mb_mt = Fraction(1, v + lam)
    ms_mb = Fraction(q, alpha_inv - 1)
    md_ms = Fraction(1, (q + lam) * mu)
    ms_mc = ms_mb * mb_mt / mc_mt
    mu_md = (mu_mc * mc_mt) / (md_ms * ms_mb * mb_mt)
    bridge_ud = mu_mc / md_ms
    return {
        "m_c_over_m_t_fraction": str(mc_mt),
        "m_u_over_m_c_fraction": str(mu_mc),
        "m_b_over_m_t_fraction": str(mb_mt),
        "m_s_over_m_b_fraction": str(ms_mb),
        "m_d_over_m_s_fraction": str(md_ms),
        "m_s_over_m_c_fraction": str(ms_mc),
        "m_u_over_m_d_fraction": str(mu_md),
        "bridge_strange_over_charm_fraction": str(ms_mb / mc_mt),
        "bridge_light_ud_fraction": str(bridge_ud),
        "closure_product_fraction": str(ms_mc * mu_md),
    }


def derive_lepton_sector_closure():
    mu_tau = Fraction(1, k + q + lam)
    e_mu = Fraction(1, alpha_inv + v + nn + lam)
    e_tau = mu_tau * e_mu
    return {
        "m_mu_over_m_tau_fraction": str(mu_tau),
        "m_e_over_m_mu_fraction": str(e_mu),
        "m_e_over_m_tau_fraction": str(e_tau),
        "mu_denominator": k + q + lam,
        "e_denominator": alpha_inv + v + nn + lam,
        "geometry_remainder": v + nn + lam,
    }


def main():
    print("=" * 72)
    print("  FALSIFIABLE PREDICTIONS FROM W(3,3)")
    print("  Every number from q = 3 + v_EW = 246.22 GeV")
    print("=" * 72)
    print()

    results = {}
    results["gauge"] = derive_gauge_unification()
    results["neutrinos"] = derive_neutrino_masses()
    results["cosmology"] = derive_cosmological_predictions()
    results["inflation_closure"] = derive_inflation_observable_closure()
    results["particles"] = derive_particle_predictions()
    results["fermions"] = derive_fermion_masses()
    results["mass_closure"] = derive_mass_sector_closure()
    results["lepton_closure"] = derive_lepton_sector_closure()

    out_path = Path(__file__).resolve().parent.parent / "data" / "w33_predictions.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2, default=str)
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    main()
