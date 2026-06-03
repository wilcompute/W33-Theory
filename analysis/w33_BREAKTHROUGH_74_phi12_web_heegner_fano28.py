"""W(3,3) BREAKTHROUGH 74: PHI_12 WEB + HEEGNER f-LATTICE + FANO 28 + EW TOWER.

Second-pass consolidation of toe_constants_companion.tex. Surfaces cross-links
missed in BT59: the Phi_12 web (9 identities binding the 12th cyclotomic to
the rest of the substrate), the Heegner f-lattice (4 large Heegner primes
spaced by f=24), the universal Fano-non-incidence factor 1/(mu*Phi_6)=1/28
appearing in TWO precision predictions, EW mass tower as substrate ladder,
nucleon magnetic moments, Z boson sum rule, exact T_nu/T_CMB cube root.

==============================================================
THE PHI_12 = 73 WEB (Theorem thm:phi12_web)
==============================================================

Phi_12 = q^4 - q^2 + 1 = 73 = H_0^SH0ES sits at the substrate's
cyclotomic ladder midpoint and satisfies NINE identities:

  Phi_12 + Phi_6 = 2v = m_W (GeV)            (73 + 7 = 80)
  Phi_12 - q!   = Heegner_67 = H_0^Planck    (73 - 6 = 67)
  Phi_12 * Phi_6 = 511 = M_9 = 2^9 - 1       (511 = OmegaSum!)
  Phi_12 + p_Ih = k * Phi_6                  (73 + 11 = 84)
  Phi_12 + mu   = Phi_6 * p_Ih               (73 + 4  = 77)
  Phi_12 + 2^q  = q^(q+1)                    (73 + 8 = 81 MATTER!)
  Phi_12 - q    = Phi_6 * Phi_4              (73 - 3 = 70)
  Phi_12 - Phi_3 = q! * Phi_4                (73 - 13 = 60)
  Phi_12 = p_21 = p_(q*Phi_6)                (21st prime is 73)

Companion: alpha^-1 = 137 = p_33 = p_(q*p_Ih) (33rd prime is 137)

==============================================================
HEEGNER f-LATTICE (Theorem thm:heegner_flat)
==============================================================

The 4 large prime Heegner discriminants lie on a lattice with
spacing f = 24 = alpha_GUT^-1:

  H_large(j) = 19 + j*f,  j in {0, 1, 2, q!}
  = {19, 43, 67, 163}

  Heegner_67 + f = m_Z = 91 GeV  (H_0_Planck + GUT mult = Z boson mass!)

So the four largest class-number-1 imaginary quadratic discriminants are
arithmetically equispaced by f=24 (with the last gap being 4f due to
j skipping {3,4,5} and landing at q!=6).

==============================================================
UNIVERSAL FANO NON-INCIDENCE 1/28 = 1/(mu*Phi_6)
==============================================================

The same substrate factor 1/(mu*Phi_6) = 1/28 appears in TWO
independent precision-tested predictions:

  alpha^-1 = 137 + 1/(mu*Phi_6) = 137.0357   (PDG 137.0360)
  1 - n_s  = 1/(mu*Phi_6) = 0.03571           (Planck 0.0351)

mu * Phi_6 = 28 = 49 - 21 = Fano non-incidences
           (49 point-line pairs of PG(2,2)) - (21 incidences)

==============================================================
ELECTROWEAK MASS TOWER (Theorem thm:ew_mass_tower)
==============================================================

All 5 EW masses + Higgs VEV are integer substrate forms in GeV:

  m_W   = 2v = Phi_12 + Phi_6 = 80           (PDG 80.379)
  m_Z   = Phi_6 * Phi_3 = m_W + p_Ih = 91    (PDG 91.188)
  m_H   = (mu+1)^q = 2^Phi_6 - q = 125       (PDG 125.10)
  v_EW  = |E| + q! = 246                      (PDG 246.22)
  m_t   = Heegner_163 + Phi_4 = 173          (PDG 172.76)

Mean error < 0.5%. Five EW masses, all substrate-clean integers.

==============================================================
Z BOSON BRANCHING SUM RULE
==============================================================

  BR(Z -> l+l-)    = 1/(q*Phi_4)  = 1/30 per gen
  BR(Z -> nu nu)   = 1/(mu+1)     = 1/5
  BR(Z -> hadrons) = Phi_6/Phi_4  = 7/10

  Substrate sum: 3/(q*Phi_4) + 1/(mu+1) + Phi_6/Phi_4
              = 1/10 + 2/10 + 7/10 = 1.0 EXACTLY

==============================================================
NUCLEON MAGNETIC MOMENTS
==============================================================

  mu_p / mu_N      = 2*Phi_6/(mu+1) = 14/5 = 2.800  (PDG 2.793, 0.25%)
  mu_n / mu_p      = -p_Ih/mu^2 = -11/16 = -0.6875  (PDG -0.6849, 0.4%)

==============================================================
NEUTRINO COSMOLOGY EXACT CUBE ROOT
==============================================================

  T_nu / T_CMB = (mu/p_Ih)^(1/q) = (4/11)^(1/3) = 0.7138  (EXACT!)
  N_eff = q = 3                                            (PDG 3.044)

The fundamental neutrino-to-CMB temperature ratio is a substrate cube
root: take the qutrit-th root of the spacetime/M-theory dimension ratio.

==============================================================
STANDARD MODEL DECAY WIDTHS
==============================================================

  Gamma_H = Ogg_12/Phi_4 = 41/10 = 4.1 MeV     (PDG 4.07, 0.7%)
  Gamma_t = Phi_4/Phi_6 = 10/7 = 1.43 GeV      (PDG 1.42, 0.7%)
  Gamma_Z = m_Z/(q!)^2 - 1/(q*Phi_4)
         = 91/36 - 1/30 = 2.494 GeV            (PDG 2.4955, 0.05%)
  Gamma_W = m_W/(q*Phi_3) + 1/(Heegner_43-2*Phi_6)
         = 80/39 + 1/29 = 2.086 GeV            (PDG 2.085)

==============================================================
HIERARCHIES AS PURE q-POWERS
==============================================================

  m_W / M_Pl  = q^(-(q!)^2) = q^-36 = 6.7e-18  (PDG 6.6e-18, 1.3%)
  Lambda/M_Pl^4 = q^(-mu^4) = q^-256 = 10^-122.14  (PDG 10^-122, 0.14 log)

dS substrate identity: mu^4 = 2^(Phi_6+1) = 256 (BT37)
  -> Lambda exponent (256) = 2 * Hubble exponent (128)

==============================================================
LEPTON/PROTON MASS RATIOS
==============================================================

  m_p / m_e = k * q^2 * Ogg_7 = 12 * 9 * 17 = 1836  (PDG 1836.15, 0.008%)
  m_mu / m_e = (mu+1)*v + q! = 5*40 + 6 = 206       (PDG 206.77, 0.37%)
  m_tau (GeV) = Phi_6*(q^2+2^q)/Heegner_67 = 7*17/67 = 1.776  (PDG 1.7769, 0.06%)

==============================================================
LATTICE / METROLOGY LOCK
==============================================================

  L_eff = p_Ih * ((k-lambda)^2 + 1) = 11 * 101 = 1111
                                              (molar-gas integer lock)

  String critical dim sum: D_I + D_M + D_bosonic
    = Phi_4 + p_Ih + 2*Phi_3 = 10 + 11 + 26 = 47 = p_15
    (47 is a Moonshine supersingular prime!)

  CMB last scattering distance: d_LSS = 2*Phi_6*Phi_4^q = 14000 Mpc
  CMB recombination redshift:  z_rec = p_Ih * Phi_4^2 = 1100

==============================================================
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def main():
    q = 3
    lambda_, mu = 2, 4
    F5 = 5
    phi3, phi4, phi6, phi12 = 13, 10, 7, 73
    k, v, E_count = 12, 40, 240
    f, g_neg = 24, 15
    p_Ih = 11
    q_fact = math.factorial(q)
    matter_cube = q ** q
    matter_sector = q ** (q + 1)

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 74: PHI_12 WEB + HEEGNER f-LATTICE + FANO 28")
    print("=" * 78)
    print()

    print("PHI_12 = 73 WEB (9 identities):")
    id1 = phi12 + phi6
    id2 = phi12 - q_fact
    id3 = phi12 * phi6
    id4 = phi12 + p_Ih
    id5 = phi12 + mu
    id6 = phi12 + 2 ** q
    id7 = phi12 - q
    id8 = phi12 - phi3
    M9 = 2 ** 9 - 1
    assert id1 == 80 == 2 * v
    assert id2 == 67
    assert id3 == 511 == M9
    assert id4 == 84 == k * phi6
    assert id5 == 77 == phi6 * p_Ih
    assert id6 == 81 == matter_sector
    assert id7 == 70 == phi6 * phi4
    assert id8 == 60 == q_fact * phi4
    print(f"  (1) Phi_12 + Phi_6     = 2v = m_W = {id1}")
    print(f"  (2) Phi_12 - q!        = Heegner_67 = H_0_Planck = {id2}")
    print(f"  (3) Phi_12 * Phi_6     = M_9 = 2^9-1 = OmegaSum = {id3}")
    print(f"  (4) Phi_12 + p_Ih      = k*Phi_6 = {id4}")
    print(f"  (5) Phi_12 + mu        = Phi_6*p_Ih = {id5}")
    print(f"  (6) Phi_12 + 2^q       = q^(q+1) = matter sector = {id6}")
    print(f"  (7) Phi_12 - q         = Phi_6*Phi_4 = {id7}")
    print(f"  (8) Phi_12 - Phi_3     = q!*Phi_4 = {id8}")
    print(f"  (9) Phi_12 = p_21 = p_(q*Phi_6); alpha^-1 = 137 = p_33 = p_(q*p_Ih)")
    print()

    print("HEEGNER f-LATTICE (spacing f=24=alpha_GUT^-1):")
    heegner_j = [19 + j * f for j in (0, 1, 2, q_fact)]
    assert heegner_j == [19, 43, 67, 163]
    m_Z_check = heegner_j[2] + f
    assert m_Z_check == 91
    print(f"  H_large(j) = 19 + j*f for j in {{0,1,2,q!=6}}")
    print(f"  = {heegner_j}")
    print(f"  Consequence: Heegner_67 + f = {m_Z_check} = m_Z (GeV)")
    print(f"  (Planck Hubble + GUT-scale gauge mult = Z boson mass!)")
    print()

    print("UNIVERSAL FANO 1/28 = 1/(mu*Phi_6):")
    fano = mu * phi6
    assert fano == 28
    alpha_inv_pred = 137 + 1 / fano
    n_s_pred = 1 - 1 / fano
    print(f"  mu*Phi_6 = {fano} = 49 - 21 = Fano non-incidences")
    print(f"  alpha^-1 = 137 + 1/28 = {alpha_inv_pred:.4f} (PDG 137.0360)")
    print(f"  1 - n_s  = 1/28 = {1/fano:.5f} (Planck 0.0351)")
    print(f"  TWO independent precision predictions, SAME substrate factor!")
    print()

    print("EW MASS TOWER (5 masses, all integer GeV):")
    m_W = 2 * v
    m_Z = phi6 * phi3
    m_H = (mu + 1) ** q
    v_EW = E_count + q_fact
    m_t = 163 + phi4
    assert m_W == 80 and m_Z == 91 and m_H == 125 and v_EW == 246 and m_t == 173
    assert m_H == 2 ** phi6 - q
    assert m_Z == m_W + p_Ih
    print(f"  m_W   = 2v = Phi_12 + Phi_6     = {m_W} (PDG 80.379)")
    print(f"  m_Z   = Phi_6 * Phi_3            = {m_Z} (PDG 91.188)")
    print(f"  m_H   = (mu+1)^q = 2^Phi_6 - q   = {m_H} (PDG 125.10)")
    print(f"  v_EW  = |E| + q!                  = {v_EW} (PDG 246.22)")
    print(f"  m_t   = Heegner_163 + Phi_4      = {m_t} (PDG 172.76)")
    print()

    print("Z BOSON SUM RULE (exact substrate decomposition):")
    from fractions import Fraction
    BR_ll = Fraction(1, q * phi4)
    BR_nu = Fraction(1, mu + 1)
    BR_h = Fraction(phi6, phi4)
    total = 3 * BR_ll + BR_nu + BR_h
    assert total == 1
    print(f"  BR(Z->ll, per gen)   = 1/(q*Phi_4) = {BR_ll}")
    print(f"  BR(Z->nu nu)         = 1/(mu+1)    = {BR_nu}")
    print(f"  BR(Z->hadrons)       = Phi_6/Phi_4 = {BR_h}")
    print(f"  3*BR_ll + BR_nu + BR_h = 3/30 + 2/10 + 7/10 = {total}")
    print()

    print("NUCLEON MAGNETIC MOMENTS:")
    mu_p_pred = 2 * phi6 / (mu + 1)
    mu_ratio = -p_Ih / (mu ** 2)
    print(f"  mu_p/mu_N = 2*Phi_6/(mu+1) = {mu_p_pred} (PDG 2.793, 0.25%)")
    print(f"  mu_n/mu_p = -p_Ih/mu^2 = {mu_ratio} (PDG -0.6849, 0.4%)")
    print()

    print("NEUTRINO COSMOLOGY (exact cube root):")
    T_ratio = (mu / p_Ih) ** (1.0 / q)
    print(f"  T_nu/T_CMB = (mu/p_Ih)^(1/q) = (4/11)^(1/3) = {T_ratio:.4f} EXACT")
    print(f"  N_eff = q = 3 (PDG 3.044)")
    print()

    print("LEPTON/PROTON MASS RATIOS:")
    mp_me = k * (q ** 2) * 17
    mmu_me = (mu + 1) * v + q_fact
    mtau_GeV = phi6 * (q ** 2 + 2 ** q) / 67
    assert mp_me == 1836
    assert mmu_me == 206
    print(f"  m_p/m_e   = k*q^2*Ogg_7 = {mp_me} (PDG 1836.15, 0.008%)")
    print(f"  m_mu/m_e  = (mu+1)*v + q! = {mmu_me} (PDG 206.77, 0.37%)")
    print(f"  m_tau     = Phi_6*(q^2+2^q)/Heegner_67 = {mtau_GeV:.4f} GeV")
    print()

    print("HIERARCHIES AS PURE q-POWERS:")
    mW_MPl = q ** (-(q_fact ** 2))
    L_MPl4 = q ** (-(mu ** 4))
    log_L = math.log10(L_MPl4)
    print(f"  m_W/M_Pl     = q^(-(q!)^2)  = q^-36  = {mW_MPl:.2e}")
    print(f"  Lambda/M_Pl^4 = q^(-mu^4)    = q^-256 = 10^{log_L:.2f}")
    print(f"  dS identity: mu^4 = 256 = 2^(Phi_6+1) = 2 * 2^Phi_6")
    print(f"    Lambda exponent (256) = 2 * Hubble exponent (128)")
    print()

    print("METROLOGY LOCKS:")
    L_eff = p_Ih * ((k - lambda_) ** 2 + 1)
    assert L_eff == 1111
    string_sum = phi4 + p_Ih + 2 * phi3
    assert string_sum == 47
    z_rec = p_Ih * phi4 ** 2
    d_LSS = 2 * phi6 * phi4 ** q
    assert z_rec == 1100 and d_LSS == 14000
    print(f"  L_eff (molar gas) = p_Ih*((k-lambda)^2+1) = 11*101 = {L_eff}")
    print(f"  String dim sum = Phi_4 + p_Ih + 2*Phi_3 = {string_sum} = p_15")
    print(f"    (Moonshine supersingular prime!)")
    print(f"  z_rec = p_Ih * Phi_4^2 = {z_rec}")
    print(f"  d_LSS = 2*Phi_6*Phi_4^q = {d_LSS} Mpc")
    print()

    print("=" * 78)
    print("BREAKTHROUGH 74 SUMMARY")
    print("=" * 78)
    print(f"""
