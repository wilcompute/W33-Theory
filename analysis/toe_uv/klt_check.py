"""How much suppression does the Khoury-Lin-Trodden dark-axion / dark-baryon model (arXiv:2503.16415, 2607.16191) need?  Their axion potential is Lambda^4 = eps m_pi^2 f_pi^2 ~ meV^4 with eps << 1 (their Eq. 8, eps <~ 1e-12 from perturbative control), and their coupling is set by sigma_N/m0 = 0.01-0.02 (a free input, the SM sigma term ratio is ~0.06).
If the dark sector scales like QCD:  sigma_N ~ k m_pi^2 / m0 with k ~ 4 (chiral perturbation theory, c1 ~ -1/m_N; QCD: 59 MeV * 0.94 GeV / 0.0195 GeV^2 = 2.8), and f_pi ~ m0 / 10 (QCD: 92/938).
Then m_pi^2 f_pi^2 = (sigma_N/m0) m0^2 / k * (m0/10)^2, so eps = Lambda^4 / (m_pi^2 f_pi^2) is fixed by m0 and sigma_N/m0.
If eps comes from a Z_N copy structure with suppression ~ z^N (z = m_u/m_d of the dark sector; a rough scaling of the Hook / Di Luzio et al. Z_N axion potential), N ~ ln(eps)/ln(z).
Also restated: the generic one-loop cap from Pass 12627, m < (4 pi^2 H0^2 M_P^2 / b^2)^(1/4) = 0.02 eV, which KLT evade by the shift symmetry, so the price appears as eps.
usage: py -3 klt_check.py"""
import json
import math

LAM4 = (2.3e-3) ** 4  # eV^4, dark-energy scale
out = []
for k in (2.8, 4.0):
    for s in (0.01, 0.02):
        for m0 in (1e2, 1e3, 1e6, 1e9, 1e12):
            mpi2fpi2 = s * m0 ** 2 / k * (m0 / 10) ** 2
            eps = LAM4 / mpi2fpi2
            row = dict(k=k, sigma_over_m0=s, m0_eV=m0, mpi_eV=math.sqrt(s * m0 ** 2 / k), eps=eps, N_z05=math.log(eps) / math.log(0.5), N_z08=math.log(eps) / math.log(0.8))
            out.append(row)
            if k == 4.0 and s == 0.01:
                print("m0 %8.0e eV: m_pi %.1e eV, eps %.1e, Z_N copies N ~ %.0f (z=0.5) / %.0f (z=0.8)" % (m0, row["mpi_eV"], eps, row["N_z05"], row["N_z08"]))
json.dump(out, open("klt_check.json", "w"), indent=1)
