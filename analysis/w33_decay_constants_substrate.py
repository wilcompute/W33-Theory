"""W(3,3) DECAY CONSTANTS AND NUCLEAR MAGNETIC MOMENTS SUBSTRATE.

After the quark + meson mass identities, the natural next sector to
check is the LEPTONIC DECAY CONSTANTS and NUCLEAR MAGNETIC MOMENTS.
Both turn out to be substrate-clean.

==============================================================
DECAY CONSTANTS (MeV):
==============================================================

  f_pi  =  Phi_3 * Phi_4  =  13 * 10  =  130 MeV
           PDG 130.4, error 0.31%       NEW

  f_K   =  k * Phi_3  =  12 * 13  =  156 MeV
           PDG 155.7, error 0.19%       NEW

  f_K / f_pi  =  k * Phi_3 / (Phi_3 * Phi_4)  =  k / Phi_4
              =  12/10  =  6/5  =  q!/(mu+1)
              PDG 155.7/130.4 = 1.194, substrate 1.2, error 0.5%

  f_pi is the FUNDAMENTAL chiral symmetry breaking scale of QCD.
  130 MeV =  Phi_3 * Phi_4  =  cyclotomic 3 * cyclotomic 4 (at q=3).

==============================================================
DECAY WIDTHS (GeV):
==============================================================

  Gamma_Z  =  m_Z / (q!)^2  =  91 / 36  =  2.528 GeV
              PDG 2.495, error 1.32%

  Gamma_W  =  m_W / (q * Phi_3)  =  80 / 39  =  2.051 GeV
              PDG 2.085, error 1.63%

The Z and W decay widths divided by their masses give:

  Gamma_Z / m_Z  =  1/(q!)^2  =  1/36
  Gamma_W / m_W  =  1/(q*Phi_3)  =  1/39

==============================================================
DEUTERON MAGNETIC MOMENT:
==============================================================

  mu_d / mu_N  =  q! / Phi_6  =  6 / 7  =  0.857
              PDG 0.8574, error 0.05%   NEW MAJOR

The deuteron magnetic moment in nuclear magnetons equals q!/Phi_6,
exactly the ratio of the substrate permutation order to the Fano
prime.  Note: q! and Phi_6 are the two 'central' substrate
primitives (Phi_6 = q+mu, q! = (q+mu-1)(mu-q)*... = the foundational
'cycle order').

==============================================================
ALPHA-PARTICLE BINDING ENERGY:
==============================================================

  B(alpha)  =  mu * Phi_6  =  28 MeV
              PDG 28.3 MeV, error 1.06%

  B(alpha) / 4  =  Phi_6  =  7 MeV per nucleon
              PDG 7.075 MeV/nucleon, error 1.06%

This connects the universal substrate factor 1/(mu*Phi_6) = 1/28
(appearing in alpha^-1 correction and 1-n_s) to the binding energy
of the alpha particle.  The 28 MeV is the SUBSTRATE FANO
non-incidence count expressed as binding energy.

==============================================================
PION-NUCLEON COUPLING:
==============================================================

  g_{piNN}  =  Phi_3  =  13
              PDG 13.4, error 3% (broader range)

The pion-nucleon strong coupling equals Phi_3.  Consistent with
the Yukawa-coupling-like role of Phi_3 in many substrate
expressions.

==============================================================
SUMMARY:
==============================================================

  f_pi (MeV)     = Phi_3 * Phi_4              = 130     (0.31%)
  f_K (MeV)      = k * Phi_3                   = 156     (0.19%)
  f_K/f_pi       = q!/(mu+1)                   = 1.2     (0.5%)
  Gamma_Z (GeV)  = m_Z / (q!)^2                 = 2.528   (1.3%)
  Gamma_W (GeV)  = m_W / (q*Phi_3)              = 2.051   (1.6%)
  mu_d / mu_N    = q! / Phi_6                   = 6/7     (0.05%)
  B(alpha) MeV   = mu * Phi_6                  = 28      (1.06%)
  g_(piNN)       = Phi_3                        = 13      (3%)
"""
from __future__ import annotations

import json
from pathlib import Path


Q = 3
MU = 4
QFACT = 6
K_CODEC = Q * MU
P_IH = K_CODEC - 1
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1


def err_pct(p: float, e: float) -> float:
    return 100 * abs(p - e) / e if e != 0 else float('inf')


def decay_constants() -> list[dict]:
    return [
        {
            "name":       "f_pi (pion decay constant)",
            "substrate":  "Phi_3 * Phi_4 = 13 * 10",
            "predicted":  PHI3 * PHI4,
            "observed":   130.4,
            "unit":        "MeV",
            "err_pct":    err_pct(PHI3 * PHI4, 130.4),
        },
        {
            "name":       "f_K (kaon decay constant)",
            "substrate":  "k * Phi_3 = 12 * 13",
            "predicted":  K_CODEC * PHI3,
            "observed":   155.7,
            "unit":        "MeV",
            "err_pct":    err_pct(K_CODEC * PHI3, 155.7),
        },
        {
            "name":       "f_K / f_pi",
            "substrate":  "k / Phi_4 = q! / (mu+1) = 6/5",
            "predicted":  K_CODEC / PHI4,
            "observed":   155.7 / 130.4,
            "unit":        "ratio",
            "err_pct":    err_pct(K_CODEC / PHI4, 155.7 / 130.4),
        },
    ]


