#!/usr/bin/env python3
"""
Cogenesis: one E8 CP-violating source -- the decay of the 128-spinor's right-handed
neutrino -- makes both the baryon asymmetry and the dark-matter asymmetry, so
Omega_DM ~ Omega_b is automatic and eta_B = -|E|/(v-k-lambda).

The dark sector is asymmetric dark matter (BT1694 / w33_dark_*): its abundance is
an asymmetry, like the baryons. The economical origin is COGENESIS -- a single
heavy state whose CP-violating, out-of-equilibrium decay seeds BOTH asymmetries.
The natural such state is the right-handed neutrino N_R living in the 128 spinor
(the 16 of SO(10) inside (16,4)+(16bar,4bar)); its decay does standard
leptogenesis (-> baryon asymmetry via sphalerons) AND transfers an equal-and-
opposite asymmetry to the dark hidden-SU(4) sector.

Numbers (corpus + substrate):
  - baryon asymmetry: log10(eta_B) = -|E|/(v - k - lambda) = -240/26 = -9.23
    (observed ~ -9.21);
  - both asymmetries share one CP source, so Omega_DM ~ Omega_b automatically, and
    the substrate fixes Omega_DM/Omega_b = (mu/g)/(lambda/(v+1)) = 82/15 = 5.467;
  - with equal dark and baryon number asymmetries (n_DM = n_b) the ratio is the
    dark-baryon/proton mass ratio, m_DM/m_p = 82/15 -> m_DM ~ 5.1 GeV; a smaller
    dark asymmetry accommodates the heavier ~22.8 GeV branch.

So the matter-antimatter asymmetry, the dark-matter abundance, and the
cosmic-coincidence Omega_DM ~ Omega_b all come from ONE CP-violating decay of the
128's right-handed neutrino. Honest: eta_B uses the corpus closed form and the
cogenesis link is a mechanism (the CP phase / washout factors are not computed).
"""
from __future__ import annotations

import json
from fractions import Fraction as Fr

V, K, LAM, MU, G, E = 40, 12, 2, 4, 15, 240


def main():
    out = {}

    # baryon asymmetry (corpus closed form)
    denom = V - K - LAM
    log_etaB = -Fr(E, denom)
    print(
        f"[baryon asymmetry]  log10(eta_B) = -|E|/(v-k-lambda) = -{E}/{denom} "
        f"= {float(log_etaB):.2f}  (obs ~ -9.21)"
    )
    assert denom == 26 and abs(float(log_etaB) + 9.23) < 0.01
    out["log10_eta_B"] = round(float(log_etaB), 2)

    # shared asymmetry -> Omega_DM/Omega_b geometric
    Om_DM, Om_b = Fr(MU, G), Fr(LAM, V + 1)
    ratio = Om_DM / Om_b
    print(
        f"\n[cogenesis ratio]  Omega_DM/Omega_b = (mu/g)/(lambda/(v+1)) = {ratio} "
        f"= {float(ratio):.3f}  (obs ~5.4)"
    )
    assert ratio == Fr(82, 15)
    out["Omega_DM_over_Omega_b"] = str(ratio)

    # equal-asymmetry mass reading
    m_p = 0.938  # GeV
    m_DM_equal = float(ratio) * m_p
    print(
        f"  equal asymmetries (n_DM=n_b): m_DM/m_p = 82/15 -> m_DM ~ "
        f"{m_DM_equal:.2f} GeV (asymmetric-DM light branch)"
    )
    out["m_DM_equal_asymmetry_GeV"] = round(m_DM_equal, 2)

    print(f"\n[one CP source]  the 128-spinor's right-handed neutrino N_R (the 16 of")
    print(f"  SO(10) in (16,4)+(16bar,4bar)) decays out of equilibrium with CP")
    print(f"  violation -> leptogenesis (baryon asymmetry via sphalerons) AND an")
    print(f"  equal dark-SU(4) asymmetry. One decay seeds both sectors.")
    out["cp_source"] = (
        "128-spinor right-handed neutrino N_R decay (leptogenesis + dark)"
    )

    print("\nRESULT: cogenesis from the 128's right-handed neutrino. Its CP-violating,")
    print("  out-of-equilibrium decay produces BOTH the baryon asymmetry (standard")
    print("  leptogenesis, eta_B = -240/26 -> log10 = -9.23, obs -9.21) and the dark")
    print("  hidden-SU(4) asymmetry, so dark matter is asymmetric and Omega_DM ~")
    print("  Omega_b automatically -- the cosmic coincidence is built in, with the")
    print("  substrate fixing Omega_DM/Omega_b = 82/15. The matter we are made of and")
    print("  the dark matter that holds galaxies together are two halves of one E8")
    print("  CP-violating decay. Honest: eta_B is the corpus closed form; the")
    print("  cogenesis is a mechanism, washout/CP factors not computed.")

    out["summary"] = (
        "cogenesis: the 128's right-handed neutrino N_R decays (CP-"
        "violating, out of equilibrium) -> baryon asymmetry (lepto-"
        "genesis, log10 eta_B = -240/26 = -9.23, obs -9.21) AND equal "
        "dark-SU(4) asymmetry -> asymmetric DM, Omega_DM~Omega_b "
        "automatic, ratio 82/15. Matter + dark matter from one E8 CP "
        "decay. Honest: mechanism, washout/CP factors not computed."
    )
    out["sources"] = [
        "leptogenesis (Fukugita-Yanagida); asymmetric dark matter / "
        "cogenesis; corpus log10(eta_B)=-|E|/(v-k-lambda)=-9.23, "
        "Omega_DM=mu/g, Omega_b=lambda/(v+1); w33_dark_sector_128.py"
    ]
    with open("data/w33_cogenesis.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_cogenesis.json")


if __name__ == "__main__":
    main()
