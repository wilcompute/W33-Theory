"""Passes 3584-3590: exact Monster/W33 evidence firewall.

This verifier deliberately separates four levels:
  A. exact integer identities;
  B. externally documented group facts;
  C. structural bridges requiring an explicit embedding/intertwiner;
  D. numerological coincidences that must not be promoted as mechanisms.

It does not construct the Monster and does not claim that an integer identity
is a subgroup, representation, VOA, or physical derivation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

MONSTER_ORDER = 808017424794512875886459904961710757005754368000000000
PSP43_ORDER = 25_920
WE6_ORDER = 51_840
W33_V = 40
W33_K = 12
W33_LAMBDA = 2
W33_MU = 4
W33_EDGES = 240
E8_DIM = 248
LEECH_KISSING = 196_560
MONSTER_MIN_IRREP = 196_883
J1 = 196_884

@dataclass(frozen=True)
class Claim:
    name: str
    value: bool
    level: str
    interpretation: str

claims = [
    Claim("PSp(4,3) order", PSP43_ORDER == 2**6 * 3**4 * 5, "A", "exact order identity"),
    Claim("W(E6) order", WE6_ORDER == 2 * PSP43_ORDER, "A", "exact outer-extension scale"),
    Claim("Monster divisible by PSp(4,3)", MONSTER_ORDER % PSP43_ORDER == 0, "A", "necessary, not sufficient, for embedding"),
    Claim("Monster divisible by W(E6)", MONSTER_ORDER % WE6_ORDER == 0, "A", "necessary, not sufficient, for embedding"),
    Claim("minimal irrep factorization", MONSTER_MIN_IRREP == 47 * 59 * 71, "A", "exact factorization by the three largest Monster primes"),
    Claim("first moonshine coefficient", J1 == MONSTER_MIN_IRREP + 1, "A", "trivial plus minimal representation dimension"),
    Claim("Leech correction", J1 == LEECH_KISSING + 18**2, "A", "exact decomposition; mechanism requires VOA/lattice data"),
    Claim("j constant arithmetic", 744 == 3 * E8_DIM, "A", "exact integer identity only"),
    Claim("elliptic point arithmetic", 1728 == W33_K**3, "A", "exact integer identity only"),
    Claim("central charge arithmetic", 24 == W33_K * W33_LAMBDA, "A", "matches V^natural central charge; not a derivation"),
    Claim("E8 edge correction", E8_DIM == W33_EDGES + 2 * W33_MU, "A", "exact integer identity only"),
]

assert all(c.value for c in claims)

quotients = {
    "monster_over_psp43": MONSTER_ORDER // PSP43_ORDER,
    "monster_over_we6": MONSTER_ORDER // WE6_ORDER,
}

firewall = {
    "documented_external_facts": [
        "PSp(4,3) is isomorphic to U4(2).",
        "The Monster has subgroups isomorphic to U4(2); the double cover 2.U4(2) is a distinct question.",
        "The Monster has a 196884-dimensional Griess/Moonshine degree-two space and minimal nontrivial irreducible degree 196883.",
    ],
    "not_proved_here": [
        "a canonical embedding of the repo's concrete W33 permutation action into a fixed Monster model",
        "a class-fusion map from W33 element classes to Monster conjugacy classes",
        "an intertwiner from an 81-dimensional W33 module into a specified Monster module",
        "a VOA or Majorana-algebra multiplication recovered from W33 incidence alone",
        "any physical prediction derived solely from the integer coincidences above",
    ],
    "promotion_rule": "No level-A identity may be described as a mechanism until an explicit level-C map is supplied and checked.",
}

result = {
    "verified": True,
    "claims": [asdict(c) for c in claims],
    "quotients": quotients,
    "firewall": firewall,
}

if __name__ == "__main__":
    out = Path("data/PART_3584_3590_MONSTER_EVIDENCE_FIREWALL_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
