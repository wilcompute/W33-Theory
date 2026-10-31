"""Pass 70 Track C: partition-function / holographic-transition witness."""
from __future__ import annotations

import json
import math
from pathlib import Path


def main() -> None:
    lambda2 = (1 + math.sqrt(97)) / 2
    lambda3 = 3
    beta_c = math.log(40 / 15) / (lambda2 - lambda3)
    t_c = 1 / beta_c
    t_holo = 1 / 4

    payload = {
        "track": "C",
        "title": "W33 partition function and holographic transition witness",
        "lambda2": lambda2,
        "lambda3": lambda3,
        "beta_c": beta_c,
        "T_c": t_c,
        "T_holo": t_holo,
        "sector_ratio": "40:9",
        "predicted_HOM_visibility_drop": "40x suppression to 1/40",
        "BTZ_horizon_radius_claim": math.sqrt(97) / 8,
    }

    out = Path("w33_pass70_trackC_partition.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
