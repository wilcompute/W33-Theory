#!/usr/bin/env python3
"""Pass 3283: regenerate and summarize the four exact execution fronts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "PART_BT3274_BT3285_TWISTED_ROM_RUNTIME_RESET_source_summary.json"
JOBS = [
 ("bt3274_3275_twisted_port_local_system.py","PART_BT3274_BT3275_TWISTED_PORT_LOCAL_SYSTEM_results.json"),
 ("bt3276_3277_independent_curvature_quotient.py","PART_BT3276_BT3277_INDEPENDENT_CURVATURE_QUOTIENT_results.json"),
 ("bt3278_3279_runtime_universe_firewall.py","PART_BT3278_BT3279_RUNTIME_UNIVERSE_FIREWALL_results.json"),
 ("bt3280_3281_constrained_reset_semigroup.py","PART_BT3280_BT3281_CONSTRAINED_RESET_SEMIGROUP_results.json"),
]


def main():
    artifacts = []
    for script, output in JOBS:
        subprocess.run([sys.executable, str(ROOT/"analysis"/script)], cwd=ROOT, check=True)
        path = DATA/output
        blob = path.read_bytes()
        artifacts.append({"script":script,"output":output,"sha256":hashlib.sha256(blob).hexdigest(),"bytes":len(blob)})
    loaded = {row["output"]:json.loads((DATA/row["output"]).read_text()) for row in artifacts}
    twisted = loaded[JOBS[0][1]]
    quotient = loaded[JOBS[1][1]]
    runtime = loaded[JOBS[2][1]]
    reset = loaded[JOBS[3][1]]
    payload = {
      "schema":"w33.pass3274_3285.source_summary.v1",
      "status":"SOURCE_EXACT_FOUR_FRONT_CLOSURE",
      "artifacts":artifacts,
      "checks":{
        "twisted_h1":twisted["controls"][1]["dim_H1"],
        "quotient_states":quotient["quotient_states"],
        "initial_quotient_states":quotient["initial_quotient_states"],
        "runtime_status":runtime["status"],
        "unauthorized_rank_floor":reset["global_unauthorized_rank_floor"],
        "authorized_reset_length":reset["authorized_reset"]["shortest_word_length"],
      },
      "prior_front":"PR #246 already carries the complete 1/194 + 2 baseline correction surface; this packet does not duplicate it.",
      "boundary":"Source regeneration is not observed workflow, PDF, RTL, synthesis, placement, timing, physical, optical or laboratory evidence."
    }
    assert payload["checks"]["twisted_h1"] == 870
    assert payload["checks"]["quotient_states"] == 876
    assert payload["checks"]["initial_quotient_states"] == 770
    assert payload["checks"]["unauthorized_rank_floor"] == 3
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps(payload["checks"],sort_keys=True))

if __name__ == "__main__": main()
