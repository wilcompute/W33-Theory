#!/usr/bin/env python3
"""BT1041: real/chiral finite Dirac candidate for the BT1038 A_F carrier.

Key modelling choice: reinterpret the 162 carrier as

    H = C^2_chiral \otimes HS(K),   K = C^3_weakslot \otimes C^3_color,

so dim H = 2 * 9^2 = 162.  This realizes the opposite algebra correctly:
left multiplication gives rho(A_F), while J turns left multiplication into right
multiplication.  That is the correct setting for the first-order condition.

The finite Dirac candidate is

    gamma = sigma_z \otimes 1,
    J     = sigma_x \otimes star,   star(X)=X^*,
    D_F   = sigma_x \otimes (L_Phi + R_Phi),

with Phi a Hermitian weakslot Higgs matrix tensored with color identity.  Then
J^2=1, J gamma = - gamma J, JD=DJ, and gamma D = -D gamma by construction.
"""
from __future__ import annotations

import json
from pathlib import Path

K_DIM = 9
H_DIM = 2 * K_DIM * K_DIM


def main() -> None:
    out = {
        "theorem": "BT1041 real/chiral finite Dirac candidate",
        "carrier_model": "H = C^2_chiral tensor HS(K), K=C^3_weakslot tensor C^3_color",
        "K_dimension": K_DIM,
        "HS_K_dimension": K_DIM * K_DIM,
        "carrier_dimension": H_DIM,
        "target_dimension": 162,
        "dimension_hit": H_DIM == 162,
        "operators": {
            "gamma": "sigma_z tensor identity",
            "J": "sigma_x tensor star antiunitary, star(X)=X^*",
            "D_F": "sigma_x tensor (L_Phi + R_Phi) with Phi Hermitian"
        },
        "ko_signs_candidate": {
            "J_squared": "+1",
            "J_gamma": "- gamma_J",
            "J_D": "D_J",
            "gamma_D": "- D_gamma"
        },
        "why_this_matters": "Using HS(K) gives genuine left and right actions, so the opposite algebra and first-order test can be represented without faking commutation on a single left module.",
        "next": "BT1042 verifies the first-order commutator [[D_F,L_a],R_b]=0 on generator spans."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1041_real_chiral_dirac_candidate.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
