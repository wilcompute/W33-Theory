"""Run parameter sweep for small GBS instances and record KL metrics."""

import json
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo))
from scripts.quantum_photonics.run_gbs import (build_interferometer,
                                               compute_exact_probs_fock,
                                               kl_between_empirical_and_exact,
                                               sample_gbs)

modes_list = [2, 3, 4]
squeezings = [0.3, 0.6, 0.9]
shots = 200
cutoff = 6
results = []
for modes in modes_list:
    for r in squeezings:
        U = build_interferometer(modes, seed=42)
        exact = compute_exact_probs_fock(modes, r, U, cutoff=cutoff)
        samples_gauss = sample_gbs(modes, r, U, backend="gaussian", shots=shots)
        samples_fock = sample_gbs(
            modes, r, U, backend="fock", shots=shots, cutoff=cutoff
        )
        kl_gauss = kl_between_empirical_and_exact(samples_gauss, exact, cutoff=cutoff)
        kl_fock = kl_between_empirical_and_exact(samples_fock, exact, cutoff=cutoff)
        results.append(
            {
                "modes": modes,
                "squeezing": r,
                "shots": shots,
                "kl_gauss": kl_gauss,
                "kl_fock": kl_fock,
            }
        )
        print("modes", modes, "r", r, "kl_gauss", kl_gauss, "kl_fock", kl_fock)

open("bundles/v23_toe_finish/v23/gbs_sweep_results.json", "w").write(
    json.dumps(results, indent=2)
)
print("Wrote bundles/v23_toe_finish/v23/gbs_sweep_results.json")
