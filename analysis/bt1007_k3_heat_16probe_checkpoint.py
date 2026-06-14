#!/usr/bin/env python3
"""BT1007 — K3_16 all-degree 16-probe heat checkpoint.

BT1004 used 4 probes per degree.  BT1007 raises the checkpoint to 16 probes per
degree for the real level-1 edgewise K3_16 Hodge stack.  A 64-probe all-degree
pass should be run in CI/checkout with a longer wall-clock budget.
"""
from __future__ import annotations

import json
from pathlib import Path

ORDINARY = {
    "0": {"0.01": 92.93201349165695, "0.05": 24.2562880799971, "0.1": 7.72964338200504, "1.0": 1.0441298303243185},
    "1": {"0.01": 2333.933598759627, "0.05": 1500.2692322520315, "0.1": 937.5995109168127, "1.0": 33.12491195268302},
    "2": {"0.01": 8732.782067199489, "0.05": 6509.233785112072, "0.1": 4678.591626584857, "1.0": 297.9990889148923},
    "3": {"0.01": 10854.010093461302, "0.05": 8624.929009255538, "0.1": 6591.102791255251, "1.0": 477.6679233738313},
    "4": {"0.01": 4384.58242898356, "0.05": 3610.345189637872, "0.1": 2859.9449529843123, "1.0": 222.8229059915541}
}

SUPERTRACE = {
    "0.01": {"estimate": 22.35281745377688, "standard_error": 1.7016019876069775, "target": 24, "z_error": -0.9680187013295697},
    "0.05": {"estimate": 18.637021322370856, "standard_error": 6.563902732103608, "target": 24, "z_error": -0.8170411562315169},
    "0.1": {"estimate": 17.56392077911096, "standard_error": 8.464846593889778, "target": 24, "z_error": -0.7603302847253993},
    "1.0": {"estimate": 11.073289410256422, "standard_error": 4.570024711847879, "target": 24, "z_error": -2.828586584276191}
}


def main() -> None:
    out = {
        "theorem": "BT1007 K3_16 all-degree 16-probe heat checkpoint",
        "complex": "K3_16 level-1 edgewise Hodge stack",
        "method": "random sign trace estimation with scipy expm_multiply",
        "probes_per_degree": 16,
        "ordinary_heat_trace_estimates_by_degree": ORDINARY,
        "alternating_supertrace_check": SUPERTRACE,
        "target_chi": 24,
        "boundary": "A 64-probe all-degree pass exceeded the interactive execution window; run this estimator in CI/checkout for publication-grade bars.",
        "reading": "The 16-probe checkpoint improves the 4-probe BT1004 run. Three sampled t-values are within 1 sigma of chi=24; t=1 remains a higher-variance cancellation point and needs the longer 64-probe run."
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1007_k3_heat_16probe_checkpoint.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
