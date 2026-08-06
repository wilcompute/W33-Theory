#!/usr/bin/env python3
"""Pass 3990: exact sparse W33 analog coupler and robustness certificate."""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_3990_PHYSICAL_W33_COUPLER.json"
EXPECTED_SEMANTIC = "b4f3fea2f768c124f6190719b8895dc44205fda85319a4cd94b842a9aff24a88"


def canonical_sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def normalize_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % 3 for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple(inv*y % 3 for y in v)
    raise ValueError("zero vector")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return (x[0]*y[2] + x[1]*y[3] - x[2]*y[0] - x[3]*y[1]) % 3


def build_adjacency() -> np.ndarray:
    points = sorted({normalize_projective(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    adjacency = np.zeros((40,40), dtype=np.int64)
    for i,x in enumerate(points):
        for j in range(i+1,40):
            if symplectic(x, points[j]) == 0:
                adjacency[i,j] = adjacency[j,i] = 1
    I=np.eye(40,dtype=np.int64); J=np.ones((40,40),dtype=np.int64)
    assert np.array_equal(adjacency@adjacency, 8*I-2*adjacency+4*J)
    return adjacency


def build() -> dict[str, object]:
    A=build_adjacency(); I=np.eye(40); J=np.ones((40,40))
    eigen=Counter(int(round(x)) for x in np.linalg.eigvalsh(A.astype(float)))
    assert eigen == Counter({12:1,2:24,-4:15})
    assert int(A.sum()//2)==240

    # Spectral interpolation for exp(-i*pi*A/2).
    target=-(I+A)/3 + 2*J/15
    assert np.allclose(target@target,I,atol=1e-12)
    assert np.allclose(target,target.T,atol=1e-12)
    for lam, expected in ((12,1),(2,-1),(-4,1)):
        assert abs(np.exp(-1j*np.pi*lam/2)-expected)<1e-12
    assert set(np.unique(np.round(target,12))) == {-0.2, 2/15}

    # Exact multiplicity-weighted coupling-error response.
    # For kappa*z=(pi/2)(1+eps), U0^* Ueps has phases
    # exp[-i*pi*eps*(6,1,-2)] on multiplicities (1,24,15).
    slopes=(-6,-1,2); multiplicities=(1,24,15); dimension=40
    weighted_mean=sum(s*m for s,m in zip(slopes,multiplicities))/dimension
    weighted_second=sum(s*s*m for s,m in zip(slopes,multiplicities))/dimension
    assert weighted_mean==0 and weighted_second==3

    payload: dict[str, object] = {
      "schema":"w33.pass3990.physical_sparse_coupler.v1",
      "status":"PASS_EXACT_SPARSE_ANALOG_COUPLER_MODEL_HARDWARE_PENDING",
      "graph":{"vertices":40,"degree":12,"edges":240,"adjacency_spectrum":{"12":1,"2":24,"-4":15}},
      "coupled_mode_equation":"i d psi/dz = kappa A_W33 psi",
      "exact_interaction_area":"kappa*z=pi/2 modulo 2*pi",
      "exact_transfer":"exp(-i*pi*A_W33/2)=-(I+A_W33)/3+2J/15",
      "transfer":{"involution":True,"symmetric":True,"row_amplitudes":{"point_or_neighbor":"-1/5","nonneighbor":"2/15"},"row_multiplicities":{"point_or_neighbor":13,"nonneighbor":27}},
      "implementation_counting":{"equal_coupling_links":240,"simultaneous_analog_sections":1,"programmable_diagonal_ports_needed_for_this_fixed_reflection":0},
      "uniform_fractional_coupling_error":{
        "relative_phase_slopes_in_units_of_pi_epsilon":[-6,-1,2],
        "multiplicities":[1,24,15],
        "weighted_first_moment":0,
        "weighted_second_moment":3,
        "process_fidelity_expansion":"F_pro=1-3*pi^2*epsilon^2+O(epsilon^3)",
        "average_gate_fidelity_expansion":"F_avg=1-(120/41)*pi^2*epsilon^2+O(epsilon^3)",
        "interpretation":"Uniform coupling-length miscalibration has no linear average-fidelity penalty because Tr A_W33=0."
      },
      "comparison":{"dense_36_port_adjacent_factors":398,"w33_analog_operation":"one simultaneous sparse Hamiltonian flight","warning":"These implement different target spaces and cost models; the analog result does not prove a 36-port mesh optimum."},
      "boundary":"Exact coupled-mode transfer under an ideal equal-edge W33 Hamiltonian. Layout feasibility, non-nearest physical crossings, coupling uniformity, loss, fabrication, bandwidth, and measured fidelity remain open.",
    }
    payload["semantic_sha256"]=canonical_sha(payload)
    assert payload["semantic_sha256"]==EXPECTED_SEMANTIC
    return payload


def main() -> None:
    payload=build()
    OUTPUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("PASS_PHYSICAL_W33_COUPLER",payload["semantic_sha256"])


if __name__=="__main__":
    main()