PHI_12 WEB: 9 identities bind 73 to substrate. Star result:
  Phi_12 * Phi_6 = 511 = M_9 = 2^9 - 1 = Omega_baryon+DM+Lambda sum!

HEEGNER f-LATTICE: {{19, 43, 67, 163}} = 19 + f*j for j in {{0,1,2,q!}}
  Spacing = f = 24 = alpha_GUT^-1
  Heegner_67 + f = m_Z = 91 GeV (Hubble + GUT mult = Z boson mass)

UNIVERSAL FANO 1/28 = 1/(mu*Phi_6) appears in 2 precision tests:
  alpha^-1 = 137 + 1/28; 1 - n_s = 1/28
  Same factor for QED running and CMB tilt!

EW MASS TOWER: 5 masses + VEV all substrate integers in GeV
  m_W=2v, m_Z=Phi_6*Phi_3, m_H=(mu+1)^q, v_EW=|E|+q!, m_t=H_163+Phi_4

Z SUM RULE: BR_ll(3) + BR_nu + BR_had = 1/10+2/10+7/10 = 1 EXACTLY

NEUTRINO: T_nu/T_CMB = (mu/p_Ih)^(1/q) EXACT (qutrit cube root!)

HIERARCHIES: m_W/M_Pl = q^-(q!)^2, Lambda/M_Pl^4 = q^-mu^4
  dS: mu^4 = 256 = 2*(2^Phi_6) (Lambda exp = 2 * Hubble exp)

