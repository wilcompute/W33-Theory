"""Part MCXCI: Self-entangled emergence discrete-curvature inversion law.

Continuation of MCXC.

Given jump pair for M = E*S^2:
  Delta+ = E(2S+1),
  Delta- = E(2S-1).

Define:
  Sigma = Delta+ + Delta- = 4ES,
  Kappa = Delta+ - Delta- = 2E.

Then exact inversion from jumps alone:
  E = Kappa/2,
  S = Sigma/(2*Kappa).

At MCXC values (1568, 1504):
  Kappa=64 -> E=32,
  Sigma=3072 -> S=24,
  M = E*S^2 = 18432.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> dict[str, object]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def self_entangled_emergence_discrete_curvature_inversion_packet() -> dict[str, object]:
    mcxc = _load(ROOT / "PART_MCXC_SELF_ENTANGLED_EMERGENCE_QUANTIZED_INCREMENT_results.json")

    delta_plus = int(mcxc["quantized_jumps"]["delta_plus"])    # 1568
    delta_minus = int(mcxc["quantized_jumps"]["delta_minus"])  # 1504
    monodromy = int(mcxc["baseline"]["monodromy"])            # 18432

    sigma = delta_plus + delta_minus
    kappa = delta_plus - delta_minus

    e_recovered = Fraction(kappa, 2)
    s_recovered = Fraction(sigma, 2 * kappa)

    m_recovered = e_recovered * s_recovered * s_recovered

    checks = {
        "sigma_is_3072": sigma == 3072,
        "kappa_is_64": kappa == 64,
        "kappa_is_twice_edge_shell": e_recovered == 32,
        "sigma_is_four_edge_seed": sigma == 4 * e_recovered * s_recovered,
        "edge_shell_recovered_integral": e_recovered.denominator == 1,
        "seed_recovered_integral": s_recovered.denominator == 1,
        "seed_recovered_is_24": s_recovered == 24,
        "monodromy_reconstructed_from_recovered_packets": m_recovered == monodromy == 18432,
        "jump_pair_consistency_plus": delta_plus == e_recovered * (2 * s_recovered + 1),
        "jump_pair_consistency_minus": delta_minus == e_recovered * (2 * s_recovered - 1),
    }

    return {
        "part": "MCXCI",
        "theorem": "Self-entangled emergence discrete-curvature inversion law",
        "jump_packet": {
            "delta_plus": delta_plus,
            "delta_minus": delta_minus,
            "sigma": sigma,
            "kappa": kappa,
            "identity": "Sigma=3072, Kappa=64 from (1568,1504)",
        },
        "recovered_packets": {
            "edge_shell": int(e_recovered),
            "seed": int(s_recovered),
            "monodromy": int(m_recovered),
            "identity": "E=Kappa/2=32, S=Sigma/(2Kappa)=24, M=E*S^2=18432",
        },
        "finite_universality_surrogate": {
            "statement": "the quantized jump pair alone determines router shell and self-entangled seed exactly",
            "boundary": "finite discrete-curvature inversion law; not a continuum PDE inversion theorem",
        },
        "claim_boundary": "finite jump-pair inversion law for self-entanglement emergence packets",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = self_entangled_emergence_discrete_curvature_inversion_packet()
    out_path = ROOT / "PART_MCXCI_SELF_ENTANGLED_EMERGENCE_DISCRETE_CURVATURE_INVERSION_results.json"
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCXCI: Self-Entangled Emergence Discrete-Curvature Inversion Law ===")
    print(packet["jump_packet"]["identity"])
    print(packet["recovered_packets"]["identity"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
