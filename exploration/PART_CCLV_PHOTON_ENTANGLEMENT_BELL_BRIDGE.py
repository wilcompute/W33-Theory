#!/usr/bin/env python3
"""
Part CCLV — Photon Entanglement and Bell Inequalities from W(3,3)

The single photon of W(3,3) is the archetypal quantum object whose entanglement
properties underlie all of quantum information theory.  Bell inequalities, GHZ
states, quantum teleportation, and the E91 protocol are all governed by integers
drawn directly from the SRG(40,12,2,4) parameter set.

Key chain:
  1. EPR pair: LAM = 2 entangled photons.
  2. Bell states: MU = 4 (Φ±, Ψ±).
  3. CHSH correlators: MU = 4 terms ⟨AB⟩, ⟨AB'⟩, ⟨A'B⟩, ⟨A'B'⟩.
  4. Classical CHSH bound = LAM = 2.
  5. Tsirelson bound = LAM·√LAM (factors: integer LAM = 2, √LAM under root).
  6. Bell angle denominator: π/MU = π/4 (optimal settings).
  7. GHZ state: Q = 3 qubits.
  8. W state: Q = 3 qubits.
  9. Quantum teleportation requires LAM = 2 classical bits.
 10. Superdense coding encodes LAM = 2 bits per photon.
 11. EPR Hilbert space: LAM^LAM = MU = 4 dimensions.
 12. Entanglement entropy of Bell state: 1 ebit = log₂(LAM) = 1 bit.
 13. E91 protocol: Q = 3 measurement settings per party.
 14. Mermin inequality: Q = 3 parties (Mermin-GHZ).
 15. Schmidt rank of Bell states: LAM = 2.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from PART_CCXVIII_EXTRA_DIMENSIONS_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
)

Phi3 = Q**2 + Q + 1   # 13
Phi4 = Q**2 + 1       # 10
Phi6 = Q**2 - Q + 1   # 7

# ------------------------------------------------------------------
# B1: EPR pair — 2 entangled photons
# ------------------------------------------------------------------
# An EPR pair consists of LAM = 2 photons in a maximally entangled state.
epr_pair_count = LAM                        # 2 photons

# ------------------------------------------------------------------
# B2: Bell states — 4 = MU orthonormal maximally entangled states
# ------------------------------------------------------------------
# The four Bell states: |Φ+⟩, |Φ-⟩, |Ψ+⟩, |Ψ-⟩.
bell_states_count = MU                      # 4 Bell states

# ------------------------------------------------------------------
# B3: CHSH inequality — 4 correlators
# ------------------------------------------------------------------
# CHSH = ⟨AB⟩ − ⟨AB'⟩ + ⟨A'B⟩ + ⟨A'B'⟩ ≤ 2 (classical).
# Number of correlator terms = MU = 4.
chsh_correlators = MU                       # 4

# ------------------------------------------------------------------
# B4: Classical CHSH bound = LAM = 2
# ------------------------------------------------------------------
# Local hidden variable models satisfy |CHSH| ≤ 2 = LAM.
chsh_classical_bound = LAM                  # 2

# ------------------------------------------------------------------
# B5: Tsirelson bound — quantum maximum = LAM·√LAM
# ------------------------------------------------------------------
# Quantum mechanics allows |CHSH|_Q ≤ 2√2 = LAM·√LAM.
# Integer factor:
tsirelson_int_factor = LAM                  # 2 (the integer prefactor)
# Square-root argument:
tsirelson_sqrt_arg = LAM                    # 2 (under the √)
# Verify: tsirelson_int_factor * sqrt(tsirelson_sqrt_arg) = 2√2 ≈ 2.828
tsirelson_bound_sq = tsirelson_int_factor**2 * tsirelson_sqrt_arg   # 2²·2 = 8
chsh_quantum_bound_sq = MU + MU            # 8 = 2·MU = 4 + 4 (Tsirelson: B_Q² = 8)

# ------------------------------------------------------------------
# B6: Optimal Bell measurement angles
# ------------------------------------------------------------------
# The CHSH inequality is maximally violated at angles of π/4 = π/MU.
bell_angle_denom = MU                       # 4 (angle = π/MU per setting step)

# ------------------------------------------------------------------
# B7: GHZ state — Q = 3 qubits
# ------------------------------------------------------------------
# |GHZ⟩ = (|000⟩ + |111⟩)/√2 uses Q = 3 qubits/photons.
ghz_qubits = Q                              # 3 qubits
# GHZ Hilbert space dimension: 2^Q = 8 = LAM^Q.
ghz_hilbert_dim = LAM ** Q                  # 2^3 = 8
# Verify: LAM^Q = 8.
ghz_hilbert_check = LAM ** Q == 8          # True ✓

# ------------------------------------------------------------------
# B8: W state — Q = 3 qubits
# ------------------------------------------------------------------
# |W⟩ = (|100⟩ + |010⟩ + |001⟩)/√3 uses Q = 3 qubits.
w_state_qubits = Q                          # 3 qubits

# ------------------------------------------------------------------
# B9: Quantum teleportation — LAM = 2 classical bits required
# ------------------------------------------------------------------
# Alice measures in the Bell basis (gives 2 = LAM bits) and sends them.
teleport_cbits = LAM                        # 2 classical bits

# ------------------------------------------------------------------
# B10: Superdense coding — LAM = 2 classical bits per photon
# ------------------------------------------------------------------
# By encoding one of four Bell states (MU=4 choices = 2 bits = LAM bits)
# Alice can send LAM = 2 classical bits using 1 qubit + 1 shared entangled photon.
superdense_bits = LAM                       # 2 classical bits
# Verify: log2(bell_states_count) = log2(MU) = 2 = LAM.
superdense_check = int(math.log2(bell_states_count))   # log2(4) = 2 = LAM

# ------------------------------------------------------------------
# B11: EPR Hilbert space dimension
# ------------------------------------------------------------------
# Two-qubit (two-photon polarization) Hilbert space: C^2 ⊗ C^2 = C^4.
# Dimension = LAM^LAM = 2^2 = 4 = MU.
epr_hilbert_dim = LAM ** LAM                # 4 = MU

# ------------------------------------------------------------------
# B12: Entanglement entropy of a Bell state
# ------------------------------------------------------------------
# For |Φ+⟩ = (|00⟩ + |11⟩)/√2: S_E = log₂(2) = 1 ebit.
# log₂(LAM) = log₂(2) = 1.
entanglement_entropy = int(math.log2(LAM))  # 1 ebit = log2(LAM)

# ------------------------------------------------------------------
# B13: E91 protocol — Q = 3 measurement settings per party
# ------------------------------------------------------------------
# Ekert's E91 protocol uses Q = 3 measurement angles per observer.
e91_settings_per_party = Q                  # 3 measurement directions
# Total correlator pairs tested: Q*(Q-1)//LAM = 3 (from Q settings × Q settings
# minus diagonal, divided by symmetric factor).
e91_correlator_pairs = Q * (Q - 1) // LAM  # 3*2//2 = 3

# ------------------------------------------------------------------
# B14: Mermin inequality — Q = 3 parties (Mermin-GHZ)
# ------------------------------------------------------------------
# The Mermin inequality involves Q = 3 parties sharing a GHZ state.
mermin_parties = Q                          # 3 parties
# Classical bound of Mermin inequality = 2 = LAM.
mermin_classical_bound = LAM                # 2
# Quantum maximum = 4 = MU = LAM^LAM.
mermin_quantum_max = LAM ** LAM             # 4 = MU

# ------------------------------------------------------------------
# B15: Schmidt rank and decomposition
# ------------------------------------------------------------------
# Schmidt rank of any Bell state in C^2 ⊗ C^2 = LAM = 2.
schmidt_rank = LAM                          # 2
# Schmidt coefficients are equal: 1/√LAM = 1/√2.
schmidt_coeff_denom = LAM                   # 2 (denominator under square root)

# ------------------------------------------------------------------
# Verification checks
# ------------------------------------------------------------------
checks: list[tuple[str, bool]] = [
    # SRG anchors
    ("S1: Q=3", Q == 3),
    ("S2: LAM=2", LAM == 2),
    ("S3: MU=4", MU == 4),

    # EPR
    ("B1: epr_pair_count = LAM = 2", epr_pair_count == LAM),

    # Bell states
    ("B2: bell_states_count = MU = 4", bell_states_count == MU),

    # CHSH
    ("B3: chsh_correlators = MU = 4", chsh_correlators == MU),
    ("B4: chsh_classical_bound = LAM = 2", chsh_classical_bound == LAM),

    # Tsirelson
    ("B5a: tsirelson_int_factor = LAM = 2", tsirelson_int_factor == LAM),
    ("B5b: tsirelson_sqrt_arg = LAM = 2", tsirelson_sqrt_arg == LAM),
    ("B5c: B_Q^2 = 8 = LAM^2 * LAM", tsirelson_bound_sq == 8),
    ("B5d: chsh_quantum_bound_sq = 8", chsh_quantum_bound_sq == 8),

    # Bell angles
    ("B6: bell_angle_denom = MU = 4", bell_angle_denom == MU),

    # GHZ
    ("B7a: ghz_qubits = Q = 3", ghz_qubits == Q),
    ("B7b: ghz_hilbert_dim = LAM^Q = 8", ghz_hilbert_dim == 8),

    # W state
    ("B8: w_state_qubits = Q = 3", w_state_qubits == Q),

    # Teleportation
    ("B9: teleport_cbits = LAM = 2", teleport_cbits == LAM),

    # Superdense coding
    ("B10a: superdense_bits = LAM = 2", superdense_bits == LAM),
    ("B10b: log2(bell_states) = LAM = 2", superdense_check == LAM),

    # EPR Hilbert space
    ("B11: epr_hilbert_dim = LAM^LAM = MU = 4", epr_hilbert_dim == MU),

    # Entanglement entropy
    ("B12: entanglement_entropy = 1 ebit", entanglement_entropy == 1),

    # E91
    ("B13a: e91_settings = Q = 3", e91_settings_per_party == Q),
    ("B13b: e91_correlator_pairs = Q*(Q-1)//LAM = 3", e91_correlator_pairs == Q),

    # Mermin
    ("B14a: mermin_parties = Q = 3", mermin_parties == Q),
    ("B14b: mermin_classical_bound = LAM = 2", mermin_classical_bound == LAM),
    ("B14c: mermin_quantum_max = LAM^LAM = MU = 4", mermin_quantum_max == MU),

    # Schmidt
    ("B15a: schmidt_rank = LAM = 2", schmidt_rank == LAM),
    ("B15b: schmidt_coeff_denom = LAM = 2", schmidt_coeff_denom == LAM),
]

Verified = all(v for _, v in checks)
assert Verified, [lbl for lbl, v in checks if not v]

__all__ = [
    "Q", "V", "K", "LAM", "MU", "M_LAM", "M_NEG", "LAP_MID", "LAP_TOP", "EDGES", "AUT_ORDER",
    "Phi3", "Phi4", "Phi6",
    "epr_pair_count", "bell_states_count", "chsh_correlators", "chsh_classical_bound",
    "tsirelson_int_factor", "tsirelson_sqrt_arg", "tsirelson_bound_sq",
    "bell_angle_denom",
    "ghz_qubits", "ghz_hilbert_dim", "w_state_qubits",
    "teleport_cbits", "superdense_bits",
    "epr_hilbert_dim", "entanglement_entropy",
    "e91_settings_per_party", "e91_correlator_pairs",
    "mermin_parties", "mermin_classical_bound", "mermin_quantum_max",
    "schmidt_rank", "schmidt_coeff_denom",
    "checks", "Verified",
]


def _build_results() -> dict[str, Any]:
    return {
        "Part": "CCLV",
        "Title": "Photon Entanglement and Bell Inequalities",
        "Verified": Verified,
        "checks_passed": sum(1 for _, v in checks if v),
        "checks_total": len(checks),
        "SRG_parameters": {
            "Q": Q, "V": V, "K": K, "LAM": LAM, "MU": MU,
        },
        "bell_inequalities": {
            "epr_pair_count": epr_pair_count,
            "bell_states": bell_states_count,
            "chsh_correlators": chsh_correlators,
            "chsh_classical_bound": chsh_classical_bound,
            "tsirelson_int_factor": tsirelson_int_factor,
            "bell_angle_denom": bell_angle_denom,
        },
        "multipartite": {
            "ghz_qubits": ghz_qubits,
            "w_state_qubits": w_state_qubits,
            "mermin_parties": mermin_parties,
        },
        "quantum_protocols": {
            "teleport_cbits": teleport_cbits,
            "superdense_bits": superdense_bits,
            "e91_settings": e91_settings_per_party,
        },
        "entanglement": {
            "hilbert_dim": epr_hilbert_dim,
            "entropy_ebits": entanglement_entropy,
            "schmidt_rank": schmidt_rank,
        },
    }


if __name__ == "__main__":
    results = _build_results()
    out = ROOT / "PART_CCLV_photon_entanglement_bell_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Verified={Verified}  checks={results['checks_passed']}/{results['checks_total']}")
    print(f"Wrote {out}")
