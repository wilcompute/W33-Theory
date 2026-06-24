#!/usr/bin/env python3
"""
The 128 spinor of E8 is the dark sector: E8 = SO(16) + 128, with SO(16) (dim
120 = vq) the visible gauge/CC sector and the 128 = dark matter under a hidden
SU(4) = SO(6).

The previous move identified the cosmological-constant sector as SO(16) (dim 120 =
vq) inside E8 via the conformal embedding (D8)_1 < (E8)_1. The standard E8
decomposition closes the rest:
  E8 = SO(16) + 128_spinor,   248 = 120 + 128,   128 = 2^7 = 2^{Phi6}.
Under SO(16) > SO(10) x SO(6) = SO(10) x SU(4):
  adjoint 120 = (45,1) + (1,15) + (10,6)     [visible: SO(10) GUT + SU(4) + bifund]
  spinor  128 = (16,4) + (16bar, 4bar)       [DARK: SM generation 16 x hidden SU(4)]
The 16 is the Standard-Model generation (the SO(10) spinor, one family incl
nu_R); the 4 is the fundamental of a HIDDEN SU(4) = SO(6) with mu = 4 'dark
colors'. So the 128 is visible-matter content replicated under a dark gauge group
-- a dark-matter sector mirroring the families. The corpus dark fraction is
Omega_DM = mu/g, and mu = 4 reappears as the hidden-SU(4) multiplicity.

So the holographic E8 boundary predicts a dark sector: the visible world is the
SO(16) half (dim 120 = vq), the dark world is the 128 spinor (SM families under a
hidden SU(4)), and 120 + 128 = 248 is the visible/dark split of E8. Honest: the
group theory (120/128, the SO(10)xSU(4) branchings) is exact; the identification
of the 128 with the observed Omega_DM is a model-level proposal, not a derivation
of the relic density.
"""
from __future__ import annotations

import json

V, K, LAM, MU, Q, G, PHI6 = 40, 12, 2, 4, 3, 15, 7


def main():
    out = {}

    # E8 = SO(16) + 128
    dim_so16, dim_spinor = 120, 128
    print("[E8 visible/dark split]")
    print(
        f"  E8 = SO(16) + 128_spinor: {dim_so16} + {dim_spinor} = "
        f"{dim_so16+dim_spinor} = dim E8"
    )
    print(f"  visible SO(16): dim {dim_so16} = vq = {V*Q} (gauge/CC sector)")
    print(f"  dark spinor:    dim {dim_spinor} = 2^7 = 2^Phi6 = 2^{PHI6}")
    assert dim_so16 == V * Q == 120 and dim_spinor == 2**PHI6 == 128
    assert dim_so16 + dim_spinor == 248
    out["visible_SO16"] = dim_so16
    out["dark_spinor"] = dim_spinor

    # SO(16) > SO(10) x SO(6)=SU(4) branchings
    adj_120 = {"(45,1) SO(10) GUT": 45, "(1,15) SU(4)": 15, "(10,6) bifund": 60}
    spin_128 = {"(16,4) family x dark-SU(4)": 64, "(16bar,4bar)": 64}
    print("\n[branchings under SO(10) x SU(4)]")
    print(f"  adjoint 120 = (45,1)+(1,15)+(10,6) = {sum(adj_120.values())} (visible)")
    print(f"  spinor  128 = (16,4)+(16bar,4bar) = {sum(spin_128.values())} (DARK)")
    assert sum(adj_120.values()) == 120 and sum(spin_128.values()) == 128
    print(
        f"  16 = SM generation (SO(10) spinor incl nu_R); 4 = hidden SU(4)=SO(6) "
        f"fund, mu = {MU} dark colors"
    )
    out["adjoint_120_branching"] = adj_120
    out["spinor_128_branching"] = spin_128

    # dark fraction reappearance of mu
    print("\n[dark fraction]")
    print(
        f"  corpus Omega_DM = mu/g = {MU}/{G} = {MU/G:.4f}; the hidden SU(4) "
        f"multiplicity is mu = {MU} (the dark colors)"
    )
    out["omega_dm"] = f"mu/g = {MU}/{G}"

    print("\nRESULT: the 128 spinor of E8 is the dark sector. E8 = SO(16) + 128 is")
    print("  the visible/dark split: SO(16) (dim 120 = vq) is the visible gauge and")
    print("  cosmological-constant sector, while the 128 = (16,4)+(16bar,4bar) is")
    print("  Standard-Model families (the 16) replicated under a HIDDEN SU(4)=SO(6)")
    print("  with mu=4 dark colors -- a dark-matter sector mirroring the generations.")
    print("  The holographic E8 boundary thus predicts a dark sector, and the same")
    print("  mu=4 that is the QEC distance and the de Sitter entropy factor is the")
    print("  number of dark colors. 128 = 2^Phi6 closes 120 + 128 = 248.")

    out["summary"] = (
        "E8 = SO(16)[120=vq, visible gauge/CC] + 128[dark spinor]; "
        "128 = 2^Phi6; under SO(10)xSU(4): 128 = (16,4)+(16bar,4bar) = "
        "SM family 16 x hidden SU(4)=SO(6) (mu=4 dark colors). "
        "Holographic E8 boundary predicts a dark sector mirroring the "
        "generations; Omega_DM=mu/g. Honest: branchings exact, relic "
        "density not derived."
    )
    out["sources"] = [
        "E8 = SO(16) + 128-spinor (248=120+128); SO(16)>SO(10)xSO(6) "
        "branchings; corpus Omega_DM=mu/g, 8-dim dark eigenspace; "
        "w33_e8_conformal_embeddings.py"
    ]
    with open("data/w33_dark_sector_128.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("\nwrote data/w33_dark_sector_128.json")


if __name__ == "__main__":
    main()
