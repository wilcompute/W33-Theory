#!/usr/bin/env python3
"""Passes 3993-3996: exact W33 Wigner-Smith memory and causal scaling."""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_3993_3996_WIGNER_SMITH_CAUSAL_MEMORY.json"
EXPECTED_SEMANTIC = "5a666b410a874ac934ca60271f993ae74cc0c0605ef67c15834036baa3f7182d"


def canonical_sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % 3 for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple(inv*y % 3 for y in v)
    raise ValueError("zero vector")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0]*y[2] + x[1]*y[3] - x[2]*y[0] - x[3]*y[1]) % 3


def build_w33() -> np.ndarray:
    points = sorted({normalize_projective(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    assert len(points) == 40
    A = np.zeros((40, 40), dtype=np.int64)
    for i, x in enumerate(points):
        for j in range(i + 1, 40):
            if symplectic(x, points[j]) == 0:
                A[i, j] = A[j, i] = 1
    I = np.eye(40, dtype=np.int64)
    J = np.ones((40, 40), dtype=np.int64)
    assert np.array_equal(A @ A, 8*I - 2*A + 4*J)
    return A


def convolve(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out: Counter[int] = Counter()
    for a, ma in left.items():
        for b, mb in right.items():
            out[a+b] += ma*mb
    return dict(sorted(out.items()))


def build() -> dict[str, object]:
    A = build_w33()
    L = 12*np.eye(40, dtype=np.int64) - A
    assert Counter(int(round(x)) for x in np.linalg.eigvalsh(L.astype(float))) == Counter({0:1, 10:24, 16:15})
    assert int(np.trace(L)) == 480 and int(np.trace(L @ L)) == 6240
    distribution = {0:1, 10:24, 16:15}
    mean = sum(x*m for x,m in distribution.items())/40
    second = sum(x*x*m for x,m in distribution.items())/40
    assert mean == 12 and second-mean*mean == 12

    shells: dict[str, dict[str, int]] = {}
    current = {0:1}
    for m in range(1,5):
        current = convolve(current, distribution)
        total = 40**m
        mu = sum(x*n for x,n in current.items())/total
        var = sum((x-mu)**2*n for x,n in current.items())/total
        assert sum(current.values()) == total and mu == 12*m and var == 12*m
        shells[str(m)] = {str(k):v for k,v in current.items()}

    B = np.ones((40,40), dtype=np.int64) - np.eye(40,dtype=np.int64) - A
    assert Counter(int(round(x)) for x in np.linalg.eigvalsh((A+B).astype(float))) == Counter({39:1,-1:39})
    assert Counter(int(round(x)) for x in np.linalg.eigvalsh((A-B).astype(float))) == Counter({-15:1,5:24,-7:15})

    payload: dict[str, object] = {
      "schema":"w33.pass3993_3996.wigner_smith_causal_memory.v1",
      "status":"PASS_EXACT_WIGNER_SMITH_MEMORY_WITH_DECLARED_CAUSAL_MODELS",
      "w33_laplacian":{"spectrum":{"0":1,"10":24,"16":15},"trace":480,"trace_square":6240},
      "wigner_smith_theorem":{
        "scattering_unitary":"S(omega)=exp(i theta(omega) L_W33)",
        "proper_delay_operator":"Q(omega)=-i S(omega)^dagger dS/domega=theta'(omega)L_W33",
        "proper_delay_sectors_in_units_of_theta_prime":{"0":1,"10":24,"16":15},
        "mean_delay_in_units_of_theta_prime":12,
        "delay_variance_in_units_of_theta_prime_squared":12,
        "total_delay_in_units_of_theta_prime":480,
        "density_of_states_convention":"Delta rho(omega)=Tr Q(omega)/(2 pi)",
        "interpretation":"Time-as-memory is the stored/dwell-time spectrum of the multiport. More internal resonant structure increases delay or density of states; it does not change the vacuum causal front."
      },
      "self_similar_delay_shells":{
        "generating_polynomial":"(1+24 z^10+15 z^16)^m",
        "multiplicities_m1_to_m4":shells,
        "mean_in_units_of_theta_prime":"12m",
        "variance_in_units_of_theta_prime_squared":"12m",
        "total_trace_in_units_of_theta_prime":"12m*40^m",
        "interpretation":"Tensor self-similarity multiplies mode count but adds proper-delay history. The delay distribution is an additive memory ledger over exponentially many modes."
      },
      "self_similar_information_delay_invariant":{
        "address_bits":"m*log2(40)",
        "mean_proper_delay":"12m*theta_prime",
        "bits_per_mean_proper_delay":"log2(40)/(12*theta_prime)",
        "relative_delay_standard_deviation":"1/sqrt(12m)",
        "interpretation":"Self-similarity scales accessible address space and accumulated dwell-time history together; their ratio is independent of tensor depth m."
      },
      "dual_geometry_delay_echo":{
        "common_generator":"A+B=J-I","common_spectrum":[39,-1,-1],
        "contrast_generator":"A-B","contrast_spectrum":[-15,5,-7],
        "protected_nonuniform_delay_split_in_units_of_theta_prime":12,
        "interpretation":"The common arm is geometry-blind on the 39-dimensional nonuniform sector; the contrast arm isolates W33-specific delay memory."
      },
      "causal_refinement_law":{
        "generic_graph_speed_bound":"v_graph <= C_LR(Delta) J/hbar graph-edges per second",
        "physical_speed":"v_internal <= a C_LR(Delta) J/hbar",
        "scale_invariant_condition":"a J = constant",
        "N_node_refinement":"a_N=L/N and J_N >= hbar c N/(C_LR(12)L) to keep the internal causal cone matched to c",
        "interpretation":"Packing more serial nodes without raising coupling strength slows the internal graph cone. Node density alone cannot raise or set vacuum c."
      },
      "photon_falsifier":{
        "null":"After conditioning on spectrum, transverse momentum, resonant dwell time, encoder, detector, and path length, changing mode count changes capacity/intercept but not the vacuum propagation slope.",
        "hidden_node_signal":"A residual mode-count-dependent front-arrival slope after subtracting the measured Wigner-Smith proper delays.",
        "required_firewall":"Separate causal-front timing from pulse peak/group delay and independently reconstruct Q from the frequency derivative of the scattering matrix."
      },
      "primary_sources":[
        "Patel and Michielssen, Wigner-Smith Time Delay Matrix for Electromagnetics, arXiv:2003.06985",
        "Nachtergaele, Sims, and Young, Quasi-Locality Bounds for Quantum Lattice Systems I, arXiv:1810.02428",
        "Yang et al., Programmable high-dimensional Hamiltonian in a photonic waveguide array, arXiv:2311.14951"
      ],
      "boundary":"The W33 matrix identities and tensor-shell laws are exact. The electromagnetic realization, Lieb-Robinson prefactor, reconstructed proper delays, hidden-node test, hardware, and laboratory performance are declared models or future measurements. No variable vacuum c or literal photon-node ontology is claimed."
    }
    payload["semantic_sha256"] = canonical_sha(payload)
    assert payload["semantic_sha256"] == EXPECTED_SEMANTIC
    return payload


def main() -> None:
    payload = build()
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS_WIGNER_SMITH_CAUSAL_MEMORY",payload["semantic_sha256"])


if __name__ == "__main__":
    main()
