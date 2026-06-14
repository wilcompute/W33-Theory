#!/usr/bin/env bash
set -euo pipefail

# BT999 — apply R3 edgewise/fat-tower paper integrators and verify builds.
# Run from a full repository checkout.

python tools/integrate_bt990_r3_fat_tower_w33.py
python tools/integrate_bt990_r3_fat_tower_holonet.py
python tools/integrate_bt990_open_frontiers.py
python tools/integrate_bt996_r3_edgewise_hodge_stack_w33.py
python tools/integrate_bt996_holonet_edgewise_hodge.py

printf '\nMarker check:\n'
grep -n "BT990_R3_FAT_TOWER_INSERT\|BT996_R3_EDGEWISE_HODGE_STACK_INSERT" w33_paper.tex
grep -n "BT990_HOLONET_R3_FAT_TOWER_POINTER\|BT996_HOLONET_EDGEWISE_HODGE_POINTER" photonic_holonet.tex
grep -n "BT990_R3_FAT_TOWER_STATUS" OPEN_FRONTIERS.md

mkdir -p data
python - <<'PY'
import json
from pathlib import Path
markers = {
    "w33_paper.tex": ["BT990_R3_FAT_TOWER_INSERT", "BT996_R3_EDGEWISE_HODGE_STACK_INSERT"],
    "photonic_holonet.tex": ["BT990_HOLONET_R3_FAT_TOWER_POINTER", "BT996_HOLONET_EDGEWISE_HODGE_POINTER"],
    "OPEN_FRONTIERS.md": ["BT990_R3_FAT_TOWER_STATUS"],
}
out = {"theorem": "BT999 integrator marker verification", "markers": {}}
for path, wanted in markers.items():
    text = Path(path).read_text(encoding="utf-8")
    out["markers"][path] = {m: (m in text) for m in wanted}
Path("data/bt999_integrator_marker_check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
PY

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error w33_paper.tex
  latexmk -pdf -interaction=nonstopmode -halt-on-error photonic_holonet.tex
else
  echo "latexmk not found; marker verification completed, compile skipped."
fi
