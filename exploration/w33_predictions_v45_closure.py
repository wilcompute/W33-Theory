"""
V45 companion: enhanced prediction printout with exact inflation closure packet.

This is an additive companion to exploration/w33_predictions.py. It promotes the
repaired inflation sector from a list of successful numbers to an exact closure
theorem among observables, and records the analogous mass-sector closure that
appears after the light-quark repair.
"""

from __future__ import annotations

from fractions import Fraction

# W(3,3) data
q = 3
v, k, lam, mu = 40, 12, 2, 4
g = 15
E = v * k // 2
Phi4, Phi6 = 10, 7
alpha_inv = 137


def derive_inflation_observable_closure():
    """
    Exact closure packet for the repaired inflation sector.

    Two e-fold derivations coincide:
        N = E/mu = 240/4 = 60
        N = 2(v - Phi_4) = 2(40 - 10) = 60

    Hence the observables are not independent:
        n_s      = 1 - 2/N
        r        = 12/N^2
        running  = -2/N^2
        n_T      = -r/8
        f_NL     = (5/12)(n_s - 1)

    Eliminating N gives:
        r       = 3(1 - n_s)^2
        running = -(1 - n_s)^2/2 = -r/6
        n_T     = -r/8 = 3*running/4
        f_NL    = -5(1 - n_s)/12
    """
    print("=" * 72)
    print("  V45. INFLATION OBSERVABLE CLOSURE")
    print("=" * 72)
    print()

    N_edges = E // mu
    N_modes = 2 * (v - Phi4)
    assert N_edges == N_modes == 60

    ns = Fraction(N_edges - 2, N_edges)
    r = Fraction(12, N_edges * N_edges)
    running = Fraction(-2, N_edges * N_edges)
    nT = -r / 8
    fNL = Fraction(5, 12) * (ns - 1)

    print("  E-FOLD BRIDGE:")
    print(f"    N = E/mu            = {E}/{mu} = {N_edges}")
    print(f"    N = 2(v - Phi_4)    = 2({v} - {Phi4}) = {N_modes}")
    print(f"    Exact bridge: E = 2*mu*(v - Phi_4) = {2*mu*(v-Phi4)}")
    print()

    print("  OBSERVABLE PACKET:")
    print(f"    n_s       = 1 - 2/N       = {ns} = {float(ns):.6f}")
    print(f"    r         = 12/N^2        = {r} = {float(r):.6f}")
    print(f"    dn_s/dlnk = -2/N^2        = {running} = {float(running):.6f}")
    print(f"    n_T       = -r/8          = {nT} = {float(nT):.6f}")
    print(f"    f_NL      = (5/12)(n_s-1) = {fNL} = {float(fNL):.6f}")
    print()

    print("  EXACT CLOSURE RELATIONS:")
    print(f"    r          = 3(1-n_s)^2              = {3*(1-ns)**2} = {r}")
    print(f"    dn_s/dlnk  = -(1-n_s)^2/2            = {-((1-ns)**2)/2} = {running}")
    print(f"    dn_s/dlnk  = -r/6                    = {-r/6} = {running}")
    print(f"    n_T        = -r/8                    = {-r/8} = {nT}")
    print(f"    n_T        = 3(dn_s/dlnk)/4          = {3*running/4} = {nT}")
    print(f"    f_NL       = -5(1-n_s)/12            = {-Fraction(5,12)*(1-ns)} = {fNL}")
    print()

    return {
        "N_edges": N_edges,
        "N_modes": N_modes,
        "n_s": float(ns),
        "n_s_fraction": str(ns),
        "r": float(r),
        "r_fraction": str(r),
        "running": float(running),
        "running_fraction": str(running),
        "n_T": float(nT),
        "n_T_fraction": str(nT),
        "f_NL": float(fNL),
        "f_NL_fraction": str(fNL),
    }


def derive_mass_sector_closure():
    """
    Exact closure packet for the repaired light-quark sector.
    """
    print("=" * 72)
    print("  V46. MASS-SECTOR CLOSURE")
    print("=" * 72)
    print()

    mc_mt = Fraction(1, alpha_inv - 1)          # 1/136
    mu_mc = Fraction(1, v * g)                  # 1/600
    mb_mt = Fraction(1, v + lam)                # 1/42
    ms_mb = Fraction(q, alpha_inv - 1)          # 3/136
    md_ms = Fraction(1, (q + lam) * mu)         # 1/20

    ms_mc = ms_mb * mb_mt / mc_mt               # 1/14
    mu_md = (mu_mc * mc_mt) / (md_ms * ms_mb * mb_mt)  # 7/15
    bridge_ud = mu_mc / md_ms                   # 1/30

    print("  PRIMARY RATIOS:")
    print(f"    m_c/m_t = {mc_mt}")
    print(f"    m_u/m_c = {mu_mc}")
    print(f"    m_b/m_t = {mb_mt}")
    print(f"    m_s/m_b = {ms_mb}")
    print(f"    m_d/m_s = {md_ms}")
    print()

    print("  EXACT BRIDGES:")
    print(f"    (m_s/m_b)/(m_c/m_t) = {ms_mb/mc_mt} = q")
    print(f"    (m_u/m_c)/(m_d/m_s) = {bridge_ud} = 1/(v-Phi_4)")
    print(f"    m_s/m_c             = {ms_mc} = 1/(2*Phi_6)")
    print(f"    m_u/m_d             = {mu_md} = Phi_6/g")
    print(f"    (m_s/m_c)(m_u/m_d)  = {ms_mc*mu_md} = 1/(v-Phi_4)")
    print()

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


def main():
    print()
    print("=" * 72)
    print("  ENHANCED W(3,3) CLOSURE PACKETS")
    print("=" * 72)
    print()
    derive_inflation_observable_closure()
    derive_mass_sector_closure()


if __name__ == "__main__":
    main()
