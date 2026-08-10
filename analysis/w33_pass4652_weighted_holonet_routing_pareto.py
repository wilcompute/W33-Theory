#!/usr/bin/env python3
"""Pass 4652 — weighted Holonet routing Pareto falsifier.

Compare four exact shell profiles under a technology-neutral identical-per-hop
power-transmission factor eta in (0,1]:
  W33:          12,27
  selected135:  12,56,66
  selected270:  15,118,136
  Levi160:       6,18,54,81.

Two distinct objectives are kept separate:
  normalized delivery = mean eta^distance to a uniformly chosen destination;
  aggregate delivery  = sum eta^distance over all destinations.
This avoids smuggling address count into a per-destination loss claim.

The verifier also evaluates two *component-mixed literature benchmarks*, not
claimed integrated stacks: 0.38 dB / 14 us experimental MZI switching and
~1.05 dB / 1.27 ns experimental EO switching, each plus an illustrative 1 cm
edge at 1.77 dB/m SiN propagation and a common 98% detector factor. Those
numbers are context, while the ordering theorem is symbolic in eta.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4652_WEIGHTED_HOLONET_ROUTING_PARETO.json"

SHELLS = {
    "W33": [12,27],
    "selected135": [12,56,66],
    "selected270": [15,118,136],
    "Levi160": [6,18,54,81],
}


def poly(shell, e):
    return sum(n * e**d for d,n in enumerate(shell, start=1))


def metrics(shell, hop_db, detector_eff, switch_time_s):
    eta = 10 ** (-hop_db / 10.0)
    v = 1 + sum(shell)
    aggregate = detector_eff * sum(n * eta**d for d,n in enumerate(shell, start=1))
    avg_hops = sum(n*d for d,n in enumerate(shell, start=1)) / (v-1)
    return {
        "vertices": v,
        "per_hop_power_transmission": eta,
        "aggregate_delivered_destination_equivalents": aggregate,
        "mean_destination_success": aggregate / (v-1),
        "mean_hops": avg_hops,
        "worst_shortest_path_success": detector_eff * eta**len(shell),
        "mean_switching_latency_s": avg_hops * switch_time_s,
    }


def main():
    e = sp.symbols('eta', positive=True)
    A = {k: sp.expand(poly(v,e)) for k,v in SHELLS.items()}
    M = {k: sp.factor(A[k] / sum(SHELLS[k])) for k in SHELLS}

    diffs = {
        "W33_minus_selected135": sp.factor(M["W33"] - M["selected135"]),
        "selected135_minus_selected270": sp.factor(M["selected135"] - M["selected270"]),
        "selected270_minus_Levi160": sp.factor(M["selected270"] - M["Levi160"]),
    }
    expected = {
        "W33_minus_selected135": -e*(e-1)*(429*e+190)/sp.Integer(871),
        "selected135_minus_selected270": -e*(e-1)*(235*e+609)/sp.Integer(18023),
        "selected270_minus_Levi160": -e*(e-1)*(7263*e**2+4897*e+257)/sp.Integer(14257),
    }
    for k in expected:
        assert sp.simplify(diffs[k]-expected[k]) == 0

    agg270_w33 = sp.factor(A["selected270"] - A["W33"])
    agg270_135 = sp.factor(A["selected270"] - A["selected135"])
    agg270_levi = sp.factor(A["selected270"] - A["Levi160"])
    assert agg270_w33 == e*(136*e**2+91*e+3)
    assert agg270_135 == e*(70*e**2+62*e+3)
    assert agg270_levi == -e*(81*e**3-82*e**2-100*e-9)
    cubic = 81*e**3-82*e**2-100*e-9
    assert float(cubic.subs(e,0)) < 0 and float(cubic.subs(e,1)) < 0
    crit = [complex(z) for z in sp.nroots(sp.diff(cubic,e))]
    assert not any(abs(z.imag)<1e-10 and 0 < z.real < 1 for z in crit)

    cross_poly = 81*e**3 - 12*e**2 - 38*e - 6
    roots = sorted(float(sp.re(z)) for z in sp.nroots(cross_poly) if abs(float(sp.im(z))) < 1e-12 and 0 < float(sp.re(z)) < 1)
    assert len(roots) == 1
    crossover = roots[0]

    propagation_db_per_m = 1.77
    edge_length_m = 0.01
    prop_db = propagation_db_per_m * edge_length_m
    detector = 0.98
    scenarios = {
        "low_loss_MZI_component_mix": {"switch_insertion_loss_db": 0.38, "switch_time_s": 14e-6},
        "fast_EO_component_mix": {"switch_insertion_loss_db": 1.05, "switch_time_s": 1.27e-9},
    }
    evaluated = {}
    for name,s in scenarios.items():
        hop_db = s["switch_insertion_loss_db"] + prop_db
        evaluated[name] = {
            "hop_loss_db": hop_db,
            "detector_efficiency": detector,
            "graphs": {g: metrics(sh, hop_db, detector, s["switch_time_s"]) for g,sh in SHELLS.items()}
        }

    out = {
        "pass": 4652,
        "shell_profiles": SHELLS,
        "symbolic": {
            "aggregate_polynomials": {k:str(v) for k,v in A.items()},
            "normalized_delivery_order_for_0_eta_1": "W33 > selected135 > selected270 > Levi160",
            "normalized_difference_factorizations": {k:str(v) for k,v in diffs.items()},
            "aggregate_selected270_order": "selected270 > W33, selected135, and Levi160 for every 0<eta<=1",
            "selected135_vs_Levi160_aggregate_crossover_eta": crossover,
            "pareto_statement": "W33 is loss/latency-optimal per destination under identical hop physics; selected270 is aggregate-address-throughput and connectivity dominant. No single scalar winner exists without a workload objective."
        },
        "literature_component_benchmarks": {
            "propagation": "1.77 dB/m anneal-free SiN waveguide loss (Bose et al., Light Sci Appl 2024); illustrative edge length 1 cm",
            "switch_low_loss": "0.38 dB insertion loss, 14 us switching (Nature Communications 2024 scalable silicon photonic chip)",
            "switch_fast": "1.04-1.06 dB insertion loss, 0.43/1.27 ns switching (Zhong et al., npj Nanophotonics 2024); model uses 1.05 dB and 1.27 ns",
            "detector": "98% SNSPD system detection efficiency benchmark (Hu et al. 2020 / Optics Express)",
            "warning": "These components were not demonstrated as one integrated stack; numbers are sensitivity anchors only."
        },
        "benchmark_evaluation": evaluated,
        "phase_error_boundary": "No universal per-hop phase-error number is assigned. A common multiplicative coherence factor can be absorbed into eta; architecture-specific coherent error needs a concrete circuit/layout measurement.",
        "theorem": "The routing comparison is Pareto, not scalar: for any common lossy hop, W33 strictly maximizes mean destination transmission while selected270 strictly maximizes aggregate delivered-destination score among the four exact shell profiles.",
        "boundary": "Graph-shell plus component-sensitivity model only; no measured Holonet hardware superiority is claimed."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
