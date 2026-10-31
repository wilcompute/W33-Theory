"""Pass 72 master runner: executes Tracks G, H, I and validates outputs."""
from __future__ import annotations

import importlib
import json
from pathlib import Path

TRACKS = [
    ("w33_pass72_trackG_yang_mills_gap", "w33_pass72_trackG_yang_mills_gap.json"),
    ("w33_pass72_trackH_ckm_matrix", "w33_pass72_trackH_ckm_matrix.json"),
    ("w33_pass72_trackI_koide_formula", "w33_pass72_trackI_koide_formula.json"),
]


def main() -> None:
    outputs = {}
    for module_name, out_file in TRACKS:
        mod = importlib.import_module(module_name)
        mod.main()
        outputs[out_file] = json.loads(Path(out_file).read_text())

    G = outputs["w33_pass72_trackG_yang_mills_gap.json"]
    H = outputs["w33_pass72_trackH_ckm_matrix.json"]
    I = outputs["w33_pass72_trackI_koide_formula.json"]

    assert G["delta_graph_units"] == 6.0
    assert H["spread_decomposition"]["total_spreads"] == 27
    assert 0.0 < I["koide_Q"] < 1.0


if __name__ == "__main__":
    main()
