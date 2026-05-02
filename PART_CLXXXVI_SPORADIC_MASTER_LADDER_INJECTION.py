#!/usr/bin/env python3
"""
PART CLXXXVI - Sporadic / Moonshine Master-Ladder Injection
===========================================================

CLXXXI ranked the fifth bridge as:

    sporadic tower atom injection.

Goal:
    Test whether the CLXXX master ladder

        7 -> 8 -> 27 -> 81 -> 78 -> 248

    appears inside the Suzuki / sporadic / Moonshine files.

Committed source evidence:
    pillars/THEORY_PART_CCXXXVII_SPORADIC_LANDSCAPE.py
      - Thompson group Th has minimal representation dimension 248.
      - Th < E8(F3), giving a W(3,3) over F3 -> E8(F3) -> Th -> Monster path.
      - Fi22 has minimal representation dimension 78.
      - Monster first irrep dimension 196883 and 196884=196883+1 moonshine.

    tests/test_sporadic_tower_closure_ccxv.py
      - tau=252 = k*q*Phi6 = 12*3*7.
      - Suzuki v' = Phi6*tau + lambda*q^2 = 1782.
      - Suzuki k' = q*137 + (q+2) = 416.
      - Monster chi1 = 196883 = (v+Phi6)(v+k+Phi6)(Phi12-lambda).
      - j coefficient 196884 = tau*C(v,2) + 4*q^4.
      - j constant 744 = q*E + f = 3*240+24.
      - first six Monster prime exponents sum to 86 = E6+A2 = 78+8.

Interpretation:
    The master ladder injects into the sporadic continent in three exact ways:

      1. E8/Th injection:
           248 is both dim(E8) and min rep dimension of Thompson group Th.

      2. E6/Fi22 injection:
           78 is dim(E6) and the min rep dimension listed for Fi22.

      3. Moonshine/Suzuki arithmetic injection:
           Phi6=7 and q^4=81 enter tau, Suzuki, and j-coeff formulas exactly.

Honesty note:
    This is an injection/factorization audit, not a proof that W33 causes or
    classifies sporadic groups.  It records exact arithmetic and representation
    hooks already present in repo files and separates them from speculative
    explanatory claims.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

# W33 atoms
Q = 3
Q2 = Q * Q
Q3 = Q ** 3
Q4 = Q ** 4
V = 40
K = 12
LAM = 2
MU = 4
F = 24
G = 15
E = V * K // 2
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
PHI12 = Q ** 4 - Q ** 2 + 1
J = 5
J_INV = 8
E6_DIM = 78
A2_DIM = J_INV
G0_DIM = E6_DIM + A2_DIM
E8_DIM = 248
H1_DIM = Q4

# Sporadic/Suzuki/Moonshine atoms from committed tests.
TAU = K * Q * PHI6
ALPHA_INV = 137
V_SUZ = PHI6 * TAU + LAM * Q2
K_SUZ = Q * ALPHA_INV + (Q + 2)
LAM_SUZ = (Q + 2) ** LAM * MU
MU_SUZ = LAM * Q2 * MU + F
F_SUZ = Q * TAU + F
G_SUZ = MU * TAU - PHI6
CHI1_MONSTER = (V + PHI6) * (V + K + PHI6) * (PHI12 - LAM)
J_COEFF_1 = TAU * (V * (V - 1) // 2) + 4 * Q4
J_CONSTANT = Q * E + F
LEECH_KISSING = TAU * (V * (V - 1) // 2)
MONSTER_FIRST_SIX_EXPONENT_SUM = (Q * K + PHI4) + (V // 2) + (MU + PHI6 - LAM) + (K // 2) + LAM + Q
FI22_MIN_REP = E6_DIM
TH_MIN_REP = E8_DIM
CO1_I3_POWER_OF_TWO = 2 ** J_INV


@dataclass(frozen=True)
class SporadicInjectionLayer:
    name: str
    value: int
    formula: str
    interpretation: str
    status: str


def sporadic_injection_layers() -> List[SporadicInjectionLayer]:
    return [
        SporadicInjectionLayer("Phi6_in_tau", TAU, "tau=k*q*Phi6=12*3*7=252", "Ramanujan/Suzuki tower scalar uses the heptad", "exact arithmetic"),
        SporadicInjectionLayer("Suzuki_vertices", V_SUZ, "v'=Phi6*tau+lambda*q^2=1782", "Suzuki SRG vertex count receives Phi6 and q^2", "exact arithmetic"),
        SporadicInjectionLayer("Suzuki_valency", K_SUZ, "k'=q*137+(q+2)=416", "Suzuki valency uses q and alpha inverse", "exact arithmetic"),
        SporadicInjectionLayer("Monster_chi1", CHI1_MONSTER, "196883=(v+Phi6)(v+k+Phi6)(Phi12-lambda)", "Monster first irrep factors through W33/Phi6 primes 47,59,71", "exact arithmetic"),
        SporadicInjectionLayer("j_coefficient", J_COEFF_1, "196884=tau*C(40,2)+4*q^4", "moonshine coefficient includes q^4=81 correction", "exact arithmetic"),
        SporadicInjectionLayer("j_constant", J_CONSTANT, "744=q*E+f=3*240+24", "j constant uses W33 edge/E8-root count and f=24", "exact arithmetic"),
        SporadicInjectionLayer("Leech_kissing", LEECH_KISSING, "196560=tau*C(40,2)", "Leech kissing number through tau and W33 pair count", "exact arithmetic"),
        SporadicInjectionLayer("G0_exponent_sum", MONSTER_FIRST_SIX_EXPONENT_SUM, "46+20+9+6+2+3=86=78+8", "first six Monster prime exponents sum to E6+A2 dimension", "exact arithmetic"),
        SporadicInjectionLayer("Fi22_E6_hook", FI22_MIN_REP, "minrep(Fi22)=78=dim(E6)", "Fi22 provides E6-dimensional sporadic hook", "repo-listed representation hook"),
        SporadicInjectionLayer("Th_E8_hook", TH_MIN_REP, "minrep(Th)=248=dim(E8)", "Thompson provides E8-dimensional sporadic hook", "repo-listed representation hook"),
        SporadicInjectionLayer("Co1_tau_simplex_power", CO1_I3_POWER_OF_TWO, "2^8 with 8=J^{-1}", "Co1 tau-simplex I3 uses carrier exponent 8", "exact arithmetic in test continent"),
    ]


def sporadic_master_ladder_injection_audit() -> Dict[str, object]:
    checks = {
        "master_atoms": (PHI6, J_INV, Q3, Q4, E6_DIM, E8_DIM) == (7, 8, 27, 81, 78, 248),
        "tau_is_k_q_phi6": TAU == K * Q * PHI6 == 252,
        "suzuki_vertex_formula": V_SUZ == 1782,
        "suzuki_valency_formula": K_SUZ == 416,
        "suzuki_lambda_formula": LAM_SUZ == 100,
        "suzuki_mu_formula": MU_SUZ == 96,
        "suzuki_multiplicity_closure": 1 + F_SUZ + G_SUZ == V_SUZ,
        "monster_chi1_factorization": CHI1_MONSTER == 196883,
        "monster_chi1_factors": (V + PHI6, V + K + PHI6, PHI12 - LAM) == (47, 59, 71),
        "j_coefficient_formula": J_COEFF_1 == 196884 == CHI1_MONSTER + 1,
        "j_coefficient_q4_correction": J_COEFF_1 - LEECH_KISSING == 4 * Q4 == 324,
        "j_constant_formula": J_CONSTANT == 744,
        "leech_kissing_formula": LEECH_KISSING == 196560,
        "g0_exponent_sum": MONSTER_FIRST_SIX_EXPONENT_SUM == G0_DIM == 86,
        "fi22_e6_hook": FI22_MIN_REP == E6_DIM == 78,
        "th_e8_hook": TH_MIN_REP == E8_DIM == 248,
        "co1_power_of_two_uses_carrier": CO1_I3_POWER_OF_TWO == 2 ** J_INV == 256,
        "threshold_carrier_inverse": (J * J_INV) % PHI3 == 1,
        "phi6_carrier_step": PHI6 + 1 == J_INV,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXXVI_SPORADIC_MASTER_LADDER_INJECTION",
        "status": "exact arithmetic/representation-hook audit; not a classification proof",
        "source_links": {
            "sporadic_landscape": "pillars/THEORY_PART_CCXXXVII_SPORADIC_LANDSCAPE.py",
            "sporadic_tower_test": "tests/test_sporadic_tower_closure_ccxv.py",
            "CLXXX": "master identity ladder",
            "CLXXXI": "repo hint atlas",
        },
        "w33_atoms": {
            "q": Q,
            "q2": Q2,
            "q3": Q3,
            "q4": Q4,
            "v": V,
            "k": K,
            "lambda": LAM,
            "mu": MU,
            "f": F,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "Phi12": PHI12,
            "J": J,
            "J_inverse": J_INV,
            "E6_dim": E6_DIM,
            "E8_dim": E8_DIM,
        },
        "sporadic_injection_layers": [asdict(layer) for layer in sporadic_injection_layers()],
        "bridge_identities": {
            "master_ladder": "7 -> 8 -> 27 -> 81 -> 78 -> 248",
            "E8_Th_hook": "Th has min rep 248 and is listed as Th < E8(F3)",
            "E6_Fi22_hook": "Fi22 has min rep 78",
            "tau_injection": "tau=252=k*q*Phi6",
            "Suzuki_injection": "v'=Phi6*tau+lambda*q^2 and k'=q*137+(q+2)",
            "Moonshine_injection": "196883=(v+Phi6)(v+k+Phi6)(Phi12-lambda); 196884=tau*C(v,2)+4*q^4",
            "G0_injection": "first six Monster prime exponents sum to 86=E6+A2=78+8",
        },
        "careful_boundary": {
            "proved_here": "exact arithmetic identities and repo-listed representation hooks",
            "not_proved_here": "classification of sporadics from W33, causal derivation of Monster, or full Moonshine theorem",
            "next_measurement": "inspect atom dictionaries in newer grand-synthesis tests for systematic 7/8/27/81/248 recurrence",
        },
        "checks": checks,
        "theorem_statement": (
            "The CLXXX master ladder injects into the sporadic/Moonshine tower through exact arithmetic and representation hooks. "
            "The heptad Phi6 enters tau=252=kqPhi6 and Suzuki v'=Phi6*tau+lambda*q^2; the carrier q^4=81 enters "
            "196884=tau*C(40,2)+4q^4; the E6 dimension 78 appears as Fi22's listed minimal representation; the E8 dimension "
            "248 appears as Thompson's listed minimal representation and as Th < E8(F3); and the first six Monster prime exponents "
            "sum to 86=78+8.  This is an exact injection audit, not a proof that W33 classifies sporadic groups."
        ),
        "interpretive_note": (
            "The sporadic continent is no longer disconnected from the master ladder.  The strongest safe claim is that the ladder's atoms "
            "are already threaded through the committed Suzuki/Moonshine arithmetic and through the E6/E8 representation hooks."
        ),
    }


def main() -> int:
    audit = sporadic_master_ladder_injection_audit()
    out = ROOT / "PART_CLXXXVI_sporadic_master_ladder_injection_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