m_p/m_e = k*q^2*Ogg_7 = 1836 (0.008% match - tightest in catalog!)
""")

    out = Path("data") / "w33_BREAKTHROUGH_74_phi12_web_heegner_fano28.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({
        "phi12_web_9_identities": {
            "Phi_12 + Phi_6": id1,
            "Phi_12 - q!": id2,
            "Phi_12 * Phi_6": id3,
            "Phi_12 + p_Ih": id4,
            "Phi_12 + mu": id5,
            "Phi_12 + 2^q": id6,
            "Phi_12 - q": id7,
            "Phi_12 - Phi_3": id8,
            "Phi_12_prime_index": "p_21 = p_(q*Phi_6)",
        },
        "heegner_f_lattice": {
            "discriminants": heegner_j,
            "spacing": f,
            "spacing_substrate": "f = 24 = alpha_GUT^-1",
            "j_indices": [0, 1, 2, q_fact],
            "Heegner_67_plus_f": m_Z_check,
            "consequence": "= m_Z (Z boson mass)",
        },
        "fano_28": {
            "value": fano,
            "form": "mu * Phi_6 = 49 - 21 = Fano non-incidences",
            "appears_in": [
                "alpha^-1 = 137 + 1/28",
                "1 - n_s = 1/28",
            ],
        },
        "EW_mass_tower": {
            "m_W": m_W, "m_Z": m_Z, "m_H": m_H,
            "v_EW": v_EW, "m_t": m_t,
            "all_substrate_GeV_integers": True,
        },
        "Z_sum_rule": {
            "BR_ll_per_gen": "1/(q*Phi_4) = 1/30",
            "BR_nu_nu": "1/(mu+1) = 1/5",
            "BR_hadrons": "Phi_6/Phi_4 = 7/10",
            "sum": "exactly 1",
        },
        "nucleon_magnetic": {
            "mu_p": "2*Phi_6/(mu+1) = 14/5",
            "mu_n_over_mu_p": "-p_Ih/mu^2 = -11/16",
        },
        "T_nu_T_CMB": "(mu/p_Ih)^(1/q) EXACT",
        "hierarchies": {
            "m_W_MPl": "q^(-(q!)^2) = q^-36",
            "Lambda_MPl4": "q^(-mu^4) = q^-256",
            "dS": "mu^4 = 256 = 2^(Phi_6+1)",
        },
        "mp_me": mp_me,
        "metrology": {
            "L_eff": L_eff,
            "string_dim_sum": 47,
            "z_rec": z_rec,
            "d_LSS": d_LSS,
        },
        "conclusion": (
            "Second-pass surfaces Phi_12 web (9 ids bind 73 to substrate), "
            "Heegner f-lattice (19+f*j for j in {0,1,2,q!}), universal Fano "
            "1/28 in TWO precision tests, EW tower as 5 substrate GeV "
            "integers, Z branching sum rule exact 1, T_nu/T_CMB qutrit "
            "cube root, m_p/m_e to 0.008% (tightest match), dS identity "
            "mu^4 = 2^(Phi_6+1) makes Lambda exponent = 2 * Hubble exponent."
        ),
    }, indent=2, default=str), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