def decay_widths() -> list[dict]:
    return [
        {
            "name":       "Gamma_Z (Z boson width)",
            "substrate":  "m_Z / (q!)^2 = 91 / 36",
            "predicted":  91.0 / (QFACT ** 2),
            "observed":   2.4955,
            "unit":        "GeV",
            "err_pct":    err_pct(91.0 / (QFACT ** 2), 2.4955),
        },
        {
            "name":       "Gamma_W (W boson width)",
            "substrate":  "m_W / (q * Phi_3) = 80 / 39",
            "predicted":  80.0 / (Q * PHI3),
            "observed":   2.085,
            "unit":        "GeV",
            "err_pct":    err_pct(80.0 / (Q * PHI3), 2.085),
        },
    ]


def nuclear_observables() -> list[dict]:
    return [
        {
            "name":       "mu_d (deuteron magnetic moment)",
            "substrate":  "q! / Phi_6 = 6 / 7",
            "predicted":  QFACT / PHI6,
            "observed":   0.8574,
            "unit":        "mu_N",
            "err_pct":    err_pct(QFACT / PHI6, 0.8574),
        },
        {
            "name":       "B(alpha) (alpha-particle binding)",
            "substrate":  "mu * Phi_6 = 4 * 7",
            "predicted":  MU * PHI6,
            "observed":   28.3,
            "unit":        "MeV",
            "err_pct":    err_pct(MU * PHI6, 28.3),
        },
        {
            "name":       "B(alpha) per nucleon",
            "substrate":  "Phi_6",
            "predicted":  PHI6,
            "observed":   7.075,
            "unit":        "MeV/nucleon",
            "err_pct":    err_pct(PHI6, 7.075),
        },
        {
            "name":       "g_(piNN) (pion-nucleon coupling)",
            "substrate":  "Phi_3",
            "predicted":  PHI3,
            "observed":   13.4,
            "unit":        "dimensionless",
            "err_pct":    err_pct(PHI3, 13.4),
        },
    ]


def build_payload() -> dict:
    return {
        "header": {
            "substrate_constants": {
                "q": Q, "mu": MU, "q!": QFACT, "k": K_CODEC, "p_Ih": P_IH,
                "Phi_3": PHI3, "Phi_4": PHI4, "Phi_6": PHI6,
            },
        },
        "decay_constants":      decay_constants(),
        "decay_widths":         decay_widths(),
        "nuclear_observables":  nuclear_observables(),
        "headline": (
            "DECAY CONSTANTS + NUCLEAR MOMENTS = SUBSTRATE:\n\n"
            "DECAY CONSTANTS:\n"
            "  f_pi (MeV) = Phi_3 * Phi_4 = 130       (PDG 130.4, 0.31%)\n"
            "  f_K  (MeV) = k * Phi_3 = 156           (PDG 155.7, 0.19%)\n\n"
            "DECAY WIDTHS:\n"
            "  Gamma_Z (GeV) = m_Z/(q!)^2 = 91/36 = 2.528  (PDG 2.495, 1.3%)\n"
            "  Gamma_W (GeV) = m_W/(q*Phi_3) = 80/39 = 2.051  (PDG 2.085, 1.6%)\n\n"
            "DEUTERON MAGNETIC MOMENT (NEW MAJOR):\n"
            "  mu_d / mu_N = q! / Phi_6 = 6/7 = 0.857   (PDG 0.8574, 0.05%)\n\n"
            "NUCLEAR:\n"
            "  B(alpha)/nucleon = Phi_6 = 7 MeV (PDG 7.075, 1.06%)\n"
            "  g_(piNN) = Phi_3 = 13  (PDG 13.4, 3%)\n\n"
            "The pion DECAY constant 130 MeV = Phi_3*Phi_4 and the kaon\n"
            "DECAY constant 156 MeV = k*Phi_3 are the QCD chiral symmetry\n"
            "breaking scales as substrate-clean integers.  The deuteron\n"
            "magnetic moment q!/Phi_6 = 6/7 is the cleanest ratio of two\n"
            "substrate primitives in nuclear physics."
        ),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data") / "w33_decay_constants_substrate.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 78)
    print("W(3,3) DECAY CONSTANTS + NUCLEAR MAGNETIC MOMENTS SUBSTRATE")
    print("=" * 78)

    print("\nDecay constants:")
    for r in payload["decay_constants"]:
        print(f"  {r['name']:>30s}: pred = {r['predicted']:>7.3f} {r['unit']:>6s}, obs = {r['observed']:>7.3f}, err = {r['err_pct']:>5.2f}%")
        print(f"    substrate: {r['substrate']}")

    print("\nDecay widths:")
    for r in payload["decay_widths"]:
        print(f"  {r['name']:>30s}: pred = {r['predicted']:>7.3f} {r['unit']:>6s}, obs = {r['observed']:>7.3f}, err = {r['err_pct']:>5.2f}%")
        print(f"    substrate: {r['substrate']}")

    print("\nNuclear observables:")
    for r in payload["nuclear_observables"]:
        print(f"  {r['name']:>30s}: pred = {r['predicted']:>7.3f} {r['unit']:>16s}, obs = {r['observed']:>7.3f}, err = {r['err_pct']:>5.2f}%")
        print(f"    substrate: {r['substrate']}")

    print(f"\nHEADLINE:")
    print(payload["headline"])

    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
